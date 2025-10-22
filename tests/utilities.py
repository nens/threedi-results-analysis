# coding=utf-8
"""Common functionality used by regression tests."""
from contextlib import contextmanager
from pathlib import Path

from qgis.core import QgsApplication

import logging
import shutil
import tempfile
from osgeo import gdal, osr

gdal.UseExceptions()
osr.UseExceptions()

logger = logging.getLogger(__name__)
_singletons = {}

TMP_DIR = tempfile.TemporaryDirectory()
OUT_DIR = tempfile.TemporaryDirectory()
OFFSET_X, OFFSET_Y = 140000, 460000


def ensure_qgis_app_is_initialized():
    """Make sure qgis is initialized for testing."""
    # Note: if you just need the QT app to be there, you can use the qtbot fixture
    # from https://pytest-qt.readthedocs.io/en/latest/index.html
    if "app" not in _singletons:
        app = QgsApplication([], False)
        app.initQgis()
        logger.debug("Initialized qgis (for testing). Settings: %s", app.showSettings())
        _singletons["app"] = app


@contextmanager
def TemporaryDirectory():
    name = tempfile.mkdtemp()
    try:
        yield name
    finally:
        shutil.rmtree(name)


def create_test_raster(output_path, array_data, origin_x, origin_y, pixel_width=10, pixel_height=-10,
                       epsg_code=28992, no_data_value=-9999, x_skew=0, y_skew=0):
    """
    Create a test GeoTIFF raster file with given parameters

    Parameters:
    filename - output file path
    array_data - 2D numpy array with raster data
    origin_x, origin_y - coordinates of the upper left corner
    pixel_width, pixel_height - pixel size (height is usually negative)
    epsg_code - projection code (default: 28992 - Dutch RD New)
    """
    # Get dimensions
    rows, cols = array_data.shape

    # Create driver
    driver = gdal.GetDriverByName('GTiff')

    # Create dataset with 1 band
    out_raster = driver.Create(
        output_path,
        cols, rows, 1,
        gdal.GDT_Float32,
        options=["COMPRESS=DEFLATE", "PREDICTOR=2", "TILED=YES"]
    )

    # Set geotransform (upper_left_x, pixel_width, x_skew, upper_left_y, y_skew, pixel_height)
    out_raster.SetGeoTransform((origin_x, pixel_width, x_skew, origin_y, y_skew, pixel_height))

    # Set projection
    if epsg_code is not None:
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(epsg_code)
        out_raster.SetProjection(srs.ExportToWkt())

    # Write data
    band = out_raster.GetRasterBand(1)
    band.SetNoDataValue(no_data_value)  # Set NoData value
    band.WriteArray(array_data)

    # Clean up
    band.FlushCache()
    out_raster = None
    return str(output_path)


def create_test_raster_with_defaults(
        filename,
        array_data,
        origin_x=OFFSET_X,
        origin_y=OFFSET_Y,
        pixel_width=10,
        pixel_height=-10,
        epsg_code=28992,
        no_data_value=-9999,
        x_skew=0,
        y_skew=0
):
    output_path = str(Path(TMP_DIR.name) / filename)
    return create_test_raster(
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
