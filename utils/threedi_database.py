import os
import copy

import ogr
from pyspatialite import dbapi2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .sqlalchemy_add_columns import create_and_upgrade
from ThreeDiToolbox.sql_models.model_schematisation import Base


class ThreediDatabase(object):

    def __init__(self, connection_settings, db_type='sqlite', echo=False):
        """

        :param connection_settings:
        db_type (str choice): database type. 'sqlite' and 'postgresql' are supported
        """
        self.settings = connection_settings
        self.db_type = db_type
        self.echo = echo

        self._engine = None
        self._combined_base = None
        self._base = None

    def create_and_check_fields(self):

        # engine = self.get_engine()
        create_and_upgrade(self.engine, self.get_metadata())
        # self.metadata(engine=engine, force_refresh=True)

    def create_db(self, overwrite=False):
        if self.db_type == 'sqlite':

            if overwrite and os.path.isfile(self.settings['db_file']):
                os.remove(self.settings['db_file'])

            drv = ogr.GetDriverByName('SQLite')
            db = drv.CreateDataSource(self.settings['db_file'],
                                      ["SPATIALITE=YES"])
            Base.metadata.create_all(self.engine)

            #todo: add settings to improve database creation speed for older versions of gdal

    @property
    def engine(self):
        return self.get_engine()

    def get_engine(self, get_seperate_engine=False):

        if self._engine is None or get_seperate_engine:
            if self.db_type == 'sqlite':
                engine = create_engine('sqlite:///{0}'.format(
                                                self.settings['db_path']),
                                             module=dbapi2,
                                             echo=self.echo)
                if get_seperate_engine:
                    return engine
                else:
                    self._engine = engine

            elif self.db_type == 'postgres':
                con = "postgresql://{username}:{password}@{host}:{port}/{database}".format(**self.settings)

                engine = create_engine(con,
                                             echo=self.echo)
                if get_seperate_engine:
                    return engine
                else:
                    self._engine = engine

        return self._engine

    def get_metadata(self, including_existing_tables=True, engine=None, force_refresh=False):

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
