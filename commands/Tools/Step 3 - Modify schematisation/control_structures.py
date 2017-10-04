# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import logging

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTableWidgetItem

from ThreeDiToolbox.commands.base.custom_command import CustomCommandBase
from ThreeDiToolbox.threedi_schema_edits.controlled_structures import \
    MEASURE_VARIABLE_WATERLEVEL
from ThreeDiToolbox.threedi_schema_edits.controlled_structures import \
    RULE_OPERATOR_BOTTOM_UP
from ThreeDiToolbox.threedi_schema_edits.controlled_structures import \
    RULE_OPERATOR_TOP_DOWN
from ThreeDiToolbox.threedi_schema_edits.controlled_structures import \
    TABLE_CONTROL
from ThreeDiToolbox.threedi_schema_edits.controlled_structures import \
    ControlledStructures
from ThreeDiToolbox.utils.threedi_database import get_databases
from ThreeDiToolbox.utils.threedi_database import get_database_properties
from ThreeDiToolbox.utils.constants import DICT_TABLE_NAMES
from ThreeDiToolbox.utils.constants import DICT_ACTION_TYPES
from ThreeDiToolbox.views.control_structures_dockwidget import ControlStructuresDockWidget  # noqa

log = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):
    """
    command that will load and start an edit session for the connected
    point layer and verify the data added to that layer
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.iface = kwargs.get('iface')
        self.dockwidget_controlled_structures = None
        self.control_structure = None

        self.databases = get_databases()
        # Remove 'selected' spatialite and postgresdatabases
        # from self.databases to prevent confusion about which database
        # is meant by it
        if 'spatialite: ' in self.databases:
            self.databases.pop('spatialite: ', None)
        if 'postgres: None' in self.databases:
            self.databases.pop('postgres: None', None)

    def run(self):
        """Run the controlled structures dockwidget."""
        self.show_gui()
        self.dockwidget_controlled_structures.combobox_input_model\
            .activated.connect(self.update_dockwidget_ids)
        self.setup_measuring_station_tab()
        self.dockwidget_controlled_structures.pushbutton_input_save\
            .clicked.connect(self.run_it)

    def run_it(self):
        """Save the control to the spatialite or POSTGRES database."""
        db_key = self.dockwidget_controlled_structures.combobox_input_model\
            .currentText()  # name of database
        db = get_database_properties(db_key)
        control_structure = ControlledStructures(
            flavor=db["db_entry"]['db_type'])
        control_structure.start_sqalchemy_engine(db["db_settings"])
        # The control_type is the type of control that will be saved.
        # In the future, this type can be read from a combobox.
        # Future options will be table control, pid control,
        # memory control, delta control and timed control.
        control_type = TABLE_CONTROL
        if control_type == TABLE_CONTROL:
            tablewidget = self.dockwidget_controlled_structures\
                .tablewidget_input_rule_table_control
            table_control = {}
            measure_value = tablewidget.item(0, 0).text()
            action_value = tablewidget.item(0, 1).text()
            list_of_values = [measure_value, action_value]
            table_control["action_table"] = control_structure\
                .create_action_table(list_of_values)
            if self.dockwidget_controlled_structures\
                    .combobox_input_rule_operator.currentText()\
                    == 'Bottom up':
                measure_operator = RULE_OPERATOR_BOTTOM_UP
            else:
                measure_operator = RULE_OPERATOR_TOP_DOWN
            table_control["measure_operator"] = measure_operator
            table_control["target_id"] = self.dockwidget_controlled_structures\
                .combobox_input_structure_id.currentText()
            structure_table = self.dockwidget_controlled_structures\
                .combobox_input_structure_table.currentText()
            table_control["target_type"] = DICT_TABLE_NAMES.get(
                structure_table, "")
            table_control["action_type"] = DICT_ACTION_TYPES.get(
                structure_table, "")
            table_control["measure_variable"] = "waterlevel"
            control_structure.save_table_control(table_control)

    def show_gui(self):
        """Show the gui."""
        self.dockwidget_controlled_structures = ControlStructuresDockWidget()
        self.iface.addDockWidget(
            Qt.BottomDockWidgetArea, self.dockwidget_controlled_structures)
        # Show active models
        self.dockwidget_controlled_structures.combobox_input_model.addItems(
            self.databases.keys())
        self.update_dockwidget_ids()
        self.dockwidget_controlled_structures.show()

    def update_dockwidget_ids(self):
        """
        Function to update the control structures dockwidget.
        By clicking on a different model in the GUI, the id's
        for the measuring points and structures are updated.
        """
        db_key = self.dockwidget_controlled_structures.combobox_input_model\
            .currentText()  # name of database
        db = get_database_properties(db_key)
        control_structure = ControlledStructures(
            flavor=db["db_entry"]['db_type'])
        control_structure.start_sqalchemy_engine(db["db_settings"])
        # Set the id's of the connection nodes
        self.dockwidget_controlled_structures.\
            combobox_input_measuring_point_id.clear()
        list_of_measuring_point_ids = control_structure.get_attributes(
            table_name="v2_connection_nodes", attribute_name="id")
        self.dockwidget_controlled_structures.\
            combobox_input_measuring_point_id.addItems(
                list_of_measuring_point_ids)
        # Set the id's of the structures
        self.dockwidget_controlled_structures.\
            combobox_input_structure_id.clear()
        list_of_structure_ids = control_structure.get_attributes(
            table_name="v2_weir_view", attribute_name="weir_id")
        self.dockwidget_controlled_structures.\
            combobox_input_structure_id.addItems(list_of_structure_ids)

    def setup_measuring_station_tab(self):
        """Setup the measuring station tab."""
        self.dockwidget_controlled_structures\
            .pushbutton_input_measuring_point_new.clicked\
            .connect(self.create_new_measuring_point)
        tablewidget = self.dockwidget_controlled_structures\
            .tablewidget_measuring_point
        start_row = 0
        tablewidget.setItem(start_row, 0, QTableWidgetItem(""))
        tablewidget.setCellWidget(
            start_row, 1, self.dockwidget_controlled_structures
            .combobox_input_measuring_point_table)
        tablewidget.setCellWidget(
            start_row, 2, self.dockwidget_controlled_structures
            .combobox_input_measuring_point_id)
        tablewidget.setItem(start_row, 3, QTableWidgetItem(""))
        tablewidget.setCellWidget(
            start_row, 3, self.dockwidget_controlled_structures
            .pushbutton_input_measuring_point_new_2)

    def create_new_measuring_point(self):
        """Create a new measuring point."""
        # Get the model
        db_key = self.dockwidget_controlled_structures\
            .combobox_input_model.currentText()
        db = get_database_properties(db_key)
        control_structure = ControlledStructures(
            flavor=db["db_entry"]['db_type'])
        control_structure.start_sqalchemy_engine(db["db_settings"])
        # Get last id of measure map or set to 0; set to +1
        table_name = "v2_control_measure_map"
        attribute_name = "MAX(id)"
        max_id_measure_map = int(control_structure.get_attributes(
            table_name, attribute_name)[0])
        if not max_id_measure_map:
            max_id_measure_map = 0
        new_max_id_measure_map = max_id_measure_map + 1
        # Populate the new row in the table
        self.populate_measuring_point_row(new_max_id_measure_map)
        # Insert the variables in the v2_control_table
        measuring_point_table = self.dockwidget_controlled_structures\
            .combobox_input_measuring_point_table.currentText()
        measuring_point_table_id = self.dockwidget_controlled_structures\
            .combobox_input_measuring_point_id.currentText()
        attributes = {}
        attributes["id"] = new_max_id_measure_map
        attributes["object_type"] = measuring_point_table
        attributes["object_id"] = measuring_point_table_id
        control_structure.insert_into_table(table_name, attributes)
        # Set the new ids of the v2_control_measure_map
        self.update_dockwidget_ids()

    def populate_measuring_point_row(self, id_measuring_point):
        """
        Populate a row from te measuring point table.

        Args:
            (str) id_measuring_point: The id of the measuring point."""
        tablewidget = self.dockwidget_controlled_structures\
            .tablewidget_measuring_point
        # Always put the new row on top.
        row_position = 1
        tablewidget.insertRow(row_position)
        measuring_point_id = QTableWidgetItem(str(id_measuring_point))
        tablewidget.setItem(row_position, 0, measuring_point_id)
        measuring_point_table_widget = QTableWidgetItem(
            self.dockwidget_controlled_structures
            .combobox_input_measuring_point_table.currentText())
        tablewidget.setItem(row_position, 1, measuring_point_table_widget)
        measuring_point_table_id_widget = QTableWidgetItem(
            self.dockwidget_controlled_structures
            .combobox_input_measuring_point_id.currentText())
        tablewidget.setItem(row_position, 2, measuring_point_table_id_widget)
        measuring_point_remove_widget = QPushButton("Remove")
        tablewidget = self.dockwidget_controlled_structures\
            .tablewidget_measuring_point
        measuring_point_remove_widget.clicked.connect(
            self.remove_measuring_point_row)
        tablewidget.setCellWidget(
            row_position, 3, measuring_point_remove_widget)

    def remove_measuring_point_row(self):
        """Remove a row from the measuring point table."""
        tablewidget = self.dockwidget_controlled_structures\
            .tablewidget_measuring_point
        row_number = tablewidget.currentRow()
        # Don't remove the first row.
        dont_remove = 0
        if row_number != dont_remove:
            tablewidget.removeRow(row_number)
