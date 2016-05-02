

from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsPoint, \
    QgsMapLayerRegistry
from PyQt4.QtCore import QVariant

from user_messages import pop_up_info, StatusProgressBar
from ..views.tool_dialog import ToolDialogWidget

from ..datasource.netcdf import get_channel_mapping, get_node_mapping



def make_flowline_layer(ds, progress_bar=None):
    """Make a memory layer that contains all flow lines.

    Args:
        ds: NetcdfDataSource
        progress_bar: (StatusProgressBar) - progress bar instance for feedback over progress.
                        this tool will make 100 steps

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
        QgsField("splt_id", QVariant.Int),
        QgsField("type", QVariant.String, len=25)
        ])
    vl.updateFields()  # tell the vector layer to fetch changes from the provider

    progress_bar.increase_progress(10, "create id mappings")
    # create inverse mapping
    flowid_to_inp_mapping = dict([(flowid, inp_id) for inp_id, flowid in ds.ds.variables['channel_mapping']])

    # create mapping of inp_id to spatialite_id and feature type
    inp_to_splt_mapping = {}
    for feature_type in ("v2_channel", "v2_pipe", "v2_culvert", "v2_weir", "v2_orifice"):
        if  feature_type in ds.id_mapping:
            for splt_id, inp_id in ds.id_mapping[feature_type].items():
                inp_to_splt_mapping[inp_id] = (feature_type, splt_id)


    progress_bar.increase_progress(20, "Prepare data")
    # add features
    features = []
    # Order of links in netCDF is:
    # - 2d links (x and y) (nr: part of ds.ds.nFlowElem2d)
    # - 1d links (nr: ds.ds.nFlowElem1d)
    # - 1d-2d links (nr: part of ds.ds.nFlowElem2d)
    # - 2d bound links (nr: ds.ds.nFlowElem2dBounds)
    # - 1d bound links (nr: ds.ds.nFlowElem1dBounds)
    # because there is not (yet) distinction  between number of 2d links and 1d-2d links,
    # we will guess the numbers based on the fact that only id mapping is available
    # for all 1d links. (when numbers become available, this code can be improved
    # and optimized

    cat = '2d_links'
    start_2d_bounds = flowline_connection.shape[1] - ds.ds.nFlowLine2dBounds - ds.ds.nFlowLine1dBounds
    start_1d_bounds = flowline_connection.shape[1] - ds.ds.nFlowLine1dBounds
    for i in range(flowline_connection.shape[1]):
        feat = QgsFeature()

        p1 = QgsPoint(x_p1[i], y_p1[i])
        p2 = QgsPoint(x_p2[i], y_p2[i])

        feat.setGeometry(QgsGeometry.fromPolyline([p1, p2]))

        inp_id = None
        splt_tbl = None
        splt_id = None

        try:
            inp_id = int(flowid_to_inp_mapping[i+1])
            splt_tbl, splt_id = inp_to_splt_mapping[inp_id]
            cat = '1dlink'
        except KeyError:
            if cat == '1dlink':
                cat = '1d_2d_link'
            if i == start_2d_bounds:
                cat = '2d_bound_link'
            if i == start_1d_bounds:
                cat = '1d_bound_link'
            splt_tbl = cat

        feat.setAttributes([i, inp_id, splt_id, splt_tbl])

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
        progress_bar: (StatusProgressBar) - progress bar instance for feedback over progress.
                this tool will make 100 steps

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
        QgsField("splt_id", QVariant.Int),
        QgsField("type", QVariant.String, len=25)
        ])
    vl.updateFields()  # tell the vector layer to fetch changes from the provider

    progress_bar.increase_progress(10, "create id mappings")
    # create inverse mapping
    flowid_to_inp_mapping = dict([(flowid-1, inp_id) for inp_id, flowid in ds.ds.variables['node_mapping']])

    # create mapping of inp_id to spatialite_id and feature type
    inp_to_splt_mapping = {}
    for feature_type in ("v2_connection_nodes", "v2_manhole", "v2_1d_boundary_conditions"):
        if feature_type in ds.id_mapping:
            for splt_id, inp_id in ds.id_mapping[feature_type].items():
                inp_to_splt_mapping[inp_id] = (feature_type, splt_id)

    progress_bar.increase_progress(20, "Prepare data")
    # add features
    features = []
    for i in range(flowelem_xcc.shape[0]):
        feat = QgsFeature()

        p1 = QgsPoint(flowelem_xcc[i], flowelem_ycc[i])

        feat.setGeometry(QgsGeometry.fromPoint(p1))

        inp_id = None
        splt_tbl = None
        splt_id = None
        try:
            inp_id = flowid_to_inp_mapping[i]
            splt_tbl, splt_id = inp_to_splt_mapping[inp_id]
        except KeyError:
            pass

        feat.setAttributes([i, inp_id, splt_id, splt_tbl])
        features.append(feat)
    progress_bar.increase_progress(30, "append data to memory layer")
    pr.addFeatures(features)

    progress_bar.increase_progress(25, "update extent")
    # update layer's extent when new features have been added
    # because change of extent in provider is not propagated to the layer
    vl.updateExtents()

    progress_bar.increase_progress(5, "ready")
    return vl

