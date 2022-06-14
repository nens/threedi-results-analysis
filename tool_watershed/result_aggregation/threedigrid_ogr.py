from typing import Union

from threedigrid.admin.nodes.models import Nodes, Cells
from threedigrid.admin.lines.models import Lines
from threedigrid.admin.utils import KCUDescriptor

KCU_DICT = KCUDescriptor()
KCU_DICT._descr[-9999] = 'unknown'  # to deal with the dummy flowline/cell/node that has coords [nan, nan, nan,
# nan] and kcu -9999

NODE_TYPE_DICT = {
    1: '2D surface water',
    2: '2D groundwater',
    3: '1D without storage',
    4: '1D with storage',
    5: '2D surface water boundary',
    6: '2D groundwater boundary',
    7: '1D boundary'
}

import numpy as np
from osgeo import ogr
from osgeo import osr


def threedigrid_to_ogr(threedigrid_src: Union[Nodes, Cells, Lines],
                       tgt_ds: ogr.DataSource,
                       attributes: dict = None,
                       attr_data_types: dict = None
                       ):
    """
    Create a ogr target_node_layer from the coordinates of threedigrid Nodes, Cells, or Lines with custom attributes

    :param threedigrid_src: threedigrid Nodes, Cells, or Lines object
    :param tgt_ds: ogr Datasource
    :param attributes: {attribute name: list of values}
    :param attr_data_types: {attribute name: ogr data type}
    :param epsg: EPSG code
    :return: ogr Datasource
    """
    default_attributes = {}
    default_attr_types = {}
    if attributes is None:
        attributes = dict()
    if attr_data_types is None:
        attr_data_types = dict()
    if isinstance(threedigrid_src, Nodes):
        src_type = Nodes
        coords = threedigrid_src.coordinates
        out_layer_name = 'node'
        out_geom_type = ogr.wkbPoint
    if isinstance(threedigrid_src, Cells):
        src_type = Cells
        coords = threedigrid_src.cell_coords
        out_layer_name = 'cell'
        out_geom_type = ogr.wkbPolygon
    if isinstance(threedigrid_src, Lines):
        src_type = Lines
        coords = threedigrid_src.line_coords
        out_layer_name = 'flowline'
        out_geom_type = ogr.wkbLineString
        default_attributes['id'] = threedigrid_src.id.astype(int)
        default_attr_types['id'] = ogr.OFTInteger
        if threedigrid_src.has_1d:
            default_attributes['spatialite_id'] = threedigrid_src.content_pk
            default_attr_types['spatialite_id'] = ogr.OFTInteger
            default_attributes['content_type'] = threedigrid_src.content_type
            default_attr_types['content_type'] = ogr.OFTString
        default_attributes['kcu'] = threedigrid_src.kcu
        default_attr_types['kcu'] = ogr.OFTInteger
        default_attributes['kcu_description'] = np.vectorize(KCU_DICT.get, otypes=[str])(threedigrid_src.kcu)
        default_attr_types['kcu_description'] = ogr.OFTString

    if isinstance(threedigrid_src, Cells) or isinstance(threedigrid_src, Nodes):
        default_attributes['id'] = threedigrid_src.id.astype(int)
        default_attr_types['id'] = ogr.OFTInteger
        if isinstance(threedigrid_src, Nodes) and threedigrid_src.has_1d:
            default_attributes['spatialite_id'] = threedigrid_src.content_pk
            default_attr_types['spatialite_id'] = ogr.OFTInteger
        default_attributes['node_type'] = threedigrid_src.node_type
        default_attr_types['node_type'] = ogr.OFTInteger
        print(threedigrid_src.node_type)
        default_attributes['node_type_description'] = np.vectorize(NODE_TYPE_DICT.get, otypes=[str])(
            threedigrid_src.node_type)
        default_attr_types['node_type_description'] = ogr.OFTString
        if isinstance(threedigrid_src, Cells):
            default_attributes['z_coordinate'] = threedigrid_src.z_coordinate
            default_attr_types['z_coordinate'] = ogr.OFTReal

    all_attributes = default_attributes
    all_attributes.update(attributes)
    all_attr_data_types = default_attr_types
    all_attr_data_types.update(attr_data_types)

    # create output layer
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(int(threedigrid_src.epsg_code))
    out_layer = tgt_ds.CreateLayer(out_layer_name, srs, geom_type=out_geom_type)

    # create fields
    for attr in all_attributes.keys():
        field = ogr.FieldDefn(attr, all_attr_data_types[attr])
        out_layer.CreateField(field)

    feature_defn = out_layer.GetLayerDefn()

    # create features
    for i in range(threedigrid_src.count):
        if (not np.all(np.isfinite(coords[:, i]))) or (
                not np.all(coords[:, i] != -9999)):  # skip if coordinates are invalid
            continue
        else:
            # create feature geometry
            feature = ogr.Feature(feature_defn)
            geom = ogr.Geometry(out_geom_type)
            if src_type == Nodes:
                x, y = coords[:, i]
                geom.SetPoint(0, x, y)
                feature.SetGeometry(geom)
            elif src_type == Lines:
                x0, y0, x1, y1 = coords[:, i]
                geom.AddPoint(float(x0), float(y0))
                geom.AddPoint(float(x1), float(y1))
                feature.SetGeometry(geom)
            elif src_type == Cells:
                xmin, ymin, xmax, ymax = coords[:, i]
                geom_ring = ogr.Geometry(ogr.wkbLinearRing)
                geom_ring.AddPoint(xmin, ymin)
                geom_ring.AddPoint(xmin, ymax)
                geom_ring.AddPoint(xmax, ymax)
                geom_ring.AddPoint(xmax, ymin)
                geom_ring.AddPoint(xmin, ymin)
                geom.AddGeometry(geom_ring)
                if not geom.IsValid():
                    continue
                elif geom.IsEmpty():
                    continue
                else:
                    feature.SetGeometry(geom)

            # create feature attributes
            for attr in all_attributes.keys():
                val = all_attributes[attr][i]
                if all_attr_data_types[attr] in [ogr.OFTInteger]:
                    val = int(val)
                elif all_attr_data_types[attr] in [ogr.OFTString]:
                    if isinstance(val, bytes):
                        val = val.decode('utf-8')
                    else:
                        val = str(val)
                elif all_attr_data_types[attr] in [ogr.OFTReal]:
                    if np.isnan(val):
                        val = None
                if val is not None:
                    feature[attr] = val

            # create the actual feature
            out_layer.CreateFeature(feature)
            feature = None
    return
