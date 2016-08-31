# -*- coding: utf-8 -*-
import os
from PyQt4.QtCore import pyqtSignal, QSettings
from PyQt4.QtGui import QDialog, QFileDialog, QMessageBox
from PyQt4.QtSql import QSqlDatabase
from PyQt4 import uic
from qgis.core import QgsDataSourceURI, QgsVectorLayer, QgsMapLayerRegistry


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), os.pardir, 'ui', 'import_sufhyd_dialog.ui'))


class ImportSufhydDialogWidget(QDialog, FORM_CLASS):

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
        super(ImportSufhydDialogWidget, self).__init__(parent)
        self.setupUi(self)

        self.iface = iface
        self.ts_datasource = ts_datasource
        self.command = command

        self.db_path = ts_datasource.model_spatialite_filepath
        self.database_combo.addItems(
            [ts_datasource.model_spatialite_filepath])

        self.file_button.clicked.connect(self.select_sufhyd_file)

        # Connect signals
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)

        self.filename = None

    def select_sufhyd_file(self):

        settings = QSettings('3di', 'qgisplugin')

        try:
            init_path = settings.value('last_used_import_path', type=str)
        except TypeError:
            init_path = os.path.expanduser("~")

        filename = QFileDialog.getOpenFileName(self,
                                            'Select import file',
                                            init_path ,
                                            'Sufhyd (*.hyd)')

        if filename:
            self.filename = filename
            self.file_combo.addItems([filename])

            settings.setValue('last_used_import_path',
                              os.path.dirname(filename))

    def on_accept(self):
        """Accept and run the Command.run_it method."""
        self.accept()


        self.command.run_it(self.filename, self.db_path)


    def on_reject(self):
        """Cancel"""
        self.reject()
        print("Reject")

    def closeEvent(self, event):
        """
        Close widget, called by Qt on close
        :param event: QEvent, close event
        """

        self.buttonBox.accepted.disconnect(self.on_accept)
        self.buttonBox.rejected.disconnect(self.on_reject)
        self.file_button.clicked.disconnect(self.select_sufhyd_file)

        event.accept()
