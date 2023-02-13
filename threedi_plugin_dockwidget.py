from logging import getLogger
from pathlib import Path

from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem
from threedi_results_analysis.utils.constants import TOOLBOX_QGIS_SETTINGS_GROUP
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import QModelIndex
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.core import QgsSettings
from qgis.PyQt.QtGui import QPixmap
from threedi_results_analysis import PLUGIN_DIR

logger = getLogger(__name__)

FORM_CLASS, _ = uic.loadUiType(
    Path(__file__).parent / 'threedi_plugin_dockwidget_base.ui',
)


class ThreeDiPluginDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    grid_file_selected = pyqtSignal(str)
    result_file_selected = pyqtSignal(str, ThreeDiGridItem)
    remove_current_index_clicked = pyqtSignal(QModelIndex)

    item_selected = pyqtSignal(QModelIndex)
    item_deselected = pyqtSignal(QModelIndex)

    def __init__(self, parent):
        super(ThreeDiPluginDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_AddGrid.clicked.connect(self._add_grid_clicked)
        self.pushButton_AddResult.clicked.connect(self._add_result_clicked)
        self.pushButton_RemoveItem.clicked.connect(self._remove_current_index_clicked)

        # Set logo
        path_3di_logo = str(PLUGIN_DIR / "icons" / "icon.png")
        logo_3di = QPixmap(path_3di_logo)
        logo_3di = logo_3di.scaledToHeight(30)
        self.logo.setPixmap(logo_3di)

    def set_model(self, model):

        tree_view = self.treeView
        tree_view.setModel(model)

        tree_view.selectionModel().selectionChanged.connect(self._selection_changed)
        tree_view.setColumnWidth(1, 65)

        header = tree_view.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)
        header.setSectionResizeMode(1, header.ResizeMode.Fixed)

    def get_tools_widget(self):
        return self.toolWidget

    def _add_grid_clicked(self):
        dir_path = self._get_dir()
        input_gridadmin_h5_or_gpkg, _ = QFileDialog.getOpenFileName(
            self,
            "Load HDF5 or GeoPackage",
            dir_path,
            "HDF5 or GeoPackage (*.h5 *.gpkg)",
        )
        if not input_gridadmin_h5_or_gpkg:
            return
        self._set_dir(input_gridadmin_h5_or_gpkg)
        self.grid_file_selected.emit(input_gridadmin_h5_or_gpkg)

    def _add_result_clicked(self):
        index = self.treeView.selectionModel().currentIndex()
        if index is None:
            return

        model = self.treeView.model()

        item = model.itemFromIndex(index)
        if not isinstance(item, ThreeDiGridItem):
            return

        dir_path = self._get_dir()
        input_result_nc, _ = QFileDialog.getOpenFileName(
            self,
            "Load NetCDF",
            dir_path,
            "NetCDF (*.nc)"
        )
        if not input_result_nc:
            return
        self._set_dir(input_result_nc)
        self.result_file_selected.emit(input_result_nc, item)

    def _remove_current_index_clicked(self):
        # not that index is the "current", not the "selected"
        index = self.treeView.selectionModel().currentIndex()
        if index is not None:
            self.remove_current_index_clicked.emit(index)

    def _selection_changed(self, selected, deselected):
        deselected_indexes = deselected.indexes()
        if deselected_indexes:
            self.item_deselected.emit(deselected_indexes[0])
        selected_indexes = selected.indexes()
        if selected_indexes:
            self.item_selected.emit(selected_indexes[0])

    def _get_dir(self) -> str:
        value = QgsSettings().value(TOOLBOX_QGIS_SETTINGS_GROUP + "/lastOpenDir")
        if value is None:
            return ""
        dir_path = Path(value)
        if not dir_path.is_dir():
            return ""
        return str(dir_path)

    def _set_dir(self, path: str):
        dir_path = Path(path).parent
        if dir_path.is_dir():
            QgsSettings().setValue(TOOLBOX_QGIS_SETTINGS_GROUP + "/lastOpenDir", str(dir_path))
        else:
            QgsSettings().remove(TOOLBOX_QGIS_SETTINGS_GROUP + "/lastOpenDir")

    @pyqtSlot()
    def toggle_visible(self, *args, **kwargs):
        self.setVisible(not self.isVisible())

    @pyqtSlot(ThreeDiGridItem)
    def expand_grid(self, item: ThreeDiGridItem):
        index = self.treeView.model().indexFromItem(item)
        self.treeView.expand(index)
        selection_model = self.treeView.selectionModel()
        # Deselect other grids
        selection_model.clearSelection()

        selection_model.setCurrentIndex(index, selection_model.Select)
