"""Functions for creation of QgsVectorLayers from 3Di netCDF files"""
from osgeo import ogr
from qgis.core import QgsDataSourceUri
from qgis.core import QgsVectorLayer
from ThreeDiToolbox.datasource.spatialite import disable_sqlite_synchronous

import logging
import os


logger = logging.getLogger(__name__)


# Hardcoded default names
FLOWLINES_LAYER_NAME = "flowlines"
NODES_LAYER_NAME = "nodes"
CELLS_LAYER_NAME = "cells"
PUMPLINES_LAYER_NAME = "pumplines"
WGS84_EPSG = 4326

IGNORE_FIRST = slice(1, None, None)


def contains_layer(sqlite_path, layer_name):
    driver = ogr.GetDriverByName("SQLite")
    data_source = driver.Open(sqlite_path)
    has_layer = False
    for i in range(data_source.GetLayerCount()):
        lyr = data_source.GetLayer(i)
        if lyr.GetName() == layer_name:
            has_layer = True
            break
    data_source = None  # close data source
    return has_layer


def _get_vector_layer(sqlite_path, layer_name, geom_column="the_geom"):
    """Helper function to construct a QgsVectorLayer."""
    uri = QgsDataSourceUri()
    uri.setDatabase(sqlite_path)
    uri.setDataSource("", layer_name, geom_column)
    return QgsVectorLayer(uri.uri(), layer_name, "spatialite")


@disable_sqlite_synchronous
def get_or_create_flowline_layer(ds, output_path):
    if not os.path.exists(output_path) or not contains_layer(
        output_path, FLOWLINES_LAYER_NAME
    ):
        ga = ds.gridadmin
        from .gridadmin import QgisLinesOgrExporter

        exporter = QgisLinesOgrExporter("dont matter")
        exporter.driver = ogr.GetDriverByName("SQLite")
        sliced = ga.lines.slice(IGNORE_FIRST).reproject_to(str(WGS84_EPSG))
        exporter.save(output_path, FLOWLINES_LAYER_NAME, sliced.data, 4326)
    return _get_vector_layer(output_path, FLOWLINES_LAYER_NAME)


@disable_sqlite_synchronous
def get_or_create_node_layer(ds, output_path):
    if not os.path.exists(output_path) or not contains_layer(
        output_path, NODES_LAYER_NAME
    ):
        ga = ds.gridadmin
        from .gridadmin import QgisNodesOgrExporter

        exporter = QgisNodesOgrExporter("dont matter")
        exporter.driver = ogr.GetDriverByName("SQLite")
        sliced = ga.nodes.slice(IGNORE_FIRST).reproject_to(str(WGS84_EPSG))
        exporter.save(output_path, NODES_LAYER_NAME, sliced.data, WGS84_EPSG)
    return _get_vector_layer(output_path, NODES_LAYER_NAME)


@disable_sqlite_synchronous
def get_or_create_cell_layer(ds, output_path):
    if not os.path.exists(output_path) or not contains_layer(
        output_path, CELLS_LAYER_NAME
    ):
        ga = ds.gridadmin
        from .gridadmin import QgisNodesOgrExporter

        exporter = QgisNodesOgrExporter("dont matter")
        exporter.driver = ogr.GetDriverByName("SQLite")
        sliced = ga.cells.slice(
            IGNORE_FIRST
        )  # do not reproject to prevent coordinate drift
        exporter.save(
            output_path, CELLS_LAYER_NAME, sliced.data, int(ga.epsg_code), as_cells=True
        )
    return _get_vector_layer(output_path, CELLS_LAYER_NAME)


@disable_sqlite_synchronous
def get_or_create_pumpline_layer(ds, output_path):
    ga = ds.gridadmin
    if not os.path.exists(output_path) or not contains_layer(
        output_path, PUMPLINES_LAYER_NAME
    ):
        if ga.has_pumpstations:
            from .gridadmin import QgisPumpsOgrExporter

            exporter = QgisPumpsOgrExporter(node_data=ga.nodes.data)
            exporter.driver = ogr.GetDriverByName("SQLite")
            sliced = ga.pumps.slice(IGNORE_FIRST).reproject_to(str(WGS84_EPSG))
            exporter.save(output_path, PUMPLINES_LAYER_NAME, sliced.data, WGS84_EPSG)
    if ga.has_pumpstations:
        return _get_vector_layer(output_path, PUMPLINES_LAYER_NAME)
