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
from typing import List, Dict

import numpy as np
from osgeo import gdal
from qgis.core import QgsFeedback
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingException
from qgis.core import QgsProcessingParameterColor
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingUtils
from qgis.core import QgsRasterLayer
from qgis.PyQt.QtGui import QColor
from threedidepth.calculate import calculate_waterdepth, calculate_water_quality
from threedidepth.calculate import MODE_CONSTANT
from threedidepth.calculate import MODE_CONSTANT_VAR
from threedidepth.calculate import MODE_LIZARD
from threedidepth.calculate import MODE_LIZARD_VAR

from threedigrid.admin.gridresultadmin import GridH5WaterQualityResultAdmin
from threedigrid.admin.gridresultadmin import GridH5ResultAdmin
from threedigrid.admin.gridresultadmin import GridH5AggregateResultAdmin
from threedigrid.admin.gridresultadmin import CustomizedResultAdmin
from threedigrid.admin.gridresultadmin import CustomizedWaterQualityResultAdmin

import logging
from pathlib import Path

from threedi_results_analysis.processing.widgets.widgets import ThreediResultTimeSliderWidgetWrapper
from threedi_results_analysis.processing.widgets.widgets import SubstanceWidgetWrapper

from threedi_results_analysis.utils.color import color_ramp_from_data, COLOR_RAMP_OCEAN_HALINE
from threedi_results_analysis.utils.geo_utils import mask, multiband_raster_min_max
from threedi_results_analysis.utils.netcdf import substances_from_netcdf
from threedi_results_analysis.utils.styling import (
    apply_transparency_gradient,
    apply_gradient_ramp,
)

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

SINGLE = "SINGLE"
MULTIPLE = "MULTIPLE"
MAXIMUM = "MAXIMUM"

STYLE_DIR = Path(__file__).parent / "styles"

