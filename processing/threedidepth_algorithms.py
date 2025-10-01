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
from processing.gui.wrappers import DIALOG_STANDARD
from processing.gui.wrappers import WidgetWrapper
from qgis.core import QgsFeedback
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingContext
from qgis.core import QgsProcessingException
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsMeshLayer
from qgis.core import QgsRasterLayer
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import QComboBox
from threedidepth.calculate import calculate_waterdepth
from threedidepth.calculate import MODE_CONSTANT
from threedidepth.calculate import MODE_CONSTANT_S1
from threedidepth.calculate import MODE_LINEAR
from threedidepth.calculate import MODE_LIZARD
from threedidepth.calculate import MODE_LIZARD_S1
from threedi_results_analysis.utils.user_messages import pop_up_info

import h5py
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)
plugin_path = Path(__file__).resolve().parent.parent
Mode = namedtuple("Mode", ["name", "description"])


class ProcessingParameterNetcdfNumber(QgsProcessingParameterNumber):
    def __init__(self, *args, parentParameterName="", optional=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.parentParameterName = parentParameterName
        self.optional = optional
        self.setMetadata({"widget_wrapper": {"class": ThreediResultTimeSliderWidget}})


class ThreediResultTimeSliderWidget(WidgetWrapper):
    def createWidget(self):
        if self.dialogType == DIALOG_STANDARD:
            if not self.parameterDefinition().optional:
                self._widget = TimeSliderWidget()
            else:
                self._widget = CheckboxTimeSliderWidget()
        else:
            self._widget = TimeStepsCombobox()
        return self._widget

    def value(self):
        return self._widget.getValue()

    def postInitialize(self, wrappers):
        # Connect the result-file parameter to the TimeSliderWidget/TimeStepsCombobox
        for wrapper in wrappers:
            if wrapper.parameterDefinition().name() == self.param.parentParameterName:
                wrapper.wrappedWidget().fileChanged.connect(self._widget.new_file_event)


WIDGET, BASE = uic.loadUiType(plugin_path / "processing" / "ui" / "widgetTimeSlider.ui")


class TimeSliderWidget(BASE, WIDGET):
    """
    Timeslider form widget. Provide a horizontal slider and an LCD connected to the slider.
    """

    def __init__(self):
        super(TimeSliderWidget, self).__init__(None)
        self.setupUi(self)
        self.horizontalSlider.valueChanged.connect(self.set_lcd_value)
        self.index = None
        self.timestamps = None
        self.reset()

    def getValue(self):
        return self.index

    def set_timestamps(self, timestamps):
        self.setDisabled(False)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(len(timestamps) - 1)
        self.timestamps = timestamps
        self.set_lcd_value(0)  # also sets self.index

    def set_lcd_value(self, index: int):
        self.index = index
        if self.timestamps is not None:
            value = self.timestamps[index]
        else:
            value = 0
        lcd_value = format_timestep_value(value=value, drop_leading_zero=True)
        self.lcdNumber.display(lcd_value)

    def reset(self):
        self.setDisabled(True)
        self.index = None
        self.timestamps = None
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(0)
        self.horizontalSlider.setValue(0)

    def new_file_event(self, file_path):
        """New file has been selected by the user. Try to read in the timestamps from the file."""
        if not file_path or not os.path.isfile(file_path):
            self.reset()
            return

        try:
            with h5py.File(file_path, "r") as results:
                timestamps = results["time"][()]
                self.set_timestamps(timestamps)
        except Exception as e:
            logger.exception(e)
            pop_up_info(msg="Unable to read the file, see the logging for more information.")
            self.reset()


WIDGET, BASE = uic.loadUiType(plugin_path / "processing" / "ui" / "widgetTimeSliderCheckbox.ui")


class CheckboxTimeSliderWidget(TimeSliderWidget, WIDGET, BASE):
    """Timeslider widget with a checkbox to enable/disable the timeslider"""

    def __init__(self):
        super().__init__()
        self.horizontalSlider.setDisabled(not self.checkBox.isChecked())
        self.checkBox.stateChanged.connect(self.new_check_box_event)

    def getValue(self):
        if self.checkBox.isChecked():
            return self.index
        else:
            return None

    def new_check_box_event(self, state):
        self.horizontalSlider.setDisabled(not self.checkBox.isChecked())


class TimeStepsCombobox(QComboBox):
    """Combobox with populated timestep data."""

    def getValue(self):
        return self.currentIndex()

    def populate_timestamps(self, timestamps):
        for i, value in enumerate(timestamps):
            human_readable_value = format_timestep_value(value)
            if human_readable_value.startswith("0"):
                human_readable_value = human_readable_value.split(" ", 1)[-1]
            self.addItem(human_readable_value)
        self.setCurrentIndex(0)

    def new_file_event(self, file_path):
        """New file has been selected by the user. Try to read in the timestamps from the file."""
        if not file_path or not os.path.isfile(file_path):
            self.clear()
            return

        try:
            with h5py.File(file_path, "r") as results:
                timestamps = results["time"][()]
                self.populate_timestamps(timestamps)
        except Exception as e:
            logger.exception(e)
            pop_up_info(msg="Unable to read the file, see the logging for more information.")
            self.clear()


class ThreediDepthAlgorithm(QgsProcessingAlgorithm):
    """
    Calculates water depth or water level rasters from 3Di result NetCDF
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    MODES = [
        Mode(MODE_LIZARD, "Interpolated water depth"),
        Mode(MODE_LIZARD_S1, "Interpolated water level"),
        Mode(MODE_CONSTANT, "Non-interpolated water depth"),
        Mode(MODE_CONSTANT_S1, "Non-interpolated water level"),
    ]

    GRIDADMIN_INPUT = "GRIDADMIN_INPUT"
    RESULTS_3DI_INPUT = "RESULTS_3DI_INPUT"
    DEM_INPUT = "DEM_INPUT"
    MODE_INPUT = "MODE_INPUT"
    CALCULATION_STEP_INPUT = "CALCULATION_STEP_INPUT"
    AS_NETCDF_INPUT = "AS_NETCDF_INPUT"
    CALCULATION_STEP_END_INPUT = "CALCULATION_STEP_END_INPUT"
    WATER_DEPTH_LEVEL_NAME = "WATER_DEPTH_LEVEL_NAME"
    OUTPUT_DIRECTORY = "OUTPUT_DIRECTORY"
    WATER_DEPTH_OUTPUT = "WATER_DEPTH_OUTPUT"

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return ThreediDepthAlgorithm()

    def name(self):
        """Returns the algorithm name, used for identifying the algorithm"""
        return "threedidepth"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Water depth/level raster")

    def group(self):
        """Returns the name of the group this algorithm belongs to"""
        return self.tr("Post-process results")

    def groupId(self):
        """Returns the unique ID of the group this algorithm belongs to"""
        return "postprocessing"

    def shortHelpString(self):
        """Returns a localised short helper string for the algorithm"""
        return self.tr(
            """
            <h3>Calculate water depth or level raster for specified timestep(s)</h3>
            <p>The 3Di simulation result contains a single water level for each cell, for each time step. However, the water depth is different for each pixel within the cell. To calculate water depths from water levels, the DEM needs to be subtracted from the water level. This results in a raster with a water depth value for each pixel.</p>
            <p>For some applications, it is useful to have water levels as a raster file. For example, to use them as <i>Initial water levels</i> in the next simulation.</p>
            <p>It is often preferable to spatially interpolate the water levels. This is recommended to use if the water level gradients are large, such as is often the case in sloping areas.</p>
            <h3>Parameters</h3>
            <h4>Gridadmin file</h4>
            <p>HDF5 file (*.h5) containing the computational grid of a 3Di model</p>
            <h4>3Di simulation output (.nc)</h4>
            <p>NetCDF (*.nc) containing the results or aggregated resultes of a 3Di simulation. When using aggregated results (aggregate_results_3di.nc), make sure to use "maximum water level" as one of the aggregation variables in the simulation.</p>
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
        )

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm"""
        # Input parameters
        self.addParameter(
            QgsProcessingParameterFile(
                self.GRIDADMIN_INPUT,
                self.tr("Gridadmin file"), extension="h5")
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.RESULTS_3DI_INPUT,
                self.tr("3Di simulation output (.nc)"),
                extension="nc"
            )
        )
        self.addParameter(QgsProcessingParameterRasterLayer(self.DEM_INPUT, self.tr("DEM")))
        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.MODE_INPUT,
                description=self.tr("Output type"),
                options=[m.description for m in self.MODES],
                defaultValue=MODE_LINEAR,
            )
        )
        self.addParameter(
            ProcessingParameterNetcdfNumber(
                name=self.CALCULATION_STEP_INPUT,
                description=self.tr("Time step"),
                defaultValue=-1,
                parentParameterName=self.RESULTS_3DI_INPUT,
            )
        )
        self.addParameter(
            ProcessingParameterNetcdfNumber(
                name=self.CALCULATION_STEP_END_INPUT,
                description=self.tr("Last time step"),
                defaultValue=-2,
                parentParameterName=self.RESULTS_3DI_INPUT,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.WATER_DEPTH_LEVEL_NAME,
                self.tr("Output file name"),
                defaultValue="water_depth_level",
            )
        )
        output_param = QgsProcessingParameterFile(
            self.OUTPUT_DIRECTORY,
            self.tr("Output directory"),
            behavior=QgsProcessingParameterFile.Behavior.Folder,
        )
        self.addParameter(output_param)
        self.addParameter(
            QgsProcessingParameterBoolean(
                name=self.AS_NETCDF_INPUT,
                description="Save to NetCDF (experimental)",
                defaultValue=False,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Create the water depth raster with the provided user inputs
        """
        dem_filename = self.parameterAsRasterLayer(parameters, self.DEM_INPUT, context).source()
        gridadmin_path = parameters[self.GRIDADMIN_INPUT]
        results_3di_path = parameters[self.RESULTS_3DI_INPUT]
        mode_index = self.parameterAsEnum(parameters, self.MODE_INPUT, context)
        step = parameters[self.CALCULATION_STEP_INPUT]
        endstep = parameters[self.CALCULATION_STEP_END_INPUT]
        if endstep:
            if endstep <= step:
                feedback.reportError(
                    "The last timestep should be larger than the first timestep.",
                    fatalError=True,
                )
                return {}
            timesteps = list(range(step, endstep))
        else:
            timesteps = [step]

        raster_filename = parameters[self.WATER_DEPTH_LEVEL_NAME]
        if not raster_filename:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.WATER_DEPTH_LEVEL_NAME))

        output_location = parameters[self.OUTPUT_DIRECTORY]
        if not output_location:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT_DIRECTORY))

        as_netcdf = parameters[self.AS_NETCDF_INPUT]
        raster_extension = "nc" if as_netcdf else "tif"
        raster_filename_with_ext = f"{raster_filename}.{raster_extension}"
        waterdepth_output_file = os.path.join(output_location, raster_filename_with_ext)
        if os.path.isfile(waterdepth_output_file):
            os.remove(waterdepth_output_file)

        try:
            calculate_waterdepth(
                gridadmin_path=gridadmin_path,
                results_3di_path=results_3di_path,
                dem_path=dem_filename,
                waterdepth_path=waterdepth_output_file,
                calculation_steps=timesteps,
                mode=self.MODES[mode_index].name,
                progress_func=Progress(feedback),
                netcdf=as_netcdf,
            )
        except CancelError:
            # When the process is cancelled, we just show the intermediate product
            pass
        except KeyError as e:
            if Path(results_3di_path).name == "aggregate_results_3di.nc" and e.args[0] == "s1_max":
                raise QgsProcessingException(
                    "Input aggregation NetCDF does not contain maximum water level aggregation (s1_max)."
                )

        if as_netcdf:
            layer = QgsMeshLayer(waterdepth_output_file, raster_filename, "mdal")
        else:
            layer = QgsRasterLayer(waterdepth_output_file, raster_filename)
        context.temporaryLayerStore().addMapLayer(layer)
        layer_details = QgsProcessingContext.LayerDetails(raster_filename, context.project(), self.WATER_DEPTH_OUTPUT)
        context.addLayerToLoadOnCompletion(layer.id(), layer_details)
        return {}


