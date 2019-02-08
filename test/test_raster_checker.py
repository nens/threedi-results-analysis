"""
Test Raster Checker
"""
import unittest
import os

from gdal import GA_ReadOnly
from osgeo import gdal


# import mock  # python 2
# from mock import patch, Mock
import unittest.mock # python 3

from ThreeDiToolbox.utils.raster_checker import RasterChecker
from ThreeDiToolbox.utils.constants import RASTER_CHECKER_MAPPER
from ThreeDiToolbox.utils.threedi_database import ThreediDatabase
from ThreeDiToolbox.views.raster_checker_dialog import RasterCheckerDialogWidget  # noqa
from ThreeDiToolbox.utils.raster_checker_prework import (DataModelSource, RasterCheckerEntrees)  # noqa
from ThreeDiToolbox.utils.raster_checker_log import (RasterCheckerResults, RasterCheckerProgressBar)  # noqa
from sqlalchemy import MetaData


class TestRasterCheckerEntrees(unittest.TestCase):
    """Test the QGIS Environment"""

    def setUp(self):
        here = os.path.split(os.path.abspath(__file__))[0]
        sqlite_filename = 'rasterchecker_2entree_5tiff.sqlite'
        self.test_sqlite_path = os.path.join(here, 'data', sqlite_filename)
        db_type = 'spatialite'
        db_set = {'db_path': self.test_sqlite_path}
        db = ThreediDatabase(db_set, db_type)
        session = db.get_session()
        engine = db.get_engine()
        self.metadata = MetaData(bind=engine)
        self.datamodel = DataModelSource(self.metadata)
        self.rc_entrees =  RasterCheckerEntrees(self.datamodel, session)
        self.all_raster_ref_expect = [
            ('v2_global_settings', 1, 'dem_file', 'rasters/test1.tif'),
            ('v2_global_settings', 2, 'dem_file', 'rasters/test3.tif'),
            ('v2_global_settings', 2, 'frict_coef_file', 'rasters/test2.tif'),
            ('v2_groundwater', 4, 'leakage_file', 'rasters/test2.tif'),
            ('v2_interflow', 1, 'porosity_file', 'rasters/test1.tif')]

    def test_datamodel_v2weir_name(self):
        self.assertEqual(self.datamodel.v2_weir.name, 'v2_weir')

    def test_sqlite_and_rasters_found(self):
        # sqlite exists?
        self.assertTrue(os.path.isfile(self.test_sqlite_path))
        # rasters exists?
        here = os.path.split(os.path.abspath(__file__))[0]
        for tif in ['test1.tif', 'test2.tif', 'test3.tif']:
            self.assertTrue(os.path.isfile(os.path.join(
                here, 'data', 'rasters', tif)))

    def test_get_all_raster_ref(self):
        self.assertTrue(hasattr(self.rc_entrees, "all_raster_ref"))
        all_raster_ref = self.rc_entrees.all_raster_ref
        self.assertEqual(len(all_raster_ref), len(self.all_raster_ref_expect))
        self.assertEqual(sorted(all_raster_ref), sorted(
            self.all_raster_ref_expect))

    def test_get_foreign_keys(self):
        self.assertTrue(hasattr(self.rc_entrees, "foreign_keys"))
        foreign_keys_expect = [
            ('v2_global_settings', 2, 'interflow_settings_id', 1),
            ('v2_global_settings', 1, 'groundwater_settings_id', 4)]
        foreign_keys = self.rc_entrees.foreign_keys
        self.assertEqual(len(foreign_keys), len(foreign_keys_expect))
        self.assertEqual(sorted(foreign_keys), sorted(foreign_keys_expect))

    def test_get_unique_setting_ids(self):
        self.assertTrue(hasattr(self.rc_entrees, "unique_setting_ids"))
        unique_setting_ids = self.rc_entrees.unique_setting_ids
        self.assertEqual(unique_setting_ids, [1, 2])

    def test_entrees(self):
        self.assertTrue(hasattr(self.rc_entrees, "entrees"))
        entrees = self.rc_entrees.entrees
        entrees_expect = {
            1: ('rasters/test1.tif', 'rasters/test2.tif'),
            2: ('rasters/test3.tif', 'rasters/test2.tif', 'rasters/test1.tif')}
        # do not sort entrees as that dict,values (=tuple with string) must have
        # specific order (dem = first)
        self.assertEqual(entrees, entrees_expect)

    def test_entrees_metadata(self):
        self.assertTrue(hasattr(self.rc_entrees, "entrees_metadata"))
        entrees = self.rc_entrees.entrees_metadata
        entrees_meta_expect = [
            (1, 'v2_global_settings', 'dem_file', 'rasters/test1.tif'),
            (1, 'v2_groundwater', 'leakage_file', 'rasters/test2.tif'),
            (2, 'v2_global_settings', 'dem_file', 'rasters/test3.tif'),
            (2, 'v2_global_settings', 'frict_coef_file', 'rasters/test2.tif'),
            (2, 'v2_interflow', 'porosity_file', 'rasters/test1.tif'),]
        self.assertEqual(len(entrees), len(entrees_meta_expect))
        self.assertEqual(sorted(entrees), sorted(entrees_meta_expect))


