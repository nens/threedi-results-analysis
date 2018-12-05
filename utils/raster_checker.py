# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.
import itertools

from sqlalchemy import (Boolean, Column, Integer, String, Float, ForeignKey)
from sqlalchemy import (create_engine, Table, Column, Integer, String, Float,
                        MetaData, ForeignKey)
from sqlalchemy import select
from sqlalchemy import update
from ThreeDiToolbox.utils.threedi_database import ThreediDatabase
from ThreeDiToolbox.utils.user_messages import (
    pop_up_info, messagebar_message)
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
import time
import os
import string
import logging
import osr
from gdal import GA_ReadOnly
from osgeo import gdal
import numpy as np
from osgeo import osr
from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsFields, QgsField, QgsVectorFileWriter, QGis,
                       QgsFeature, QgsGeometry, QgsPoint,
                       QgsCoordinateReferenceSystem, QgsCoordinateTransform)
from itertools import izip

# from qgis._core import QgsFields, QgsField, QgsVectorFileWriter, QGis, \
#     QgsFeature, QgsGeometry, QgsPoint, QgsCoordinateReferenceSystem, \
#     QgsCoordinateTransform


log = logging.getLogger(__name__)
Base = declarative_base()

"""
Module that checks the rasters of a threedi model on multiple requirements:
1. does a global settings entrees exists with references to raster(s)?
2. do the rasters (references from the model) really exists?
3. no special chars in the raster filename?
4. is extension really .tif?
5. can we read-in the raster? (file-corruption)
5. can we read-in the raster? (file-corruption)
6. is the raster single_band?
7. nodata = -9999?
8. projection unit in meters? and not degrees..
9. is projection complete?
10. is the data_type float_32?
11. is the raster compressed? (compression=deflate)
12. pixels are square?
13. logic max, min values in raster?
14. is the extent of all the rasters in 1 model entree the same?
15. max number pixels not exceeded
"""

v2_tables_list = [
    'v2_1d_boundary_conditions',
    'v2_1d_lateral',
    'v2_2d_boundary_conditions',
    'v2_2d_lateral',
    'v2_aggregation_settings',
    'v2_calculation_point',
    'v2_channel',
    'v2_connected_pnt',
    'v2_connection_nodes',
    'v2_control',
    'v2_control_delta',
    'v2_control_group',
    'v2_control_measure_group',
    'v2_control_measure_map',
    'v2_control_memory',
    'v2_control_pid',
    'v2_control_table',
    'v2_control_timed',
    'v2_cross_section_definition',
    'v2_cross_section_location',
    'v2_cross_section_view',
    'v2_culvert',
    'v2_culvert_view',
    'v2_dem_average_area',
    'v2_global_settings',
    'v2_grid_refinement',
    'v2_grid_refinement_area',
    'v2_groundwater',
    'v2_impervious_surface',
    'v2_impervious_surface_map',
    'v2_interflow',
    'v2_levee',
    'v2_manhole',
    'v2_manhole_view',
    'v2_numerical_settings',
    'v2_obstacle',
    'v2_orifice',
    'v2_pipe',
    'v2_pumpstation',
    'v2_simple_infiltration',
    'v2_surface',
    'v2_surface_map',
    'v2_surface_parameters',
    'v2_weir',
    'v2_windshielding',
]

non_settings_tbl_with_rasters = [
    ['v2_simple_infiltration', 'simple_infiltration_settings_id'],
    ['v2_groundwater', 'groundwater_settings_id'],
    ['v2_interflow', 'interflow_settings_id']
]


def _iter_block_row(band, offset_y, block_height, block_width, no_data_value):
    ncols = int(band.XSize / block_width)
    for i in range(ncols):
        arr = band.ReadAsArray(i * block_width, offset_y, block_width,
                               block_height)
        # if no_data_value is not None:
        #     arr[arr == no_data_value] = -9999.
        # idx_nodata = np.argwhere(arr == -9999.)
        # arr = None
        yield (i * block_width, offset_y, (i + 1) * block_width, offset_y +
               block_height), arr
    # possible leftover block
    width = band.XSize - (ncols * block_width)
    if width > 0:
        arr = band.ReadAsArray(i * block_width, offset_y, width, block_height)
        # if no_data_value is not None:
        #     arr[arr == no_data_value] = -9999.
        # idx_nodata = np.argwhere(arr == no_data_value)
        yield (ncols * block_width, offset_y, ncols * block_width + width,
               offset_y + block_height), arr

        # offset_y + block_height), arr


