from pathlib import Path
from qgis.PyQt import QtWidgets
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QDockWidget

import logging


logger = logging.getLogger(__name__)

ui_file = Path(__file__).parent / "dockwidget.ui"
assert ui_file.is_file()
FORM_CLASS, _ = uic.loadUiType(ui_file)


class ControlStructuresDockWidget(QDockWidget, FORM_CLASS):

    closingWidget = pyqtSignal()

    def __init__(self, iface=None, command=None):
        """Constructor."""
        super().__init__()  # iface.mainWindow()
        # Set up the user interface from Designer.
        self.setupUi(self)
        # See https://wiki.qt.io/PySide_Pitfalls.
        self.keep_reference_so_it_doesnt_garbage_collect = command

    def closeEvent(self, event):
        self.closingWidget.emit()
        event.accept()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    controlStructureDockWidget = ControlStructuresDockWidget()
    controlStructureDockWidget.show()
    sys.exit(app.exec_())
