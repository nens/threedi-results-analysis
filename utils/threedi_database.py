from .sqlalchemy_add_columns import create_and_upgrade
from osgeo import ogr
from qgis.PyQt.QtCore import QSettings
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from ThreeDiToolbox.utils.user_messages import StatusProgressBar

import collections
import copy
import logging
import os


Base = declarative_base()

logger = logging.getLogger(__name__)


def load_spatialite(con, connection_record):
    """Load spatialite extension as described in
    https://geoalchemy-2.readthedocs.io/en/latest/spatialite_tutorial.html"""
    import sqlite3

    con.enable_load_extension(True)
    cur = con.cursor()
    libs = [
        # SpatiaLite >= 4.2 and Sqlite >= 3.7.17, should work on all platforms
        ("mod_spatialite", "sqlite3_modspatialite_init"),
        # SpatiaLite >= 4.2 and Sqlite < 3.7.17 (Travis)
        ("mod_spatialite.so", "sqlite3_modspatialite_init"),
        # SpatiaLite < 4.2 (linux)
        ("libspatialite.so", "sqlite3_extension_init"),
    ]
    found = False
    for lib, entry_point in libs:
        try:
            cur.execute("select load_extension('{}', '{}')".format(lib, entry_point))
        except sqlite3.OperationalError:
            logger.exception(
                "Loading extension %s from %s failed, trying the next", entry_point, lib
            )
            continue
        else:
            logger.info("Successfully loaded extension %s from %s.", entry_point, lib)
            found = True
            break
    if not found:
        raise RuntimeError("Cannot find any suitable spatialite module")
    cur.close()
    con.enable_load_extension(False)


