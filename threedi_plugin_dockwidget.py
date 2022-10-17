import os
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'threedi_plugin_dockwidget_base.ui'))

class ThreeDiPluginDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    closingPlugin=pyqtSignal()
    grid_file_selected = pyqtSignal(str)
    result_file_selected = pyqtSignal(str)
    
    def __init__(self, parent):
        super(ThreeDiPluginDockWidget,self).__init__(parent)
        self.setupUi(self)
        self.pushButton_AddGrid.clicked.connect(self._add_grid_clicked)
        self.pushButton_AddResult.clicked.connect(self._add_result_clicked)
        
    # TODO: check whether this is necessary
    def closeEvent(self,event):
        self.closingPlugin.emit()
        event.accept()

    def _add_grid_clicked(self):
        input_gridadmin_h5, _ = QFileDialog.getOpenFileName(self, "Load HDF5", "", "HDF5 (*.h5)")
        if not input_gridadmin_h5:
            return

        self.grid_file_selected.emit(input_gridadmin_h5)

    def _add_result_clicked(self):
        input_gridadmin_netcdf, _ = QFileDialog.getOpenFileName(self, "Load NetCDF", "", "NetCDF (*.nc)")
        if not input_gridadmin_netcdf:
            return

        self.result_file_selected.emit(input_gridadmin_netcdf)
