from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QDockWidget

import logging
import os


logger = logging.getLogger(__name__)

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(
        os.path.dirname(__file__), "..", "ui", "control_structures_dockwidget.ui"
    )
)


class ControlStructuresDockWidget(QDockWidget, FORM_CLASS):

    closingWidget = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)
        # Set up the user interface from Designer.
        self.setupUi(self)

    def closeEvent(self, event):
        self.closingWidget.emit()
        event.accept()