class ThreediDatabase(object):
    def __init__(self, connection_settings, db_type="spatialite", echo=False):
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
        self._combined_base = None  # TODO: unused?
        self._base = None  # TODO: unused?
        self._base_metadata = None

    def create_and_check_fields(self):

        # engine = self.get_engine()
        create_and_upgrade(self.engine, self.get_metadata())
        # self.metadata(engine=engine, force_refresh=True)

    def create_db(self, overwrite=False):
        if self.db_type == "spatialite":

            if overwrite and os.path.isfile(self.settings["db_file"]):
                os.remove(self.settings["db_file"])

            drv = ogr.GetDriverByName("SQLite")
            drv.CreateDataSource(self.settings["db_file"], ["SPATIALITE=YES"])
            Base.metadata.bind = self.engine
            Base.metadata.create_all(self.engine)

            # todo: add settings to improve database creation speed for older
            # versions of gdal

    @property
    def engine(self):
        # TODO: can this become a cached_property? Depends on the following method.
        return self.get_engine()

    def get_engine(self, get_seperate_engine=False):

        if self._engine is None or get_seperate_engine:
            if self.db_type == "spatialite":
                engine = create_engine(
                    "sqlite:///{0}".format(self.settings["db_path"]), echo=self.echo
                )
                listen(engine, "connect", load_spatialite)
                if get_seperate_engine:
                    return engine
                else:
                    self._engine = engine

            elif self.db_type == "postgres":
                con = (
                    "postgresql://{username}:{password}@{host}:"
                    "{port}/{database}".format(**self.settings)
                )

                engine = create_engine(con, echo=self.echo)
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

    def create_views(self):
        conn = self.get_session()

        conn.execute(
            """
        CREATE VIEW IF NOT EXISTS v2_manhole_view 
        AS SELECT manh.rowid AS ROWID, node.id AS node_id, manh.bottom_level
        AS manh_bottom_level, manh.surface_level AS manh_surface_level,
        manh.display_name AS manh_display_name, manh.shape AS manh_shape,
        manh.width AS manh_width, manh.length AS manh_length, 
        manh.manhole_indicator AS manh_manhole_indicator, manh.calculation_type
        AS manh_calculation_type, manh.drain_level AS manh_drain_level,
        manh.zoom_category AS manh_zoom_category, node.initial_waterlevel AS
        node_initial_waterlevel, manh.id AS manh_id, manh.connection_node_id  AS 
        manh_connection_node_id, node.storage_area AS node_storage_area,
        manh.code AS manh_code, node.code AS node_code, node.the_geom,
        node.the_geom_linestring AS node_the_geom_linestring, 
        manh.sediment_level AS manh_sediment_level 
        FROM v2_manhole manh, v2_connection_nodes node
        WHERE manh.connection_node_id = node.id;
        """
        )

        conn.execute(
            """
        DELETE FROM views_geometry_columns
        WHERE view_name = 'v2_manhole_view';"""
        )

        conn.execute(
            """
        INSERT INTO views_geometry_columns (view_name, view_geometry,
        view_rowid, f_table_name, f_geometry_column)
        VALUES('v2_manhole_view', 'the_geom', 'ROWID',
        'v2_connection_nodes', 'the_geom');"""
        )

        conn.execute(
            """
        CREATE VIEW IF NOT EXISTS v2_pumpstation_point_view
        AS SELECT a.ROWID AS ROWID, a.id AS pump_id, a.display_name, a.code,
        a.classification, a.sewerage, a.start_level, a.lower_stop_level,
        a.upper_stop_level, a.capacity, a.zoom_category,
        a.connection_node_start_id, a.connection_node_end_id, a.type,
        b.id AS connection_node_id, b.storage_area, b.the_geom
        FROM v2_pumpstation a
        JOIN v2_connection_nodes b
        ON a.connection_node_start_id = b.id;"""
        )

        conn.execute(
            """
        DELETE FROM views_geometry_columns
        WHERE view_name = 'v2_pumpstation_point_view';"""
        )

        conn.execute(
            """
        INSERT INTO views_geometry_columns (view_name, view_geometry,
        view_rowid, f_table_name, f_geometry_column)
        VALUES('v2_pumpstation_point_view', 'the_geom',
        'connection_node_start_id', 'v2_connection_nodes', 'the_geom');"""
        )

        conn.execute(
            """
        CREATE VIEW IF NOT EXISTS v2_1d_lateral_view
        AS SELECT a.ROWID AS ROWID, a.id AS id,
        a.connection_node_id AS connection_node_id,
        a.timeseries AS timeseries, b.the_geom
        FROM v2_1d_lateral a
        JOIN v2_connection_nodes b ON a.connection_node_id = b.id;"""
        )

        conn.execute(
            """
        DELETE FROM views_geometry_columns
        WHERE view_name = 'v2_1d_lateral_view';"""
        )

        conn.execute(
            """
        INSERT INTO views_geometry_columns (view_name, view_geometry,
        view_rowid, f_table_name, f_geometry_column)
        VALUES('v2_1d_lateral_view', 'the_geom', 'connection_node_id',
        'v2_connection_nodes', 'the_geom');"""
        )

        conn.execute(
            """
        CREATE VIEW IF NOT EXISTS v2_1d_boundary_conditions_view
        AS SELECT a.ROWID AS ROWID, a.id AS id,
        a.connection_node_id AS connection_node_id,
        a.boundary_type AS boundary_type, a.timeseries AS timeseries,
        b.the_geom
        FROM v2_1d_boundary_conditions a
        JOIN v2_connection_nodes b ON a.connection_node_id = b.id;"""
        )

        conn.execute(
            """
        DELETE FROM views_geometry_columns
        WHERE view_name = 'v2_1d_boundary_conditions_view';"""
        )

        conn.execute(
            """
        INSERT INTO views_geometry_columns (view_name, view_geometry,
        view_rowid, f_table_name, f_geometry_column)
        VALUES('v2_1d_boundary_conditions_view', 'the_geom',
        'connection_node_id', 'v2_connection_nodes', 'the_geom');"""
        )
        conn.execute(
            """
        CREATE VIEW IF NOT EXISTS v2_cross_section_location_view 
        AS SELECT loc.ROWID as ROWID, loc.id as loc_id, loc.code as loc_code, 
        loc.reference_level as loc_reference_level, 
        loc.bank_level as loc_bank_level, loc.friction_type as 
        loc_friction_type, loc.friction_value as loc_friction_value, 
        loc.definition_id as loc_definition_id, loc.channel_id as 
        loc_channel_id, loc.the_geom as the_geom, def.id as def_id, 
        def.shape as def_shape, def.width as def_width, def.code as 
        def_code, def.height as def_height 
        FROM v2_cross_section_location loc, v2_cross_section_definition def 
        WHERE loc.definition_id = def.id;"""
        )

        conn.execute(
            """
        DELETE FROM views_geometry_columns
        WHERE view_name = 'v2_cross_section_location_view';"""
        )

        conn.execute(
            """
        INSERT INTO views_geometry_columns (view_name, view_geometry,
        view_rowid, f_table_name, f_geometry_column)
        VALUES('v2_cross_section_location_view', 'the_geom',
        'ROWID', 'v2_cross_section_location', 'the_geom');"""
        )

        conn.commit()
        conn.close()

    def check_unexpected_index_table(self, existing_tables, expected_tables):
        too_many_index_tables = list(set(existing_tables) - set(expected_tables))
        if len(too_many_index_tables) > 0:
            msg = (
                "database contains one or more index table(s) that should not exist: "
                + str(too_many_index_tables)
            )
            logger.warning(msg)

    def get_missing_index_tables(self, expected_index_table_names):

        existing_tables = self.engine.table_names()
        existing_index_tables = [
            table
            for table in existing_tables
            if table.startswith("idx_") and "v2_" in table
        ]
        # Each table with geometry has four index tables in existing_index_tables, e.g.
        # table with geometry = "v2_channel" has 1) idx_v2_channel_the_geom,
        # 2) idx_v2_channel_the_geom_node, 3) idx_v2_channel_the_geom_parent,
        # and 4) idx_v2_channel_the_geom_rowid. From these four index tables we only
        # want to retrieve string "v2_channel"
        existing_index_table_names = list(
            set(
                [
                    table.split("idx_")[1].split("_the_geom")[0]
                    for table in existing_index_tables
                ]
            )
        )
        self.check_unexpected_index_table(
            existing_index_table_names, expected_index_table_names
        )
        missing_index_tables = list(
            set(expected_index_table_names) - set(existing_index_table_names)
        )
        return missing_index_tables

    def fix_spatial_indices(self):
        """ fixes spatial index all tables in spatialite in multiple steps
        1.  Create new spatial indices.
            -   Each v2_ tbl must have spatial index, otherwise one gets an SQL error
                while deleting an feature (row) from a table (e.g.
                v2_2d_boundary_conditions row delete returns
                "no such table:  main.idx_v2_2d_boundary_conditions_the_geom"
            -   Only create sp if sp not exists since this takes long
        2.  Make sure all spatial indices are valid, otherwise recover
        3.  Disable spatial index, otherwise layers sometimes will not be shown in QGIS
        4.  VACUUM spatialite to clean up spatialite (reclaims unused space)
        """

        if self.db_type != "spatialite":
            return

        expected_index_tables = [
            ("v2_2d_boundary_conditions", "the_geom"),
            ("v2_2d_lateral", "the_geom"),
            ("v2_calculation_point", "the_geom"),
            ("v2_channel", "the_geom"),
            ("v2_connected_pnt", "the_geom"),
            ("v2_connection_nodes", "the_geom"),
            ("v2_connection_nodes", "the_geom_linestring"),
            ("v2_cross_section_location", "the_geom"),
            ("v2_culvert", "the_geom"),
            ("v2_dem_average_area", "the_geom"),
            ("v2_floodfill", "the_geom"),
            ("v2_grid_refinement", "the_geom"),
            ("v2_grid_refinement_area", "the_geom"),
            ("v2_impervious_surface", "the_geom"),
            ("v2_initial_waterlevel", "the_geom"),
            ("v2_levee", "the_geom"),
            ("v2_obstacle", "the_geom"),
            ("v2_pumped_drainage_area", "the_geom"),
            ("v2_surface", "the_geom"),
            ("v2_windshielding", "the_geom"),
        ]

        progress_percentage_vacuum = 5
        total_progress = len(expected_index_tables) + progress_percentage_vacuum
        progress_bar = StatusProgressBar(total_progress, "prepare schematisation")
        expected_index_table_names = [table[0] for table in expected_index_tables]
        missing_index_tables = self.get_missing_index_tables(expected_index_table_names)
        for (table, geom_column) in expected_index_tables:
            # 1. create spatial index (idx_ tables) if not exists
            if table in missing_index_tables:
                self.create_spatial_index(table, geom_column)
            # 2. Ensure valid spatial index
            if not self.has_valid_spatial_index(table, geom_column):
                self.recover_spatial_index(table, geom_column)
            # 3. disable spatial index
            self.disable_spatial_index(table, geom_column)
            progress_bar.increase_progress(1, "")
        # 4. Vacuum spatialite
        self.run_vacuum()
        progress_bar.increase_progress(progress_percentage_vacuum, "")

    def create_spatial_index(self, table_name, geom_column):
        if self.db_type == "spatialite":
            select_statement = """
               SELECT CreateSpatialIndex('{table_name}', '{geom_column}');
            """.format(
                table_name=table_name, geom_column=geom_column
            )
            with self.engine.begin() as connection:
                connection.execute(text(select_statement))

    def delete_from(self, table_name):
        del_statement = """DELETE FROM {}""".format(table_name)

        # runs a transaction
        with self.engine.begin() as connection:
            connection.execute(text(del_statement))

    def table_is_empty(self, table_name):
        """
        check if the given table is empty

        :returns False if the table contains a least one entry
        """
        select_statement = """SELECT 0 FROM {table_name} LIMIT 1;""".format(
            table_name=table_name
        )
        with self.engine.begin() as connection:
            res = connection.execute(text(select_statement))
            result = res.fetchone()
            return result is None

    def has_valid_spatial_index(self, table_name, geom_column):
        """
        validate the spatial index for the given table with the given
        geometry column
        """
        # runs a transaction
        if self.db_type == "spatialite":
            select_statement = """
               SELECT CheckSpatialIndex('{table_name}', '{geom_column}');
            """.format(
                table_name=table_name, geom_column=geom_column
            )
            with self.engine.begin() as connection:
                result = connection.execute(text(select_statement))
                return bool(result.fetchone()[0])

    def recover_spatial_index(self, table_name, geom_column):
        """
        recover the spatial index for the given table with the given
        geometry column
        :returns True when recovery was successful, False otherwise
        """
        if self.db_type == "spatialite":
            select_statement = """
               SELECT RecoverSpatialIndex('{table_name}', '{geom_column}');
            """.format(
                table_name=table_name, geom_column=geom_column
            )
            with self.engine.begin() as connection:
                result = connection.execute(text(select_statement))
                return bool(result.fetchone()[0])

    def disable_spatial_index(self, table_name, geom_column):
        if self.db_type == "spatialite":
            select_statement = """
               SELECT DisableSpatialIndex('{table_name}', '{geom_column}');
            """.format(
                table_name=table_name, geom_column=geom_column
            )
            with self.engine.begin() as connection:
                connection.execute(text(select_statement))

    def drop_idx_table_if_exists(self, idx_name):
        if self.db_type == "spatialite":
            drop_statement = """DROP TABLE IF EXISTS '{idx_name}'""".format(
                idx_name=idx_name
            )
            with self.engine.begin() as connection:
                connection.execute(text(drop_statement))

    def run_vacuum(self):
        """
        call vacuum on a sqlite DB which reclaims any unused storage space from sqlite
        """
        if self.db_type == "spatialite":
            statement = """VACUUM;"""
            with self.engine.begin() as connection:
                connection.execute(text(statement))


