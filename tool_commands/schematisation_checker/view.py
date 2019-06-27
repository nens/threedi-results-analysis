# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!
# flake8: noqa

from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.save_file_location_display = QtWidgets.QLineEdit(self.outputFileBox)
        self.save_file_location_display.setEnabled(False)
        self.save_file_location_display.setObjectName("save_file_location_display")
        self.horizontalLayout.addWidget(self.save_file_location_display)
        self.save_file_location_button = QtWidgets.QPushButton(self.outputFileBox)
        self.save_file_location_button.setObjectName("save_file_location_button")
        self.horizontalLayout.addWidget(self.save_file_location_button)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.outputFileBox)
        self.horizontalLayout_control_buttons = QtWidgets.QHBoxLayout()
        self.horizontalLayout_control_buttons.setObjectName("horizontalLayout_control_buttons")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_control_buttons.addItem(spacerItem)
        self.open_result_button = QtWidgets.QPushButton(SchemaCheckerDialog)
        self.open_result_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_result_button.sizePolicy().hasHeightForWidth())
        self.open_result_button.setSizePolicy(sizePolicy)
        self.open_result_button.setIconSize(QtCore.QSize(16, 16))
        self.open_result_button.setObjectName("open_result_button")
        self.horizontalLayout_control_buttons.addWidget(self.open_result_button)
        self.cancel_button = QtWidgets.QPushButton(SchemaCheckerDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_control_buttons.addWidget(self.cancel_button)
        self.run_button = QtWidgets.QPushButton(SchemaCheckerDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.run_button.sizePolicy().hasHeightForWidth())
        self.run_button.setSizePolicy(sizePolicy)
        self.run_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.run_button.setObjectName("run_button")
        self.horizontalLayout_control_buttons.addWidget(self.run_button)
        self.verticalLayout.addLayout(self.horizontalLayout_control_buttons)

        self.retranslateUi(SchemaCheckerDialog)
        QtCore.QMetaObject.connectSlotsByName(SchemaCheckerDialog)

    def retranslateUi(self, SchemaCheckerDialog):
        _translate = QtCore.QCoreApplication.translate
        SchemaCheckerDialog.setWindowTitle(_translate("SchemaCheckerDialog", "Schematisation Checker"))
        self.databaseSelectionGroup.setTitle(_translate("SchemaCheckerDialog", "Threedi model database"))
        self.outputFileBox.setTitle(_translate("SchemaCheckerDialog", "Output file"))
        self.save_file_location_button.setText(_translate("SchemaCheckerDialog", "Save"))
        self.open_result_button.setText(_translate("SchemaCheckerDialog", "Open"))
        self.cancel_button.setText(_translate("SchemaCheckerDialog", "Cancel"))
        self.run_button.setText(_translate("SchemaCheckerDialog", "Run"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SchemaCheckerDialog = QtWidgets.QDialog()
    ui = Ui_SchemaCheckerDialog()
    ui.setupUi(SchemaCheckerDialog)
    SchemaCheckerDialog.show()
    sys.exit(app.exec_())

