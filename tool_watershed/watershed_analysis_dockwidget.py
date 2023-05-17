# -*- coding: utf-8 -*-
# TODO Analyzed target nodes behouden bij afsluiten plugin
# TODO analyzed target nodes leegmaken bij clear ouputs

# TODO: If source is polygon layer, transfer polygon id to result layers
# TODO mogelijkheid om van een pand op te vragen wat het downstream effect is

# TODO: Allow save and loading of result sets to a single geopackage incl. styling

# TODO: auto-Enable/disable buttons in Target Nodes and Outputs sections

# TODO: handle removal of layer tree group (make impossible)

# TODO: add sub-categories to result flowline styling
# TODO: add discharge (q net sum) attribute to result flowlines
# TODO: add flow direction styling to result flowlines
import os
import pathlib
import processing
import numpy as np
from typing import Iterable, List
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal, Qt, QVariant
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsTask,
    QgsMessageLog,
    QgsProject,
    QgsDataSourceUri,
    QgsFeatureRequest,
    QgsExpression,
    QgsGeometry,
    QgsProcessingFeedback,
    QgsMapLayerProxyModel,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsField,
    QgsVectorLayer,
)
from qgis.gui import QgsMapToolIdentify
from osgeo import ogr, osr
from threedigrid.admin.gridresultadmin import GridH5ResultAdmin
from .watershed_analysis_networkx import Graph3Di
from .result_aggregation.threedigrid_ogr import threedigrid_to_ogr
from .ogr2qgis import as_qgis_memory_layer, append_to_qgs_vector_layer
from .smoothing import polygon_gaussian_smooth
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), "watershed_analysis_dockwidget_base.ui"))

STYLE_DIR = os.path.join(os.path.dirname(__file__), "style")
MEMORY_DRIVER = ogr.GetDriverByName("MEMORY")
DEFAULT_THRESHOLD = 1
MESSAGE_CATEGORY = "Watershed Analysis"


class LayerExistsError(Exception):
    """Raised when attempting to create a target_node_layer that already exists"""

    pass


class FindImperviousSurfaceError(Exception):
    """Raised when something goes wrong when finding impervious surfaces"""

    pass


def bbox_of_features(features: List):
    """Returns None if empty list is given as input"""
    first_pass = True
    bbox = None
    for feat in features:
        if first_pass:
            bbox = feat.geometry().boundingBox()
            first_pass = False
        else:
            bbox.combineExtentWith(feat.geometry().boundingBox())
    return bbox


