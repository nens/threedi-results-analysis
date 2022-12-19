import os
from collections import OrderedDict
import h5py
from osgeo import ogr

from threedigrid.admin.exporters.geopackage import GeopackageExporter
from qgis.PyQt.QtCore import QObject, pyqtSlot, pyqtSignal
from qgis.core import Qgis, QgsVectorLayer, QgsProject, QgsMapLayer

from ThreeDiToolbox.threedi_plugin_model import ThreeDiGridItem, ThreeDiResultItem
from ThreeDiToolbox.utils.constants import TOOLBOX_QGIS_GROUP_NAME
from ThreeDiToolbox.utils.user_messages import StatusProgressBar, messagebar_message, pop_up_critical
from ThreeDiToolbox.utils.utils import safe_join

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


class ThreeDiPluginLayerManager(QObject):
    """
    The Layer manager creates layers from a geopackage and keeps track
    of the connection between model items (grids) and layers.

    In case a model item is deleted, the corresponding layers are also
    deleted. In case all layers of a grid are deleted, the item in the model
    should also be deleted.
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

        messagebar_message(MSG_TITLE, "Added layers to the project")

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
        # As the result itself does not need to be preloaded (this data is accessed
        # via the tools), we just consider it loaded (and leave validation to the
        # validator)
        self.result_loaded.emit(threedi_result_item)
        return True

    @pyqtSlot(ThreeDiResultItem)
    def unload_result(self, threedi_result_item: ThreeDiResultItem) -> bool:
        # As the result itself does not need to be preloaded (this data is accessed
        # via the tools), we just consider it unloaded when the threedigrid wrapper
        # is destroyed (in the model)
        return True

    @dirty
    @pyqtSlot(ThreeDiResultItem)
    def update_result(self, item: ThreeDiResultItem) -> bool:
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

        invalid_layers = []
        empty_layers = []

        item.layer_group = ThreeDiPluginLayerManager._get_or_create_group(item.text())
        
        # Use to modify grid name when LayerGroup is renamed
        item.layer_group.nameChanged.connect(lambda _, text: item.setText(text))

        for layer_name, table_name in gpkg_layers.items():

            # Check whether the QgsProject already contains this layer
            if table_name in item.layer_ids.keys():
                if QgsProject.instance().mapLayer(item.layer_ids[table_name]):
                    logger.info(f"Map layer corresponding to table {table_name} already exist in project")
                    continue

            # Using the QgsInterface function addVectorLayer shows (annoying) confirmation dialogs
            # iface.addVectorLayer(gpkg_file + "|layername=" + layer, layer, 'ogr')
            vector_layer = QgsVectorLayer(str(path) + "|layername=" + table_name, layer_name, "ogr")
            if not vector_layer.isValid():
                invalid_layers.append(layer_name)
                continue

            # only load layers that contain some features
            if not vector_layer.featureCount():
                empty_layers.append(layer_name)
                continue

            # apply the style
            qml_path = safe_join(styles_dir, f"{table_name}.qml")
            if os.path.exists(qml_path):
                vector_layer.loadNamedStyle(qml_path)
                # prior to QGIS 3.24, this method would show an (annoying) message box
                # warning when a style with the same styleName already existed. Unfortunately,
                # QgsProviderRegistry::styleExists is not available in Python
                if table_name not in vector_layer.listStylesInDatabase()[2]:
                    vector_layer.saveStyleToDatabase(table_name, "", True, "")

            vector_layer.setReadOnly(True)
            vector_layer.setFlags(QgsMapLayer.Searchable | QgsMapLayer.Identifiable)

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
