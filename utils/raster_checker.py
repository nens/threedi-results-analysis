# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

from sqlalchemy import (Table, MetaData, select)

from ThreeDiToolbox.utils.threedi_database import ThreediDatabase
from ThreeDiToolbox.utils.user_messages import (
    pop_up_info, messagebar_message)
from sqlalchemy.ext.declarative import declarative_base
import time
import os
import string
import logging
import osr
from gdal import GA_ReadOnly
from osgeo import gdal, osr
import numpy as np
from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsFields, QgsField, QgsVectorFileWriter, QGis,
                       QgsFeature, QgsGeometry, QgsPoint,
                       QgsCoordinateReferenceSystem, QgsCoordinateTransform)
from itertools import (izip, chain)

log = logging.getLogger(__name__)
Base = declarative_base()

"""
Module that checks the rasters of a threedi model on multiple requirements:
1: Does the model entree refer to at least one raster?
2: Do these referenced rasters exists?
3: Is the raster filename valid?
4: Is the raster single band?
5: Is the nodata value -9999?
6: Does raster have UTM projection (unit in meters)?
7: Is the data type float 32?
8: Is the raster compressed (compression=deflate)?
9: Are the pixels square?
10: No extreme pixel values?
11: Cumulative pixel count of all rasters in one model entree < 1 billion?
12: Is the projection equal to the dem projection?
13: Is the pixel size equal to the dem pixel size?
14: Is the number of data/nodata pixels equal to the dem?
15: Is the number of rows-colums equal to the dem?
16: Are pixels correctly aligned when comparing the dem with another raster?
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
    ['v2_simple_infiltration', 'simple_infiltration_setting_id'],
    ['v2_groundwater', 'groundwater_setting_id'],
    ['v2_interflow', 'interflow_setting_id']
]

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

    def init_messages(self):
        """enters some (general) explaining lines."""
        msg = '-- Intro: --\n' \
              'The RasterChecker checks your rasters based on the raster ' \
              'references in your sqlite. \n' \
              'This is done per v2_global_settings id (model entree). \n' \
              'The following checks are executed: \n\n' \
              '-- Per individual raster: -- \n' \
              'check 1: Does the model entree refer to at least one raster?\n' \
              'check 2: Do these referenced rasters exists? \n' \
              'check 3: Is the raster filename valid? \n' \
              'check 4: Is the raster single band? \n' \
              'check 5: Is the nodata value -9999? \n' \
              'check 6: Does raster have UTM projection (unit in meters)? \n' \
              'check 7: Is the data type float 32? \n' \
              'check 8: Is the raster compressed? (compression=deflate) \n' \
              'check 9: Are the pixels square? \n' \
              'check 10: No extreme pixel values? (dem: -10kmMSL<x<10kmMSL,'\
              ' other rasters: 0<x<10k) \n\n' \
              '-- Raster comparison: -- \n' \
              'check 11: Is the cumulative pixel count of all rasters in one ' \
              'model entree < 1 billion? \n' \
              'check 12: Is the projection equal to the dem projection? \n' \
              'check 13: Is the pixel size equal to the dem pixel size? \n' \
              'check 14: Is the number of data/nodata pixels equal to the '\
              'dem? \n' \
              'check 15: Is the number of rows-colums equal to the dem? \n\n' \
              '-- Pixel comparison: -- \n' \
              'check 16: Are pixels correctly aligned when comparing the ' \
              'dem with another raster: ?\n\n ' \
              '-- Report: --\n'
        self.messages.append("{}".format(msg))

    def close_session(self):
        try:
            self.session.close()
        except Exception as e:
            log.error(e)

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

    def get_unique_setting_ids(self, ds):
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

    def get_entrees(self, all_raster_ref, foreign_keys):
        """
        group raster_ref per model_entree_id
        :param all_raster_ref:
        :param foreign_keys:
        :return: entree_dict: a dictionary with
            - keys = global_setting_id
            - values = list with raster reference ['test1.tif, test2.tif]
        """
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
                msg = 'entree id %d does not (but must) include an elevation' \
                      ' raster' % entree_id
                self.messages.append("[Error]: {}. \n".format(msg))
                del entrees_dict[entree_id]

        # Change order of entrees.value() (=list of raster_path strings), so
        # that the dem_raster is on the first index. The dem is the leading
        # model raster when comparing two rasters
        for setting_id, rasters in entrees_dict.iteritems():
            dem = self.get_dem_per_entree(
                entrees_dict, setting_id, all_raster_ref)
            dem_index = rasters.index(dem)
            if dem_index <> 0:
                rasters[0], rasters[dem_index] = rasters[dem_index], rasters[0]
        return entrees_dict

    def get_dem_per_entree(self, entrees, entree_id, all_raster_ref):
        for entree_id_item, rasters in entrees.iteritems():
            if entree_id_item == entree_id:
                for raster in rasters:
                    for item in all_raster_ref:
                        if raster == item[3] and item[2] == 'dem_file':
                            dem_per_entree = raster
            return dem_per_entree

    def _iter_block_row(self, band, offset_y, block_height, block_width,
                        no_data_value):
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
            arr = band.ReadAsArray(i * block_width, offset_y, width,
                                   block_height)
            # if no_data_value is not None:
            #     arr[arr == no_data_value] = -9999.
            # idx_nodata = np.argwhere(arr == no_data_value)
            yield (ncols * block_width, offset_y, ncols * block_width + width,
                   offset_y + block_height), arr
            # offset_y + block_height), arr

    def iter_blocks(self, band, block_width=0, block_height=0):
        """ Iterate over native blocks in a GDal raster data band.
        Optionally, provide a minimum block dimension.
        Returns a tuple of bbox (x1, y1, x2, y2) and the data as ndarray. """
        nrows = int(band.YSize / block_height)
        no_data_value = band.GetNoDataValue()
        for j in range(nrows):
            for block in self._iter_block_row(band, j * block_height,
                                              block_height, block_width,
                                              no_data_value):
                yield block
        # possible leftover row
        height = band.YSize - (nrows * block_height)
        if height > 0:
            for block in self._iter_block_row(band, nrows * block_height,
                                              height, block_width,
                                              no_data_value):
                yield block

    def optimize_blocksize(self, band, min_blocksize=256, max_blocksize=256):
        raster_height = band.YSize
        raster_width = band.XSize
        block_height, block_width = band.GetBlockSize()

        # optimize block_width
        if block_width <= min_blocksize <= raster_width:
            block_width = min_blocksize
        # in case of very small rasters
        elif block_width <= min_blocksize:
            block_width = raster_width
        # avoid too big blocks
        elif block_width >= max_blocksize:
            block_width = max_blocksize

        # optimize block_height
        if block_height <= min_blocksize <= raster_height:
            block_height = min_blocksize
        # in case of very small rasters
        elif block_height <= min_blocksize:
            block_height = raster_height
        # avoid too big blocks
        elif block_height >= max_blocksize:
            block_height = max_blocksize

        block_area = block_height * block_width
        raster_area = raster_width * raster_height
        nr_blocks = raster_area / block_area
        return block_width, block_height, nr_blocks

    def count_data_nodata(self, src_ds):
        band = src_ds.GetRasterBand(1)
        src_ds = None
        w, h, nr_blocks = self.optimize_blocksize(band)
        raster_generator = self.iter_blocks(band, block_width=w, block_height=h)
        count_data = 0
        count_nodata = 0
        nodata_value = -9999
        for data in raster_generator:
            bbox, arr = data
            total_size = arr.size
            add_cnt_nodata = np.count_nonzero(arr == nodata_value)
            arr = None
            add_cnt_data = (total_size - add_cnt_nodata)
            count_nodata += add_cnt_nodata
            count_data += add_cnt_data
        return count_data, count_nodata

    def check1_entrees(self, setting_id, rasters):
        """
        check 1. does a global settings entrees exists with references
        to raster(s)?
        :param entrees:
        :return:
        """
        check_entrees = []
        if setting_id and rasters:
            msg = 'raster checker will check v2_global_settings id %d that ' \
                  'includes rasters: %s' % (setting_id, str(rasters))
            self.messages.append("[Info]: {}. \n".format(msg))
            check_entrees.append(True)
        elif rasters is None:
            msg = 'no raster references found for v2_global_settings id ' \
                  '%d \n' % setting_id
            self.messages.append("[Warning]: {}. \n".format(msg))
            check_entrees.append(False)

        if all(check_entrees):
            return True
        else:
            return False

    def check2_tif_exists(self, setting_id, rasters):
        """
        check 2. does the raster (reference from the model) really exists?
        :param entrees:
        :return:
        """
        check_tif_exists = []
        for rast_item in rasters:
            raster_path = os.path.join(self.sqlite_dir, rast_item)
            if os.path.isfile(raster_path):
                check_tif_exists.append(True)
                msg = 'raster %s found for global settings id %d' \
                      % (raster_path, setting_id)
                self.messages.append("[Info]: {}. \n".format(msg))
            else:
                check_tif_exists.append(False)
                msg = 'raster %s not found for global settings id %d. Please' \
                      ' check the reference' % (raster_path, setting_id)
                self.messages.append("[Error]: {}. \n".format(msg))

        if all(check_tif_exists):
            return True
        else:
            return False

    def check3_tif_filename(self, setting_id, rasters):
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

        for rast_item in rasters:
            if not (rast_item[-4:] == '.tif' or rast_item[-5:] == '.tiff'):
                msg = "exetension of raster %s must be  .tif or .tiff" \
                      % rast_item
                self.messages.append("[Error]: {}. \n".format(msg))
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
                self.messages.append("[Error]: {}. \n".format(msg))
            msg = 'Invalid filename, please remove the special chars: ' + str(
                invalid_chars_in_filename)
            self.messages.append("[Error]: {}. \n".format(msg))

        if all(check_tif_filename):
            msg = 'all rasters for v2_global_settings id %d have valid ' \
                  'filenames' % setting_id
            self.messages.append("[Info]: {}. \n".format(msg))
            return True
        else:
            return False

    def check4_singleband(self, src_ds, rast_item):
        # check4. is the raster singleband ?
        try:
            cnt_rasterband = src_ds.RasterCount
            if cnt_rasterband != 1:
                msg = 'raster %s is not (but must be) a single-band raster' \
                      % rast_item
                self.messages.append("[Error]: {}. \n".format(msg))
                return False
            elif cnt_rasterband == 1:
                return True
        except Exception as e:
            log.error(e)
            msg = 'unable to get raster bands of raster %s' % rast_item
            self.messages.append("[Warning]: {}. \n".format(msg))
            return False

    def check5_nodata(self, src_ds, rast_item):
        # check5. is the raster nodata -9999 ?
        try:
            srcband = src_ds.GetRasterBand(1)
            nodata = srcband.GetNoDataValue()
            if nodata == -9999:
                return True
            else:
                msg = 'no_data value of raster %s is %s, but must be -9999' \
                      % (rast_item, str(nodata))
                self.messages.append("[Error]: {}. \n".format(msg))
                return False
        except Exception as e:
            log.error(e)
            return False

    def check6_utm(self, src_ds, rast_item):
        # check 6 is the raster projection in meters ?
        try:
            proj = src_ds.GetProjection()
            spat_ref = osr.SpatialReference()
            spat_ref.ImportFromWkt(proj)
            unit = spat_ref.GetLinearUnitsName()
            if unit == 'metre':
                return True
            elif unit == 'degree':
                msg = 'projection raster %s has unit degree, but must be in ' \
                      'meters. Please us UTM projection' % rast_item
                self.messages.append("[Error]: {}. \n".format(msg))
                return False
        except Exception as e:
            log.error(e)
            return False

    def check7_flt32(self, src_ds, rast_item):
        # check 7 is the raster datatype float32 ?
        try:
            srcband = src_ds.GetRasterBand(1)
            data_type = srcband.DataType
            data_type_name = gdal.GetDataTypeName(data_type)
            if data_type_name == 'Float32':
                return True
            else:
                msg = 'datatype raster %s is not (but must be) float_32' \
                      % rast_item
                self.messages.append("[Error]: {}. \n".format(msg))
                return False
        except Exception as e:
            log.error(e)
            return False

    def check8_compress(self, src_ds, rast_item):
        # check 8 is the raster compressed ?
        try:
            compr_method = src_ds.GetMetadata('IMAGE_STRUCTURE')[
                'COMPRESSION']
            if compr_method == 'DEFLATE':
                return True
            else:
                msg = "raster %s is not (but should be) compressed " \
                      "please use gdal_translate -co " \
                      "'COMPRESS=DEFLATE'" % rast_item
                self.messages.append("[Error]: {}. \n".format(msg))
                return False
        except Exception as e:
            msg = 'unable to get compression method for raster %s' % rast_item
            self.messages.append("[Waring]: {}. \n".format(msg))
            log.error(e)
            return False

    def check9_square_pixel(self, src_ds, rast_item):
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
                msg = 'raster %s has a pixel resolution with more than ' \
                      'three decimals' % rast_item
                self.messages.append("[Warning]: {}. \n".format(msg))
            if xres == yres:
                return True
            else:
                return False
        except Exception as e:
            msg = 'unable to get pixel resolution for raster %s' \
                  % rast_item
            self.messages.append("[Error]: {}. \n".format(msg))
            log.error(e)
            return False

    def check10_extreme_value(self, src_ds, rast_item):
        # check 10 are there no extreme values?
        srcband = src_ds.GetRasterBand(1)
        stats = srcband.GetStatistics(True, True)
        min = stats[0]
        max = stats[1]
        min_allow = -10000
        max_allow = 10000
        if min_allow < min < max_allow and min_allow < max < max_allow:
            return True
        else:
            msg = 'raster %s has a an extreme minimum: %d or maximum: %d' \
                  % (rast_item, min, max)
            self.messages.append("[Warning]: {}. \n".format(msg))
            return False

    def check11_cum_pixel_cnt(self, cols, rows, setting_id):
        """
        check11: cummulative pixel count
        :param cols: (int)
        :param rows: (int)
        :param setting_id: (int)
        :return: updates list: check11_cum_pixel_cnt_list
        """
        max_pixels_allow = 1000000000  # 1 billion for all rasters 1 entree
        pixelcount = cols * rows
        cum_pixelcount =+ pixelcount
        if cum_pixelcount > max_pixels_allow:
            msg = 'setting_id %d: all rasters together have %d pixels. ' \
                  'This is probably more than 3Di can handle: %d ' \
                  'pixels' % (setting_id, pixelcount, max_pixels_allow)
            self.messages.append("[Warning]: {}. \n".format(msg))
            return False
        else:
            return True

    def check12_proj(self, *args):
        """
        check12: compare projection of dem with another raster
        :param args: dem_projcs (str), projcs (str), setting_id (int),
        dem (unicode), rast_item (unicode)
        :return: updates list: check12_proj_list
        """
        (dem_projcs, projcs, setting_id, dem, rast_item) = args
        if dem_projcs == projcs:
            return True
        else:
            msg = 'setting_id %d: raster %s has projection= %s, ' \
                  'while raster %s has projection %s (must be equal)'\
                  %(setting_id, dem, dem_projcs, rast_item, projcs)
            self.messages.append("[Error]: {}. \n".format(msg))
            return False

    def check13_pixelsize(self, *args):
        """
        check13: compare pixelsize of dem with another raster
        :param args: dem_xres (float), dem_yres (float), xres (float),
        yres (float), setting_id (int), dem (unicode), rast_item (unicode)
        :return: updates list: check13_pixelsize_list
        """
        (dem_xres, dem_yres, xres, yres, setting_id, dem, rast_item) = args
        if (dem_xres, dem_yres) == (xres, yres):
            return True
        else:
            msg = 'setting_id %d: raster %s has pixelsize= %s, while raster ' \
                  '%s has pixelsize %s (must be equal)' % (
                setting_id, dem, (dem_xres, dem_yres), rast_item, (xres, yres))
            self.messages.append("[Error]: {}. \n".format(msg))
            return False

    def check14_cnt_nodata(self, *args):
        """
        check14: compare data/nodata count of dem with another raster
        :param args: dem_cnt_data (int), dem_cnt_nodata (int), cnt_data (int),
        cnt_nodata (int), setting_id (int), dem (unicode), rast_item (unicode)
        :return: updates list: check13_pixelsize_list
        """
        (dem_cnt_data, dem_cnt_nodata, cnt_data, cnt_nodata, setting_id,
         dem, rast_item) = args
        if (dem_cnt_data, dem_cnt_nodata) == (cnt_data, cnt_nodata):
            return True
        else:
            msg = 'setting_id %d: raster %s has %d data pixels ' \
                  'and %d nodata pixels, while raster %s has %d data ' \
                  'pixels and %d nodata pixels' \
                  % (setting_id, dem, dem_cnt_data, dem_cnt_nodata,
                     rast_item, cnt_data, cnt_nodata)
            self.messages.append("[Error]: {}. \n".format(msg))
            return False

    def check15_ext(self, *args):
        """
        check15: compare extent (number rows/colums) of dem with another raster
        :param args: dem_cols (int), dem_rows (int), cols (int), rows (int),
        setting_id (int), dem (unicode), rast_item (unicode)
        :return: updates list: check15_ext_list
        """
        (dem_cols, dem_rows, cols, rows, setting_id, dem, rast_item) = args
        if (dem_cols, dem_rows) == (cols, rows):
            return True
        else:
            msg = 'setting_id %d: raster %s has %s colums-rows, ' \
                  'while raster %s has %s colums-rows (must be equal)' \
                  % (setting_id, dem, (dem_cols, dem_rows), rast_item,
                     (cols, rows))
            self.messages.append("[Error]: {}. \n".format(msg))
            return False

    def check16_pixel_aligned(self, setting_id, rasters):

        # TODO: No need to check a raster multiple times...
        # if this is the case then 1 (or more) raster(s) have been refered
        # multiple times. No need to check a raster multiple times...

        dem = rasters[0]
        dem_path = os.path.join(self.sqlite_dir, dem)
        generator_dem = self.create_generator(dem_path)
        self.pixel_specs = self.get_pixel_specs(dem_path)

        for other_tif in rasters[1:]:
            other_tif_path = os.path.join(self.sqlite_dir, other_tif)
            generator_other = self.create_generator(other_tif_path)

            for data1, data2 in izip(
                    generator_dem.next(), generator_other.next()):

                self.check_pixel(setting_id, other_tif, data1, data2)

    def run_checks1_to_3(self, setting_id, rasters):
        """ Check raster on multiple aspects (1 to 3)
        :param setting_id: int
        :param rasters: list
        :return: updates id_track_1_3 with setting_id if checks succeeds
        """
        check1 = self.check1_entrees(setting_id, rasters)
        check2 = self.check2_tif_exists(setting_id, rasters)
        check3 = self.check3_tif_filename(setting_id, rasters)

        if all([check1, check2, check3]):
            msg = 'check 1 to 3 succeeded for v2_global_settings id ' \
                  '%d. Successive checks for this id will be executed' \
                  % setting_id
            self.messages.append("[Info]: {}. \n".format(msg))
            self.id_track_1_3.append(setting_id)
        else:
            msg = 'check 1 to 3 did not succeed for v2_global_settings ' \
                  'id %d. Therefore, successive checks for this id ' \
                  'can not be executed. ' \
                  'Please fix and try again' % setting_id
            self.messages.append("[Error]: {}. \n".format(msg))
            return False

    def run_checks4_to_10(self, setting_id, rasters):
        """ Check raster on multiple aspects (4 to 10)
        This method calls 7 checks so that the raster has to be opened
        and closed only 1 time per raster
        :param setting_id: int
        :param rasters: list
        :return: updates id_track_4_10 with setting_id (int) if checks succes
        for that setting id
        """

        setting_id_track = []

        for rast_item in rasters:
            raster_path = os.path.join(self.sqlite_dir, rast_item)
            src_ds = gdal.Open(raster_path, GA_ReadOnly)
            check4 = self.check4_singleband(src_ds, rast_item)
            check5 = self.check5_nodata(src_ds, rast_item)
            check6 = self.check6_utm(src_ds, rast_item)
            check7 = self.check7_flt32(src_ds, rast_item)
            check8 = self.check8_compress(src_ds, rast_item)
            check9 = self.check9_square_pixel(src_ds, rast_item)
            check10 = self.check10_extreme_value(src_ds, rast_item)
            # close raster dataset
            src_ds = None

            # check per raster
            if all([check4, check5, check6, check7, check8, check9, check10]):
                msg = 'check 4 to 10 succeeded for v2_global_settings id ' \
                  '%d raster %s' % (setting_id, rast_item)
                self.messages.append("[Info]: {}. \n".format(msg))
                setting_id_track.append(True)
            else:
                msg = 'check 4 to 10 did not succeed for v2_global_settings ' \
                      'id %d raster %s' % (setting_id, rast_item)
                self.messages.append("[Error]: {}. \n".format(msg))
                setting_id_track.append(False)

        # check per setting_id
        if all(setting_id_track):
            msg = 'check 4 to 10 succeeded for all rasters in ' \
                  'v2_global_settings id %d. Successive checks for this id ' \
                  'will be executed' % setting_id
            self.messages.append("[Info]: {}. \n".format(msg))
            self.id_track_4_10.append(setting_id)
        else:
            msg = 'check 4 to 10 did not succeed for all rasters in ' \
                  'v2_global_settings id %d. Therefore, successive checks ' \
                  'for this id can not be executed. ' \
                  'Please fix and try again' % setting_id
            self.messages.append("[Error]: {}. \n".format(msg))

    def run_checks11_to_15(self, setting_id, rasters):
        """ a simple raster comparence. Function compares multiple rasters
        within 1 model entree:
        - 11: Is the cummulative pixelcount of all rasters < 1 billion?
        - 12-15: Is the projection, pixelsize, extent, nodata/data count of all
          rasters consistent?
        :param setting_id: int
        :param rasters: list
        :return: updates id_track_4_10 with setting_id if checks succeeds
        """

        dem = rasters[0]
        dem_path = os.path.join(self.sqlite_dir, dem)
        dem_src_ds = gdal.Open(dem_path, GA_ReadOnly)
        dem_ext = dem_src_ds.GetGeoTransform()
        dem_ulx, dem_xres, dem_xskew, dem_uly, dem_yskew, dem_yres = dem_ext

        dem_cols = dem_src_ds.RasterXSize
        dem_rows = dem_src_ds.RasterYSize
        self.check11_cum_pixel_cnt(dem_cols, dem_rows, setting_id)

        dem_src_srs = osr.SpatialReference()
        dem_src_srs.ImportFromWkt(dem_src_ds.GetProjection())
        dem_cnt_data, dem_cnt_nodata = self.count_data_nodata(dem_src_ds)
        dem_projcs = dem_src_srs.GetAttrValue('projcs')
        dem_src_ds = None

        setting_id_11_13_track = []
        setting_id_14_15_track = []

        for rast_item in rasters[1:]:
            path = os.path.join(self.sqlite_dir, rast_item)
            src_ds = gdal.Open(path, GA_ReadOnly)
            ext = src_ds.GetGeoTransform()
            ulx, xres, xskew, uly, yskew, yres = ext
            cols = src_ds.RasterXSize
            rows = src_ds.RasterYSize
            src_srs = osr.SpatialReference()
            src_srs.ImportFromWkt(src_ds.GetProjection())
            cnt_data, cnt_nodata = self.count_data_nodata(src_ds)
            projcs = src_srs.GetAttrValue('projcs')
            src_ds = None

            check11 = self.check11_cum_pixel_cnt(cols, rows, setting_id)

            args = dem_projcs, projcs, setting_id, dem, rast_item
            check12 = self.check12_proj(*args)

            args = dem_xres, dem_yres, xres, yres, setting_id, dem, rast_item
            check13 = self.check13_pixelsize(*args)

            args = dem_cnt_data, dem_cnt_nodata, cnt_data, cnt_nodata, \
                   setting_id, dem, rast_item
            check14 = self.check14_cnt_nodata(*args)

            args = dem_cols, dem_rows, cols, rows, setting_id, dem, rast_item
            check15 = self.check15_ext(*args)

            # check (11, 12, 13) per raster
            if all([check11, check12, check13]):
                msg = 'check 11 to 13 succeeded for v2_global_settings id ' \
                      '%d raster %s' % (setting_id, rast_item)
                self.messages.append("[Info]: {}. \n".format(msg))
                setting_id_11_13_track.append(True)
            else:
                msg = 'check 11 to 13 did not succeed for v2_global_settings' \
                      ' id %d raster %s' % (setting_id, rast_item)
                self.messages.append("[Error]: {}. \n".format(msg))
                setting_id_11_13_track.append(False)

            # check (14, 15) per raster
            if all([check14, check15]):
                msg = 'check 14 and 15 succeeded for v2_global_settings id ' \
                      '%d raster %s' % (setting_id, rast_item)
                self.messages.append("[Info]: {}. \n".format(msg))
                setting_id_14_15_track.append(True)
            else:
                msg = 'check 14 and 15 did not succeed for v2_global_settings' \
                      ' id %d raster %s' % (setting_id, rast_item)
                self.messages.append("[Error]: {}. \n".format(msg))
                setting_id_14_15_track.append(False)

        # check (11, 12 and 13) per setting_id
        if all(setting_id_11_13_track):
            msg = 'check 11 to 13 succeeded for v2_global_settings id %d. ' \
                  'Pixel check (if selected by user) can be executed for ' \
                  'this id' % setting_id
            self.messages.append("[Info]: {}. \n".format(msg))
            self.id_track_11_13.append(setting_id)
        else:
            msg = 'check 11 to 13 did not succeed for v2_global_settings id ' \
                  '%d. Pixel check (if selected by user) can not be executed ' \
                  'for this id. Please fix and try again' % setting_id
            self.messages.append("[Error]: {}. \n".format(msg))

        # check (14 and 15) per setting_id
        if all(setting_id_14_15_track):
            msg = 'check 14 and 15 succeeded for v2_global_settings id %d. ' \
                  'Therefore, pixel check (if selected by user) is not ' \
                  'needed and will be skipped' % setting_id
            self.messages.append("[Info]: {}. \n".format(msg))
        else:
            msg = 'check 14 and 15 did not succeed for v2_global_settings id ' \
                  '%d. Pixel check (if selected by user) will be executed ' \
                  'for this id' % setting_id
            self.messages.append("[Error]: {}. \n".format(msg))
            # append settings id. Pixel Checker can only run for these ids
            self.id_track_14_15.append(setting_id)

    def get_entrees_to_check(self):
        """
        :return: entrees_to_check (dict) with
        keys = setting_id (int)
        values = rasters (list of strings)
        e.g. [(1, [u'rasters/test1.tif', u'rasters/test2.tif'])]
        """
        all_raster_ref = self.get_all_raster_ref()  # called only here
        foreign_keys = self.get_foreign_keys()  # called only here
        entrees = self.get_entrees(all_raster_ref, foreign_keys)

        entrees_to_check = {}
        for setting_id, rasters in entrees.iteritems():
            if len(rasters) < 2:
                msg = 'setting_id %d: no pixels to compare for this ' \
                      'v2_global_settings id as only one raster is ' \
                      'used in this id' % setting_id
                self.messages.append("[Warning]: {}. \n".format(msg))
            elif setting_id in self.id_track_14_15:
                msg = 'setting_id %d: we skip the pixel check for this ' \
                      'setting_id as checks 14 and 15 succeeded for ' \
                      'this setting_id' % setting_id
                self.messages.append("[Info]: {}. \n".format(msg))
            elif setting_id in self.id_track_11_13:
                    msg = 'setting_id %d: pixel check will be done for ' \
                          'this setting_id as checks 1 to 13 succeeded for ' \
                          'this setting_id' % setting_id
                    self.messages.append("[Info]: {}. \n".format(msg))
                    entrees_to_check[setting_id] = rasters
            else:
                msg = 'setting_id %d: we skip the pixel check for this ' \
                      'setting_id as checks 1 to 13 did not ' \
                      'succeed' % setting_id
                self.messages.append("[Warning]: {}. \n".format(msg))
        return entrees_to_check

    def create_generator(self, raster_path):
        raster = gdal.Open(raster_path, GA_ReadOnly)
        band = raster.GetRasterBand(1)

        # optimize_blocksize
        w, h, nr_blocks = self.optimize_blocksize(band)

        # create generators
        while True:
            yield self.iter_blocks(band, block_width=w, block_height=h)

    def get_pixel_specs(self, dem_path):
        dem = gdal.Open(dem_path, GA_ReadOnly)
        ulx, xres, xskew, uly, yskew, yres = dem.GetGeoTransform()
        pixelsize = abs(min(xres, yres))
        dem = None
        pixel_specs = (ulx, xres, xskew, uly, yskew, yres, pixelsize)
        return pixel_specs

    def get_wrong_pixel(self, setting_id, other_tif, bbox1, compare_mask):
        wrong_pixels = []
        ulx, xres, xskew, uly, yskew, yres, pixelsize = self.pixel_specs

        # (0,0) is (x,y) left-upper corner of first bbox. Going down
        # bbox_row increases. Going right bbox_col increases
        l_up_col = bbox1[0]
        l_up_row = bbox1[1]
        # r_down_col = bbox1[2]
        # r_down_row = bbox1[3]

        # get indices of True
        true_idx = np.where(compare_mask)
        x_coords = true_idx[0]
        y_coords = true_idx[1]
        # (array([1, 1, 2, 2]), array([2, 3, 0, 1]))
        for pixel in zip(x_coords, y_coords):
            bbox_row = pixel[0]
            bbox_column = pixel[1]
            loc_col = l_up_col + bbox_column
            loc_row = l_up_row + bbox_row
            # times 0.5 because we want centre coord and not left up corner
            x_coor = ulx + pixelsize * loc_col + 0.5 * pixelsize
            y_coor = uly - pixelsize * loc_row - 0.5 * pixelsize
            wrong_pixels.append([x_coor, y_coor])

        # create row in .shp for dem nodata where other raster is data
        self.input_data_shp.append(
            {'setting_id': setting_id,
             'cause': 'dem_nodata',
             'raster': str(other_tif),
             'coords': wrong_pixels
             }
        )

    def check_pixel(self, setting_id, other_tif, data1, data2):
        bbox1, arr1 = data1
        data1 = None
        bbox2, arr2 = data2
        data2 = None

        # create masks (without data fill_value, but only mask)
        mask1 = (arr1[:] == -9999.)
        mask2 = (arr2[:] == -9999.)

        # xor gives array with trues for wrong pixels
        compare_mask = np.logical_xor(mask1, mask2)
        mask1 = None
        mask2 = None

        # is there any True in the compare mask? then there is at least
        # one wrong pixel
        if np.any(compare_mask):
            self.get_wrong_pixel(setting_id, other_tif, bbox1, compare_mask)

    def run_all_checks(self, run_pixel_checker=False):

        self.id_track_1_3 = []
        self.id_track_4_10 = []
        self.id_track_11_13 = []
        self.id_track_14_15 = []

        all_raster_ref = self.get_all_raster_ref()  # called only here
        foreign_keys = self.get_foreign_keys()  # called only here
        entrees = self.get_entrees(all_raster_ref, foreign_keys)

        # check 1 - 3
        for setting_id, rasters in entrees.iteritems():
            self.run_checks1_to_3(setting_id, rasters)

        # check 4 - 10
        for setting_id, rasters in entrees.iteritems():
            if setting_id in self.id_track_1_3:
                self.run_checks4_to_10(setting_id, rasters)

        # check 11 - 15
        for setting_id, rasters in entrees.iteritems():
            if setting_id in self.id_track_4_10:
                if len(rasters) < 2:
                    msg = 'no rasters to compare for v2_global_settings id ' \
                          '%d as only one raster is used' % setting_id
                    self.messages.append("[Warning]: {}. \n".format(msg))
                else:
                    # check 11 to 15
                    self.run_checks11_to_15(setting_id, rasters)

        # check 16
        if run_pixel_checker:
            for setting_id, rasters in entrees.iteritems():
                if setting_id in self.id_track_14_15:
                    self.input_data_shp = []
                    self.check16_pixel_aligned(setting_id, rasters)

    def create_log(self):
        timestr = time.strftime("_%Y%m%d_%H%M%S")
        log_with_ext = self.sqltname_without_ext + timestr + '.log'
        self.log_path = os.path.join(self.sqlite_dir, log_with_ext)
        # write to log
        try:
            log_file = open(self.log_path, 'w')
            for message_row in self.messages:
                log_file.write(message_row)
            log_file.close()
        except Exception as e:
            log.error(e)

    def create_shp(self):
        # https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/
        # vector.html#writing-vector-layers
        # define fields for feature attributes. A QgsFields object is needed
        fields = QgsFields()
        fields.append(QgsField("setting_id", QVariant.String))
        fields.append(QgsField("cause", QVariant.String))
        fields.append(QgsField("raster", QVariant.String))
        fields.append(QgsField("x centre", QVariant.String))
        fields.append(QgsField("y centre", QVariant.String))

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

        # TODO enable transformation (test buitenland modellen!!)
        source_epsg = 28992
        dest_epsg = 28992
        source_crs = QgsCoordinateReferenceSystem(int(source_epsg))
        dest_crs = QgsCoordinateReferenceSystem(int(dest_epsg))
        transform = QgsCoordinateTransform(source_crs, dest_crs)

        self.shape_path = '/home/renier.kramer/Desktop/my_shapes26_' \
                          + str(source_epsg) + '.shp'

        writer = QgsVectorFileWriter(self.shape_path, "CP1250", fields,
                                     QGis.WKBPoint, None, "ESRI Shapefile")

        try:
            if writer.hasError() != QgsVectorFileWriter.NoError:
                msg = 'Error when creating shapefile: ' + \
                      str(writer.errorMessage())
                log.error(msg)
                self.messages.append("[Error]: {}. \n".format(msg))
            else:
                for pixel_check_dict in self.input_data_shp:
                    raster = pixel_check_dict.get('raster')
                    cause = pixel_check_dict.get('cause')
                    setting_id = pixel_check_dict.get('setting_id')
                    coords = pixel_check_dict.get('coords')
                    for point in coords:
                        point_x = point[0]
                        point_y = point[1]
                        feat = QgsFeature()
                        feat.setGeometry(QgsGeometry.fromPoint(
                            QgsPoint(point_x, point_y)))
                        feat.setAttributes([
                            setting_id, cause, raster, point_x, point_y])
                        writer.addFeature(feat)
        except Exception as e:
            log.error(e)
        # delete the writer to flush features to disk
        del writer

    def pop_up_finished(self, logfile=True, shpfile=False):
        header = 'Raster checker is finished'
        if logfile and shpfile:
            msg = 'The check results have been written to: \n %s \n ' \
                  'The coordinates of wrong pixels are written to: \n' \
                  '%s' % (self.log_path, self.shape_path)
        elif logfile:
            msg = 'The check results have been written to: \n %s \n ' \
                  % self.log_path
        else:
            msg = 'no check results have been written, this is not okay'
        pop_up_info(msg, header)

    def progress_bar(self):
        pass
        # TODO: create progressbar for all checks

    def run(self, checks):
        """
        Run the raster checks
        :param checks:
        :return:
        """

        self.reset_messages()  # start with no messages
        self.init_messages()  # enter some (general) explaining lines

        # TODO: now checks are done for all entrees. Enable checks for 1 entree
        if 'check all rasters' in checks:
            if 'check pixels' in checks:
                self.run_all_checks(run_pixel_checker=True)
            else:
                self.run_all_checks(run_pixel_checker=False)

        if 'improve when necessary' in checks:
            pass  # TODO: write improvement function

        self.close_session()
        self.create_log()

        if 'check pixels' in checks:
            self.create_shp()
            self.pop_up_finished(logfile=True, shpfile=True)
        else:
            self.pop_up_finished(logfile=True, shpfile=False)


"""
# example
import numpy as np
a = np.array([True, False, False, True, False, True], dtype=bool)
b = np.array([False, True, True, True, False, False], dtype=bool)
c_and = np.logical_and(a, b)
c_or = np.logical_or(a, b)
c_xor = np.logical_xor(a, b)
print c_and
print c_or
print c_xor
# [False False False  True False False]
# [ True  True  True  True False  True]
# [ True  True  True False False  True]


import numpy as np
import numpy.ma as ma

arr1 = np.array([
    [0., 0., 0., 0.],
    [1., 2., 3., -9999.],
    [5., 6., 7., -9999.],
    [9., -9999., 11., 12.]
])

arr2 = np.array([
    [1., 2., 3., -9999.],
    [5., 6., -9999, 8.],
    [-9999., 10., 11., 12.]
])  

# create masks (with data and mask and fill_value)
# mask1 = ma.masked_values(arr1, -9999.)
# mask2 = ma.masked_values(arr2, -9999.)        

# create masks (without data fill_value, but only mask)
mask1 = (arr1[:] == -9999.)
mask2 = (arr2[:] == -9999.)

# mask1
# array([[False, False, False,  True],
#        [False, False, False,  True],
#        [False,  True, False, False]])

# mask2
# array([[False, False, False,  True],
#        [False, False,  True, False],
#        [ True, False, False, False]])

# xor ("one or the other but not both") geeft een true daar waar pixels 
# fout zijn  
mask1 en mask2 van elkaar verschillen
compare_mask = np.logical_xor(mask1, mask2)

# compare_mask
# array([[False, False, False, False],
#        [False, False,  True,  True],
#        [ True,  True, False, False]])

# daar waar compare_mask = True, daar is een probleem      

# now get indices of true (with np.where or np.argwhere: serveral test 
# with %timeit showed that .where is faster

    # %timeit for pixel in np.argwhere(compare_mask): print pixel
    # 1000 loops, best of 3: 167 µs per loop
    # 
    # %timeit for pixel in zip(np.where(compare_mask)[0], np.where(compare_mask)[1]): print pixel
    # The slowest run took 5.90 times longer than the fastest. 
    # This could mean that an intermediate result is being cached.
    # 10000 loops, best of 3: 21.8 µs per loop


# np.where is faster than np.argwhere, but where output has to be modified..  
true_idx = np.where(compare_mask)
# (array([1, 1, 2, 2]), array([2, 3, 0, 1]))
for pixel in zip(true_idx[0], true_idx[1]):
    print pixel
# (1, 2)
# (1, 3)
# (2, 0)
# (2, 1)
"""





"""
from sqlalchemy import (create_engine, Table, Column, Integer, String, Float,
                        MetaData, Boolean, ForeignKey, select, update)
                        
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