class Graph3DiQgsConnector:
    """Connect a Graph3Di and its inputs and outputs to a QGIS Project"""

    # TODO: class alles laten erven van Graph3Di en evt. nieuw object met alle QGIS-dingen
    result_cell_attr_types = {
        "id": ogr.OFTInteger,
        "node_type": ogr.OFTInteger,
        "node_type_description": ogr.OFTString,
        "location": ogr.OFTString,
        "catchment_id": ogr.OFTInteger,
        "from_polygon": ogr.OFTInteger,
    }

    result_flowline_attr_types = {
        "id": ogr.OFTInteger,
        "content_type": ogr.OFTString,
        "kcu": ogr.OFTInteger,
        "kcu_description": ogr.OFTString,
        "location": ogr.OFTString,
        "catchment_id": ogr.OFTInteger,
        "from_polygon": ogr.OFTInteger,
    }

    def __init__(self, parent_dock):
        """Constructor."""
        self._filter = None
        self.parent_dock = parent_dock
        self.iface = parent_dock.iface
        self.epsg = None
        self.graph_3di = Graph3Di(subset=None)
        self._sqlite = None

        self.layer_group = None
        self.target_node_layer = None
        self.result_cell_layer = None
        self.result_flowline_layer = None
        self.result_catchment_layer = None
        self.impervious_surface_layer = None

        self.result_sets = []
        self.dissolved_result_sets = []
        self.smooth_result_catchments = []
        QgsProject.instance().layersWillBeRemoved.connect(self.qgs_project_layers_will_be_removed)
        self.protect_layers = True

    def __del__(self):
        QgsProject.instance().layersWillBeRemoved.disconnect(self.qgs_project_layers_will_be_removed)

    @property
    def gr(self):
        return self.graph_3di.gr

    @gr.setter
    def gr(self, value):
        # ! Do not use any QObject that lives on the main thread here, because this setter is called from a QgsTask
        # See https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/tasks.html
        self.graph_3di.gr = value

    @property
    def sqlite(self):
        return self._sqlite

    @sqlite.setter
    def sqlite(self, sqlite):
        sqlite_pathlib_path = pathlib.Path(sqlite)
        if not isinstance(sqlite_pathlib_path, pathlib.PurePath):
            raise TypeError
        value_changed = sqlite != self._sqlite
        self._sqlite = sqlite_pathlib_path
        if value_changed:
            if self.impervious_surface_layer is None and self._sqlite is not None:
                self.create_impervious_surface_layer()

    @property
    def threshold(self):
        return self.graph_3di.threshold

    @threshold.setter
    def threshold(self, value):
        self.graph_3di.threshold = value

    @property
    def start_time(self):
        return self.graph_3di.start_time

    @start_time.setter
    def start_time(self, value):
        self.graph_3di.start_time = value

    @property
    def end_time(self):
        return self.graph_3di.end_time

    @end_time.setter
    def end_time(self, value):
        self.graph_3di.end_time = value

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, ids: List):
        if isinstance(ids, list):
            for id_i in ids:
                if not isinstance(id_i, int):
                    raise TypeError("Filter must be set to None or list of int")
            self._filter = ids.copy()
        elif ids is None:
            self._filter = None
        else:
            raise TypeError("Filter must be set to None or list of int")
        self.update_layer_filters()

    def average_cell_size(self, result_set_id):
        request = QgsFeatureRequest()
        request.setFilterExpression(f"catchment_id = {result_set_id}")
        features = self.result_cell_layer.getFeatures(request)
        count = 0
        area = 0
        for feat in features:
            count += 1
            area += feat.geometry().area()
        if area > 0:
            return area / count
        else:
            return None

    def qgs_project_layers_will_be_removed(self, layer_ids):
        if self.protect_layers:
            layer_replaced = False
            try:
                if self.target_node_layer is not None:
                    if self.target_node_layer.id() in layer_ids:
                        self.target_node_layer = None
                        self.create_target_node_layer()
                        layer_replaced = True
            except AttributeError:
                pass

            try:
                if self.result_cell_layer is not None:
                    if self.result_cell_layer.id() in layer_ids:
                        self.result_cell_layer = None
                        self.create_result_cell_layer()
                        layer_replaced = True
            except AttributeError:
                pass

            try:
                if self.result_flowline_layer is not None:
                    if self.result_flowline_layer.id() in layer_ids:
                        self.result_flowline_layer = None
                        self.create_result_flowline_layer()
                        layer_replaced = True
            except AttributeError:
                pass

            try:
                if self.result_catchment_layer is not None:
                    if self.result_catchment_layer.id() in layer_ids:
                        self.result_catchment_layer = None
                        self.create_catchment_layer()
                        layer_replaced = True
            except AttributeError:
                pass

            try:
                if self.impervious_surface_layer is not None:
                    if self.impervious_surface_layer.id() in layer_ids:
                        self.impervious_surface_layer = None
                        self.create_impervious_surface_layer()
                        layer_replaced = True
            except AttributeError:
                pass

            if layer_replaced:
                self.iface.messageBar().pushMessage(
                    MESSAGE_CATEGORY, "Oops, I needed the layer(s) you deleted! I created them again", Qgis.Info
                )

    def update_layer_filters(self):
        filtered_ids = set(self.result_sets) & set(self.filter if self.filter is not None else self.result_sets)
        filtered_ids_str = ",".join(map(str, filtered_ids))
        if self.filter is None:
            subset_string = ""
            target_node_layer_analyzed_nodes_rule_str = "result_sets != ''"
        else:
            subset_string = "catchment_id IN ({})".format(filtered_ids_str)
            target_node_layer_analyzed_nodes_rule_str = (
                f'array_intersect( string_to_array("result_sets"),  array({filtered_ids_str}))'
            )
        # filter to leave subset_string out if empty
        flowline_subset_string = " AND ".join(filter(None, [subset_string, "kcu != 100"]))
        self.result_catchment_layer.setSubsetString(subset_string)
        self.result_cell_layer.setSubsetString(subset_string)
        self.result_flowline_layer.setSubsetString(flowline_subset_string)
        self.target_node_layer.renderer().rootRule().children()[0].setFilterExpression(
            target_node_layer_analyzed_nodes_rule_str
        )
        if self.impervious_surface_layer is not None:
            self.impervious_surface_layer.setSubsetString(subset_string)

    def new_result_set_id(self):
        if len(self.result_sets) == 0:
            self.result_sets.append(1)  # 1-based index because this is common in GIS id fields
        else:
            self.result_sets.append(max(self.result_sets) + 1)
        return max(self.result_sets)

    def gr_updated(self):
        """Executed when a new 3Di result is selected (self.gr is changed)"""
        if isinstance(self.graph_3di.gr, GridH5ResultAdmin):
            self.epsg = int(self.graph_3di.gr.epsg_code)
            self.create_layer_group()
            # Note: the sequence is deliberate; the target nodes are below the result layers because otherwise, if \
            # zoomed out too much, the target nodes will cover the result.
            self.create_target_node_layer()
            self.create_result_cell_layer()
            self.create_result_flowline_layer()
            self.create_catchment_layer()

    def add_to_layer_tree_group(self, layer):
        """
        Add a layer to the 3Di Network Analysis layer tree group
        """
        project = QgsProject.instance()
        project.addMapLayer(layer, addToLegend=False)
        self.layer_group.insertLayer(0, layer)

    def remove_empty_layers(self):
        """For all locked layers, remove locks or layers themselves"""
        remove_group = True
        try:
            self.remove_target_node_layer()
        except AttributeError:
            pass

        try:
            if self.result_cell_layer is not None:
                if self.result_cell_layer.featureCount() == 0:
                    self.remove_result_cell_layer()
                else:
                    remove_group = False
        except AttributeError:
            pass

        try:
            if self.result_flowline_layer is not None:
                if self.result_flowline_layer.featureCount() == 0:
                    self.remove_result_flowline_layer()
                else:
                    remove_group = False
        except AttributeError:
            pass

        try:
            if self.result_catchment_layer is not None:
                if self.result_catchment_layer.featureCount() == 0:
                    self.remove_catchment_layer()
                else:
                    remove_group = False
        except AttributeError:
            pass

        try:
            if self.impervious_surface_layer is not None:
                if self.impervious_surface_layer.featureCount() == 0:
                    self.remove_impervious_surface_layer()
                else:
                    remove_group = False
        except AttributeError:
            pass

        if remove_group:
            self.remove_layer_group()

        self.iface.mapCanvas().refresh()

    def create_layer_group(self):
        root = QgsProject.instance().layerTreeRoot()
        self.layer_group = root.insertGroup(0, "3Di Watershed Analysis")

    def remove_layer_group(self):
        try:
            QgsProject.instance().layerTreeRoot().removeChildNode(self.layer_group)
        except RuntimeError:
            pass

    def create_target_node_layer(self):
        if isinstance(self.gr, GridH5ResultAdmin):
            nodes = self.gr.nodes
            nodes_ds = MEMORY_DRIVER.CreateDataSource("")
            attributes = {"result_sets": [""] * nodes.count}
            attr_data_types = {"result_sets": ogr.OFTString}
            threedigrid_to_ogr(
                threedigrid_src=nodes, tgt_ds=nodes_ds, attributes=attributes, attr_data_types=attr_data_types
            )
            ogr_lyr = nodes_ds.GetLayerByName("node")
            self.target_node_layer = as_qgis_memory_layer(ogr_lyr, "Target nodes")
            qml = os.path.join(STYLE_DIR, "target_nodes.qml")
            self.target_node_layer.loadNamedStyle(qml)
            self.add_to_layer_tree_group(self.target_node_layer)

    def clear_target_node_layer(self):
        """Empty the result_set field of all features in the target_node_layer"""
        if self.target_node_layer is not None:
            request = QgsFeatureRequest()
            request.setFilterExpression("result_sets != ''")
            idx = self.target_node_layer.fields().indexFromName("result_sets")
            self.target_node_layer.startEditing()
            for feat in self.target_node_layer.getFeatures(request):
                self.target_node_layer.changeAttributeValue(feat.id(), idx, "")
            self.target_node_layer.commitChanges()

    def remove_target_node_layer(self):
        try:
            if self.target_node_layer is not None:
                self.protect_layers = False
                project = QgsProject.instance()
                project.removeMapLayer(self.target_node_layer)
                self.protect_layers = True
        except AttributeError:
            pass
        self.target_node_layer = None

    def create_result_cell_layer(self):
        try:
            if self.result_cell_layer is not None:
                raise LayerExistsError("Attempt to create existing result cell layer")
        except AttributeError:
            pass
        ogr_driver = ogr.GetDriverByName("Memory")
        ogr_data_source = ogr_driver.CreateDataSource("")
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(self.epsg)
        ogr_lyr = ogr_data_source.CreateLayer("", srs, geom_type=ogr.wkbPolygon)
        for fieldname, fieldtype in self.result_cell_attr_types.items():
            field = ogr.FieldDefn(fieldname, fieldtype)
            ogr_lyr.CreateField(field)

        qgs_lyr_name = "Result cells"
        self.result_cell_layer = as_qgis_memory_layer(ogr_lyr, qgs_lyr_name)
        qml = os.path.join(STYLE_DIR, "result_cells.qml")
        self.result_cell_layer.loadNamedStyle(qml)
        self.add_to_layer_tree_group(self.result_cell_layer)

    def update_analyzed_target_cells(self, target_node_ids, result_set):
        ids_str = ",".join(map(str, target_node_ids))
        request = QgsFeatureRequest()
        request.setFilterExpression(f"id IN ({ids_str})")
        idx = self.target_node_layer.fields().indexFromName("result_sets")
        self.target_node_layer.startEditing()
        for feat in self.target_node_layer.getFeatures(request):
            old_result_sets = feat["result_sets"]
            result_sets_list = old_result_sets.split(",")
            result_sets_list.append(result_set)
            new_result_sets = ",".join(map(str, result_sets_list))
            self.target_node_layer.changeAttributeValue(feat.id(), idx, new_result_sets)
        self.target_node_layer.commitChanges()
        self.update_layer_filters()

    def find_cells(self, target_node_ids: List, upstream: bool, result_set: int):
        """Find cells upstream or downstream from the list of target nodes and append them to the result cell layer"""
        if upstream:
            cell_ids_full_set = self.graph_3di.upstream_nodes(target_node_ids)
        else:
            cell_ids_full_set = self.graph_3di.downstream_nodes(target_node_ids)
        # cell_ids = cell_ids_full_set - set(target_node_ids)
        self.append_result_cells(cell_ids=cell_ids_full_set, upstream=upstream, result_set=result_set)
        self.update_analyzed_target_cells(target_node_ids, result_set)

    def append_result_cells(self, cell_ids, upstream: bool, result_set: int):
        cells = self.gr.cells.filter(id__in=list(cell_ids))

        nw_ids = list(cells.id)

        nw_catchment_ids = [result_set] * cells.count

        if upstream:
            location = ["upstream"] * cells.count
        else:
            location = ["downstream"] * cells.count

        from_polygon = [0] * cells.count

        attributes = {
            "id": nw_ids,
            "location": location,
            "catchment_id": nw_catchment_ids,
            "from_polygon": from_polygon,
        }

        ds = MEMORY_DRIVER.CreateDataSource("")
        threedigrid_to_ogr(
            threedigrid_src=cells, tgt_ds=ds, attributes=attributes, attr_data_types=self.result_cell_attr_types
        )
        layer = ds.GetLayerByName("cell")
        append_to_qgs_vector_layer(ogr_layer=layer, qgs_vector_layer=self.result_cell_layer)

    def clear_result_cell_layer(self):
        """Remove all features from layer that contains the upstream and/or downstream cells"""
        if self.result_cell_layer is not None:
            self.result_cell_layer.dataProvider().truncate()

    def remove_result_cell_layer(self):
        """Remove layer that contains the upstream and/or downstream cells"""
        if self.result_cell_layer is not None:
            self.protect_layers = False
            QgsProject.instance().removeMapLayer(self.result_cell_layer)
            self.result_cell_layer = None
            self.protect_layers = True

    def create_result_flowline_layer(self):
        try:
            if self.result_flowline_layer is not None:
                raise LayerExistsError("Attempt to create existing result flowline layer")
        except AttributeError:
            pass
        ogr_driver = ogr.GetDriverByName("Memory")
        ogr_data_source = ogr_driver.CreateDataSource("")
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(self.epsg)
        ogr_lyr = ogr_data_source.CreateLayer("", srs, geom_type=ogr.wkbLineString)
        for fieldname, fieldtype in self.result_flowline_attr_types.items():
            field = ogr.FieldDefn(fieldname, fieldtype)
            ogr_lyr.CreateField(field)

        qgs_lyr_name = "Result flowlines (1D)"
        self.result_flowline_layer = as_qgis_memory_layer(ogr_lyr, qgs_lyr_name)
        qml = os.path.join(STYLE_DIR, "result_flowlines.qml")
        self.result_flowline_layer.loadNamedStyle(qml)
        self.add_to_layer_tree_group(self.result_flowline_layer)
        self.result_flowline_layer.setSubsetString("kcu != 100")

    def find_flowlines(self, node_ids: List, upstream: bool, result_set: int):
        """Find flowlines that connect the input nodes \
        and append them to the result flowline layer"""
        flowlines_ids = self.graph_3di.flowlines_between_nodes(node_ids=node_ids)
        self.append_result_flowlines(flowline_ids=flowlines_ids, upstream=upstream, result_set=result_set)

    def append_result_flowlines(self, flowline_ids, upstream: bool, result_set: int):
        flowlines = self.gr.lines.filter(id__in=list(flowline_ids))
        nw_ids = list(flowlines.id)
        nw_catchment_ids = [result_set] * flowlines.count
        if upstream:
            location = ["upstream"] * flowlines.count
        else:
            location = ["downstream"] * flowlines.count
        from_polygon = [0] * flowlines.count
        attributes = {
            "id": nw_ids,
            "location": location,
            "catchment_id": nw_catchment_ids,
            "from_polygon": from_polygon,
        }

        ds = MEMORY_DRIVER.CreateDataSource("")
        threedigrid_to_ogr(
            threedigrid_src=flowlines, tgt_ds=ds, attributes=attributes, attr_data_types=self.result_flowline_attr_types
        )
        layer = ds.GetLayerByName("flowline")
        append_to_qgs_vector_layer(ogr_layer=layer, qgs_vector_layer=self.result_flowline_layer)

    def clear_result_flowline_layer(self):
        """Remove all features from layer that contains the upstream and/or downstream flowlines"""
        if self.result_flowline_layer is not None:
            self.result_flowline_layer.dataProvider().truncate()

    def remove_result_flowline_layer(self):
        """Remove layer that contains the upstream and/or downstream flowlines"""
        if self.result_flowline_layer is not None:
            self.protect_layers = False
            QgsProject.instance().removeMapLayer(self.result_flowline_layer)
            self.result_flowline_layer = None
            self.protect_layers = True

    def create_catchment_layer(self):
        try:
            if self.result_catchment_layer is not None:
                raise LayerExistsError("Attempt to create existing result catchment layer")
        except AttributeError:
            pass
        ogr_driver = ogr.GetDriverByName("Memory")
        ogr_data_source = ogr_driver.CreateDataSource("")
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(self.epsg)
        ogr_lyr = ogr_data_source.CreateLayer("", srs, geom_type=ogr.wkbPolygon)

        for fieldname, fieldtype in self.result_cell_attr_types.items():
            field = ogr.FieldDefn(fieldname, fieldtype)
            ogr_lyr.CreateField(field)

        qgs_lyr_name = "Result catchments"
        self.result_catchment_layer = as_qgis_memory_layer(ogr_lyr, qgs_lyr_name)
        qml = os.path.join(STYLE_DIR, "result_catchments.qml")
        self.result_catchment_layer.loadNamedStyle(qml)
        self.add_to_layer_tree_group(self.result_catchment_layer)

    def clear_catchment_layer(self):
        """Remove all features from layer that contains the upstream and/or downstream cells"""
        if self.result_catchment_layer is not None:
            fids = [feat.id() for feat in self.result_catchment_layer.getFeatures()]
            self.result_catchment_layer.dataProvider().truncate()
            self.result_catchment_layer.featuresDeleted.emit(fids)

    def dissolve_cells(self):
        """Dissolve cells in self.result_cells_layer of all not yet dissolved result sets"""
        saved_subsetstring = self.result_cell_layer.subsetString()
        non_dissolved_ids = set(self.result_sets) - set(self.dissolved_result_sets)
        non_dissolved_ids_str = ",".join(map(str, non_dissolved_ids))
        subset_string = "catchment_id IN ({})".format(non_dissolved_ids_str)
        self.result_cell_layer.setSubsetString(subset_string)

        feedback = QgsProcessingFeedback()
        dslv_params = {
            "INPUT": self.result_cell_layer,  # QgsVectorLayer
            "FIELD": ["location", "catchment_id"],  # dissolve field (str)
            "OUTPUT": "memory:",
        }

        multipolys = processing.run("qgis:dissolve", dslv_params, feedback=feedback)["OUTPUT"]
        to_single_params = {"INPUT": multipolys, "OUTPUT": "memory:Result Catchments"}  # QgsVectorLayer
        nw_result_catchments_layer = processing.run("qgis:multiparttosingleparts", to_single_params, feedback=feedback)[
            "OUTPUT"
        ]

        self.result_catchment_layer.startEditing()
        self.result_catchment_layer.dataProvider().addFeatures(nw_result_catchments_layer.getFeatures())
        self.result_catchment_layer.commitChanges()
        self.dissolved_result_sets = self.result_sets.copy()
        self.result_catchment_layer.triggerRepaint()
        self.result_cell_layer.setSubsetString(saved_subsetstring)
        self.result_catchment_layer.featureAdded.emit(self.result_catchment_layer.featureCount())

    def smooth_catchment_layer(self):
        saved_subsetstring = self.result_catchment_layer.subsetString()
        self.result_catchment_layer.setSubsetString("")
        self.result_catchment_layer.startEditing()
        for feature in self.result_catchment_layer.getFeatures():
            if feature.id() not in self.smooth_result_catchments:
                avg_cell_size = self.average_cell_size(feature["catchment_id"])
                avg_grid_space = np.sqrt(avg_cell_size)
                sigma = np.max([10, 16 * np.log(avg_grid_space) - 30])  # formula fitted to trial and error results
                sample_dist = np.max([2, 2 * np.log(avg_grid_space) - 3])
                geom = feature.geometry()
                ogr_geom = ogr.CreateGeometryFromWkb(geom.asWkb())
                ogr_geom_smooth = polygon_gaussian_smooth(ogr_geom, sigma=sigma, sample_dist=sample_dist)
                qgs_geom_smooth = QgsGeometry()
                qgs_geom_smooth.fromWkb(ogr_geom_smooth.ExportToWkb())
                self.result_catchment_layer.changeGeometry(feature.id(), qgs_geom_smooth)
            self.smooth_result_catchments.append(feature.id())
        self.result_catchment_layer.commitChanges()
        self.result_catchment_layer.setSubsetString(saved_subsetstring)

    def remove_catchment_layer(self):
        """Remove layer that contains the upstream and/or downstream catchments"""
        if self.result_catchment_layer is not None:
            self.protect_layers = False
            QgsProject.instance().removeMapLayer(self.result_catchment_layer)
            self.result_catchment_layer = None
            self.protect_layers = True

    def create_impervious_surface_layer(self):
        # This layer is different from the other result layers, because it is a copy of an existing layer from the
        # spatialite; It is easier to copy the layer using the QGIS API
        self.impervious_surface_source_layer = QgsVectorLayer(
            path=str(self.sqlite) + "|layername=v2_impervious_surface",
            baseName="v2_impervious_surface",
            providerLib="ogr",
        )

        fields = self.impervious_surface_source_layer.fields().toList()
        catchment_id_field = QgsField("catchment_id", QVariant.Int)
        fields.append(catchment_id_field)
        self.impervious_surface_layer = QgsVectorLayer("Polygon", "Impervious surface", "memory")
        crs = QgsCoordinateReferenceSystem()
        crs.createFromId(4326)
        self.impervious_surface_layer.setCrs(crs)
        self.impervious_surface_layer.dataProvider().addAttributes(fields)
        self.impervious_surface_layer.updateFields()
        qml = os.path.join(STYLE_DIR, "result_impervious_surfaces.qml")
        self.impervious_surface_layer.loadNamedStyle(qml)
        self.add_to_layer_tree_group(self.impervious_surface_layer)

    def append_impervious_surfaces(self, result_set: int, ids: List = None, expression: str = None):
        """
        Copy features from the source v2_impervious_surface table to the result table
        impervious surfaces may be selected by ids or by expression. Expression overrules ids
        """
        impervious_surface_layer_subset_string = self.impervious_surface_layer.subsetString()
        self.impervious_surface_layer.setSubsetString("")
        max_fid_before = self.impervious_surface_layer.dataProvider().featureCount()
        if expression is None:
            ids_str = ",".join(map(str, ids))
            expression = f"id IN ({ids_str})"
        self.impervious_surface_source_layer.setSubsetString(expression)
        features = self.impervious_surface_source_layer.getFeatures()
        success = self.impervious_surface_layer.dataProvider().addFeatures(features)
        if not success:
            return False
        request = QgsFeatureRequest(QgsExpression(f"$id > {max_fid_before}"))
        added_features = self.impervious_surface_layer.getFeatures(request)
        catchment_id_field_idx = self.impervious_surface_layer.dataProvider().fieldNameIndex("catchment_id")
        attr_map = {feat.id(): {catchment_id_field_idx: result_set} for feat in added_features}
        success = self.impervious_surface_layer.dataProvider().changeAttributeValues(attr_map)
        if not success:
            return False
        self.impervious_surface_layer.updateExtents()
        self.impervious_surface_layer.setSubsetString(impervious_surface_layer_subset_string)
        return True

    def clear_impervious_surface_layer(self):
        """
        Remove all features from layer
        """
        if self.impervious_surface_layer is not None:
            self.impervious_surface_layer.dataProvider().truncate()

    def remove_impervious_surface_layer(self):
        """
        Remove layer that contains the upstream and/or downstream flowlines
        """
        if self.impervious_surface_layer is not None:
            self.protect_layers = False
            QgsProject.instance().removeMapLayer(self.impervious_surface_layer)
            self.impervious_surface_layer = None
            self.protect_layers = True

    def find_impervious_surfaces(self, node_ids: List, result_set: int = None):
        """
        Find impervious surfaces connected to nodes and append them to the impervious surface layer
        """
        if self.impervious_surface_layer is not None and self.sqlite is not None:
            nodes = self.gr.nodes.filter(id__in=node_ids)
            connection_node_ids = set(nodes.content_pk) - {None, -9999}
            connection_node_ids_str = ",".join(map(str, connection_node_ids))
            expression = (
                "id in (SELECT impervious_surface_id FROM v2_impervious_surface_map "
                f"WHERE connection_node_id IN ({connection_node_ids_str}))"
            )
            success = self.append_impervious_surfaces(result_set=result_set, expression=expression)
            if not success:
                raise FindImperviousSurfaceError()

    def upstream_downstream_analysis(self, target_node_ids: Iterable, upstream: bool, downstream: bool):
        progress_message_bar = self.iface.messageBar().createMessage("3Di Network Analysis is being performed...")
        progress = QtWidgets.QProgressBar()
        current_progress = 0
        max_progress = 2
        if upstream:
            max_progress += 4
        if downstream:
            max_progress += 3
        progress.setMaximum(max_progress)
        progress.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        progress_message_bar.layout().addWidget(progress)
        self.iface.messageBar().pushWidget(progress_message_bar, Qgis.Info)
        self.iface.mainWindow().repaint()  # to show the message before the task starts

        result_set = self.new_result_set_id()

        if upstream:
            upstream_node_ids = self.graph_3di.upstream_nodes(target_node_ids)
            # upstream_node_ids -= set(target_node_ids) # remove the target nodes from the result
            current_progress += 1
            progress.setValue(current_progress)
            print(f"{current_progress}/{max_progress}: upstream_node_ids identified")

            self.append_result_cells(cell_ids=upstream_node_ids, upstream=True, result_set=result_set)
            current_progress += 1
            progress.setValue(current_progress)
            print(f"{current_progress}/{max_progress}: upstream result cells appended")

            upstream_node_ids.update(set(target_node_ids))
            self.find_flowlines(node_ids=list(upstream_node_ids), upstream=True, result_set=result_set)
            current_progress += 1
            progress.setValue(current_progress)
            print(f"{current_progress}/{max_progress}: upstream flowlines found")

            try:
                self.find_impervious_surfaces(node_ids=list(upstream_node_ids), result_set=result_set)
            except FindImperviousSurfaceError:
                self.iface.messageBar().pushMessage(
                    MESSAGE_CATEGORY, "Something went wrong when finding impervious surfaces", Qgis.Warning
                )
            current_progress += 1
            progress.setValue(current_progress)
            print(f"{current_progress}/{max_progress}: impervious surfaces found")

        if downstream:
            downstream_node_ids = self.graph_3di.downstream_nodes(target_node_ids)
            current_progress += 1
            progress.setValue(current_progress)
            print(f"{current_progress}/{max_progress}: downstream_node_ids identified")

            # downstream_node_ids -= set(target_node_ids) # remove the target nodes from the result
            self.append_result_cells(cell_ids=downstream_node_ids, upstream=False, result_set=result_set)
            current_progress += 1
            progress.setValue(current_progress)
            print(f"{current_progress}/{max_progress}: downstream result cells appended")

            downstream_node_ids.update(set(target_node_ids))
            self.find_flowlines(node_ids=list(downstream_node_ids), upstream=False, result_set=result_set)
            current_progress += 1
            progress.setValue(current_progress)
            print(f"{current_progress}/{max_progress}: downstream flowlines found")

        self.dissolve_cells()
        current_progress += 1
        progress.setValue(current_progress)
        print(f"{current_progress}/{max_progress}: cells dissolved")

        self.smooth_catchment_layer()
        current_progress += 1
        progress.setValue(current_progress)
        print(f"{current_progress}/{max_progress}: catchments smoothed")

        self.result_cell_layer.triggerRepaint()
        self.result_flowline_layer.triggerRepaint()
        if self.impervious_surface_layer is not None:
            self.impervious_surface_layer.triggerRepaint()
        self.update_analyzed_target_cells(target_node_ids, result_set)
        current_progress += 1
        progress.setValue(current_progress)
        print(f"{current_progress}/{max_progress}: finished")

        self.iface.messageBar().clearWidgets()

    def zoom_to_results(self):
        # catchments
        # not needed, because bbox of catchments < bbox of cells

        project_crs = QgsProject.instance().crs()
        source_crs = QgsCoordinateReferenceSystem(f"EPSG:{self.epsg}")
        transform = QgsCoordinateTransform(source_crs, project_crs, QgsProject.instance())
        impervious_surface_crs = QgsCoordinateReferenceSystem("EPSG:4326")
        impervious_surface_transform = QgsCoordinateTransform(
            impervious_surface_crs, project_crs, QgsProject.instance()
        )
        transformed_bbox = None

        # target nodes
        if self.target_node_layer is not None:
            request = QgsFeatureRequest(QgsExpression("result_sets != ''"))
            features = self.target_node_layer.getFeatures(request)
            nodes_bbox = bbox_of_features(features=features)
            if nodes_bbox is not None:
                transformed_bbox = transform.transformBoundingBox(nodes_bbox)

        # cells
        if self.result_cell_layer is not None:
            features = self.result_cell_layer.getFeatures()
            cells_bbox = bbox_of_features(features=features)
            if cells_bbox is not None:
                transformed_cells_bbox = transform.transformBoundingBox(cells_bbox)
                if transformed_bbox is None:
                    transformed_bbox = transformed_cells_bbox
                elif transformed_cells_bbox is not None:
                    transformed_bbox.combineExtentWith(transformed_cells_bbox)

        # flowlines
        if self.result_flowline_layer is not None:
            features = self.result_flowline_layer.getFeatures()
            flowlines_bbox = bbox_of_features(features=features)
            if flowlines_bbox is not None:  # layer exists but no contains no features
                transformed_flowlines_bbox = transform.transformBoundingBox(flowlines_bbox)
                if transformed_bbox is None:
                    transformed_bbox = transformed_flowlines_bbox
                elif transformed_flowlines_bbox is not None:
                    transformed_bbox.combineExtentWith(transformed_flowlines_bbox)

        # impervious surfaces
        if self.impervious_surface_layer is not None:
            features = self.impervious_surface_layer.getFeatures()
            impervious_surface_bbox = bbox_of_features(features=features)
            if impervious_surface_bbox is not None:
                transformed_impervious_surface_bbox = impervious_surface_transform.transformBoundingBox(
                    impervious_surface_bbox
                )
                if transformed_bbox is None:
                    transformed_bbox = transformed_impervious_surface_bbox
                elif transformed_impervious_surface_bbox is not None:
                    transformed_bbox.combineExtentWith(transformed_impervious_surface_bbox)

        if transformed_bbox is not None:
            transformed_bbox.scale(1.1)
            self.iface.mapCanvas().setExtent(transformed_bbox)
        return

    def clear_all(self):
        self.clear_target_node_layer()
        self.clear_result_cell_layer()
        self.clear_result_flowline_layer()
        self.clear_catchment_layer()
        self.clear_impervious_surface_layer()
        self.result_sets = []
        self.iface.mapCanvas().refreshAllLayers()


