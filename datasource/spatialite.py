from pyspatialite import dbapi2 as sqlite

from ..utils.user_messages import log


WATERLEVEL = ('s1', 'waterlevel','m MSL')
DISCHARGE = ('q', 'discharge', 'm3/s')
# TODO: unorm is deprecated, now simpy 'u'
VELOCITY = ('unorm', 'velocity', 'm/s')
VOLUME = ('vol', 'volume', 'm3')
DISCHARGE_PUMP = ('q_pump', 'discharge', 'm3/s')

VARIABLE_LABELS = {
    'v2_connection_nodes': (WATERLEVEL, ),
    'v2_pipe': (DISCHARGE, VELOCITY, ),
    'v2_channel': (DISCHARGE, VELOCITY, ),
    'v2_culvert': (DISCHARGE, VELOCITY, ),
    'v2_pumpstation': (DISCHARGE_PUMP, ),
    'v2_weir': (DISCHARGE, VELOCITY, ),
    'v2_orifice': (DISCHARGE, VELOCITY, ),
    'sewerage_manhole': (WATERLEVEL, VOLUME, ),
    'sewerage_pipe': (DISCHARGE, VELOCITY, ),
    'sewerage_weir': (DISCHARGE, VELOCITY, ),
    'sewerage_orifice': (DISCHARGE, VELOCITY, ),
    'sewerage_pumpstation': (DISCHARGE_PUMP, )
}


# todo: this is the right place for these 2 supportive functions?
def get_available_parameters(object_type):
    return VARIABLE_LABELS[object_type]


layer_information = [
    # layer name, object_type, q/h type
    ('v2_connection_nodes', 'connection_nodes', 'h'),
    ('v2_pipe_view', 'pipe', 'q'),
    ('v2_channel', 'channel', 'q'),
    ('v2_culvert', 'culvert', 'q'),
    ('v2_pumpstation', 'pumpstation', 'q'),
    ('v2_pumpstation_view', 'pumpstation', 'q'),
    ('v2_weir_view', 'weir', 'q'),
    ('v2_orifice_view', 'orifice', 'q'),
    ('sewerage_manhole', 'manhole', 'h'),
    ('sewerage_pipe_view', 'pipe', 'q'),
    ('sewerage_pumpstation', 'pumpstation', 'q'),
    ('sewerage_pumpstation_view', 'pumpstation', 'q'),
    ('sewerage_weir_view', 'weir', 'q'),
    ('sewerage_orifice_view', 'orifice', 'q')
]

# Old names
# TODO: remove them
# layer_information = [
#     #layer name, object_type, q/h type
#     ('v2_connection_nodes', 'v2_connection_nodes', 'h'),
#     ('v2_pipe_view', 'v2_pipe', 'q'),
#     ('v2_channel', 'v2_channel', 'q'),
#     ('v2_culvert', 'v2_culvert', 'q'),
#     ('v2_pumpstation', 'v2_pumpstation', 'q'),
#     ('v2_pumpstation_view', 'v2_pumpstation', 'q'),
#     ('v2_weir_view', 'v2_weir', 'q'),
#     ('v2_orifice_view', 'v2_orifice', 'q'),
#     ('sewerage_manhole', 'sewerage_manhole', 'h'),
#     ('sewerage_pipe_view', 'sewerage_pipe', 'q'),
#     ('sewerage_pumpstation', 'sewerage_pumpstation', 'q'),
#     ('sewerage_pumpstation_view', 'sewerage_pumpstation', 'q'),
#     ('sewerage_weir_view', 'sewerage_weir', 'q'),
#     ('sewerage_orifice_view', 'sewerage_orifice', 'q')
# ]

