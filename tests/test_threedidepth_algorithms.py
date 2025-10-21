from pathlib import Path
from typing import Dict

import pytest

from qgis.core import QgsProcessingAlgorithm, QgsProcessingContext, QgsProcessingFeedback
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


@pytest.mark.parametrize("alg_class, parameters", [
    (WaterDepthOrLevelSingleTimeStepAlgorithm, water_depth_single_time_step_algorithm_inputs),
    (WaterDepthOrLevelMultipleTimeStepAlgorithm, water_depth_multiple_time_step_algorithm_inputs),
    (WaterDepthOrLevelMaximumAlgorithm, water_depth_maximum_algorithm_inputs),
    (ConcentrationSingleTimeStepAlgorithm, concentration_raster_single_time_step_algorithm_inputs),
    (ConcentrationMultipleTimeStepAlgorithm, concentration_raster_multiple_time_step_algorithm_inputs),
    (ConcentrationMaximumAlgorithm, concentration_raster_maximum_algorithm_inputs),
])
def test_water_depth_algorithm(alg_class: QgsProcessingAlgorithm, parameters: Dict):
    alg = alg_class()

    # Create the QGIS processing context & feedback
    context = QgsProcessingContext()
    feedback = QgsProcessingFeedback()

    output_file = Path(parameters["OUTPUT_FILENAME"])
    try:
        result = alg.run(parameters, context, feedback)
        assert result is not None
        assert output_file.exists()
    finally:
        if output_file.exists():
            output_file.unlink()
