from sqlalchemy import (Table, select)
from ThreeDiToolbox.utils.constants import (
    V2_TABLES, NON_SETTINGS_TBL_WITH_RASTERS, RASTER_CHECKER_MAPPER)

import logging
log = logging.getLogger(__name__)

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
            except Exception as e:
                msg = "table {tbl_xx} could not be converted into a " \
                      "SQLAlchemy Table".format(tbl_xx=tblname)
                log.error(msg)
                log.error(e)


class RasterCheckerEntrees(object):
    """
    Class for getting all rasters references in a sqlite
    """
    def __init__(self, datamodel, session):
        self.datamodel_pre = datamodel
        self.session_pre = session

    def get_all_v2_tables(self):
        return list(
            set([a for a in dir(self.datamodel_pre) if a.startswith('v2_')]))

    def get_all_raster_ref(self):
        """
        get all raster references from the sqlite datamodel
        :param :
        :return: all_raster_ref: list with tuples (<tablename>, <columnname>,
        <tbl_id>, <rastername>) e.g.:
        [('v2_global_settings', 1, 'dem_file', 'rasters/test1.tif'),
         ('v2_global_settings', 1, 'frict_coef_file', 'rasters/test2.tif'),
        """
        file_tbl = []
        file_id = []
        file_column = []
        file_name = []
        table_list = self.get_all_v2_tables()
        for tbl in table_list:
            all_columns = getattr(self.datamodel_pre, tbl).columns.keys()
            file_columns = [x for x in all_columns if '_file' in x]
            for column in file_columns:
                sql_tbl = getattr(self.datamodel_pre, tbl).c
                sql_column = getattr(sql_tbl, column)
                q = select([sql_column, sql_tbl.id])
                res = self.session_pre.execute(q)
                select_rows = [x for x in res if x[column]] # e.g. row['dem_file'] not None:
                for row in select_rows:
                    file_tbl.append(tbl)
                    file_id.append(row['id'])
                    file_column.append(column)
                    file_name.append(str(row[column]))
        all_raster_ref = zip(file_tbl, file_id, file_column, file_name)
        return all_raster_ref

    def get_foreign_keys(self):
        """
        get all foreign keys from v2_global_settings to other tables that may
        contain raster references
        :param :
        :return:
        """
        file_tbl = []
        file_id = []
        file_column = []
        file_name = []
        tbl_settings = 'v2_global_settings'
        all_settings_columns = getattr(
            self.datamodel_pre, tbl_settings).columns.keys()
        for column in all_settings_columns:
            for tbl, col in NON_SETTINGS_TBL_WITH_RASTERS.iteritems():
                if col == column:
                    sql_tbl = getattr(self.datamodel_pre, tbl_settings).c
                    sql_column = getattr(sql_tbl, col)
                    q = select([sql_column, sql_tbl.id])
                    res = self.session_pre.execute(q)
                    select_rows = [x for x in res if x[column]]
                    for row in select_rows:
                        file_tbl.append(tbl_settings)
                        file_id.append(row['id'])
                        file_column.append(column)
                        file_name.append(row[column])
        foreign_keys = zip(file_tbl, file_id, file_column, file_name)
        return foreign_keys

    def get_unique_setting_ids(self, all_raster_ref):
        """
        get all uniqe_ids from v2_global_settings
        item[0] = tbl, item[1] = id, item[2] = clm_name, item[3] = rastername
        :param ds:
        :return:
        """
        unique_ids = list(set([item[1] for item in all_raster_ref if
                               item[0] == 'v2_global_settings']))
        return unique_ids

    def get_entrees(self):
        """
        group raster_ref per model_entree_id
        :param all_raster_ref:
        :param foreign_keys:
        :return: entree_dict: a dictionary with
            - keys = global_setting_id
            - values = list with raster reference ['test1.tif, test2.tif]
        """
        all_raster_ref = self.get_all_raster_ref()
        foreign_keys = self.get_foreign_keys()

        entrees_dict = {}

        model_entree_ids = self.get_unique_setting_ids(all_raster_ref)
        for entree_id in model_entree_ids:
            entrees_dict.setdefault(entree_id, [])
            dem_used = False
            for ref_item in all_raster_ref:
                ref_tbl_name = ref_item[0]
                ref_setting_id = ref_item[1]
                ref_column_name = ref_item[2]
                ref_raster_str = ref_item[3]
                if ref_column_name == 'dem_file':
                    dem_used = True
                if ref_setting_id == entree_id and \
                        ref_tbl_name == 'v2_global_settings':
                    entrees_dict[entree_id].append(ref_raster_str)

                for tbl, col in NON_SETTINGS_TBL_WITH_RASTERS.iteritems():
                    if ref_tbl_name == tbl:
                        for fk_item in foreign_keys:
                            fk_setting_id = fk_item[1]
                            fk_column_name = fk_item[2]
                            fk_id = fk_item[3]
                            if fk_setting_id == entree_id \
                                    and fk_column_name == col \
                                    and fk_id == ref_setting_id:
                                entrees_dict[entree_id].append(ref_raster_str)
            if dem_used is False:
                log.warning('RasterChecker skips v2_global_settings id %d as'
                            'this id does not (but must) refer to an '
                            'elevation raster' % entree_id)
                del entrees_dict[entree_id]

        # Change order of entrees.value() (=list of raster_path strings), so
        # that the dem_raster is on the first index. The dem is the leading
        # model raster when comparing rasters
        for setting_id, rasters in entrees_dict.iteritems():
            for tbl, id, column, raster in all_raster_ref:
                if setting_id == id and column == 'dem_file':
                    dem = raster
                    dem_index = rasters.index(dem)
                    if dem_index <> 0:
                        rasters[0], rasters[dem_index] = rasters[dem_index], rasters[0]
        return entrees_dict
