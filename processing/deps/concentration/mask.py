from osgeo import gdal
from pathlib import Path
import numpy as np

gdal.UseExceptions()


# TODO Use the checks and fixes from water depth difference algorithm here as well
def mask(source: str | Path, mask: str | Path, output: str | Path):
    """
    Masks source raster with mask: sets all pixels in source to nodata
    wherever mask has nodata. Supports single- and multi-band rasters
    (with the same number of bands).
    """
    # Open source and mask datasets
    source_ds = gdal.Open(str(source))
    mask_ds = gdal.Open(str(mask))

    bands = source_ds.RasterCount
    mask_bands = mask_ds.RasterCount
    if bands != mask_bands:
        raise ValueError(f"Source has {bands} bands, mask has {mask_bands} bands")

    # Prepare output dataset
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
        bands,
        source_ds.GetRasterBand(1).DataType,
        options=creation_options
    )
    out_ds.SetGeoTransform(source_ds.GetGeoTransform())
    out_ds.SetProjection(source_ds.GetProjection())

    # Process band by band
    for i in range(1, bands + 1):  # GDAL bands are 1-based
        source_band = source_ds.GetRasterBand(i)
        source_nodata = source_band.GetNoDataValue() or -9999
        source_array = source_band.ReadAsArray()

        mask_band = mask_ds.GetRasterBand(i if mask_bands > 1 else 1)
        mask_nodata = mask_band.GetNoDataValue()
        mask_array = mask_band.ReadAsArray()

        # Apply masking
        source_masked = np.where(mask_array == mask_nodata, source_nodata, source_array)

        # Write out band
        out_band = out_ds.GetRasterBand(i)
        out_band.WriteArray(source_masked)
        out_band.SetNoDataValue(source_nodata)
        out_band.FlushCache()
