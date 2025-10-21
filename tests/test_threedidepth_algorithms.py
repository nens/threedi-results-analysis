from pathlib import Path
import pytest

from qgis.core import QgsProcessingContext, QgsProcessingFeedback
from qgis.PyQt.QtGui import QColor
from threedi_results_analysis.processing.threedidepth_algorithms import (
    WaterDepthOrLevelSingleTimeStepAlgorithm,
    WaterDepthOrLevelMultipleTimeStepAlgorithm,
    WaterDepthOrLevelMaximumAlgorithm,
    ConcentrationSingleTimeStepAlgorithm,
    ConcentrationMultipleTimeStepAlgorithm,
    ConcentrationMaximumAlgorithm,
)
from threedi_results_analysis.tests.utilities import TMP_DIR
from threedi_results_analysis import PLUGIN_DIR


DATA_DIR = PLUGIN_DIR / "tests" / "data" / "water_quality_results"

water_depth_single_time_step_algorithm_inputs = {
    'GRIDADMIN_INPUT': str(DATA_DIR / "gridadmin.h5"),
    'NETCDF_INPUT': str(DATA_DIR / "results_3di.nc"),
    'DEM_INPUT': str(DATA_DIR / "schematisation" / "rasters" / "dem.tif"),
    'MODE_INPUT': 0,
    'CALCULATION_STEP_INPUT': 3,
    'OUTPUT_FILENAME': str(Path(TMP_DIR.name) / "water_depth_single_time_step.tif")
}

water_depth_multiple_time_step_algorithm_inputs = {
    'GRIDADMIN_INPUT': str(DATA_DIR / "gridadmin.h5"),
    'NETCDF_INPUT': str(DATA_DIR / "results_3di.nc"),
    'DEM_INPUT': str(DATA_DIR / "schematisation" / "rasters" / "dem.tif"),
    'MODE_INPUT': 0,
    'CALCULATION_STEP_START_INPUT': 1,
    'CALCULATION_STEP_END_INPUT': 3,
    'OUTPUT_FILENAME': str(Path(TMP_DIR.name) / "water_depth_multiple_time_step.tif")
}

water_depth_maximum_algorithm_inputs = {
    'GRIDADMIN_INPUT': str(DATA_DIR / "gridadmin.h5"),
    'NETCDF_INPUT': str(DATA_DIR / "results_3di.nc"),
    'DEM_INPUT': str(DATA_DIR / "schematisation" / "rasters" / "dem.tif"),
    'MODE_INPUT': 0,
    'OUTPUT_FILENAME': str(Path(TMP_DIR.name) / "water_depth_maximum.tif")
}

concentration_raster_single_time_step_algorithm_inputs = {
    'GRIDADMIN_INPUT': str(DATA_DIR / "gridadmin.h5"),
    'NETCDF_INPUT': str(DATA_DIR / "water_quality_results_3di.nc"),
    'WATERDEPTH_INPUT': str(DATA_DIR / "water_depth_03_00.tif"),
    'SUBSTANCE_INPUT': 'Rain (label)',
    'COLOR_INPUT': QColor(165, 42, 42),
    'MODE_INPUT': 1,
    'CALCULATION_STEP_INPUT': 3,
    'OUTPUT_FILENAME': str(Path(TMP_DIR.name) / "concentration_raster_single_time_step.tif")
}

concentration_raster_multiple_time_step_algorithm_inputs = {
    'GRIDADMIN_INPUT': str(DATA_DIR / "gridadmin.h5"),
    'NETCDF_INPUT': str(DATA_DIR / "water_quality_results_3di.nc"),
    'WATERDEPTH_INPUT': str(DATA_DIR / "water_depth_all_time_steps.tif"),
    'SUBSTANCE_INPUT': 'Rain (label)',
    'COLOR_INPUT': QColor(165, 42, 42),
    'MODE_INPUT': 1,
    'CALCULATION_STEP_START_INPUT': 0,
    'CALCULATION_STEP_END_INPUT': 4,
    'OUTPUT_FILENAME': str(Path(TMP_DIR.name) / "concentration_raster_multiple_time_step.tif")
}

concentration_raster_maximum_algorithm_inputs = {
    'GRIDADMIN_INPUT': str(DATA_DIR / "gridadmin.h5"),
    'NETCDF_INPUT': str(DATA_DIR / "water_quality_results_3di.nc"),
    'WATERDEPTH_INPUT': None,
    'SUBSTANCE_INPUT': 'Rain (label)',
    'COLOR_INPUT': QColor(165, 42, 42),
    'MODE_INPUT': 1,
    'OUTPUT_FILENAME': str(Path(TMP_DIR.name) / "concentration_raster_maximum.tif")
}


@pytest.mark.parametrize("alg, parameters", [
    (WaterDepthOrLevelSingleTimeStepAlgorithm, water_depth_single_time_step_algorithm_inputs),
    (WaterDepthOrLevelMultipleTimeStepAlgorithm, water_depth_multiple_time_step_algorithm_inputs),
    (WaterDepthOrLevelMaximumAlgorithm, water_depth_maximum_algorithm_inputs),
    (ConcentrationSingleTimeStepAlgorithm, concentration_raster_single_time_step_algorithm_inputs),
    (ConcentrationMultipleTimeStepAlgorithm, concentration_raster_multiple_time_step_algorithm_inputs),
    (ConcentrationMaximumAlgorithm, concentration_raster_maximum_algorithm_inputs),
])
def test_water_depth_algorithm(alg, parameters):

    # Create the QGIS processing context & feedback
    context = QgsProcessingContext()
    feedback = QgsProcessingFeedback()

    # Run algorithm directly
    result = alg.run(parameters, context, feedback)

    # Assertions
    assert result is not None
    assert Path(parameters["OUTPUT_FILENAME"]).exists()
