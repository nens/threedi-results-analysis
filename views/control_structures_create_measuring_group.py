# -*- coding: utf-8 -*-
import os
import logging


from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
from PyQt4.QtGui import QAbstractItemView
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


class CreateMeasuringGroupDialogWidget(QDialog, FORM_CLASS):

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
        # Show gui
        self.setupUi(self)

        self.measuring_group_id = measuring_group_id
        self.command = command
        self.dockwidget_controlled_structures = \
            dockwidget_controlled_structures

        self.db_key = db_key
        self.databases = get_databases()
        self.db = get_database_properties(self.db_key)
        self.control_structure = ControlledStructures(
            flavor=self.db["db_entry"]['db_type'])
        self.setup_tablewidget()
        self.update_ids()
        self.connect_signals()

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

    def setup_tablewidget(self):
        tablewidget = self.tablewidget_measuring_point
        tablewidget.setCellWidget(
            0, 0, self.combobox_input_measuring_point_table)
        tablewidget.setCellWidget(0, 1, self.combobox_input_measuring_point_id)
        tablewidget.setCellWidget(
            0, 3, self.pushbutton_input_measuring_point_new)

    def update_ids(self):
        """Setup the id's for the measuring group and measuring points."""
        # Set the id of the measuring group
        self.label_measuring_group_id_info.setText(self.measuring_group_id)
        self.control_structure.start_sqalchemy_engine(self.db["db_settings"])
        # Set all id's of the measuring groups
        self.combobox_measuring_group_load.clear()
        list_of_measuring_group_ids = self.control_structure.get_attributes(
            table_name="v2_control_measure_group", attribute_name="id")
        self.combobox_measuring_group_load.addItems(
            list_of_measuring_group_ids)
        # Set all id's of the connection nodes
        self.combobox_input_measuring_point_id.clear()
        list_of_connection_node_ids = self.control_structure.get_attributes(
            table_name="v2_connection_nodes", attribute_name="id")
        self.combobox_input_measuring_point_id.addItems(
            list_of_connection_node_ids)

    def connect_signals(self):
        """Connect the signals."""
        self.pushbutton_measuring_group_load.clicked.connect(
            self.load_measuring_group)
        self.pushbutton_input_measuring_point_new.clicked.connect(
            self.create_new_measuring_point)
        self.buttonbox.accepted.connect(self.on_accept)
        self.buttonbox.rejected.connect(self.on_reject)

    def create_new_measuring_point(self):
        # Get the model
        self.control_structure.start_sqalchemy_engine(self.db["db_settings"])
        # Get last id of measure map or set to 0; set to +1
        table_name = "v2_control_measure_map"
        attribute_name = "MAX(id)"
        try:
            max_id_measure_map = int(self.control_structure.get_attributes(
                table_name, attribute_name)[0])
        except ValueError:
            max_id_measure_map = 0
        new_max_id_measure_map = max_id_measure_map + 1
        # Populate the new row in the table
        self.populate_measuring_point_row(new_max_id_measure_map)

    def populate_measuring_point_row(self, id_measuring_point):
        """
        Populate a row from the measuring point table.

        Args:
            (str) id_measuring_point: The id of the measuring point."""
        tablewidget = self.tablewidget_measuring_point
        # Always put the new row on top.
        row_position = 1
        tablewidget.insertRow(row_position)
        measuring_point_id = QTableWidgetItem(str(id_measuring_point))
        # tablewidget.setItem(row_position, 0, measuring_point_id)
        measuring_point_table_widget = QTableWidgetItem(
            self.combobox_input_measuring_point_table.currentText())
        tablewidget.setItem(row_position, 0, measuring_point_table_widget)
        measuring_point_table_id_widget = QTableWidgetItem(
            self.combobox_input_measuring_point_id.currentText())
        tablewidget.setItem(row_position, 1, measuring_point_table_id_widget)
        try:
            measuring_point_weight = tablewidget.item(0, 2).text()
        except AttributeError:
            measuring_point_weight = ""
        tablewidget.setItem(
            row_position, 2, QTableWidgetItem(measuring_point_weight))
        measuring_point_remove_widget = QPushButton("Remove")
        measuring_point_remove_widget.clicked.connect(
            self.remove_measuring_point_row)
        tablewidget.setCellWidget(
            row_position, 3, measuring_point_remove_widget)

    def remove_measuring_point_row(self):
        """Remove a row from the measuring point table."""
        tablewidget = self.tablewidget_measuring_point
        row_number = tablewidget.currentRow()
        # Remove measuring point from dockwidget
        # Don't remove the first row.
        BUTTON_ROW = 0
        if row_number != BUTTON_ROW:
            tablewidget.removeRow(row_number)

    def load_measuring_group(self):
        """Load a measuring group in the tablewidget."""
        # Remove all current rows, besides te first.
        tablewidget = self.tablewidget_measuring_point
        BUTTON_ROW = 0
        row_count = tablewidget.rowCount()
        for row in range(row_count - 1):
            tablewidget.removeRow(1)
        self.control_structure.start_sqalchemy_engine(self.db["db_settings"])
        # Get all the measuring points from a certain measure group
        table_name = "v2_control_measure_map"
        attribute_name = "*"
        where_clause = "measure_group_id={}".format(
            self.combobox_measuring_group_load.currentText())
        measure_groups = self.control_structure.get_features_with_where_clause(
            table_name=table_name, attribute_name=attribute_name,
            where=where_clause)
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
            measuring_point_remove.clicked.connect(self.remove_measuring_point)
            self.tablewidget_measuring_point.setCellWidget(
                row_position, 3, measuring_point_remove)

    def remove_measuring_point(self):
        """Remove a certain measuring point from the tablewidget."""
        tablewidget = self.tablewidget_measuring_point
        row_number = tablewidget.currentRow()
        tablewidget.removeRow(row_number)

    def save_measuring_group(self):
        """Save the measuring group in the database."""
        self.control_structure.start_sqalchemy_engine(self.db["db_settings"])
        # Insert the measuring group in the v2_control_measure_group
        table_name = "v2_control_measure_group"
        attributes = {
            "id": self.measuring_group_id
        }
        self.control_structure.insert_into_table(
            table_name=table_name, attributes=attributes)
        # Create a tab in the tabwidget of the 'Measuring group' tab in
        # the controlled structures dockwidget
        self.add_measuring_group_tab_dockwidget()
        table_name = "v2_control_measure_map"
        BUTTON_ROW = 0
        for row in range(self.tablewidget_measuring_point.rowCount()):
            if row != BUTTON_ROW:
                # Get the new measuring_point id
                attribute_name = "MAX(id)"
                try:
                    max_id_measure_point = int(
                        self.control_structure.get_attributes(
                            table_name, attribute_name)[0])
                except ValueError:
                    max_id_measure_point = 0
                new_measuring_point_id = max_id_measure_point + 1
                measure_point_attributes = self.get_measuring_point_attributes(
                    row, new_measuring_point_id)
                # Save the measuring point in the v2_control_measure_map
                self.control_structure.insert_into_table(
                    table_name, measure_point_attributes)
                # Setup new tab of "Measuring group" tab
                self.setup_measuring_group_table_dockwidget(
                    measure_point_attributes)

    def add_measuring_group_tab_dockwidget(self):
        """
        Create a tab for the measure group within the Measure group tab
        in the dockwidget.
        """
        tab = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(tab)
        tab.setLayout(layout)

        table_measuring_group = QtGui.QTableWidget(tab)
        table_measuring_group.setGeometry(10, 10, 741, 266)
        table_measuring_group.insertColumn(0)
        table_measuring_group.setHorizontalHeaderItem(
            0, QTableWidgetItem("table"))
        table_measuring_group.insertColumn(1)
        table_measuring_group.setHorizontalHeaderItem(
            1, QTableWidgetItem("table_id"))
        table_measuring_group.insertColumn(2)
        table_measuring_group.setHorizontalHeaderItem(
            2, QTableWidgetItem("weight"))
        table_measuring_group.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dockwidget_controlled_structures.table_measuring_group = \
            table_measuring_group
        # Add the tab to the left
        self.dockwidget_controlled_structures\
            .tab_measuring_group_view_2.insertTab(
                0, tab, "Group: {}".format(
                    str(self.label_measuring_group_id_info.text())))

    def get_measuring_point_attributes(self, row_nr, new_measuring_point_id):
        """
        Get the attributes of the measuring point from the table.


        Args:
            (int) row_nr: The row number of the tablewidget.
            (int) new_measuring_point_id: The id of the new measuring point.

        Returns:
            (dict) attributes: A list containing the attributes
                               of the measuring point.
        """
        measuring_point_table = self.tablewidget_measuring_point.item(
            row_nr, 0).text()
        try:
            measuring_point_table_id = self.tablewidget_measuring_point\
                .item(row_nr, 1).text()
        except AttributeError:
            measuring_point_table_id = self.tablewidget_measuring_point\
                .cellWidget(row_nr, 1).currentText()
        try:
            measuring_point_weight = self.tablewidget_measuring_point.item(
                row_nr, 2).text()
        except AttributeError:
            measuring_point_weight = ""
        attributes = {
            "id": new_measuring_point_id,
            "measure_group_id": self.measuring_group_id,
            "object_type": measuring_point_table,
            "object_id": measuring_point_table_id,
            "weight": measuring_point_weight
        }
        return attributes

    def setup_measuring_group_table_dockwidget(
            self, measure_map_attributes):
        """
        Setup a tab for the measure group in the Measure group tab
        in the dockwidget.

        Args:
            (dict) measure_map_attributes: A dict containing the attributes
                                           from the measuring point
                                            (from v2_control_measure_map).
        """
        row_position = self.dockwidget_controlled_structures\
            .table_measuring_group.rowCount()
        self.dockwidget_controlled_structures\
            .table_measuring_group.insertRow(row_position)
        self.dockwidget_controlled_structures.table_measuring_group\
            .setItem(row_position, 0, QTableWidgetItem(
                "v2_connection_nodes"))
        self.dockwidget_controlled_structures.table_measuring_group\
            .setItem(row_position, 1, QTableWidgetItem(
                measure_map_attributes["object_id"]))
        self.dockwidget_controlled_structures.table_measuring_group\
            .setItem(row_position, 2, QTableWidgetItem(
                measure_map_attributes["weight"]))