def iter_blocks(band, block_width=0, block_height=0):
    """ Iterate over native blocks in a GDal raster data band.
    Optionally, provide a minimum block dimension.
    Returns a tuple of bbox (x1, y1, x2, y2) and the data as ndarray. """
    nrows = int(band.YSize / block_height)
    no_data_value = band.GetNoDataValue()
    for j in range(nrows):
        for block in _iter_block_row(band, j * block_height, block_height,
                                     block_width, no_data_value):
            yield block
    # possible leftover row
    height = band.YSize - (nrows * block_height)
    if height > 0:
        for block in _iter_block_row(band, nrows * block_height, height,
                                     block_width, no_data_value):
            yield block


def optimize_blocksize(band, min_blocksize=256, max_blocksize=1024):
    raster_height = band.YSize
    raster_width = band.XSize
    block_height, block_width = band.GetBlockSize()
    # optimize block_width
    if min_blocksize <= block_width <= max_blocksize:
        # in betweek is okay
        pass
    elif block_width <= min_blocksize:
        if min_blocksize <= raster_width:
            block_width = min_blocksize
        else:
            block_width = raster_width
    elif block_width >= max_blocksize:
        block_width = max_blocksize
    # optimize block_height
    if min_blocksize <= block_height <= max_blocksize:
        # in betweek is okay
        pass
    elif block_height <= min_blocksize:
        if min_blocksize <= raster_height:
            block_height = min_blocksize
        else:
            block_height = raster_height
    elif block_height >= max_blocksize:
        block_height = max_blocksize

    block_area = block_height * block_width
    raster_area = raster_width * raster_height
    nr_blocks = raster_area / block_area
    print 'block_height = ' + str(block_height)
    print 'block_width = ' + str(block_width)
    print 'block_area = ' + str(block_area)
    print 'raster_height = ' + str(raster_height)
    print 'raster_width = ' + str(raster_width)
    print 'raster_area = ' + str(raster_area)
    print 'nr_blocks = ' + str(nr_blocks)
    return block_width, block_height, nr_blocks


class DataModelSource(object):
    def __init__(self, metadata):
        self.dms_metatdata = metadata
        for tblname in v2_tables_list:
            try:
                __table__ = Table(tblname, metadata, autoload=True)
                setattr(self, tblname, __table__)
            except Exception as e:
                msg = "table {tbl_xx} could not be converted into a " \
                      "SQLAlchemy Table".format(tbl_xx=tblname)
                log.error(msg)
                log.error(e)


