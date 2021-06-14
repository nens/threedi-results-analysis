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
from processing.gui.NumberInputPanel import NumberInputPanel
from processing.gui.wrappers import DIALOG_STANDARD
from processing.gui.wrappers import WidgetWrapper
from qgis.core import QgsFeedback
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QCoreApplication
from threedidepth.calculate import calculate_waterdepth
from threedidepth.calculate import MODE_CONSTANT
from threedidepth.calculate import MODE_CONSTANT_S1
from threedidepth.calculate import MODE_LINEAR
from threedidepth.calculate import MODE_LIZARD
from threedidepth.calculate import MODE_LIZARD_S1
from ThreeDiToolbox.utils.user_messages import pop_up_info

import h5py
import logging
import os


logger = logging.getLogger(__name__)
pluginPath = os.path.split(os.path.dirname(__file__))[0]
Mode = namedtuple("Mode", ["name", "description"])


class ProcessingParamterNetcdfNumber(QgsProcessingParameterNumber):
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
            self._widget = NumberInputPanel(
                QgsProcessingParameterNumber(
                    self.parameterDefinition().name(),
                    defaultValue=self.parameterDefinition().defaultValue(),
                    minValue=-1,
                    optional=self.parameterDefinition().optional,
                )
            )
        return self._widget

    def value(self):
        return self._widget.getValue()

    def postInitialize(self, wrappers):
        if self.dialogType != DIALOG_STANDARD:
            return

        # Connect the result-file parameter to the TimeSliderWidget
        for wrapper in wrappers:
            if wrapper.parameterDefinition().name() == self.param.parentParameterName:
                wrapper.wrappedWidget().fileChanged.connect(self._widget.new_file_event)


WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, "processing", "ui", "widgetTimeSlider.ui")
)


class TimeSliderWidget(BASE, WIDGET):
    """Timeslider form widget

    Provide a horizontal slider and an LCD display connected to the slider.
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

    def set_lcd_value(self, index: int):
        self.index = index
        if self.timestamps is not None:
            value = self.timestamps[index]
        else:
            value = 0
        lcd_value = self.format_lcd_value(value)
        self.lcdNumber.display(lcd_value)

    def format_lcd_value(self, value: float) -> str:
        days, seconds = divmod(int(value), 24 * 60 * 60)
        hours, seconds = divmod(seconds, 60 * 60)
        minutes, seconds = divmod(seconds, 60)
        formatted_display = "{:d} {:02d}:{:02d}".format(days, hours, minutes)
        return formatted_display

    def reset(self):
        self.setDisabled(True)
        self.index = None
        self.timestamps = None
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(0)
        self.horizontalSlider.setValue(0)

    def new_file_event(self, file_path):
        """New file has been selected by the user

        Try to read in the timestamps from the file
        """
        if file_path == "":
            self.reset()
            return

        try:
            with h5py.File(file_path, "r") as results:
                timestamps = results["time"].value
                self.set_timestamps(timestamps)
        except Exception as e:
            logger.exception(e)
            pop_up_info(
                msg="Unable to read the file, see the logging for more information."
            )
            self.reset()


WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, "processing", "ui", "widgetTimeSliderCheckbox.ui")
)


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


class ThreediDepth(QgsProcessingAlgorithm):
    """
    Calculates waterdepths for 3Di results
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
    WATER_DEPTH_OUTPUT = "WATER_DEPTH_OUTPUT"

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return ThreediDepth()

    def name(self):
        """Returns the algorithm name, used for identifying the algorithm"""
        return "threedidepth"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Water depth")

    def group(self):
        """Returns the name of the group this algorithm belongs to"""
        return self.tr("Post-process results")

    def groupId(self):
        """Returns the unique ID of the group this algorithm belongs to"""
        return "postprocessing"

    def shortHelpString(self):
        """Returns a localised short helper string for the algorithm"""
        return self.tr("Calculate water depths for 3Di results.")

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm"""
        # Input parameters
        self.addParameter(
            QgsProcessingParameterFile(
                self.GRIDADMIN_INPUT, self.tr("Gridadmin.h5 file"), extension="h5"
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.RESULTS_3DI_INPUT, self.tr("Results_3di.nc file"), extension="nc"
            )
        )
        self.addParameter(
            QgsProcessingParameterRasterLayer(self.DEM_INPUT, self.tr("DEM"))
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.MODE_INPUT,
                description=self.tr("Interpolation mode"),
                options=[m.description for m in self.MODES],
                defaultValue=MODE_LINEAR,
            )
        )
        self.addParameter(
            ProcessingParamterNetcdfNumber(
                name=self.CALCULATION_STEP_INPUT,
                description=self.tr(
                    "The timestep in the simulation for which you want to generate a raster"
                ),
                defaultValue=-1,
                parentParameterName=self.RESULTS_3DI_INPUT,
            )
        )
        self.addParameter(
            ProcessingParamterNetcdfNumber(
                name=self.CALCULATION_STEP_END_INPUT,
                description=self.tr(
                    "In case you want to export water depths of multiple timesteps, enable this option and select "
                    "the last timestep. All water depth rasters between these two timesteps will be generated."
                ),
                defaultValue=-2,
                parentParameterName=self.RESULTS_3DI_INPUT,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                name=self.AS_NETCDF_INPUT,
                description="export the water depth as a netcdf file",
                defaultValue=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.WATER_DEPTH_OUTPUT, self.tr("Water depth raster")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Create the waterdepth raster with the provided user inputs
        """
        waterdepth_output_file = self.parameterAsOutputLayer(
            parameters, self.WATER_DEPTH_OUTPUT, context
        )
        mode_index = self.parameterAsEnum(parameters, self.MODE_INPUT, context)

        endstep = parameters[self.CALCULATION_STEP_END_INPUT]
        if endstep:
            if endstep <= parameters[self.CALCULATION_STEP_INPUT]:
                feedback.reportError(
                    "The last timestep should be larger than the first timestep.",
                    fatalError=True,
                )
                return {}
            timesteps = list(range(parameters[self.CALCULATION_STEP_INPUT], endstep))
        else:
            timesteps = [parameters[self.CALCULATION_STEP_INPUT]]

        try:
            calculate_waterdepth(
                gridadmin_path=parameters[self.GRIDADMIN_INPUT],
                results_3di_path=parameters[self.RESULTS_3DI_INPUT],
                dem_path=parameters[self.DEM_INPUT],
                waterdepth_path=waterdepth_output_file,
                calculation_steps=timesteps,
                mode=self.MODES[mode_index].name,
                progress_func=Progress(feedback),
                netcdf=parameters[self.AS_NETCDF_INPUT],
            )
        except CancelError:
            # When the process is cancelled, we just show the intermediate product
            pass

        return {self.WATER_DEPTH_OUTPUT: waterdepth_output_file}


class CancelError(Exception):
    """Error which gets raised when a user presses the 'cancel' button"""


class Progress:
    def __init__(self, feedback: QgsFeedback):
        self.feedback = feedback

    def __call__(self, progress: float):
        self.feedback.setProgress(progress * 100)
        if self.feedback.isCanceled():
            raise CancelError()
