from logging import getLogger
from pathlib import Path

from ThreeDiToolbox.threedi_plugin_model import ThreeDiGridItem
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import QModelIndex
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.core import QgsSettings

logger = getLogger(__name__)

FORM_CLASS, _ = uic.loadUiType(
    Path(__file__).parent / 'threedi_plugin_dockwidget_base.ui',
)


class ThreeDiPluginDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    grid_file_selected = pyqtSignal(str)
    result_file_selected = pyqtSignal(str)
    grid_removal_selected = pyqtSignal(ThreeDiGridItem)

    item_selected = pyqtSignal(QModelIndex)
    item_deselected = pyqtSignal(QModelIndex)

    QSETTING_KEY_DIR = "ThreeDiPluginDockWidget.path"

    def __init__(self, parent):
        super(ThreeDiPluginDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_AddGrid.clicked.connect(self._add_grid_clicked)
        self.pushButton_AddResult.clicked.connect(self._add_result_clicked)
        self.pushButton_RemoveGrid.clicked.connect(self._remove_grid_clicked)

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

    def _remove_grid_clicked(self):
        index = self.treeView.selectionModel().currentIndex()
        if index is None or index.model() is None:
            return

        item = index.model().itemFromIndex(index)
        if isinstance(item, ThreeDiGridItem):
            self.grid_removal_selected.emit(item)

    def _add_result_clicked(self):
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
        self.result_file_selected.emit(input_result_nc)

    def _selection_changed(self, selected, deselected):
        deselected_indexes = deselected.indexes()
        if deselected_indexes:
            self.item_deselected.emit(deselected_indexes[0])
        selected_indexes = selected.indexes()
        if selected_indexes:
            self.item_selected.emit(selected_indexes[0])

    def _get_dir(self) -> str:
        value = QgsSettings().value(self.QSETTING_KEY_DIR)
        if value is None:
            return ""
        dir_path = Path(value)
        if not dir_path.is_dir():
            return ""
        return str(dir_path)

    def _set_dir(self, path: str):
        dir_path = Path(path).parent
        if dir_path.is_dir():
            QgsSettings().setValue(self.QSETTING_KEY_DIR, str(dir_path))
        else:
            QgsSettings().remove(self.QSETTING_KEY_DIR)
