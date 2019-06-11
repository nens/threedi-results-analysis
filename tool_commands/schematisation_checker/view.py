# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'model_checker_view.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!
# flake8: noqa

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 153)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.databaseSelectionGroup = QtWidgets.QGroupBox(Dialog)
        self.databaseSelectionGroup.setMaximumSize(QtCore.QSize(341, 141))
        self.databaseSelectionGroup.setObjectName("databaseSelectionGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.databaseSelectionGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.database_combobox = QtWidgets.QComboBox(self.databaseSelectionGroup)
        self.database_combobox.setObjectName("database_combobox")
        self.verticalLayout_2.addWidget(self.database_combobox)
        self.verticalLayout.addWidget(self.databaseSelectionGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.databaseSelectionGroup.setTitle(
            _translate("Dialog", "Threedi model database")
        )
