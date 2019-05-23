# (c) Nelen & Schuurmans, see LICENSE.rst.

from qgis.PyQt.QtCore import QMetaObject
from qgis.PyQt.QtCore import QRect
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QCheckBox
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QDialogButtonBox
from qgis.PyQt.QtWidgets import QGroupBox
from qgis.PyQt.QtWidgets import QSizePolicy
from qgis.PyQt.QtWidgets import QVBoxLayout
from ThreeDiToolbox.utils.threedi_database import get_databases

import logging
import os


logger = logging.getLogger(__name__)


class RasterCheckerDialogWidget(QDialog):
    def __init__(self, parent=None, checks=[], command=None):
        """Constructor
        Args:
            parent: Qt parent Widget
            iface: QGiS interface
            ts_datasource: TimeseriesDatasourceModel instance
            command: Command instance with a run_it method which will be
                     called on acceptance of the dialog
        """
        super(RasterCheckerDialogWidget, self).__init__(parent)
        self.checks = checks
        self.setupUi(checks)
        self.command = command

        # rasterchecker only works on spatialte db (and not also postgres db)
        self.databases = {}
        self.all_databases = get_databases()
        for k, v in self.all_databases.items():
            if "spatialite" in k:
                if v["db_name"]:
                    self.databases[k] = v

        self.database_combo.addItems(self.databases.keys())

        # Connect signals
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)

    def on_accept(self):
        """Accept and run the Command.run_it method."""
        db_key = self.database_combo.currentText()
        settings = self.databases[db_key]
        db_set = settings["db_settings"]

        if not os.path.isfile(db_set["db_path"]):
            msg = "sqlite %s not found" % str(db_set["db_path"])
            raise Exception(msg)

        # TODO: check_all_rasters always runs. Enable check per model entree
        checks = []
        if self.check_all_rasters.isChecked():
            checks.append("check all rasters")
            # TODO: write improve first
            # improve_when_necessary may only be checked when
            # 'check_all_rasters' is checked
            # if self.improve_when_necessary.isChecked():
            #     checks.append('improve when necessary')

        self.command.run_it(checks, db_set, settings["db_type"])
        self.accept()

    def on_reject(self):
        """Cancel"""
        self.reject()
        logger.debug("Reject")

    def closeEvent(self, event):
        """
        Close widget, called by Qt on close
        :param event: QEvent, close event
        """
        self.buttonBox.accepted.disconnect(self.on_accept)
        self.buttonBox.rejected.disconnect(self.on_reject)

        event.accept()

    def setupUi(self, checks):

        self.resize(815, 266)
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

        self.check_all_rasters = QCheckBox(self.groupBox)
        self.check_all_rasters.setChecked(True)
        self.check_all_rasters.setDisabled(True)
        self.verticalLayoutBox.addWidget(self.check_all_rasters)

        # TODO: write improve function first
        # self.improve_when_necessary = QCheckBox(self.groupBox)
        # self.improve_when_necessary.setChecked(False)
        # self.improve_when_necessary.setDisabled(True)
        # self.verticalLayoutBox.addWidget(self.improve_when_necessary)

        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QMetaObject.connectSlotsByName(self)
