"""
    functions for creation of QgsVectorLayers from 3di netCDF files
"""

from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, \
    QgsPoint
from PyQt4.QtCore import QVariant

from ..datasource.netcdf import get_node_mapping
from .user_messages import StatusProgressBar


def make_flowline_layer(ds, progress_bar=None):
    """Make a memory layer that contains all flow lines.

    Args:
        ds: NetcdfDataSource
        progress_bar: (StatusProgressBar) - progress bar instance for feedback
            about progress. This tool will make 100 steps

    Returns:
        (QgsVectorLayer) In memory layer with all lines
    """
    if progress_bar is None:
        progress_bar = StatusProgressBar(100, 'create flow line: ')

    progress_bar.increase_progress(0, "read data from netCDF")
    # Get relevant netCDF.Variables
    projection = ds.ds.variables['projected_coordinate_system']
    epsg = projection.epsg  # = 28992
    # Connections (2, nFlowLine):
    try:
        flowline_connection = ds.ds.variables['FlowLine_connection']
    except KeyError:
        # temporary fix for bug in netCDF export routine. Remove after May 2016
        flowline_connection = ds.ds.variables['flowline_connection']

    # FlowElem centers:
    flowelem_xcc = ds.ds.variables['FlowElem_xcc']  # in meters
    flowelem_ycc = ds.ds.variables['FlowElem_ycc']  # in meters

    # -1 probably because of fortran indexing
    flowline_p1 = flowline_connection[0, :].astype(int) - 1
    flowline_p2 = flowline_connection[1, :].astype(int) - 1

    # Point 1 of the connection
    x_p1 = flowelem_xcc[:][flowline_p1]
    y_p1 = flowelem_ycc[:][flowline_p1]

    # Point 2 of the connection
    x_p2 = flowelem_xcc[:][flowline_p2]
    y_p2 = flowelem_ycc[:][flowline_p2]

    progress_bar.increase_progress(10, "create memory layer")
    # create layer
    # "Point?crs=epsg:4326&field=id:integer&field=name:string(20)&index=yes"
    uri = "LineString?crs=epsg:{}&index=yes".format(
        epsg)
    vl = QgsVectorLayer(uri, "flowlines", "memory")
    pr = vl.dataProvider()

    # add fields
    pr.addAttributes([
        # This is the flowline index in Python (0-based indexing)
        # Important: this differs from the feature id which is flowline idx+1!!
        QgsField("flowline_idx", QVariant.Int),
        QgsField("inp_id", QVariant.Int),
        QgsField("spatialite_id", QVariant.Int),
        QgsField("type", QVariant.String, len=25)
        ])
    # tell the vector layer to fetch changes from the provider
    vl.updateFields()

    progress_bar.increase_progress(10, "create id mappings")
    # create inverse mapping
    flowid_to_inp_mapping = dict([(flowid, inp_id) for inp_id, flowid in
                                  ds.ds.variables['channel_mapping']])

    # create mapping of inp_id to spatialite_id and feature type
    inp_to_splt_mapping = {}
    for feature_type in ("v2_channel", "v2_pipe", "v2_culvert", "v2_weir",
                         "v2_orifice"):
        if feature_type in ds.id_mapping:
            for spatialite_id, inp_id in ds.id_mapping[feature_type].items():
                inp_to_splt_mapping[inp_id] = (feature_type, spatialite_id)

    progress_bar.increase_progress(20, "Prepare data")
    # add features
    features = []

    # TODO: because there is not (yet) distinction  between number of 2d
    # links and 1d-2d links, we will guess the numbers based on the fact that
    # only id mapping is available for all 1d links. (when numbers become
    # available, this code can be improved and optimized
    for i in range(flowline_connection.shape[1]):
        feat = QgsFeature()

        p1 = QgsPoint(x_p1[i], y_p1[i])
        p2 = QgsPoint(x_p2[i], y_p2[i])

        feat.setGeometry(QgsGeometry.fromPolyline([p1, p2]))

        inp_id = None
        spatialite_tbl = None
        spatialite_id = None

        try:
            inp_id = int(flowid_to_inp_mapping[i+1])
            spatialite_tbl, spatialite_id = inp_to_splt_mapping[inp_id]
        except KeyError:
            cat = ds.get_line_type(i)
            if cat == '1d':
                cat = '1d_2d'
            spatialite_tbl = cat

        feat.setAttributes([i, inp_id, spatialite_id, spatialite_tbl])

        features.append(feat)

    progress_bar.increase_progress(30, "append data to memory layer")
    pr.addFeatures(features)

    progress_bar.increase_progress(25, "update extent")
    # update layer's extent when new features have been added
    # because change of extent in provider is not propagated to the layer
    vl.updateExtents()

    progress_bar.increase_progress(5, "ready")
    return vl


