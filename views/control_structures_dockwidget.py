# -*- coding: utf-8 -*-
import os
import logging

# from qgis.core import QgsMapLayerRegistry

from PyQt4 import uic
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal
# from PyQt4.QtCore import SIGNAL
# from PyQt4.QtCore import QRect
# from PyQt4.QtCore import Qt
# from PyQt4.QtCore import QObject
# from PyQt4.QtCore import QMetaObject
# from PyQt4.QtGui import QVBoxLayout
# from PyQt4.QtGui import QPushButton
# from PyQt4.QtGui import QGroupBox
# from PyQt4.QtGui import QComboBox
# from PyQt4.QtGui import QSizePolicy
# from PyQt4.QtGui import QDialogButtonBox
from PyQt4.QtGui import QApplication
# from PyQt4.QtGui import QDialog
# from PyQt4.QtGui import QDockWidget
# from PyQt4.QtGui import QTableWidget

# from ThreeDiToolbox.utils.threedi_database import get_databases  # nodig voor laten zien van models in dialog
# from ThreeDiToolbox.threedi_schema_edits.breach_location import BreachLocation

log = logging.getLogger(__name__)

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

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), '..', 'ui',
    'control_structures_dockwidget.ui'))


class ControlStructuresDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingWidget = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(ControlStructuresDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        self.setupUi(self)

    def closeEvent(self, event):
        self.closingWidget.emit()
        event.accept()


# class ControlStructuresDockWidget(QtGui.QDockWidget, FORM_CLASS):

#     def __init__(self, parent=None,
#                  command=None):
#         """Constructor

#         Args:
#             parent: Qt parent Widget
#             iface: QGiS interface
#             ts_datasource: TimeseriesDatasourceModel instance
#             command: Command instance with a run_it method which will be called
#                      on acceptance of the dialog
#         """
#         super(ControlStructuresDockWidget, self).__init__(parent)
#         self.setupUi(QDockWidget)

#         self.command = command

#         # self.databases = get_databases()  # show databases from QGIS in model
#         # self.database_combo.addItems(self.databases.keys())

#         # Connect signals
#         # self.buttonBox.accepted.connect(self.on_accept)  # when OK is pressed
#         # self.buttonBox.rejected.connect(self.on_reject)  # cancel

#         self.filename = None

#     def on_accept(self):
#         """Accept and run the Command.run_it method."""

#         db_key = self.database_combo.currentText()
#         db_entry = self.databases[db_key]
#         db_type = db_entry['db_type']

#         _db_settings = db_entry['db_settings']

#         if db_type == 'spatialite':
#             # usage of db_type 'spatialite' instead of 'sqlite'
#             # makes much more sense because it also used internally
#             # by qgis, for example when by the ``QgsVectorLayer()``-object
#             host = _db_settings['db_path']
#             db_settings = {
#                 'host': host,
#                 'port': '',
#                 'name': '',
#                 'username': '',
#                 'password': '',
#                 'schema': '',
#                 'database': '',
#                 'db_path': host,
#             }
#         else:
#             db_settings = _db_settings
#             db_settings['schema'] = 'public'
#         self.command.run_it(db_settings, db_type)

#         self.accept()

#     def on_reject(self):
#         """Cancel"""
#         self.reject()
#         log.debug("Reject")

#     def closeEvent(self, event):
#         """
#         Close widget, called by Qt on close
#         :param event: QEvent, close event
#         """

#         # self.buttonBox.accepted.disconnect(self.on_accept)
#         # self.buttonBox.rejected.disconnect(self.on_reject)

#         event.accept()

#     def setupUi(self, DockWidget):
#         self.setObjectName(_fromUtf8("DockWidget"))
#         self.resize(764, 273)
#         self.dockWidgetContents = QtGui.QWidget()
#         self.dockWidgetContents.setFocusPolicy(QtCore.Qt.NoFocus)
#         self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
#         self.horizontalLayoutWidget = QtGui.QWidget(self.dockWidgetContents)
#         self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 741, 51))
#         self.horizontalLayoutWidget.setObjectName(
#             _fromUtf8("horizontalLayoutWidget"))
#         self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
#         self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
#         self.pushButton = QtGui.QPushButton(self.horizontalLayoutWidget)
#         self.pushButton.setObjectName(_fromUtf8("pushButton"))
#         self.horizontalLayout.addWidget(self.pushButton)
#         spacerItem = QtGui.QSpacerItem(
#             40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
#         self.horizontalLayout.addItem(spacerItem)
#         self.horizontalLayoutWidget_2 = QtGui.QWidget(self.dockWidgetContents)
#         self.horizontalLayoutWidget_2.setGeometry(
#             QtCore.QRect(10, 50, 741, 51))
#         self.horizontalLayoutWidget_2.setObjectName(
#             _fromUtf8("horizontalLayoutWidget_2"))
#         self.horizontalLayout_2 = QtGui.QHBoxLayout(
#             self.horizontalLayoutWidget_2)
#         self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
#         self.pushButton_2 = QtGui.QPushButton(self.horizontalLayoutWidget_2)
#         self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
#         self.horizontalLayout_2.addWidget(self.pushButton_2)
#         spacerItem1 = QtGui.QSpacerItem(
#             40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
#         self.horizontalLayout_2.addItem(spacerItem1)
#         self.tableWidget = QtGui.QTableWidget(self.dockWidgetContents)
#         self.tableWidget.setGeometry(QtCore.QRect(10, 100, 741, 91))
#         self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
#         self.tableWidget.setColumnCount(6)
#         self.tableWidget.setRowCount(2)
#         item = QtGui.QTableWidgetItem()
#         self.tableWidget.setVerticalHeaderItem(0, item)
#         item = QtGui.QTableWidgetItem()
#         self.tableWidget.setVerticalHeaderItem(1, item)
#         item = QtGui.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(0, item)
#         item = QtGui.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(1, item)
#         item = QtGui.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(2, item)
#         item = QtGui.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(3, item)
#         item = QtGui.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(4, item)
#         item = QtGui.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(5, item)
#         item = QtGui.QTableWidgetItem()
#         self.tableWidget.setItem(0, 1, item)
#         item = QtGui.QTableWidgetItem()
#         self.tableWidget.setItem(1, 1, item)
#         item = QtGui.QTableWidgetItem()
#         self.tableWidget.setItem(1, 2, item)
#         item = QtGui.QTableWidgetItem()
#         self.tableWidget.setItem(1, 3, item)
#         item = QtGui.QTableWidgetItem()
#         self.tableWidget.setItem(1, 4, item)
#         self.tableWidget.horizontalHeader().setDefaultSectionSize(120)
#         self.horizontalLayoutWidget_3 = QtGui.QWidget(self.dockWidgetContents)
#         self.horizontalLayoutWidget_3.setGeometry(
#             QtCore.QRect(10, 190, 741, 51))
#         self.horizontalLayoutWidget_3.setObjectName(
#             _fromUtf8("horizontalLayoutWidget_3"))
#         self.horizontalLayout_3 = QtGui.QHBoxLayout(
#             self.horizontalLayoutWidget_3)
#         self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
#         self.pushButton_3 = QtGui.QPushButton(self.horizontalLayoutWidget_3)
#         self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
#         self.horizontalLayout_3.addWidget(self.pushButton_3)
#         spacerItem2 = QtGui.QSpacerItem(
#             40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
#         self.horizontalLayout_3.addItem(spacerItem2)
#         self.checkBox = QtGui.QCheckBox(self.dockWidgetContents)
#         self.checkBox.setGeometry(QtCore.QRect(70, 130, 21, 22))
#         self.checkBox.setText(_fromUtf8(""))
#         self.checkBox.setTristate(False)
#         self.checkBox.setObjectName(_fromUtf8("checkBox"))
#         self.comboBox = QtGui.QComboBox(self.dockWidgetContents)
#         self.comboBox.setGeometry(QtCore.QRect(270, 130, 111, 27))
#         self.comboBox.setObjectName(_fromUtf8("comboBox"))
#         self.comboBox.addItem(_fromUtf8(""))
#         self.comboBox_2 = QtGui.QComboBox(self.dockWidgetContents)
#         self.comboBox_2.setGeometry(QtCore.QRect(390, 130, 111, 27))
#         self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
#         self.comboBox_2.addItem(_fromUtf8(""))
#         self.comboBox_3 = QtGui.QComboBox(self.dockWidgetContents)
#         self.comboBox_3.setGeometry(QtCore.QRect(510, 130, 111, 27))
#         self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
#         self.comboBox_3.addItem(_fromUtf8(""))
#         self.comboBox_3.addItem(_fromUtf8(""))
#         self.comboBox_3.addItem(_fromUtf8(""))
#         self.comboBox_3.addItem(_fromUtf8(""))
#         self.comboBox_3.addItem(_fromUtf8(""))
#         self.pushButton_4 = QtGui.QPushButton(self.dockWidgetContents)
#         self.pushButton_4.setGeometry(QtCore.QRect(630, 130, 111, 27))
#         self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
#         self.checkBox_2 = QtGui.QCheckBox(self.dockWidgetContents)
#         self.checkBox_2.setGeometry(QtCore.QRect(70, 160, 21, 22))
#         self.checkBox_2.setText(_fromUtf8(""))
#         self.checkBox_2.setTristate(False)
#         self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
#         self.pushButton_5 = QtGui.QPushButton(self.dockWidgetContents)
#         self.pushButton_5.setGeometry(QtCore.QRect(630, 160, 111, 27))
#         self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
#         self.setWidget(self.dockWidgetContents)

#         self.retranslateUi(DockWidget)
#         QtCore.QMetaObject.connectSlotsByName(self)

#     def retranslateUi(self, DockWidget):
#         self.setWindowTitle(
#             _translate("DockWidget", "Controlled structures", None))
#         self.pushButton.setText(_translate("DockWidget", "New", None))
#         self.pushButton_2.setText(_translate("DockWidget", "Load", None))
#         item = self.tableWidget.verticalHeaderItem(0)
#         item.setText(_translate("DockWidget", "1", None))
#         item = self.tableWidget.verticalHeaderItem(1)
#         item.setText(_translate("DockWidget", "2", None))
#         item = self.tableWidget.horizontalHeaderItem(0)
#         item.setText(_translate("DockWidget", "Activate", None))
#         item = self.tableWidget.horizontalHeaderItem(1)
#         item.setText(_translate("DockWidget", "Name", None))
#         item = self.tableWidget.horizontalHeaderItem(2)
#         item.setText(_translate("DockWidget", "Meetgroep", None))
#         item = self.tableWidget.horizontalHeaderItem(3)
#         item.setText(_translate("DockWidget", "Controller", None))
#         item = self.tableWidget.horizontalHeaderItem(4)
#         item.setText(_translate("DockWidget", "Control type", None))
#         item = self.tableWidget.horizontalHeaderItem(5)
#         item.setText(_translate("DockWidget", "Action", None))
#         __sortingEnabled = self.tableWidget.isSortingEnabled()
#         self.tableWidget.setSortingEnabled(False)
#         item = self.tableWidget.item(0, 1)
#         item.setText(_translate("DockWidget", "Test 1", None))
#         item = self.tableWidget.item(1, 1)
#         item.setText(_translate("DockWidget", "Test 2", None))
#         item = self.tableWidget.item(1, 2)
#         item.setText(_translate("DockWidget", "Measuring group 1", None))
#         item = self.tableWidget.item(1, 3)
#         item.setText(_translate("DockWidget", "Controller 1", None))
#         item = self.tableWidget.item(1, 4)
#         item.setText(_translate("DockWidget", "Table control", None))
#         self.tableWidget.setSortingEnabled(__sortingEnabled)
#         self.pushButton_3.setText(_translate("DockWidget", "Run model", None))
#         self.comboBox.setItemText(
#             0, _translate("DockWidget", "Selecteer meetgroep...", None))
#         self.comboBox_2.setItemText(
#             0, _translate("DockWidget", "Selecteer controller...", None))
#         self.comboBox_3.setItemText(
#             0, _translate("DockWidget", "Table control", None))
#         self.comboBox_3.setItemText(
#             1, _translate("DockWidget", "PID control", None))
#         self.comboBox_3.setItemText(
#             2, _translate("DockWidget", "Delta control", None))
#         self.comboBox_3.setItemText(
#             3, _translate("DockWidget", "Memory control", None))
#         self.comboBox_3.setItemText(
#             4, _translate("DockWidget", "Timed control", None))
#         self.pushButton_4.setText(_translate("DockWidget", "Create", None))
#         self.pushButton_5.setText(_translate("DockWidget", "Remove", None))
