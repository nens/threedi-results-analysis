# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import logging

from PyQt4.QtCore import Qt

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
            if self.dockwidget_controlled_structures\
                    .combobox_input_measuring_point_field.currentText()\
                    == "initial_waterlevel":
                measure_variable = MEASURE_VARIABLE_WATERLEVEL
            else:
                measure_variable = ""
            table_control["measure_variable"] = measure_variable
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
        self.dockwidget_controlled_structures.\
            combobox_input_measuring_point_id.clear()
        self.dockwidget_controlled_structures.\
            combobox_input_structure_id.clear()
        db_key = self.dockwidget_controlled_structures.combobox_input_model\
            .currentText()  # name of database
        db = get_database_properties(db_key)
        control_structure = ControlledStructures(
            flavor=db["db_entry"]['db_type'])
        control_structure.start_sqalchemy_engine(db["db_settings"])
        # Get all id's of the connection nodes
        list_of_measuring_point_ids = control_structure.get_attributes(
            table_name="v2_connection_nodes", attribute_name="id")
        self.dockwidget_controlled_structures.\
            combobox_input_measuring_point_id.addItems(
                list_of_measuring_point_ids)
        # Get the id's of the structures
        list_of_structure_ids = control_structure.get_attributes(
            table_name="v2_weir_view", attribute_name="weir_id")
        self.dockwidget_controlled_structures.\
            combobox_input_structure_id.addItems(list_of_structure_ids)