class RasterChecker(object):
    """
    Class for checking all rasters in a sqlie we create abstract models of
    each table in the datasource (sqlite/ postgres) that contains possible
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

    def __init__(self, threedi_database):
        """Init method.
        :param threedi_database - ThreediDatabase instance
        :return:
        """
        self.db = threedi_database
        # session required for SqlAlchemy queries
        self.session = self.db.get_session()
        # datamodel required for dynamic creation of ORM models
        self.engine = self.db.get_engine()
        self.metadata = MetaData(bind=self.engine)
        self.datamodel = DataModelSource(self.metadata)
        # user messages in Qgis
        self.messages = []

        self.sqlite_path = str(self.db.settings['db_path'])
        # e.g. '/home/renier.kramer/Desktop/wezep/wezep2.sqlite'
        self.sqlite_dir, self.sqltname_with_ext = os.path.split(
            self.sqlite_path)
        self.sqltname_without_ext = os.path.splitext(self.sqltname_with_ext)[0]

    def reset_messages(self):
        """Reset messages."""
        self.messages = []

    def close_session(self):
        self.session.close()

    def get_all_raster_ref(self):
        """
        get all raster references from the datamodel (and their
        # tablename, columnname, rowid)
        :param :
        :return:
        """
        table_list = [a for a in dir(self.datamodel) if a.startswith('v2_')]
        file_tbl = []
        file_id = []
        file_column = []
        file_name = []
        for tbl in set(table_list):
            try:
                all_columns = getattr(self.datamodel, tbl).columns.keys()
                for column in all_columns:
                    if '_file' in column:
                        get_table = getattr(self.datamodel, tbl).c
                        get_column = getattr(get_table, column)
                        q = select([get_column, get_table.id])
                        res = self.session.execute(q)
                        for row in res:
                            if row[column]:  # e.g. row['dem_file'] not None:
                                file_tbl.append(tbl)
                                file_id.append(row['id'])
                                file_column.append(column)
                                file_name.append(row[column])
                all_raster_ref = zip(file_tbl, file_id, file_column, file_name)
                return all_raster_ref
            except Exception as e:
                log.error(e)
                pass

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
            self.datamodel, tbl_settings).columns.keys()
        try:
            for column in all_settings_columns:
                for tbl_xxx, fk_column in non_settings_tbl_with_rasters:
                    if fk_column == column:
                        get_table = getattr(self.datamodel, tbl_settings).c
                        get_column = getattr(get_table, fk_column)
                        q = select([get_column, get_table.id])
                        res = self.session.execute(q)
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
            pass

    def get_unique_settings_ids(self, ds):
        """
        get all uniqe_ids from v2_global_settings
        item[0] = tbl, item[1] = id, item[2] = clm_name, item[3] = file_name
        :param ds:
        :return:
        """
        try:
            unique_ids = list(set([item[1] for item in
                                   ds if item[0] == 'v2_global_settings']))
            return unique_ids
        except Exception as e:
            log.error(e)
            pass

    def get_raster_ref_per_entrees(self, all_raster_ref, foreign_keys):
        """
        group raster_ref per model_entree_id
        :param all_raster_ref:
        :param foreign_keys:
        :return: entrees_dict
        """
        entrees_dict = {}

        model_entree_ids = self.get_unique_settings_ids(all_raster_ref)
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
                for tbl, column in non_settings_tbl_with_rasters:
                    if ref_tbl_name == tbl:
                        for fk_item in foreign_keys:
                            fk_setting_id = fk_item[1]
                            fk_column_name = fk_item[2]
                            fk_id = fk_item[3]
                            if fk_setting_id == entree_id \
                                    and fk_column_name == column \
                                    and fk_id == ref_setting_id:
                                entrees_dict[entree_id].append(ref_raster_str)
            if dem_used is False:
                msg = 'entree id %d does not (but must) include a ' \
                      'dem_tif' % entree_id
                del entrees_dict[entree_id]
        return entrees_dict

    def get_dem_per_entree(self, entrees, entree_id, all_raster_ref):
        for entree_id_item, rasters in entrees.iteritems():
            if entree_id_item == entree_id:
                for raster in rasters:
                    for item in all_raster_ref:
                        if raster == item[3] and item[2] == 'dem_file':
                            dem_per_entree = raster
            return dem_per_entree

    def check_sqlite_exists(self):
        # if sqlite exists, then return True, otherwise False
        if os.path.isfile(self.sqlite_path):
            msg = "found sqlite on your machine"
            return True
        else:
            msg = "could not find sqlite on your machine"
            return False

    def check1_entrees(self, entrees):
        """
        check 1. does a global settings entrees exists with references
        to raster(s)?
        :param entrees:
        :return:
        """
        check_entrees = []
        for key, value in entrees.iteritems():
            if key and value:
                msg = 'raster checker will check global settings entree ' \
                      'id %d that includes rasters: %s' % (key, str(value))
                self.messages.append("[Info]: {}. \n".format(msg))
                check_entrees.append(True)
            elif value is None:
                msg = 'no raster references found for global settings ' \
                      'entree %d \n' % key
                self.messages.append("[Warning]: {}. \n".format(msg))
                check_entrees.append(False)

        if all(check_entrees):
            return True
        else:
            return False

    def check2_tif_exists(self, entrees):
        """
        check 2. does the raster (reference from the model) really exists?
        :param entrees:
        :return:
        """
        check_tif_exists = []
        for key, value in entrees.iteritems():
            for rast_item in value:
                raster_path = os.path.join(self.sqlite_dir, rast_item)
                if os.path.isfile(raster_path):
                    check_tif_exists.append(True)
                else:
                    check_tif_exists.append(True)
        if all(check_tif_exists):
            return True
        else:
            return False

    def check3_tif_filename(self, entrees):
        """
        check 3. does the raster filename have valid chars (also space is not
        allowed)
        Exceptions:
        a) forward slash ('/') is a invalideChars but we exept only one
            occurence in the relative reference
        b) In the .sqlite these are always forward slash ('/') on both
            - Linux machine (os.name = 'posix')
            - and on Windows machine (os.name = 'nt')
        c) The dot ('.') is a invalideChars but we exept only one occurence
            in the relative reference
        :param entrees:
        :return:
        """
        check_tif_filename = []
        invalidChars = set(string.punctuation.replace("_", ""))
        invalidChars.add(' ')
        invalid_chars_in_filename = []

        for key, value in entrees.iteritems():
            for rast_item in value:
                if rast_item[-4:] != '.tif':
                    msg = "exetension of %s must be  .tif" % rast_item
                    check_tif_filename.append(False)

                count_forward_slash = 0
                count_dot = 0
                for char in rast_item:
                    if char in invalidChars:
                        if char == '/' and count_forward_slash < 1:
                            count_forward_slash += 1
                        elif char == '.' and count_dot < 1:
                            count_dot += 1
                        else:
                            invalid_chars_in_filename.append(char)
                            check_tif_filename.append(False)

        if invalid_chars_in_filename:
            # list is not empty
            if count_forward_slash > 1 or count_dot > 1:
                msg = "only one '.' and '/' is allowed in relative path"
            msg = 'Invalid filename, please remove the special chars: ' + str(
                invalid_chars_in_filename)

        if all(check_tif_filename):
            return True
        else:
            return False

    def checks4_to_9(self, entrees, all_raster_ref):
        """
        check 4. is the raster singleband ?
        check 5. is the raster nodata -9999 ?
        check 6. is the raster projection in meters ?
        check 7. is the raster datatype float32 ?
        check 8. is the raster compressed ?
        check 9. has the raster square pixels?
        :param entrees:
        :return:
        """
        self.check_singleband = []
        self.check_nodata = []
        self.check_projectn = []
        self.check_flt32 = []
        self.check_copmress = []
        self.check_square_pixels = []

        for key, value in entrees.iteritems():
            dem_cols = None
            dem_rows = None
            dem_upx = None  # upper x pixel
            dem_xres = None
            dem_xskew = None  # shear in the x direction
            dem_upy = None
            dem_yskew = None  # shear in the y direction
            dem_yres = None

            # upx, xres, xskew, upy, yskew, yres = gdalsrc.GetGeoTransform()
            # cols = gdalsrc.RasterXSize
            # rows = gdalsrc.RasterYSize

            dem = self.get_dem_per_entree(entrees, key, all_raster_ref)
            dem_index = value.index(dem)
            if dem_index == 0:
                pass
            else:
                # change order of raster list 'value' so that the dem_raster
                # becomes first to analyse. The dem is the leading model raster
                value[0], value[dem_index] = value[dem_index], value[0]
            for raster_index, rast_item in enumerate(value):
                raster_path = os.path.join(self.sqlite_dir, rast_item)
                src_ds = gdal.Open(raster_path, GA_ReadOnly)
                srcband = src_ds.GetRasterBand(1)

                # check4. is the raster singleband ?
                try:
                    cnt_rasterband = src_ds.RasterCount
                    if cnt_rasterband != 1:
                        msg = '%s.tif is not (but must be) a single-band ' \
                              'raster' % rast_item
                        self.check_singleband.append(False)
                    elif cnt_rasterband == 1:
                        self.check_singleband.append(True)
                except Exception as e:
                    log.error(e)
                    msg = 'unable to get raster bands'
                    self.check_singleband.append(False)

                # check5. is the raster nodata -9999 ?
                try:
                    nodata = srcband.GetNoDataValue()
                    if nodata == -9999:
                        self.check_nodata.append(True)
                    else:
                        self.check_nodata.append(False)
                        msg = 'no_data value %s.tif is not (but must be) ' \
                              '-9999' % rast_item
                except Exception as e:
                    log.error(e)
                    self.check_nodata.append(False)

                # check 6 is the raster projection in meters ?
                try:
                    proj = src_ds.GetProjection()
                    spat_ref = osr.SpatialReference()
                    spat_ref.ImportFromWkt(proj)
                    unit = spat_ref.GetLinearUnitsName()
                    if unit == 'metre':
                        self.check_projectn.append(True)
                    elif unit == 'degree':
                        msg = 'projection %s.tif is not (but must be) in ' \
                              'meters' % rast_item
                        self.check_projectn.append(False)
                except Exception as e:
                    log.error(e)
                    self.check_projectn.append(False)

                # check 7 is the raster datatype float32 ?
                try:
                    data_type = srcband.DataType
                    data_type_name = gdal.GetDataTypeName(data_type)
                    if data_type_name == 'Float32':
                        self.check_flt32.append(True)
                    else:
                        msg = 'datatype %s.tif is not (but must be) float_32' \
                              % rast_item
                        self.check_flt32.append(False)
                except Exception as e:
                    log.error(e)
                    self.check_flt32.append(False)

                # check 8 is the raster compressed ?
                try:
                    compr_method = src_ds.GetMetadata('IMAGE_STRUCTURE')[
                        'COMPRESSION']
                    if compr_method == 'DEFLATE':
                        self.check_copmress.append(True)
                    else:
                        msg = "%s.tif is not (but should be) compressed " \
                              "please use gdal_translate -co " \
                              "'COMPRESS=DEFLATE'" % rast_item
                        self.check_copmress.append(False)
                except Exception as e:
                    msg = 'unable to get compression method for ' \
                          '%s.tif' % rast_item
                    log.error(e)
                    self.check_flt32.append(False)

                # check 9 has the raster square pixels?
                try:
                    geotransform = src_ds.GetGeoTransform()
                    # horizontal pixel resolution
                    xres = abs(geotransform[1])
                    cnt_decimal_xres = str(xres)[::-1].find('.')
                    # vertical pixel resolution
                    yres = abs(geotransform[5])
                    cnt_decimal_yres = str(yres)[::-1].find('.')

                    if cnt_decimal_xres > 3 or cnt_decimal_yres > 3:
                        msg = 'watch out! %s.tif has a pixel resolution with' \
                              ' more than 3 decimals' % rast_item
                    if xres == yres:
                        self.check_square_pixels.append(True)
                    else:
                        self.check_square_pixels.append(False)
                except Exception as e:
                    msg = 'unable to get pixel resolution for %s.tif'\
                          % rast_item
                    log.error(e)
                    self.check_square_pixels.append(False)

    # def get_src_ds(self, entrees):
    #     for key, value in entrees.iteritems():
    #         for rast_item in value:
    #             raster_path = os.path.join(self.sqlite_dir, rast_item)
    #             src_ds = gdal.Open(raster_path, GA_ReadOnly)
    #             srcband = src_ds.GetRasterBand(1)
    #     for raster in [rast_item for rast_item in value for key, value in
    #      entrees_dict.iteritems()]:
    #         raster_path = os.path.join(self.sqlite_dir, raster)
    #         src_ds = gdal.Open(raster_path, GA_ReadOnly)
    #         return src_ds
    #
    # def check4_singleband(self, src_ds):
    #     # check4. is the raster singleband ?
    #     check_singleband = []
    #     try:
    #         cnt_rasterband = src_ds.RasterCount
    #         if cnt_rasterband <> 1:
    #             msg = '%s.tif is not (but must be) a single-band ' \
    #                   'raster' % rast_item
    #             check_singleband.append(False)
    #         elif cnt_rasterband == 1:
    #             check_singleband.append(True)
    #     except Exception as e:
    #         log.error(e)
    #         msg = 'unable to get raster bands'
    #         check_singleband.append(False)
    #
    #     if all(check_singleband):
    #         return True
    #     else:
    #         return False
    #
    # a get_src_ds(entrees)

    def check_pixels(self):

        raster_path1 = '/home/renier.kramer/jupyter_notebook/rasterchecker' \
                       '/dem_3di_logo.tif'
        raster_path2 = '/home/renier.kramer/jupyter_notebook/rasterchecker' \
                       '/dem_3di_logo_edit.tif'

        raster_path1 = '/home/renier.kramer/jupyter_notebook/rasterchecker' \
                       '/test1.tif'
        raster_path2 = '/home/renier.kramer/jupyter_notebook/rasterchecker' \
                       '/test2.tif'

        # raster_path1 = '/home/renier.kramer/jupyter_notebook/rasterchecker
        # /wezep_dem_wezep5.tif'
        # raster_path2 = '/home/renier.kramer/jupyter_notebook/rasterchecker
        # /wezep_inf87_24_0.tif'

        # raster_path1 = '/home/renier.kramer/jupyter_notebook/rasterchecker
        # /bergermeer_5m.tif'
        # raster_path2 = '/home/renier.kramer/jupyter_notebook/rasterchecker
        # /bergermeer_5m_copy.tif'

        raster1 = gdal.Open(raster_path1, GA_ReadOnly)
        raster2 = gdal.Open(raster_path2, GA_ReadOnly)

        band1 = raster1.GetRasterBand(1)
        band2 = raster2.GetRasterBand(1)

        # optimize_blocksize
        w, h, nr_blocks = optimize_blocksize(band1)

        # create generators
        raster1_generator = iter_blocks(band1, block_width=w, block_height=h)
        raster2_generator = iter_blocks(band2, block_width=w, block_height=h)

        ulx, xres, xskew, uly, yskew, yres = raster1.GetGeoTransform()
        pixelsize = abs(min(xres, yres))

        # np.set_printoptions(precision=4, suppress=True, formatter={
        # 'int_kind': '{:f}'.format})

        self.dem_nd_other_d_coor = []
        self.dem_d_other_nd_coor = []

        for data1, data2 in izip(raster1_generator, raster2_generator):
            bbox1, dem = data1
            data1 = None
            idx_nodata_dem = np.argwhere(dem == -9999.)
            dem = None
            bbox2, b = data2
            data2 = None
            idx_nodata_b = np.argwhere(b == -9999.)
            b = None
            # Comparing two numpy arrays for equality (element-wise)
            if len(idx_nodata_dem) > 1 and len(idx_nodata_b) > 1 and \
                    np.all(idx_nodata_dem == idx_nodata_b):
                pass
            elif len(idx_nodata_dem) < 1 and len(idx_nodata_b) < 1 and \
                    np.array_equal(idx_nodata_dem, idx_nodata_b):
                pass
            else:
                # (0,0) is (x,y) left-upper corner of first bbox. Going d
                # own bbox_row
                # increases. Going right bbox_col increases
                l_up_col = bbox1[0]
                l_up_row = bbox1[1]
                # r_down_col = bbox1[2]
                # r_down_row = bbox1[3]
                for pixel in idx_nodata_dem.tolist():
                    if pixel not in idx_nodata_b.tolist():
                        bbox_row = pixel[0]
                        bbox_column = pixel[1]
                        loc_col = l_up_col + bbox_column
                        loc_row = l_up_row + bbox_row
                        x_coor = ulx + pixelsize * loc_col
                        y_coor = uly - pixelsize * loc_row
                        self.dem_nd_other_d_coor.append([x_coor, y_coor])
                for pixel in idx_nodata_b.tolist():
                    if pixel not in idx_nodata_dem.tolist():
                        bbox_row = pixel[0]
                        bbox_column = pixel[1]
                        loc_col = l_up_col + bbox_column
                        loc_row = l_up_row + bbox_row
                        x_coor = ulx + pixelsize * loc_col
                        y_coor = uly - pixelsize * loc_row
                        self.dem_d_other_nd_coor.append([x_coor, y_coor])
        print 'dem_nd_other_d_coor = ' + str(self.dem_nd_other_d_coor)
        print 'dem_d_other_nd_coor = ' + str(self.dem_d_other_nd_coor)

    def all_checks(self):
        """
        some preperation steps:
        a. get_all_raster_ref(self)
        b. get_foreign_keys(self)
        c. get_unique_settings_ids(self, ds):
        d. get_raster_ref_per_entrees(self, all_raster_ref, foreign_keys)
        checks:
        1.  check_raster_ref(self, entrees):
        """

        if self.check_sqlite_exists():
            pass
        else:
            raise Exception('could not find sqlite')

        all_raster_ref = self.get_all_raster_ref()  # called only here

        foreign_keys = self.get_foreign_keys()  # called only here

        # get_unique_settings_ids
        # only called in get_raster_ref_per_entrees()

        entrees = self.get_raster_ref_per_entrees(all_raster_ref, foreign_keys)
        # called only here

        check_1 = self.check1_entrees(entrees)
        check_2 = self.check2_tif_exists(entrees)
        check_3 = self.check3_tif_filename(entrees)

        # checks456789
        self.checks4_to_9(entrees, all_raster_ref)

        # check 10
        self.check_pixels()

    def create_log(self):
        timestr = time.strftime("_%Y%m%d_%H%M%S")
        log_with_ext = self.sqltname_without_ext + timestr + '.log'
        self.log_path = os.path.join(self.sqlite_dir, log_with_ext)
        # write to log
        log_file = open(self.log_path, 'w')
        for message_row in self.messages:
            log_file.write(message_row)
        log_file.close()

    def create_shp(self, dem_nd_other_d_coor, dem_d_other_nd_coor):
        # https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/
        # vector.html#writing-vector-layers
        # define fields for feature attributes. A QgsFields object is needed
        fields = QgsFields()
        fields.append(QgsField("id", QVariant.Int))
        fields.append(QgsField("cause", QVariant.String))
        fields.append(QgsField("x_coor", QVariant.String))
        fields.append(QgsField("y_coor", QVariant.String))

        """ create an instance of vector file writer, which will create
        the vector file.
        Arguments:
        1. path to new file (will fail if exists already)
        2. encoding of the attributes
        3. field map
        4. geometry type - from WKBTYPE enum
        5. layer's spatial reference (instance of
           QgsCoordinateReferenceSystem) - optional
        6. driver name for the output file """

        self.shape_path = '/home/renier.kramer/Desktop/my_shapes24.shp'

        writer = QgsVectorFileWriter(self.shape_path, "CP1250", fields,
                                     QGis.WKBPoint, None, "ESRI Shapefile")

        if writer.hasError() != QgsVectorFileWriter.NoError:
            print("Error when creating shapefile: ", writer.errorMessage())

        source_epsg = 28992
        source_crs = QgsCoordinateReferenceSystem(int(source_epsg))
        dest_crs = QgsCoordinateReferenceSystem(28992)
        transform = QgsCoordinateTransform(source_crs, dest_crs)

        for idx, point in enumerate(dem_nd_other_d_coor):
            feat = QgsFeature()
            point_x = point[0]
            point_y = point[1]
            feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(point_x, point_y)))
            feat.setAttributes([idx, 'dem_nodata', point_x, point_y])
            writer.addFeature(feat)
        for idx, point in enumerate(dem_d_other_nd_coor):
            feat = QgsFeature()
            point_x = point[0]
            point_y = point[1]
            feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(point_x, point_y)))
            feat.setAttributes([idx, 'dem_data', point_x, point_y])
            writer.addFeature(feat)

        # delete the writer to flush features to disk
        del writer

    def pop_up_finished(self):
            pop_up_info("Raster checker is finished. "
                        "Check results written to: \n"
                        "{0}"
                        "Wrong pixels written to: \n"
                        "{1}".format(str(self.log_path), str(self.shp)))

    def progress_bar(self):
        pass
        # TODO:
        # create progressbar for all checks

    def run(self, checks):
        """
        Run the raster checks
        :param checks:
        :return:
        """
        # """Run the raster checks."""
        self.reset_messages()  # start with no messages

        try:
            self.all_checks()
        except Exception as e:
            msg = "all checks lukt niet jongen"
            log.error(msg)
            log.error(e)

        try:
            self.close_session()
        except Exception as e:
            msg = "session close lukt niet jongen"
            log.error(msg)
            log.error(e)

        try:
            self.create_log()
        except Exception as e:
            msg = "write to log lukt niet jongen"
            log.error(msg)
            log.error(e)

        try:
            list_a = self.dem_nd_other_d_coor
            list_b = self.dem_d_other_nd_coor
            self.create_shp(list_a, list_b)
        except Exception as e:
            msg = "create shp lukt niet jongen"
            log.error(msg)
            log.error(e)

        try:
            self.pop_up_finished()
        except Exception as e:
            msg = "pop up info lukt niet jongen"
            log.error(msg)
            log.error(e)

        if self.messages:
            return " ".join(self.messages)
        else:
            return "no messages"

# foreign_keys = [
#     ('v2_global_settings', 3, 'interflow_settings_id', 1),
#     ('v2_global_settings', 3, 'simple_infiltration_settings_id', 1)
# ]
#
# all_raster_ref = [
#     ('v2_global_settings', 3, 'dem_file', u'rasters/dem_wezep5.tif'),
#     ('v2_global_settings', 3, 'frict_coef_file', u'rasters/
# friction_wezep7.tif'),
#     ('v2_global_settings', 3, 'initial_waterlevel_file', u'rasters/
# ini05.tif')
# ]
#
# entrees_dict = {3: [u'rasters/dem_wezep5.tif',
#                     u'rasters/friction_wezep7.tif',
#                     u'rasters/ini05.tif']
#                 }
#
# for key, value in entrees_dict.iteritems():
#     for rast_item in value:
#         print rast_item

# list comprehension syntax (double for loop in 1 line)
# if you want to avoid multiple for loops below eachother, like this:
# for x_item in x:
#     for y_item in y:
#         if y_item == x_item:
#             dothis
# # you can do that in 1 line, like this:
# [dothis for y_item in y for x_item in x if y_item == x_item]


"""
sqlite_file_path = '/home/renier.kramer/Desktop/wezep/wezep2.sqlite'
engine = create_engine('sqlite:///{0}'.format(sqlite_file_path), echo=False)
echo=False will disable all the SQL logging
metadata = MetaData(bind=engine)
# 1.  __init__
db = ThreediDatabase({'db_path': u'/home/renier.kramer/Desktop/wezep/
wezep2.sqlite'}, 'spatialite')
session = db.get_session()
# 2. reset_messages
messages = []
# now we can do:
datamodel = DataModelSource()
# to get all data from v2_weir, just do:
datamodel.v2_weir
# to get column names from v2_weir, just do:
datamodel.v2_weir.columns.keys()
# get all columns with content from 1 table
q = select([datamodel.v2_weir])
# with getattr this becomes
tbl = 'v2_weir'
q = select([getattr(datamodel,tbl)])
result = session.execute(q)
for row in result:
    print row
# do you want the column names of result?
result.keys
# get 1 column with content from 1 table
q = select([datamodel.v2_weir.c.id])
# with getattr this becomes
tbl = 'v2_weir'
q = select([getattr(datamodel,tbl).c.id])
result = session.execute(q)
for row in result:
    print row
# get the integers right away:
for row in result:
    print row['id']
# do you want the column names of result?
result.keys()
# get 1 column with content from 1 table (more sophistic)
tbl = 'v2_global_settings'
column = 'frict_coef_file'
get_table = getattr(datamodel, tbl).c
get_column = getattr(get_table, column)
q = select([get_column])
res = session.execute(q)
for row in res:
    print row[column]
# select 2 columns from 1 table
q = select([datamodel.v2_weir.c.id, datamodel.v2_weir.c.crest_level])
res = session.execute(q)
res = session.execute(q)
for row in res:
    print row['id']
    print row['crest_level']
# select 2 columns from 1 table (more sophistic)
tbl = 'v2_global_settings'
column = 'frict_coef_file'
get_table = getattr(datamodel, tbl).c
get_column = getattr(get_table, column)
q = select([get_column, get_table.id])
res = session.execute(q)
for row in res:
    print row['id']
    print row[column]
# filter out the special methods by using a list comprehension
[a for a in dir(datamodel) if not a.startswith('__')]
# filter out the methods, you can use the builtin callable as a check.
[a for a in dir(datamodel) if not a.startswith('__') and not callable(
getattr(datamodel,a))]
# all tables from the datamodel
for tbl in [a for a in dir(datamodel) if a.startswith('v2_')]:
    print tbl
"""