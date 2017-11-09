import logging

from qgis.core import QgsDataSourceURI
from qgis.gui import QgsMessageBar
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.exc import OperationalError

from ThreeDiToolbox.utils.threedi_database import ThreediDatabase
from ThreeDiToolbox.utils.user_messages import messagebar_message

logger = logging.getLogger(__name__)

RULE_OPERATOR_BOTTOM_UP = '>'
RULE_OPERATOR_TOP_DOWN = '<'
MEASURE_VARIABLE_WATERLEVEL = 'waterlevel'


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
        action_table = ""
        row_nr = 0
        for row in list_of_values:
            if row_nr > 0:
                action_table += "#"
            action_table += "{};{}".format(row[0], row[1])
            row_nr += 1
        return action_table

    def get_attributes(self, table_name, attribute_name, all_features=False):
        """
        Get all values of an attribute from a table.


        Args:
            (str) table_name: The table name of a spatialite or postgres
                              database.
            (str) attribute_name: The name of the attribute of a spatialite or
                                  postgres database.

        Returns:
            (list) list_of_attributes: A list of all the attribute values
                                       of the table.
                                       The attribute values are strings.
        """
        list_of_attributes = []
        try:
            with self.engine.connect() as con:
                rs = con.execute(
                    '''SELECT {attribute} FROM {table};'''.format(
                        attribute=attribute_name, table=table_name)
                )
                attributes = rs.fetchall()
                if all_features is False:
                    list_of_attributes = [str(attribute_value[0]) for
                                          attribute_value in attributes]
                else:
                    list_of_attributes += attributes
        except OperationalError as e:
            msg = str(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)
        except ProgrammingError as e:
            msg = str(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)
        except Exception as e:
            msg = "An unknown exception occured: {}".format(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)
        return list_of_attributes

    def get_features_with_where_clause(
            self, table_name, attribute_name, where):
        """
        Get all values of an attribute from a table.


        Args:
            (str) table_name: The table name of a spatialite or postgres
                              database.
            (str) attribute_name: The name of the attribute of a spatialite or
                                  postgres database.
            (str) where: The where clause for the sql statement.

        Returns:
            (list) list_of_features: A list of all the features
                                       of the table.
                                       The features are tuples.
        """
        list_of_features = []
        try:
            with self.engine.connect() as con:
                rs = con.execute(
                    '''SELECT {attribute} FROM {table} WHERE {where};'''.format(
                        attribute=attribute_name, table=table_name,
                        where=where)
                )
                features = rs.fetchall()
                list_of_features = [feature for feature in features]
        except OperationalError as e:
            msg = str(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)
        except ProgrammingError as e:
            msg = str(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)
        except Exception as e:
            msg = "An unknown exception occured: {}".format(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)
        return list_of_features

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
        # Get new id
        table_name = "v2_control_table"
        # MAX(id) returns None if the sql statement yields nothing.
        # In this case, max_id_control_table is set to 0 to prevent
        # TypeErrors when adding 1 to create new_id_control_table.
        attribute_name = "MAX(id)"
        try:
            max_id_control_table = int(self.get_attributes(
                table_name, attribute_name)[0])
        except ValueError:
            max_id_control_table = 0
        new_id_control_table = max_id_control_table + 1
        # Insert the variables in the v2_control_table
        table_control["id"] = new_id_control_table
        self.insert_into_table(table_name, table_control)

    def insert_into_table(self, table_name, attributes):
        """
        Function to insert data in a table (table_name).
        The list of values is inserted in the list of attributes.


        Args
            (str) table_name: The table name of a spatialite or postgres
                              database
            (dict) attributes: A dictionary of attributes to insert into
                               the table.
        """
        attribute_names = ""
        attribute_values = ""
        for key, value in attributes.iteritems():
            if attribute_names != "":
                attribute_names += ", '{}'".format(str(key))
            else:
                attribute_names += "'{}'".format(str(key))
            if attribute_values != "":
                attribute_values += ", '{}'".format(str(value))
            else:
                attribute_values += "'{}'".format(str(value))
        try:
            with self.engine.connect() as con:
                con.execute(
                    '''INSERT INTO {table} ({attributes}) VALUES ({values});'''
                    .format(table=table_name, attributes=attribute_names,
                            values=attribute_values)
                )
        except OperationalError as e:
            msg = str(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)
        except ProgrammingError as e:
            msg = str(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)
        except Exception as e:
            msg = "An unknown exception occured: {}".format(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)

    def delete_from_database(self, table_name, where=""):
        """
        Function to delete data from a table (table_name).

        Args
            (str) table_name: The table name of a spatialite or postgres
                              database
            (str) where: A where clause for the delete statement.
        """
        try:
            with self.engine.connect() as con:
                con.execute(
                    '''DELETE FROM {table}{where};'''.format(
                        table=table_name, where=where)
                )
        except OperationalError as e:
            msg = str(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)
        except ProgrammingError as e:
            msg = str(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)
        except Exception as e:
            msg = "An unknown exception occured: {}".format(e)
            messagebar_message(
                "Error", msg, level=QgsMessageBar.CRITICAL, duration=5)

    def delete_controls_and_control_groups(
            self, id_name, id_value, tabwidget):
        """
        Remove the database entries of the controls and delete them.
        Delete empty control groups

        Args:
            (str) id_name: The attribute name to find the corresponding
                           control with. This could for example be
                           "measure_group_id".
            (int) id_value: The value of the id to find the corresponding
                            control group with.
            (QTabWidget) tabwidget: The tabwidget with control group tabs.
                                    If an empty control group is created by
                                    deleting controls, the control group is
                                    also removed from the tabwidget
        """
        try:
            # Get the control id(s) from v2_control
            table_name = "v2_control"
            attribute_name = "id"
            where = "{id_name} = {id_value}".format(
                id_name=id_name, id_value=id_value)
            control_ids = self.get_features_with_where_clause(
                table_name=table_name, attribute_name=attribute_name,
                where=where)
            for control in control_ids:
                control_id = control[0]
                # Get the control group id from v2_control
                table_name = "v2_control"
                attribute_name = "control_group_id"
                where = "id = '{}'".format(str(control_id))
                control_group_ids = self.get_features_with_where_clause(
                    table_name=table_name, attribute_name=attribute_name,
                    where=where)
                for control_group in control_group_ids:
                    control_group_id = control_group[0]
                    # Remove control from v2_control
                    table_name = "v2_control"
                    where = " WHERE id = '{}'".format(
                        str(control_id))
                    self.delete_from_database(
                        table_name=table_name, where=where)
                    # Check whether there are still controls linked to this
                    # control group. If not, delete these empty control groups.
                    self.delete_empty_control_groups(
                        control_group_id, tabwidget)
        except Exception:
            # No linked controls
            pass

    def delete_empty_control_groups(self, control_group_id, tabwidget):
        """
        Delete empty control groups that are created by removing controls.

        Args:
            (int) control_group_id: The value of the control group id.
            (QTabWidget) tabwidget: The tabwidget with control group tabs.
                                    If an empty control group is created by
                                    deleting controls, the control group is
                                    also removed from the tabwidget
        """
        try:
            table_name = "v2_control"
            attribute_name = "COUNT(*)"
            where = "control_group_id = '{}'".format(str(control_group_id))
            count_control_group_ids = self.get_features_with_where_clause(
                table_name=table_name, attribute_name=attribute_name,
                where=where)[0][0]
            if count_control_group_ids == 0:
                # Remove these control groups from v2_control_group
                table_name = "v2_control_group"
                attribute_name = "id"
                where = " WHERE {attribute} = {value}".format(
                    attribute=attribute_name, value=control_group_id)
                self.delete_from_database(table_name=table_name, where=where)
                # Also remove these control groups in
                # tab Control groups
                tabs_to_remove = []
                tab_number = tabwidget.count()
                for tab in range(tab_number):
                    if tabwidget.tabText(tab) == "Control group: {}".format(
                            control_group_id):
                        tabs_to_remove += [tab]
                        # Removing a tabs makes the tab go to the left, so
                        # delete the tabs in reversed order
                        # (from right to left).
                [tabwidget.removeTab(tab)
                    for tab in reversed(tabs_to_remove)]
        except Exception:
            # No empty control groups
            pass
