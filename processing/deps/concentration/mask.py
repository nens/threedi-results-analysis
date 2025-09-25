from osgeo import gdal
from pathlib import Path
import numpy as np

gdal.UseExceptions()

# TODO Use the checks and fixes from water depth difference algorithm here as well


def mask(source: str | Path, mask: str | Path, output: str | Path):
    """
    Masks source raster with mask, i.e. setting all pixels in source to nodata that have nodata in mask
    """
    # Open source raster
    source_ds = gdal.Open(str(source))
    source_band = source_ds.GetRasterBand(1)
    source_nodata = source_band.GetNoDataValue() or -9999
    source_array = source_band.ReadAsArray()

    # Open mask raster
    mask_ds = gdal.Open(str(mask))
    mask_band = mask_ds.GetRasterBand(1)
    mask_nodata = mask_band.GetNoDataValue()
    mask_array = mask_band.ReadAsArray()

    # Mask source where mask has nodata
    source_masked = np.where(mask_array == mask_nodata, source_nodata, source_array)
    
    # Create output file
    creation_options = [
        "COMPRESS=DEFLATE",
        "PREDICTOR=2",
        "ZLEVEL=9",
        "TILED=YES",
        "BLOCKXSIZE=512",
        "BLOCKYSIZE=512"
    ]
    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(
        str(output),
        source_ds.RasterXSize,
        source_ds.RasterYSize,
        1,
        source_band.DataType,
        options=creation_options
    )

    # Copy georeferencing
    out_ds.SetGeoTransform(source_ds.GetGeoTransform())
    out_ds.SetProjection(source_ds.GetProjection())

    # Write masked data
    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(source_masked)
    out_band.SetNoDataValue(source_nodata)
    out_band.FlushCache()
