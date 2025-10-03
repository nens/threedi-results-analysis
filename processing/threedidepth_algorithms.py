# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
from collections import namedtuple
from datetime import datetime, timedelta
from typing import List, Dict, Callable, Tuple

import numpy as np
from osgeo import gdal
from qgis.core import QgsFeedback
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingContext
from qgis.core import QgsProcessingException
from qgis.core import QgsProcessingOutputLayerDefinition
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterColor
from qgis.core import QgsProcessingParameterDefinition
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingUtils
from qgis.core import QgsRasterBandStats
from qgis.core import QgsMeshLayer
from qgis.core import QgsRasterLayer
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QColor
from threedidepth.calculate import calculate_waterdepth, calculate_water_quality
from threedidepth.calculate import MODE_CONSTANT
from threedidepth.calculate import MODE_CONSTANT_VAR
from threedidepth.calculate import MODE_LINEAR
from threedidepth.calculate import MODE_LIZARD
from threedidepth.calculate import MODE_LIZARD_VAR

from threedigrid.admin.gridresultadmin import GridH5WaterQualityResultAdmin
from threedigrid.admin.gridresultadmin import GridH5ResultAdmin
from threedigrid.admin.gridresultadmin import GridH5AggregateResultAdmin
from threedigrid.admin.gridresultadmin import CustomizedResultAdmin
from threedigrid.admin.gridresultadmin import CustomizedWaterQualityResultAdmin

import logging
from pathlib import Path

from threedi_results_analysis.processing.widgets.widgets import ProcessingParameterNetcdfNumber
from threedi_results_analysis.processing.deps.concentration.mask import mask
from threedi_results_analysis.processing.deps.concentration.styling import (
    apply_transparency_gradient,
    apply_gradient_ramp,
)
from threedi_results_analysis.utils.color import color_ramp_from_data, COLOR_RAMP_OCEAN_HALINE

logger = logging.getLogger(__name__)
plugin_path = Path(__file__).resolve().parent.parent
Mode = namedtuple("Mode", ["name", "description"])


CALCULATION_STEP_END_INPUT = "CALCULATION_STEP_END_INPUT"
CALCULATION_STEP_INPUT = "CALCULATION_STEP_INPUT"
CALCULATION_STEP_START_INPUT = "CALCULATION_STEP_START_INPUT"
COLOR_INPUT = "COLOR_INPUT"
DEM_INPUT = "DEM_INPUT"
GRIDADMIN_INPUT = "GRIDADMIN_INPUT"
MODE_INPUT = "MODE_INPUT"
NETCDF_INPUT = "NETCDF_INPUT"
OUTPUT_DIRECTORY = "OUTPUT_DIRECTORY"
OUTPUT_FILENAME = "OUTPUT_FILENAME"
SUBSTANCE_INPUT = "SUBSTANCE_INPUT"
WATER_DEPTH_INPUT = "WATERDEPTH_INPUT"
WATER_DEPTH_LEVEL_NAME = "WATER_DEPTH_LEVEL_NAME"
WATER_DEPTH_OUTPUT = "WATER_DEPTH_OUTPUT"

WATER_QUALITY = "WATER_QUALITY"
WATER_QUANTITY = "WATER_QUANTITY"

STYLE_DIR = Path(__file__).parent / "styles"


def multiband_raster_min_max(layer) -> Tuple[float, float]:
    """Return the min and max values across all bands"""
    provider = layer.dataProvider()
    band_count = provider.bandCount()

    global_min = float("inf")
    global_max = float("-inf")

    for band in range(1, band_count + 1):
        stats = provider.bandStatistics(
            band,
            QgsRasterBandStats.Min | QgsRasterBandStats.Max
        )
        global_min = min(global_min, stats.minimumValue)
        global_max = max(global_max, stats.maximumValue)

    return global_min, global_max


class CancelError(Exception):
    """Error which gets raised when a user presses the 'cancel' button"""


class Progress:
    def __init__(self, feedback: QgsFeedback):
        self.feedback = feedback

    def __call__(self, progress: float):
        self.feedback.setProgress(progress * 100)
        if self.feedback.isCanceled():
            raise CancelError()