class TestRasterChecker(unittest.TestCase):
    """Test the QGIS Environment"""

    def setUp(self):
        here = os.path.split(os.path.abspath(__file__))[0]
        sqlite_filename = 'small_2019_01_2entree_4tiff.sqlite'
        self.test_sqlite_path = os.path.join(here, 'data', sqlite_filename)
        self.test_sqlite_dir = os.path.split(self.test_sqlite_path)[0]
        db_type = 'spatialite'
        db_set = {'db_path': self.test_sqlite_path}
        self.db = ThreediDatabase(db_set, db_type)
        self.checker = RasterChecker(self.db)
        self.entrees_expect = {
            1: ('rasters/test1.tif', 'rasters/test2.tif'),
            2: ('rasters/test3.tif', 'rasters/test2.tif', 'rasters/test12.tif')}

    def test_has_raster_checker_run_method(self):
        self.assertTrue(hasattr(self.checker, 'run'))

    def test_get_check_ids_names(self):
        pass

    def test_check_defined_in_constants_exist_as_method(self):
        # test if checks defined in ..utils.constants.RASTER_CHECKER_MAPPER
        # exists as methods in self.checker
        method_names = [chck.get('base_check_name') for chck in
                        RASTER_CHECKER_MAPPER]
        methods_expect = ['id_tifname_unique', 'tif_exists', 'extension',
                          'filename', 'singleband', 'nodata', 'utm', 'flt32',
                          'compress', 'pixel_decimal', 'square_pixel',
                          'extreme_value', 'cum_pixel_cnt', 'proj',
                          'pixelsize', 'cnt_nodata', 'extent',
                          'pixel_alignment']
        self.assertEqual(sorted(method_names), sorted(methods_expect))
        prefix = "check_"
        for base_check_name in method_names:
            check_name = prefix + base_check_name
            self.assertTrue(hasattr(self.checker, check_name))

    def test_check_defined_in_constants_uniqueness(self):
        # test if checks defined in ..utils.constants.RASTER_CHECKER_MAPPER
        # have a unique check_i
        method_ids = [chck.get('check_id') for chck in
                      RASTER_CHECKER_MAPPER]
        self.assertTrue(len(method_ids) == len(list(set(method_ids))))

    def test_get_nr_phases(self):
        self.assertEqual(self.checker.get_nr_phases(run_pixel_checker=False), 4)
        self.assertEqual(self.checker.get_nr_phases(run_pixel_checker=True), 5)

    def test_result_per_check(self):
        """ each check should add a result (a list with dict per raster) to
        self.checker.results.result_per_check. We test two things:
        1. what happens we run a check with 1 raster?
        2. what happens we run a check with 2 rasters?
        """
        self.checker.results.result_per_check = []
        setting_id = 1; rast_item = 'xxxxx.tif'; check_id = 1
        # run a check "check_tif_exists"
        self.checker.check_tif_exists(setting_id, rast_item, check_id)
        # raster does not exists so we expect result is False
        expect = [{'check_id': 1, 'raster': 'xxxxx.tif', 'result': False,
                   'setting_id': 1, 'detail': ''}]
        self.assertEqual(self.checker.results.result_per_check, expect)

        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'test3.tif'; check_id = 13
        self.checker.check_tif_exists(setting_id, rast_item, check_id)
        setting_id = 1; rast_item = 'test1.tif'; check_id = 13
        self.checker.check_tif_exists(setting_id, rast_item, check_id)
        # both rasters exists so we expect result is True
        expect = [{'detail': '', 'result': False, 'check_id': 13,
                   'raster': 'test3.tif', 'setting_id': 2},
                  {'detail': '', 'result': False, 'check_id': 13,
                   'raster': 'test1.tif', 'setting_id': 1}]
        self.assertEqual(self.checker.results.result_per_check, expect)

    def get_result(self,):
        """ this is not a test, but just a helperfunction to get the result for
        result_per_check. From now on, we only compare result of a check with
        what we expect (instead of the whole dict..) """
        result = [x.get('result') for x in
                  self.checker.results.result_per_check][0]
        return result

    def test_id_tifname_unique(self):
        self.assertTrue(hasattr(self.checker, "check_id_tifname_unique"))
        self.checker.results.result_per_check = []
        setting_id = 1; rast_item = 'abc.tif'; check_id = 1
        self.checker.check_id_tifname_unique(setting_id, rast_item, check_id)
        self.assertTrue(self.get_result())  # rastername is unique

        setting_id = 1; rast_item = 'abc.tif'; check_id = 1
        self.checker.check_id_tifname_unique(setting_id, rast_item, check_id)
        res = [x.get('result') for x in self.checker.results.result_per_check]
        self.assertEqual(res, [True, False])  #2nd tifname isnt unique anymore

    def test_check_tif_exists(self):
        self.assertTrue(hasattr(self.checker, "check_tif_exists"))
        self.checker.results.result_per_check = []
        setting_id = 1; rast_item = 'xxxxx.tif'; check_id = 1
        self.checker.check_tif_exists(setting_id, rast_item, check_id)
        self.assertFalse(self.get_result()) # raster does not exists so we expect False

        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'rasters/test3.tif'; check_id = 13
        self.checker.check_tif_exists(setting_id, rast_item, check_id)
        self.assertTrue(self.get_result()) # raster does exists so we expect True

    def test_check_extension(self):
        self.assertTrue(hasattr(self.checker, "check_extension"))
        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'rasters/test3.tif'; check_id = 13
        self.checker.check_extension(setting_id, rast_item, check_id)
        self.assertTrue(self.get_result()) # True as extension is 'tiff'/'tif'

        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'rasters/test3.txt'; check_id = 2
        self.checker.check_extension(setting_id, rast_item, check_id)
        result = [x.get('result') for x in
                  self.checker.results.result_per_check][0]
        self.assertFalse(result) # False as extension is not 'tiff'/'tif'

    def test_check_filename(self):
        self.assertTrue(hasattr(self.checker, "check_filename"))
        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'rasters/test3.tif'; check_id = 13
        self.checker.check_filename(setting_id, rast_item, check_id)
        self.assertTrue(self.get_result())  # True as filename is valid

        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'rasters/te-st3.tif'; check_id = 13
        self.checker.check_filename(setting_id, rast_item, check_id)
        self.assertFalse(self.get_result())  # True as filename is invalid

    def test_check_singleband(self):
        raster_path = os.path.join(self.test_sqlite_dir, 'rasters/test1.tif')
        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'rasters/test1.tif'; check_id = 13
        src_ds = gdal.Open(raster_path, GA_ReadOnly)
        self.checker.check_singleband(setting_id, rast_item, check_id, src_ds)
        src_ds = None
        self.assertTrue(self.get_result())  # True as test1.tif is singleband

    def test_check_nodata(self):
        raster_path = os.path.join(self.test_sqlite_dir, 'rasters/test1.tif')
        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'rasters/test1.tif'; check_id = 13
        src_ds = gdal.Open(raster_path, GA_ReadOnly)
        self.checker.check_nodata(setting_id, rast_item, check_id, src_ds)
        src_ds = None
        self.assertTrue(self.get_result())  # True as test1.tif has nodata=-9999

    def test_check_utm(self):
        raster_path = os.path.join(self.test_sqlite_dir, 'rasters/test1.tif')
        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'rasters/test1.tif'; check_id = 13
        src_ds = gdal.Open(raster_path, GA_ReadOnly)
        self.checker.check_utm(setting_id, rast_item, check_id, src_ds)
        src_ds = None
        self.assertTrue(self.get_result())  # True as unit is 'metre' (UTM)

    def test_check_flt32(self):
        raster_path = os.path.join(self.test_sqlite_dir, 'rasters/test1.tif')
        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'rasters/test1.tif'; check_id = 13
        src_ds = gdal.Open(raster_path, GA_ReadOnly)
        self.checker.check_flt32(setting_id, rast_item, check_id, src_ds)
        src_ds = None
        self.assertTrue(self.get_result())

    def test_check_compress(self):
        raster_path = os.path.join(self.test_sqlite_dir, 'rasters/test1.tif')
        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'rasters/test1.tif'; check_id = 13
        src_ds = gdal.Open(raster_path, GA_ReadOnly)
        self.checker.check_compress(setting_id, rast_item, check_id, src_ds)
        src_ds = None
        self.assertTrue(self.get_result())

    def test_check_pixel_decimal(self):
        raster_path = os.path.join(self.test_sqlite_dir, 'rasters/test1.tif')
        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'rasters/test1.tif'; check_id = 13
        src_ds = gdal.Open(raster_path, GA_ReadOnly)
        self.checker.check_pixel_decimal(
            setting_id, rast_item, check_id, src_ds)
        src_ds = None
        self.assertTrue(self.get_result())

    def test_check_square_pixel(self):
        raster_path = os.path.join(self.test_sqlite_dir, 'rasters/test1.tif')
        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'rasters/test1.tif'; check_id = 13
        src_ds = gdal.Open(raster_path, GA_ReadOnly)
        self.checker.check_square_pixel(
            setting_id, rast_item, check_id, src_ds)
        src_ds = None
        self.assertTrue(self.get_result())

    def test_check_extreme_value(self):
        raster_path = os.path.join(self.test_sqlite_dir,
                                   'rasters/test1.tif')
        self.checker.results.result_per_check = []
        setting_id = 2; rast_item = 'rasters/test1.tif'; check_id = 13
        src_ds = gdal.Open(raster_path, GA_ReadOnly)
        self.checker.check_extreme_value(
            setting_id, rast_item, check_id, src_ds)
        src_ds = None
        self.assertTrue(self.get_result())

    def test_check_cum_pixel_cnt(self):
        rasters = [
            'rasters/test3.tif', 'rasters/test2.tif', 'rasters/test1.tif']
        setting_id = 2; check_id = 12
        self.checker.results.result_per_check = []
        self.checker.check_cum_pixel_cnt(rasters, setting_id, check_id)
        src_ds = None
        self.assertTrue(self.get_result())

    def test_check_proj(self):
        dem = 'rasters/test1.tif'
        rast_item = 'rasters/test2.tif'
        dem_path = os.path.join(self.test_sqlite_dir, dem)
        other_path = os.path.join(self.test_sqlite_dir, rast_item)
        dem_src_ds = gdal.Open(dem_path, GA_ReadOnly)
        src_ds = gdal.Open(other_path, GA_ReadOnly)
        setting_id = 2; check_id = 12
        self.checker.results.result_per_check = []
        self.checker.check_proj(
            setting_id, rast_item, check_id, src_ds, dem_src_ds)
        dem_src_ds = None
        src_ds = None
        self.assertTrue(self.get_result())

    def test_check_pixelsize(self):
        dem = 'rasters/test1.tif'
        rast_item = 'rasters/test2.tif'
        dem_path = os.path.join(self.test_sqlite_dir, dem)
        other_path = os.path.join(self.test_sqlite_dir, rast_item)
        dem_src_ds = gdal.Open(dem_path, GA_ReadOnly)
        src_ds = gdal.Open(other_path, GA_ReadOnly)
        setting_id = 2; check_id = 12
        self.checker.results.result_per_check = []
        self.checker.check_pixelsize(
            setting_id, rast_item, check_id, src_ds, dem_src_ds)
        dem_src_ds = None
        src_ds = None
        self.assertTrue(self.get_result())

    def test_check_cnt_nodata(self):
        # this test updates appends two lists (with dicts). Test both lists!
        self.checker.results.result_per_check = []
        self.checker.results.store_cnt_data_nodata = []
        dem = 'rasters/test1.tif'
        rast_item = 'rasters/test2.tif'
        dem_path = os.path.join(self.test_sqlite_dir, dem)
        other_path = os.path.join(self.test_sqlite_dir, rast_item)
        dem_src_ds = gdal.Open(dem_path, GA_ReadOnly)
        src_ds = gdal.Open(other_path, GA_ReadOnly)
        setting_id = 1; check_id = 12
        self.checker.check_cnt_nodata(
            setting_id, rast_item, check_id, src_ds, dem_src_ds)
        dem_src_ds = None
        src_ds = None
        self.assertFalse(self.get_result())  # False as counts are not equal
        store_cnt_data_nodata_expect = [{
            'setting_id': setting_id,
            'raster': rast_item,
            'cnt_data': 97,
            'cnt_nodata': 3,
            'dem_cnt_data': 98,
            'dem_cnt_nodata': 2}]
        self.assertEqual(self.checker.results.store_cnt_data_nodata,
                         store_cnt_data_nodata_expect)

    def test_check_extent(self):
        dem = 'rasters/test1.tif'
        rast_item = 'rasters/test2.tif'
        dem_path = os.path.join(self.test_sqlite_dir, dem)
        other_path = os.path.join(self.test_sqlite_dir, rast_item)
        dem_src_ds = gdal.Open(dem_path, GA_ReadOnly)
        src_ds = gdal.Open(other_path, GA_ReadOnly)
        setting_id = 2; check_id = 12
        self.checker.results.result_per_check = []
        self.checker.check_extent(
            setting_id, rast_item, check_id, src_ds, dem_src_ds)
        dem_src_ds = None
        src_ds = None
        self.assertTrue(self.get_result())

    def test_pixel_alignment(self):
        """" this test updates appends two lists (with dicts). we test both """
        self.checker.results.result_per_check = []      # test this list
        self.checker.input_data_shp = []                # test this list

        dem = 'rasters/test1.tif'
        rast_item = 'rasters/test2.tif'
        setting_id = 2; check_id = 12

        self.checker.results.store_cnt_data_nodata = [{
            'cnt_data': 97, 'cnt_nodata': 3, 'dem_cnt_data': 96,
            'dem_cnt_nodata': 4, 'raster': 'rasters/test2.tif',
            'setting_id': 2}]

        self.checker.progress_bar = unittest.mock.MagicMock()
        self.checker.check_pixel_alignment(
            setting_id, rast_item, check_id, dem)
        dem_src_ds = None
        src_ds = None
        result = self.get_result()
        self.assertFalse(result)

        input_data_shp_expect = [{
            'raster': rast_item,
            'coords': [[[8.5, 1.5], [0.5, 0.5], [0.5, 6.5]]],
            'setting_id': setting_id}]
        self.assertEqual(self.checker.input_data_shp, input_data_shp_expect)

    def test_phase_update(self):
        # TODO:
        pass