class CatchmentMapTool(QgsMapToolIdentify):
    def __init__(self, parent_widget, parent_button, gq: Graph3DiQgsConnector, upstream=False, downstream=False):
        super().__init__(gq.canvas)
        self.gq = gq
        self.upstream = upstream
        self.downstream = downstream
        self.parent_widget = parent_widget
        self.parent_button = parent_button
        self.set_cursor()

    @property
    def upstream(self):
        return self._upstream

    @upstream.setter
    def upstream(self, value):
        self._upstream = value

    @property
    def downstream(self):
        return self._downstream

    @downstream.setter
    def downstream(self, value):
        self._downstream = value

    def canvasReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        identify_results = self.identify(x=int(x), y=int(y), layerList=[self.gq.target_node_layer])
        if len(identify_results) == 0:
            self.parent_widget.iface.messageBar().pushMessage(
                MESSAGE_CATEGORY, "Please click on a target node", level=Qgis.Info
            )
        else:
            target_node_id = identify_results[0].mFeature.id()
            self.gq.upstream_downstream_analysis(
                target_node_ids=[target_node_id], upstream=self.upstream, downstream=self.downstream
            )

    def activate(self):
        pass

    def deactivate(self):
        if self.parent_button is not None:
            self.parent_button.setChecked(False)

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True

    def set_cursor(self):
        cursor = QtGui.QCursor()
        cursor.setShape(Qt.CrossCursor)
        self.canvas().setCursor(cursor)


class WatershedAnalystDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    closingWidget = pyqtSignal()

    def __init__(self, iface, model, parent=None):
        """Constructor."""
        super(WatershedAnalystDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.iface = iface
        self.model = model
        self.catchment_map_tool = None
        self.tm = QgsApplication.taskManager()
        self.connect_gq()
        self.mMapLayerComboBoxTargetPolygons.setFilters(QgsMapLayerProxyModel.PolygonLayer)
        self.QgsFileWidgetSqlite.fileChanged.connect(self.sqlite_selected)

        self.doubleSpinBoxThreshold.valueChanged.connect(self.threshold_changed)
        self.doubleSpinBoxThreshold.setSingleStep(1)
        self.doubleSpinBoxThreshold.setMinimum(0)
        self.doubleSpinBoxThreshold.setValue(DEFAULT_THRESHOLD)
        self.doubleSpinBoxStartTime.valueChanged.connect(self.start_time_changed)
        self.doubleSpinBoxEndTime.valueChanged.connect(self.end_time_changed)
        self.checkBoxUpstream.stateChanged.connect(self.checkbox_upstream_state_changed)
        self.checkBoxDownstream.stateChanged.connect(self.checkbox_downstream_state_changed)
        self.pushButtonClickOnCanvas.clicked.connect(self.pushbutton_click_on_canvas_clicked)
        self.pushButtonCatchmentForSelectedNodes.clicked.connect(self.pushbutton_catchment_for_selected_nodes_clicked)
        self.pushButtonCatchmentForPolygons.clicked.connect(self.pushbutton_catchment_for_polygons_clicked)
        self.checkBoxBrowseResultSets.stateChanged.connect(self.checkbox_browse_result_sets_state_changed)
        self.spinBoxBrowseResultSets.valueChanged.connect(self.spinbox_browse_result_sets_value_changed)
        self.pushButtonClearResults.clicked.connect(self.pushbutton_clear_results_clicked)

        QgsProject.instance().cleared.connect(self.close)
        self.comboBoxResult.activated.connect(self.select_result)
        self._populate_results()
        self.comboBoxResult.setCurrentIndex(-1)

    def _populate_results(self) -> None:
        self.comboBoxResult.clear()
        for result in self.model.get_results(checked_only=False):
            self.comboBoxResult.addItem(result.text(), result.id)

    def select_result(self, index: int) -> None:
        result_id = self.comboBoxResult.itemData(index)
        result = self.model.get_result(result_id)
        results_3di = result.path
        gridadmin = result.parent().path.with_suffix('.h5')
        assert os.path.isfile(results_3di) and os.path.isfile(gridadmin)

        self.disconnect_gq()
        self.connect_gq()
        gr = GridH5ResultAdmin(str(gridadmin), str(results_3di))
        self.gq.end_time = int(gr.nodes.timestamps[-1])
        if self.doubleSpinBoxThreshold.value() is not None:
            self.gq.threshold = self.doubleSpinBoxThreshold.value()
        else:
            self.gq.threshold = DEFAULT_THRESHOLD
        update_gr_task = UpdateGridAdminTask(
            description="Preprocess 3Di Results for Network Analysis", parent=self, gr=gr
        )
        self.iface.messageBar().pushMessage(
            MESSAGE_CATEGORY, "Started pre-processing simulation results", Qgis.Info
        )
        self.tm.addTask(update_gr_task)
        self.iface.mainWindow().repaint()  # to show the message before the task starts

    def add_result(self, result_item: ThreeDiResultItem) -> None:
        currentIndex = self.comboBoxResult.currentIndex()
        self.comboBoxResult.addItem(result_item.text(), result_item.id)
        self.comboBoxResult.setCurrentIndex(currentIndex)

    def remove_result(self, result_item: ThreeDiResultItem):
        idx = self.comboBoxResult.findData(result_item.id)
        assert idx != -1
        # TODO: if current, clean up
        self.comboBoxResult.removeItem(idx)

    def closeEvent(self, event):
        QgsProject.instance().cleared.disconnect(self.close)
        self.disconnect_gq()
        self.closingWidget.emit()
        event.accept()

    def connect_gq(self):
        self.gq = Graph3DiQgsConnector(parent_dock=self)
        self.gq.start_time = 0  # initial value of widget is 0, so valueChanged() signal will not be emitted when ...
        # ... a 3Di result is loaded for the first time

    def disconnect_gq(self):
        self.unset_map_tool()
        self.gq.remove_empty_layers()
        self.gq.clear_all()
        if self.gq.layer_group is not None:
            self.gq.remove_layer_group()
        self.gq = None

    def sqlite_selected(self):
        uri = QgsDataSourceUri()
        uri.setDatabase(self.QgsFileWidgetSqlite.filePath())
        schema = ""
        table = "v2_impervious_surface"
        geom_column = "the_geom"
        uri.setDataSource(schema, table, geom_column)

        display_name = "just for validity"
        vlayer = QgsVectorLayer(uri.uri(), display_name, "spatialite")
        if vlayer.isValid():
            self.gq.sqlite = self.QgsFileWidgetSqlite.filePath()
            self.iface.messageBar().pushMessage(
                MESSAGE_CATEGORY, "Succesfully added impervious surfaces from model", level=Qgis.Success
            )
        else:
            self.iface.messageBar().pushMessage(
                MESSAGE_CATEGORY, "Invalid 3Di model sqlite selected", level=Qgis.Warning
            )
            self.QgsFileWidgetSqlite.setFilePath("")

    def threshold_changed(self):
        self.gq.threshold = self.doubleSpinBoxThreshold.value()

    def start_time_changed(self):
        self.gq.start_time = self.doubleSpinBoxStartTime.value()

    def end_time_changed(self):
        self.gq.end_time = self.doubleSpinBoxEndTime.value()

    def unset_map_tool(self):
        try:
            if self.catchment_map_tool is not None:
                self.iface.mapCanvas().unsetMapTool(self.catchment_map_tool)
                self.catchment_map_tool = None
        except AttributeError:
            pass

    def pushbutton_click_on_canvas_clicked(self):
        if self.pushButtonClickOnCanvas.isChecked() and self.gq.graph_3di.isready:
            self.catchment_map_tool = CatchmentMapTool(
                parent_widget=self,
                parent_button=self.pushButtonClickOnCanvas,
                gq=self.gq,
                upstream=self.checkBoxUpstream.isChecked(),
                downstream=self.checkBoxDownstream.isChecked(),
            )
            self.iface.mapCanvas().setMapTool(self.catchment_map_tool)
        else:
            self.unset_map_tool()

    def pushbutton_catchment_for_selected_nodes_clicked(self):
        selected_node_ids = []
        for feature in self.gq.target_node_layer.getSelectedFeatures():
            selected_node_ids.append(feature.id())

        if len(selected_node_ids) == 0:
            self.iface.messageBar().pushMessage(
                MESSAGE_CATEGORY, "Please first select one or more target nodes", level=Qgis.Warning
            )
        else:
            if self.gq.graph_3di.isready:
                self.gq.upstream_downstream_analysis(
                    target_node_ids=selected_node_ids,
                    upstream=self.checkBoxUpstream.isChecked(),
                    downstream=self.checkBoxDownstream.isChecked(),
                )
            else:
                self.iface.messageBar().pushMessage(
                    MESSAGE_CATEGORY, "Please select 3Di results first", level=Qgis.Warning
                )

    def pushbutton_catchment_for_polygons_clicked(self):
        if self.gq.graph_3di.isready:
            polygon_lyr = self.mMapLayerComboBoxTargetPolygons.currentLayer()
            src_crs = polygon_lyr.crs()
            tgt_crs = QgsCoordinateReferenceSystem(f"EPSG:{self.gq.epsg}")
            tr = QgsCoordinateTransform(src_crs, tgt_crs, QgsProject.instance())

            if self.checkBoxSelectedPolygonsOnly.isChecked():
                polygon_features = polygon_lyr.getSelectedFeatures()
            else:
                polygon_features = polygon_lyr.getFeatures()
            for feat in polygon_features:
                target_node_ids = []
                geom = feat.geometry()
                geom.transform(tr)
                req = QgsFeatureRequest(geom.boundingBox())  # for performance
                for point in self.gq.target_node_layer.getFeatures(req):
                    if geom.contains(point.geometry()):
                        target_node_ids.append(point.id())
                self.gq.upstream_downstream_analysis(
                    target_node_ids=target_node_ids,
                    upstream=self.checkBoxUpstream.isChecked(),
                    downstream=self.checkBoxDownstream.isChecked(),
                )

    def pushbutton_clear_results_clicked(self):
        self.gq.clear_all()
        self.checkBoxBrowseResultSets.setEnabled(False)
        self.spinBoxBrowseResultSets.setValue(1)
        self.spinBoxBrowseResultSets.setMinimum(1)
        self.spinBoxBrowseResultSets.setMaximum(1)
        self.spinBoxBrowseResultSets.setEnabled(False)

    def checkbox_upstream_state_changed(self):
        try:
            if self.catchment_map_tool is not None:
                self.catchment_map_tool.upstream = self.checkBoxUpstream.isChecked()
        except AttributeError:
            pass

    def checkbox_downstream_state_changed(self):
        try:
            if self.catchment_map_tool is not None:
                self.catchment_map_tool.downstream = self.checkBoxDownstream.isChecked()
        except AttributeError:
            pass

    def checkbox_browse_result_sets_state_changed(self):
        self.spinBoxBrowseResultSets.setEnabled(self.checkBoxBrowseResultSets.isChecked())
        if self.checkBoxBrowseResultSets.isChecked():
            self.gq.filter = [self.spinBoxBrowseResultSets.value()]
        else:
            self.gq.filter = None
        self.gq.zoom_to_results()
        self.iface.mapCanvas().refreshAllLayers()

    def spinbox_browse_result_sets_value_changed(self):
        if self.checkBoxBrowseResultSets.isChecked():
            self.gq.filter = [self.spinBoxBrowseResultSets.value()]
            self.gq.zoom_to_results()
            self.iface.mapCanvas().refreshAllLayers()

    def result_sets_count_changed(self):
        if len(self.gq.result_sets) > 0:
            self.checkBoxBrowseResultSets.setEnabled(True)
            self.spinBoxBrowseResultSets.setMinimum(min(self.gq.result_sets))
            self.spinBoxBrowseResultSets.setMaximum(max(self.gq.result_sets))
            self.spinBoxBrowseResultSets.setValue(max(self.gq.result_sets))
            self.spinbox_browse_result_sets_value_changed()
        else:
            self.checkBoxBrowseResultSets.setEnabled(False)


class UpdateGridAdminTask(QgsTask):
    def __init__(self, description: str, parent: WatershedAnalystDockWidget, gr: GridH5ResultAdmin):
        super().__init__(description, QgsTask.CanCancel)
        self.exception = None
        self.parent = parent
        if not isinstance(gr, GridH5ResultAdmin):
            raise TypeError
        self.gr = gr
        self.parent.setEnabled(False)
        QgsMessageLog.logMessage("Started pre-processing simulation results", MESSAGE_CATEGORY, level=Qgis.Info)

    def run(self):
        try:
            self.parent.gq.gr = self.gr
            return True
        except Exception as e:
            self.exception = e

        return False

    def finished(self, result):
        if self.exception is not None:
            self.parent.setEnabled(True)
            self.parent.widget().repaint()
            raise self.exception
        if result:
            self.parent.gq.gr_updated()
            output_timestep_best_guess = int(
                self.parent.gq.gr.nodes.timestamps[-1] / (len(self.parent.gq.gr.nodes.timestamps) - 1)
            )
            start_time = 0
            end_time = int(self.parent.gq.gr.nodes.timestamps[-1])

            self.parent.doubleSpinBoxStartTime.setMaximum(end_time)
            self.parent.doubleSpinBoxStartTime.setSingleStep(output_timestep_best_guess)
            self.parent.doubleSpinBoxStartTime.setValue(start_time)

            self.parent.doubleSpinBoxEndTime.setMaximum(end_time)
            self.parent.doubleSpinBoxEndTime.setSingleStep(output_timestep_best_guess)
            self.parent.doubleSpinBoxEndTime.setValue(end_time)

            if self.parent.gq.result_catchment_layer.receivers(QgsVectorLayer.featureAdded) == 0:
                self.parent.gq.result_catchment_layer.featureAdded.connect(self.parent.result_sets_count_changed)

            if self.parent.gq.result_catchment_layer.receivers(QgsVectorLayer.featuresDeleted) == 0:
                self.parent.gq.result_catchment_layer.featuresDeleted.connect(self.parent.result_sets_count_changed)
            self.parent.setEnabled(True)
            QgsMessageLog.logMessage("Finished pre-processing simulation results", MESSAGE_CATEGORY, level=Qgis.Success)

        else:
            self.parent.setEnabled(True)
            QgsMessageLog.logMessage("Failed pre-processing simulation results", MESSAGE_CATEGORY, level=Qgis.Critical)

    def cancel(self):
        QgsMessageLog.logMessage(
            "Pre-processing simulation results cancelled by user", MESSAGE_CATEGORY, level=Qgis.Info
        )
        super().cancel()