class BaseThreediDepthAlgorithm(QgsProcessingAlgorithm):
    """
    Base processing algorithm wrapping threedidepth functionalities
    """

    @property
    # Not implemented as proper abstractmethod because QgsProcessingAlgorithm already has a metaclass
    # and setting ABCMeta as metaclass creates complicated problems
    def output_modes(self) -> List[Mode]:
        """
        List of modes available for this processing algorithm
        """
        return NotImplementedError("Subclasses must implement this method")

    @property
    def default_mode(self) -> Mode:
        """
        Mode to be set as the default in the user interface
        """
        return NotImplementedError("Subclasses must implement this method")

    @property
    def data_type(self) -> str:
        """
        WATER_QUANITTY or WATER_QUALITY
        """
        return NotImplementedError("Subclasses must implement this method")

    @property
    def parameters(self) -> List:
        return [
            QgsProcessingParameterFile(
                name=GRIDADMIN_INPUT,
                description="Gridadmin file",
                extension="h5"
            ),
            QgsProcessingParameterFile(
                name=NETCDF_INPUT,
                description="3Di simulation output (.nc)",
                extension="nc"
            ),
            QgsProcessingParameterEnum(
                name=MODE_INPUT,
                description="Output type",
                options=[m.description for m in self.output_modes],
                defaultValue=self.default_mode,
            ),
            QgsProcessingParameterRasterDestination(
                name=OUTPUT_FILENAME,
                description="Output raster"
            ),
            # # Prevent QGIS from auto-adding it to the project
            # output_param.setFlags(output_param.flags() | QgsProcessingParameterDefinition.FlagHidden)
            # result.append(output_param)
        ]

    def output_file(self, parameters, context) -> Path:
        return Path(self.parameterAsFileOutput(parameters, OUTPUT_FILENAME, context))

    @property
    def threedidepth_method(self):
        if self.data_type == WATER_QUANTITY:
            return calculate_waterdepth
        elif self.data_type == WATER_QUALITY:
            return calculate_water_quality

    @property
    def netcdf_path(self) -> Path:
        return Path(
            self.threedidepth_args.get("results_3di_path") or
            self.threedidepth_args.get("water_quality_results_3di_path")
        )

    def get_threedidepth_args(self, parameters, context, feedback) -> Dict:
        return {
                "gridadmin_path": parameters[GRIDADMIN_INPUT],
                "mode": self.output_mode.name,
                "progress_func": Progress(feedback),
            }

    @property
    def results_reader(self):
        """Get the correct GridH5...Admin"""
        reader_classes = {
            "water_quality_results_3di.nc": GridH5WaterQualityResultAdmin,
            "results_3di.nc": GridH5ResultAdmin,
            "aggregate_results_3di.nc": GridH5AggregateResultAdmin,
            "customized_results_3di.nc": CustomizedResultAdmin,
            "customized_water_quality_results_3di.nc": CustomizedWaterQualityResultAdmin,
        }
        reader_class = reader_classes[Path(self.netcdf_path).name]
        reader = reader_class(str(self.threedidepth_args["gridadmin_path"]), str(self.netcdf_path))
        return reader

    def get_formatted_datetime_timestamps(self, formatting: str = '%Y-%m-%d %H:%M:%S') -> List[str]:
        indices = self.threedidepth_args["calculation_steps"]
        dt_timestamps = np.array(self.results_reader.nodes.dt_timestamps)[indices]
        result = []
        for dt_timestamp in dt_timestamps:
            dt = datetime.fromisoformat(dt_timestamp)
            formatted = dt.strftime(formatting)
            result.append(formatted)
        return result

    def set_timestamps_as_band_descriptions(
            self,
            raster: str | Path,
            formatting: str = '%Y-%m-%d %H:%M:%S'
    ):
        ds = gdal.Open(str(raster), gdal.GA_Update)
        if (
                self.threedidepth_args.get("calculate_maximum_waterlevel")
                or self.threedidepth_args.get("calculate_maximum_concentration")
        ):
            ds.GetRasterBand(1).SetDescription("Maximum")
        else:
            indices = self.threedidepth_args["calculation_steps"]
            reader = self.results_reader
            if isinstance(reader, (GridH5WaterQualityResultAdmin, CustomizedWaterQualityResultAdmin)):
                # all substances have the same timestamps and there is always a substance1
                dt_timestamps = np.array(reader.substance1.dt_timestamps)[indices]
            else:
                dt_timestamps = np.array(reader.nodes.dt_timestamps)[indices]
            for i in range(ds.RasterCount):
                dt = datetime.fromisoformat(str(dt_timestamps[i]))
                formatted = dt.strftime(formatting)
                ds.GetRasterBand(i + 1).SetDescription(formatted)

    @property
    def timestamps_seconds(self) -> List[int]:
        """
        Get the timestamps in seconds since start of simulation for the requested output time steps
        """
        indices = self.threedidepth_args["calculation_steps"]
        reader = self.results_reader
        if isinstance(reader, (GridH5WaterQualityResultAdmin, CustomizedWaterQualityResultAdmin)):
            # all substances have the same timestamps and there is always a substance1
            return reader.substance1.timestamps[indices]
        else:
            return reader.nodes.timestamps[indices]

    def output_layer_name_from_parameters(self, parameters, context):
        mode_index = self.parameterAsEnum(parameters, MODE_INPUT, context)
        return self.output_modes[mode_index].description

    def apply_style(self, layer):
        if self.data_type == WATER_QUALITY:
            min_value, max_value = multiband_raster_min_max(layer)
            apply_transparency_gradient(
                layer=layer,
                color=self.color,
                min_value=min_value,
                max_value=max_value,
            )

        elif self.data_type == WATER_QUANTITY:
            if self.output_mode.name in [
                MODE_CONSTANT_VAR, MODE_LIZARD_VAR
            ]:
                # Water level styling
                min_value, max_value = multiband_raster_min_max(layer)
                color_ramp = color_ramp_from_data(COLOR_RAMP_OCEAN_HALINE)
                apply_gradient_ramp(
                    layer=layer,
                    color_ramp=color_ramp,
                    min_value=min_value,
                    max_value=max_value,
                    band=1
                )
            elif self.output_mode.name in [
                MODE_CONSTANT, MODE_LIZARD
            ]:
                # Water depth styling
                layer.loadNamedStyle(str(STYLE_DIR / "water_depth.qml"))

    @property
    def layer_name_suffix(self):
        return ""

    def group(self):
        """Returns the name of the group this algorithm belongs to"""
        return "Post-process results"

    def groupId(self):
        """Returns the unique ID of the group this algorithm belongs to"""
        return "postprocessing"

    def initAlgorithm(self, config=None):
        """Add parameters that apply to all subclasses"""
        self.output_layer_name = "Output raster"
        for param in self.parameters:
            self.addParameter(param)

    def processAlgorithm(self, parameters, context, feedback):
        """
        Create the water depth raster with the provided user inputs
        """
        mode_index = self.parameterAsEnum(parameters, MODE_INPUT, context)
        self.output_mode = self.output_modes[mode_index]
        self.threedidepth_args = self.get_threedidepth_args(parameters=parameters, context=context, feedback=feedback)
        output_file = self.output_file(parameters, context)
        if output_file.is_file():
            output_file.unlink()
        try:
            feedback.pushInfo(f"threedidepth_args: {self.threedidepth_args}")
            self.threedidepth_method(**self.threedidepth_args)
        except CancelError:
            # When the process is cancelled, we just show the intermediate product
            pass
        except KeyError as e:
            if Path(self.netcdf_path).name == "aggregate_results_3di.nc" and e.args[0] == "s1_max":
                raise QgsProcessingException(
                    "Input aggregation NetCDF does not contain maximum water level aggregation (s1_max)."
                )
        try:
            self.set_timestamps_as_band_descriptions(
                raster=str(output_file)
            )
        except ValueError:
            # occurs when water quality results have missing time units, known issue (2025-10-02)
            pass

        # Save data to be used in postProcessAlgorithm
        self.output_layer_name = self.output_layer_name_from_parameters(parameters, context)
        self._results = {OUTPUT_FILENAME: str(output_file)}
        return self._results

    def postProcessAlgorithm(self, context, feedback):
        output_file = self._results[OUTPUT_FILENAME]
        output_layers = []
        timestamps_seconds = self.timestamps_seconds
        threedidepth_calculation_steps = self.threedidepth_args.get("calculation_steps") or [None]
        for i, time_step in enumerate(threedidepth_calculation_steps):
            if isinstance(time_step, int):
                layer_name_suffix = str(timedelta(seconds=int(timestamps_seconds[i])))
            else:
                layer_name_suffix = self.layer_name_suffix
            layer_name = f"{self.output_layer_name}: {layer_name_suffix}"
            output_layers.append(QgsRasterLayer(output_file, layer_name, "gdal"))
            self.apply_style(output_layers[i])
            if hasattr(output_layers[i].renderer(), "setBand"):
                output_layers[i].renderer().setBand(i+1)
            output_layers[i].setName(layer_name)
            context.project().addMapLayer(output_layers[i])
        return {}


