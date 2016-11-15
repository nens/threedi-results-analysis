# -*- coding: utf-8 -*-
import logging
from PyQt4.QtGui import QDialog

from PyQt4.QtCore import SIGNAL, QRect, Qt, QObject, QMetaObject
from PyQt4.QtGui import (
    QVBoxLayout, QGroupBox, QComboBox, QSizePolicy,
    QDialogButtonBox, QApplication)

from ThreeDiToolbox.utils.threedi_database import get_databases

log = logging.getLogger(__name__)


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class PredictCalcPointsDialogWidget(QDialog):

    def __init__(self, parent=None,
                 command=None):
        """Constructor

        Args:
            parent: Qt parent Widget
            iface: QGiS interface
            ts_datasource: TimeseriesDatasourceModel instance
            command: Command instance with a run_it method which will be called
                     on acceptance of the dialog
        """
        super(PredictCalcPointsDialogWidget, self).__init__(parent)
        self.setupUi()

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
        db_entry = self.databases[db_key]

        _db_settings = db_entry['db_settings']

        if db_entry['db_type'] == 'spatialite':
            host = _db_settings['db_path']
            db_settings = {
                'host': host,
                'port': '',
                'name': '',
                'username':'',
                'password': '',
                'schema': '',
                'database': '',
                'db_path': host,
            }
        else:
            db_settings = _db_settings
            db_settings['schema'] = 'public'
        self.command.run_it(db_settings, db_type)

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


    def setupUi(self):


        self.resize(515, 250)
        self.verticalLayout = QVBoxLayout(self)

        self.groupBox_2 = QGroupBox(self)
        self.groupBox_2.setObjectName("groupBox_2")
        self.database_combo = QComboBox(self.groupBox_2)
        self.database_combo.setGeometry(QRect(10, 20, 481, 20))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.database_combo.sizePolicy().hasHeightForWidth())
        self.database_combo.setSizePolicy(sizePolicy)
        self.database_combo.setObjectName("database_combo")
        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self)
        self.verticalLayoutBox = QVBoxLayout(self.groupBox)


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
        self.setWindowTitle(_translate("self", "Predict calc points", None))
        self.groupBox_2.setTitle(_translate("self", "Model schematisation database", None))

class AddCoonnectedPointsDialogWidget(QDialog):

    def __init__(self, parent=None,
                 command=None):
        """Constructor

        Args:
            parent: Qt parent Widget
            iface: QGiS interface
            ts_datasource: TimeseriesDatasourceModel instance
            command: Command instance with a run_it method which will be called
                     on acceptance of the dialog
        """
        super(AddCoonnectedPointsDialogWidget, self).__init__(parent)
        self.setupUi()

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
        db_entry = self.databases[db_key]
        db_type = db_entry['db_type']

        _db_settings = db_entry['db_settings']

        if db_type == 'spatialite':
            # usage of db_type 'spatialite' instead of 'sqlite'
            # makes much more sense because it also used internally
            # by qgis, for example when by the ``QgsVectorLayer()``-object
            host = _db_settings['db_path']
            db_settings = {
                'host': host,
                'port': '',
                'name': '',
                'username':'',
                'password': '',
                'schema': '',
                'database': '',
                'db_path': host,
            }
        else:
            db_settings = _db_settings
            db_settings['schema'] = 'public'
        self.command.run_it(db_settings, db_type)

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


    def setupUi(self):

        self.resize(515, 250)
        self.verticalLayout = QVBoxLayout(self)

        self.groupBox_2 = QGroupBox(self)
        self.groupBox_2.setObjectName("groupBox_2")
        self.database_combo = QComboBox(self.groupBox_2)
        self.database_combo.setGeometry(QRect(10, 20, 481, 20))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.database_combo.sizePolicy().hasHeightForWidth())
        self.database_combo.setSizePolicy(sizePolicy)
        self.database_combo.setObjectName("database_combo")
        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self)
        self.verticalLayoutBox = QVBoxLayout(self.groupBox)


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
        self.setWindowTitle(_translate("self", "Add connected points", None))
        self.groupBox_2.setTitle(_translate("self", "Load from model database", None))
