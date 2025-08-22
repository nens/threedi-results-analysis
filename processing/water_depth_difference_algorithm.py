from pathlib import Path

import numpy as np
from osgeo import gdal, osr
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterFileDestination,
    QgsProcessingUtils,
)

gdal.UseExceptions()
osr.UseExceptions()

STYLE_DIR = Path(__file__).parent / "styles"


def get_authority_code(raster: gdal.Dataset) -> str | None:
    """
    Return authority code (e.g. EPSG:28992) for given raster
    Returns None if no projection is defined
    """
    wkt = raster.GetProjection()
    if not wkt:
        return None  # no projection defined

    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt)

    if srs.IsGeographic():
        key = "GEOGCS"
    else:
        key = "PROJCS"

    code = srs.GetAuthorityCode(key)
    auth = srs.GetAuthorityName(key)

    if code and auth:
        return f"{auth}:{code}"
    return None


def get_extent(raster):
    gt = raster.GetGeoTransform()
    ulx = gt[0]
    uly = gt[3]
    lrx = gt[0] + (raster.RasterXSize * gt[1])
    lry = gt[3] + (raster.RasterYSize * gt[5])  # '+' because gt[5] is negative
    return [ulx, uly, lrx, lry]


def get_shared_extent(extent1, extent2):
    ulx = max(extent1[0], extent2[0])
    uly = min(extent1[1], extent2[1])
    lrx = min(extent1[2], extent2[2])
    lry = max(extent1[3], extent2[3])

    return [ulx, uly, lrx, lry]


def water_depth_diff(raster1_fn: Path | str, raster2_fn: Path | str, output: Path | str):
    """
    Calculate difference between two overlapping water depth tiffs. Result is raster2 - raster1.
    Regards nodata as 0 water depth
    Nodatavalue of output is always 0
    If input rasters have different extents, difference raster will be calculated for the overlapping part of the input
    rasters
    """
    output = Path(output)

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
    authority_code_raster1 = get_authority_code(raster1)
    authority_code_raster2 = get_authority_code(raster2)
    if not authority_code_raster1 == authority_code_raster2:
        raise ValueError(f"Input rasters have different CRS ({authority_code_raster1} vs {authority_code_raster2}")

    # Clip rasters if they do not have the same extent
    raster1extent = get_extent(raster1)
    raster2extent = get_extent(raster2)

    if raster1extent == raster2extent:
        raster1_array = raster1.ReadAsArray()
        raster2_array = raster2.ReadAsArray()
        gt = raster1.GetGeoTransform()

    else:
        shared_extent = get_shared_extent(raster1extent, raster2extent)

        raster1_shared_extent = gdal.Translate('', raster1, format='MEM', projWin=shared_extent)
        raster1_array = raster1_shared_extent.ReadAsArray()
        raster1_shared_extent = None

        raster2_shared_extent = gdal.Translate('', raster2, format='MEM', projWin=shared_extent)
        raster2_array = raster2_shared_extent.ReadAsArray()
        raster2_shared_extent = None

        gt = list(raster1.GetGeoTransform())  # (upper_left_x, x_resolution, x_skew, upper_left_y, y_skew, y_resolution)
        gt[0] = shared_extent[0]
        gt[3] = shared_extent[1]
        gt = tuple(gt)

    # Replace all nodata pixels by 0
    ndv1 = raster1.GetRasterBand(1).GetNoDataValue()
    raster1_array[np.where(raster1_array == ndv1)] = 0
    ndv2 = raster2.GetRasterBand(1).GetNoDataValue()
    raster2_array[np.where(raster2_array == ndv2)] = 0

    # Calculate difference
    result = np.subtract(raster2_array, raster1_array)

    # Write to raster with 0 as nodatavalue
    height = result.shape[0]
    width = result.shape[1]
    wkt = raster1.GetProjection()

    if output.exists():
        output.unlink()

    dst_drv = gdal.GetDriverByName('GTiff')
    dst_ds = dst_drv.Create(
        output,
        xsize=width,
        ysize=height,
        bands=1,
        eType=gdal.GDT_Float32,
        options=["COMPRESS=DEFLATE", "PREDICTOR=2", "ZLEVEL=9", "TILED=YES", "BLOCKXSIZE=512", "BLOCKYSIZE=512"],
    )
    dst_ds.SetGeoTransform(gt)
    dst_ds.SetProjection(wkt)
    dst_ds.GetRasterBand(1).SetNoDataValue(0)
    dst_ds.GetRasterBand(1).WriteArray(result)
    dst_ds = None


class WaterDepthDiffAlgorithm(QgsProcessingAlgorithm):
    INPUT_RASTER1 = "INPUT_RASTER1"
    INPUT_RASTER2 = "INPUT_RASTER2"
    OUTPUT_RASTER = "OUTPUT_RASTER"

    def createInstance(self):
        return WaterDepthDiffAlgorithm()

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER1, "Water depth reference raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER2, "Water depth raster to compare"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_RASTER,
                "Output raster",
                fileFilter="GeoTIFF (*.tif)"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        raster1 = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER1, context)
        raster2 = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER2, context)
        self.output = self.parameterAsFileOutput(parameters, self.OUTPUT_RASTER, context)

        water_depth_diff(raster1.source(), raster2.source(), self.output)
        layer = QgsProcessingUtils.mapLayerFromString(self.output, context)
        self.output_layer_id = layer.id()
        context.temporaryLayerStore().addMapLayer(layer)
        layer_details = QgsProcessingContext.LayerDetails(
            "Water depth difference [m]", context.project(), "Water depth difference [m]"
        )
        context.addLayerToLoadOnCompletion(layer.id(), layer_details)

        return {self.OUTPUT_RASTER: self.output}

    def postProcessAlgorithm(self, context, feedback):
        output_layer = context.getMapLayer(self.output_layer_id)
        output_layer.loadNamedStyle(str(STYLE_DIR / "water_depth_difference.qml"))
        context.project().addMapLayer(output_layer)
        return {self.OUTPUT_RASTER: self.output}


    def name(self):
        return "water_depth_diff"

    def displayName(self):
        return "Water depth difference"

    def group(self):
        return "Post-process results"

    def groupId(self):
        return "postprocessing"

    def shortHelpString(self):
        return (
            "Calculate difference between two overlapping water depth rasters.\n\n"
            "The resulting values are [compare raster] - [reference raster]: "
            "negative values (green) mean the water depth has decreased, "
            "positive values (pink) mean the water depth has increased "
            "relative to the reference raster.\n\n"
            "Pixels with a difference of less than a centimeter are not visualised."
        )
