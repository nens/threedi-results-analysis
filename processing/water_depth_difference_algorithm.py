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

from threedi_results_analysis.utils.geo_utils import (
    get_arrays,
    replace_no_data_values,
)

gdal.UseExceptions()
osr.UseExceptions()

STYLE_DIR = Path(__file__).parent / "styles"


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
