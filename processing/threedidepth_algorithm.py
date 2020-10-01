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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsFeedback,
    QgsProcessingException,
    QgsProcessingAlgorithm,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFile,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from threedidepth.calculate import calculate_waterdepth
from threedidepth.calculate import (
    MODE_INTERPOLATED,
    MODE_CONSTANT,
    MODE_INTERPOLATED_S1,
    MODE_CONSTANT_S1,
    MODE_COPY
)


Mode = namedtuple("Mode", ["name", "description"])


class ThreediDepth(QgsProcessingAlgorithm):
    """
    Calculates waterdepths for 3Di results
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    MODES = [
        Mode(MODE_INTERPOLATED, "Interpolated waterdepth"),
        Mode(MODE_CONSTANT, "Waterdepth"),
        Mode(MODE_INTERPOLATED_S1, "Interpolated waterlevel"),
        Mode(MODE_CONSTANT_S1, "Waterlevel"),
    ]

    GRIDADMIN_INPUT = 'GRIDADMIN_INPUT'
    RESULTS_3DI_INPUT = 'RESULTS_3DI_INPUT'
    DEM_INPUT = 'DEM_INPUT'
    MODE_INPUT = 'MODE_INPUT'
    CALCULATION_STEP_INPUT = 'CALCULATION_STEP_INPUT'
    WATERDEPTH_OUTPUT = 'WATERDEPTH_OUTPUT'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ThreediDepth()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'threedidepth'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Waterdepth')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Post-process results')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'postprocessing'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Calculate waterdepths for 3Di results.")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        # Input parameters
        self.addParameter(
            QgsProcessingParameterFile(
                self.GRIDADMIN_INPUT,
                self.tr('Gridadmin.h5 file'),
                extension="h5"
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.RESULTS_3DI_INPUT,
                self.tr('Results_3di.nc file'),
                extension="nc"
            )
        )
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.DEM_INPUT,
                self.tr('DEM')
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.MODE_INPUT,
                description=self.tr('Interpolation mode'),
                options=[m.description for m in self.MODES],
                defaultValue=MODE_INTERPOLATED
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.CALCULATION_STEP_INPUT,
                description=self.tr(
                    'The timestep in the simulation for which you want to generate a '
                    'waterdepth raster'
                ),
                defaultValue=-1
            )
        )

        # Output raster
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.WATERDEPTH_OUTPUT,
                self.tr('Waterdepth raster')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Create the waterdepth raster with the provided user settings
        """
        waterdepth_output_file = self.parameterAsOutputLayer(
            parameters, self.WATERDEPTH_OUTPUT, context
        )
        mode_index = self.parameterAsEnum(parameters, self.MODE_INPUT, context)
        try:
            calculate_waterdepth(
                gridadmin_path=parameters[self.GRIDADMIN_INPUT],
                results_3di_path=parameters[self.RESULTS_3DI_INPUT],
                dem_path=parameters[self.DEM_INPUT],
                waterdepth_path=waterdepth_output_file,
                calculation_step=parameters[self.CALCULATION_STEP_INPUT],
                mode=self.MODES[mode_index].name,
                progress_func=Progress(feedback),
            )
        except CancelError:
            # When the process is cancelled, we just show the intermediate product
            pass

        return {self.WATERDEPTH_OUTPUT: waterdepth_output_file}


class CancelError(Exception):
    """Error which gets raised when a user presses the 'cancel' button"""


class Progress:
    def __init__(self, feedback: QgsFeedback):
        self.feedback = feedback

    def __call__(self, progress: float):
        self.feedback.setProgress(progress * 100)
        if self.feedback.isCanceled():
            raise CancelError()
