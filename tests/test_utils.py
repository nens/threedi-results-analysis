import pytest
import numpy as np
from osgeo import gdal

from threedi_results_analysis.utils.utils import get_authority_code

from threedi_results_analysis.tests.utilities import create_test_raster


@pytest.mark.parametrize("epsg_code, expected_epsg_code", [
    (28992, 'EPSG:28992'),
    (None, None)
])
def test_get_authority_code(tmpdir, epsg_code, expected_epsg_code):
    outpath = tmpdir.join("test.tif")
    raster_file = create_test_raster(str(outpath), np.zeros((10, 10)), origin_x=0, origin_y=0, epsg_code=epsg_code)
    raster = gdal.Open(raster_file)
    assert get_authority_code(raster) == expected_epsg_code
