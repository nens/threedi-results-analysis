# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/import_sufhyd_dialog.ui'
#
# Created: Fri Sep 02 00:03:50 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Import_dialog(object):
    def setupUi(self, Import_dialog):
        Import_dialog.setObjectName(_fromUtf8("Import_dialog"))
        Import_dialog.resize(515, 166)
        self.verticalLayout = QtGui.QVBoxLayout(Import_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Import_dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 481, 34))
        self.horizontalLayoutWidget.setObjectName(
            _fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.file_combo = QtGui.QComboBox(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.file_combo.sizePolicy().hasHeightForWidth())
        self.file_combo.setSizePolicy(sizePolicy)
        self.file_combo.setObjectName(_fromUtf8("file_combo"))
        self.horizontalLayout.addWidget(self.file_combo)
        self.file_button = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.file_button.setObjectName(_fromUtf8("file_button"))
        self.horizontalLayout.addWidget(self.file_button)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(Import_dialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.database_combo = QtGui.QComboBox(self.groupBox_2)
        self.database_combo.setGeometry(QtCore.QRect(10, 20, 481, 20))
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.database_combo.sizePolicy().hasHeightForWidth())
        self.database_combo.setSizePolicy(sizePolicy)
        self.database_combo.setObjectName(_fromUtf8("database_combo"))
        self.verticalLayout.addWidget(self.groupBox_2)
        self.buttonBox = QtGui.QDialogButtonBox(Import_dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
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
        self.groupBox.setTitle(_translate(
            "Import_dialog", "Sufhyd file", None))
        self.file_button.setText(_translate(
            "Import_dialog", "Select", None))
        self.groupBox_2.setTitle(_translate(
            "Import_dialog", "Destination database", None))
