from pathlib import Path

from osgeo import gdal


def get_authority_code(raster: gdal.Dataset) -> str:
    """Return authority code (e.g. EPSG:28992) for given raster"""
    srs = raster.GetProjection()
    key = "GEOGCS" if srs.IsGeographic() else "PROJCS"
    return srs.GetAuthorityCode(key)


def water_depth_diff(raster1_fn: Path | str, raster2_fn: Path | str, output_fn: Path | str):
    """
    Calculate difference between two overlapping water depth tiffs. Result is raster2 - raster1.
    Regards nodata as 0 water depth
    Nodatavalue of output is always 0
    """
    raster1 = gdal.Open(raster1_fn)
    raster2 = gdal.Open(raster2_fn)

    # raise error if pixel sizes differ
    if not raster1.GetGeoTransform()[1] == raster2.GetGeoTransform()[1] and \
            raster1.GetGeoTransform()[5] == raster2.GetGeoTransform()[5]:
        raise ValueError("Input rasters have different pixel sizes")

    # raise error if pixel skews differ
    if not raster1.GetGeoTransform()[2] == raster2.GetGeoTransform()[2] and \
            raster1.GetGeoTransform()[4] == raster2.GetGeoTransform()[4]:
        raise ValueError("Input rasters have different pixel skew")

    # raise error if projections differ
    # compare on EPSG code to prevent errors from insignificant differences between the projections

    ## assert raster1.GetProjection() == raster2.GetProjection()

    # Als extents verschillen:
    # 2. Bepaal gemeenschappelijke extent
    # 3. Knip de rasters op die gemeenschappelijke extent met gdal.Translate
    # 4 Lees het resultaat van beiden in als array

    raster1extent = getExtent(raster1)
    raster2extent = getExtent(raster2)

    if raster1extent == raster2extent:
        raster1Array = raster1.ReadAsArray()
        raster2Array = raster2.ReadAsArray()
        gt = raster1.GetGeoTransform()

    else:
        sharedExtent = getSharedExtent(raster1extent, raster2extent)

        raster1SharedExt = gdal.Translate('', raster1, format='MEM', projWin=sharedExtent)
        raster1Array = raster1SharedExt.ReadAsArray()
        raster1SharedExt = None

        raster2SharedExt = gdal.Translate('', raster2, format='MEM', projWin=sharedExtent)
        raster2Array = raster2SharedExt.ReadAsArray()
        raster2SharedExt = None

        gt = list(raster1.GetGeoTransform())  # (upper_left_x, x_resolution, x_skew, upper_left_y, y_skew, y_resolution)
        gt[0] = sharedExtent[0]
        gt[3] = sharedExtent[1]
        gt = tuple(gt)

    # 5 Vervang alle nodatavalues door 0
    ndv1 = raster1.GetRasterBand(1).GetNoDataValue()
    raster1Array[np.where(raster1Array == ndv1)] = 0
    ndv2 = raster2.GetRasterBand(1).GetNoDataValue()
    raster2Array[np.where(raster2Array == ndv2)] = 0

    # 6 Bereken verschilarray
    result = np.subtract(raster2Array, raster1Array)

    # 7 Schrijf weg naar raster met 0 als nodatavalue
    height = result.shape[0]  # dit nog aanpassen als stap 2 & 3 worden geimplementeerd
    width = result.shape[1]  # dit nog aanpassen als stap 2 & 3 worden geimplementeerd

    wkt = raster1.GetProjection()

    if os.path.exists(output_fn):
        os.remove(output_fn)

    drv = gdal.GetDriverByName('Mem')
    ds = drv.Create('', xsize=width, ysize=height, bands=1, eType=gdal.GDT_Float32)
    ds.SetGeoTransform(gt)
    ds.SetProjection(wkt)
    ds.GetRasterBand(1).SetNoDataValue(0)
    ds.GetRasterBand(1).WriteArray(result)

    dst_drv = gdal.GetDriverByName('GTiff')
    dst_ds = dst_drv.CreateCopy(output_fn, ds, options=["TILED=YES", "COMPRESS=DEFLATE"])
    dst_ds = None
    ds = None

    ext_len = len(os.path.basename(output_fn).split('.')[-1])
    qml_fn = output_fn[:-1 * ext_len - 1] + '.qml'

    with open(qml_fn, "w") as qml:
        qml.write(STYLESTRING)
