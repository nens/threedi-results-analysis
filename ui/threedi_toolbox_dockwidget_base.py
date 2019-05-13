# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\threedi_toolbox_dockwidget_base.ui'
#
# Created: Sat Mar 19 07:00:22 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from qgis.PyQt import QtCore
from qgis.PyQt import QtGui
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtWidgets import QCheckBox
from qgis.PyQt.QtWidgets import QGridLayout
from qgis.PyQt.QtWidgets import QTabWidget
from qgis.PyQt.QtWidgets import QTreeView
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.PyQt.QtWidgets import QWidget


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


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(391, 453)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QTabWidget()
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeView = QTreeView(self.tab)
        self.treeView.setHeaderHidden(True)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.verticalLayout.addWidget(self.treeView)
        self.checkBox = QCheckBox(self.tab)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        Form.setWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "3Di toolbox", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab), _translate("Form", "Toolbox", None)
        )