# TODO: unorm is deprecated, now simpy 'u'
parameter_config = {
    'q': [{'name': 'Debiet', 'unit': 'm3/s', 'parameters': ['q', 'q_pump']},
          {'name': 'Snelheid', 'unit': 'm/s', 'parameters': ['unorm', 'u']}],
    'h': [{'name': 'Waterstand', 'unit': 'mNAP', 'parameters': ['s1']},
          {'name': 'Volume', 'unit': 'm3', 'parameters': ['vol']}]
}

layer_object_type_mapping = dict([(a[0], a[1]) for a in layer_information])
layer_qh_type_mapping = dict([(a[0], a[2]) for a in layer_information])


def get_object_type(current_layer_name):

    if current_layer_name in layer_object_type_mapping.keys():
        return layer_object_type_mapping[current_layer_name]
    else:
        msg = "Unsupported layer: %s." % current_layer_name
        log(msg, level='WARNING')
        return None



def _get_spatialite_path(self):
    """Return the full path of the spatialite."""
    provider = self.layer.dataProvider()
    if not provider.name() == 'spatialite':
        return
    # uri is something like
    # ---------------------
    # u'dbname=\'/d/dev/models/sewerage/purmerend/purmerend_result.sqlite\'
    # table="sewerage_manhole" (the_geom) sql='
    # ---------------------
    uri = provider.dataSourceUri()
    dbname = uri.split("'")[1]
    return dbname


