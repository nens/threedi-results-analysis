# (c) Nelen & Schuurmans, see LICENSE.rst.
from typing import Tuple, Sequence, List

from osgeo import gdal, osr
from pathlib import Path
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsCoordinateTransform
from qgis.core import QgsProject
from qgis.core import QgsRasterBandStats
import numpy as np

gdal.UseExceptions()
osr.UseExceptions()


def get_coord_transformation_instance(src_epsg, dest_epsg):
    """
    :param src_epsg: epsg code of the source geometry
    :param dest_epsg: epsg code to transform to
    """
    src_crs = QgsCoordinateReferenceSystem(int(src_epsg))
    dest_crs = QgsCoordinateReferenceSystem(int(dest_epsg))
    return QgsCoordinateTransform(src_crs, dest_crs, QgsProject.instance())


def closest_point_on_segment(p, a, b):
    ap = p - a
    ab = b - a
    ab_squared = np.dot(ab, ab)
    # Length ab vector is zero, or: segment is a point
    if ab_squared == 0:
        return a
    # https://en.wikipedia.org/wiki/Scalar_projection
    t = max(min(np.dot(ap, ab) / ab_squared, 1), 0)
    assert t <= 1
    assert t >= 0
    return a + t * ab


def distance_to_polyline(px, py, x_data, y_data):
    # Closest projected point
    min_dist = float('inf')
    # Closest data point
    closest = None
    point = np.array([px, py])
    for i in range(len(x_data) - 1):
        a = np.array([x_data[i], y_data[i]])
        b = np.array([x_data[i+1], y_data[i+1]])
        proj = closest_point_on_segment(point, a, b)
        dist = np.linalg.norm(proj - point)
        if dist < min_dist:
            min_dist = dist
            closest = a if np.linalg.norm(point-a) < np.linalg.norm(point-b) else b
    return min_dist, closest


def inbetween_polylines(px, py, x_data, y1_data, y2_data):
    if px < x_data[0] or px > x_data[-1]:
        return False

    y1 = np.interp(px, x_data, y1_data)
    y2 = np.interp(px, x_data, y2_data)
    return (min(y1, y2) <= py <= max(y1, y2))


def below_polyline(px, py, x_data, y_data):
    if px < x_data[0] or px > x_data[-1]:
        return False

    y = np.interp(px, x_data, y_data)
    return py < y


def closest_point_on_polyline(px, py, x_data, y_data):
    dists = (x_data - px)**2 + (y_data - py)**2
    idx = np.argmin(dists)
    return x_data[idx], y_data[idx], idx


def multiband_raster_min_max(layer) -> Tuple[float, float]:
    """Return the min and max values across all bands"""
    provider = layer.dataProvider()
    band_count = provider.bandCount()

    global_min = float("inf")
    global_max = float("-inf")

    for band in range(1, band_count + 1):
        stats = provider.bandStatistics(
            band,
            QgsRasterBandStats.Min | QgsRasterBandStats.Max
        )
        global_min = min(global_min, stats.minimumValue)
        global_max = max(global_max, stats.maximumValue)

    return global_min, global_max


def get_shared_extent_size(
    raster1: gdal.Dataset,
    raster2: gdal.Dataset
) -> Tuple[int, int]:
    """
    Compute the pixel dimensions (RasterXSize, RasterYSize) of the shared extent
    between two rasters.

    Parameters
    ----------
    raster1 : gdal.Dataset
        The first raster dataset.
    raster2 : gdal.Dataset
        The second raster dataset.

    Returns
    -------
    Optional[Tuple[int, int]]
        A tuple (x_size, y_size) representing the number of columns and rows
        in the shared extent. Returns `None` if the rasters do not overlap.
    """
    check_raster_properties_are_equal(raster1, raster2)

    extent1 = get_extent(raster1)
    extent2 = get_extent(raster2)
    shared_extent = get_shared_extent(extent1, extent2)

    gt = raster1.GetGeoTransform()
    pixel_width = gt[1]
    pixel_height = abs(gt[5])  # Use absolute value

    ulx, uly, lrx, lry = shared_extent

    x_size = int(round((lrx - ulx) / pixel_width))
    y_size = int(round((uly - lry) / pixel_height))

    return x_size, y_size


