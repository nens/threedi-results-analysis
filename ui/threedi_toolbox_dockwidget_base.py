# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\threedi_toolbox_dockwidget_base.ui'
#
# Created: Sat Mar 19 07:00:22 2016
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(391, 453)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeView = QtGui.QTreeView(self.tab)
        self.treeView.setHeaderHidden(True)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.verticalLayout.addWidget(self.treeView)
        self.checkBox = QtGui.QCheckBox(self.tab)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tableView = QtGui.QTableView(self.tab_2)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout_2.addWidget(self.tableView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(self.tab_2)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.tab_2)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tableView_2 = QtGui.QTableView(self.tab_2)
        self.tableView_2.setObjectName(_fromUtf8("tableView_2"))
        self.verticalLayout_2.addWidget(self.tableView_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_3 = QtGui.QPushButton(self.tab_2)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_4 = QtGui.QPushButton(self.tab_2)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        Form.setWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "3di toolbox", None))
        self.checkBox.setText(_translate("Form", "auto update logboek", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Toolbox", None))
        self.pushButton.setText(_translate("Form", "PushButton", None))
        self.pushButton_2.setText(_translate("Form", "PushButton", None))
        self.pushButton_3.setText(_translate("Form", "PushButton", None))
        self.pushButton_4.setText(_translate("Form", "PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Instellingen", None))

