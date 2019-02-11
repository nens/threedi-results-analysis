# (c) Nelen & Schuurmans, see LICENSE.rst.

from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtCore import QRect, Qt, QObject, QMetaObject
from qgis.PyQt.QtWidgets import (
    QVBoxLayout, QGroupBox, QComboBox, QSizePolicy, QCheckBox,
    QDialogButtonBox, QApplication)
from ThreeDiToolbox.utils.threedi_database import get_databases
import os
import logging

log = logging.getLogger(__name__)

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class RasterCheckerDialogWidget(QDialog):

    def __init__(self, parent=None, checks=[],
                 command=None):
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
            if 'spatialite' in k:
                if v['db_name']:
                    self.databases[k] = v

        self.database_combo.addItems(self.databases.keys())

        # Connect signals
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)

    def on_accept(self):
        """Accept and run the Command.run_it method."""
        db_key = self.database_combo.currentText()
        settings = self.databases[db_key]
        db_set = settings['db_settings']

        if not os.path.isfile(db_set['db_path']):
            msg = 'sqlite %s not found' % str(db_set['db_path'])
            raise Exception(msg)

        # TODO: check_all_rasters always runs. Enable check per model entree
        checks = []
        if self.check_all_rasters.isChecked():
            checks.append('check all rasters')
            # check_pixels may only be checked when 'check_all_rasters' is
            # checked
            if self.check_pixels.isChecked():
                checks.append('check pixels')
                # TODO: write improve first
                # improve_when_necessary may only be checked when
                # 'check_all_rasters' is checked
                # if self.improve_when_necessary.isChecked():
                #     checks.append('improve when necessary')

        self.command.run_it(checks, db_set, settings['db_type'])

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

        self.check_all_rasters = QCheckBox(self.groupBox)
        self.check_all_rasters.setChecked(True)
        self.check_all_rasters.setDisabled(True)
        self.verticalLayoutBox.addWidget(self.check_all_rasters)

        self.check_pixels = QCheckBox(self.groupBox)
        self.check_pixels.setChecked(False)
        self.verticalLayoutBox.addWidget(self.check_pixels)

        # TODO: write improve function first
        # self.improve_when_necessary = QCheckBox(self.groupBox)
        # self.improve_when_necessary.setChecked(False)
        # self.improve_when_necessary.setDisabled(True)
        # self.verticalLayoutBox.addWidget(self.improve_when_necessary)

        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("self", "Raster Checker", None))
        self.groupBox_2.setTitle(_translate(
            "self", "Model schematisation database", None))

        self.groupBox.setTitle(_translate("Import_dialog", "Options", None))

        self.check_all_rasters.setText(_translate(
            "Import_dialog",
            "1. Check all rasters of all v2_global_settings rows",
            None))

        self.check_pixels.setText(_translate(
            "Import_dialog",
            "2. Compare pixel alignment (only in combination with option 1)",
            None))

        # TODO: write improve function first
        # self.improve_when_necessary.setText(_translate(
        #     "Import_dialog",
        #     "3. Improve when necessary (only in combination with option 2)",
        #     None))