class TdiSpatialite(object):

    def __init__(self, data_source_uri):
        """
        :param data_source_uri: string with path of spatialite
        :return:
        """
        self.data_source_uri = data_source_uri

    @property
    def metadata(self):
        """
        metadata of datasource
        :return: dictionary with metadata
        """
        return {
            '3di_script_version': self._get_3di_script_version()
        }

    def get_db_cursor(self, raise_exception_on_failure=False):
        """
        Return a cursor for the spatialite.
        :param raise_exception_on_failure: bool, raise exeption or fail silently
        :return: cursor of spatialite database
        """
        dbname = self.data_source_uri
        log(dbname)
        conn = sqlite.connect(dbname)
        cursor = conn.cursor()
        if not cursor and raise_exception_on_failure:
            raise "Error connecting to database."
        return cursor

    def _get_3di_script_version(self):
        """Get which version of process_sewerage_result the spatialite
        database was made with. Note: because a PRAGMA is used to save the
        version it must be an integer."""
        cursor = self.get_db_cursor()
        query = """PRAGMA user_version;"""
        res = cursor.execute(query)
        row = res.fetchone()
        if row:
            return row[0]
        else:
            return -1

    def get_parameters(self, object_type=None):
        """
        list of available parameter identifiers for all objects or specific objects
        :param object_type: single or list of object_types ['sewer_manhole', etc.]
        :return: list of strings (parameter identifiers)
        """
        query = "SELECT DISTINCT variable FROM result_type"

        if hasattr(object_type, '__iter__'):
            query += " WHERE object_type in (%(object_type)s)"%{
                    'object_type': ','.join(["'%s'"%ot for ot in object_type])
            }
        elif object_type is not None:
            query += " WHERE object_type = '%(object_type)s'"%{
                    'object_type': object_type
            }

        log("Executing query: %s" % query)
        cursor = self.get_db_cursor( raise_exception_on_failure=True)
        res = cursor.execute(query)
        rows = res.fetchall()
        if rows:
            return [row[0] for row in rows]
        else:
            return []

    def get_object_types(self, parameter=None):
        """
        List of available object types for all parameters or selection
        :param parameter: single or list of parameter identifiers ['s1, 'q', etc.]
        :return: list of object_types
        """

        query = "SELECT DISTINCT object_type FROM result_type"

        if hasattr(parameter, '__iter__'):
            query += " WHERE variable in (%(parameter)s)"%{
                    'parameter': ','.join(["'%s'"%p for p in parameter])
            }
        elif parameter is not None:
            query += " WHERE variable = '%(parameter)s'"%{
                    'parameter': parameter
            }

        log("Executing query: %s" % query)
        cursor = self.get_db_cursor( raise_exception_on_failure=True)
        res = cursor.execute(query)
        rows = res.fetchall()
        if rows:
            return [row[0] for row in rows]
        else:
            return []

    def get_objects(self, object_type):

        query = "SELECT * from %(table)s; "%{'table': object_type}
        log("Executing query: %s" % query)
        cursor = self.get_db_cursor( raise_exception_on_failure=True)
        res = cursor.execute(query)
        rows = res.fetchall()
        if rows:
            return rows
        else:
            return []

    def get_object_count(self, object_type):
        """
        get number of objects of object_type
        :param object_type: object identifier string
        :return: number of objects
        """
        query = "SELECT COUNT(*) FROM %(table)s;" % {'table': object_type}
        log("Executing query: %s" % query)
        cursor = self.get_db_cursor( raise_exception_on_failure=True)
        res = cursor.execute(query)
        row = res.fetchone()
        if row:
            return row[0]
        else:
            return 0

    def get_object(self, object_type, object_id):
        raise NotImplemented
        pass

    def get_timestamps(self, object_type, parameters):

        query = """SELECT DISTINCT v.time FROM result_type t, result_value v
            WHERE v.result_type_id = t.id
            AND t.object_type='%(object_type)s'
            AND t.variable in ['%(variable)s']
            ORDER BY v.time;""" % {'object_type': object_type,
                                   'variable': ','.join(["'%s'"%p for p in parameters])}
        log("Executing query: %s" % query)
        cursor = self.get_db_cursor()
        res = cursor.execute(query)
        rows = res.fetchall()
        if rows:
            return rows
        else:
            []


    def get_timestamp_count(self, object_type, parameters):

        query = """SELECT DISTINCT count(*) FROM result_type t, result_value v
            WHERE v.result_type_id = t.id
            AND t.object_type='%(object_type)s'
            AND t.variable in [%(variable)s]
            ORDER BY v.time;""" % {'object_type': object_type,
                                   'variable': ','.join(["'%s'"%p for p in parameters])}
        log("Executing query: %s" % query)
        cursor = self.get_db_cursor()
        res = cursor.execute(query)
        rows = res.fetchone()
        if rows:
            return rows[0]
        else:
            return 0



    def get_timeseries(self, object_type, object_id, parameters):
        """Get a list of time series from spatialite.

        Args:
            object_type: e.g. 'v2_weir'
            object_id: spatialite id?
            parameters: a list of params, e.g.: ['q', 'q_pump']

        Returns: a list of 2-tuples (time, value)
        """

        object_type = get_object_type(object_type)
        query = """SELECT t.id FROM result_type t
            WHERE t.object_type='%(object_type)s'
            AND t.object_id='%(object_id)s'
            AND t.variable in (%(variable)s);""" % {'object_type': object_type,
                                    'object_id': object_id,
                                    'variable': ','.join(["'%s'"%p for p in parameters])}
        log("Executing query: %s" % query)
        cursor = self.get_db_cursor()
        res = cursor.execute(query)
        rows = res.fetchall()
        if not rows:
            return []

        result_id = rows[0][0]

        query = """SELECT v.time, v.value FROM result_value v
            WHERE v.result_type_id = %(result_id)s
            ORDER BY v.time;""" % {'result_id': result_id}
        log("Executing query: %s" % query)
        cursor = self.get_db_cursor()
        res = cursor.execute(query)
        rows = res.fetchall()
        if rows:
            return rows
        else:
            # rows is something like:
            # [(0.0, 0.0), (66.875, 0.0), (120.625, 0.0), ...]
            msg = ("No data found for object_type %(object_type)s "
                   "with object_id: %(object_id)s and variable: %(variable)s."
                   "Query: %(query)s" % {'object_type': object_type,
                                  'object_id': object_id,
                                  'variable': ','.join(["'%s'"%p for p in parameters]),
                                  'query': query,
                                 })
            log(msg, level='WARNING')
            return []
