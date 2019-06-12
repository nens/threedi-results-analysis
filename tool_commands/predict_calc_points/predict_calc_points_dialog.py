from PyQt5.QtCore import QMetaObject
from PyQt5.QtCore import QRect
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QVBoxLayout
from ThreeDiToolbox.utils.threedi_database import get_databases

import logging


logger = logging.getLogger(__name__)


class AddConnectedPointsDialogWidget(QDialog):
    def __init__(self, parent=None, command=None):
        """Constructor

        Args:
            parent: Qt parent Widget
            iface: QGiS interface
            command: Command instance with a run_it method which will be called
                     on acceptance of the dialog
        """
        super().__init__(parent)
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
        logger.debug("Reject")

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
        self.setWindowTitle("Add connected points")
        self.groupBox_2.setTitle("Load from model database")
