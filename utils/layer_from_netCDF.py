"""Functions for creation of QgsVectorLayers from 3Di netCDF files"""
from qgis.core import (
    QgsFeature, QgsGeometry, QgsPoint, QgsCoordinateTransform,
    QgsCoordinateReferenceSystem, QGis)

from .user_messages import StatusProgressBar


def make_flowline_layer(ds, spatialite, progress_bar=None):
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
    source_epsg = projection.epsg
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

    progress_bar.increase_progress(10, "create layer")
    # create layer

    fields = [
        "id INTEGER",
        "inp_id INTEGER",
        "spatialite_id INTEGER",
        "type STRING(25)",
        "start_node_idx INTEGER NOT NULL",
        "end_node_idx INTEGER NOT NULL"
    ]

    layer = spatialite.create_empty_layer('flowlines', QGis.WKBLineString, fields, 'id')

    pr = layer.dataProvider()

    progress_bar.increase_progress(10, "create id mappings")
    # create inverse mapping
    if 'channel_mapping' not in ds.ds.variables:
        progress_bar.increase_progress(0, "no channel mapping found in netCDF, skip object mapping. Model only has 2d?")
        flowid_to_inp_mapping = {}
        inp_to_splt_mapping = {}
    else:
        pass
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

    source_crs = QgsCoordinateReferenceSystem(int(source_epsg))
    dest_crs = QgsCoordinateReferenceSystem(4326)

    transform = QgsCoordinateTransform(source_crs, dest_crs)

    # TODO: because there is not (yet) distinction  between number of 2d
    # links and 1d-2d links, we will guess the numbers based on the fact that
    # only id mapping is available for all 1d links. (when numbers become
    # available, this code can be improved and optimized

    for i in range(flowline_connection.shape[1]):
        feat = QgsFeature()

        p1 = transform.transform(QgsPoint(x_p1[i], y_p1[i]))
        p2 = transform.transform(QgsPoint(x_p2[i], y_p2[i]))

        feat.setGeometry(QgsGeometry.fromPolyline([p1, p2]))

        inp_id = None
        spatialite_tbl = None
        spatialite_id = None

        try:
            inp_id = int(flowid_to_inp_mapping[i+1])
            spatialite_tbl, spatialite_id = inp_to_splt_mapping[inp_id]
        except KeyError:
            cat = ds.line_type_of(i)
            if cat == '1d':
                cat = '1d_2d'
            spatialite_tbl = cat

        feat.setAttributes([i, inp_id, spatialite_id, spatialite_tbl,
                            int(flowline_p1[i]), int(flowline_p2[i])])

        features.append(feat)

    progress_bar.increase_progress(30, "append data to memory layer")
    pr.addFeatures(features)

    progress_bar.increase_progress(25, "update extent")

    # update layer's extent when new features have been added
    # because change of extent in provider is not propagated to the layer
    layer.updateExtents()

    progress_bar.increase_progress(15, "ready")
    return layer


def make_node_layer(ds, spatialite, progress_bar=None):
    """Make a memory layer that contains all nodes.

    Args:
        ds: NetcdfDataSource
        progress_bar: (StatusProgressBar) - progress bar instance for feedback
            about progress. This tool will make 100 steps.
        layer_type (string) - layer type, 'memory' or 'ogr' for a shapefile

    Returns:
        (QgsVectorLayer) In memory layer with all points or shapefile layer
    """
    if progress_bar is None:
        progress_bar = StatusProgressBar(100, 'create node layer: ')

    progress_bar.increase_progress(0, "read data from netCDF")
    # Get relevant netCDF.Variables
    projection = ds.ds.variables['projected_coordinate_system']
    source_epsg = projection.epsg  # = 28992
    # FlowElem centers:
    flowelem_xcc = ds.ds.variables['FlowElem_xcc']  # in meters
    flowelem_ycc = ds.ds.variables['FlowElem_ycc']  # in meters

    progress_bar.increase_progress(10, "create layer")
    # create layer
    fields = [
        "id INTEGER",
        "inp_id INTEGER",
        "spatialite_id INTEGER",
        "feature_type STRING(25)",
        "type STRING(25)"
    ]

    layer = spatialite.create_empty_layer('nodes', QGis.WKBPoint, fields, 'id' )

    pr = layer.dataProvider()

    progress_bar.increase_progress(10, "create id mappings")
    # create inverse mapping

    if 'node_mapping' not in ds.ds.variables:
        progress_bar.increase_progress(0, "no node mapping found in netCDF, skip object mapping. Model only has 2d?")
        node_idx_to_inp_id = {}
        inp_to_splt_mapping = {}
    else:
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

    source_crs = QgsCoordinateReferenceSystem(int(source_epsg))
    dest_crs = QgsCoordinateReferenceSystem(4326)
    transform = QgsCoordinateTransform(source_crs, dest_crs)

    for i in range(flowelem_xcc.shape[0]):
        feat = QgsFeature()

        p1 = transform.transform(QgsPoint(flowelem_xcc[i], flowelem_ycc[i]))

        feat.setGeometry(QgsGeometry.fromPoint(p1))

        # Getting all node types, feature types, and whatnot:
        node_type = ds.node_type_of(i)
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
    layer.updateExtents()

    progress_bar.increase_progress(15, "ready")
    return layer