class WaterDepthOrLevelSingleTimeStepAlgorithm(BaseThreediDepthAlgorithm):
    """
    Calculates water depth or water level from 3Di result NetCDF for a single time step
    """
    @property
    def output_modes(self) -> List[Mode]:
        return [
            Mode(MODE_LIZARD, "Interpolated water depth"),
            Mode(MODE_LIZARD_VAR, "Interpolated water level"),
            Mode(MODE_CONSTANT, "Non-interpolated water depth"),
            Mode(MODE_CONSTANT_VAR, "Non-interpolated water level"),
        ]

    @property
    def default_mode(self) -> Mode:
        return Mode(MODE_LIZARD, "Interpolated water depth")

    @property
    def data_type(self) -> str:
        """
        WATER_QUANITTY or WATER_QUALITY
        """
        return WATER_QUANTITY

    @property
    def parameters(self) -> List:
        result = super().parameters
        result.insert(
            -1,
            ProcessingParameterNetcdfNumber(
                name=CALCULATION_STEP_INPUT,
                description="Time step",
                defaultValue=-1,
                parentParameterName=NETCDF_INPUT,
            )
        )
        result.insert(2, QgsProcessingParameterRasterLayer(DEM_INPUT, "DEM"))
        return result

    def get_threedidepth_args(self, parameters, context, feedback) -> Dict:
        args = super().get_threedidepth_args(parameters=parameters, context=context, feedback=feedback)
        args.update(
            {
                "results_3di_path": parameters[NETCDF_INPUT],
                "dem_path": self.parameterAsRasterLayer(parameters, DEM_INPUT, context).source(),
                "waterdepth_path": str(self.output_file(parameters, context)),
                "calculation_steps": [parameters[CALCULATION_STEP_INPUT]],
            }
        )
        return args

    def createInstance(self):
        return WaterDepthOrLevelSingleTimeStepAlgorithm()

    def name(self):
        """Returns the algorithm name, used for identifying the algorithm"""
        return "waterdepthorlevelsingletimestep"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return "Water depth/level raster (single time step)"

    def shortHelpString(self):
        """Returns a localised short helper string for the algorithm"""
        return """
            <h3>Calculate water depth or level raster for specified timestep(s)</h3>
            <p>The 3Di simulation result contains a single water level for each cell, for each time step. However, the water depth is different for each pixel within the cell. To calculate water depths from water levels, the DEM needs to be subtracted from the water level. This results in a raster with a water depth value for each pixel.</p>
            <p>For some applications, it is useful to have water levels as a raster file. For example, to use them as <i>Initial water levels</i> in the next simulation.</p>
            <p>It is often preferable to spatially interpolate the water levels. This is recommended to use if the water level gradients are large, such as is often the case in sloping areas.</p>
            <h3>Parameters</h3>
            <h4>Gridadmin file</h4>
            <p>HDF5 file (*.h5) containing the computational grid of a 3Di model</p>
            <h4>3Di simulation output (.nc)</h4>
            <p>NetCDF (*.nc) containing the results or aggregated results of a 3Di simulation. When using aggregated results (aggregate_results_3di.nc), make sure to use "maximum water level" as one of the aggregation variables in the simulation.</p>
            <h4>DEM</h4>
            <p>Digital elevation model (.tif) that was used as input for the 3Di model used for this simulation. Using a different DEM in this tool than in the simulation may give unexpected results.</p>
            <h4>Output type</h4>
            <p>Choose between water depth (m above the surface) and water level (m MSL), with or without spatial interpolation.</p>
            <h4>Time step</h4>
            <p>The time step in the simulation for which you want to generate a raster. If you want outputs for multiple time steps, this is the first time step.</p>
            <h4>Enable multiple time steps export</h4>
            <p>Check this box if you want outputs for multiple time steps.</p>
            <h4>Last time step</h4>
            <p>If you want outputs for multiple time steps, specify the last time step here.</p>
            <h4>Output file name</h4>
            <p>File name for the output file. If multiple output rasters are generated, a time stamp will be added to each file name.</p>
            <h4>Output directory</h4>
            <p>Directory where the output file(s) are to be stored.</p>
            <h3>Save to NetCDF (experimental)</h3>
            <h4>Write the output of the processing algorithm to a NetCDF instead of to (multiple) GeoTIFF files. This is mainly useful when output for multiple time steps is enabled.</h4>
            """


