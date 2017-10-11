# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import logging

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget

from ThreeDiToolbox.commands.base.custom_command import CustomCommandBase
from ThreeDiToolbox.threedi_schema_edits.controlled_structures import \
    RULE_OPERATOR_BOTTOM_UP
from ThreeDiToolbox.threedi_schema_edits.controlled_structures import \
    RULE_OPERATOR_TOP_DOWN
from ThreeDiToolbox.threedi_schema_edits.controlled_structures import \
    TABLE_CONTROL
from ThreeDiToolbox.threedi_schema_edits.controlled_structures import \
    ControlledStructures
from ThreeDiToolbox.views.control_structures_create_measuring_group import \
    CreateMeasuringGroupDialogWidget # noqa
from ThreeDiToolbox.views.control_structures_create_table_control_dialog \
    import CreateTableControlDialogWidget # noqa
from ThreeDiToolbox.utils.threedi_database import get_databases
from ThreeDiToolbox.utils.threedi_database import get_database_properties
from ThreeDiToolbox.utils.constants import DICT_TABLE_NAMES
from ThreeDiToolbox.utils.constants import DICT_ACTION_TYPES
from ThreeDiToolbox.views.control_structures_dockwidget import \
    ControlStructuresDockWidget  # noqa

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
        self.setup_measuring_group_tab()
        self.setup_rule_tab()
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
        # Set the id's of the measuring groups
        self.dockwidget_controlled_structures.\
            combobox_input_measuring_group_view.clear()
        list_of_measuring_group_ids = control_structure.get_attributes(
            table_name="v2_control_measure_group", attribute_name="id")
        self.dockwidget_controlled_structures.\
            combobox_input_measuring_group_view.addItems(
                list_of_measuring_group_ids)
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
            .pushbutton_input_measuring_point_new)

    def setup_measuring_group_tab(self):
        """Setup the measuring station tab."""
        self.dockwidget_controlled_structures\
            .pushbutton_input_measuring_group_new.clicked.connect(
                self.create_new_measuring_group)
        self.dockwidget_controlled_structures\
            .pushbutton_input_measuring_group_view.clicked.connect(
                self.view_measuring_group)
        self.dockwidget_controlled_structures\
            .pushbutton_input_measuring_group_clear.clicked.connect(
                self.remove_all_measuring_group_tabs)
        self.dockwidget_controlled_structures.tab_measuring_group_view_2\
            .tabCloseRequested.connect(self.remove_measuring_group_tab)

    def setup_rule_tab(self):
        """Setup the rule tab."""
        self.dockwidget_controlled_structures\
            .pushbutton_input_rule_new.clicked.connect(
                self.create_new_rule)

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
        try:
            max_id_measure_map = int(control_structure.get_attributes(
                table_name, attribute_name)[0])
        except ValueError:
            max_id_measure_map = 0
        new_max_id_measure_map = max_id_measure_map + 1
        # Populate the new row in the table
        self.populate_measuring_point_row(new_max_id_measure_map)
        # Insert the variables in the v2_control_table
        measuring_point_table = self.dockwidget_controlled_structures\
            .combobox_input_measuring_point_table.currentText()
        measuring_point_table_id = self.dockwidget_controlled_structures\
            .combobox_input_measuring_point_id.currentText()
        attributes = {
            "id": new_max_id_measure_map,
            "object_type": measuring_point_table,
            "object_id": measuring_point_table_id
        }
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

    def create_new_measuring_group(self):
        """Create a new measuring group."""
        db_key = self.dockwidget_controlled_structures\
            .combobox_input_model.currentText()  # name of database
        db = get_database_properties(db_key)
        control_structure = ControlledStructures(
            flavor=db["db_entry"]['db_type'])
        control_structure.start_sqalchemy_engine(db["db_settings"])
        # Get last id of measure group or set to 0; set to +1
        table_name = "v2_control_measure_group"
        attribute_name = "MAX(id)"
        try:
            max_id_measure_group = int(control_structure.get_attributes(
                table_name, attribute_name)[0])
        except ValueError:
            max_id_measure_group = 0
        new_id_measure_group = max_id_measure_group + 1
        self.dialog_create_measuring_group = \
            CreateMeasuringGroupDialogWidget(
                command=self, db_key=db_key,
                measuring_group_id=str(new_id_measure_group),
                dockwidget_controlled_structures=self.
                dockwidget_controlled_structures)
        self.dialog_create_measuring_group.exec_()  # block execution

    def view_measuring_group(self):
        """View a measuring group in a new tab in the Measure groups tab."""
        measuring_group_id_name = "measure_group_id"
        measuring_group_id = self.dockwidget_controlled_structures\
            .combobox_input_measuring_group_view.currentText()
        if measuring_group_id == "":
            return
        else:
            attribute_name = "*"
            table_name = "v2_control_measure_map"
            where = "{id_name} = {id_value}"\
                .format(id_name=measuring_group_id_name,
                        id_value=measuring_group_id)
            db_key = self.dockwidget_controlled_structures\
                .combobox_input_model.currentText()  # name of database
            db = get_database_properties(db_key)
            control_structure = ControlledStructures(
                flavor=db["db_entry"]['db_type'])
            control_structure.start_sqalchemy_engine(db["db_settings"])
            measure_group = control_structure.get_features_with_where_clause(
                table_name, attribute_name, where)
            # Add a tab in the tabwidget of the 'Measuring group' tab in
            # the controlled structures dockwidget
            self.populate_measuring_group_tab(
                measuring_group_id, measure_group)

    def populate_measuring_group_tab(self, measuring_group_id, measure_group):
        """
        Add a tab in the tabwidget of the 'Measuring group' tab.

        Args:
            (int) measuring_group_id: The id of the measure group.
            (list) measure_group: A list of tuples. The tuples contain the
                                  different measuring points.
        """
        self.create_measuring_group_tab(measuring_group_id)
        # Populate new tab of "Measuring group" tab
        for measure_point in measure_group:
            row_position = self.dockwidget_controlled_structures\
                .table_measuring_group.rowCount()
            self.dockwidget_controlled_structures\
                .table_measuring_group.insertRow(row_position)
            self.dockwidget_controlled_structures.table_measuring_group\
                .setItem(row_position, 0, QTableWidgetItem(
                    "v2_connection_nodes"))
            self.dockwidget_controlled_structures.table_measuring_group\
                .setItem(row_position, 1, QTableWidgetItem(
                    str(measure_point[3])))
            self.dockwidget_controlled_structures.table_measuring_group\
                .setItem(row_position, 2, QTableWidgetItem(
                    str(measure_point[4])))

    def create_measuring_group_tab(self, measuring_group_id):
        """Create a tab in the Measuring group tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        tab.setLayout(layout)

        label_field = QLabel(tab)
        label_field.setGeometry(10, 10, 741, 21)
        label_field.setText("Field: {}".format("initial_waterlevel"))

        table_measuring_group = QTableWidget(tab)
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
        # Set the new tab as the first tab
        self.dockwidget_controlled_structures\
            .tab_measuring_group_view_2.insertTab(0, tab, "Group: {}".format(
                str(measuring_group_id)))

    def remove_measuring_group_tab(self):
        """Remove a tab in the Measuring group tab."""
        self.dockwidget_controlled_structures.tab_measuring_group_view_2\
            .removeTab(self.dockwidget_controlled_structures
                       .tab_measuring_group_view_2.currentIndex())

    def remove_all_measuring_group_tabs(self):
        """Remove all tabs in the Measuring group tab."""
        self.dockwidget_controlled_structures.tab_measuring_group_view_2\
            .clear()

    def create_new_rule(self):
        """Create a new rule."""
        self.dialog_create_table_control = CreateTableControlDialogWidget()
        self.dialog_create_table_control.exec_()  # block execution
