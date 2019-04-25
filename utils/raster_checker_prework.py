# (c) Nelen & Schuurmans, see LICENSE.rst.

from sqlalchemy import Table, select
from ThreeDiToolbox.utils.constants import V2_TABLES, NON_SETTINGS_TBL_WITH_RASTERS
import logging

logger = logging.getLogger(__name__)


class DataModelSource(object):
    """
    we create abstract models of
    each table in the datasource sqlite that contains possible
    raster reference links. We do this as:
    1. the datasource tablestructure has been modified a lot the last
    years;
    2. the raster checker should work for all sqlites (also those of 3
    years ago);
    3. users should not have to migrate the sqlite before they can use the
    checker;
    4: the models in sql_models/model_schematisation are outdated;
    5. we do not want to care about all the possilbe combinations of table
    content;
    6. luckly enough the column names did not change the last years;
    """

    def __init__(self, metadata):
        self.dms_metatdata = metadata
        for tblname in V2_TABLES:
            try:
                __table__ = Table(tblname, metadata, autoload=True)
                setattr(self, tblname, __table__)
            except Exception:
                pass


class RasterCheckerEntrees(object):
    """
    Class for getting all rasters references in a sqlite
    """

    def __init__(self, datamodel, session):
        self.datamodel_pre = datamodel
        self.session_pre = session
        self._all_raster_ref = None
        self._foreign_keys = None
        self._entrees = None
        self._entrees_metadata = None
        self._unique_setting_ids = None

    def get_all_v2_tables(self):
        return list(set([a for a in dir(self.datamodel_pre) if a.startswith("v2_")]))

    @property
    def all_raster_ref(self):
        """
        get all raster references from the sqlite datamodel
        :param :
        :return: all_raster_ref: list with tuples:
        [(tablename>, <row_id>, <columnname>, , <rastername>)] e.g.: [
            ('v2_global_settings', 1, 'dem_file', 'rasters/test1.tif'),
            ('v2_global_settings', 2, 'dem_file', 'rasters/test3.tif'),
            ('v2_global_settings', 2, 'frict_coef_file', 'rasters/test2.tif'),
            ('v2_interflow', 1, 'porosity_file', 'rasters/test2.tif'),
            ('v2_groundwater', 4, 'leakage_file', 'rasters/test2.tif')]
        """

        if self._all_raster_ref:
            return self._all_raster_ref

        file_tbl = []
        file_id = []
        file_column = []
        file_name = []
        table_list = self.get_all_v2_tables()
        for tbl in table_list:
            all_columns = getattr(self.datamodel_pre, tbl).columns.keys()
            file_columns = [x for x in all_columns if "_file" in x]
            for column in file_columns:
                sql_tbl = getattr(self.datamodel_pre, tbl).c
                sql_column = getattr(sql_tbl, column)
                q = select([sql_column, sql_tbl.id])
                res = self.session_pre.execute(q)
                select_rows = [x for x in res if x[column]]
                for row in select_rows:
                    file_tbl.append(tbl)
                    file_id.append(row["id"])
                    file_column.append(column)
                    file_name.append(str(row[column]))
        # in python3 zip returns iterator so return the list of zip object
        self._all_raster_ref = list(zip(file_tbl, file_id, file_column, file_name))
        return self._all_raster_ref

    @property
    def foreign_keys(self):
        """
        get all foreign keys from v2_global_settings to other tables that may
        contain raster references
        :param :
        :return: all_raster_ref: list with tuples:
        [(tablename>, <row_id>, <columnname>, , <foreign_key_id>)] e.g.: [
            ('v2_global_settings', 1, 'groundwater_settings_id', 4),
            ('v2_global_settings', 2, 'interflow_settings_id', 1)]
        """
        if self._foreign_keys:
            return self._foreign_keys

        file_tbl = []
        file_id = []
        file_column = []
        file_name = []
        tbl_settings = "v2_global_settings"
        all_settings_columns = getattr(self.datamodel_pre, tbl_settings).columns.keys()
        for column in all_settings_columns:
            for tbl, col in NON_SETTINGS_TBL_WITH_RASTERS.items():
                if col == column:
                    sql_tbl = getattr(self.datamodel_pre, tbl_settings).c
                    sql_column = getattr(sql_tbl, col)
                    q = select([sql_column, sql_tbl.id])
                    res = self.session_pre.execute(q)
                    select_rows = [x for x in res if x[column]]
                    for row in select_rows:
                        file_tbl.append(tbl_settings)
                        file_id.append(row["id"])
                        file_column.append(column)
                        file_name.append(row[column])
        # in python3 zip returns iterator so return the list of zip object
        self._foreign_keys = list(zip(file_tbl, file_id, file_column, file_name))
        return self._foreign_keys

    @property
    def unique_setting_ids(self):
        """
        get all unique_ids from v2_global_settings
        item[0] = tbl, item[1] = id, item[2] = clm_name, item[3] = rastername
        :param
        :return:
        """
        if self._unique_setting_ids:
            return self._unique_setting_ids

        self._unique_setting_ids = list(
            set(
                [
                    item[1]
                    for item in self.all_raster_ref
                    if item[0] == "v2_global_settings"
                ]
            )
        )
        self._unique_setting_ids.sort()
        return self._unique_setting_ids

    def check_dem_used(self, entree_id):
        dem_used = False
        for ref_item in self.all_raster_ref:
            ref_column_name = ref_item[2]
            if ref_column_name == "dem_file":
                dem_used = True
        if not dem_used:
            logger.warning(
                "RasterChecker skips v2_global_settings id %d as"
                "this id does not (but must) refer to an "
                "elevation raster" % entree_id
            )
        return dem_used

    @property
    def entrees_metadata(self):
        """
        get all raster references (and other metadata) per model_entree_id
        :return: _entrees_metadata: a tuple with with tuples with metadata:
            ((model entree id, table name, column name, raster name)) e.g.:
            ((1, 'v2_global_settings', 'dem_file', 'rasters/test1.tif'),
             (1, 'v2_groundwater', 'leakage_file', 'rasters/test2.tif'),
             (2, 'v2_global_settings', 'dem_file', 'rasters/test3.tif'),
             (2, 'v2_global_settings', 'frict_coef_file', 'rasters/test2.tif'),
             (2, 'v2_interflow', 'porosity_file', 'rasters/test2.tif'))
        """
        if self._entrees_metadata:
            return self._entrees_metadata

        entrees_dict_log_file = []

        model_entree_ids = self.unique_setting_ids
        for entree_id in model_entree_ids:

            if not self.check_dem_used(entree_id):
                # no elevation raster here, so go to next model_entree
                continue
            # first find the dem (assumed that this is always in the
            # v2_global_settings table)
            for ref_item in self.all_raster_ref:
                ref_tbl_name = ref_item[0]
                ref_setting_id = ref_item[1]
                ref_column_name = ref_item[2]
                ref_raster_str = ref_item[3]
                if (
                    ref_setting_id == entree_id
                    and ref_tbl_name == "v2_global_settings"
                    and ref_column_name == "dem_file"
                ):
                    entrees_dict_log_file.append(
                        (entree_id, ref_tbl_name, ref_column_name, ref_raster_str)
                    )
            # now the rest of the rasters (in the v2_global_settings)
            for ref_item in self.all_raster_ref:
                ref_tbl_name = ref_item[0]
                ref_setting_id = ref_item[1]
                ref_column_name = ref_item[2]
                ref_raster_str = ref_item[3]
                if (
                    ref_setting_id == entree_id
                    and ref_tbl_name == "v2_global_settings"
                    and ref_column_name != "dem_file"
                ):
                    entrees_dict_log_file.append(
                        (entree_id, ref_tbl_name, ref_column_name, ref_raster_str)
                    )
            # now the rest of the rasters outside of the v2_global_settings
            for ref_item in self.all_raster_ref:
                ref_tbl_name = ref_item[0]
                ref_setting_id = ref_item[1]
                ref_column_name = ref_item[2]
                ref_raster_str = ref_item[3]
                for tbl, col in NON_SETTINGS_TBL_WITH_RASTERS.items():
                    if ref_tbl_name == tbl:
                        for fk_item in self.foreign_keys:
                            fk_setting_id = fk_item[1]
                            fk_column_name = fk_item[2]
                            fk_id = fk_item[3]
                            if (
                                fk_setting_id == entree_id
                                and fk_column_name == col
                                and fk_id == ref_setting_id
                            ):
                                entrees_dict_log_file.append(
                                    (
                                        entree_id,
                                        ref_tbl_name,
                                        ref_column_name,
                                        ref_raster_str,
                                    )
                                )
        # sort the list with tuple based on the first element of tuple, which
        # is the setting_id
        entrees_dict_log_file.sort(key=self.sort_by_setting_id)
        # convert list with tuple to tuple with tuples so that dem is always
        # on the first index (important in the rest of the RasterChecker)
        self._entrees_metadata = tuple(entrees_dict_log_file)
        return self._entrees_metadata

    def sort_by_setting_id(self, elem):
        if len(elem) != 4:
            raise AssertionError("should have 4 elements setting_id on 1st")
        return elem[0]

    @property
    def entrees(self):
        """
        abstracts only necessary info (setting_id and rasternames) from
        self.entrees_metadata and puts it in a dictionary. Each element in that
        dict is a modelentree
        So from this (self.entrees_metadata)
            ((1, 'v2_global_settings', 'dem_file', 'rasters/test1.tif'),
             (1, 'v2_groundwater', 'leakage_file', 'rasters/test2.tif'),
             (2, 'v2_global_settings', 'dem_file', 'rasters/test3.tif'),
             (2, 'v2_global_settings', 'frict_coef_file', 'rasters/test2.tif'),
             (2, 'v2_interflow', 'porosity_file', 'rasters/test2.tif'))
        to this: (self._entrees)
         {1: ('rasters/test1.tif', 'rasters/test2.tif'),
          2: ('rasters/test3.tif', 'rasters/test2.tif', 'rasters/test2.tif')}
        :return: self._entrees (dict)
        """
        if self._entrees:
            return self._entrees
        entrees = {}
        for unique_id in self.unique_setting_ids:
            entrees.setdefault(unique_id, ())
            for row in self.entrees_metadata:
                setting_id = row[0]
                raster = row[3]
                if unique_id == setting_id:
                    entrees[setting_id] = entrees[setting_id] + (raster,)
        self._entrees = entrees
        return self._entrees