def make_pumpline_layer(nds, spatialite, progress_bar=None):
    """Make a layer that contains all pumplines.

    Args:
        nds: netCDF Datasource
    """
    # Get relevant netCDF.Variables
    projection = nds.ds.variables['projected_coordinate_system']
    source_epsg = projection.epsg  # = 28992
    # Pumpline connections (2, jap1d):
    pumpline = nds.ds.variables['PumpLine_connection']

    # FlowElem centers:
    flowelem_xcc = nds.ds.variables['FlowElem_xcc']  # in meters
    flowelem_ycc = nds.ds.variables['FlowElem_ycc']  # in meters

    # -1 probably because of fortran indexing
    # CAUTION: pumpline index can be 0, (which means it is pumping out of the,
    # system) thus we can get a -1 here, which is NOT a valid index
    pumpline_p1 = pumpline[0, :].astype(int) - 1
    pumpline_p2 = pumpline[1, :].astype(int) - 1

    # Point 1 of the connection
    x_p1 = flowelem_xcc[:][pumpline_p1]
    y_p1 = flowelem_ycc[:][pumpline_p1]

    # Point 2 of the connection
    x_p2 = flowelem_xcc[:][pumpline_p2]
    y_p2 = flowelem_ycc[:][pumpline_p2]

    # create layer

    fields = [
        "id INTEGER",
        "node_idx1 INTEGER",
        "node_idx2 INTEGER"
    ]

    layer = spatialite.create_empty_layer('pumplines', QGis.WKBLineString, fields, 'id')

    pr = layer.dataProvider()

    # add features
    features = []
    number_of_pumplines = pumpline.shape[1]

    source_crs = QgsCoordinateReferenceSystem(int(source_epsg))
    dest_crs = QgsCoordinateReferenceSystem(4326)
    transform = QgsCoordinateTransform(source_crs, dest_crs)

    for i in range(number_of_pumplines):
        fet = QgsFeature()

        coord1 = (x_p1[i], y_p1[i])
        coord2 = (x_p2[i], y_p2[i])
        try:
            # -1 means the pump is pumping out of the model
            idx = [pumpline_p1[i], pumpline_p2[i]].index(-1)
            if idx == 0:
                start_coord = coord2
            elif idx == 1:
                start_coord = coord1
            # Give these pumps a special geometry
            p1 = QgsPoint(start_coord[0], start_coord[1])
            p2 = QgsPoint(start_coord[0] - 3, start_coord[1] + 5)
            p3 = QgsPoint(start_coord[0] + 3, start_coord[1] + 10)
            p4 = QgsPoint(start_coord[0], start_coord[1] + 15)
            geom = QgsGeometry.fromPolyline([p1, p2, p3, p4])
        except ValueError:
            p1 = QgsPoint(coord1[0], coord1[1])
            p2 = QgsPoint(coord2[0], coord2[1])
            geom = QgsGeometry.fromPolyline([p1, p2])

        node_idx1 = int(pumpline_p1[i])
        node_idx2 = int(pumpline_p2[i])

        geom.transform(transform)
        fet.setGeometry(geom)
        fet.setAttributes([i, node_idx1, node_idx2])
        features.append(fet)
    pr.addFeatures(features)

    # update layer's extent when new features have been added
    # because change of extent in provider is not propagated to the layer
    layer.updateExtents()

    return layer
