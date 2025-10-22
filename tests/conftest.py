import numpy as np
import pytest
from osgeo import gdal

gdal.UseExceptions()

from threedi_results_analysis.tests.utilities import ensure_qgis_app_is_initialized, create_test_raster_with_defaults


@pytest.fixture(autouse=True)
def qgis_app_initialized():
    ensure_qgis_app_is_initialized()


@pytest.fixture(scope='session')
def raster_zeros_file():
    return create_test_raster_with_defaults("zeros.tif", np.zeros((10, 10)))


@pytest.fixture(scope='session')
def raster_zeros(raster_zeros_file):
    return gdal.Open(raster_zeros_file)


@pytest.fixture(scope='session')
def raster_ones_file():
    return create_test_raster_with_defaults("ones.tif", np.ones((10, 10)))


@pytest.fixture(scope='session')
def raster_ones(raster_zeros_file):
    return gdal.Open(raster_zeros_file)
