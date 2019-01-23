# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

from sqlalchemy import MetaData
from ThreeDiToolbox.utils.user_messages import (
    pop_up_info, messagebar_message)
from ThreeDiToolbox.utils.raster_checker_prework import (
    DataModelSource, RasterCheckerEntrees)
from ThreeDiToolbox.utils.constants import RASTER_CHECKER_MAPPER
from ThreeDiToolbox.utils.raster_checker_log import (
    RasterCheckerResults, RasterCheckerProgressBar)

from sqlalchemy.ext.declarative import declarative_base

import os
import string
import logging
import osr
from gdal import GA_ReadOnly
from osgeo import gdal, osr
import numpy as np
from itertools import izip
from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsFields, QgsField, QgsVectorFileWriter, QGis,
                       QgsFeature, QgsGeometry, QgsPoint,
                       QgsCoordinateReferenceSystem, QgsCoordinateTransform)

log = logging.getLogger(__name__)
Base = declarative_base()


class RasterChecker(object):
    def __init__(self, threedi_database):
        self.db = threedi_database
        # session required for SqlAlchemy queries
        self.session = self.db.get_session()
        # datamodel required for dynamic creation of ORM models
        self.engine = self.db.get_engine()
        self.metadata = MetaData(bind=self.engine)

        datamodel = DataModelSource(self.metadata)

        self.entrees = RasterCheckerEntrees(
            datamodel, self.session).get_entrees()

        self.all_raster_ref = RasterCheckerEntrees(
            datamodel, self.session).get_all_raster_ref()

        sqlite_path = str(self.db.settings['db_path'])
        self.sqlite_dir = os.path.split(sqlite_path)[0]
        self.results = RasterCheckerResults(sqlite_path)
        self.check_constants()

    def close_session(self):
        try:
            self.session.close()
        except Exception as e:
            log.error(e)

    def iter_block_row(self, band, offset_y, block_height, block_width,
                        no_data_value):
        ncols = int(band.XSize / block_width)
        for i in range(ncols):
            arr = band.ReadAsArray(i * block_width, offset_y, block_width,
                                   block_height)
            yield (i * block_width, offset_y, (i + 1) * block_width, offset_y +
                   block_height), arr
        # possible leftover block
        width = band.XSize - (ncols * block_width)
        if width > 0:
            arr = band.ReadAsArray(i * block_width, offset_y, width,
                                   block_height)
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
            for block in self.iter_block_row(band, j * block_height,
                                              block_height, block_width,
                                              no_data_value):
                yield block
        # possible leftover row
        height = band.YSize - (nrows * block_height)
        if height > 0:
            for block in self.iter_block_row(band, nrows * block_height,
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
        raster_generator = self.iter_blocks(
            band, block_width=w, block_height=h)
        count_data = 0
        count_nodata = 0
        nodata_value = -9999
        for data in raster_generator:
            bbox, arr = data
            total_size = arr.size
            add_cnt_nodata = np.count_nonzero(arr == nodata_value)
            add_cnt_data = (total_size - add_cnt_nodata)
            count_nodata += add_cnt_nodata
            count_data += add_cnt_data
        return count_data, count_nodata

    def check_tif_exists(self, setting_id, rast_item, check_id):
        # Does the raster (reference from the model) really exists?
        detail = str()
        raster_path = os.path.join(self.sqlite_dir, rast_item)
        if os.path.isfile(raster_path):
            result = True
        else:
            result = False
        self.results._add(setting_id=setting_id, raster=rast_item,
                          check_id=check_id, result=result, detail=detail)

    def check_extension(self, setting_id, rast_item, check_id):
        # exetension of raster must be  .tif or .tiff
        detail = str()
        extension = rast_item.split('.')[-1]
        if extension not in ['tif', 'tiff']:
            result = False
            detail = 'found extension: %s' % extension
        else:
            result = True
        self.results._add(setting_id=setting_id, raster=rast_item,
                          check_id=check_id, result=result, detail=detail)

    def check_filename(self, setting_id, rast_item, check_id):
        # what is the purpose ??
        # TODO: lars suggest to use just 'os' to check its 1 folder deep

        # Does the raster filename have valid chars (also space is not allowed)
        detail = str()
        invalid_chars = set(string.punctuation.replace("_", ""))
        invalid_chars.add(' ')
        invalid_chars_in_filename = []

        # only one '.' and '/' is allowed in relative path
        count_forward_slash = 0
        count_dot = 0
        for char in rast_item:
            if char in invalid_chars:
                if char == '/' and count_forward_slash < 1:
                    count_forward_slash += 1
                elif char == '.' and count_dot < 1:
                    count_dot += 1
                else:
                    invalid_chars_in_filename.append(char)
        if invalid_chars_in_filename:
            result = False
            detail = invalid_chars_in_filename
        else:
            result = True
        self.results._add(setting_id=setting_id, raster=rast_item,
                          check_id=check_id, result=result, detail=detail)

    def check_singleband(self, setting_id, rast_item, check_id, src_ds):
        # Is the raster singleband ?
        detail = str()
        try:
            cnt_rasterband = src_ds.RasterCount
            if cnt_rasterband == 1:
                result = True
            else:
                result = False
                detail = 'found %d rasterbands' % cnt_rasterband
        except Exception as detail:
            log.error(detail)
            result = False
        finally:
            self.results._add(setting_id=setting_id, raster=rast_item,
                              check_id=check_id, result=result, detail=detail)

    def check_nodata(self, setting_id, rast_item, check_id, src_ds):
        # Is the raster nodata -9999 ?
        detail = str()
        try:
            srcband = src_ds.GetRasterBand(1)
            nodata = srcband.GetNoDataValue()
            if nodata == -9999:
                result = True
            else:
                result = False
                detail = 'nodata value is %d' % nodata
        except Exception as detail:
            log.error(detail)
            result = False
        finally:
            self.results._add(setting_id=setting_id, raster=rast_item,
                              check_id=check_id, result=result, detail=detail)

    def check_utm(self, setting_id, rast_item, check_id, src_ds):
        # Is the raster projection in meters ?
        detail = str()
        try:
            proj = src_ds.GetProjection()
            spat_ref = osr.SpatialReference()
            spat_ref.ImportFromWkt(proj)
            unit = spat_ref.GetLinearUnitsName()
            if unit == 'metre':
                result = True
            else:
                result = False
                detail = 'unit is %s' % unit
        except Exception as detail:
            log.error(detail)
            result = False
        finally:
            self.results._add(setting_id=setting_id, raster=rast_item,
                              check_id=check_id, result=result, detail=detail)

    def check_flt32(self, setting_id, rast_item, check_id, src_ds):
        # Is the raster datatype float32 ?
        detail = str()
        try:
            srcband = src_ds.GetRasterBand(1)
            data_type = srcband.DataType
            data_type_name = gdal.GetDataTypeName(data_type)
            if data_type_name == 'Float32':
                result = True
            else:
                result = False
                detail = 'data_type is %s' % data_type_name
        except Exception as detail:
            log.error(detail)
            result = False
        finally:
            self.results._add(setting_id=setting_id, raster=rast_item,
                              check_id=check_id, result=result, detail=detail)

    def check_compress(self, setting_id, rast_item, check_id, src_ds):
        # Is the raster compressed ?
        detail = str()
        try:
            compr_method = src_ds.GetMetadata('IMAGE_STRUCTURE')[
                'COMPRESSION']
            if compr_method == 'DEFLATE':
                result = True
            else:
                result = False
                detail = 'compression_method is %s' %compr_method
        except Exception as detail:
            log.error(detail)
            detail = str()
            result = False
        finally:
            self.results._add(setting_id=setting_id, raster=rast_item,
                              check_id=check_id, result=result, detail=detail)
    def check_pixel_decimal(self, setting_id, rast_item, check_id, src_ds):
        # Has the pixel resolution less than three decimal places?
        detail = str()
        try:
            geotransform = src_ds.GetGeoTransform()
            # horizontal pixel resolution
            xres = abs(geotransform[1])
            cnt_decimal_xres = str(xres)[::-1].find('.')
            # vertical pixel resolution
            yres = abs(geotransform[5])
            cnt_decimal_yres = str(yres)[::-1].find('.')

            if cnt_decimal_xres > 3 or cnt_decimal_yres > 3:
                result = False
                detail = 'found %d and %d decimal places for x- and ' \
                         'y- resolution respectively' % (
                    cnt_decimal_xres, cnt_decimal_yres)
            else:
                result = True
        except Exception as detail:
            log.error(detail)
            result = False
        finally:
            self.results._add(setting_id=setting_id, raster=rast_item,
                              check_id=check_id, result=result, detail=detail)

    def check_square_pixel(self, setting_id, rast_item, check_id, src_ds):
        # check 10 has the raster square pixels?
        detail = str()
        try:
            geotransform = src_ds.GetGeoTransform()
            # horizontal pixel resolution
            xres = abs(geotransform[1])
            # vertical pixel resolution
            yres = abs(geotransform[5])

            if xres == yres:
                result = True
            else:
                result = False
                detail = 'we found %d and %d for x- and y-resolution. Must ' \
                         'be equal' % (xres, yres)
        except Exception as detail:
            log.error(detail)
            result = False
        finally:
            self.results._add(setting_id=setting_id, raster=rast_item,
                              check_id=check_id, result=result, detail=detail)

    def check_extreme_value(self, setting_id, rast_item, check_id, src_ds):
        # are there no extreme values?
        detail = str()
        try:
            srcband = src_ds.GetRasterBand(1)
            stats = srcband.GetStatistics(True, True)
            min = stats[0]
            max = stats[1]
            min_allow = -10000
            max_allow = 10000
            if min_allow < min < max_allow and min_allow < max < max_allow:
                result = True
            else:
                result = False
                detail = 'found extreme values: min=%d, max=%d' % (min, max)
        except Exception as detail:
            log.error(detail)
            result = False
        finally:
            self.results._add(setting_id=setting_id, raster=rast_item,
                              check_id=check_id, result=result, detail=detail)

    def check_cum_pixel_cnt(self, rasters, setting_id, check_id):
        # cummulative pixel count
        detail = str()
        max_pixels_allow = 1000000000  # 1 billion for all rasters 1 entree
        cum_pixelcount = 0
        for rast_item in rasters:
            raster_path = os.path.join(self.sqlite_dir, rast_item)
            src_ds = gdal.Open(raster_path, GA_ReadOnly)
            cols = src_ds.RasterXSize
            rows = src_ds.RasterYSize
            pixelcount = cols * rows
            cum_pixelcount =+ pixelcount
        if cum_pixelcount > max_pixels_allow:
            result = False
            detail = 'cumulative pixelcount= %d for all rasters in ' \
                     'setting_id %d. This is more than 3Di can handle ' \
                     '1.000.000.000' % (cum_pixelcount, setting_id)
        else:
            result = True
        for rast_item in rasters:
            self.results._add(setting_id=setting_id, raster=rast_item,
                              check_id=check_id, result=result, detail=detail)

    def check_proj(self, setting_id, rast_item, check_id, src_ds, dem_src_ds):
        # compare projection of dem with another raster
        detail = str()
        try:
            dem_src_srs = osr.SpatialReference()
            dem_src_srs.ImportFromWkt(dem_src_ds.GetProjection())
            dem_projcs = dem_src_srs.GetAttrValue('projcs')

            src_srs = osr.SpatialReference()
            src_srs.ImportFromWkt(src_ds.GetProjection())
            projcs = src_srs.GetAttrValue('projcs')

            if dem_projcs == projcs:
                result = True
            else:
                result = False
                detail = 'found dem projection=%s, while %s projection=%s' % (
                    dem_projcs, rast_item, projcs)
        except Exception as detail:
            log.error(detail)
            result = False
        finally:
            self.results._add(setting_id=setting_id, raster=rast_item,
                          check_id=check_id, result=result, detail=detail)

    def check_pixelsize(self, setting_id, rast_item, check_id, src_ds,
                        dem_src_ds):
        # compare pixelsize of dem with another raster
        detail = str()
        dem_ext = dem_src_ds.GetGeoTransform()
        dem_ulx, dem_xres, dem_xskew, dem_uly, dem_yskew, dem_yres = dem_ext
        ext = src_ds.GetGeoTransform()
        ulx, xres, xskew, uly, yskew, yres = ext

        if (dem_xres, dem_yres) == (xres, yres):
            result = True
        else:
            result = False
            detail = 'dem has pixel size x:%d y:%d, while %s has pixel ' \
                     'size x:%d y:%d' % (
                dem_xres, dem_yres, rast_item, xres, yres)
        self.results._add(setting_id=setting_id, raster=rast_item,
                          check_id=check_id, result=result, detail=detail)

    def check_cnt_nodata(self, setting_id, rast_item, check_id, src_ds,
                        dem_src_ds):
        # compare data/nodata count of dem with another raster
        detail = str()
        dem_cnt_data, dem_cnt_nodata = self.count_data_nodata(dem_src_ds)
        cnt_data, cnt_nodata = self.count_data_nodata(src_ds)

        if (dem_cnt_data, dem_cnt_nodata) == (cnt_data, cnt_nodata):
            result = True
        else:
            result = False
            detail = 'dem has %d data- and %d nodata pixels, while %s has ' \
                     '%d data- and %d nodata pixels' % (
                dem_cnt_data, dem_cnt_nodata, rast_item, cnt_data, cnt_nodata)
        self.results._add(setting_id=setting_id, raster=rast_item,
                          check_id=check_id, result=result, detail=detail)

    def check_extent(self, setting_id, rast_item, check_id, src_ds,
                     dem_src_ds):
        # compare extent (number rows/colums) of dem with another raster
        detail = str()
        dem_cols = dem_src_ds.RasterXSize
        dem_rows = dem_src_ds.RasterYSize
        cols = src_ds.RasterXSize
        rows = src_ds.RasterYSize
        if (dem_cols, dem_rows) == (cols, rows):
            result = True
        else:
            result = False
            detail = 'dem has %d columns and % d rows, while %s has ' \
                     '%d columns and %d rows' % (
                dem_cols, dem_rows, rast_item, cols, rows)
        self.results._add(setting_id=setting_id, raster=rast_item,
                          check_id=check_id, result=result, detail=detail)

    def check_pixel_alignment(self, setting_id, rast_item, check_id, dem):
        detail = str()
        dem_path = os.path.join(self.sqlite_dir, dem)
        generator_dem = self.create_generator(dem_path)
        self.pixel_specs = self.get_pixel_specs(dem_path)

        current_status = self.progress_bar.get_current_status()

        progress_per_raster = self.progress_bar.get_progress_per_raster(
            self.entrees, self.results, current_status)
        self.progress_bar.increase_progress(progress_per_raster)

        other_tif_path = os.path.join(self.sqlite_dir, rast_item)
        generator_other = self.create_generator(other_tif_path)

        self.found_wrong_pixel = False
        self.wrong_pixels = []

        # compare two rasters blockwise
        for data1, data2 in izip(
                generator_dem.next(), generator_other.next()):
            self.compare_pixel_bbox(setting_id, rast_item, data1, data2)

        if self.found_wrong_pixel:
            self.input_data_shp.append(
                {'setting_id': setting_id,
                 'raster': rast_item,
                 'coords': self.wrong_pixels}
            )
            result = False
        else:
            result = True
        self.results._add(setting_id=setting_id, raster=rast_item,
                          check_id=check_id, result=result, detail=detail)

    def get_nr_blocks(self, raster_path):
        raster = gdal.Open(raster_path, GA_ReadOnly)
        band = raster.GetRasterBand(1)
        # optimize_blocksize
        w, h, nr_blocks = self.optimize_blocksize(band)
        return nr_blocks

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
        pixel_specs = (ulx, xres, xskew, uly, yskew, yres, pixelsize)
        return pixel_specs

    def get_wrong_pixel(self, setting_id, other_tif, bbox1, compare_mask):

        ulx, xres, xskew, uly, yskew, yres, pixelsize = self.pixel_specs

        # (0,0) is (x,y) left-upper corner of first bbox. Going down
        # bbox_row increases. Going right bbox_col increases
        l_up_col = bbox1[0]
        l_up_row = bbox1[1]

        true_idx = np.argwhere(compare_mask)
        # x = true_idx_test[0][0]
        # y = true_idx_test[0][1]
        bbox_idx = true_idx + [l_up_row, l_up_col]
        raster_centre_coor = [uly, ulx] + (bbox_idx * [-pixelsize, pixelsize]) + [-0.5 * pixelsize, 0.5 * pixelsize]
        # somehow x and y flipped ??
        # y = raster_lu_coor[0][0]
        # x = raster_lu_coor[0][1]
        # times 0.5 because we want centre coord and not left up corner

        self.wrong_pixels.append(raster_centre_coor.tolist())

        # wrong_pixels = []
        # # get indices of True
        # true_idx = np.where(compare_mask)
        # x_coords = true_idx[0]
        # y_coords = true_idx[1]
        # # (array([1, 1, 2, 2]), array([2, 3, 0, 1]))
        # for pixel in zip(x_coords, y_coords):
        #     bbox_row = pixel[0]
        #     bbox_column = pixel[1]
        #     loc_col = l_up_col + bbox_column
        #     loc_row = l_up_row + bbox_row
        #     # times 0.5 because we want centre coord and not left up corner
        #     x_coor = ulx + pixelsize * loc_col + 0.5 * pixelsize
        #     y_coor = uly - pixelsize * loc_row - 0.5 * pixelsize
        #     wrong_pixels.append((x_coor, y_coor))
        #
        # # create row in .shp for dem nodata where other raster is data
        # self.input_data_shp.append(
        #     {'geom_type': 'point',
        #      'setting_id': setting_id,
        #      'raster': str(other_tif),
        #      'coords': wrong_pixels
        #      }
        # )

    def compare_pixel_bbox(self, setting_id, other_tif, data1, data2):
        bbox1, arr1 = data1
        bbox2, arr2 = data2

        # create masks (without data and fill_value. Only mask)
        mask1 = (arr1[:] == -9999.)
        mask2 = (arr2[:] == -9999.)

        # xor gives array with trues for wrong pixels
        compare_mask = np.logical_xor(mask1, mask2)

        # is there any True in the compare mask? then there is at least
        # one wrong pixel
        if np.any(compare_mask):
            self.found_wrong_pixel = True
            self.get_wrong_pixel(setting_id, other_tif, bbox1, compare_mask)

    def run_check(self, base_check_name, **kwargs):
        prefix = "check_"
        check_name = prefix + base_check_name
        return getattr(self, check_name)(**kwargs)

    def get_check_ids_names(self, check_phase=None):
        # returns lst with tuples e.g [(1, 'tif_exists'), (2, 'tif_extension')]
        return [(chck.get('check_id'), chck.get('base_check_name')) for chck
                in RASTER_CHECKER_MAPPER if chck.get('phase') == check_phase]

    def run_phase_checks(self, setting_id, rasters, check_phase):

        check_ids_names = self.get_check_ids_names(check_phase)

        # phase 1 does check over multiple rasters, then next check
        if check_phase == 1:
            if not all([setting_id, rasters]):
                return
            for rast_item in rasters:
                for check_id, base_check_name in check_ids_names:
                    self.run_check(base_check_name, setting_id=setting_id,
                                   rast_item=rast_item, check_id=check_id)

        # phase 2 does multiple checks over one raster, then next raster
        elif check_phase == 2:
            for rast_item in rasters:
                raster_path = os.path.join(self.sqlite_dir, rast_item)
                src_ds = gdal.Open(raster_path, GA_ReadOnly)
                for check_id, base_check_name in check_ids_names:
                    self.run_check(base_check_name, setting_id=setting_id,
                                   rast_item=rast_item, check_id=check_id,
                                   src_ds=src_ds)

        # pixel cumulative
        # phase 3 does check over multiple rasters at once, then next check
        elif check_phase == 3:
            for check_id, base_check_name in check_ids_names:
                self.run_check(base_check_name, setting_id=setting_id,
                               rasters=rasters, check_id=check_id)

        # phase 4 (compare with dem)
        elif check_phase == 4:
            dem = rasters[0]
            dem_path = os.path.join(self.sqlite_dir, dem)
            dem_src_ds = gdal.Open(dem_path, GA_ReadOnly)
            for rast_item in rasters[1:]:
                path = os.path.join(self.sqlite_dir, rast_item)
                src_ds = gdal.Open(path, GA_ReadOnly)
                for check_id, base_check_name in check_ids_names:
                    self.run_check(base_check_name, setting_id=setting_id,
                                   rast_item=rast_item, check_id=check_id,
                                   src_ds=src_ds, dem_src_ds=dem_src_ds)
        # phase 5
        elif check_phase == 5:
            dem = rasters[0]
            for rast_item in rasters[1:]:
                for check_id, base_check_name in check_ids_names:
                    self.run_check(base_check_name, setting_id=setting_id,
                                   rast_item=rast_item, check_id=check_id,
                                   dem=dem)

    def get_nr_phases(self, run_pixel_checker):
        nr_phases  = max([chck.get('phase') for chck in RASTER_CHECKER_MAPPER])
        if run_pixel_checker:
            return nr_phases
        else:
            return nr_phases - 1

    def run_all_checks(self, run_pixel_checker=False):
        """
        -   We run checks in phases (multiple checks per phase over 1 raster),
            so that we do not have to open and close a raster that often.
        -   If a raster succeeds a phase that it goes to the next phase, but
            note that not all checks are blocking (written in
            RASTER_CHECKER_MAPPER)
        """

        nr_phases = self.get_nr_phases(run_pixel_checker)

        self.progress_bar = RasterCheckerProgressBar(
            nr_phases, run_pixel_checker, maximum=100,
            message_title='Raster Checker')

        progress_per_phase = self.progress_bar.get_progress_per_phase()

        phase = 1
        self.progress_bar.increase_progress(0, 'phase 1')
        for setting_id, rasters in self.entrees.iteritems():
            self.run_phase_checks(setting_id, rasters, phase)
        self.results.update_result_per_phase(setting_id, rasters, phase)

        phase = 2
        self.progress_bar.increase_progress(progress_per_phase, 'phase 2')
        for setting_id, rasters in self.entrees.iteritems():
            # we only check rasters that passed blocking checks previous phase
            rasters_ready = self.results.get_rasters_ready(setting_id, phase)
            if rasters_ready:
                self.run_phase_checks(setting_id, rasters_ready, phase)
        self.results.update_result_per_phase(setting_id, rasters, phase)

        phase = 3
        self.progress_bar.increase_progress(progress_per_phase, 'phase 3')
        # cumulative pixels
        for setting_id, rasters in self.entrees.iteritems():
            # we only check rasters that passed blocking checks previous phase
            rasters_ready = self.results.get_rasters_ready(setting_id, phase)
            self.run_phase_checks(setting_id, rasters_ready, phase)

        phase = 4
        self.progress_bar.increase_progress(progress_per_phase, 'phase 4')
        # compare with dem
        for setting_id, rasters in self.entrees.iteritems():
            # we only check rasters that passed blocking checks of phase 2
            rasters_ready = self.results.get_rasters_ready(setting_id, 3)
            # We will compare the dem with other rasters. We need:
            # - at least two rasters per entree and
            # - the dem_file (which is the first value (rasters[0])
            if len(rasters_ready) >= 2 and rasters[0] in rasters_ready:
                rasters_ready = self.dem_to_first_index(rasters, rasters_ready)
                self.run_phase_checks(setting_id, rasters_ready, phase)
        self.results.update_result_per_phase(setting_id, rasters, phase)

        phase = 5
        self.progress_bar.increase_progress(progress_per_phase, 'phase 5')
        if not run_pixel_checker:
            return
        self.input_data_shp = []
        for setting_id, rasters in self.entrees.iteritems():
            rasters_ready = self.results.get_rasters_ready(setting_id, phase)
            # Note that the dem always passed the previous phase (as we then
            # compared the dem with other rasters). If other raster was
            # dem alike (extent, pixelsize, etc) then that raster was added
            # to self.results. However (!!) the dem was not added to
            # self.results. From now we only continue if there is at least
            # 1 raster
            if len(rasters_ready) >= 1:
                # Still need to add the dem (rasters[0]) to rasters_ready
                rasters_ready.insert(0, rasters[0])
                self.run_phase_checks(setting_id, rasters_ready, phase)
        self.results.update_result_per_phase(setting_id, rasters, phase)

        # delete progress bar
        self.progress_bar.__del__()

    def dem_to_first_index(self, rasters_orig, rasters_ready):
        # assumes dem is in both arguments !!
        dem = rasters_orig[0]
        dem_index = rasters_ready.index(dem)
        if dem_index <> 0:
            rasters_ready[0], rasters_ready[dem_index] = \
                rasters_ready[dem_index], rasters_ready[0]
        return rasters_ready

    def create_shp(self):
        # https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/
        # vector.html#writing-vector-layers
        # define fields for feature attributes. A QgsFields object is needed
        fields = QgsFields()
        fields.append(QgsField("setting_id", QVariant.String))
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

        # # TODO enable transformation (test buitenland modellen!!)
        # source_epsg = 28992
        # dest_epsg = 28992
        # source_crs = QgsCoordinateReferenceSystem(int(source_epsg))
        # dest_crs = QgsCoordinateReferenceSystem(int(dest_epsg))
        # transform = QgsCoordinateTransform(source_crs, dest_crs)

        self.shape_path = self.results.log_path.split('.log')[0] + '.shp'

        writer = QgsVectorFileWriter(self.shape_path, "CP1250", fields,
                                     QGis.WKBPoint, None, "ESRI Shapefile")
        try:
            if writer.hasError() != QgsVectorFileWriter.NoError:
                msg = 'Error while creating shapefile: ' + \
                      str(writer.errorMessage())
                log.error(msg)
                raise Exception (msg)
            else:

                for pixel_check_dict in self.input_data_shp:
                    raster = pixel_check_dict.get('raster')
                    setting_id = pixel_check_dict.get('setting_id')
                    coords = pixel_check_dict.get('coords')
                    for row in coords:
                        for point in row:
                            point_x = point[0]
                            point_y = point[1]
                            feat = QgsFeature()
                            feat.setGeometry(QgsGeometry.fromPoint(
                                QgsPoint(point_x, point_y)))
                            feat.setAttributes([
                                setting_id, raster, point_x, point_y])
                            writer.addFeature(feat)
        except Exception as e:
            log.error(e)
        # delete the writer to flush features to disk
        del writer

    def pop_up_finished(self, shpfile=False):
        header = 'Raster checker is finished'
        if shpfile:
            msg = 'The check results have been written to: \n %s \n ' \
                  'The coordinates of wrong pixels are written to: \n' \
                  '%s' % (self.results.log_path, self.shape_path)
        else:
            msg = 'The check results have been written to:\n%s' % \
                  self.results.log_path
        pop_up_info(msg, header)

    def check_constants(self):
        method_names = [chck.get('base_check_name') for chck in
                          RASTER_CHECKER_MAPPER]
        prefix = "check_"
        for base_check_name in method_names:
            check_name = prefix + base_check_name
            if not hasattr(self, check_name):
                raise AttributeError('RasterChecker has no attr ' + check_name)

        method_ids = [chck.get('check_id') for chck in RASTER_CHECKER_MAPPER]

        if len(method_ids) != len(list(set(method_ids))):
            raise AttributeError('Not all unique check_ids in '
                                 'RASTER_CHECKER_MAPPER')

    def run(self, checks):
        run_pixels_bool = 'check pixels' in checks
        if 'check all rasters' in checks:
            self.run_all_checks(run_pixel_checker=run_pixels_bool)
        # if 'improve when necessary' in checks:
        # TODO: write improvement function
        # TODO: now checks are done for all entrees. Enable checks for 1 entree
        self.close_session()
        self.results.sort_results()
        # write and save log file (here the self.results.log_path is created)
        self.results.write_log(self.all_raster_ref)
        if run_pixels_bool:
            self.create_shp()
        self.pop_up_finished(shpfile=run_pixels_bool)


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
