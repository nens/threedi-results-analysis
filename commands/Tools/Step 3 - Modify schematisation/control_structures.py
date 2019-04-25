# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

from builtins import str
from builtins import range
import logging

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAbstractItemView
from qgis.PyQt.QtWidgets import QLabel
from qgis.PyQt.QtWidgets import QTableWidget
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.PyQt.QtWidgets import QWidget

from ThreeDiToolbox.commands.base.custom_command import CustomCommandBase
from ThreeDiToolbox.threedi_schema_edits.controlled_structures import (
    ControlledStructures,
)
from ThreeDiToolbox.views.control_structures_create_measuring_group import (
    CreateMeasuringGroupDialogWidget,
)
from ThreeDiToolbox.views.control_structures_create_table_control_dialog import (
    CreateTableControlDialogWidget,
)
from ThreeDiToolbox.views.control_structures_create_control_group_dialog import (
    CreateControlGroupDialogWidget,
)
from ThreeDiToolbox.utils.threedi_database import get_databases
from ThreeDiToolbox.utils.threedi_database import get_database_properties
from ThreeDiToolbox.views.control_structures_dockwidget import (
    ControlStructuresDockWidget,
)

logger = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):
    """
    command that will load and start an edit session for the connected
    point layer and verify the data added to that layer
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.iface = kwargs.get("iface")
        self.dockwidget_controlled_structures = None
        self.control_structure = None

        self.databases = get_databases()
        # Remove 'selected' spatialite and postgresdatabases
        # from self.databases to prevent confusion about which database
        # is meant by it
        if "spatialite: " in self.databases:
            self.databases.pop("spatialite: ", None)
        if "postgres: None" in self.databases:
            self.databases.pop("postgres: None", None)

    def run(self):
        """Run the controlled structures dockwidget."""
        self.show_gui()
        self.setup_model_tab()
        self.setup_measuring_station_tab()
        self.setup_measuring_group_tab()
        self.setup_rule_tab()
        self.setup_control_group_tab()

    def run_it(self):
        """Run the controlled structures dockwidget."""

    def show_gui(self):
        """Show the gui."""
        self.dockwidget_controlled_structures = ControlStructuresDockWidget()
        self.iface.addDockWidget(
            Qt.BottomDockWidgetArea, self.dockwidget_controlled_structures
        )
        # Show active models
        self.dockwidget_controlled_structures.combobox_input_model.addItems(
            list(self.databases.keys())
        )
        self.dockwidget_controlled_structures.show()

    def update_dockwidget_ids(self):
        """
        Function to update the control structures dockwidget.
        By clicking on a different model in the GUI, the id's
        for the measuring points and structures are updated.
        """
        db_key = (
            self.dockwidget_controlled_structures.combobox_input_model.currentText()
        )  # name of database
        db = get_database_properties(db_key)
        control_structure = ControlledStructures(flavor=db["db_entry"]["db_type"])
        control_structure.start_sqalchemy_engine(db["db_settings"])
        self.update_measuring_group_ids(control_structure)
        self.update_measuring_point_ids(control_structure)
        self.update_rule_ids(control_structure)
        self.update_control_ids(control_structure)

    def update_measuring_group_ids(self, control_structure):
        self.dockwidget_controlled_structures.combobox_input_measuring_group_view.clear()
        self.dockwidget_controlled_structures.combobox_input_measuring_group_delete.clear()
        list_of_measuring_group_ids = control_structure.get_attributes(
            table_name="v2_control_measure_group", attribute_name="id"
        )
        self.dockwidget_controlled_structures.combobox_input_measuring_group_view.addItems(
            list_of_measuring_group_ids
        )
        self.dockwidget_controlled_structures.combobox_input_measuring_group_delete.addItems(
            list_of_measuring_group_ids
        )

    def update_measuring_point_ids(self, control_structure):
        self.dockwidget_controlled_structures.combobox_input_measuring_point_view.clear()
        list_of_measuring_group_ids = control_structure.get_attributes(
            table_name="v2_control_measure_map", attribute_name="id"
        )
        self.dockwidget_controlled_structures.combobox_input_measuring_point_view.addItems(
            list_of_measuring_group_ids
        )

    def update_rule_ids(self, control_structure):
        self.dockwidget_controlled_structures.combobox_input_rule_view.clear()
        self.dockwidget_controlled_structures.combobox_input_rule_delete.clear()
        list_of_rule_ids = control_structure.get_attributes(
            table_name="v2_control_table", attribute_name="id"
        )
        self.dockwidget_controlled_structures.combobox_input_rule_view.addItems(
            list_of_rule_ids
        )
        self.dockwidget_controlled_structures.combobox_input_rule_delete.addItems(
            list_of_rule_ids
        )

    def update_control_ids(self, control_structure):
        self.dockwidget_controlled_structures.combobox_input_control_view.clear()
        self.dockwidget_controlled_structures.combobox_input_control_delete.clear()
        list_of_rule_ids = control_structure.get_attributes(
            table_name="v2_control_group", attribute_name="id"
        )
        self.dockwidget_controlled_structures.combobox_input_control_view.addItems(
            list_of_rule_ids
        )
        self.dockwidget_controlled_structures.combobox_input_control_delete.addItems(
            list_of_rule_ids
        )

    def setup_model_tab(self):
        """
        Connect the signals for the model tab.
        By clicking on a different model in the GUI, the id's
        for the measuring points and structures are updated.
        """
        self.dockwidget_controlled_structures.combobox_input_model.currentIndexChanged.connect(
            self.clear_all_tabs
        )
        self.dockwidget_controlled_structures.combobox_input_model.activated.connect(
            self.update_dockwidget_ids
        )

    def setup_measuring_group_tab(self):
        """Connect the signals for the measuring group tab."""
        self.dockwidget_controlled_structures.pushbutton_input_measuring_group_new.clicked.connect(
            self.create_new_measuring_group
        )
        self.dockwidget_controlled_structures.pushbutton_input_measuring_group_view.clicked.connect(
            self.view_measuring_group
        )
        self.dockwidget_controlled_structures.pushbutton_input_measuring_group_close_all.clicked.connect(
            self.remove_all_measuring_group_tabs
        )
        self.dockwidget_controlled_structures.tab_measuring_group_view_2.tabCloseRequested.connect(
            self.remove_measuring_group_tab
        )
        self.dockwidget_controlled_structures.pushbutton_input_measuring_group_delete.clicked.connect(
            self.delete_measuring_group_from_database
        )

    def setup_measuring_station_tab(self):
        """Connect the signals for the measuring station tab."""
        self.dockwidget_controlled_structures.pushbutton_input_measuring_point_view_all.clicked.connect(
            self.view_all_measuring_points
        )
        self.dockwidget_controlled_structures.pushbutton_input_measuring_point_view.clicked.connect(
            self.view_measuring_point
        )
        self.dockwidget_controlled_structures.pushbutton_input_measuring_point_clear.clicked.connect(
            self.clear_measuring_point_table
        )
        tablewidget = self.dockwidget_controlled_structures.tablewidget_measuring_point
        tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def setup_rule_tab(self):
        """Connect the signals for the rule tab."""
        self.dockwidget_controlled_structures.pushbutton_input_rule_new.clicked.connect(
            self.create_new_rule
        )
        self.dockwidget_controlled_structures.pushbutton_input_rule_view.clicked.connect(
            self.view_rule
        )
        self.dockwidget_controlled_structures.pushbutton_input_rule_close_all.clicked.connect(
            self.remove_all_rule_tabs
        )
        self.dockwidget_controlled_structures.tab_table_control_view.tabCloseRequested.connect(
            self.remove_rule_tab
        )
        self.dockwidget_controlled_structures.pushbutton_input_rule_delete.clicked.connect(
            self.delete_rule_from_database
        )

    def setup_control_group_tab(self):
        """Connect the signals for the control tab."""
        self.dockwidget_controlled_structures.pushbutton_input_control_new.clicked.connect(
            self.create_new_control_group
        )
        self.dockwidget_controlled_structures.pusbutton_input_control_view.clicked.connect(
            self.view_control_group
        )
        self.dockwidget_controlled_structures.pushbutton_control_close_all.clicked.connect(
            self.remove_all_control_tabs
        )
        self.dockwidget_controlled_structures.tab_control_view.tabCloseRequested.connect(
            self.remove_control_tab
        )
        self.dockwidget_controlled_structures.pushbutton_control_delete.clicked.connect(
            self.delete_control_group_from_database
        )

    def clear_all_tabs(self):
        """Clear all the tabs of the dockwidget."""
        self.clear_measuring_point_table()
        self.remove_all_measuring_group_tabs()
        self.remove_all_rule_tabs()
        self.remove_all_control_tabs()

    def connect_to_database(self):
        """
        This function sets up a connection to the database with the database
        key selected in the Model tab.

        Returns:
            (ControlledStructures) control_structure: The connection to the
                database. With this connection, inserts and deletes can be
                done.
        """
        db_key = (
            self.dockwidget_controlled_structures.combobox_input_model.currentText()
        )
        db = get_database_properties(db_key)
        control_structure = ControlledStructures(flavor=db["db_entry"]["db_type"])
        control_structure.start_sqalchemy_engine(db["db_settings"])
        return control_structure

    def create_new_measuring_group(self):
        """
        Open a dialog for creating and saving a new measuring group in the
        database. A new id for this measuring group is created to show in
        the dialog.
        """
        control_structure = self.connect_to_database()
        db_key = (
            self.dockwidget_controlled_structures.combobox_input_model.currentText()
        )
        table_name = "v2_control_measure_group"
        attribute_name = "MAX(id)"
        # Get last id of measure group or set to 0; set to +1
        try:
            max_id_measure_group = int(
                control_structure.get_attributes(table_name, attribute_name)[0]
            )
        except ValueError:
            max_id_measure_group = 0
        new_id_measure_group = max_id_measure_group + 1
        self.dialog_create_measuring_group = CreateMeasuringGroupDialogWidget(
            command=self,
            db_key=db_key,
            measuring_group_id=str(new_id_measure_group),
            dockwidget_controlled_structures=self.dockwidget_controlled_structures,
        )
        self.dialog_create_measuring_group.exec_()  # block execution
        self.update_measuring_point_ids(control_structure)
        self.update_measuring_group_ids(control_structure)

    def view_measuring_group(self):
        """
        View a measuring group in a new tab in the Measuring groups tab.
        A new tab is created with the measuring group id of the selected
        combobox, and populated with data of this measuring group.
        """
        measuring_group_id_name = "measure_group_id"
        measuring_group_id = (
            self.dockwidget_controlled_structures.combobox_input_measuring_group_view.currentText()
        )
        if measuring_group_id == "":
            return
        else:
            attribute_name = "*"
            table_name = "v2_control_measure_map"
            where = "{id_name} = {id_value}".format(
                id_name=measuring_group_id_name, id_value=measuring_group_id
            )
            control_structure = self.connect_to_database()
            measure_group = control_structure.get_features_with_where_clause(
                table_name, attribute_name, where
            )
            # Add a tab in the tabwidget of the 'Measuring group' tab in
            # the controlled structures dockwidget
            self.populate_measuring_group_tab(measuring_group_id, measure_group)

    def populate_measuring_group_tab(self, measuring_group_id, measure_group):
        """
        Add and populate a tab in the tabwidget of the 'Measuring group' tab.

        Args:
            (int) measuring_group_id: The id of the measure group.
            (list) measure_group: A list of tuples. The tuples contain the
                                  different measuring points.
        """
        self.create_measuring_group_tab(measuring_group_id)
        # Populate new tab of "Measuring group" tab
        for measure_point in measure_group:
            row_position = (
                self.dockwidget_controlled_structures.table_measuring_group.rowCount()
            )
            self.dockwidget_controlled_structures.table_measuring_group.insertRow(
                row_position
            )
            self.dockwidget_controlled_structures.table_measuring_group.setItem(
                row_position, 0, QTableWidgetItem("v2_connection_nodes")
            )
            self.dockwidget_controlled_structures.table_measuring_group.setItem(
                row_position, 1, QTableWidgetItem(str(measure_point[3]))
            )
            self.dockwidget_controlled_structures.table_measuring_group.setItem(
                row_position, 2, QTableWidgetItem(str(measure_point[4]))
            )

    def create_measuring_group_tab(self, measuring_group_id):
        """
        Create a new measuring group in te Measuring group tab.
        The new tab is added to the left.
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        tab.setLayout(layout)

        table_measuring_group = QTableWidget(tab)
        table_measuring_group.setGeometry(10, 10, 741, 266)
        table_measuring_group.insertColumn(0)
        table_measuring_group.setHorizontalHeaderItem(0, QTableWidgetItem("table"))
        table_measuring_group.insertColumn(1)
        table_measuring_group.setHorizontalHeaderItem(1, QTableWidgetItem("table_id"))
        table_measuring_group.insertColumn(2)
        table_measuring_group.setHorizontalHeaderItem(2, QTableWidgetItem("weight"))
        table_measuring_group.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dockwidget_controlled_structures.table_measuring_group = (
            table_measuring_group
        )
        # Set the new tab as the first tab
        self.dockwidget_controlled_structures.tab_measuring_group_view_2.insertTab(
            0, tab, "Group: {}".format(str(measuring_group_id))
        )

    def remove_measuring_group_tab(self):
        self.dockwidget_controlled_structures.tab_measuring_group_view_2.removeTab(
            self.dockwidget_controlled_structures.tab_measuring_group_view_2.currentIndex()
        )

    def remove_all_measuring_group_tabs(self):
        self.dockwidget_controlled_structures.tab_measuring_group_view_2.clear()

    def delete_measuring_group_from_database(self):
        """
        Delete a measuring group from the database.
        Measuring stations that belong to these measuring groups are
        deleted.
        Controls that contain these measuring groups are also
        deleted. If this results in an empty control group, this control
        group is also removed from the database and from the Control group
        tab.
        Tabs that contain these measuring groups are removed from the
        Measuring group tab.
        """
        control_structure = self.connect_to_database()
        # Get id of measuring group
        measuring_group_id = (
            self.dockwidget_controlled_structures.combobox_input_measuring_group_delete.currentText()
        )
        # Remove measuring points of the measuring group from database
        table_name = "v2_control_measure_map"
        where = " WHERE measure_group_id = '{}'".format(str(measuring_group_id))
        control_structure.delete_from_database(table_name=table_name, where=where)
        # Remove the database entries of the controls the measuring group is
        # linked to and delete them. Delete empty control groups
        id_name = "measure_group_id"
        id_value = measuring_group_id
        tabwidget = self.dockwidget_controlled_structures.tab_control_view
        control_structure.delete_controls_and_control_groups(
            id_name, id_value, tabwidget
        )
        # Remove measuring group from database
        table_name = "v2_control_measure_group"
        where = " WHERE id = '{}'".format(str(measuring_group_id))
        control_structure.delete_from_database(table_name=table_name, where=where)
        # Remove measuring group from tabs in Measuring group tab
        tabwidget = self.dockwidget_controlled_structures.tab_measuring_group_view_2
        tabs_to_remove = []
        tab_number = tabwidget.count()
        for tab in range(tab_number):
            if tabwidget.tabText(tab) == "Group: {}".format(measuring_group_id):
                tabs_to_remove += [tab]
        # Removing a tabs makes the tab go to the left, so delete the tabs in
        # reversed order (from right to left)
        [tabwidget.removeTab(tab) for tab in reversed(tabs_to_remove)]
        self.update_measuring_point_ids(control_structure)
        self.update_measuring_group_ids(control_structure)
        self.update_control_ids(control_structure)

    def view_all_measuring_points(self):
        """
        View all the measuring stations in the Measuring station tab.
        The ids of the measuring stations are obtained from the database.
        A new row is made in the tab for each measuring station.
        """
        tablewidget = self.dockwidget_controlled_structures.tablewidget_measuring_point
        self.clear_measuring_point_table()
        control_structure = self.connect_to_database()
        table_name = "v2_control_measure_map"
        attribute_name = "*"
        measure_points = control_structure.get_attributes(
            table_name=table_name, attribute_name=attribute_name, all_features=True
        )
        for measure_point in measure_points:
            row_position = tablewidget.rowCount()
            tablewidget.insertRow(row_position)
            measuring_point_id = QTableWidgetItem(str(measure_point[0]))
            tablewidget.setItem(row_position, 0, measuring_point_id)
            measuring_point_table = QTableWidgetItem(str(measure_point[2]))
            tablewidget.setItem(row_position, 1, measuring_point_table)
            measuring_point_table_id = QTableWidgetItem(str(measure_point[3]))
            tablewidget.setItem(row_position, 2, measuring_point_table_id)

    def view_measuring_point(self):
        """
        View a measuring station in 'Ḿeasuring station' tab.
        The id of the measuring station is read from the combobox.
        A new row is made in the tab with the data from this measuring
        station.
        """
        tablewidget = self.dockwidget_controlled_structures.tablewidget_measuring_point
        measure_point_id = (
            self.dockwidget_controlled_structures.combobox_input_measuring_point_view.currentText()
        )
        control_structure = self.connect_to_database()
        table_name = "v2_control_measure_map"
        attribute_name = "*"
        where = "id={}".format(measure_point_id)
        measure_point = control_structure.get_features_with_where_clause(
            table_name=table_name, attribute_name=attribute_name, where=where
        )[0]
        # Insert on top of the table
        row_position = 0
        tablewidget.insertRow(row_position)
        measuring_point_id = QTableWidgetItem(str(measure_point[0]))
        tablewidget.setItem(row_position, 0, measuring_point_id)
        measuring_point_table = QTableWidgetItem(str(measure_point[2]))
        tablewidget.setItem(row_position, 1, measuring_point_table)
        measuring_point_table_id = QTableWidgetItem(str(measure_point[3]))
        tablewidget.setItem(row_position, 2, measuring_point_table_id)

    def clear_measuring_point_table(self):
        row_count = (
            self.dockwidget_controlled_structures.tablewidget_measuring_point.rowCount()
        )
        for row in range(row_count):
            self.dockwidget_controlled_structures.tablewidget_measuring_point.removeRow(
                0
            )

    def create_new_rule(self):
        """
        Open a dialog for creating and saving a new rule in the database.
        A new id for this rule is created to show in the dialog.
        """
        control_structure = self.connect_to_database()
        db_key = (
            self.dockwidget_controlled_structures.combobox_input_model.currentText()
        )
        table_name = "v2_control_table"
        attribute_name = "MAX(id)"
        # Get last id of measure group or set to 0; set to +1
        try:
            max_id_table_control = int(
                control_structure.get_attributes(table_name, attribute_name)[0]
            )
        except ValueError:
            max_id_table_control = 0
        new_id_table_control = max_id_table_control + 1
        self.dialog_create_table_control = CreateTableControlDialogWidget(
            db_key=db_key,
            table_control_id=new_id_table_control,
            dockwidget_controlled_structures=self.dockwidget_controlled_structures,
        )
        self.dialog_create_table_control.exec_()  # block execution
        self.update_rule_ids(control_structure)

    def view_rule(self):
        """
        View a rule in a new tab in the Rule tab.
        A new tab is created with the rule id of the selected
        combobox, and populated with data of this rule.
        """
        rule_type = (
            self.dockwidget_controlled_structures.combobox_input_rule_type_view.currentText()
        )
        rule_id_name = "id"
        rule_id = (
            self.dockwidget_controlled_structures.combobox_input_rule_view.currentText()
        )
        if rule_id == "":
            return
        else:
            attribute_name = "*"
            table_name = "v2_control_table"
            where = "{id_name} = {id_value}".format(
                id_name=rule_id_name, id_value=rule_id
            )
            control_structure = self.connect_to_database()
            rule = control_structure.get_features_with_where_clause(
                table_name, attribute_name, where
            )[0]
            # Add a tab in the tabwidget of the 'Measuring group' tab in
            # the controlled structures dockwidget
            self.create_rule_tab(rule_id, rule)
            self.populate_rule_tab(rule_type, rule_id, rule)

    def create_rule_tab(self, rule_id, rule):
        """
        Create a tab in the Rule tab. The tab is added to the left.

        Args:
            (int) rule_id: The id of the rule.
            (list) rule: A list of tuples containing the attributes
                                  of the rule.
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        tab.setLayout(layout)

        label_field = QLabel(tab)
        label_field.setGeometry(10, 10, 300, 21)
        label_field.setText("Measure variable: {}".format(rule[4]))

        label_field = QLabel(tab)
        label_field.setGeometry(10, 40, 300, 21)
        operator = ""
        if rule[1] == ">":
            operator = "Bottom up"
        elif rule[1] == "<":
            operator = "Top down"
        label_field.setText("Operator: {}".format(operator))

        label_field = QLabel(tab)
        label_field.setGeometry(310, 10, 300, 21)
        structure_type = ""
        if rule[3] == "v2_culvert":
            structure_type = "culvert"
        elif rule[3] == "v2_pumpstation":
            structure_type = "pumpstation"
        elif rule[3] == "v2_orifice":
            structure_type = "orifice"
        elif rule[3] == "v2_weir":
            structure_type = "weir"
        label_field.setText("Structure type: {}".format(structure_type))

        label_field = QLabel(tab)
        label_field.setGeometry(310, 40, 300, 21)
        label_field.setText("Structure id: {}".format(rule[2]))

        label_field = QLabel(tab)
        label_field.setGeometry(310, 70, 741, 21)
        label_field.setText("Action type: {}".format(rule[5]))

        table_control_table = QTableWidget(tab)
        table_control_table.setGeometry(10, 100, 741, 181)
        table_control_table.insertColumn(0)
        table_control_table.setHorizontalHeaderItem(
            0, QTableWidgetItem("measuring_value")
        )
        table_control_table.insertColumn(1)
        table_control_table.setHorizontalHeaderItem(1, QTableWidgetItem("action_value"))
        table_control_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dockwidget_controlled_structures.table_control_view = table_control_table

        self.dockwidget_controlled_structures.tab_table_control_view.insertTab(
            0, tab, "Table control: {}".format(str(rule_id))
        )

    def populate_rule_tab(self, rule_type, rule_id, rule):
        """
        Populate a tab in the tabwidget of the 'Rule' tab with data of the
        selected rule.

        Args:
            (str) rule_type: The type of the rule.
            (int) rule_id: The id of the rule.
            (list) rule: A list of tuples. The tuples contain the
                                  different rules.
        """
        action_table = rule[0]
        action_pairs = action_table.split("#")
        # Check if there is an action_pair
        if ";" in action_pairs[0]:
            row = 0
            for action_pair in action_pairs:
                self.dockwidget_controlled_structures.table_control_view.insertRow(row)
                measure_value, action_value = action_pair.split(";")
                self.dockwidget_controlled_structures.table_control_view.setItem(
                    row, 0, QTableWidgetItem(measure_value)
                )
                self.dockwidget_controlled_structures.table_control_view.setItem(
                    row, 1, QTableWidgetItem(action_value)
                )
                row += 1

    def remove_rule_tab(self):
        self.dockwidget_controlled_structures.tab_table_control_view.removeTab(
            self.dockwidget_controlled_structures.tab_table_control_view.currentIndex()
        )

    def remove_all_rule_tabs(self):
        self.dockwidget_controlled_structures.tab_table_control_view.clear()

    def delete_rule_from_database(self):
        """
        Delete a rule from the database.
        Controls that contain these rules are deleted. If this results in an
        empty control group, this control group is also removed from the
        database and from the Control group tab.
        Tabs that contain these rules are removed from the Rule tab.
        """
        control_structure = self.connect_to_database()
        # Get id and type of rule
        rule_id = (
            self.dockwidget_controlled_structures.combobox_input_rule_delete.currentText()
        )
        rule_type = (
            self.dockwidget_controlled_structures.combobox_input_rule_type_delete.currentText()
        )
        # Remove the database entries of the the controls the rule is linked to
        # and delete them. Delete empty control groups
        id_name = "control_id"
        id_value = rule_id
        tabwidget = self.dockwidget_controlled_structures.tab_control_view
        control_structure.delete_controls_and_control_groups(
            id_name, id_value, tabwidget
        )
        # Remove these rules from v2_control
        table_name = "v2_control"
        where = " WHERE control_id = '{}'".format(str(rule_id))
        control_structure.delete_from_database(table_name=table_name, where=where)
        # Remove rule from database
        if rule_type == "table_control":
            table_name = "v2_control_table"
        where = " WHERE id = '{}'".format(str(rule_id))
        control_structure.delete_from_database(table_name=table_name, where=where)
        # Remove rule from tabs in dockwidget
        tabwidget = self.dockwidget_controlled_structures.tab_table_control_view
        tabs_to_remove = []
        tab_number = tabwidget.count()
        for tab in range(tab_number):
            if tabwidget.tabText(tab) == "Table control: {}".format(rule_id):
                tabs_to_remove += [tab]
        # Removing a tabs makes the tab go to the left, so delete the tabs in
        # reversed order (from right to left)
        [tabwidget.removeTab(tab) for tab in reversed(tabs_to_remove)]
        self.update_rule_ids(control_structure)
        self.update_control_ids(control_structure)

    def create_new_control_group(self):
        """
        Open a dialog for creating and saving a new control group in the
        database. A new id for this control group is created to show in the
        dialog.
        """
        control_structure = self.connect_to_database()
        db_key = (
            self.dockwidget_controlled_structures.combobox_input_model.currentText()
        )
        table_name = "v2_control_group"
        attribute_name = "MAX(id)"
        # Get last id of control group or set to 0; set to +1
        try:
            max_id_control_group = int(
                control_structure.get_attributes(table_name, attribute_name)[0]
            )
        except ValueError:
            max_id_control_group = 0
        new_id_control_group = max_id_control_group + 1
        self.dialog_create_control_group = CreateControlGroupDialogWidget(
            db_key=db_key,
            control_group_id=new_id_control_group,
            dockwidget_controlled_structures=self.dockwidget_controlled_structures,
        )
        self.dialog_create_control_group.exec_()  # block execution
        self.update_control_ids(control_structure)

    def view_control_group(self):
        """
        View a control group in a new tab in the Control group tab.
        A new tab is created with the control group id of the selected
        combobox, and populated with data of this control group.
        """
        control_group_id = (
            self.dockwidget_controlled_structures.combobox_input_control_view.currentText()
        )
        if control_group_id == "":
            return
        else:
            attribute_name = "*"
            table_name = "v2_control_group"
            where = "{id_name} = {id_value}".format(
                id_name="id", id_value=control_group_id
            )
            control_structure = self.connect_to_database()
            control_group = control_structure.get_features_with_where_clause(
                table_name, attribute_name, where
            )[0]
            # Create a new tab for the Control tab in the dockwidget
            self.create_control_group_tab(control_group_id, control_group)
            attribute_name = "*"
            table_name = "v2_control"
            where = "{id_name} = {id_value}".format(
                id_name="control_group_id", id_value=control_group_id
            )
            controls = control_structure.get_features_with_where_clause(
                table_name, attribute_name, where
            )
            self.populate_control_group_tab(control_group_id, controls)

    def create_control_group_tab(self, control_group_id, control_group):
        """
        Create a tab in the Control group tab. The tab is added to the left.

        Args:
            (int) control_group_id: The id of the control group.
            (list) control_group: A list of tuples containing the attributes
                                  of the control group.
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        tab.setLayout(layout)

        label_field = QLabel(tab)
        label_field.setGeometry(10, 10, 741, 21)
        label_field.setText("Name: {}".format(control_group[2]))

        label_field = QLabel(tab)
        label_field.setGeometry(10, 40, 741, 51)
        label_field.setText("Description: {}".format(control_group[0]))

        control_group_table = QTableWidget(tab)
        control_group_table.setGeometry(10, 100, 741, 181)
        control_group_table.insertColumn(0)
        control_group_table.setHorizontalHeaderItem(
            0, QTableWidgetItem("measuring_group_id")
        )
        control_group_table.insertColumn(1)
        control_group_table.setHorizontalHeaderItem(1, QTableWidgetItem("rule_type"))
        control_group_table.insertColumn(2)
        control_group_table.setHorizontalHeaderItem(2, QTableWidgetItem("rule_id"))
        control_group_table.insertColumn(3)
        control_group_table.setHorizontalHeaderItem(3, QTableWidgetItem("structure"))
        control_group_table.insertColumn(4)
        control_group_table.setHorizontalHeaderItem(4, QTableWidgetItem("structure_id"))
        control_group_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Add the tab to the tabwidget in the dockwidget
        self.dockwidget_controlled_structures.control_group_table = control_group_table
        self.dockwidget_controlled_structures.tab_control_view.insertTab(
            0, tab, "Control group: {}".format(str(control_group_id))
        )

    def populate_control_group_tab(self, control_group_id, controls):
        """
        Populate the new tab in the Control group tab with data of the
        selected control group.

        Args:
            (int) control_group_id: The id of the control group.
            (list) controls: A list of tuples. The tuples contain the
                                  different controls.
        """
        control_structure = self.connect_to_database()
        tablewidget = self.dockwidget_controlled_structures.control_group_table
        row = 0
        for control in controls:
            tablewidget.insertRow(row)
            tablewidget.setItem(row, 0, QTableWidgetItem(str(control[6])))
            tablewidget.setItem(row, 1, QTableWidgetItem(control[2]))
            tablewidget.setItem(row, 2, QTableWidgetItem(str(control[3])))
            # Get structure type and id
            attribute_name = "target_type"
            table_name = "v2_control_table"
            where = "{id_name} = {id_value}".format(id_name="id", id_value=control[3])
            structure_type = control_structure.get_features_with_where_clause(
                table_name, attribute_name, where
            )[0][0]
            structure = ""
            if structure_type == "v2_culvert":
                structure = "culvert"
            elif structure_type == "v2_orifice":
                structure = "orifice"
            elif structure_type == "v2_pumpstation":
                structure = "pumpstation"
            elif structure_type == "v2_weir":
                structure = "weir"
            tablewidget.setItem(row, 3, QTableWidgetItem(str(structure)))
            attribute_name = "target_id"
            table_name = "v2_control_table"
            where = "{id_name} = {id_value}".format(id_name="id", id_value=control[3])
            structure_id = control_structure.get_features_with_where_clause(
                table_name, attribute_name, where
            )[0]
            tablewidget.setItem(row, 4, QTableWidgetItem(str(structure_id[0])))
            row += 1

    def remove_control_tab(self):
        self.dockwidget_controlled_structures.tab_control_view.removeTab(
            self.dockwidget_controlled_structures.tab_control_view.currentIndex()
        )

    def remove_all_control_tabs(self):
        self.dockwidget_controlled_structures.tab_control_view.clear()

    def delete_control_group_from_database(self):
        """
        Delete a control group from the database. This also deletes the
        controls that are part of this control group.
        Tabs that contain this control group are removed from the Control
        group tab.
        """
        control_structure = self.connect_to_database()
        # Get id of control group
        control_group_id = (
            self.dockwidget_controlled_structures.combobox_input_control_delete.currentText()
        )
        # Remove control of control group from database
        table_name = "v2_control"
        where = " WHERE control_group_id = '{}'".format(str(control_group_id))
        control_structure.delete_from_database(table_name=table_name, where=where)
        # Remove control group from database
        table_name = "v2_control_group"
        where = " WHERE id = '{}'".format(str(control_group_id))
        control_structure.delete_from_database(table_name=table_name, where=where)
        # Remove control group from tabs in dockwidget
        tabwidget = self.dockwidget_controlled_structures.tab_control_view
        tabs_to_remove = []
        tab_number = tabwidget.count()
        for tab in range(tab_number):
            if tabwidget.tabText(tab) == "Control group: {}".format(control_group_id):
                tabs_to_remove += [tab]
        # Removing a tabs makes the tab go to the left, so delete the tabs in
        # reversed order (from right to left)
        [tabwidget.removeTab(tab) for tab in reversed(tabs_to_remove)]
        self.update_control_ids(control_structure)
