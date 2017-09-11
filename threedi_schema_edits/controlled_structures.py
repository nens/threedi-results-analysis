from qgis.core import QgsDataSourceURI

from ThreeDiToolbox.utils.threedi_database import ThreediDatabase

import logging

logger = logging.getLogger(__name__)


class ControlledStructures(object):
    _QUERY_TYPE_DICT = {
        'postgres': 'QPSQL',
        'spatialite': 'QSQLITE',
        'spatialite2': 'QSQLITE2'
    }

    def __init__(self, flavor, lyr_name=""):
        self.flavor = flavor
        self.lyr_name = lyr_name
        if not self.lyr_name:
            self.lyr_name = "temporary_lyr"
        self.data_provider = None
        self.mem_layer = None
        self._schema = None  # will passed to get_uri()
        self.query = None
        self.network_dict = {}
        self._calc_pnt_features = []
        self._connected_pnt_features = []
        self._trans = None

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
