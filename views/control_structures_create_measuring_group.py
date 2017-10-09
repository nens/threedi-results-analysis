# -*- coding: utf-8 -*-
import os
import logging


from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

from ThreeDiToolbox.threedi_schema_edits.controlled_structures import \
    ControlledStructures
from ThreeDiToolbox.utils.threedi_database import get_databases
from ThreeDiToolbox.utils.threedi_database import get_database_properties

log = logging.getLogger(__name__)


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), os.pardir, 'ui',
    'controlled_structures_create_measuring_group_dialog.ui'))


class CreateMeasuringGroupDialogWidget(QDialog):

    def __init__(self, parent=None,
                 command=None, db_key=None, measuring_group_id=None,
                 dockwidget_controlled_structures=None):
        """Constructor

        Args:
            parent: Qt parent Widget
            iface: QGiS interface
            ts_datasource: TimeseriesDatasourceModel instance
            command: Command instance with a run_it method which will be called
                     on acceptance of the dialog
        """
        super(CreateMeasuringGroupDialogWidget, self).__init__(parent)
        self.setupUi()
        # Set the id of the measuring group
        self.label_measuring_group_id_info.setText(measuring_group_id)

        self.command = command
        self.db_key = db_key
        self.measuring_group_id = measuring_group_id
        self.dockwidget_controlled_structures = \
            dockwidget_controlled_structures

        self.databases = get_databases()

        self.db = get_database_properties(self.db_key)
        self.control_structure = ControlledStructures(
            flavor=self.db["db_entry"]['db_type'])
        self.control_structure.start_sqalchemy_engine(self.db["db_settings"])
        # Get all id's of the measuring groups
        list_of_measuring_group_ids = self.control_structure.get_attributes(
            table_name="v2_control_measure_group", attribute_name="id")
        for measuring_group_id in list_of_measuring_group_ids:
            id_nr = measuring_group_id[0]
            self.combobox_measuring_group_load.addItem(str(id_nr))
        # Get all id's of the measuring points
        list_of_measuring_point_ids = self.control_structure.get_attributes(
            table_name="v2_control_measure_map", attribute_name="id")
        for measuring_point_id in list_of_measuring_point_ids:
            id_nr = measuring_point_id[0]
            self.combobox_measuring_point_load.addItem(str(id_nr))

        # db_key = self.db_key  # name of database
        # db_entry = self.databases[db_key]

        # # Set the id of the measuring group that is about to be made
        # self.label_measuring_group_id_info.setText(measuring_group_id)

        # _db_settings = db_entry['db_settings']

        # if db_entry['db_type'] == 'spatialite':
        #     host = _db_settings['db_path']
        #     db_settings = {
        #         'host': host,
        #         'port': '',
        #         'name': '',
        #         'username': '',
        #         'password': '',
        #         'schema': '',
        #         'database': '',
        #         'db_path': host,
        #     }
        # else:
        #     db_settings = _db_settings
        #     db_settings['schema'] = 'public'
        # control_structure = ControlledStructures(flavor=db_entry['db_type'])
        # control_structure.start_sqalchemy_engine(db_settings)
        # # Get all id's of the measuring groups
        # with control_structure.engine.connect() as con:
        #     rs = con.execute(
        #         '''SELECT id FROM v2_control_measure_group;'''
        #     )
        #     measure_group_ids = rs.fetchall()
        # con.close()
        # for measure_group_id in measure_group_ids:
        #     id_nr = measure_group_id[0]
        #     self.combobox_measuring_group_load.addItem(str(id_nr))
        # # Get all id's of the measuring points
        # with control_structure.engine.connect() as con:
        #     rs = con.execute(
        #         '''SELECT id FROM v2_control_measure_map;'''
        #     )
        #     measure_map_ids = rs.fetchall()
        # con.close()
        # for measure_map_id in measure_map_ids:
        #     id_nr = measure_map_id[0]
        #     self.combobox_measuring_point_load.addItem(str(id_nr))

        # Connect signals
        self.pushbutton_measuring_group_load.clicked.connect(
            self.load_measuring_group)
        self.pushbutton_measuring_point_add_point.clicked.connect(
            self.add_measuring_point)
        self.pushbutton_measuring_point_load.clicked.connect(
            self.load_measuring_point)
        self.buttonbox.accepted.connect(self.on_accept)
        self.buttonbox.rejected.connect(self.on_reject)

    def on_accept(self):
        """Accept and run the Command.run_it method."""
        self.save_measuring_group()

        self.accept()

    def on_reject(self):
        """Cancel"""
        self.reject()
        log.debug("Reject")

    def closeEvent(self, event):
        """
        Close widget, called by Qt on close
        :param event: QEvent, close event
        """

        self.buttonbox.accepted.disconnect(self.on_accept)
        self.buttonbox.rejected.disconnect(self.on_reject)

        event.accept()

    def update_dialog(self):
        """
        Function to update the create measuring group dialog.
        """
        # Get the model
        db_key = self.db_key  # name of database
        db_entry = self.databases[db_key]

        _db_settings = db_entry['db_settings']

        if db_entry['db_type'] == 'spatialite':
            host = _db_settings['db_path']
            db_settings = {
                'host': host,
                'port': '',
                'name': '',
                'username': '',
                'password': '',
                'schema': '',
                'database': '',
                'db_path': host,
            }
        else:
            db_settings = _db_settings
            db_settings['schema'] = 'public'
        control_structure = ControlledStructures(flavor=db_entry['db_type'])
        control_structure.start_sqalchemy_engine(db_settings)
        # Get all id's of the connection nodes
        with control_structure.engine.connect() as con:
            rs = con.execute(
                '''SELECT id FROM v2_connection_nodes;'''
            )
            connection_node_ids = rs.fetchall()
        con.close()
        for connection_node_id in connection_node_ids:
            id_nr = connection_node_id[0]
            self.combobox_measuring_group_table_id.addItem(str(id_nr))

    def add_measuring_point(self):
        """Add a measuring point to the tablewidget."""
        # The measuring point should be added on the top of the table
        row_position = 0
        self.tablewidget_measuring_point.insertRow(row_position)
        self.tablewidget_measuring_point.setItem(
            row_position, 0, QTableWidgetItem("v2_connection_nodes"))
        self.combobox_measuring_group_table_id = QComboBox()
        self.tablewidget_measuring_point.setCellWidget(
            row_position, 1, self.combobox_measuring_group_table_id)
        measuring_point_remove = QPushButton("Remove")
        measuring_point_remove.clicked.connect(self.remove_row)
        self.tablewidget_measuring_point.setCellWidget(
            row_position, 3, measuring_point_remove)
        self.update_dialog()

    def remove_row(self):
        """Remove a certain row."""
        tablewidget = self.tablewidget_measuring_point
        row_number = tablewidget.currentRow()
        tablewidget.removeRow(row_number)

    def load_measuring_group(self):
        """Load a measuring group in the tablewidget."""
        # Clear table
        row_count = self.tablewidget_measuring_point.rowCount()
        for row in range(row_count):
            self.tablewidget_measuring_point.removeRow(0)
        db_key = self.db_key  # name of database
        db_entry = self.databases[db_key]

        _db_settings = db_entry['db_settings']

        if db_entry['db_type'] == 'spatialite':
            host = _db_settings['db_path']
            db_settings = {
                'host': host,
                'port': '',
                'name': '',
                'username': '',
                'password': '',
                'schema': '',
                'database': '',
                'db_path': host,
            }
        else:
            db_settings = _db_settings
            db_settings['schema'] = 'public'
        control_structure = ControlledStructures(flavor=db_entry['db_type'])
        control_structure.start_sqalchemy_engine(db_settings)
        # Get all the measuring points
        with control_structure.engine.connect() as con:
            rs = con.execute(
                '''SELECT * FROM v2_control_measure_map WHERE measure_group_id={};'''
                .format(self.combobox_measuring_group_load.currentText())
            )
            measure_groups = rs.fetchall()
        con.close()
        for measure_group in measure_groups:
            row_position = self.tablewidget_measuring_point.rowCount()
            self.tablewidget_measuring_point.insertRow(row_position)
            self.tablewidget_measuring_point.setItem(
                row_position, 0, QTableWidgetItem(str(measure_group[2])))
            self.tablewidget_measuring_point.setItem(
                row_position, 1, QTableWidgetItem(str(measure_group[3])))
            self.tablewidget_measuring_point.setItem(
                row_position, 2, QTableWidgetItem(str(measure_group[4])))
            measuring_point_remove = QPushButton("Remove")
            measuring_point_remove.clicked.connect(self.remove_row)
            self.tablewidget_measuring_point.setCellWidget(
                row_position, 3, measuring_point_remove)

    def load_measuring_point(self):
        """Load a measuring group in the tablewidget."""
        db_key = self.db_key  # name of database
        db_entry = self.databases[db_key]

        _db_settings = db_entry['db_settings']

        if db_entry['db_type'] == 'spatialite':
            host = _db_settings['db_path']
            db_settings = {
                'host': host,
                'port': '',
                'name': '',
                'username': '',
                'password': '',
                'schema': '',
                'database': '',
                'db_path': host,
            }
        else:
            db_settings = _db_settings
            db_settings['schema'] = 'public'
        control_structure = ControlledStructures(flavor=db_entry['db_type'])
        control_structure.start_sqalchemy_engine(db_settings)
        # Get the measuring points
        with control_structure.engine.connect() as con:
            rs = con.execute(
                '''SELECT * FROM v2_control_measure_map WHERE id={};'''
                .format(self.combobox_measuring_point_load.currentText())
            )
            measure_point = rs.fetchone()
        con.close()
        # The measuring point should be added on the top of the table
        row_position = 0
        self.tablewidget_measuring_point.insertRow(row_position)
        self.tablewidget_measuring_point.setItem(
            row_position, 0, QTableWidgetItem(str(measure_point[2])))
        self.tablewidget_measuring_point.setItem(
            row_position, 1, QTableWidgetItem(str(measure_point[3])))
        self.tablewidget_measuring_point.setItem(
            row_position, 2, QTableWidgetItem(str(measure_point[4])))
        measuring_point_remove = QPushButton("Remove")
        measuring_point_remove.clicked.connect(self.remove_row)
        self.tablewidget_measuring_point.setCellWidget(
            row_position, 3, measuring_point_remove)

    def save_measuring_group(self):
        """Save the measuring group in the database."""
        db_key = self.db_key  # name of database
        db_entry = self.databases[db_key]

        _db_settings = db_entry['db_settings']

        if db_entry['db_type'] == 'spatialite':
            host = _db_settings['db_path']
            db_settings = {
                'host': host,
                'port': '',
                'name': '',
                'username': '',
                'password': '',
                'schema': '',
                'database': '',
                'db_path': host,
            }
        else:
            db_settings = _db_settings
            db_settings['schema'] = 'public'
        control_structure = ControlledStructures(flavor=db_entry['db_type'])
        control_structure.start_sqalchemy_engine(db_settings)
        # Get the new measuring_group id
        with control_structure.engine.connect() as con:
            rs = con.execute(
                '''SELECT MAX(id) FROM v2_control_measure_group;'''
            )
            measuring_group_id = rs.fetchone()[0]
            if not measuring_group_id:
                measuring_group_id = 0
            new_measuring_group_id = measuring_group_id + 1
        con.close()
        # Insert the variables in the v2_control_measure_group
        with control_structure.engine.connect() as con:
            rs = con.execute(
                '''INSERT INTO v2_control_measure_group (id) \
                VALUES ('{}');'''
                .format(new_measuring_group_id)
            )
        con.close()
        # Add a tab in the tabwidget of the 'Measuring group' tab in
        # the controlled structures dockwidget
        tab = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(tab)
        tab.setLayout(layout)

        label_field = QtGui.QLabel(tab)
        label_field.setGeometry(10, 10, 741, 21)
        label_field.setText("Field: {}".format(
            self.combobox_measuring_point_field.currentText()))

        table_measuring_group = QtGui.QTableWidget(tab)
        table_measuring_group.setGeometry(10, 40, 741, 311)
        table_measuring_group.insertColumn(0)
        table_measuring_group.setHorizontalHeaderItem(
            0, QTableWidgetItem("table"))
        table_measuring_group.insertColumn(1)
        table_measuring_group.setHorizontalHeaderItem(
            1, QTableWidgetItem("table_id"))
        table_measuring_group.insertColumn(2)
        table_measuring_group.setHorizontalHeaderItem(
            2, QTableWidgetItem("weight"))
        self.dockwidget_controlled_structures.table_measuring_group = \
            table_measuring_group

        self.dockwidget_controlled_structures\
            .tab_measuring_group_view_2.insertTab(
                0, tab, "Group: {}".format(
                    str(self.label_measuring_group_id_info.text())))
        # Insert the variables in the v2_control_measure_map
        # and in the newly made tab of the "Measuring group" tab
        for row in range(self.tablewidget_measuring_point.rowCount()):
            # Get the new measuring_point id
            with control_structure.engine.connect() as con:
                rs = con.execute(
                    '''SELECT MAX(id) FROM v2_control_measure_map;'''
                )
                measuring_point_id = rs.fetchone()[0]
                if not measuring_point_id:
                    measuring_point_id = 0
                new_measuring_point_id = measuring_point_id + 1
            con.close()
            measuring_point_table = self.tablewidget_measuring_point.item(
                row, 0).text()
            try:
                measuring_point_table_id = self.tablewidget_measuring_point\
                    .item(row, 1).text()
            except AttributeError:
                measuring_point_table_id = self.tablewidget_measuring_point\
                    .cellWidget(row, 1).currentText()
            try:
                measuring_point_weight = self.tablewidget_measuring_point.item(
                    row, 2).text()
            except AttributeError:
                measuring_point_weight = ""
            # Save the variables in the v2_control_measure_map
            with control_structure.engine.connect() as con:
                rs = con.execute(
                    '''INSERT INTO v2_control_measure_map (id, \
                    measure_group_id, object_type, object_id, \
                    weight) \
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');'''
                    .format(new_measuring_point_id, new_measuring_group_id,
                            measuring_point_table, measuring_point_table_id,
                            measuring_point_weight))
            con.close()
            # Populate new tab of "Measuring group" tab
            row_position = self.dockwidget_controlled_structures\
                .table_measuring_group.rowCount()
            self.dockwidget_controlled_structures\
                .table_measuring_group.insertRow(row_position)
            self.dockwidget_controlled_structures.table_measuring_group\
                .setItem(row_position, 0, QTableWidgetItem(
                    "v2_connection_nodes"))
            self.dockwidget_controlled_structures.table_measuring_group\
                .setItem(row_position, 1, QTableWidgetItem(
                    measuring_point_table_id))
            self.dockwidget_controlled_structures.table_measuring_group\
                .setItem(row_position, 2, QTableWidgetItem(
                    measuring_point_weight))

    def setupUi(self):
        self.setObjectName(_fromUtf8("dialog_create_measuring_group"))
        self.resize(779, 513)
        self.buttonbox = QtGui.QDialogButtonBox(self)
        self.buttonbox.setGeometry(QtCore.QRect(190, 460, 191, 32))
        self.buttonbox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonbox.setObjectName(_fromUtf8("buttonbox"))
        self.groupbox_measuring_group = QtGui.QGroupBox(self)
        self.groupbox_measuring_group.setGeometry(
            QtCore.QRect(10, 10, 761, 111))
        self.groupbox_measuring_group.setObjectName(
            _fromUtf8("groupbox_measuring_group"))
        self.label_measuring_group_id = QtGui.QLabel(
            self.groupbox_measuring_group)
        self.label_measuring_group_id.setGeometry(
            QtCore.QRect(20, 80, 101, 21))
        self.label_measuring_group_id.setObjectName(_fromUtf8(
            "label_measuring_group_id"))
        self.label_measuring_group_id_info = QtGui.QLabel(
            self.groupbox_measuring_group)
        self.label_measuring_group_id_info.setGeometry(
            QtCore.QRect(200, 90, 311, 20))
        self.label_measuring_group_id_info.setText(_fromUtf8(""))
        self.label_measuring_group_id_info.setObjectName(_fromUtf8(
            "label_measuring_group_id_info"))
        self.pushbutton_measuring_group_load = QtGui.QPushButton(
            self.groupbox_measuring_group)
        self.pushbutton_measuring_group_load.setGeometry(
            QtCore.QRect(20, 40, 161, 27))
        self.pushbutton_measuring_group_load.setObjectName(
            _fromUtf8("pushbutton_measuring_group_load"))
        self.combobox_measuring_group_load = QtGui.QComboBox(
            self.groupbox_measuring_group)
        self.combobox_measuring_group_load.setGeometry(
            QtCore.QRect(200, 40, 311, 27))
        self.combobox_measuring_group_load.setObjectName(_fromUtf8(
            "combobox_measuring_group_load"))
        self.label_measuring_group_load_description = QtGui.QLabel(
            self.groupbox_measuring_group)
        self.label_measuring_group_load_description.setGeometry(
            QtCore.QRect(530, 40, 231, 31))
        self.label_measuring_group_load_description.setObjectName(
            _fromUtf8("label_measuring_group_load_description"))
        self.label_measuring_group_description = QtGui.QLabel(
            self.groupbox_measuring_group)
        self.label_measuring_group_description.setGeometry(
            QtCore.QRect(530, 80, 231, 41))
        self.label_measuring_group_description.setObjectName(
            _fromUtf8("label_measuring_group_description"))
        self.groupbox_measuring_points = QtGui.QGroupBox(self)
        self.groupbox_measuring_points.setGeometry(
            QtCore.QRect(10, 120, 761, 321))
        self.groupbox_measuring_points.setObjectName(_fromUtf8(
            "groupbox_measuring_points"))
        self.tablewidget_measuring_point = QtGui.QTableWidget(
            self.groupbox_measuring_points)
        self.tablewidget_measuring_point.setGeometry(
            QtCore.QRect(20, 70, 731, 151))
        self.tablewidget_measuring_point.setObjectName(_fromUtf8(
            "tablewidget_measuring_point"))
        self.tablewidget_measuring_point.setColumnCount(4)
        self.tablewidget_measuring_point.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tablewidget_measuring_point.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tablewidget_measuring_point.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tablewidget_measuring_point.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tablewidget_measuring_point.setHorizontalHeaderItem(3, item)
        self.label_measuring_point_field = QtGui.QLabel(
            self.groupbox_measuring_points)
        self.label_measuring_point_field.setGeometry(
            QtCore.QRect(20, 30, 101, 31))
        self.label_measuring_point_field.setObjectName(
            _fromUtf8("label_measuring_point_field"))
        self.combobox_measuring_point_field = QtGui.QComboBox(
            self.groupbox_measuring_points)
        self.combobox_measuring_point_field.setGeometry(
            QtCore.QRect(200, 30, 311, 27))
        self.combobox_measuring_point_field.setObjectName(_fromUtf8(
            "combobox_measuring_point_field"))
        self.combobox_measuring_point_field.addItem(_fromUtf8(""))
        self.pushbutton_measuring_point_add_point = QtGui.QPushButton(
            self.groupbox_measuring_points)
        self.pushbutton_measuring_point_add_point.setGeometry(
            QtCore.QRect(20, 240, 161, 27))
        self.pushbutton_measuring_point_add_point.setObjectName(
            _fromUtf8("pushbutton_measuring_point_add_point"))
        self.label_measuring_point_add_point = QtGui.QLabel(
            self.groupbox_measuring_points)
        self.label_measuring_point_add_point.setGeometry(
            QtCore.QRect(200, 240, 311, 31))
        self.label_measuring_point_add_point.setObjectName(
            _fromUtf8("label_measuring_point_add_point"))
        self.pushbutton_measuring_point_load = QtGui.QPushButton(
            self.groupbox_measuring_points)
        self.pushbutton_measuring_point_load.setGeometry(
            QtCore.QRect(20, 280, 161, 27))
        self.pushbutton_measuring_point_load.setObjectName(
            _fromUtf8("pushbutton_measuring_point_load"))
        self.combobox_measuring_point_load = QtGui.QComboBox(
            self.groupbox_measuring_points)
        self.combobox_measuring_point_load.setGeometry(
            QtCore.QRect(190, 280, 311, 27))
        self.combobox_measuring_point_load.setObjectName(
            _fromUtf8("combobox_measuring_point_load"))
        self.label_measuring_point_field_description = QtGui.QLabel(
            self.groupbox_measuring_points)
        self.label_measuring_point_field_description.setGeometry(
            QtCore.QRect(530, 20, 231, 41))
        self.label_measuring_point_field_description.setObjectName(
            _fromUtf8("label_measuring_point_field_description"))
        self.label_measuring_point_load_point = QtGui.QLabel(
            self.groupbox_measuring_points)
        self.label_measuring_point_load_point.setGeometry(
            QtCore.QRect(510, 280, 231, 31))
        self.label_measuring_point_load_point.setObjectName(_fromUtf8(
            "label_measuring_point_load_point"))
        self.groupbox_measuring_points.raise_()
        self.buttonbox.raise_()
        self.groupbox_measuring_group.raise_()

        self.retranslateUi(self)
        QtCore.QObject.connect(self.buttonbox, QtCore.SIGNAL(_fromUtf8(
            "accepted()")), self.accept)
        QtCore.QObject.connect(self.buttonbox, QtCore.SIGNAL(_fromUtf8(
            "rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, dialog_create_measuring_group):
        dialog_create_measuring_group.setWindowTitle(_translate(
            "dialog_create_measuring_group", "Create measuring group", None))
        self.groupbox_measuring_group.setTitle(_translate(
            "dialog_create_measuring_group", "Measuring group", None))
        self.label_measuring_group_id.setText(_translate(
            "dialog_create_measuring_group", "id:", None))
        self.pushbutton_measuring_group_load.setText(_translate(
            "dialog_create_measuring_group", "Load measuring group", None))
        self.label_measuring_group_load_description.setText(_translate(
            "dialog_create_measuring_group", "Load a measuring group.", None))
        self.label_measuring_group_description.setText(_translate(
            "dialog_create_measuring_group", "The id of the measure group.",
            None))
        self.groupbox_measuring_points.setTitle(_translate(
            "dialog_create_measuring_group", "Measuring stations", None))
        item = self.tablewidget_measuring_point.horizontalHeaderItem(0)
        item.setText(_translate(
            "dialog_create_measuring_group", "table", None))
        item = self.tablewidget_measuring_point.horizontalHeaderItem(1)
        item.setText(_translate(
            "dialog_create_measuring_group", "table_id", None))
        item = self.tablewidget_measuring_point.horizontalHeaderItem(2)
        item.setText(_translate(
            "dialog_create_measuring_group", "weight", None))
        item = self.tablewidget_measuring_point.horizontalHeaderItem(3)
        item.setText(_translate(
            "dialog_create_measuring_group", "action", None))
        self.label_measuring_point_field.setText(_translate(
            "dialog_create_measuring_group", "field:", None))
        self.combobox_measuring_point_field.setItemText(0, _translate(
            "dialog_create_measuring_group", "initial_waterlevel", None))
        self.pushbutton_measuring_point_add_point.setText(_translate(
            "dialog_create_measuring_group", "Add station", None))
        self.label_measuring_point_add_point.setText(_translate(
            "dialog_create_measuring_group", "<html><head/><body><p>Add a measuring station to the table.</p></body></html>", None))
        self.pushbutton_measuring_point_load.setText(_translate(
            "dialog_create_measuring_group", "Load station", None))
        self.label_measuring_point_field_description.setText(_translate(
            "dialog_create_measuring_group", "The measure value.", None))
        self.label_measuring_point_load_point.setText(_translate(
            "dialog_create_measuring_group", "Load a measuring station.",
            None))
