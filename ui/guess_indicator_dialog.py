# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/guess_indicator_dialog.ui'
#
# Created: Fri Sep 02 08:58:15 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from builtins import object
from qgis.PyQt import QtCore, QtGui
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.PyQt.QtWidgets import QGroupBox
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtWidgets import QSizePolicy
from qgis.PyQt.QtWidgets import QCheckBox
from qgis.PyQt.QtWidgets import QDialogButtonBox

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class Ui_Import_dialog(object):
    def setupUi(self, Import_dialog):
        Import_dialog.setObjectName(_fromUtf8("Import_dialog"))
        Import_dialog.resize(515, 210)
        self.verticalLayout = QVBoxLayout(Import_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QGroupBox(Import_dialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.database_combo = QComboBox(self.groupBox_2)
        self.database_combo.setGeometry(QtCore.QRect(10, 20, 481, 20))
        sizePolicy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.database_combo.sizePolicy().hasHeightForWidth())
        self.database_combo.setSizePolicy(sizePolicy)
        self.database_combo.setObjectName(_fromUtf8("database_combo"))
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QGroupBox(Import_dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.check_pipe_friction = QCheckBox(self.groupBox)
        self.check_pipe_friction.setGeometry(QtCore.QRect(10, 20, 171, 17))
        self.check_pipe_friction.setChecked(True)
        self.check_pipe_friction.setObjectName(
            _fromUtf8("check_pipe_friction"))
        self.checkBox_3 = QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(10, 40, 171, 17))
        self.checkBox_3.setChecked(True)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.verticalLayout.addWidget(self.groupBox)
        self.check_only_empty_fields = QCheckBox(Import_dialog)
        self.check_only_empty_fields.setObjectName(
            _fromUtf8("check_only_empty_fields"))
        self.verticalLayout.addWidget(self.check_only_empty_fields)
        self.buttonBox = QDialogButtonBox(Import_dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Import_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(
            _fromUtf8("accepted()")), Import_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(
            _fromUtf8("rejected()")), Import_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Import_dialog)

    def retranslateUi(self, Import_dialog):
        Import_dialog.setWindowTitle(_translate(
            "Import_dialog", "Import sufhyd", None))
        self.groupBox_2.setTitle(_translate(
            "Import_dialog", "Model schematisation database", None))
        self.groupBox.setTitle(_translate("Import_dialog", "Guess", None))
        self.check_pipe_friction.setText(_translate(
            "Import_dialog", "Pipe friction", None))
        self.checkBox_3.setText(_translate(
            "Import_dialog", "Manhole indicator", None))
        self.check_only_empty_fields.setText(_translate(
            "Import_dialog", "Only empty fields", None))
