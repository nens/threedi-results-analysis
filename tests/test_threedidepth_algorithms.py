from pathlib import Path

from qgis.core import QgsProcessingContext, QgsProcessingFeedback
from threedi_results_analysis.processing.threedidepth_algorithms import WaterDepthOrLevelSingleTimeStepAlgorithm
from threedi_results_analysis.tests.utilities import TMP_DIR
from threedi_results_analysis import PLUGIN_DIR

DATA_DIR = PLUGIN_DIR / "tests" / "data" / "water_quality_results"

# concentration_raster_single_time_step_algorithm_inputs = {
#     'GRIDADMIN_INPUT': DATA_DIR / "gridadmin.h5",
#     'NETCDF_INPUT': DATA_DIR / "water_quality_results_3di.nc",
#     'WATERDEPTH_INPUT': None,
#     'SUBSTANCE_INPUT': 'substance1',
#     'COLOR_INPUT': QColor(165, 42, 42), 'MODE_INPUT': 1, 'CALCULATION_STEP_INPUT': 3,
#     'OUTPUT_FILENAME': TMP_DIR / "concentration_raster_single_time_step"
# }

water_depth_single_time_step_algorithm_inputs = {
    'GRIDADMIN_INPUT': str(DATA_DIR / "gridadmin.h5"),
    'NETCDF_INPUT': str(DATA_DIR / "results_3di.nc"),
    'DEM_INPUT': str(DATA_DIR / "schematisation" / "rasters" / "dem.tif"),
    'MODE_INPUT': 0,
    'CALCULATION_STEP_INPUT': 3,
    'OUTPUT_FILENAME': str(Path(TMP_DIR) / "water_depth_single_time_step.tif")
}


def test_water_depth_algorithm(tmp_path):
    alg = WaterDepthOrLevelSingleTimeStepAlgorithm()

    # Create the QGIS processing context & feedback
    context = QgsProcessingContext()
    feedback = QgsProcessingFeedback()

    # Define your input parameters dictionary (keys must match your algorithm)
    parameters = water_depth_single_time_step_algorithm_inputs

    # Run algorithm directly
    result = alg.run(parameters, context, feedback)

    # Assertions
    assert result is not None
    assert water_depth_single_time_step_algorithm_inputs["OUTPUT_FILENAME"].exists()