class ThreediMaxDepthAlgorithm(QgsProcessingAlgorithm):
    """
    Calculates maximum water depth or water level rasters from 3Di result NetCDF
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    MODES = [
        Mode(MODE_LIZARD, "Interpolated water depth"),
        Mode(MODE_LIZARD_S1, "Interpolated water level"),
        Mode(MODE_CONSTANT, "Non-interpolated water depth"),
        Mode(MODE_CONSTANT_S1, "Non-interpolated water level"),
    ]

    GRIDADMIN_INPUT = "GRIDADMIN_INPUT"
    RESULTS_3DI_INPUT = "RESULTS_3DI_INPUT"
    DEM_INPUT = "DEM_INPUT"
    MODE_INPUT = "MODE_INPUT"
    OUTPUT_FILENAME = "OUTPUT_FILENAME"
    WATER_DEPTH_OUTPUT = "WATER_DEPTH_OUTPUT"

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return ThreediMaxDepthAlgorithm()

    def name(self):
        """Returns the algorithm name, used for identifying the algorithm"""
        return "threedidepth_max"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Maximum water depth/level raster")

    def group(self):
        """Returns the name of the group this algorithm belongs to"""
        return self.tr("Post-process results")

    def groupId(self):
        """Returns the unique ID of the group this algorithm belongs to"""
        return "postprocessing"

    def shortHelpString(self):
        """Returns a localised short helper string for the algorithm"""
        return self.tr(
            """
            <h3>Calculate maximum water depth/level raster over all time steps in the simulation.</h3>
            <p>The 3Di simulation result contains a single water level for each cell, for each time step. However, the water depth is different for each pixel within the cell. To calculate water depths from water levels, the DEM needs to be subtracted from the water level. This results in a raster with a water depth value for each pixel.</p>
            <p>For some applications, it is useful to have water levels as a raster file. For example, to use them as <i>Initial water levels</i> in the next simulation.</p>
            <p>It is often preferable to spatially interpolate the water levels. This is recommended to use if the water level gradients are large, such as is often the case in sloping areas.</p>
            <p>Note that the maximum water level may occur at different time steps in different cells. Therefore, the maximum water level situation that this tool calculates may never have occurred as such during the simulation.<\p>
            <h3>Parameters</h3>
            <h4>Gridadmin file</h4>
            <p>HDF5 file (*.h5) containing the computational grid of a 3Di model</p>
            <h4>3Di simulation output</h4>
            <p>NetCDF (*.nc) containing the results or aggregated resultes of a 3Di simulation. When using aggregated results (aggregate_results_3di.nc), make sure to use "maximum water level" as one of the aggregation variables in the simulation.</p>
            <h4>DEM</h4>
            <p>Digital elevation model (.tif) that was used as input for the 3Di model used for this simulation. Using a different DEM in this tool than in the simulation may give unexpected results.</p>
            <h4>Output type</h4>
            <p>Choose between water depth (m above the surface) and water level (m MSL), with or without spatial interpolation.</p>
            <h4>Output file</h4>
            <p>Destination file path for the water depth/level raster</p>
            """
        )

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm"""
        # Input parameters
        self.addParameter(
            QgsProcessingParameterFile(
                self.GRIDADMIN_INPUT,
                self.tr("Gridadmin file"), extension="h5")
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.RESULTS_3DI_INPUT,
                self.tr("3Di simulation output"),
                extension="nc"
            )
        )
        self.addParameter(QgsProcessingParameterRasterLayer(self.DEM_INPUT, self.tr("DEM")))
        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.MODE_INPUT,
                description=self.tr("Output type"),
                options=[m.description for m in self.MODES],
                defaultValue=MODE_LINEAR,
            )
        )
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_FILENAME,
                self.tr("Output file"),
                fileFilter="*.tif",
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Create the water depth raster with the provided user inputs
        """
        dem_filename = self.parameterAsRasterLayer(parameters, self.DEM_INPUT, context).source()
        gridadmin_path = parameters[self.GRIDADMIN_INPUT]
        results_3di_path = parameters[self.RESULTS_3DI_INPUT]
        mode_index = self.parameterAsEnum(parameters, self.MODE_INPUT, context)

        waterdepth_output_file = parameters[self.OUTPUT_FILENAME]
        if not waterdepth_output_file:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT_FILENAME))

        layer_name = Path(waterdepth_output_file).stem

        if os.path.isfile(waterdepth_output_file):
            os.remove(waterdepth_output_file)

        try:
            calculate_waterdepth(
                gridadmin_path=gridadmin_path,
                results_3di_path=results_3di_path,
                dem_path=dem_filename,
                waterdepth_path=waterdepth_output_file,
                calculate_maximum_waterlevel=True,
                mode=self.MODES[mode_index].name,
                progress_func=Progress(feedback),
            )
        except CancelError:
            # When the process is cancelled, we just show the intermediate product
            pass
        except KeyError as e:
            if Path(results_3di_path).name == "aggregate_results_3di.nc" and e.args[0] == "s1_max":
                raise QgsProcessingException(
                    "Input aggregation NetCDF does not contain maximum water level aggregation (s1_max)."
                )

        layer = QgsRasterLayer(waterdepth_output_file, layer_name)
        context.temporaryLayerStore().addMapLayer(layer)
        layer_details = QgsProcessingContext.LayerDetails(layer_name, context.project(), self.WATER_DEPTH_OUTPUT)
        context.addLayerToLoadOnCompletion(layer.id(), layer_details)
        return {}


class CancelError(Exception):
    """Error which gets raised when a user presses the 'cancel' button"""


class Progress:
    def __init__(self, feedback: QgsFeedback):
        self.feedback = feedback

    def __call__(self, progress: float):
        self.feedback.setProgress(progress * 100)
        if self.feedback.isCanceled():
            raise CancelError()


def format_timestep_value(value: float, drop_leading_zero: bool = False) -> str:
    days, seconds = divmod(int(value), 24 * 60 * 60)
    hours, seconds = divmod(seconds, 60 * 60)
    minutes, seconds = divmod(seconds, 60)

    if days == 0 and drop_leading_zero:
        formatted_display = "{:02d}:{:02d}".format(hours, minutes)
        return formatted_display

    formatted_display = "{:d} {:02d}:{:02d}".format(days, hours, minutes)
    return formatted_display
