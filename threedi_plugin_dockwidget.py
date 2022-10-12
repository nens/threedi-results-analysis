import os
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtCore import pyqtSignal
from qgis.core import Qgis
from qgis.utils import iface
from threedigrid.admin.exporters.geopackage import GeopackageExporter
from ThreeDiToolbox.utils.user_messages import progress_bar

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'threedi_plugin_dockwidget_base.ui'))

class ThreeDiPluginDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    closingPlugin=pyqtSignal()
    
    def __init__(self, parent):
        super(ThreeDiPluginDockWidget,self).__init__(parent)
        self.setupUi(self)
        self.pushButton_AddGrid.clicked.connect(self.add_grid_clicked)
        
    # To check whether this is necessary
    def closeEvent(self,event):
        self.closingPlugin.emit()
        event.accept()

    def add_grid_clicked(self):
        input_gridadmin_h5, _ = QFileDialog.getOpenFileName(self, "Load HDF5", "", "HDF5 (*.h5)")
        if not input_gridadmin_h5:
            return

        # Convert h5 file to gpkg
        input_gridadmin_base, _ = os.path.splitext(input_gridadmin_h5)
        input_gridadmin_gpkg = input_gridadmin_base + '.gpkg'
        exporter = GeopackageExporter(input_gridadmin_h5, input_gridadmin_gpkg)
        with progress_bar(iface) as pb:
            exporter.export(lambda count, total, pb=pb: pb.setValue((count * 100) // total))
        
        iface.messageBar().pushMessage("GeoPackage", "Generated geopackage", Qgis.Info)
