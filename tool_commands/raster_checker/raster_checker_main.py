# (c) Nelen & Schuurmans, see LICENSE.rst.
from cached_property import cached_property
from gdal import GA_ReadOnly
from osgeo import gdal
from osgeo import osr
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsFeature
from qgis.core import QgsField
from qgis.core import QgsFields
from qgis.core import QgsGeometry
from qgis.core import QgsPointXY
from qgis.core import QgsVectorFileWriter
from qgis.core import QgsWkbTypes
from qgis.PyQt.QtCore import QVariant
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from ThreeDiToolbox.tool_commands.raster_checker import raster_checker_log
from ThreeDiToolbox.tool_commands.raster_checker import raster_checker_prework
from ThreeDiToolbox.tool_commands.raster_checker.constants import RASTER_CHECKER_MAPPER
from ThreeDiToolbox.utils.user_messages import pop_up_info
from ThreeDiToolbox.utils.user_messages import pop_up_question

import logging
import numpy as np
import os
import string


logger = logging.getLogger(__name__)
Base = declarative_base()


class RasterChecker(object):
    def __init__(self, threedi_database):
        self.db = threedi_database
        # session required for SqlAlchemy queries
        self.session = self.db.get_session()
        # datamodel required for dynamic creation of ORM models
        self.engine = self.db.get_engine()
        self.metadata = MetaData(bind=self.engine)

        datamodel = raster_checker_prework.DataModelSource(self.metadata)

        raster_checker_entries = raster_checker_prework.RasterCheckerEntries(
            datamodel, self.session
        )
        self.entries = raster_checker_entries.entries
        self.entries_metadata = raster_checker_entries.entries_metadata

        sqlite_path = str(self.db.settings["db_path"])
        self.sqlite_dir = os.path.split(sqlite_path)[0]
        self.results = raster_checker_log.RasterCheckerResults(sqlite_path)

        self.progress_bar = None
        self.unique_id_name = []
        self.too_many_wrong_pixels = False

        # some check constants
        self.no_data_value_int = -9999
        self.no_data_value_flt = -9999.0
        self.max_pixels_allow = 1000000000  # 1 billion all rasters 1 entry

    def close_session(self):
        try:
            self.session.close()
        except Exception:
            logger.exception("Error closing session")

    def iter_block_row(self, band, offset_y, block_height, block_width):
        ncols = int(band.XSize / block_width)
        for i in range(ncols):
            arr = band.ReadAsArray(i * block_width, offset_y, block_width, block_height)
            yield (
                i * block_width,
                offset_y,
                (i + 1) * block_width,
                offset_y + block_height,
            ), arr
        # possible leftover block
        width = band.XSize - (ncols * block_width)
        if width > 0:
            arr = band.ReadAsArray(i * block_width, offset_y, width, block_height)
            yield (
                ncols * block_width,
                offset_y,
                ncols * block_width + width,
                offset_y + block_height,
            ), arr
            # offset_y + block_height), arr

    def iter_blocks(self, band, block_width=0, block_height=0):
        """ Iterate over native blocks in a GDal raster data band.
        Optionally, provide a minimum block dimension.
        Returns a tuple of bbox (x1, y1, x2, y2) and the data as ndarray. """
        nrows = int(band.YSize / block_height)
        for j in range(nrows):
            for block in self.iter_block_row(
                band, j * block_height, block_height, block_width
            ):
                yield block
        # possible leftover row
        height = band.YSize - (nrows * block_height)
        if height > 0:
            for block in self.iter_block_row(
                band, nrows * block_height, height, block_width
            ):
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
        src_ds = None  # close raster
        w, h, nr_blocks = self.optimize_blocksize(band)
        raster_generator = self.iter_blocks(band, block_width=w, block_height=h)
        count_data = 0
        count_nodata = 0
        for data in raster_generator:
            bbox, arr = data
            total_size = arr.size
            add_cnt_nodata = np.count_nonzero(arr == self.no_data_value_int)
            add_cnt_data = total_size - add_cnt_nodata
            count_nodata += add_cnt_nodata
            count_data += add_cnt_data
        return count_data, count_nodata

    def check_id_tifname_unique(self, setting_id, rast_item, check_id):
        detail = ""
        id_name = "%d_%s" % (setting_id, rast_item)
        self.unique_id_name.append(id_name)
        if len(self.unique_id_name) == len(set(self.unique_id_name)):
            result = True
        else:
            result = False
        self.results._add(
            setting_id=setting_id,
            raster=rast_item,
            check_id=check_id,
            result=result,
            detail=detail,
        )

    def check_tif_exists(self, setting_id, rast_item, check_id):
        # Does the raster (reference from the model) really exists?
        detail = ""
        raster_path = os.path.join(self.sqlite_dir, rast_item)
        if os.path.isfile(raster_path):
            result = True
        else:
            result = False
        self.results._add(
            setting_id=setting_id,
            raster=rast_item,
            check_id=check_id,
            result=result,
            detail=detail,
        )

    def check_extension(self, setting_id, rast_item, check_id):
        # exetension of raster must be  .tif or .tiff
        detail = ""
        extension = rast_item.split(".")[-1]
        if extension.lower() not in ["tif", "tiff"]:
            result = False
            detail = "found extension: %s" % extension
        else:
            result = True
        self.results._add(
            setting_id=setting_id,
            raster=rast_item,
            check_id=check_id,
            result=result,
            detail=detail,
        )

    def check_filename(self, setting_id, rast_item, check_id):
        # what is the purpose ??
        # TODO: lars suggest to use just 'os' to check its 1 folder deep

        # Does the raster filename have valid chars (also space is not allowed)
        detail = ""
        invalid_chars = set(string.punctuation.replace("_", ""))
        invalid_chars.add(" ")
        invalid_chars_in_filename = []

        # only one '.' and '/' is allowed in relative path
        count_forward_slash = 0
        count_dot = 0
        for char in rast_item:
            if char in invalid_chars:
                if char == "/" and count_forward_slash < 1:
                    count_forward_slash += 1
                elif char == "." and count_dot < 1:
                    count_dot += 1
                else:
                    invalid_chars_in_filename.append(char)
        if invalid_chars_in_filename:
            result = False
            detail = str(invalid_chars_in_filename)
        else:
            result = True
        self.results._add(
            setting_id=setting_id,
            raster=rast_item,
            check_id=check_id,
            result=result,
            detail=detail,
        )

    def check_singleband(self, setting_id, rast_item, check_id, src_ds):
        # Is the raster singleband ?
        detail = ""
        try:
            cnt_rasterband = src_ds.RasterCount
            if cnt_rasterband == 1:
                result = True
            else:
                result = False
                detail = "found %d rasterbands" % cnt_rasterband
        except Exception:
            logger.exception("Error checking singleband")
            result = False
        finally:
            # TODO: the method "just" checks, but apparently it also adds to
            # the results?
            self.results._add(
                setting_id=setting_id,
                raster=rast_item,
                check_id=check_id,
                result=result,
                detail=detail,
            )

    def check_nodata(self, setting_id, rast_item, check_id, src_ds):
        # Is the raster nodata -9999 ?
        detail = ""
        try:
            srcband = src_ds.GetRasterBand(1)
            nodata = srcband.GetNoDataValue()
            if nodata == self.no_data_value_int:
                result = True
            else:
                result = False
                detail = "nodata value is %d" % nodata
        except Exception:
            logger.exception("Error checking nodata")
            result = False
        finally:
            self.results._add(
                setting_id=setting_id,
                raster=rast_item,
                check_id=check_id,
                result=result,
                detail=detail,
            )

    def check_proj_unit(self, setting_id, rast_item, check_id, src_ds):
        # Does the raster have a projected coordinate system? (unit: meters)?
        detail = ""
        try:
            proj = src_ds.GetProjection()
            spat_ref = osr.SpatialReference()
            spat_ref.ImportFromWkt(proj)
            unit = spat_ref.GetLinearUnitsName()
            if unit == "metre":
                result = True
            else:
                result = False
                detail = "unit is %s" % unit
        except Exception:
            logger.exception("Error checking projection")
            result = False
        finally:
            self.results._add(
                setting_id=setting_id,
                raster=rast_item,
                check_id=check_id,
                result=result,
                detail=detail,
            )

    def check_flt32(self, setting_id, rast_item, check_id, src_ds):
        # Is the raster datatype float32 ?
        detail = ""
        try:
            srcband = src_ds.GetRasterBand(1)
            data_type = srcband.DataType
            data_type_name = gdal.GetDataTypeName(data_type)
            if data_type_name == "Float32":
                result = True
            else:
                result = False
                detail = "data_type is %s" % data_type_name
        except Exception:
            logger.exception("Error checking float32")
            result = False
        finally:
            self.results._add(
                setting_id=setting_id,
                raster=rast_item,
                check_id=check_id,
                result=result,
                detail=detail,
            )

    def check_compress(self, setting_id, rast_item, check_id, src_ds):
        # Is the raster compressed ?
        detail = ""
        try:
            compr_method = src_ds.GetMetadata("IMAGE_STRUCTURE")["COMPRESSION"]
            if compr_method == "DEFLATE":
                result = True
            else:
                result = False
                detail = "compression_method is %s" % compr_method
        except Exception:
            detail = "Not able to get compression type"
            logger.exception(detail)
            result = False
        finally:
            self.results._add(
                setting_id=setting_id,
                raster=rast_item,
                check_id=check_id,
                result=result,
                detail=detail,
            )

    def check_pixel_decimal(self, setting_id, rast_item, check_id, src_ds):
        # Has the pixel resolution less than three decimal places?
        detail = ""
        try:
            geotransform = src_ds.GetGeoTransform()
            # horizontal pixel resolution
            xres = abs(geotransform[1])
            cnt_decimal_xres = str(xres)[::-1].find(".")
            # vertical pixel resolution
            yres = abs(geotransform[5])
            cnt_decimal_yres = str(yres)[::-1].find(".")

            if cnt_decimal_xres > 3 or cnt_decimal_yres > 3:
                result = False
                detail = (
                    "found %d and %d decimal places for x- and "
                    "y- resolution respectively" % (cnt_decimal_xres, cnt_decimal_yres)
                )
            else:
                result = True
        except Exception:
            logger.exception("Error checking pixel decimal resolution")
            result = False
        finally:
            self.results._add(
                setting_id=setting_id,
                raster=rast_item,
                check_id=check_id,
                result=result,
                detail=detail,
            )

    def check_square_pixel(self, setting_id, rast_item, check_id, src_ds):
        # check 10 has the raster square pixels?
        detail = ""
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
                detail = (
                    "we found %d and %d for x- and y-resolution. Must "
                    "be equal" % (xres, yres)
                )
        except Exception:
            logger.exception("Error checking square pixels")
            result = False
        finally:
            self.results._add(
                setting_id=setting_id,
                raster=rast_item,
                check_id=check_id,
                result=result,
                detail=detail,
            )

    def check_extreme_value(self, setting_id, rast_item, check_id, src_ds):
        # are there no extreme values?
        detail = ""
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
                detail = "found extreme values: min=%d, max=%d" % (min, max)
        except Exception:
            logger.exception("Error checking extreme values")
            result = False
        finally:
            self.results._add(
                setting_id=setting_id,
                raster=rast_item,
                check_id=check_id,
                result=result,
                detail=detail,
            )

    def check_cum_pixel_cnt(self, rasters, setting_id, check_id):
        # cummulative pixel count
        detail = ""
        cum_pixelcount = 0
        for rast_item in rasters:
            raster_path = os.path.join(self.sqlite_dir, rast_item)
            src_ds = gdal.Open(raster_path, GA_ReadOnly)
            cols = src_ds.RasterXSize
            rows = src_ds.RasterYSize
            src_ds = None  # close raster
            pixelcount = cols * rows
            cum_pixelcount += pixelcount
        if cum_pixelcount > self.max_pixels_allow:
            result = False
            detail = (
                "cumulative pixelcount= %d for all rasters in "
                "setting_id %d. This is more than 3Di can handle "
                "1.000.000.000" % (cum_pixelcount, setting_id)
            )
        else:
            result = True
        for rast_item in rasters:
            self.results._add(
                setting_id=setting_id,
                raster=rast_item,
                check_id=check_id,
                result=result,
                detail=detail,
            )

    def check_proj(self, setting_id, rast_item, check_id, src_ds, dem_src_ds):
        # compare projection of dem with another raster
        detail = ""
        try:
            dem_src_srs = osr.SpatialReference()
            dem_src_srs.ImportFromWkt(dem_src_ds.GetProjection())
            dem_projcs = dem_src_srs.GetAttrValue("projcs")

            src_srs = osr.SpatialReference()
            src_srs.ImportFromWkt(src_ds.GetProjection())
            projcs = src_srs.GetAttrValue("projcs")

            if dem_projcs == projcs:
                result = True
            else:
                result = False
                detail = "found dem projection=%s, while %s projection=%s" % (
                    dem_projcs,
                    rast_item,
                    projcs,
                )
        except Exception:
            logger.exception("Error checking projection")
            result = False
        finally:
            self.results._add(
                setting_id=setting_id,
                raster=rast_item,
                check_id=check_id,
                result=result,
                detail=detail,
            )

    def check_pixelsize(self, setting_id, rast_item, check_id, src_ds, dem_src_ds):
        # compare pixelsize of dem with another raster
        detail = ""
        dem_ext = dem_src_ds.GetGeoTransform()
        dem_ulx, dem_xres, dem_xskew, dem_uly, dem_yskew, dem_yres = dem_ext
        ext = src_ds.GetGeoTransform()
        ulx, xres, xskew, uly, yskew, yres = ext

        if (dem_xres, dem_yres) == (xres, yres):
            result = True
        else:
            result = False
            detail = (
                "dem has pixel size x:%d y:%d, while %s has pixel "
                "size x:%d y:%d" % (dem_xres, dem_yres, rast_item, xres, yres)
            )
        self.results._add(
            setting_id=setting_id,
            raster=rast_item,
            check_id=check_id,
            result=result,
            detail=detail,
        )

    def check_cnt_nodata(self, setting_id, rast_item, check_id, src_ds, dem_src_ds):
        """ compare data/nodata count of dem with another raster and store the
        counts as we use it later before pixel alignment check """
        detail = ""
        dem_cnt_data, dem_cnt_nodata = self.count_data_nodata(dem_src_ds)
        cnt_data, cnt_nodata = self.count_data_nodata(src_ds)
        self.results.store_cnt_data_nodata.append(
            {
                "setting_id": setting_id,
                "raster": rast_item,
                "dem_cnt_data": dem_cnt_data,
                "dem_cnt_nodata": dem_cnt_nodata,
                "cnt_data": cnt_data,
                "cnt_nodata": cnt_nodata,
            }
        )

        if (dem_cnt_data, dem_cnt_nodata) == (cnt_data, cnt_nodata):
            result = True
        else:
            result = False
            detail = "dem: %d/%d data/nodata, while %s: %d/%d data/nodata" % (
                dem_cnt_data,
                dem_cnt_nodata,
                rast_item,
                cnt_data,
                cnt_nodata,
            )
        self.results._add(
            setting_id=setting_id,
            raster=rast_item,
            check_id=check_id,
            result=result,
            detail=detail,
        )

    def check_extent(self, setting_id, rast_item, check_id, src_ds, dem_src_ds):
        """ compare extent (number rows/colums) of dem with another raster """
        detail = ""
        dem_cols = dem_src_ds.RasterXSize
        dem_rows = dem_src_ds.RasterYSize
        cols = src_ds.RasterXSize
        rows = src_ds.RasterYSize
        if (dem_cols, dem_rows) == (cols, rows):
            result = True
        else:
            result = False
            detail = (
                "dem has %d columns and % d rows, while %s has "
                "%d columns and %d rows" % (dem_cols, dem_rows, rast_item, cols, rows)
            )
        self.results._add(
            setting_id=setting_id,
            raster=rast_item,
            check_id=check_id,
            result=result,
            detail=detail,
        )

    def check_pixel_alignment(self, setting_id, rast_item, check_id, dem):
        """
        # we will check pixel alignment for raster A and B only if:
        # - diff between nr data pixels A and nr data pixels B < 50000, and
        # - diff between nr nodata pixels A and nr nodata pixels B < 50000
        # Otherwise it likely that this check takes too long.
        :param setting_id:
        :param rast_item:
        :param check_id:
        :param dem:
        :return:
        """

        detail = ""
        [(dem_cnt_data, dem_cnt_nodata, cnt_data, cnt_nodata)] = [
            (
                chck.get("dem_cnt_data"),
                chck.get("dem_cnt_nodata"),
                chck.get("cnt_data"),
                chck.get("cnt_nodata"),
            )
            for chck in self.results.store_cnt_data_nodata
            if chck.get("raster") == rast_item and chck.get("setting_id") == setting_id
        ]
        diff_data = abs(dem_cnt_data - cnt_data)
        diff_nodata = abs(dem_cnt_nodata - cnt_nodata)
        max_wrong_pixels = 50000
        if diff_data > max_wrong_pixels or diff_nodata > max_wrong_pixels:
            detail = (
                "Wrong pixels are not written too .shp as too many "
                "wrong pixels were found"
            )
            self.too_many_wrong_pixels = True
            result = False
            self.results._add(
                setting_id=setting_id,
                raster=rast_item,
                check_id=check_id,
                result=result,
                detail=detail,
            )
            return

        dem_path = os.path.join(self.sqlite_dir, dem)
        dem_raster = gdal.Open(dem_path, GA_ReadOnly)
        dem_band = dem_raster.GetRasterBand(1)

        other_tif_path = os.path.join(self.sqlite_dir, rast_item)
        other_tif_raster = gdal.Open(other_tif_path, GA_ReadOnly)
        other_tif_band = other_tif_raster.GetRasterBand(1)

        generator_dem = self.create_generator(dem_band)
        generator_other = self.create_generator(other_tif_band)

        current_status = self.progress_bar.current_status
        progress_per_raster = self.progress_bar.get_progress_per_raster(
            self.entries, self.results, current_status
        )
        self.progress_bar.increase_progress(progress_per_raster)

        self.pixel_specs = self.get_pixel_specs(dem_path)

        found_wrong_pixel = False
        wrong_pixels_list = []

        # compare two rasters blockwise
        for data1, data2 in list(
            zip(generator_dem.__next__(), generator_other.__next__())
        ):
            wrong_pixels = self.compare_pixel_bbox(data1, data2)
            if wrong_pixels:
                found_wrong_pixel = True
                wrong_pixels_list.append(wrong_pixels)

        dem_raster = None  # close raster
        other_tif_raster = None  # close raster

        if found_wrong_pixel:
            self.input_data_shp.append(
                {
                    "setting_id": setting_id,
                    "raster": rast_item,
                    "coords": wrong_pixels_list,
                }
            )
            result = False
            detail = "the mismatch locations have been written to .shp file"
        else:
            result = True
        self.results._add(
            setting_id=setting_id,
            raster=rast_item,
            check_id=check_id,
            result=result,
            detail=detail,
        )

    def get_nr_blocks(self, raster_path):
        raster = gdal.Open(raster_path, GA_ReadOnly)
        band = raster.GetRasterBand(1)
        raster = None  # close raster
        # optimize_blocksize
        w, h, nr_blocks = self.optimize_blocksize(band)
        return nr_blocks

    def create_generator(self, band):
        w, h, nr_blocks = self.optimize_blocksize(band)
        # create generators
        while True:
            yield self.iter_blocks(band, block_width=w, block_height=h)

    @staticmethod
    def get_pixel_specs(dem_path):
        dem = gdal.Open(dem_path, GA_ReadOnly)
        ulx, xres, xskew, uly, yskew, yres = dem.GetGeoTransform()
        pixelsize = abs(min(xres, yres))
        pixel_specs = (ulx, xres, xskew, uly, yskew, yres, pixelsize)
        return pixel_specs

    def get_wrong_pixel(self, bbox1, compare_mask):
        """ The function finds the x,y coordinates (in same projection as the
        dem) of wrong pixels:
        - where dem is data and other raster nodata
        - where dem is nodata and other raster data
        We dont analyse whole raster at once, but blockwise (per boundingbox).
        Each pixel is represented by a column nr (in the end used to get
        x-coor) and a row nr (in the end used to get y-coor).
        :param setting_id: int (v2_global_setting id of model entry)
        :param bbox1:
        :param compare_mask:
        :return: coords
        """
        ulx, xres, xskew, uly, yskew, yres, pixelsize = self.pixel_specs

        # get the column and row nr of the left upper pixel of bounding box
        # the left upper pixel of whole rasters has column = 0 and row = 0
        # Going south row nr increases. Going right column nr increases
        ul_col = bbox1[0]
        ul_row = bbox1[1]

        # indices in the bbox of wrong (True) pixels
        bbox_idx = np.argwhere(compare_mask)
        # bbox_idx is 2D np.array:
        # 1st element = nth column (in west-east direction) in bbox
        # 2nd element = nth row (in north-south direction) in bbox

        """
        # 1. indices in the whole raster of wrong (True) pixels
        raster_idx = bbox_idx + [ul_row, ul_col]
        # 1st element = nth column (in west-east direction) in whole raster
        # 2nd element = nth row (in north-south direction) in whole raster

        # 2. distance from whole raster's lup corner to wrong pixels
        distance = raster_idx * pixelsize

        # 3. now get the centre coords (remember: row=y, col=x) of wrong pixels
        coords = [uly, ulx] + (distance * [-1, 1]) + \
                        [-0.5 * pixelsize, 0.5 * pixelsize]
        # 1st element (y-dir) is "distance *-1" as we substract to go south
        # 2nd element (x-dir) is "distance -1" as we add to go east
        # times 0.5 because we want centre coord and not left up corner
        """

        # all (1, 2 and 3) in once:
        coords = (
            [uly, ulx]
            + ((bbox_idx + [ul_row, ul_col]) * pixelsize) * [-1, 1]
            + [-0.5 * pixelsize, 0.5 * pixelsize]
        )
        # note that: x = coords[:][0] and y = coords[:][1]
        return coords

    def compare_pixel_bbox(self, data1, data2):
        bbox1, arr1 = data1
        bbox2, arr2 = data2
        # create masks (without data and fill_value. Only mask)
        mask1 = arr1[:] == self.no_data_value_flt
        mask2 = arr2[:] == self.no_data_value_flt
        # xor gives array with trues for wrong pixels
        compare_mask = np.logical_xor(mask1, mask2)
        # is there any True in the compare mask? then there is at least
        # one wrong pixel
        if np.any(compare_mask):
            coords = self.get_wrong_pixel(bbox1, compare_mask)
            return coords.tolist()

    def run_check(self, base_check_name, **kwargs):
        prefix = "check_"
        check_name = prefix + base_check_name
        return getattr(self, check_name)(**kwargs)

    @staticmethod
    def get_check_ids_names(check_phase=None):
        """
        :param check_phase: int (1 to 5)
        :return: list with tuples with (check_id, check_name), e.g:
        [(1, 'tif_exists'), (2, 'tif_extension')]
        """
        return [
            (chck.get("check_id"), chck.get("base_check_name"))
            for chck in RASTER_CHECKER_MAPPER
            if chck.get("phase") == check_phase
        ]

    @cached_property
    def nr_phases(self):
        return max([chck.get("phase") for chck in RASTER_CHECKER_MAPPER])

    def dem_to_first_index(self, rasters_orig, rasters_ready):
        # assumes dem is in both arguments !!
        dem = rasters_orig[0]
        dem_index = rasters_ready.index(dem)
        if dem_index != 0:
            rasters_ready[0], rasters_ready[dem_index] = (
                rasters_ready[dem_index],
                rasters_ready[0],
            )
        # we do not have to return 'rasters_ready' since inplace edit

    def run_phase_checks(self, setting_id, rasters, check_phase):
        check_ids_names = self.get_check_ids_names(check_phase)

        # phase 1 does check over multiple rasters, then next check
        if check_phase == 1:
            if not all([setting_id, rasters]):
                return
            for rast_item in rasters:
                for check_id, base_check_name in check_ids_names:
                    self.run_check(
                        base_check_name,
                        setting_id=setting_id,
                        rast_item=rast_item,
                        check_id=check_id,
                    )

        # phase 2 does multiple checks over one raster, then next raster
        elif check_phase == 2:
            for rast_item in rasters:
                raster_path = os.path.join(self.sqlite_dir, rast_item)
                src_ds = gdal.Open(raster_path, GA_ReadOnly)
                for check_id, base_check_name in check_ids_names:
                    self.run_check(
                        base_check_name,
                        setting_id=setting_id,
                        rast_item=rast_item,
                        check_id=check_id,
                        src_ds=src_ds,
                    )
                src_ds = None  # close raster

        # pixel cumulative
        # phase 3 does check over multiple rasters at once, then next check
        elif check_phase == 3:
            for check_id, base_check_name in check_ids_names:
                self.run_check(
                    base_check_name,
                    setting_id=setting_id,
                    rasters=rasters,
                    check_id=check_id,
                )

        # phase 4 (compare with dem)
        elif check_phase == 4:
            dem = rasters[0]
            dem_path = os.path.join(self.sqlite_dir, dem)
            dem_src_ds = gdal.Open(dem_path, GA_ReadOnly)
            for rast_item in rasters[1:]:
                path = os.path.join(self.sqlite_dir, rast_item)
                src_ds = gdal.Open(path, GA_ReadOnly)
                for check_id, base_check_name in check_ids_names:
                    self.run_check(
                        base_check_name,
                        setting_id=setting_id,
                        rast_item=rast_item,
                        check_id=check_id,
                        src_ds=src_ds,
                        dem_src_ds=dem_src_ds,
                    )
            dem_src_ds = None  # close raster
            src_ds = None  # close raster

        # phase 5
        elif check_phase == 5:
            dem = rasters[0]
            for rast_item in rasters[1:]:
                for check_id, base_check_name in check_ids_names:
                    self.run_check(
                        base_check_name,
                        setting_id=setting_id,
                        rast_item=rast_item,
                        check_id=check_id,
                        dem=dem,
                    )

    def run_all_checks(self):
        """
        - We run checks in phases. Each phase consists of 1 or more checks:
        - Phase 1 has e.g. a check: "can the .tif be found on machine?"
        - Not all checks are blocking (defined in RASTER_CHECKER_MAPPER dict)
        - If a raster succeeds (the blocking checks of) a phase then the
          raster goes to the next phase
        - the last phase is the pixel_checker (pixel_alignment pixel by pixel),
          which is an optional phase (in case selected by user).
        Basically, we do two types of checks:
        1) we check individual raster (e.g. "is data_type correct?")
        2) we compare raster with dem in same setting_id (dem always leading)
        ps: adding or deleting a check can be done via RASTER_CHECKER_MAPPER
        """

        self.progress_bar = raster_checker_log.RasterCheckerProgressBar(
            self.nr_phases, maximum=100, message_title="Raster Checker"
        )

        progress_per_phase = self.progress_bar.progress_per_phase

        phase = 1
        self.progress_bar.set_progress(0)
        for setting_id, rasters in self.entries.items():
            self.run_phase_checks(setting_id, rasters, phase)
            self.results.update_result_per_phase(setting_id, rasters, phase)
        self.progress_bar.increase_progress(progress_per_phase, "done phase 1")

        phase = 2
        # invidual raster checks (e.g. datatype, projection unit, etc)
        for setting_id, rasters in self.entries.items():
            # we only check rasters that passed blocking checks previous phase
            rasters_ready = self.results.get_rasters_ready(setting_id, phase)
            if rasters_ready:
                self.run_phase_checks(setting_id, rasters_ready, phase)
            self.results.update_result_per_phase(setting_id, rasters, phase)
        self.progress_bar.increase_progress(progress_per_phase, "done phase 2")

        phase = 3
        # cumulative pixels of all rasters in 1 entry not too much?
        for setting_id, rasters in self.entries.items():
            # we only check rasters that passed blocking checks previous phase
            rasters_ready = self.results.get_rasters_ready(setting_id, phase)
            self.run_phase_checks(setting_id, rasters_ready, phase)
            self.results.update_result_per_phase(setting_id, rasters, phase)
        self.progress_bar.increase_progress(progress_per_phase, "done phase 3")

        phase = 4
        # compare rasters with dem in same entry
        for setting_id, rasters in self.entries.items():
            # we only check rasters that passed blocking checks of phase 2
            rasters_ready = self.results.get_rasters_ready(setting_id, 3)
            # We will compare the dem with other rasters. We need:
            # - at least two rasters per entry and
            # - the dem_file (which is the first value (rasters[0])
            if len(rasters_ready) >= 2 and rasters[0] in rasters_ready:
                # make sure again that dem is on first index
                self.dem_to_first_index(rasters, rasters_ready)
                self.run_phase_checks(setting_id, rasters_ready, phase)
            self.results.update_result_per_phase(setting_id, rasters, phase)
        self.progress_bar.increase_progress(progress_per_phase, "done phase 4")

        phase = 5
        self.input_data_shp = []
        for setting_id, rasters in self.entries.items():
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

        self.progress_bar.set_progress(100)

    def create_shp(self):
        fields = QgsFields()
        fields.append(QgsField("setting_id", QVariant.String))
        fields.append(QgsField("raster", QVariant.String))
        fields.append(QgsField("x centre", QVariant.String))
        fields.append(QgsField("y centre", QVariant.String))

        self.shape_path = self.results.log_path.split(".logger")[0] + ".shp"
        writer = QgsVectorFileWriter(
            self.shape_path,
            "CP1250",
            fields,
            QgsWkbTypes.Point,
            QgsCoordinateReferenceSystem(),
            "ESRI Shapefile",
        )
        try:
            if writer.hasError() != QgsVectorFileWriter.NoError:
                msg = "Error while creating shapefile: " + str(writer.errorMessage())
                logger.error(msg)
                raise Exception(msg)
            else:
                for pixel_check_dict in self.input_data_shp:
                    raster = pixel_check_dict.get("raster")
                    setting_id = pixel_check_dict.get("setting_id")
                    coords = pixel_check_dict.get("coords")
                    for row in coords:
                        for point in row:
                            point_y = point[0]
                            point_x = point[1]
                            feat = QgsFeature()
                            feat.setGeometry(
                                QgsGeometry.fromPointXY(QgsPointXY(point_x, point_y))
                            )
                            feat.setAttributes([setting_id, raster, point_x, point_y])
                            writer.addFeature(feat)
        except Exception:
            # TODO: there's a "raise" inside the try, there's a raise
            # below. What's the intention?
            logger.exception("Error creating shapefile")
            raise AssertionError("could not write XY point to shp file")
        # delete the writer to flush features to disk
        del writer

    def pop_up_finished(self):
        header = "Raster checker is finished"
        if self.need_to_create_shp:
            msg = (
                "The check results have been written to: \n %s \n "
                "The coordinates of wrong pixels are written to: \n"
                "%s" % (self.results.log_path, self.shape_path)
            )
        else:
            msg = "The check results have been written to:\n%s" % self.results.log_path
        pop_up_info(msg, header)

    def add_shp_to_iface(self):
        basename = ""
        provider = "ogr"
        from qgis.utils import iface

        layer = iface.addVectorLayer(self.shape_path, basename, provider)
        if not layer:
            logger.error("Layer %s failed to load!", self.shape_path)

    def pop_up_finished_or_question(self):
        """3 things (columns below) can be true or false. Dependent on that we
        return a pop_up_info (user clicks okay),
        pop_up_question (user clicks yes/no), Assertionerror

            self.results.nr_error_logrows   self.need_to_create_shp self.too_many_wrong_pixels (more rows than shp can handle)
            count_error > 0                 shp contains pixels     too many pixels for shp
        1.  True                            False                   False   --> pop_up_info
        2.  True                            False                   True    --> pop_up_info + warning
        3.  True                            True                    False   --> pop_up_question
        4.  True                            True                    True    --> pop_up_question + warning
        5.  False                           False                   False   --> pop_up_info
        6.  False                           False                   True    --> raise AssertionError
        7.  False                           True                    False   --> raise AssertionError
        8.  False                           True                    True    --> raise AssertionError
        """

        a = self.results.nr_error_logrows
        b = self.need_to_create_shp
        c = self.too_many_wrong_pixels

        header = "Raster checker is finished"
        question = "Do you want to add .shp to current view?"

        # case 1
        if a > 0 and not b and not c:
            # pop_up_info
            msg = (
                "Found %d errors (see .logger) and no wrong pixels. \n\n"
                "The check results have been written to: \n "
                "%s" % (self.results.nr_error_logrows, self.results.log_path)
            )
            pop_up_info(msg, header)
        # case 2
        elif a > 0 and not b and c:
            # pop_up_info + warning
            msg = (
                "Found %d errors (see .logger). \n"
                "Found too many wrong pixels to write to .shp file "
                "(see .logger). \n\n "
                "The check results have been written to: \n "
                "%s" % (self.results.nr_error_logrows, self.results.log_path)
            )
            pop_up_info(msg, header)
        # case 3
        elif a > 0 and b and not c:
            # pop_up_question
            msg = (
                "Found %d errors and some wrong pixels. \n\n "
                "The check results have been written to: \n %s \n\n "
                "The coordinates of wrong pixels are written to: \n %s"
                % (
                    self.results.nr_error_logrows,
                    self.results.log_path,
                    self.shape_path,
                )
            )
            pop_up_info(msg, header)
            if pop_up_question(question, "Add shapefile?"):
                self.add_shp_to_iface()
        # case 4
        elif a > 0 and b and c:
            # pop_up_question + warning
            msg = (
                "Found %d errors and some wrong pixels. \n "
                "Also found for 1 or more rasters too many wrong pixels "
                "to write to .shp file. \n\n"
                "The check results have been written to: \n %s \n\n "
                "The coordinates of wrong pixels are written to: \n %s"
                % (
                    self.results.nr_error_logrows,
                    self.results.log_path,
                    self.shape_path,
                )
            )
            pop_up_info(msg, header)
            if pop_up_question(question, "Add shapefile?"):
                self.add_shp_to_iface()
        # case 5
        elif a == 0 and not b and not c:
            # pop_up_info()
            msg = (
                "Found no errors (see .logger) and no wrong pixels. \n\n "
                "The check results have been written to: \n "
                "%s" % self.results.log_path
            )
            pop_up_info(msg, header)
        # scenario 6, 7, or 8
        elif a == 0 and b ^ c:
            raise AssertionError("this result combination is impossible")

    def run(self, tasks):
        """ runs the Raster checks.
        :param tasks: list with strings dependent on what user selected
        ['check all rasters', 'improve rasters] <-- latter is optional """

        self.run_all_checks()

        # TODO: improve rasters here
        # if 'improve rasters' in tasks:
        #     pass

        self.close_session()
        self.results.sort_results()
        # write and save logger file (here the self.results.log_path is created)
        self.results.write_log(self.entries_metadata)

        # only create shp if wrong pixels found
        self.need_to_create_shp = bool(self.input_data_shp)

        if self.need_to_create_shp:
            self.create_shp()

        # delete progress bar
        self.progress_bar.__del__()

        self.pop_up_finished_or_question()
