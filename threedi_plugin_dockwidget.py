import os
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import QModelIndex

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'threedi_plugin_dockwidget_base.ui'))


class ThreeDiPluginDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    closingPlugin = pyqtSignal()
    grid_file_selected = pyqtSignal(str)
    result_file_selected = pyqtSignal(str)
    result_selected = pyqtSignal(QModelIndex)
    result_deselected = pyqtSignal(QModelIndex)

    def __init__(self, parent):
        super(ThreeDiPluginDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_AddGrid.clicked.connect(self._add_grid_clicked)
        self.pushButton_AddResult.clicked.connect(self._add_result_clicked)

    # TODO: check whether this is necessary
    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

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

    def _add_result_clicked(self):
        input_result_nc, _ = QFileDialog.getOpenFileName(self, "Load NetCDF", "", "NetCDF (*.nc)")
        if not input_result_nc:
            return

        self.result_file_selected.emit(input_result_nc)

    def _selection_changed(self, selected, deselected):
        deselected_indexes = deselected.indexes()
        if deselected_indexes:
            self.result_deselected.emit(deselected_indexes[0])
        selected_indexes = selected.indexes()
        if selected_indexes:
            self.result_selected.emit(selected_indexes[0])
