import numpy as np
from osgeo import ogr
from scipy.ndimage import gaussian_filter1d

ogr.UseExceptions()


def linestring_gaussian_smooth(line: ogr.Geometry, sigma: float = 1.0, sample_dist: float = 1.0):
    """Apply gaussian smoothing to an ogr Linestring.
    Also suitable for ring linestrings

    :param line: input linestring geometry
    :param sigma: higher sigma for smoother result
    :param sample_dist: lower sample_dist for smoother result
    :return: smoothed linestring geometry
    :rtype: ogr.Geometry
    """
    # based on stackoverflow.com/questions/15178146/line-smoothing-algorithm-in-python
    line.Segmentize(sample_dist)  # densify the input geometry with more vertices
    arr = np.array(line.GetPoints(nCoordDimension=2))
    x, y = arr.T
    out_line = ogr.Geometry(ogr.wkbLineString)
    line.FlattenTo2D()
    first_vertex = (x[0], y[0])
    last_vertex = (x[-1], y[-1])
    input_is_ring = False
    if line.IsRing() or first_vertex == last_vertex:
        input_is_ring = True
    if input_is_ring:
        mode = "wrap"
    else:
        mode = "nearest"
        out_line.AddPoint(x[0], y[0])  # to ensure start vertex remains in same location

    # equally spaced numbers between 0 en 1 for each vertex
    t = np.linspace(0, 1, len(x))
    # equally spaced numbers between 0 en 1, every {sample_dist} meter
    t2 = np.linspace(0, 1, int(line.Length() / sample_dist))

    x2 = np.interp(t2, t, x)
    y2 = np.interp(t2, t, y)
    x3 = gaussian_filter1d(x2, sigma, mode=mode)
    y3 = gaussian_filter1d(y2, sigma, mode=mode)
    x4 = np.interp(t, t2, x3)
    y4 = np.interp(t, t2, y3)

    for i in range(x4.shape[0]):
        out_line.AddPoint(x4[i], y4[i])

    if input_is_ring:
        point = out_line.GetPoint(0)
        out_line.AddPoint(*point)
    else:
        out_line.AddPoint(x[-1], y[-1])

    return out_line


def polygon_gaussian_smooth(polygon: ogr.Geometry, sigma=1.0, sample_dist=1.0):
    """Apply gaussian smoothing to an ogr Linestring.
    Also suitable for ring linestrings

    :param polygon: input Polygon geometry
    :param sigma: higher sigma for smoother result
    :param sample_dist: lower sample_dist for smoother result
    :return: smoothed polygon geometry
    :rtype: ogr.Geometry
    """
    if polygon.GetGeometryType() not in [ogr.wkbPolygon, ogr.wkbPolygon25D]:
        return polygon
    else:
        exterior_ring = polygon.GetGeometryRef(0)
        exterior_ring_smoothed = linestring_gaussian_smooth(exterior_ring, sigma, sample_dist)
        exterior_ring_smoothed.FlattenTo2D()
        result = ogr.Geometry(ogr.wkbPolygon)
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for point in exterior_ring_smoothed.GetPoints():
            ring.AddPoint(*point)
        result.AddGeometry(ring)
        return result


def layer_gaussian_smooth(datasource: ogr.DataSource, layer_name: str, sigma=1.0, sample_dist=1.0):
    """
    Apply gaussian smoothing to all features in a layer
    Only affects (single) Polygon and (single) LineString geometries
    :param datasource:
    :param layer_name:
    :param sigma: higher sigma for smoother result
    :param sample_dist: lower sample_dist for smoother result
    :return:
    """
    layer = datasource.GetLayerByName(layer_name)
    layer.ResetReading()
    for feature in layer:
        geom = feature.GetGeometryRef()
        if geom.GetGeometryType() in [ogr.wkbLineString, ogr.wkbLineString25D]:
            if geom.Length() > sample_dist:
                smooth_geom = linestring_gaussian_smooth(geom, sigma=sigma, sample_dist=sample_dist)
                feature.SetGeometry(smooth_geom)
                layer.SetFeature(feature)
        elif geom.GetGeometryType() in [ogr.wkbPolygon, ogr.wkbPolygon25D]:
            if geom.Boundary().Length() > sample_dist:
                smooth_geom = polygon_gaussian_smooth(geom, sigma=sigma, sample_dist=sample_dist)
                feature.SetGeometry(smooth_geom)
                layer.SetFeature(feature)
    return
