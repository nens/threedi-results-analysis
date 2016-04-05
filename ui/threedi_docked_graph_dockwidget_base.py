# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\threedi_docked_graph_dockwidget_base.ui'
#
# Created: Thu Mar 31 19:48:41 2016
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

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(565, 300)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.parameterComboBox = QtGui.QComboBox(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parameterComboBox.sizePolicy().hasHeightForWidth())
        self.parameterComboBox.setSizePolicy(sizePolicy)
        self.parameterComboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.parameterComboBox.setObjectName(_fromUtf8("parameterComboBox"))
        self.horizontalLayout.addWidget(self.parameterComboBox)
        self.addSelectedObjectButton = QtGui.QPushButton(self.dockWidgetContents)
        self.addSelectedObjectButton.setObjectName(_fromUtf8("addSelectedObjectButton"))
        self.horizontalLayout.addWidget(self.addSelectedObjectButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.graphTabWidget = QtGui.QTabWidget(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(6)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphTabWidget.sizePolicy().hasHeightForWidth())
        self.graphTabWidget.setSizePolicy(sizePolicy)
        self.graphTabWidget.setObjectName(_fromUtf8("graphTabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.graphTabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.graphTabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout.addWidget(self.graphTabWidget, 1, 0, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "DockWidget", None))
        self.addSelectedObjectButton.setText(_translate("DockWidget", "PushButton", None))
        self.graphTabWidget.setTabText(self.graphTabWidget.indexOf(self.tab), _translate("DockWidget", "Tab 1", None))
        self.graphTabWidget.setTabText(self.graphTabWidget.indexOf(self.tab_2), _translate("DockWidget", "Tab 2", None))

