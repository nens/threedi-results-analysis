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

from threedi_results_analysis.utils.utils import get_authority_code

STYLE_DIR = Path(__file__).parent / "styles"


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


def get_arrays(raster1, raster2):
    raster1_extend = get_extent(raster1)
    raster2_extend = get_extent(raster2)
    if raster1_extend == raster2_extend:
        raster1_array = raster1.ReadAsArray()
        raster2_array = raster2.ReadAsArray()
        gt = raster1.GetGeoTransform()
    else:
        shared_extent = get_shared_extent(raster1_extend, raster2_extend)
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
    return raster1_array, raster2_array, gt


def replace_no_data_values(raster, raster_array):
    ndv = raster.GetRasterBand(1).GetNoDataValue()
    raster_array[np.where(raster_array == ndv)] = 0
    return raster_array


def water_depth_diff(reference: Path | str, compare: Path | str, output: Path | str):
    """
    Calculate difference between two overlapping water depth tiffs. Result is compare - reference.
    Regards nodata as 0 water depth
    Nodatavalue of output is always 0
    If input rasters have different extents, difference raster will be calculated for the overlapping part of the input
    rasters
    """
    output = Path(output)

    reference_raster = gdal.Open(reference)
    compare_raster = gdal.Open(compare)

    # raise error if pixel sizes differ
    if not (reference_raster.GetGeoTransform()[1] == compare_raster.GetGeoTransform()[1] and
            reference_raster.GetGeoTransform()[5] == compare_raster.GetGeoTransform()[5]):
        raise ValueError("Input rasters have different pixel sizes")

    # raise error if pixel skews differ
    if not (reference_raster.GetGeoTransform()[2] == compare_raster.GetGeoTransform()[2] and
            reference_raster.GetGeoTransform()[4] == compare_raster.GetGeoTransform()[4]):
        raise ValueError("Input rasters have different pixel skew")

    # raise error if projections differ
    # compare on EPSG code to prevent errors from insignificant differences between the projections
    authority_code_reference = get_authority_code(reference_raster)
    authority_code_compare = get_authority_code(compare_raster)
    if not authority_code_reference == authority_code_compare:
        raise ValueError(f"Input rasters have different CRS ({authority_code_reference} vs {authority_code_compare}")

    # Clip rasters if they do not have the same extent
    reference_array, compare_array, gt = get_arrays(reference_raster, compare_raster)

    # Replace all nodata pixels by 0
    reference_array = replace_no_data_values(reference_raster, reference_array)
    compare_array = replace_no_data_values(compare_raster, compare_array)

    # Calculate difference
    result = np.subtract(compare_array, reference_array)

    # Write to raster with 0 as nodatavalue
    height = result.shape[0]
    width = result.shape[1]
    wkt = reference_raster.GetProjection()

    if output.exists():
        output.unlink()
    dst_drv = gdal.GetDriverByName('GTiff')
    dst_ds = dst_drv.Create(
        str(output),
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
    REFERENCE = "REFERENCE"
    COMPARE = "COMPARE"
    OUTPUT = "OUTPUT"

    def createInstance(self):
        return WaterDepthDiffAlgorithm()

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.REFERENCE, "Water depth reference raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.COMPARE, "Water depth raster to compare"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                "Output raster",
                fileFilter="GeoTIFF (*.tif)"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        reference = self.parameterAsRasterLayer(parameters, self.REFERENCE, context)
        compare = self.parameterAsRasterLayer(parameters, self.COMPARE, context)
        self.output = self.parameterAsFileOutput(parameters, self.OUTPUT, context)

        water_depth_diff(reference.source(), compare.source(), self.output)
        layer = QgsProcessingUtils.mapLayerFromString(self.output, context)
        self.output_layer_id = layer.id()
        context.temporaryLayerStore().addMapLayer(layer)
        layer_details = QgsProcessingContext.LayerDetails(
            "Water depth difference [m]", context.project(), "Water depth difference [m]"
        )
        context.addLayerToLoadOnCompletion(layer.id(), layer_details)

        return {self.OUTPUT: self.output}

    def postProcessAlgorithm(self, context, feedback):
        output_layer = context.getMapLayer(self.output_layer_id)
        output_layer.loadNamedStyle(str(STYLE_DIR / "water_depth_difference.qml"))
        context.project().addMapLayer(output_layer)
        return {self.OUTPUT: self.output}

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