class WaterDepthOrLevelMaximumAlgorithm(BaseThreediDepthAlgorithm):
    """
    Calculates maximum water depth or water level from 3Di result NetCDF
    """
    @property
    def output_modes(self) -> List[Mode]:
        return [
            Mode(MODE_LIZARD, "Interpolated water depth"),
            Mode(MODE_LIZARD_VAR, "Interpolated water level"),
            Mode(MODE_CONSTANT, "Non-interpolated water depth"),
            Mode(MODE_CONSTANT_VAR, "Non-interpolated water level"),
        ]

    @property
    def default_mode(self) -> Mode:
        return Mode(MODE_LIZARD, "Interpolated water depth")

    @property
    def data_type(self) -> str:
        """
        WATER_QUANITTY or WATER_QUALITY
        """
        return WATER_QUANTITY

    @property
    def parameters(self) -> List:
        result = super().parameters
        result.insert(2, QgsProcessingParameterRasterLayer(DEM_INPUT, "DEM"))
        return result

    def get_threedidepth_args(self, parameters, context, feedback) -> Dict:
        args = super().get_threedidepth_args(parameters=parameters, context=context, feedback=feedback)
        args.update(
            {
                "results_3di_path": parameters[NETCDF_INPUT],
                "dem_path": self.parameterAsRasterLayer(parameters, DEM_INPUT, context).source(),
                "waterdepth_path": str(self.output_file(parameters, context)),
                "calculate_maximum_waterlevel": True,
                "calculation_steps": None,
            }
        )
        return args

    @property
    def layer_name_suffix(self):
        return "Maximum"

    def createInstance(self):
        return WaterDepthOrLevelMaximumAlgorithm()

    def name(self):
        """Returns the algorithm name, used for identifying the algorithm"""
        return "waterdepthorlevelmaximum"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-   visible display of the algorithm name.
        """
        return "Water depth/level raster (maximum)"

    def shortHelpString(self):
        """Returns a localised short helper string for the algorithm"""
        return """
            <h3>Calculate water depth or level raster for specified timestep(s)</h3>
            <p>The 3Di simulation result contains a single water level for each cell, for each time step. However, the water depth is different for each pixel within the cell. To calculate water depths from water levels, the DEM needs to be subtracted from the water level. This results in a raster with a water depth value for each pixel.</p>
            <p>For some applications, it is useful to have water levels as a raster file. For example, to use them as <i>Initial water levels</i> in the next simulation.</p>
            <p>It is often preferable to spatially interpolate the water levels. This is recommended to use if the water level gradients are large, such as is often the case in sloping areas.</p>
            <h3>Parameters</h3>
            <h4>Gridadmin file</h4>
            <p>HDF5 file (*.h5) containing the computational grid of a 3Di model</p>
            <h4>3Di simulation output (.nc)</h4>
            <p>NetCDF (*.nc) containing the results or aggregated results of a 3Di simulation. When using aggregated results (aggregate_results_3di.nc), make sure to use "maximum water level" as one of the aggregation variables in the simulation.</p>
            <h4>DEM</h4>
            <p>Digital elevation model (.tif) that was used as input for the 3Di model used for this simulation. Using a different DEM in this tool than in the simulation may give unexpected results.</p>
            <h4>Output type</h4>
            <p>Choose between water depth (m above the surface) and water level (m MSL), with or without spatial interpolation.</p>
            <h4>Time step</h4>
            <p>The time step in the simulation for which you want to generate a raster. If you want outputs for multiple time steps, this is the first time step.</p>
            <h4>Enable multiple time steps export</h4>
            <p>Check this box if you want outputs for multiple time steps.</p>
            <h4>Last time step</h4>
            <p>If you want outputs for multiple time steps, specify the last time step here.</p>
            <h4>Output file name</h4>
            <p>File name for the output file. If multiple output rasters are generated, a time stamp will be added to each file name.</p>
            <h4>Output directory</h4>
            <p>Directory where the output file(s) are to be stored.</p>
            <h3>Save to NetCDF (experimental)</h3>
            <h4>Write the output of the processing algorithm to a NetCDF instead of to (multiple) GeoTIFF files. This is mainly useful when output for multiple time steps is enabled.</h4>
            """


class WaterDepthOrLevelMultipleTimeStepAlgorithm(BaseThreediDepthAlgorithm):
    """
    Calculates water depth or water level from 3Di result NetCDF for multiple time steps
    """
    # TODO: zo aanpassen dat rekening wordt gehouden met dat er één file uitkomt en dat dat ook een netcdf kan zijn
    # TODO: styling
    @property
    def output_modes(self) -> List[Mode]:
        return [
            Mode(MODE_LIZARD, "Interpolated water depth"),
            Mode(MODE_LIZARD_VAR, "Interpolated water level"),
            Mode(MODE_CONSTANT, "Non-interpolated water depth"),
            Mode(MODE_CONSTANT_VAR, "Non-interpolated water level"),
        ]

    @property
    def default_mode(self) -> Mode:
        return Mode(MODE_LIZARD, "Interpolated water depth")

    @property
    def data_type(self) -> str:
        """
        WATER_QUANITTY or WATER_QUALITY
        """
        return WATER_QUANTITY

    @property
    def parameters(self) -> List:
        result = super().parameters
        result.insert(
            -1,
            ProcessingParameterNetcdfNumber(
                name=CALCULATION_STEP_START_INPUT,
                description="First time step",
                defaultValue=0,
                parentParameterName=NETCDF_INPUT,
            )
        )
        result.insert(
            -1,
            ProcessingParameterNetcdfNumber(
                name=CALCULATION_STEP_END_INPUT,
                description="Last time step",
                defaultValue=-1,
                parentParameterName=NETCDF_INPUT,
            )
        )
        result.insert(2, QgsProcessingParameterRasterLayer(DEM_INPUT, "DEM"))
        return result

    def get_threedidepth_args(self, parameters, context, feedback) -> Dict:
        args = super().get_threedidepth_args(parameters=parameters, context=context, feedback=feedback)
        calculation_step_start = parameters[CALCULATION_STEP_START_INPUT]
        calculation_step_end = parameters[CALCULATION_STEP_END_INPUT]
        if calculation_step_end <= calculation_step_start:
            feedback.reportError(
                "The last timestep should be larger than the first timestep.",
                fatalError=True,
            )
            return {}
        calculation_steps = list(range(calculation_step_start, calculation_step_end))
        args.update(
            {
                "calculation_steps": calculation_steps,
                "results_3di_path": parameters[NETCDF_INPUT],
                "dem_path": self.parameterAsRasterLayer(parameters, DEM_INPUT, context).source(),
                "waterdepth_path": str(self.output_file(parameters, context)),
            }
        )
        return args

    def apply_style(self, layer):
        # TODO apply different style for water level
        layer.loadNamedStyle(str(STYLE_DIR / "water_depth.qml"))

    def createInstance(self):
        return WaterDepthOrLevelMultipleTimeStepAlgorithm()

    def name(self):
        """Returns the algorithm name, used for identifying the algorithm"""
        return "waterdepthorlevelmultipletimestep"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return "Water depth/level raster (multiple time steps)"

    def shortHelpString(self):
        """Returns a localised short helper string for the algorithm"""
        return """
            <h3>Calculate water depth or level raster for specified timestep(s)</h3>
            <p>The 3Di simulation result contains a single water level for each cell, for each time step. However, the water depth is different for each pixel within the cell. To calculate water depths from water levels, the DEM needs to be subtracted from the water level. This results in a raster with a water depth value for each pixel.</p>
            <p>For some applications, it is useful to have water levels as a raster file. For example, to use them as <i>Initial water levels</i> in the next simulation.</p>
            <p>It is often preferable to spatially interpolate the water levels. This is recommended to use if the water level gradients are large, such as is often the case in sloping areas.</p>
            <h3>Parameters</h3>
            <h4>Gridadmin file</h4>
            <p>HDF5 file (*.h5) containing the computational grid of a 3Di model</p>
            <h4>3Di simulation output (.nc)</h4>
            <p>NetCDF (*.nc) containing the results or aggregated results of a 3Di simulation. When using aggregated results (aggregate_results_3di.nc), make sure to use "maximum water level" as one of the aggregation variables in the simulation.</p>
            <h4>DEM</h4>
            <p>Digital elevation model (.tif) that was used as input for the 3Di model used for this simulation. Using a different DEM in this tool than in the simulation may give unexpected results.</p>
            <h4>Output type</h4>
            <p>Choose between water depth (m above the surface) and water level (m MSL), with or without spatial interpolation.</p>
            <h4>Time step</h4>
            <p>The time step in the simulation for which you want to generate a raster. If you want outputs for multiple time steps, this is the first time step.</p>
            <h4>Enable multiple time steps export</h4>
            <p>Check this box if you want outputs for multiple time steps.</p>
            <h4>Last time step</h4>
            <p>If you want outputs for multiple time steps, specify the last time step here.</p>
            <h4>Output file name</h4>
            <p>File name for the output file. If multiple output rasters are generated, a time stamp will be added to each file name.</p>
            <h4>Output directory</h4>
            <p>Directory where the output file(s) are to be stored.</p>
            <h3>Save to NetCDF (experimental)</h3>
            <h4>Write the output of the processing algorithm to a NetCDF instead of to (multiple) GeoTIFF files. This is mainly useful when output for multiple time steps is enabled.</h4>
            """


class ConcentrationSingleTimeStepAlgorithm(BaseThreediDepthAlgorithm):
    """
    Calculates concentration from 3Di result NetCDF for a single time step
    """
    @property
    def output_modes(self) -> List[Mode]:
        return [
            Mode(MODE_LIZARD_VAR, "Interpolated concentrations"),
            Mode(MODE_CONSTANT_VAR, "Non-interpolated concentrations"),
        ]

    @property
    def default_mode(self) -> Mode:
        return Mode(MODE_LIZARD_VAR, "Interpolated concentrations"),

    @property
    def data_type(self) -> str:
        """
        WATER_QUANITTY or WATER_QUALITY
        """
        return WATER_QUALITY

    @property
    def parameters(self) -> List:
        result = super().parameters
        result.insert(
            -1,
            ProcessingParameterNetcdfNumber(
                name=CALCULATION_STEP_INPUT,
                description="Time step",
                defaultValue=-1,
                parentParameterName=NETCDF_INPUT,
            )
        )
        result.insert(
            2,
            QgsProcessingParameterRasterLayer(
                WATER_DEPTH_INPUT,
                "Water depth (mask layer)",
                optional=True
            )
        )
        result.insert(
            3,
            QgsProcessingParameterString(
                SUBSTANCE_INPUT,
                "Substance",
            )
        )
        result.insert(
            4,
            QgsProcessingParameterColor(
                COLOR_INPUT,
                "Color",
                defaultValue=QColor("brown")
            )
        )
        return result

    def get_threedidepth_args(self, parameters, context, feedback) -> Dict:
        args = super().get_threedidepth_args(parameters=parameters, context=context, feedback=feedback)
        gwq = GridH5WaterQualityResultAdmin(parameters[GRIDADMIN_INPUT], parameters[NETCDF_INPUT])
        substances = {getattr(gwq, substance_key).name: substance_key for substance_key in gwq.substances}
        variable = substances[self.parameterAsString(parameters, SUBSTANCE_INPUT, context)]  # TODO handle KeyError
        mask_layer = self.parameterAsRasterLayer(parameters, WATER_DEPTH_INPUT, context)
        if mask_layer:
            extent = mask_layer.extent()  # QgsRectangle
            output_extent = (extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum())
        else:
            output_extent = gwq.get_model_extent()

        args.update(
            {
                "water_quality_results_3di_path": parameters[NETCDF_INPUT],
                "variable": variable,
                "output_extent": output_extent,  # TODO make this separate input?
                "output_path": str(self.output_file(parameters, context)),
                "calculation_steps": [parameters[CALCULATION_STEP_INPUT]],
            }
        )
        return args

    def output_layer_name_from_parameters(self, parameters, context) -> str:
        mode_description = super().output_layer_name_from_parameters(parameters, context)
        substance_name = self.parameterAsString(parameters, SUBSTANCE_INPUT, context)
        return f"{substance_name}: {mode_description}"

    def processAlgorithm(self, parameters, context, feedback):
        """
        Create the water depth raster with the provided user inputs
        """
        mask_layer = self.parameterAsRasterLayer(parameters, WATER_DEPTH_INPUT, context)
        result_file_name = self.output_file(parameters, context)
        if mask_layer:
            parameters[OUTPUT_FILENAME] = QgsProcessingUtils.generateTempFilename("non_masked.tif")
        non_masked_file_name = super().processAlgorithm(parameters, context, feedback)[OUTPUT_FILENAME]
        if mask_layer:
            mask(source=non_masked_file_name, mask=mask_layer.source(), output=result_file_name)
        self.color = self.parameterAsColor(parameters, COLOR_INPUT, context)
        self._results = {OUTPUT_FILENAME: str(result_file_name)}
        return {OUTPUT_FILENAME: result_file_name}

    def createInstance(self):
        return ConcentrationSingleTimeStepAlgorithm()

    def name(self):
        """Returns the algorithm name, used for identifying the algorithm"""
        return "concentrationsingletimestep"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return "Concentration raster (single time step)"

    def shortHelpString(self):
        """Returns a localised short helper string for the algorithm"""
        return """
            <h3>Calculate water depth or level raster for specified timestep(s)</h3>
            <p>The 3Di simulation result contains a single water level for each cell, for each time step. However, the water depth is different for each pixel within the cell. To calculate water depths from water levels, the DEM needs to be subtracted from the water level. This results in a raster with a water depth value for each pixel.</p>
            <p>For some applications, it is useful to have water levels as a raster file. For example, to use them as <i>Initial water levels</i> in the next simulation.</p>
            <p>It is often preferable to spatially interpolate the water levels. This is recommended to use if the water level gradients are large, such as is often the case in sloping areas.</p>
            <h3>Parameters</h3>
            <h4>Gridadmin file</h4>
            <p>HDF5 file (*.h5) containing the computational grid of a 3Di model</p>
            <h4>3Di simulation output (.nc)</h4>
            <p>NetCDF (*.nc) containing the results or aggregated results of a 3Di simulation. When using aggregated results (aggregate_results_3di.nc), make sure to use "maximum water level" as one of the aggregation variables in the simulation.</p>
            <h4>DEM</h4>
            <p>Digital elevation model (.tif) that was used as input for the 3Di model used for this simulation. Using a different DEM in this tool than in the simulation may give unexpected results.</p>
            <h4>Output type</h4>
            <p>Choose between water depth (m above the surface) and water level (m MSL), with or without spatial interpolation.</p>
            <h4>Time step</h4>
            <p>The time step in the simulation for which you want to generate a raster. If you want outputs for multiple time steps, this is the first time step.</p>
            <h4>Enable multiple time steps export</h4>
            <p>Check this box if you want outputs for multiple time steps.</p>
            <h4>Last time step</h4>
            <p>If you want outputs for multiple time steps, specify the last time step here.</p>
            <h4>Output file name</h4>
            <p>File name for the output file. If multiple output rasters are generated, a time stamp will be added to each file name.</p>
            <h4>Output directory</h4>
            <p>Directory where the output file(s) are to be stored.</p>
            <h3>Save to NetCDF (experimental)</h3>
            <h4>Write the output of the processing algorithm to a NetCDF instead of to (multiple) GeoTIFF files. This is mainly useful when output for multiple time steps is enabled.</h4>
            """


# class ORIGINAL_ALGORITHM(QgsProcessingAlgorithm):
#     """
#     Calculates water depth or water level rasters from 3Di result NetCDF
#     """
#
#     # Constants used to refer to parameters and outputs. They will be
#     # used when calling the algorithm from another algorithm, or when
#     # calling from the QGIS console.
#
#     MODES = [
#         Mode(MODE_LIZARD, "Interpolated water depth"),
#         Mode(MODE_LIZARD_S1, "Interpolated water level"),
#         Mode(MODE_CONSTANT, "Non-interpolated water depth"),
#         Mode(MODE_CONSTANT_S1, "Non-interpolated water level"),
#     ]
#
#     GRIDADMIN_INPUT = "GRIDADMIN_INPUT"
#     RESULTS_3DI_INPUT = "RESULTS_3DI_INPUT"
#     DEM_INPUT = "DEM_INPUT"
#     MODE_INPUT = "MODE_INPUT"
#     CALCULATION_STEP_INPUT = "CALCULATION_STEP_INPUT"
#     AS_NETCDF_INPUT = "AS_NETCDF_INPUT"
#     CALCULATION_STEP_END_INPUT = "CALCULATION_STEP_END_INPUT"
#     WATER_DEPTH_LEVEL_NAME = "WATER_DEPTH_LEVEL_NAME"
#     OUTPUT_DIRECTORY = "OUTPUT_DIRECTORY"
#     WATER_DEPTH_OUTPUT = "WATER_DEPTH_OUTPUT"
#
#     def tr(self, string):
#         """
#         Returns a translatable string with the self.tr() function.
#         """
#         return QCoreApplication.translate("Processing", string)
#
#     def createInstance(self):
#         return WaterDepthOrLevelAlgorithm()
#
#     def name(self):
#         """Returns the algorithm name, used for identifying the algorithm"""
#         return "threedidepth"
#
#     def displayName(self):
#         """
#         Returns the translated algorithm name, which should be used for any
#         user-visible display of the algorithm name.
#         """
#         return self.tr("Water depth/level raster")
#
#     def group(self):
#         """Returns the name of the group this algorithm belongs to"""
#         return self.tr("Post-process results")
#
#     def groupId(self):
#         """Returns the unique ID of the group this algorithm belongs to"""
#         return "postprocessing"
#
#     def shortHelpString(self):
#         """Returns a localised short helper string for the algorithm"""
#         return self.tr(
#             """
#             <h3>Calculate water depth or level raster for specified timestep(s)</h3>
#             <p>The 3Di simulation result contains a single water level for each cell, for each time step. However, the water depth is different for each pixel within the cell. To calculate water depths from water levels, the DEM needs to be subtracted from the water level. This results in a raster with a water depth value for each pixel.</p>
#             <p>For some applications, it is useful to have water levels as a raster file. For example, to use them as <i>Initial water levels</i> in the next simulation.</p>
#             <p>It is often preferable to spatially interpolate the water levels. This is recommended to use if the water level gradients are large, such as is often the case in sloping areas.</p>
#             <h3>Parameters</h3>
#             <h4>Gridadmin file</h4>
#             <p>HDF5 file (*.h5) containing the computational grid of a 3Di model</p>
#             <h4>3Di simulation output (.nc)</h4>
#             <p>NetCDF (*.nc) containing the results or aggregated results of a 3Di simulation. When using aggregated results (aggregate_results_3di.nc), make sure to use "maximum water level" as one of the aggregation variables in the simulation.</p>
#             <h4>DEM</h4>
#             <p>Digital elevation model (.tif) that was used as input for the 3Di model used for this simulation. Using a different DEM in this tool than in the simulation may give unexpected results.</p>
#             <h4>Output type</h4>
#             <p>Choose between water depth (m above the surface) and water level (m MSL), with or without spatial interpolation.</p>
#             <h4>Time step</h4>
#             <p>The time step in the simulation for which you want to generate a raster. If you want outputs for multiple time steps, this is the first time step.</p>
#             <h4>Enable multiple time steps export</h4>
#             <p>Check this box if you want outputs for multiple time steps.</p>
#             <h4>Last time step</h4>
#             <p>If you want outputs for multiple time steps, specify the last time step here.</p>
#             <h4>Output file name</h4>
#             <p>File name for the output file. If multiple output rasters are generated, a time stamp will be added to each file name.</p>
#             <h4>Output directory</h4>
#             <p>Directory where the output file(s) are to be stored.</p>
#             <h3>Save to NetCDF (experimental)</h3>
#             <h4>Write the output of the processing algorithm to a NetCDF instead of to (multiple) GeoTIFF files. This is mainly useful when output for multiple time steps is enabled.</h4>
#             """
#         )
#
#     def initAlgorithm(self, config=None):
#         """Here we define the inputs and output of the algorithm"""
#         # Input parameters
#         self.addParameter(
#             QgsProcessingParameterFile(
#                 self.GRIDADMIN_INPUT,
#                 self.tr("Gridadmin file"), extension="h5")
#         )
#         self.addParameter(
#             QgsProcessingParameterFile(
#                 self.RESULTS_3DI_INPUT,
#                 self.tr("3Di simulation output (.nc)"),
#                 extension="nc"
#             )
#         )
#         self.addParameter(QgsProcessingParameterRasterLayer(self.DEM_INPUT, self.tr("DEM")))
#         self.addParameter(
#             QgsProcessingParameterEnum(
#                 name=self.MODE_INPUT,
#                 description=self.tr("Output type"),
#                 options=[m.description for m in self.MODES],
#                 defaultValue=MODE_LINEAR,
#             )
#         )
#         self.addParameter(
#             ProcessingParameterNetcdfNumber(
#                 name=self.CALCULATION_STEP_INPUT,
#                 description=self.tr("Time step"),
#                 defaultValue=-1,
#                 parentParameterName=self.RESULTS_3DI_INPUT,
#             )
#         )
#         self.addParameter(
#             ProcessingParameterNetcdfNumber(
#                 name=self.CALCULATION_STEP_END_INPUT,
#                 description=self.tr("Last time step"),
#                 defaultValue=-2,
#                 parentParameterName=self.RESULTS_3DI_INPUT,
#                 optional=True,
#             )
#         )
#         self.addParameter(
#             QgsProcessingParameterString(
#                 self.WATER_DEPTH_LEVEL_NAME,
#                 self.tr("Output file name"),
#                 defaultValue="water_depth_level",
#             )
#         )
#         output_param = QgsProcessingParameterFile(
#             self.OUTPUT_DIRECTORY,
#             self.tr("Output directory"),
#             behavior=QgsProcessingParameterFile.Folder,
#         )
#         self.addParameter(output_param)
#         self.addParameter(
#             QgsProcessingParameterBoolean(
#                 name=self.AS_NETCDF_INPUT,
#                 description="Save to NetCDF (experimental)",
#                 defaultValue=False,
#             )
#         )
#
#     def processAlgorithm(self, parameters, context, feedback):
#         """
#         Create the water depth raster with the provided user inputs
#         """
#         dem_filename = self.parameterAsRasterLayer(parameters, self.DEM_INPUT, context).source()
#         gridadmin_path = parameters[self.GRIDADMIN_INPUT]
#         results_3di_path = parameters[self.RESULTS_3DI_INPUT]
#         mode_index = self.parameterAsEnum(parameters, self.MODE_INPUT, context)
#         step = parameters[self.CALCULATION_STEP_INPUT]
#         endstep = parameters[self.CALCULATION_STEP_END_INPUT]
#         if endstep:
#             if endstep <= step:
#                 feedback.reportError(
#                     "The last timestep should be larger than the first timestep.",
#                     fatalError=True,
#                 )
#                 return {}
#             timesteps = list(range(step, endstep))
#         else:
#             timesteps = [step]
#
#         raster_filename = parameters[self.WATER_DEPTH_LEVEL_NAME]
#         if not raster_filename:
#             raise QgsProcessingException(self.invalidSourceError(parameters, self.WATER_DEPTH_LEVEL_NAME))
#
#         output_location = parameters[self.OUTPUT_DIRECTORY]
#         if not output_location:
#             raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT_DIRECTORY))
#
#         as_netcdf = parameters[self.AS_NETCDF_INPUT]
#         raster_extension = "nc" if as_netcdf else "tif"
#         raster_filename_with_ext = f"{raster_filename}.{raster_extension}"
#         waterdepth_output_file = Path(output_location) / raster_filename_with_ext
#         if waterdepth_output_file.is_file():
#             waterdepth_output_file.unlink()
#
#         try:
#             calculate_waterdepth(
#                 gridadmin_path=gridadmin_path,
#                 results_3di_path=results_3di_path,
#                 dem_path=dem_filename,
#                 waterdepth_path=str(waterdepth_output_file),
#                 calculation_steps=timesteps,
#                 mode=self.MODES[mode_index].name,
#                 progress_func=Progress(feedback),
#                 netcdf=as_netcdf,
#             )
#         except CancelError:
#             # When the process is cancelled, we just show the intermediate product
#             pass
#         except KeyError as e:
#             if Path(results_3di_path).name == "aggregate_results_3di.nc" and e.args[0] == "s1_max":
#                 raise QgsProcessingException(
#                     "Input aggregation NetCDF does not contain maximum water level aggregation (s1_max)."
#                 )
#
#         if as_netcdf:
#             layer = QgsMeshLayer(str(waterdepth_output_file), raster_filename, "mdal")
#         else:
#             layer = QgsRasterLayer(str(waterdepth_output_file), raster_filename)
#         context.temporaryLayerStore().addMapLayer(layer)
#         layer_details = QgsProcessingContext.LayerDetails(raster_filename, context.project(), self.WATER_DEPTH_OUTPUT)
#         context.addLayerToLoadOnCompletion(layer.id(), layer_details)
#         return {}
#
#
# class ConcentrationRasterAlgorithm(QgsProcessingAlgorithm):
#     """
#     Calculates concentration raster from 3Di water quality result NetCDF
#     """
#
#     MODES = [
#         Mode(MODE_LIZARD, "Interpolated concentration"),
#         Mode(MODE_CONSTANT, "Non-interpolated concentration"),
#     ]
#
#     GRIDADMIN_INPUT = "GRIDADMIN_INPUT"
#     WQ_RESULTS_3DI_INPUT = "WQ_RESULTS_3DI_INPUT"
#     MODE_INPUT = "MODE_INPUT"
#     CALCULATION_STEP_INPUT = "CALCULATION_STEP_INPUT"
#     AS_NETCDF_INPUT = "AS_NETCDF_INPUT"
#     CALCULATION_STEP_END_INPUT = "CALCULATION_STEP_END_INPUT"
#     OUTPUT_FILE_NAME = "OUTPUT_FILE_NAME"
#     OUTPUT_DIRECTORY = "OUTPUT_DIRECTORY"
#     OUTPUT = "OUTPUT"
#
#     def tr(self, string):
#         """
#         Returns a translatable string with the self.tr() function.
#         """
#         return QCoreApplication.translate("Processing", string)
#
#     def createInstance(self):
#         return WaterDepthOrLevelAlgorithm()
#
#     def name(self):
#         """Returns the algorithm name, used for identifying the algorithm"""
#         return "concentration_raster"
#
#     def displayName(self):
#         """
#         Returns the translated algorithm name, which should be used for any
#         user-visible display of the algorithm name.
#         """
#         return self.tr("Concentration raster")
#
#     def group(self):
#         """Returns the name of the group this algorithm belongs to"""
#         return self.tr("Post-process results")
#
#     def groupId(self):
#         """Returns the unique ID of the group this algorithm belongs to"""
#         return "postprocessing"
#
#     def shortHelpString(self):
#         """Returns a localised short helper string for the algorithm"""
#         return self.tr("Calculate concentration raster for specified time step")
#
#     def initAlgorithm(self, config=None):
#         """Here we define the inputs and output of the algorithm"""
#         # Input parameters
#         self.addParameter(
#             QgsProcessingParameterFile(self.GRIDADMIN_INPUT, self.tr("Gridadmin.h5 file"), extension="h5")
#         )
#         self.addParameter(
#             QgsProcessingParameterFile(self.RESULTS_3DI_INPUT, self.tr("Water quality results file"), extension="nc")
#         )
#         self.addParameter(QgsProcessingParameterRasterLayer(self.DEM_INPUT, self.tr("DEM")))
#         self.addParameter(
#             QgsProcessingParameterEnum(
#                 name=self.MODE_INPUT,
#                 description=self.tr("Interpolation mode"),
#                 options=[m.description for m in self.MODES],
#                 defaultValue=MODE_LINEAR,
#             )
#         )
#         self.addParameter(
#             ProcessingParameterNetcdfNumber(
#                 name=self.CALCULATION_STEP_INPUT,
#                 description=self.tr("The timestep in the simulation for which you want to generate a raster"),
#                 defaultValue=-1,
#                 parentParameterName=self.RESULTS_3DI_INPUT,
#             )
#         )
#         self.addParameter(
#             ProcessingParameterNetcdfNumber(
#                 name=self.CALCULATION_STEP_END_INPUT,
#                 description=self.tr("Last timestep (for multiple timesteps export)"),
#                 defaultValue=-2,
#                 parentParameterName=self.RESULTS_3DI_INPUT,
#                 optional=True,
#             )
#         )
#         self.addParameter(
#             QgsProcessingParameterString(
#                 self.WATER_DEPTH_LEVEL_NAME,
#                 self.tr("Water depth/level raster name"),
#                 defaultValue="water_depth_level",
#             )
#         )
#         output_param = QgsProcessingParameterFile(
#             self.OUTPUT_DIRECTORY,
#             self.tr("Destination folder for water depth/level raster"),
#             behavior=QgsProcessingParameterFile.Folder,
#         )
#         self.addParameter(output_param)
#         self.addParameter(
#             QgsProcessingParameterBoolean(
#                 name=self.AS_NETCDF_INPUT,
#                 description="Export the water depth/level as a NetCDF file (experimental)",
#                 defaultValue=False,
#             )
#         )
#
#     def processAlgorithm(self, parameters, context, feedback):
#         """
#         Create the water depth raster with the provided user inputs
#         """
#         dem_filename = self.parameterAsRasterLayer(parameters, self.DEM_INPUT, context).source()
#         gridadmin_path = parameters[self.GRIDADMIN_INPUT]
#         results_3di_path = parameters[self.RESULTS_3DI_INPUT]
#         mode_index = self.parameterAsEnum(parameters, self.MODE_INPUT, context)
#         step = parameters[self.CALCULATION_STEP_INPUT]
#         endstep = parameters[self.CALCULATION_STEP_END_INPUT]
#         if endstep:
#             if endstep <= step:
#                 feedback.reportError(
#                     "The last timestep should be larger than the first timestep.",
#                     fatalError=True,
#                 )
#                 return {}
#             timesteps = list(range(step, endstep))
#         else:
#             timesteps = [step]
#
#         raster_filename = parameters[self.WATER_DEPTH_LEVEL_NAME]
#         if not raster_filename:
#             raise QgsProcessingException(self.invalidSourceError(parameters, self.WATER_DEPTH_LEVEL_NAME))
#
#         output_location = parameters[self.OUTPUT_DIRECTORY]
#         if not output_location:
#             raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT_DIRECTORY))
#
#         as_netcdf = parameters[self.AS_NETCDF_INPUT]
#         raster_extension = "nc" if as_netcdf else "tif"
#         raster_filename_with_ext = f"{raster_filename}.{raster_extension}"
#         waterdepth_output_file = Path(output_location) / raster_filename_with_ext
#         if waterdepth_output_file.is_file():
#             waterdepth_output_file.unlink()
#
#         try:
#             calculate_waterdepth(
#                 gridadmin_path=gridadmin_path,
#                 results_3di_path=results_3di_path,
#                 dem_path=dem_filename,
#                 waterdepth_path=str(waterdepth_output_file),
#                 calculation_steps=timesteps,
#                 mode=self.MODES[mode_index].name,
#                 progress_func=Progress(feedback),
#                 netcdf=as_netcdf,
#             )
#         except CancelError:
#             # When the process is cancelled, we just show the intermediate product
#             pass
#
#         if as_netcdf:
#             layer = QgsMeshLayer(str(waterdepth_output_file), raster_filename, "mdal")
#         else:
#             layer = QgsRasterLayer(str(waterdepth_output_file), raster_filename)
#         context.temporaryLayerStore().addMapLayer(layer)
#         layer_details = QgsProcessingContext.LayerDetails(raster_filename, context.project(), self.WATER_DEPTH_OUTPUT)
#         context.addLayerToLoadOnCompletion(layer.id(), layer_details)
#         return {}
#
#
# class MaxWaterDepthOrLevelAlgorithm(QgsProcessingAlgorithm):
#     """
#     Calculates maximum water depth or water level rasters from 3Di result NetCDF
#     """
#
#     # Constants used to refer to parameters and outputs. They will be
#     # used when calling the algorithm from another algorithm, or when
#     # calling from the QGIS console.
#
#     MODES = [
#         Mode(MODE_LIZARD, "Interpolated water depth"),
#         Mode(MODE_LIZARD_S1, "Interpolated water level"),
#         Mode(MODE_CONSTANT, "Non-interpolated water depth"),
#         Mode(MODE_CONSTANT_S1, "Non-interpolated water level"),
#     ]
#
#     GRIDADMIN_INPUT = "GRIDADMIN_INPUT"
#     RESULTS_3DI_INPUT = "RESULTS_3DI_INPUT"
#     DEM_INPUT = "DEM_INPUT"
#     MODE_INPUT = "MODE_INPUT"
#     OUTPUT_FILENAME = "OUTPUT_FILENAME"
#     WATER_DEPTH_OUTPUT = "WATER_DEPTH_OUTPUT"
#
#     def tr(self, string):
#         """
#         Returns a translatable string with the self.tr() function.
#         """
#         return QCoreApplication.translate("Processing", string)
#
#     def createInstance(self):
#         return MaxWaterDepthOrLevelAlgorithm()
#
#     def name(self):
#         """Returns the algorithm name, used for identifying the algorithm"""
#         return "threedidepth_max"
#
#     def displayName(self):
#         """
#         Returns the translated algorithm name, which should be used for any
#         user-visible display of the algorithm name.
#         """
#         return self.tr("Maximum water depth/level raster")
#
#     def group(self):
#         """Returns the name of the group this algorithm belongs to"""
#         return self.tr("Post-process results")
#
#     def groupId(self):
#         """Returns the unique ID of the group this algorithm belongs to"""
#         return "postprocessing"
#
#     def shortHelpString(self):
#         """Returns a localised short helper string for the algorithm"""
#         return self.tr(
#             """
#             <h3>Calculate maximum water depth/level raster over all time steps in the simulation.</h3>
#             <p>The 3Di simulation result contains a single water level for each cell, for each time step. However, the water depth is different for each pixel within the cell. To calculate water depths from water levels, the DEM needs to be subtracted from the water level. This results in a raster with a water depth value for each pixel.</p>
#             <p>For some applications, it is useful to have water levels as a raster file. For example, to use them as <i>Initial water levels</i> in the next simulation.</p>
#             <p>It is often preferable to spatially interpolate the water levels. This is recommended to use if the water level gradients are large, such as is often the case in sloping areas.</p>
#             <p>Note that the maximum water level may occur at different time steps in different cells. Therefore, the maximum water level situation that this tool calculates may never have occurred as such during the simulation.<\p>
#             <h3>Parameters</h3>
#             <h4>Gridadmin file</h4>
#             <p>HDF5 file (*.h5) containing the computational grid of a 3Di model</p>
#             <h4>3Di simulation output</h4>
#             <p>NetCDF (*.nc) containing the results or aggregated results of a 3Di simulation. When using aggregated results (aggregate_results_3di.nc), make sure to use "maximum water level" as one of the aggregation variables in the simulation.</p>
#             <h4>DEM</h4>
#             <p>Digital elevation model (.tif) that was used as input for the 3Di model used for this simulation. Using a different DEM in this tool than in the simulation may give unexpected results.</p>
#             <h4>Output type</h4>
#             <p>Choose between water depth (m above the surface) and water level (m MSL), with or without spatial interpolation.</p>
#             <h4>Output file</h4>
#             <p>Destination file path for the water depth/level raster</p>
#             """
#         )
#
#     def initAlgorithm(self, config=None):
#         """Here we define the inputs and output of the algorithm"""
#         # Input parameters
#         self.addParameter(
#             QgsProcessingParameterFile(
#                 self.GRIDADMIN_INPUT,
#                 self.tr("Gridadmin file"), extension="h5")
#         )
#         self.addParameter(
#             QgsProcessingParameterFile(
#                 self.RESULTS_3DI_INPUT,
#                 self.tr("3Di simulation output"),
#                 extension="nc"
#             )
#         )
#         self.addParameter(QgsProcessingParameterRasterLayer(self.DEM_INPUT, self.tr("DEM")))
#         self.addParameter(
#             QgsProcessingParameterEnum(
#                 name=self.MODE_INPUT,
#                 description=self.tr("Output type"),
#                 options=[m.description for m in self.MODES],
#                 defaultValue=MODE_LINEAR,
#             )
#         )
#         self.addParameter(
#             QgsProcessingParameterFileDestination(
#                 self.OUTPUT_FILENAME,
#                 self.tr("Output file"),
#                 fileFilter="*.tif",
#             )
#         )
#
#     def processAlgorithm(self, parameters, context, feedback):
#         """
#         Create the water depth raster with the provided user inputs
#         """
#         dem_filename = self.parameterAsRasterLayer(parameters, self.DEM_INPUT, context).source()
#         gridadmin_path = parameters[self.GRIDADMIN_INPUT]
#         results_3di_path = parameters[self.RESULTS_3DI_INPUT]
#         mode_index = self.parameterAsEnum(parameters, self.MODE_INPUT, context)
#
#         waterdepth_output_file = Path(parameters[self.OUTPUT_FILENAME])
#         if not waterdepth_output_file:
#             raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT_FILENAME))
#
#         layer_name = Path(waterdepth_output_file).stem
#
#         if waterdepth_output_file.is_file():
#             waterdepth_output_file.unlink()
#
#         try:
#             calculate_waterdepth(
#                 gridadmin_path=gridadmin_path,
#                 results_3di_path=results_3di_path,
#                 dem_path=dem_filename,
#                 waterdepth_path=str(waterdepth_output_file),
#                 calculate_maximum_waterlevel=True,
#                 mode=self.MODES[mode_index].name,
#                 progress_func=Progress(feedback),
#             )
#         except CancelError:
#             # When the process is cancelled, we just show the intermediate product
#             pass
#         except KeyError as e:
#             if Path(results_3di_path).name == "aggregate_results_3di.nc" and e.args[0] == "s1_max":
#                 raise QgsProcessingException(
#                     "Input aggregation NetCDF does not contain maximum water level aggregation (s1_max)."
#                 )
#
#         layer = QgsRasterLayer(str(waterdepth_output_file), layer_name)
#         context.temporaryLayerStore().addMapLayer(layer)
#         layer_details = QgsProcessingContext.LayerDetails(layer_name, context.project(), self.WATER_DEPTH_OUTPUT)
#         context.addLayerToLoadOnCompletion(layer.id(), layer_details)
#         return {}


