import os
from collections import OrderedDict
import h5py
from osgeo import ogr
import uuid
from PyQt5.QtCore import Qt
from threedigrid.admin.exporters.geopackage import GeopackageExporter
from qgis.PyQt.QtCore import QObject, pyqtSlot, pyqtSignal, QVariant
from qgis.core import Qgis, QgsVectorLayer, QgsProject, QgsMapLayer, QgsField, QgsWkbTypes, QgsLayerTreeNode
from ThreeDiToolbox.threedi_plugin_model import ThreeDiGridItem, ThreeDiResultItem
from ThreeDiToolbox.utils.constants import TOOLBOX_QGIS_GROUP_NAME
from ThreeDiToolbox.utils.user_messages import StatusProgressBar, messagebar_message, pop_up_critical
from ThreeDiToolbox.utils.utils import safe_join
from qgis.utils import iface

styles_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "layer_styles", "grid")

import logging
logger = logging.getLogger(__name__)

MSG_TITLE = "3Di Results Manager"


def dirty(func):
    """
    This decorator ensures the QGIS project is marked as dirty when
    the function is done.
    """
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        QgsProject.instance().setDirty()
    return wrapper


def copy_layer_into_memory_layer(source_layer, layer_name, dest_layer):

    source_provider = source_layer.dataProvider()

    uri = "{0}?crs=EPSG:{1}".format(
        QgsWkbTypes.displayString(source_provider.wkbType()).lstrip("WKB"),
        str(source_provider.crs().postgisSrid()),
    )

    if dest_layer is None:
        dest_layer = QgsVectorLayer(uri, layer_name, "memory")
    else:
        logger.info("Reusing memory layer instance")

    dest_provider = dest_layer.dataProvider()

    dest_provider.addAttributes(source_provider.fields())
    dest_layer.updateFields()

    dest_provider.addFeatures(source_provider.getFeatures())
    dest_layer.updateExtents()

    return dest_layer


# Layers need to be in specific order and naming:
gpkg_layers = OrderedDict(
    [
        ("Pump (point)", "pump"),
        ("Node", "node"),
        ("Pump (line)", "pump_linestring"),
        ("Flowline", "flowline"),
        ("Cell", "cell"),
        ("Obstacle", "obstacle"),
    ]
)