def make_node_layer(ds, progress_bar=None):
    """Make a memory layer that contains all nodes.

    Args:
        ds: NetcdfDataSource
        progress_bar: (StatusProgressBar) - progress bar instance for feedback
            about progress. This tool will make 100 steps.

    Returns:
        (QgsVectorLayer) In memory layer with all points
    """
    if progress_bar is None:
        progress_bar = StatusProgressBar(100, 'create node layer: ')

    progress_bar.increase_progress(0, "read data from netCDF")
    # Get relevant netCDF.Variables
    projection = ds.ds.variables['projected_coordinate_system']
    epsg = projection.epsg  # = 28992
    # FlowElem centers:
    flowelem_xcc = ds.ds.variables['FlowElem_xcc']  # in meters
    flowelem_ycc = ds.ds.variables['FlowElem_ycc']  # in meters

    progress_bar.increase_progress(10, "create memory layer")
    # create layer
    # "Point?crs=epsg:4326&field=id:integer&field=name:string(20)&index=yes"
    uri = "Point?crs=epsg:{}&index=yes".format(
        epsg)
    vl = QgsVectorLayer(uri, "nodes", "memory")
    pr = vl.dataProvider()

    # add fields
    pr.addAttributes([
        # This is the node index in Python (0-based indexing)
        # Important: this differs from the feature id which is node idx+1!!
        QgsField("node_idx", QVariant.Int),
        QgsField("inp_id", QVariant.Int),
        QgsField("spatialite_id", QVariant.Int),
        QgsField("feature_type", QVariant.String, len=25),
        QgsField("node_type", QVariant.String, len=25)
        ])
    # tell the vector layer to fetch changes from the provider
    vl.updateFields()

    progress_bar.increase_progress(10, "create id mappings")
    # create inverse mapping
    node_idx_to_inp_id = dict([(flowid-1, inp_id) for inp_id, flowid in
                               ds.ds.variables['node_mapping']])

    # create mapping of inp_id to spatialite_id and feature type
    inp_to_splt_mapping = {}
    for feature_type in ("v2_connection_nodes", "v2_manhole",
                         "v2_1d_boundary_conditions"):
        if feature_type in ds.id_mapping:
            for spatialite_id, inp_id in ds.id_mapping[feature_type].items():
                inp_to_splt_mapping[inp_id] = (feature_type, spatialite_id)

    progress_bar.increase_progress(20, "Prepare data")
    # add features
    features = []
    for i in range(flowelem_xcc.shape[0]):
        feat = QgsFeature()

        p1 = QgsPoint(flowelem_xcc[i], flowelem_ycc[i])

        feat.setGeometry(QgsGeometry.fromPoint(p1))

        # Getting all node types, feature types, and whatnot:
        node_type = ds.get_node_type(i)
        inp_id = node_idx_to_inp_id.get(i, None)
        feature_type, spatialite_id = inp_to_splt_mapping.get(
            inp_id, (None, None))

        feat.setAttributes([i, inp_id, spatialite_id, feature_type, node_type])
        features.append(feat)
    progress_bar.increase_progress(30, "append data to memory layer")
    pr.addFeatures(features)

    progress_bar.increase_progress(25, "update extent")
    # update layer's extent when new features have been added
    # because change of extent in provider is not propagated to the layer
    vl.updateExtents()

    progress_bar.increase_progress(5, "ready")
    return vl


def make_pumpline_layer(nds):
    """Make a memory layer that contains all pumplines.

    Args:
        nds: netCDF Datasource
    """
    # Get relevant netCDF.Variables
    projection = nds.ds.variables['projected_coordinate_system']
    epsg = projection.epsg  # = 28992
    # Pumpline connections (2, jap1d):
    pumpline = nds.ds.variables['pump_mapping']
    # FlowElem centers:
    flowelem_xcc = nds.ds.variables['FlowElem_xcc']  # in meters
    flowelem_ycc = nds.ds.variables['FlowElem_ycc']  # in meters

    # -1 probably because of fortran indexing
    pumpline_p1 = pumpline[0, :].astype(int)  # - 1
    pumpline_p2 = pumpline[1, :].astype(int)  # - 1

    # TODO: Not very efficient, but this mapping is not needed anyway in the
    # future, so who cares?
    node_mapping = get_node_mapping(nds.ds)
    for i in range(pumpline.shape[1]):
        # Note: there is no need to subtract 1 from the index because the
        # node_mapping already does this for you
        pumpline_p1[i] = node_mapping.get(pumpline_p1[i], 0)
        pumpline_p2[i] = node_mapping.get(pumpline_p2[i], 0)

    # Point 1 of the connection
    x_p1 = flowelem_xcc[:][pumpline_p1]
    y_p1 = flowelem_ycc[:][pumpline_p1]

    # Point 2 of the connection
    x_p2 = flowelem_xcc[:][pumpline_p2]
    y_p2 = flowelem_ycc[:][pumpline_p2]

    # create layer
    # "Point?crs=epsg:4326&field=id:integer&field=name:string(20)&index=yes"
    uri = "LineString?crs=epsg:{}&index=yes".format(
        epsg)
    vl = QgsVectorLayer(uri, "pumplines", "memory")
    pr = vl.dataProvider()

    # add fields
    pr.addAttributes([
        # This is the flowline index in Python (0-based indexing)
        # Important: this differs from the feature id which is flowline idx+1!!
        QgsField("pumpline_idx", QVariant.Int),
        ])
    # tell the vector layer to fetch changes from the provider
    vl.updateFields()

    # add features
    features = []
    number_of_pumplines = pumpline.shape[1]
    for i in range(number_of_pumplines):
        fet = QgsFeature()

        p1 = QgsPoint(x_p1[i], y_p1[i])
        p2 = QgsPoint(x_p2[i], y_p2[i])

        fet.setGeometry(QgsGeometry.fromPolyline([p1, p2]))
        fet.setAttributes([i])
        features.append(fet)
    pr.addFeatures(features)

    # update layer's extent when new features have been added
    # because change of extent in provider is not propagated to the layer
    vl.updateExtents()

    return vl
