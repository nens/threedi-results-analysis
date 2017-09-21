import logging

from qgis.core import QgsDataSourceURI
from qgis.gui import QgsMessageBar
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.exc import OperationalError

from ThreeDiToolbox.utils.threedi_database import ThreediDatabase
from ThreeDiToolbox.utils.user_messages import messagebar_message

logger = logging.getLogger(__name__)

TABLE_CONTROL = 'table_control'
RULE_OPERATOR_BOTTOM_UP = '>'
RULE_OPERATOR_TOP_DOWN = '<'
V2_WEIR_VIEW_TABLE = "v2_weir_view"
V2_WEIR_TABLE = 'v2_weir'
MEASURE_VARIABLE_WATERLEVEL = 'waterlevel'
ACTION_TYPE_SET_CREST_LEVEL = 'set_crest_level'


class ControlledStructures(object):

    def __init__(self, flavor):
        self.flavor = flavor
        self._schema = None  # will passed to get_uri()

    def get_uri(self, **kwargs):
        """
        :returns an QgsDataSourceURI() instance

        kwargs :
            'host' --> network address (postgres) or
                file path location (spatialite)
            'port' --> port for the network address. Can
                be omitted for spatialite
            'user_name' --> database credential. Can
                be omitted for spatialite
            'password' --> database credential. Can
                be omitted for spatialite
            'schema' --> database schema name

         """

        self._uri = QgsDataSourceURI()
        host = kwargs['host']
        port = kwargs['port']
        database = kwargs['database']
        username = kwargs['username']
        password = kwargs['password']
        self._schema = kwargs['schema']
        if self.flavor == 'spatialite':
            self._uri.setDatabase(host)
        elif self.flavor == 'postgres':
            self._uri.setConnection(host, port, database, username, password)
        return self._uri

    def start_sqalchemy_engine(self, kwargs):
        """
        kwargs :
            'host' --> network address (postgres) or
                file path location (spatialite)
            'port' --> port for the network address. Can
                be omitted for spatialite
            'user_name' --> database credential. Can
                be omitted for spatialite
            'password' --> database credential. Can
                be omitted for spatialite
            'schema' --> database schema name
        """
        self.threedi_db = ThreediDatabase(kwargs, db_type=self.flavor)
        self.engine = self.threedi_db.engine

    def create_action_table(self, list_of_values):
        """
        Create an action table (string) of a list of
        measure and action values.

        Args:
            (list) list_of_values: A list of values, containing measuring
                                   values and action values.

        Returns:
            (str) action_table: A string representing the action table to
                                be saved.
        """
        action_table = '{0};{1}'.format(list_of_values[0], list_of_values[1])
        return action_table

    def get_target_type(self, table_name):
        """
        Get the target type.

        Args:
            (str) table_name: The table name.

        Returns:
            (str) target_type: The target type, used for saving the control.
        """
        if table_name == V2_WEIR_VIEW_TABLE:
            target_type = V2_WEIR_TABLE
        else:
            target_type = ""
        return target_type

    def get_action_type(self, table_name):
        """
        Get the action type.

        Args:
            (str) table_name: The table name.

        Returns:
            (str) action_type: The action type, used for saving the control.
        """
        if table_name == V2_WEIR_VIEW_TABLE:
            action_type = ACTION_TYPE_SET_CREST_LEVEL
        else:
            action_type = ""
        return action_type

    def save_table_control(self, table_control):
        """
        Function to save the table control in the v2_control_table.

        Args:
            (dict) table_control: This dict contains the values for
                                  saving the table control. It containts
                                  table_control["action_table"],
                                  table_control["measure_operator"],
                                  table_control["target_id"],
                                  table_control["target_type"],
                                  table_control["action_type"],
                                  table_control["measure_variable"].
        """
        action_table = table_control["action_table"]
        measure_operator = table_control["measure_operator"]
        target_id = table_control["target_id"]
        target_type = table_control["target_type"]
        action_type = table_control["action_type"]
        measure_variable = table_control["measure_variable"]
        try:
            with self.engine.connect() as con:
                # MAX(id) returns None if the sql statement yields nothing.
                # In this case, max_id_control_table is set to 0 to prevent
                # TypeErrors when adding 1 to create new_id_control_table.
                rs = con.execute(
                    '''SELECT MAX(id) FROM v2_control_table;'''
                )
                max_id_control_table = rs.fetchone()[0]
                if not max_id_control_table:
                    max_id_control_table = 0
                new_id_control_table = max_id_control_table + 1
        except (OperationalError, ProgrammingError) as e:
            if "unable to open database file" in str(e):
                msg = "Database not found."
            elif "no such table" in str(e):
                msg = "Table {} not found.".format("v2_control_table")
            else:
                msg = "".format(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)
            return
        # Insert the variables in the v2_control_table
        try:
            with self.engine.connect() as con:
                rs = con.execute(
                    '''INSERT INTO v2_control_table (action_table, \
                    measure_operator, target_id, target_type, \
                    measure_variable, action_type, id) \
                    VALUES ('{0}', '{1}', {2}, '{3}', '{4}', '{5}', '{6}');'''
                    .format(
                        action_table, measure_operator, target_id, target_type,
                        measure_variable, action_type, new_id_control_table)
                )
        except (OperationalError, ProgrammingError) as e:
            if "unable to open database file" in str(e):
                msg = "Database not found."
            elif "no such table" in str(e):
                msg = "Table {} not found.".format("v2_control_table")
            else:
                msg = "".format(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)
