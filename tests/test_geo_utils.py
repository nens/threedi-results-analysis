"""
Test geo utils.
"""
import numpy as np
from osgeo import gdal
from qgis.core import QgsCoordinateTransform
from threedi_results_analysis.tests.utilities import (
    ensure_qgis_app_is_initialized,
    create_test_raster,
    create_test_raster_with_defaults,
    OFFSET_X,
    OFFSET_Y,
)
from threedi_results_analysis.utils.geo_utils import (
    get_coord_transformation_instance,
    get_authority_code,
    get_extent,
    replace_no_data_values,
    get_shared_extent,
    get_arrays,
)

import pytest

gdal.UseExceptions()


@pytest.fixture
def rdnew_to_wgs84():
    ensure_qgis_app_is_initialized()
    src_epsg, dest_epsg = 28992, 4326
    transformer = get_coord_transformation_instance(src_epsg, dest_epsg)
    return transformer


@pytest.fixture
def wgs84_to_rdnew():
    ensure_qgis_app_is_initialized()
    src_epsg, dest_epsg = 4326, 28992
    transformer = get_coord_transformation_instance(src_epsg, dest_epsg)
    return transformer


def test_get_coord_transformation_instance(rdnew_to_wgs84, wgs84_to_rdnew):
    assert isinstance(rdnew_to_wgs84, QgsCoordinateTransform)
    assert isinstance(wgs84_to_rdnew, QgsCoordinateTransform)


def test_get_coord_transformation_epsg(rdnew_to_wgs84):
    assert rdnew_to_wgs84.sourceCrs().isValid()
    assert rdnew_to_wgs84.sourceCrs().authid() == "EPSG:28992"
    assert rdnew_to_wgs84.destinationCrs().isValid()
    assert rdnew_to_wgs84.destinationCrs().authid() == "EPSG:4326"


def test_get_coord_transformation_epsg_reverse(wgs84_to_rdnew):
    assert wgs84_to_rdnew.sourceCrs().isValid()
    assert wgs84_to_rdnew.sourceCrs().authid() == "EPSG:4326"
    assert wgs84_to_rdnew.destinationCrs().isValid()
    assert wgs84_to_rdnew.destinationCrs().authid() == "EPSG:28992"


@pytest.mark.parametrize("epsg_code, expected_epsg_code", [
    (28992, 'EPSG:28992'),
    (None, None)
])
def test_get_authority_code(tmpdir, epsg_code, expected_epsg_code):
    outpath = tmpdir.join("test.tif")
    raster_file = create_test_raster(str(outpath), np.zeros((10, 10)), origin_x=0, origin_y=0, epsg_code=epsg_code)
    raster = gdal.Open(raster_file)
    assert get_authority_code(raster) == expected_epsg_code


def get_raster(array_data, origin_x, origin_y, no_data_value=-9999):
    raster_file = create_test_raster_with_defaults("temp.tif", array_data, origin_x, origin_y, no_data_value=no_data_value)
    return gdal.Open(raster_file)


def test_get_extent(raster_zeros):
    extent = get_extent(raster_zeros)
    np.testing.assert_array_equal(extent, (OFFSET_X, OFFSET_Y, OFFSET_X + 100, OFFSET_Y - 100))


def test_get_shared_extent(raster_zeros):
    raster_share = get_raster(np.zeros((10, 10)), OFFSET_X + 50, OFFSET_Y + 50)
    shared_extent = get_shared_extent(get_extent(raster_zeros), get_extent(raster_share))
    np.testing.assert_array_equal(shared_extent, (OFFSET_X + 50, OFFSET_Y, OFFSET_X + 100, OFFSET_Y - 50))


class TestGetArrays:

    def test_extent_mismatch(self):
        raster1 = get_raster(np.ones((10, 10)), origin_x=OFFSET_X, origin_y=OFFSET_Y)
        data2 = np.arange(100).reshape(10, 10)
        raster2 = get_raster(data2, origin_x=OFFSET_X + 50, origin_y=OFFSET_Y + 50)
        array1, array2, gt = get_arrays(raster1, raster2)
        np.testing.assert_array_equal(array1, np.ones((5, 5)))
        np.testing.assert_array_equal(array2, data2[5:, 0:5])
        np.testing.assert_array_equal(gt, (OFFSET_X + 50, 10, 0, OFFSET_Y, 0, -10))

    def test_extent_match(self):
        raster1 = get_raster(np.ones((10, 10)), origin_x=OFFSET_X, origin_y=OFFSET_Y)
        data2 = np.arange(100).reshape(10, 10)
        raster2 = get_raster(data2, origin_x=OFFSET_X, origin_y=OFFSET_Y)
        array1, array2, gt = get_arrays(raster1, raster2)
        np.testing.assert_array_equal(array1, np.ones((10, 10)))
        np.testing.assert_array_equal(array2, data2)
        np.testing.assert_array_equal(gt, (OFFSET_X, 10, 0, OFFSET_Y, 0, -10))


def test_replace_no_data_values():
    data = np.ones((10, 10))
    data[1, 1] = -9999
    data[3, 3] = -1337
    raster = get_raster(np.ones((10, 10)), origin_x=OFFSET_X, origin_y=OFFSET_Y, no_data_value=-1337)
    replace_no_data_values(raster, data)
    expected_data = np.ones((10, 10))
    expected_data[1, 1] = -9999
    expected_data[3, 3] = 0
    np.testing.assert_array_equal(data, expected_data)
