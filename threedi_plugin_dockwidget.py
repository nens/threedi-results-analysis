import os
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import QModelIndex
from ThreeDiToolbox.threedi_plugin_model import ThreeDiGridItem
import logging

logger = logging.getLogger(__name__)

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'threedi_plugin_dockwidget_base.ui'))


class ThreeDiPluginDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    grid_file_selected = pyqtSignal(str)
    result_file_selected = pyqtSignal(str)
    grid_removal_selected = pyqtSignal(ThreeDiGridItem)

    item_selected = pyqtSignal(QModelIndex)
    item_deselected = pyqtSignal(QModelIndex)

    def __init__(self, parent):
        super(ThreeDiPluginDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_AddGrid.clicked.connect(self._add_grid_clicked)
        self.pushButton_AddResult.clicked.connect(self._add_result_clicked)
        self.pushButton_RemoveGrid.clicked.connect(self._remove_grid_clicked)

    def _add_grid_clicked(self):
        input_gridadmin_h5_or_gpkg, _ = QFileDialog.getOpenFileName(
            self,
            "Load HDF5 or GeoPackage",
            "",
            "HDF5 or GeoPackage (*.h5 *.gpkg)",
        )
        if not input_gridadmin_h5_or_gpkg:
            return

        self.grid_file_selected.emit(input_gridadmin_h5_or_gpkg)

    def _remove_grid_clicked(self):
        index = self.treeView.selectionModel().currentIndex()
        if index is None or index.model() is None:
            return

        item = index.model().itemFromIndex(index)
        if isinstance(item, ThreeDiGridItem):
            self.grid_removal_selected.emit(item)

    def _add_result_clicked(self):
        input_result_nc, _ = QFileDialog.getOpenFileName(self, "Load NetCDF", "", "NetCDF (*.nc)")
        if not input_result_nc:
            return

        self.result_file_selected.emit(input_result_nc)

    def _selection_changed(self, selected, deselected):
        deselected_indexes = deselected.indexes()
        if deselected_indexes:
            self.item_deselected.emit(deselected_indexes[0])
        selected_indexes = selected.indexes()
        if selected_indexes:
            self.item_selected.emit(selected_indexes[0])
