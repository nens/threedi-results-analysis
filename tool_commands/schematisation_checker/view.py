# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!
# flake8: noqa

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class Ui_SchemaCheckerDialog(object):
    def setupUi(self, SchemaCheckerDialog):
        SchemaCheckerDialog.setObjectName("SchemaCheckerDialog")
        SchemaCheckerDialog.resize(458, 236)
        self.verticalLayout = QtWidgets.QVBoxLayout(SchemaCheckerDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.databaseSelectionGroup = QtWidgets.QGroupBox(SchemaCheckerDialog)
        self.databaseSelectionGroup.setMaximumSize(QtCore.QSize(341, 141))
        self.databaseSelectionGroup.setObjectName("databaseSelectionGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.databaseSelectionGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.database_combobox = QtWidgets.QComboBox(self.databaseSelectionGroup)
        self.database_combobox.setObjectName("database_combobox")
        self.verticalLayout_2.addWidget(self.database_combobox)
        self.verticalLayout.addWidget(self.databaseSelectionGroup)
        self.outputFileBox = QtWidgets.QGroupBox(SchemaCheckerDialog)
        self.outputFileBox.setObjectName("outputFileBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.outputFileBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.outputfile_path_display = QtWidgets.QLineEdit(self.outputFileBox)
        self.outputfile_path_display.setEnabled(False)
        self.outputfile_path_display.setObjectName("outputfile_path_display")
        self.horizontalLayout.addWidget(self.outputfile_path_display)
        self.open_file_button = QtWidgets.QPushButton(self.outputFileBox)
        self.open_file_button.setObjectName("open_file_button")
        self.horizontalLayout.addWidget(self.open_file_button)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.outputFileBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(SchemaCheckerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SchemaCheckerDialog)
        self.buttonBox.accepted.connect(SchemaCheckerDialog.accept)
        self.buttonBox.rejected.connect(SchemaCheckerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SchemaCheckerDialog)

    def retranslateUi(self, SchemaCheckerDialog):
        _translate = QtCore.QCoreApplication.translate
        SchemaCheckerDialog.setWindowTitle(_translate("SchemaCheckerDialog", "Dialog"))
        self.databaseSelectionGroup.setTitle(
            _translate("SchemaCheckerDialog", "Threedi model database")
        )
        self.outputFileBox.setTitle(_translate("SchemaCheckerDialog", "Output file"))
        self.open_file_button.setText(_translate("SchemaCheckerDialog", "Open"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    SchemaCheckerDialog = QtWidgets.QDialog()
    ui = Ui_SchemaCheckerDialog()
    ui.setupUi(SchemaCheckerDialog)
    SchemaCheckerDialog.show()
    sys.exit(app.exec_())
