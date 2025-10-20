"""
Test geo utils.
"""
import numpy as np
from osgeo import gdal
from qgis.core import QgsCoordinateTransform
from threedi_results_analysis.tests.utilities import ensure_qgis_app_is_initialized, create_test_raster
from threedi_results_analysis.utils.geo_utils import get_coord_transformation_instance, get_authority_code

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
