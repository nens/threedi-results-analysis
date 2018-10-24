# -*- coding: utf-8 -*-
import os
import logging
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtWidgets import QDialog, QFileDialog
from qgis.PyQt.QtSql import QSqlDatabase
from qgis.PyQt import uic
from qgis.core import QgsDataSourceUri
from qgis.gui import QgsCredentialDialog
from ThreeDiToolbox.utils.threedi_database import get_databases
log = logging.getLogger(__name__)


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
        self.databases = get_databases()
        self.database_combo.addItems(
            list(self.databases.keys()))

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

        filename, __ = QFileDialog.getOpenFileName(self,
                                               'Select import file',
                                               init_path,
                                               'Sufhyd (*.hyd)')

        if filename:
            self.filename = filename
            self.file_combo.addItems([filename])

            settings.setValue('last_used_import_path',
                              os.path.dirname(filename))

    def on_accept(self):
        """Accept and run the Command.run_it method."""

        db_key = self.database_combo.currentText()

        settings = self.databases[db_key]
        db_set = settings['db_settings']

        if settings['db_type'] == 'spatialite':
            pass
        else:  # postgres

            successful_connection = False

            uname = db_set['username']
            passwd = db_set['password']
            msg = 'Log in'

            while not successful_connection:

                uri = QgsDataSourceUri()
                uri.setConnection(db_set['host'],
                                  db_set['port'],
                                  db_set['database'],
                                  db_set['username'],
                                  db_set['password'])

                # try to connect
                # create a PostgreSQL connection using QSqlDatabase
                db = QSqlDatabase.addDatabase('QPSQL')
                # check to see if it is valid

                db.setHostName(uri.host())
                db.setDatabaseName(uri.database())
                db.setPort(int(uri.port()))
                db.setUserName(uri.username())
                db.setPassword(uri.password())

                # open (create) the connection
                if db.open():
                    successful_connection = True
                    break
                else:
                    # todo - provide feedback what is wrong
                    pass

                connInfo = uri.connectionInfo()
                (success, uname, passwd) = QgsCredentialDialog.instance().get(
                    connInfo, uname, passwd, msg)

                if success:
                    db_set['username'] = passwd
                    db_set['password'] = uname
                else:
                    return

        self.command.run_it(self.filename, db_set, settings['db_type'])

        self.accept()

    def on_reject(self):
        """Cancel"""
        self.reject()
        log.debug("Reject")

    def closeEvent(self, event):
        """
        Close widget, called by Qt on close
        :param event: QEvent, close event
        """

        self.buttonBox.accepted.disconnect(self.on_accept)
        self.buttonBox.rejected.disconnect(self.on_reject)
        self.file_button.clicked.disconnect(self.select_sufhyd_file)

        event.accept()
