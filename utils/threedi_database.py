import os
import copy

import ogr
import collections
from pyspatialite import dbapi2
from PyQt4.QtCore import QSettings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from .sqlalchemy_add_columns import create_and_upgrade

from ThreeDiToolbox.sql_models.model_schematisation import Base


class ThreediDatabase(object):

    def __init__(self, connection_settings, db_type='spatialite', echo=False):
        """

        :param connection_settings:
        db_type (str choice): database type. 'sqlite' and 'postgresql' are
                              supported
        """
        self.settings = connection_settings
        # make sure within the ThreediDatabase object we always use 'sqlite'
        # as the db_type identifier
        self.db_type = db_type
        self.echo = echo

        self._engine = None
        self._combined_base = None
        self._base = None
        self._base_metadata = None

    def create_and_check_fields(self):

        # engine = self.get_engine()
        create_and_upgrade(self.engine, self.get_metadata())
        # self.metadata(engine=engine, force_refresh=True)

    def create_db(self, overwrite=False):
        if self.db_type == 'spatialite':

            if overwrite and os.path.isfile(self.settings['db_file']):
                os.remove(self.settings['db_file'])

            drv = ogr.GetDriverByName('SQLite')
            db = drv.CreateDataSource(self.settings['db_file'],
                                      ["SPATIALITE=YES"])
            Base.metadata.create_all(self.engine)

            # todo: add settings to improve database creation speed for older
            # versions of gdal

    @property
    def engine(self):
        return self.get_engine()

    def get_engine(self, get_seperate_engine=False):

        if self._engine is None or get_seperate_engine:
            if self.db_type == 'spatialite':
                engine = create_engine('sqlite:///{0}'.format(
                    self.settings['db_path']),
                    module=dbapi2,
                    echo=self.echo)
                if get_seperate_engine:
                    return engine
                else:
                    self._engine = engine

            elif self.db_type == 'postgres':
                con = "postgresql://{username}:{password}@{host}:" \
                      "{port}/{database}".format(**self.settings)

                engine = create_engine(con,
                                       echo=self.echo)
                if get_seperate_engine:
                    return engine
                else:
                    self._engine = engine

        return self._engine

    def get_metadata(self, including_existing_tables=True, engine=None):

        if including_existing_tables:
            metadata = copy.deepcopy(Base.metadata)
            if engine is None:
                engine = self.engine

            metadata.bind = engine
            metadata.reflect(extend_existing=True)
            return metadata
        else:
            if self._base_metadata is None:
                self._base_metadata = copy.deepcopy(Base.metadata)
            return self._base_metadata

    def get_session(self):
        return sessionmaker(bind=self.engine)()

    def fix_views(self):
        """fixes views in spatialite by disabeling indexes for views

        """
        if self.db_type == 'spatialite':
            session = self.get_session()

            session.execute(
                """SELECT DisableSpatialIndex('v2_connection_nodes',
                                              'the_geom_linestring');"""
            )

            session.execute(
                """SELECT RecoverSpatialIndex('v2_impervious_surface',
                                              'the_geom');""")

            session.commit()

    def delete_from(self, table_name):
        """
        """
        del_statement = """DELETE FROM {}""".format(table_name)

        # runs a transaction
        with self.engine.begin() as connection:
            connection.execute(text(del_statement))

    def table_is_empty(self, table_name):
        """
        check if the given table is empty

        :returns False if the table contains a least one entry
        """
        is_empty = False
        select_statement = """SELECT 0 FROM {table_name} LIMIT 1;""".format(
            table_name=table_name)
        with self.engine.begin() as connection:
            res = connection.execute(text(select_statement))
            result = res.fetchone()
            if result:
                is_empty = result[0]
            return is_empty

    def has_valid_spatial_index(self, table_name, geom_column):
        """
        validate the spatial index for the given table with the given
        geometry column
        """
        # runs a transaction

        if self.db_type == 'spatialite':
            select_statement = """
               SELECT CheckSpatialIndex('{table_name}', '{geom_column}');
            """.format(table_name=table_name, geom_column=geom_column)
            with self.engine.begin() as connection:
                result = connection.execute(text(select_statement))
                return bool(result.fetchone()[0])

    def recover_spatial_index(self, table_name, geom_column):
        """
        recover the spatial index for the given table with the given
        geometry column
        :returns True when recovery was successful, False otherwise
        """
        if self.db_type == 'spatialite':
            select_statement = """
               SELECT RecoverSpatialIndex('{table_name}', '{geom_column}');
            """.format(table_name=table_name, geom_column=geom_column)
            with self.engine.begin() as connection:
                result = connection.execute(text(select_statement))
                return bool(result.fetchone()[0])


def get_databases():
    d = {}
    qs = QSettings()

    # spatialite
    qs.beginGroup("SpatiaLite/connections")

    for db_entry in qs.allKeys():
        db_name, _ = os.path.split(db_entry)

        settings = {
            'key': os.path.basename(db_entry),
            'db_name': db_name,
            'combo_key': 'spatialite: {0}'.format(
                os.path.splitext(db_name)[0]),
            'db_type': 'spatialite',
            'db_settings': {
                'db_path': qs.value(db_entry)
            }
        }

        d[settings['combo_key']] = settings
    qs.endGroup()

    qs.beginGroup("PostgreSQL/connections")
    for db_entry in qs.allKeys():
        prefix, attribute = os.path.split(db_entry)
        db_name = qs.value(prefix + '/database')
        settings = {
            'key': db_entry,
            'db_name': db_name,
            'combo_key': 'postgres: {0}'.format(db_name),
            'db_type': 'postgres',
            'db_settings': {
                'host': qs.value(prefix + '/host'),
                'port': qs.value(prefix + '/port'),
                'database': qs.value(prefix + '/database'),
                'username': qs.value(prefix + '/username'),
                'password': qs.value(prefix + '/password'),
            }
        }

        if qs.value(prefix + '/saveUsername') == u'true':
            settings['saveUsername'] = True
            settings['db_settings']['username'] = qs.value(
                prefix + '/username')
        else:
            settings['saveUsername'] = False

        if qs.value(prefix + '/savePassword') == u'true':
            settings['savePassword'] = True
            settings['db_settings']['password'] = qs.value(
                prefix + '/password')
        else:
            settings['savePassword'] = False

        d[settings['combo_key']] = settings
    qs.endGroup()
    available_dbs = collections.OrderedDict(sorted(d.items()))

    return available_dbs


def get_database_properties(db_key):
    """
    Get the properties of a specific database.

    Args: (str) db_key: The database key, a string where the
                        database type (spatialite/ postgres) and
                        name of the database are combined.

    Returns: (dict) db: A dictionary containing the database properties,
                        such as db_key, db_entry and db_settings.
    """
    db = {}
    db["db_key"] = db_key
    db["db_entry"] = get_databases()[db_key]

    _db_settings = db["db_entry"]['db_settings']

    if db["db_entry"]['db_type'] == 'spatialite':
        host = _db_settings['db_path']
        db["db_settings"] = {
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
        db["db_settings"] = _db_settings
        db["db_settings"]['schema'] = 'public'
    return db
