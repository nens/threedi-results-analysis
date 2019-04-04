# -*- coding: utf-8 -*-
import os
import logging

from qgis.core import QgsProject

from qgis.PyQt import uic

from qgis.PyQt.QtCore import QRect
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtCore import QMetaObject
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.PyQt.QtWidgets import QGroupBox
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtWidgets import QSizePolicy
from qgis.PyQt.QtWidgets import QDialogButtonBox
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtWidgets import QDialog

from ThreeDiToolbox.utils.threedi_database import get_databases
from ThreeDiToolbox.threedi_schema_edits.breach_location import BreachLocation

log = logging.getLogger(__name__)


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)


except AttributeError:

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), os.pardir, "ui", "move_connected_pnts.ui")
)


class PredictCalcPointsDialogWidget(QDialog):
    def __init__(self, parent=None, command=None):
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
        self.database_combo.addItems(list(self.databases.keys()))

        # Connect signals
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)

        self.filename = None

    def on_accept(self):
        """Accept and run the Command.run_it method."""

        db_key = self.database_combo.currentText()
        db_entry = self.databases[db_key]

        _db_settings = db_entry["db_settings"]

        if db_entry["db_type"] == "spatialite":
            host = _db_settings["db_path"]
            db_settings = {
                "host": host,
                "port": "",
                "name": "",
                "username": "",
                "password": "",
                "schema": "",
                "database": "",
                "db_path": host,
            }
        else:
            db_settings = _db_settings
            db_settings["schema"] = "public"
        self.command.run_it(db_settings, db_entry["db_type"])

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
        self.resize(815, 250)
        self.verticalLayout = QVBoxLayout(self)

        self.groupBox_2 = QGroupBox(self)
        self.groupBox_2.setObjectName("groupBox_2")
        self.database_combo = QComboBox(self.groupBox_2)
        self.database_combo.setGeometry(QRect(10, 30, 481, 34))

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.database_combo.sizePolicy().hasHeightForWidth()
        )
        self.database_combo.setSizePolicy(sizePolicy)
        self.database_combo.setObjectName("database_combo")
        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self)
        self.verticalLayoutBox = QVBoxLayout(self.groupBox)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("self", "Predict calc points", None))
        self.groupBox_2.setTitle(
            _translate("self", "Model schematisation database", None)
        )


class AddCoonnectedPointsDialogWidget(QDialog):
    def __init__(self, parent=None, command=None):
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
        self.database_combo.addItems(list(self.databases.keys()))

        # Connect signals
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)

        self.filename = None

    def on_accept(self):
        """Accept and run the Command.run_it method."""

        db_key = self.database_combo.currentText()
        db_entry = self.databases[db_key]
        db_type = db_entry["db_type"]

        _db_settings = db_entry["db_settings"]

        if db_type == "spatialite":
            # usage of db_type 'spatialite' instead of 'sqlite'
            # makes much more sense because it also used internally
            # by qgis, for example when by the ``QgsVectorLayer()``-object
            host = _db_settings["db_path"]
            db_settings = {
                "host": host,
                "port": "",
                "name": "",
                "username": "",
                "password": "",
                "schema": "",
                "database": "",
                "db_path": host,
            }
        else:
            db_settings = _db_settings
            db_settings["schema"] = "public"
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

        self.resize(815, 250)
        self.verticalLayout = QVBoxLayout(self)

        self.groupBox_2 = QGroupBox(self)
        self.groupBox_2.setObjectName("groupBox_2")
        self.database_combo = QComboBox(self.groupBox_2)
        self.database_combo.setGeometry(QRect(10, 30, 481, 34))

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.database_combo.sizePolicy().hasHeightForWidth()
        )
        self.database_combo.setSizePolicy(sizePolicy)
        self.database_combo.setObjectName("database_combo")
        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self)
        self.verticalLayoutBox = QVBoxLayout(self.groupBox)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("self", "Add connected points", None))
        self.groupBox_2.setTitle(_translate("self", "Load from model database", None))


class CreateBreachLocationsDialogWidget(QDialog, FORM_CLASS):
    def __init__(self, parent=None, command=None):
        """Constructor
        Args:
            parent: Qt parent Widget
            iface: QGiS interface
            ts_datasource: TimeseriesDatasourceModel instance
            command: Command instance with a run_it method which will be called
                     on acceptance of the dialog
        """
        super(CreateBreachLocationsDialogWidget, self).__init__(parent)
        self.setupUi(self)
        # default maximum for QSpinBox is 99, so setValue is limited to 99.
        # That's why we set the Maximum to 5000
        self.spinbox_search_distance.setMaximum(5000)
        self.spinbox_search_distance.setMinimum(2)
        self.spinbox_levee_distace.setMaximum(5000)
        self.spinbox_levee_distace.setMinimum(1)
        self.setWindowTitle(_translate("self", "Create breach locations", None))
        tool_help = """
        Move connected points across the nearest levee. You can limit your
        point set to your current selection. Using the dry-run option will
        not save the new geometries to the database table yet but will store
        them to a memory layer called 'temp_connected_pnt'. Like this you can
        test your settings first before actually applying them to your model.
        Using the 'dry-run' option thus is highly recommended."""
        self.help_text_browser.setText(
            tool_help.replace("        ", "")
            .replace("\n", "")
            .replace("\r", "")
        )
        connected_pnt_lyr = QgsProject.instance().mapLayersByName("v2_connected_pnt")
        # automatically pre-select the right layer if present
        if connected_pnt_lyr:
            lyr = connected_pnt_lyr[0]
            self.connected_pny_lyr_box.setLayer(lyr)

        self.command = command
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)

    def on_accept(self):
        """Accept and run the Command.run_it method."""

        breach_loc = BreachLocation(
            search_distance=self.spinbox_search_distance.value(),
            distance_to_levee=self.spinbox_levee_distace.value(),
            use_selection=self.checkBox_feat.isChecked(),
            is_dry_run=self.checkBox_dry_run.isChecked(),
            connected_pnt_lyr=self.connected_pny_lyr_box.currentLayer(),
        )
        self.command.run_it(breach_loc, self.checkBox_auto_commit.isChecked())
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
        # self.buttonBox.accepted.disconnect(self.on_accept)
        # self.buttonBox.rejected.disconnect(self.on_reject)
        event.accept()
