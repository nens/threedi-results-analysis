# -*- coding: utf-8 -*-
import logging

from PyQt4.QtCore import pyqtSignal, QSettings
from PyQt4.QtGui import QDialog
from PyQt4.QtSql import QSqlDatabase
from PyQt4.QtCore import SIGNAL, QRect, Qt, QObject, QMetaObject
from PyQt4.QtGui import (
    QVBoxLayout, QGroupBox, QWidget, QComboBox, QSizePolicy, QHBoxLayout,
    QCheckBox, QDialogButtonBox, QApplication)

from qgis.core import QgsDataSourceURI, QgsVectorLayer, QgsMapLayerRegistry
from qgis.gui import QgsCredentialDialog

from ThreeDiToolbox.utils.threedi_database import get_databases

log = logging.getLogger(__name__)


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class GuessIndicatorDialogWidget(QDialog):

    def __init__(self, parent=None, checks=[],
                 command=None):
        """Constructor

        Args:
            parent: Qt parent Widget
            iface: QGiS interface
            ts_datasource: TimeseriesDatasourceModel instance
            command: Command instance with a run_it method which will be called
                     on acceptance of the dialog
        """
        super(GuessIndicatorDialogWidget, self).__init__(parent)
        self.checks = checks
        self.setupUi(checks)

        self.command = command

        self.databases = get_databases()
        self.database_combo.addItems(self.databases.keys())

        # Connect signals
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)

        self.filename = None

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

                uri = QgsDataSourceURI()
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
                try:
                    # port can be an empty string, e.g. for spatialite db's
                    db.setPort(int(uri.port()))
                except ValueError:
                    pass
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

        checks = []

        if self.check_manhole_indicator.isChecked():
            checks.append('manhole_indicator')

        if self.check_pipe_friction.isChecked():
            checks.append('pipe_friction')

        if self.check_manhole_area.isChecked():
            checks.append('manhole_area')

        self.command.run_it(checks,
                            self.check_only_empty_fields.isChecked(),
                            db_set,
                            settings['db_type'])

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

        event.accept()

    def setupUi(self, checks):

        self.resize(515, 250)
        self.verticalLayout = QVBoxLayout(self)

        # self.file_combo = QComboBox(self.horizontalLayoutWidget)
        # sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.file_combo.sizePolicy().hasHeightForWidth())
        # self.file_combo.setSizePolicy(sizePolicy)
        # self.file_combo.setObjectName("file_combo")
        # self.horizontalLayout.addWidget(self.file_combo)
        #
        # self.file_button = QPushButton(self.horizontalLayoutWidget)
        # self.file_button.setObjectName("file_button")
        # self.horizontalLayout.addWidget(self.file_button)

        self.groupBox_2 = QGroupBox(self)
        self.groupBox_2.setObjectName("groupBox_2")
        self.database_combo = QComboBox(self.groupBox_2)
        self.database_combo.setGeometry(QRect(10, 20, 481, 20))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.database_combo.sizePolicy().hasHeightForWidth())
        self.database_combo.setSizePolicy(sizePolicy)
        self.database_combo.setObjectName("database_combo")
        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self)
        self.verticalLayoutBox = QVBoxLayout(self.groupBox)

        self.check_pipe_friction = QCheckBox(self.groupBox)
        self.check_pipe_friction.setChecked(True)
        self.verticalLayoutBox.addWidget(self.check_pipe_friction)

        self.check_manhole_indicator = QCheckBox(self.groupBox)
        self.check_manhole_indicator.setChecked(True)
        self.verticalLayoutBox.addWidget(self.check_manhole_indicator)

        self.check_manhole_area = QCheckBox(self.groupBox)
        self.check_manhole_area.setChecked(True)
        self.verticalLayoutBox.addWidget(self.check_manhole_area)

        self.verticalLayout.addWidget(self.groupBox)

        self.check_only_empty_fields = QCheckBox(self)
        self.check_only_empty_fields.setChecked(True)
        self.verticalLayout.addWidget(self.check_only_empty_fields)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        QObject.connect(self.buttonBox, SIGNAL("accepted()"),
                        self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"),
                        self.reject)
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("self", "Guess indicators", None))
        self.groupBox_2.setTitle(_translate(
            "self", "Model schematisation database", None))

        self.groupBox.setTitle(_translate("Import_dialog", "Guess", None))
        self.check_pipe_friction.setText(_translate(
            "Import_dialog", "Pipe friction", None))
        self.check_manhole_indicator.setText(_translate(
            "Import_dialog", "Manhole indicator", None))
        self.check_only_empty_fields.setText(
            _translate("Import_dialog", "Only null fields", None))
        self.check_manhole_area.setText(_translate(
            "Import_dialog", "Manhole area (only null fields)", None))
