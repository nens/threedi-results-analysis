# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import logging

from PyQt4.QtCore import Qt


from ThreeDiToolbox.views.control_structures_dockwidget import ControlStructuresDockWidget  # noqa
from ThreeDiToolbox.commands.base.custom_command import CustomCommandBase
from ThreeDiToolbox.utils.threedi_database import get_databases
from ThreeDiToolbox.threedi_schema_edits.controlled_structures import \
    ControlledStructures

log = logging.getLogger(__name__)

ACTIVE_TAB = " (active tab)"
TABLE_CONTROL = 'table_control'
BOTTOM_UP = 'Bottom up'
RULE_OPERATOR_BOTTOM_UP = '>'
RULE_OPERATOR_TOP_DOWN = '<'
V2_WEIR_VIEW_TABLE = "v2_weir_view"
V2_WEIR_TABLE = 'v2_weir'
INITIAL_WATERLEVEL = "initial_waterlevel"
WATERLEVEL = 'waterlevel'
ACTION_TYPE_SET_CREST_LEVEL = 'set_crest_level'


class CustomCommand(CustomCommandBase):
    """
    command to that will load and start an edit session for the connected
    point layer and verify the data added to that layer
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.iface = kwargs.get('iface')
        self.ts_datasource = kwargs.get('ts_datasource')
        self.dockwidget_controlled_structures = None
        self.control_structure = None

        self.databases = get_databases()
        # Remove u'selected' spatialite and postgresdatabases
        # from self.databases to prevent confusion about which database
        # is meant by it
        if 'spatialite: ' in self.databases:
            self.databases.pop('spatialite: ', None)
        if 'postgres: None' in self.databases:
            self.databases.pop('postgres: None', None)

    def run(self):
        self.show_gui()
        self.dockwidget_controlled_structures.combobox_input_model\
            .activated.connect(self.update_dockwidget_ids)
        self.dockwidget_controlled_structures.pushbutton_input_save\
            .clicked.connect(self.save_control_structure)

    def show_gui(self):
        self.dockwidget_controlled_structures = ControlStructuresDockWidget()
        self.iface.addDockWidget(
            Qt.LeftDockWidgetArea, self.dockwidget_controlled_structures)
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
        # Get the model
        self.dockwidget_controlled_structures.\
            combobox_input_measuring_point_id.clear()
        self.dockwidget_controlled_structures.\
            combobox_input_structure_id.clear()
        db_key = self.dockwidget_controlled_structures.combobox_input_model\
            .currentText()  # name of database
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
            self.dockwidget_controlled_structures.\
                combobox_input_measuring_point_id.addItem(str(id_nr))
        # Get all id's of the structures
        control_structure.start_sqalchemy_engine(db_settings)
        with control_structure.engine.connect() as con:
            rs = con.execute(
                '''SELECT weir_id FROM v2_weir_view;'''
            )
            weir_ids = rs.fetchall()
        con.close()
        for weir_id in weir_ids:
            id_nr = weir_id[0]
            self.dockwidget_controlled_structures.\
                combobox_input_structure_id.addItem(str(id_nr))

    def save_control_structure(self):
        """
        Function to save the created control in the designated table.
        Currently only works for table control.
        """
        control_type = TABLE_CONTROL
        # Get the model
        db_key = self.dockwidget_controlled_structures\
            .combobox_input_model.currentText()
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
        control_structure = ControlledStructures(
            flavor=db_entry['db_type'])
        control_structure.start_sqalchemy_engine(db_settings)
        # Get the variables as input for the v2_control_table
        if control_type == TABLE_CONTROL:
            measure_value = self.dockwidget_controlled_structures\
                .tablewidget_input_rule_table_control.item(0, 0).text()
            action_value = self.dockwidget_controlled_structures\
                .tablewidget_input_rule_table_control.item(0, 1).text()
            action_table = '{0};{1}'.format(measure_value, action_value)
            if self.dockwidget_controlled_structures\
                    .combobox_input_rule_operator.currentText()\
                    == BOTTOM_UP:
                measure_operator = RULE_OPERATOR_BOTTOM_UP
            else:
                measure_operator = RULE_OPERATOR_TOP_DOWN
            target_id = self.dockwidget_controlled_structures\
                .combobox_input_structure_id.currentText()
            if self.dockwidget_controlled_structures\
                    .combobox_input_structure_table.currentText()\
                    == V2_WEIR_VIEW_TABLE:
                target_type = V2_WEIR_TABLE
                action_type = ACTION_TYPE_SET_CREST_LEVEL
            else:
                target_type = ""
                action_type = ''
            if self.dockwidget_controlled_structures\
                    .combobox_input_measuring_point_field.currentText()\
                    == INITIAL_WATERLEVEL:
                measure_variable = WATERLEVEL
            else:
                measure_variable = ""
            with control_structure.engine.connect() as con:
                rs = con.execute(
                    '''SELECT MAX(id) FROM v2_control_table;'''
                )
                max_id_control_table = rs.fetchone()[0]
                if not max_id_control_table:
                    max_id_control_table = 0
                new_id_control_table = max_id_control_table + 1
            con.close()
            # Insert the variables in the v2_control_table
            with control_structure.engine.connect() as con:
                rs = con.execute(
                    '''INSERT INTO v2_control_table (action_table, \
                    measure_operator, target_id, target_type, \
                    measure_variable, action_type, id) \
                    VALUES ('{0}', '{1}', {2}, '{3}', '{4}', '{5}', '{6}');'''
                    .format(
                        action_table, measure_operator, target_id, target_type,
                        measure_variable, action_type, new_id_control_table)
                )
            con.close()