# Fix TEMPORARY FILE
# TODO: tests
# TODO: shortHelpStrings


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
    def data_type(self) -> str:
        """
        WATER_QUANTITY or WATER_QUALITY
        """
        return NotImplementedError("Subclasses must implement this method")

    @property
    def time_step_type(self) -> str:
        """
        SINGLE, MULTIPLE, or MAXIMUM
        """
        return NotImplementedError("Subclasses must implement this method")

    @property
    # Not implemented as proper abstractmethod because QgsProcessingAlgorithm already has a metaclass
    # and setting ABCMeta as metaclass creates complicated problems
    def output_modes(self) -> List[Mode]:
        """
        List of modes available for this processing algorithm
        """
        if self.data_type == WATER_QUANTITY:
            return [
                Mode(MODE_LIZARD, "Interpolated water depth"),
                Mode(MODE_LIZARD_VAR, "Interpolated water level"),
                Mode(MODE_CONSTANT, "Non-interpolated water depth"),
                Mode(MODE_CONSTANT_VAR, "Non-interpolated water level"),
            ]
        elif self.data_type == WATER_QUALITY:
            return [
                Mode(MODE_LIZARD_VAR, "Interpolated concentrations"),
                Mode(MODE_CONSTANT_VAR, "Non-interpolated concentrations"),
            ]

    @property
    def default_mode(self) -> Mode:
        """
        Mode to be set as the default in the user interface
        """
        if self.data_type == WATER_QUANTITY:
            return Mode(MODE_LIZARD, "Interpolated water depth")
        elif self.data_type == WATER_QUALITY:
            return Mode(MODE_LIZARD_VAR, "Interpolated concentrations")

    def calculation_steps(self, parameters, feedback):
        if self.time_step_type == SINGLE:
            return [parameters[CALCULATION_STEP_INPUT]]
        elif self.time_step_type == MULTIPLE:
            calculation_step_start = parameters[CALCULATION_STEP_START_INPUT]
            calculation_step_end = parameters[CALCULATION_STEP_END_INPUT]
            if calculation_step_end <= calculation_step_start:
                feedback.reportError(
                    "The last timestep should be larger than the first timestep.",
                    fatalError=True,
                )
                return {}
            calculation_steps = list(range(calculation_step_start, calculation_step_end))
            return calculation_steps
        elif self.time_step_type == MAXIMUM:
            return [None]

    @property
    def parameters(self) -> List:
        result = [
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
        ]
        if self.time_step_type == SINGLE:
            calculation_step_input_param = QgsProcessingParameterNumber(
                name=CALCULATION_STEP_INPUT,
                description="Time step",
                defaultValue=-1,
            )
            calculation_step_input_param.setMetadata(
                {
                    "widget_wrapper": {"class": ThreediResultTimeSliderWidgetWrapper},
                    "parentParameterName": NETCDF_INPUT
                }
            )
            result.insert(
                -1,
                calculation_step_input_param
            )
        elif self.time_step_type == MULTIPLE:
            calculation_step_start_input_param = QgsProcessingParameterNumber(
                    name=CALCULATION_STEP_START_INPUT,
                    description="First time step",
                    defaultValue=0,
                )
            calculation_step_start_input_param.setMetadata(
                {
                    "widget_wrapper": {"class": ThreediResultTimeSliderWidgetWrapper},
                    "parentParameterName": NETCDF_INPUT
                }
            )
            result.insert(
                -1,
                calculation_step_start_input_param
            )
            calculation_step_end_input_param = QgsProcessingParameterNumber(
                    name=CALCULATION_STEP_END_INPUT,
                    description="Last time step",
                    defaultValue=-1,
                )
            calculation_step_end_input_param.setMetadata(
                {
                    "widget_wrapper": {"class": ThreediResultTimeSliderWidgetWrapper},
                    "parentParameterName": NETCDF_INPUT
                }
            )
            result.insert(
                -1,
                calculation_step_end_input_param
            )
        if self.data_type == WATER_QUANTITY:
            result.insert(2, QgsProcessingParameterRasterLayer(DEM_INPUT, "DEM"))
        elif self.data_type == WATER_QUALITY:
            result.insert(
                2,
                QgsProcessingParameterRasterLayer(
                    WATER_DEPTH_INPUT,
                    "Water depth (mask layer)",
                    optional=True
                )
            )
            substance_param = QgsProcessingParameterString(
                SUBSTANCE_INPUT,
                "Substance",
            )
            substance_param.setMetadata(
                {
                    "widget_wrapper": {"class": SubstanceWidgetWrapper},
                    "parentParameterName": NETCDF_INPUT
                }
            )
            result.insert(3, substance_param)
            result.insert(
                4,
                QgsProcessingParameterColor(
                    COLOR_INPUT,
                    "Color",
                    defaultValue=QColor("brown")
                )
            )
        return result

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

    def get_substance_id(self, parameters, context):
        netcdf_input = self.parameterAsFile(parameters, NETCDF_INPUT, context)
        substance_id = self.parameterAsString(parameters, SUBSTANCE_INPUT, context)
        substances = substances_from_netcdf(netcdf_input)
        if substance_id not in substances:
            # Perhaps the substance name was given as input instead of the substance id
            for substance_id, substance_name in substances.items():
                if substance_name == substance_id:
                    substance_id = substance_id
                    break
        if substance_id not in substances:
            raise QgsProcessingException(f"Substance {substance_id} not found in file {netcdf_input}")
        return substance_id

    def get_threedidepth_args(self, parameters, context, feedback) -> Dict:
        args = {
                "gridadmin_path": parameters[GRIDADMIN_INPUT],
                "calculation_steps": self.calculation_steps(parameters, feedback),
                "mode": self.output_mode.name,
                "progress_func": Progress(feedback),
            }
        if self.data_type == WATER_QUANTITY:
            args.update(
                {
                    "results_3di_path": parameters[NETCDF_INPUT],
                    "dem_path": self.parameterAsRasterLayer(parameters, DEM_INPUT, context).source(),
                    "waterdepth_path": str(self.output_file(parameters, context)),
                }
            )
        elif self.data_type == WATER_QUALITY:
            netcdf_input = self.parameterAsFile(parameters, NETCDF_INPUT, context)
            gwq = GridH5WaterQualityResultAdmin(parameters[GRIDADMIN_INPUT], netcdf_input)
            variable = self.get_substance_id(parameters, context)
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
                }
            )
        if self.time_step_type == MAXIMUM:
            if self.data_type == WATER_QUANTITY:
                args.update({"calculate_maximum_waterlevel": True})
            elif self.data_type == WATER_QUALITY:
                args.update({"calculate_maximum_concentration": True})
        return args

    @property
    def results_reader(self):
        """Get the correct threedigrid ...ResultAdmin"""
        reader_classes = {
            "water_quality_results_3di.nc": GridH5WaterQualityResultAdmin,
            "results_3di.nc": GridH5ResultAdmin,
            "aggregate_results_3di.nc": GridH5AggregateResultAdmin,
            "customized_results_3di.nc": CustomizedResultAdmin,
            "customized_water_quality_results_3di.nc": CustomizedWaterQualityResultAdmin,
        }
        reader_class = reader_classes[self.netcdf_path.name]
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
        if self.time_step_type == MAXIMUM:
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
    def timestamps_seconds(self) -> List[int | None]:
        """
        Get the timestamps in seconds since start of simulation for the requested output time steps
        """
        if self.time_step_type == MAXIMUM:
            return [None]
        indices = self.threedidepth_args["calculation_steps"]
        reader = self.results_reader
        if self.data_type == WATER_QUALITY:
            # all substances have the same timestamps and there is always a substance1
            return reader.substance1.timestamps[indices]
        elif self.data_type == WATER_QUANTITY:
            return reader.nodes.timestamps[indices]

    def output_layer_name_from_parameters(self, parameters, context):
        mode_index = self.parameterAsEnum(parameters, MODE_INPUT, context)
        output_layer_name = self.output_modes[mode_index].description
        if self.data_type == WATER_QUALITY:
            gwq = GridH5WaterQualityResultAdmin(parameters[GRIDADMIN_INPUT], parameters[NETCDF_INPUT])
            substance_id = self.get_substance_id(parameters, context)
            substance_name = getattr(gwq, substance_id).name
            output_layer_name = f"{substance_name}: {output_layer_name}"
        if self.time_step_type == MAXIMUM:
            output_layer_name += " (Maximum)"
        return output_layer_name

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
        # Water quality part (1/2)
        if self.data_type == WATER_QUALITY:
            mask_layer = self.parameterAsRasterLayer(parameters, WATER_DEPTH_INPUT, context)
            masked_result_file_name = self.output_file(parameters, context)
            if mask_layer:
                output_file_generic_part = QgsProcessingUtils.generateTempFilename("non_masked.tif")
            else:
                output_file_generic_part = self.output_file(parameters, context)
        elif self.data_type == WATER_QUANTITY:
            output_file_generic_part = self.output_file(parameters, context)

        # Generic part
        mode_index = self.parameterAsEnum(parameters, MODE_INPUT, context)
        self.output_mode = self.output_modes[mode_index]
        self.threedidepth_args = self.get_threedidepth_args(parameters=parameters, context=context, feedback=feedback)
        if Path(output_file_generic_part).is_file():
            Path(output_file_generic_part).unlink()
        if self.data_type == WATER_QUALITY:
            self.threedidepth_args["output_path"] = output_file_generic_part
        elif self.data_type == WATER_QUANTITY:
            self.threedidepth_args["waterdepth_path"] = output_file_generic_part
        try:
            self.threedidepth_method(**self.threedidepth_args)
        except CancelError:
            # When the process is cancelled, we just show the intermediate product
            pass
        except KeyError as e:
            if Path(self.netcdf_path).name == "aggregate_results_3di.nc" and e.args[0] == "s1_max":
                raise QgsProcessingException(
                    "Input aggregation NetCDF does not contain maximum water level aggregation (s1_max)."
                )

        # Water quality part (2/2)
        if self.data_type == WATER_QUALITY:
            self.color = self.parameterAsColor(parameters, COLOR_INPUT, context)
            if mask_layer:
                if Path(masked_result_file_name).is_file():
                    Path(masked_result_file_name).unlink()
                mask(source=str(output_file_generic_part), mask=mask_layer.source(), output=masked_result_file_name)
                final_output = masked_result_file_name
            else:
                final_output = output_file_generic_part
        elif self.data_type == WATER_QUANTITY:
            final_output = output_file_generic_part

        try:
            self.set_timestamps_as_band_descriptions(
                raster=str(final_output)
            )
        except ValueError:
            # occurs when water quality results have missing time units, known issue (2025-10-02)
            pass

        # Save data to be used in postProcessAlgorithm
        self.output_layer_name = self.output_layer_name_from_parameters(parameters, context)
        self._results = {OUTPUT_FILENAME: str(final_output)}
        return self._results

    def postProcessAlgorithm(self, context, feedback):
        output_file = self._results[OUTPUT_FILENAME]
        output_layers = []
        timestamps_seconds = self.timestamps_seconds
        threedidepth_calculation_steps = self.threedidepth_args.get("calculation_steps") or [None]
        for i, time_step in enumerate(threedidepth_calculation_steps):
            if self.time_step_type in [SINGLE, MULTIPLE]:
                layer_name_suffix = f" ({str(timedelta(seconds=int(timestamps_seconds[i])))})"
            else:
                layer_name_suffix = ""
            layer_name = f"{self.output_layer_name}{layer_name_suffix}"
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
    def data_type(self) -> str:
        """
        WATER_QUANITTY or WATER_QUALITY
        """
        return WATER_QUANTITY

    @property
    def time_step_type(self) -> str:
        return SINGLE

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
    def data_type(self) -> str:
        """
        WATER_QUANTITY or WATER_QUALITY
        """
        return WATER_QUANTITY

    @property
    def time_step_type(self) -> str:
        return MAXIMUM

    def createInstance(self):
        return WaterDepthOrLevelMaximumAlgorithm()

    def name(self):
        """Returns the algorithm name, used for identifying the algorithm"""
        return "waterdepthorlevelmaximum"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
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
    @property
    def data_type(self) -> str:
        """
        WATER_QUANITTY or WATER_QUALITY
        """
        return WATER_QUANTITY

    @property
    def time_step_type(self) -> str:
        return MULTIPLE

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
    def data_type(self) -> str:
        """
        WATER_QUANITTY or WATER_QUALITY
        """
        return WATER_QUALITY

    @property
    def time_step_type(self) -> str:
        return SINGLE

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


class ConcentrationMultipleTimeStepAlgorithm(BaseThreediDepthAlgorithm):
    """
    Calculates concentration rasters from 3Di result NetCDF for multiple time steps
    """
    @property
    def data_type(self) -> str:
        """
        WATER_QUANTITY or WATER_QUALITY
        """
        return WATER_QUALITY

    @property
    def time_step_type(self) -> str:
        return MULTIPLE

    def createInstance(self):
        return ConcentrationMultipleTimeStepAlgorithm()

    def name(self):
        """Returns the algorithm name, used for identifying the algorithm"""
        return "concentrationmultipletimestep"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return "Concentration raster (multiple time steps)"

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


class ConcentrationMaximumAlgorithm(BaseThreediDepthAlgorithm):
    """
    Calculates maximum concentration raster from 3Di result NetCDF
    """
    @property
    def data_type(self) -> str:
        """
        WATER_QUANITTY or WATER_QUALITY
        """
        return WATER_QUALITY

    @property
    def time_step_type(self) -> str:
        return MAXIMUM

    def createInstance(self):
        return ConcentrationMaximumAlgorithm()

    def name(self):
        """Returns the algorithm name, used for identifying the algorithm"""
        return "concentrationmaximum"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return "Concentration raster (maximum)"

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