def mask(source: str | Path, mask: str | Path, output: str | Path):
    """
    Masks source raster with mask: sets all pixels in source to nodata
    wherever mask has nodata. Supports single- and multi-band rasters
    (with the same number of bands).
    """
    # Open source and mask datasets
    source_ds = gdal.Open(str(source))
    mask_ds = gdal.Open(str(mask))

    check_raster_properties_are_equal(source_ds, mask_ds)

    bands = source_ds.RasterCount
    mask_bands = mask_ds.RasterCount
    if bands != mask_bands:
        raise ValueError(f"Source has {bands} bands, mask has {mask_bands} bands")

    # Prepare output dataset
    creation_options = [
        "COMPRESS=DEFLATE",
        "PREDICTOR=2",
        "ZLEVEL=9",
        "TILED=YES",
        "BLOCKXSIZE=512",
        "BLOCKYSIZE=512"
    ]
    driver = gdal.GetDriverByName("GTiff")
    raster_x_size, raster_y_size = get_shared_extent_size(raster1=source_ds, raster2=mask_ds)
    out_ds = driver.Create(
        str(output),
        raster_x_size,
        raster_y_size,
        bands,
        source_ds.GetRasterBand(1).DataType,
        options=creation_options
    )
    out_ds.SetGeoTransform(source_ds.GetGeoTransform())
    out_ds.SetProjection(source_ds.GetProjection())

    # Process band by band
    for i in range(1, bands + 1):  # GDAL bands are 1-based
        source_band = source_ds.GetRasterBand(i)
        source_nodata = source_band.GetNoDataValue() or -9999

        mask_band = mask_ds.GetRasterBand(i if mask_bands > 1 else 1)
        mask_nodata = mask_band.GetNoDataValue()

        source_array, mask_array, gt = get_arrays(source_ds, mask_ds, band_raster1=i, band_raster2=i)

        # Apply masking
        source_masked = np.where(mask_array == mask_nodata, source_nodata, source_array)

        # Write out band
        out_band = out_ds.GetRasterBand(i)
        out_band.WriteArray(source_masked)
        out_band.SetNoDataValue(source_nodata)
        out_band.FlushCache()


def get_extent(raster: gdal.Dataset) -> List[float]:
    """
    Compute the spatial extent of a GDAL raster dataset.

    Parameters
    ----------
    raster : gdal.Dataset
        The GDAL raster dataset for which to compute the extent.

    Returns
    -------
    List[float]
        A list representing the raster extent in the format:
        [ulx, uly, lrx, lry], where:
        - ulx: upper-left x coordinate
        - uly: upper-left y coordinate
        - lrx: lower-right x coordinate
        - lry: lower-right y coordinate
    """
    gt = raster.GetGeoTransform()
    ulx = gt[0]
    uly = gt[3]
    lrx = gt[0] + (raster.RasterXSize * gt[1])
    lry = gt[3] + (raster.RasterYSize * gt[5])  # '+' because gt[5] is negative
    return [ulx, uly, lrx, lry]


def get_shared_extent(extent1: Sequence[float], extent2: Sequence[float]) -> List[float]:
    """
    Compute the shared (overlapping) extent between two raster extents.

    Parameters
    ----------
    extent1 : Sequence[float]
        The extent of the first raster, typically in the format [ulx, uly, lrx, lry],
        where:
        - ulx: upper-left x coordinate
        - uly: upper-left y coordinate
        - lrx: lower-right x coordinate
        - lry: lower-right y coordinate
    extent2 : Sequence[float]
        The extent of the second raster, in the same format as extent1.

    Returns
    -------
    List[float]
        The shared extent [ulx, uly, lrx, lry] that represents the overlapping area
        between both extents.

    Notes
    -----
    - If the extents do not overlap, the result may be invalid (e.g., ulx > lrx or uly < lry).
      You may wish to add validation logic depending on your use case.
    """
    ulx = max(extent1[0], extent2[0])
    uly = min(extent1[1], extent2[1])
    lrx = min(extent1[2], extent2[2])
    lry = max(extent1[3], extent2[3])

    # Check for non-overlapping extents
    if ulx >= lrx or uly <= lry:
        raise ValueError("Extents do not overlap")

    return [ulx, uly, lrx, lry]


def replace_no_data_values(raster: gdal.Dataset, raster_array: np.ndarray) -> np.ndarray:
    """
    Replace 'no data' values in a raster array with zeros.

    Parameters
    ----------
    raster : gdal.Dataset
        The GDAL raster dataset from which to retrieve the NoData value.
    raster_array : np.ndarray
        The raster data array where NoData values will be replaced.

    Returns
    -------
    np.ndarray
        The modified raster array with NoData values replaced by 0.
    """
    ndv = raster.GetRasterBand(1).GetNoDataValue()
    raster_array[np.where(raster_array == ndv)] = 0
    return raster_array