def get_databases():
    d = {}
    qs = QSettings()

    # spatialite
    qs.beginGroup("SpatiaLite/connections")

    for db_entry in qs.allKeys():
        db_name, _ = os.path.split(db_entry)

        settings = {
            "key": os.path.basename(db_entry),
            "db_name": db_name,
            "combo_key": "spatialite: {0}".format(os.path.splitext(db_name)[0]),
            "db_type": "spatialite",
            "db_settings": {"db_path": qs.value(db_entry)},
        }

        d[settings["combo_key"]] = settings
    qs.endGroup()

    qs.beginGroup("PostgreSQL/connections")
    for db_entry in qs.allKeys():
        prefix, attribute = os.path.split(db_entry)
        db_name = qs.value(prefix + "/database")
        settings = {
            "key": db_entry,
            "db_name": db_name,
            "combo_key": "postgres: {0}".format(db_name),
            "db_type": "postgres",
            "db_settings": {
                "host": qs.value(prefix + "/host"),
                "port": qs.value(prefix + "/port"),
                "database": qs.value(prefix + "/database"),
                "username": qs.value(prefix + "/username"),
                "password": qs.value(prefix + "/password"),
            },
        }

        if qs.value(prefix + "/saveUsername") == u"true":
            settings["saveUsername"] = True
            settings["db_settings"]["username"] = qs.value(prefix + "/username")
        else:
            settings["saveUsername"] = False

        if qs.value(prefix + "/savePassword") == u"true":
            settings["savePassword"] = True
            settings["db_settings"]["password"] = qs.value(prefix + "/password")
        else:
            settings["savePassword"] = False

        d[settings["combo_key"]] = settings
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

    _db_settings = db["db_entry"]["db_settings"]

    if db["db_entry"]["db_type"] == "spatialite":
        host = _db_settings["db_path"]
        db["db_settings"] = {
            "host": host,
            "port": "",
            "name": "",
            "username": "",
            "password": "",
            "schema": "",
            "database": "",
            "db_path": host,
        }
    else:
        db["db_settings"] = _db_settings
        db["db_settings"]["schema"] = "public"
    return db
