# -*- coding: utf-8 -*-
import os
from PyQt4.QtCore import pyqtSignal, QSettings
from PyQt4.QtGui import QDialog, QFileDialog, QMessageBox
from PyQt4.QtSql import QSqlDatabase
from PyQt4 import uic
from qgis.core import QgsDataSourceURI, QgsVectorLayer, QgsMapLayerRegistry


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), os.pardir, 'ui', 'tool_dialog.ui'))


class ToolDialogWidget(QDialog, FORM_CLASS):
    closingDialog = pyqtSignal()

    def __init__(self, parent=None, iface=None, ts_datasource=None,
                 command=None):
        """Constructor

        Args:
            parent: Qt parent Widget
            iface: QGiS interface
            ts_datasource: TimeseriesDatasourceModel instance
            command: Command instance with a run_it method which will be called
                      on acceptance of the dialog
        """
        super(ToolDialogWidget, self).__init__(parent)
        self.setupUi(self)

        self.iface = iface
        self.ts_datasource = ts_datasource
        self.command = command
        # from ..qdebug import pyqt_set_trace; pyqt_set_trace()
        # self.layerComboBox.activated.connect(self.hello)
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)

    def on_accept(self):
        """Accept and run the Command.run_it method."""
        self.accept()
        self.command.run_it()

    def on_reject(self):
        """Cancel"""
        self.reject()
        print("Reject")

    def on_close_cleanup(self):
        """Clean object on close"""
        self.buttonBox.accepted.disconnect(self.on_accept)
        self.buttonBox.rejected.disconnect(self.on_reject)

    def closeEvent(self, event):
        """
        Close widget, called by Qt on close
        :param event: QEvent, close event
        """
        self.closingDialog.emit()
        self.on_close_cleanup()
        event.accept()