class ThreeDiPluginLayerManager(QObject):
    """
    The Layer manager creates layers from a geopackage and keeps track
    of the connection between model items (grids) and layers.

    In case a model item is deleted, the corresponding layers are also
    deleted.
    """
    grid_loaded = pyqtSignal(ThreeDiGridItem)
    result_loaded = pyqtSignal(ThreeDiResultItem)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @pyqtSlot(ThreeDiGridItem)
    def load_grid(self, item: ThreeDiGridItem) -> bool:
        # generate geopackage if needed and point item path to it
        if item.path.suffix == ".h5":
            path_h5 = item.path
            path_gpkg = path_h5.with_suffix(".gpkg")
            if not path_gpkg.exists():
                self.__class__._generate_gpkg(path_h5=path_h5, path_gpkg=path_gpkg)
            item.path = path_gpkg
        else:
            path_gpkg = item.path

        if not ThreeDiPluginLayerManager._add_layers_from_gpkg(path_gpkg, item):
            pop_up_critical("Failed adding the layers to the project.")
            return False

        messagebar_message(MSG_TITLE, "Added layers to the project", duration=2)

        self.grid_loaded.emit(item)
        return True

    @pyqtSlot(ThreeDiGridItem)
    def unload_grid(self, item: ThreeDiGridItem) -> bool:
        """Removes the corresponding layers from the group in the project"""

        # TODO: does the layer also need to be removed from registry?

        # It could be possible that some layers have been dragged outside the
        # layer group. Delete the individual layers first
        for layer_id in item.layer_ids.values():
            assert QgsProject.instance().mapLayer(layer_id)
            QgsProject.instance().removeMapLayer(layer_id)
        item.layer_ids.clear()

        # Deletion of root node of a tree will delete all nodes of the tree
        assert item.layer_group
        item.layer_group.parent().removeChildNode(item.layer_group)
        item.layer_group = None

    @dirty
    @pyqtSlot(ThreeDiGridItem)
    def update_grid(self, item: ThreeDiGridItem) -> bool:
        """Updates the group name in the project"""
        assert item.layer_group
        item.layer_group.setName(item.text())
        return True

    @pyqtSlot(ThreeDiResultItem)
    def load_result(self, threedi_result_item: ThreeDiResultItem) -> bool:
        # Add result fields for this result to the grid layers
        grid_item = threedi_result_item.parent()
        assert isinstance(grid_item, ThreeDiGridItem)

        logger.info("Adding result fields to grid layers")
        for layer_id in grid_item.layer_ids.values():
            layer = QgsProject.instance().mapLayer(layer_id)
            provider = layer.dataProvider()

            # Generate a random field name, with the result text
            # as alias (display) name.
            unique_identifier = str(uuid.uuid4())

            result_field_name = "result_" + unique_identifier
            result_field = QgsField(result_field_name, QVariant.Double)
            result_field.setAlias(threedi_result_item.text())

            initial_value_field_name = "initial_value_" + unique_identifier
            initial_value_field = QgsField(initial_value_field_name, QVariant.Double)
            initial_value_field.setAlias(threedi_result_item.text() + "_initial_value")

            # Check for duplicate field names (even though QGIS does not allow
            # addition of QgsFields (both attribute or expression) with already
            # existing names AND the generated layers are marked READONLY)
            if (layer.fields().indexFromName(result_field_name) != -1 or
                    layer.fields().indexFromName(initial_value_field_name) != -1):
                logger.error("Field already exist, aborting addition.")
                return False

            provider.addAttributes([result_field, initial_value_field])
            layer.updateFields()

            # Store the added field names so we can remove the field when the result is removed
            threedi_result_item._result_field_names[layer_id] = (result_field_name, initial_value_field_name)

        self.result_loaded.emit(threedi_result_item)
        return True

    @pyqtSlot(ThreeDiResultItem)
    def unload_result(self, threedi_result_item: ThreeDiResultItem) -> bool:
        # Remove the corresponding result fields from the grid layers
        for layer_id, result_field_names in threedi_result_item._result_field_names.items():
            # It could be that the map layer is removed by QGIS
            if QgsProject.instance().mapLayer(layer_id) is not None:
                layer = QgsProject.instance().mapLayer(layer_id)
                provider = layer.dataProvider()

                assert len(result_field_names) == 2
                idx = layer.fields().indexFromName(result_field_names[0])
                assert idx != -1
                provider.deleteAttributes([idx])
                layer.updateFields()

                idx = layer.fields().indexFromName(result_field_names[1])
                assert idx != -1
                provider.deleteAttributes([idx])
                layer.updateFields()

        threedi_result_item._result_field_names.clear()
        return True

    @dirty
    @pyqtSlot(ThreeDiResultItem)
    def result_unchecked(self, item: ThreeDiResultItem):
        # In case all results are unchecked, revert back to default styling (and naming)
        grid_item = item.parent()
        assert isinstance(grid_item, ThreeDiGridItem)
        if grid_item.hasChildren():
            for i in range(grid_item.rowCount()):
                result_item = grid_item.child(i)
                if result_item.checkState == Qt.Checked:
                    return

        for layer_name, table_name in gpkg_layers.items():
            scratch_layer = None
            assert table_name in grid_item.layer_ids.keys()
            scratch_layer = QgsProject.instance().mapLayer(grid_item.layer_ids[table_name])
            assert scratch_layer

            # (Re)apply the style and naming
            qml_path = safe_join(styles_dir, f"{table_name}.qml")
            if os.path.exists(qml_path):
                msg, res = scratch_layer.loadNamedStyle(qml_path)
                if not res:
                    logger.error(f"Unable to load style: {msg}")

            scratch_layer.setName(layer_name)
            iface.layerTreeView().refreshLayerSymbology(scratch_layer.id())
            scratch_layer.triggerRepaint()

    @dirty
    @pyqtSlot(ThreeDiResultItem)
    def update_result(self, threedi_result_item: ThreeDiResultItem) -> bool:
        # Update the display name of the result fields
        logger.info("Updating result fields")
        for layer_id, result_field_names in threedi_result_item._result_field_names.items():
            layer = QgsProject.instance().mapLayer(layer_id)

            assert len(result_field_names) == 2
            idx = layer.fields().indexFromName(result_field_names[0])
            assert idx != -1
            layer.setFieldAlias(idx, threedi_result_item.text())

            idx = layer.fields().indexFromName(result_field_names[1])
            assert idx != -1
            layer.setFieldAlias(idx, threedi_result_item.text() + '_initial_value')

        return True

    @staticmethod
    def _generate_gpkg(path_h5, path_gpkg) -> None:
        progress_bar = StatusProgressBar(100, "Generating geopackage")
        exporter = GeopackageExporter(str(path_h5), str(path_gpkg))
        exporter.export(
            lambda count, total, pb=progress_bar: pb.set_value((count * 100) // total)
        )
        del progress_bar

        # Copy some info from h5 to geopackage for future validation
        # TODO: should be added to threedigrid
        try:
            h5 = h5py.File(path_h5, "r")
            model_slug = h5.attrs['model_slug'].decode()
            logger.info(f"Model slug: {model_slug}")
            driver = ogr.GetDriverByName('GPKG')
            package = driver.Open(str(path_gpkg), True)
            package.SetMetadataItem('model_slug', model_slug)
        except Exception:
            logger.error("Unable to extract meta information from h5 file")

        messagebar_message(MSG_TITLE, "Generated geopackage")

    @staticmethod
    def _add_layers_from_gpkg(path, item: ThreeDiGridItem) -> bool:
        """
        Retrieves (a subset of the) layers from gpk and add to project.
        """

        invalid_layers = []
        empty_layers = []

        item.layer_group = ThreeDiPluginLayerManager._get_or_create_group(item.text())

        # Use to modify grid name when LayerGroup is renamed
        item.layer_group.nameChanged.connect(lambda node, txt, grid_item=item: ThreeDiPluginLayerManager._layer_node_renamed(node, txt, grid_item))

        for layer_name, table_name in gpkg_layers.items():

            # QGIS does save memory layers to the project file (but without the data)
            # Removing the scratch layer and resaving the project causes QGIS to crash,
            # therefore we reuse the layer instance.
            scratch_layer = None
            if table_name in item.layer_ids.keys():
                scratch_layer = QgsProject.instance().mapLayer(item.layer_ids[table_name])
                if scratch_layer:
                    logger.info(f"Map layer corresponding to table {item.layer_ids[table_name]} already exist in project, reusing...")

            # Using the QgsInterface function addVectorLayer shows (annoying) confirmation dialogs
            # iface.addVectorLayer(gpkg_file + "|layername=" + layer, layer, 'ogr')
            vector_layer = QgsVectorLayer(str(path) + "|layername=" + table_name, layer_name, "ogr")
            if not vector_layer.isValid():
                invalid_layers.append(layer_name)
                continue

            # Only load layers that contain some features
            if not vector_layer.featureCount():
                empty_layers.append(layer_name)
                continue

            vector_layer = copy_layer_into_memory_layer(
                vector_layer, layer_name, scratch_layer
            )

            # Apply the style
            qml_path = safe_join(styles_dir, f"{table_name}.qml")
            if os.path.exists(qml_path):
                msg, res = vector_layer.loadNamedStyle(qml_path)
                if not res:
                    logger.error(f"Unable to load style: {msg}")
                # prior to QGIS 3.24, saveStyleToDatabase would show an (annoying) message box
                # warning when a style with the same styleName already existed. Unfortunately,
                # QgsProviderRegistry::styleExists is not available in Python
                # if table_name not in vector_layer.listStylesInDatabase()[2]:
                    # Memory providers do not support saving of styles, commented
                    # msg = vector_layer.saveStyleToDatabase(table_name, "", True, "")
                    # if msg:
                    #    logger.error(f"Unable to save style to DB: {msg}")

            vector_layer.setReadOnly(True)
            vector_layer.setFlags(QgsMapLayer.Searchable | QgsMapLayer.Identifiable)

            if scratch_layer is None:
                # Keep track of layer id for future reference (deletion of grid item)
                item.layer_ids[table_name] = vector_layer.id()

                QgsProject.instance().addMapLayer(vector_layer, addToLegend=False)
                item.layer_group.addLayer(vector_layer)

        # Invalid layers info
        if invalid_layers:
            invalid_info = "\n\nThe following layers are missing or invalid:\n * " + "\n * ".join(invalid_layers) + "\n\n"
            messagebar_message(MSG_TITLE, invalid_info, Qgis.Warning)

        # Empty layers info
        if empty_layers:
            empty_info = "\n\nThe following layers contained no feature:\n * " + "\n * ".join(empty_layers) + "\n\n"
            messagebar_message(MSG_TITLE, empty_info, Qgis.Warning,)

        return True

    @staticmethod
    def _get_or_create_group(group_name: str):
        root = QgsProject.instance().layerTreeRoot()
        root_group = root.findGroup(TOOLBOX_QGIS_GROUP_NAME)
        if not root_group:
            root_group = root.insertGroup(0, TOOLBOX_QGIS_GROUP_NAME)

        layer_group = root_group.findGroup(group_name)
        if not layer_group:
            layer_group = root_group.insertGroup(0, group_name)

        return layer_group

    @staticmethod
    def _layer_node_renamed(node: QgsLayerTreeNode, text: str, item: ThreeDiGridItem):
        if node is item.layer_group:
            item.setText(text)
