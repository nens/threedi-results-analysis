import pytest
from pathlib import Path
from osgeo import gdal
import numpy as np
from threedi_results_analysis import PLUGIN_DIR
import threedi_results_analysis.processing.water_depth_difference_algorithm as wdda
from threedi_results_analysis.tests.utilities import (
    create_test_raster_with_defaults,
    OUT_DIR,
)

RASTER_DIR = PLUGIN_DIR / "tests" / "data" / "rasters"


class TestWaterDepthDiff:

    @pytest.mark.parametrize("raster_args", [
        {'pixel_width': 20},
        {'pixel_height': -20},
        {'x_skew': 1},
        {'y_skew': 1},
    ])
    def test_geotransform_mismatch(self, raster_args):
        raster1_file = create_test_raster_with_defaults("raster1.tif", np.ones((10, 10)))
        raster2_file = create_test_raster_with_defaults("raster2.tif", np.ones((10, 10)), **raster_args)
        with pytest.raises(ValueError):
            wdda.water_depth_diff(raster1_file, raster2_file, "test.tif")

    def test_auth_code_diff(self):
        raster1_file = create_test_raster_with_defaults("raster1.tif", np.ones((10, 10)), epsg_code=28991)
        raster2_file = create_test_raster_with_defaults("raster2.tif", np.ones((10, 10)), epsg_code=28992)
        with pytest.raises(ValueError):
            wdda.water_depth_diff(raster1_file, raster2_file, "test.tif")

    def test_water_depth_diff_zeros(self, raster_zeros_file, raster_ones_file):
        # assert data - zeros = data
        output = str(Path(OUT_DIR.name) / 'test.tif')
        wdda.water_depth_diff(raster_zeros_file, raster_ones_file, output)
        result = gdal.Open(str(output))
        np.testing.assert_array_equal(result.ReadAsArray(), np.ones((10, 10)))

    def test_water_depth_diff_equal(self, raster_ones_file):
        # assert a - a = 0
        output = str(Path(OUT_DIR.name) / 'test.tif')
        wdda.water_depth_diff(raster_ones_file, raster_ones_file, output)
        result = gdal.Open(str(output))
        np.testing.assert_array_equal(result.ReadAsArray(), np.zeros((10, 10)))

    def test_reverse_diff(self):
        # assert that a-b = -(b-a)
        output = str(Path(OUT_DIR.name) / 'test.tif')
        output_rev = str(Path(OUT_DIR.name) / 'test_rev.tif')
        # 10x10 array filled with value 0 to 99
        raster1_file = create_test_raster_with_defaults("raster1.tif", np.arange(100).reshape(10, 10))
        # 10x10 array with ones
        raster2_file = create_test_raster_with_defaults("raster2.tif", np.ones((10, 10)))
        wdda.water_depth_diff(raster1_file, raster2_file, output)
        result = gdal.Open(str(output))
        wdda.water_depth_diff(raster2_file, raster1_file, output_rev)
        result_rev = gdal.Open(str(output_rev))
        np.testing.assert_array_equal(result.ReadAsArray(), -result_rev.ReadAsArray())

    def test_water_depth(self):
        output = str(Path(OUT_DIR.name) / 'test.tif')
        # 4x4 array filled with value 0 to 16 and no data at (1,1)
        data1 = np.arange(16).reshape(4, 4)
        data1[1, 1] = -9999
        raster1_file = create_test_raster_with_defaults("raster1.tif", data1, no_data_value=-9999)
        # 4x4 array filled with values 0 to 32 (increments of 2) an no data at (3,3)
        data2 = np.arange(0, 32, 2).reshape(4, 4)
        data2[3, 3] = -1337
        raster2_file = create_test_raster_with_defaults("raster2.tif", data2, no_data_value=-1337)
        wdda.water_depth_diff(raster1_file, raster2_file, output)
        expected_diff = data2 - data1
        expected_diff[1, 1] = data2[1, 1]
        expected_diff[3, 3] = -data1[3, 3]
        result = gdal.Open(str(output))
        np.testing.assert_array_equal(expected_diff, result.ReadAsArray())
