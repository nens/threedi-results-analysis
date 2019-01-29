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

    def get_all_raster_ref(self):
        """
        get all raster references from the datamodel (and their
        # tablename, columnname, rowid)
        :param :
        :return:
        """
        table_list = [a for a in dir(
            self.datamodel_pre) if a.startswith('v2_')]
        file_tbl = []
        file_id = []
        file_column = []
        file_name = []
        for tbl in set(table_list):
            try:
                all_columns = getattr(self.datamodel_pre, tbl).columns.keys()
                for column in all_columns:
                    if '_file' in column:
                        get_table = getattr(self.datamodel_pre, tbl).c
                        get_column = getattr(get_table, column)
                        q = select([get_column, get_table.id])
                        res = self.session_pre.execute(q)
                        for row in res:
                            if row[column]:  # e.g. row['dem_file'] not None:
                                file_tbl.append(tbl)
                                file_id.append(row['id'])
                                file_column.append(column)
                                file_name.append(str(row[column]))
                all_raster_ref = zip(file_tbl, file_id, file_column, file_name)
                return all_raster_ref
            except Exception as e:
                log.error(e)

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
        try:
            for column in all_settings_columns:
                for tbl, col in NON_SETTINGS_TBL_WITH_RASTERS.iteritems():
                    if col == column:
                        get_table = getattr(self.datamodel_pre, tbl_settings).c
                        get_column = getattr(get_table, col)
                        q = select([get_column, get_table.id])
                        res = self.session_pre.execute(q)
                        for row in res:
                            if row[column]:
                                file_tbl.append(tbl_settings)
                                file_id.append(row['id'])
                                file_column.append(column)
                                file_name.append(row[column])
            foreign_keys = zip(file_tbl, file_id, file_column, file_name)
            return foreign_keys
        except Exception as e:
            log.error(e)

    def get_unique_setting_ids(self, all_raster_ref):
        """
        get all uniqe_ids from v2_global_settings
        item[0] = tbl, item[1] = id, item[2] = clm_name, item[3] = file_name
        :param ds:
        :return:
        """
        try:
            unique_ids = list(set([item[1] for item in all_raster_ref
                                   if item[0] == 'v2_global_settings']))
            return unique_ids
        except Exception as e:
            log.error(e)

    def get_dem_per_entree(self, entrees, setting_id, all_raster_ref):
        for id, rasters in entrees.iteritems():
            if id == setting_id:
                for raster in rasters:
                    for item in all_raster_ref:
                        if raster == item[3] and item[2] == 'dem_file':
                            dem_per_entree = raster
            return dem_per_entree

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
                msg = 'entree id %d does not (but must) include an elevation' \
                      ' raster' % entree_id
                self.messages.append("[Error]: {}. \n".format(msg))
                del entrees_dict[entree_id]

        # Change order of entrees.value() (=list of raster_path strings), so
        # that the dem_raster is on the first index. The dem is the leading
        # model raster when comparing rasters
        for setting_id, rasters in entrees_dict.iteritems():
            dem = self.get_dem_per_entree(
                entrees_dict, setting_id, all_raster_ref)
            dem_index = rasters.index(dem)
            if dem_index <> 0:
                rasters[0], rasters[dem_index] = rasters[dem_index], rasters[0]
        return entrees_dict

