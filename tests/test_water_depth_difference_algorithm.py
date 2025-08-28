import pytest
import tempfile
from pathlib import Path
from osgeo import gdal
import numpy as np
from threedi_results_analysis import PLUGIN_DIR
from threedi_results_analysis.tests.utilities import create_test_raster as create_test_raster_full
import threedi_results_analysis.processing.water_depth_difference_algorithm as wdda

RASTER_DIR = PLUGIN_DIR / "tests" / "data" / "rasters"

TMP_DIR = tempfile.TemporaryDirectory()
OUT_DIR = tempfile.TemporaryDirectory()
OFFSET_X, OFFSET_Y = 140000, 460000


def create_test_raster(filename, array_data, origin_x=OFFSET_X, origin_y=OFFSET_Y, pixel_width=10, pixel_height=-10,
                       epsg_code=28992, no_data_value=-9999, x_skew=0, y_skew=0):
    output_path = str(Path(TMP_DIR.name) / filename)
    return create_test_raster_full(
        output_path=output_path,
        array_data=array_data,
        origin_x=origin_x,
        origin_y=origin_y,
        pixel_width=pixel_width,
        pixel_height=pixel_height,
        epsg_code=epsg_code,
        no_data_value=no_data_value,
        x_skew=x_skew,
        y_skew=y_skew)


def get_raster(array_data, origin_x, origin_y, no_data_value=-9999):
    raster_file = create_test_raster("temp.tif", array_data, origin_x, origin_y, no_data_value=no_data_value)
    return gdal.Open(raster_file)


@pytest.fixture(scope='session')
def raster_zeros_file():
    return create_test_raster("zeros.tif", np.zeros((10, 10)))


@pytest.fixture(scope='session')
def raster_zeros(raster_zeros_file):
    return gdal.Open(raster_zeros_file)


@pytest.fixture(scope='session')
def raster_ones_file():
    return create_test_raster("ones.tif", np.ones((10, 10)))


@pytest.fixture(scope='session')
def raster_ones(raster_zeros_file):
    return gdal.Open(raster_zeros_file)


def test_get_extent(raster_zeros):
    extent = wdda.get_extent(raster_zeros)
    np.testing.assert_array_equal(extent, (OFFSET_X, OFFSET_Y, OFFSET_X + 100, OFFSET_Y - 100))


def test_get_shared_extent(raster_zeros):
    raster_share = get_raster(np.zeros((10, 10)), OFFSET_X + 50, OFFSET_Y + 50)
    shared_extent = wdda.get_shared_extent(wdda.get_extent(raster_zeros), wdda.get_extent(raster_share))
    np.testing.assert_array_equal(shared_extent, (OFFSET_X + 50, OFFSET_Y, OFFSET_X + 100, OFFSET_Y - 50))


class TestGetArrays:

    def test_extent_mismatch(self):
        raster1 = get_raster(np.ones((10, 10)), origin_x=OFFSET_X, origin_y=OFFSET_Y)
        data2 = np.arange(100).reshape(10, 10)
        raster2 = get_raster(data2, origin_x=OFFSET_X + 50, origin_y=OFFSET_Y + 50)
        array1, array2, gt = wdda.get_arrays(raster1, raster2)
        np.testing.assert_array_equal(array1, np.ones((5, 5)))
        np.testing.assert_array_equal(array2, data2[5:, 0:5])
        np.testing.assert_array_equal(gt, (OFFSET_X + 50, 10, 0, OFFSET_Y, 0, -10))

    def test_extent_match(self):
        raster1 = get_raster(np.ones((10, 10)), origin_x=OFFSET_X, origin_y=OFFSET_Y)
        data2 = np.arange(100).reshape(10, 10)
        raster2 = get_raster(data2, origin_x=OFFSET_X, origin_y=OFFSET_Y)
        array1, array2, gt = wdda.get_arrays(raster1, raster2)
        np.testing.assert_array_equal(array1, np.ones((10, 10)))
        np.testing.assert_array_equal(array2, data2)
        np.testing.assert_array_equal(gt, (OFFSET_X, 10, 0, OFFSET_Y, 0, -10))


def test_replace_no_data_values():
    data = np.ones((10, 10))
    data[1, 1] = -9999
    data[3, 3] = -1337
    raster = get_raster(np.ones((10, 10)), origin_x=OFFSET_X, origin_y=OFFSET_Y, no_data_value=-1337)
    wdda.replace_no_data_values(raster, data)
    expected_data = np.ones((10, 10))
    expected_data[1, 1] = -9999
    expected_data[3, 3] = 0
    np.testing.assert_array_equal(data, expected_data)


class TestWaterDepthDiff:

    @pytest.mark.parametrize("raster_args", [
        {'pixel_width': 20},
        {'pixel_height': -20},
        {'x_skew': 1},
        {'y_skew': 1},
    ])
    def test_geotransform_mismatch(self, raster_args):
        raster1_file = create_test_raster("raster1.tif", np.ones((10, 10)))
        raster2_file = create_test_raster("raster2.tif", np.ones((10, 10)), **raster_args)
        with pytest.raises(ValueError):
            wdda.water_depth_diff(raster1_file, raster2_file, "test.tif")

    def test_auth_code_diff(self):
        raster1_file = create_test_raster("raster1.tif", np.ones((10, 10)), epsg_code=28991)
        raster2_file = create_test_raster("raster2.tif", np.ones((10, 10)), epsg_code=28992)
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
        raster1_file = create_test_raster("raster1.tif", np.arange(100).reshape(10, 10))
        # 10x10 array with ones
        raster2_file = create_test_raster("raster2.tif", np.ones((10, 10)))
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
        raster1_file = create_test_raster("raster1.tif", data1, no_data_value=-9999)
        # 4x4 array filled with values 0 to 32 (increments of 2) an no data at (3,3)
        data2 = np.arange(0, 32, 2).reshape(4, 4)
        data2[3, 3] = -1337
        raster2_file = create_test_raster("raster2.tif", data2, no_data_value=-1337)
        wdda.water_depth_diff(raster1_file, raster2_file, output)
        expected_diff = data2 - data1
        expected_diff[1, 1] = data2[1, 1]
        expected_diff[3, 3] = -data1[3, 3]
        result = gdal.Open(str(output))
        np.testing.assert_array_equal(expected_diff, result.ReadAsArray())
