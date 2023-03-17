from ..sql_models.statistics import Base
from osgeo import ogr
from threedi_results_analysis.utils.threedi_database import ThreediDatabase

import copy
import logging
import os


logger = logging.getLogger(__name__)


class StaticsticsDatabase(ThreediDatabase):
    """Wrapper around sql alchemy interface with functions to create, update
    databases and get connections.
    This class is equal to ThreediDatabase, except fix_views
    Two functions create_db and get_metadata added because of link to Base
    (code is beside link to different 'Base;  equal to ThreediDatabase



    """

    def create_db(self, overwrite=False):
        if self.db_type == "spatialite":

            if overwrite and os.path.isfile(self.settings["db_file"]):
                os.remove(self.settings["db_file"])

            drv = ogr.GetDriverByName("SQLite")
            drv.CreateDataSource(self.settings["db_file"], ["SPATIALITE=YES"])
            Base.metadata.create_all(self.engine)

            # todo: add settings to improve database creation speed for older
            # versions of gdal

    def get_metadata(self, including_existing_tables=True, engine=None):

        if including_existing_tables:
            metadata = copy.deepcopy(Base.metadata)
            if engine is None:
                engine = self.engine

            metadata.reflect(bind=engine, extend_existing=True)
            return metadata
        else:
            if self._base_metadata is None:
                self._base_metadata = copy.deepcopy(Base.metadata)
            return self._base_metadata
