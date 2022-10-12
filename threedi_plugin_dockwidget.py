import os
import sys
sys.path.append(os.path.dirname(__file__))

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'threedi_plugin_dockwidget_base.ui'))

class ThreeDiPluginDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    closingPlugin=pyqtSignal()
    
    def __init__(self,parent, provider):
        super(ThreeDiPluginDockWidget,self).__init__(parent)
        self.setupUi(self)
        self.pushButton_New.clicked.connect(self.new_clicked)
        
    # To check whether this is necessary
    def closeEvent(self,event):
        self.closingPlugin.emit()
        event.accept()

    def new_clicked(self):
        filename, _ = QFileDialog.getSaveFileName(self, "New geopackage", "", "GeoPackage (*.gpkg)")