def get_authority_code(raster: gdal.Dataset) -> str | None:
    """
    Return authority code (e.g. EPSG:28992) for given raster
    Returns None if no projection is defined
    """
    wkt = raster.GetProjection()
    if not wkt:
        return None  # no projection defined

    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt)

    if srs.IsGeographic():
        key = "GEOGCS"
    else:
        key = "PROJCS"

    code = srs.GetAuthorityCode(key)
    auth = srs.GetAuthorityName(key)

    if code and auth:
        return f"{auth}:{code}"
    return None


def check_raster_properties_are_equal(raster1: gdal.Dataset, raster2: gdal.Dataset) -> None:
    """
    Verify that two raster datasets have matching spatial properties.

    This function compares pixel size, skew, and coordinate reference system (CRS)
    between two GDAL raster datasets. If any of these properties differ, a
    `ValueError` is raised.

    Parameters
    ----------
    raster1 : gdal.Dataset
        The reference raster dataset.
    raster2 : gdal.Dataset
        The raster dataset to compare against the reference.

    Raises
    ------
    ValueError
        If the rasters have different pixel sizes, pixel skews, or projections.

    Notes
    -----
    - The CRS is compared using EPSG authority codes via `get_authority_code()`,
      to avoid false mismatches due to minor metadata differences.
    """
    # Compare pixel size (resolution)
    if not (
            raster1.GetGeoTransform()[1] == raster2.GetGeoTransform()[1] and
            raster1.GetGeoTransform()[5] == raster2.GetGeoTransform()[5]
    ):
        raise ValueError("Input rasters have different pixel sizes")

    # Compare pixel skew
    if not (
            raster1.GetGeoTransform()[2] == raster2.GetGeoTransform()[2] and
            raster1.GetGeoTransform()[4] == raster2.GetGeoTransform()[4]
    ):
        raise ValueError("Input rasters have different pixel skew")

    # Compare coordinate reference systems (CRS)
    authority_code_raster1 = get_authority_code(raster1)
    authority_code_raster2 = get_authority_code(raster2)

    if authority_code_raster1 != authority_code_raster2:
        raise ValueError(
            f"Input rasters have different CRS "
            f"({authority_code_raster1} vs {authority_code_raster2})"
        )


def get_arrays(
        raster1: gdal.Dataset,
        raster2: gdal.Dataset,
        band_raster1: int = 1,
        band_raster2: int = 1,
) -> Tuple[np.ndarray, np.ndarray, tuple]:
    """
    Retrieve raster data arrays and a common GeoTransform for two rasters.

    If both rasters share the same spatial extent, their full arrays are read directly.
    Otherwise, both are clipped to their shared extent using GDAL's in-memory translation.

    Will raise error if raster properties are not equal, see `check_raster_properties_are_equal()`

    Parameters
    ----------
    raster1 : gdal.Dataset
        The first GDAL raster dataset.
    raster2 : gdal.Dataset
        The second GDAL raster dataset.
    band_raster1: int
        Band number for raster 1
    band_raster2: int
        Band number for raster 2

    Returns
    -------
    tuple of (np.ndarray, np.ndarray, tuple)
        A tuple containing:
        - raster1_array : np.ndarray
            The array of raster1 (either full or clipped to shared extent).
        - raster2_array : np.ndarray
            The array of raster2 (either full or clipped to shared extent).
        - gt : tuple
            The GeoTransform for the shared extent
            (upper_left_x, pixel_width, x_skew, upper_left_y, y_skew, pixel_height)
    """
    check_raster_properties_are_equal(raster1, raster2)
    raster1_extent = get_extent(raster1)
    raster2_extent = get_extent(raster2)

    if raster1_extent == raster2_extent:
        raster1_array = raster1.ReadAsArray(band_list=[band_raster1])
        raster2_array = raster2.ReadAsArray(band_list=[band_raster2])
        gt = raster1.GetGeoTransform()
    else:
        shared_extent = get_shared_extent(raster1_extent, raster2_extent)

        raster1_shared_extent = gdal.Translate('', raster1, format='MEM', projWin=shared_extent)
        raster1_array = raster1_shared_extent.ReadAsArray(band_list=[band_raster1])
        raster1_shared_extent = None

        raster2_shared_extent = gdal.Translate('', raster2, format='MEM', projWin=shared_extent)
        raster2_array = raster2_shared_extent.ReadAsArray(band_list=[band_raster2])
        raster2_shared_extent = None

        gt = list(raster1.GetGeoTransform())
        gt[0] = shared_extent[0]
        gt[3] = shared_extent[1]
        gt = tuple(gt)

    return raster1_array, raster2_array, gt
