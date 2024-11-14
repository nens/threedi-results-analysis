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
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingException
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFileDestination
from qgis.PyQt.QtCore import QCoreApplication
from threedigrid.admin.gridresultadmin import GridH5StructureControl
from threedigrid.admin.structure_controls.exporters import (
    structure_control_actions_to_csv,
)


class StructureControlActionAlgorithm(QgsProcessingAlgorithm):
    """
    Converts a structure control actions NetCDF to CSV
    """

    SCA_INPUT = "SCA_INPUT"
    OUTPUT_FILENAME = "OUTPUT_FILENAME"
    GRIDADMIN_INPUT = "GRIDADMIN_INPUT"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return StructureControlActionAlgorithm()

    def name(self):
        return "structure_control_actions_csv"

    def displayName(self):
        return self.tr("Convert structure control actions")

    def group(self):
        return self.tr("Post-process results")

    def groupId(self):
        return "postprocessing"

    def shortHelpString(self):
        return self.tr("Convert a structure control actions NetCDF to CSV")

    def initAlgorithm(self, config=None):
        # Input parameters
        self.addParameter(
            QgsProcessingParameterFile(self.GRIDADMIN_INPUT, self.tr("Gridadmin.h5 file"), extension="h5")
        )
        self.addParameter(
            QgsProcessingParameterFile(self.SCA_INPUT, self.tr("structure_control_actions_3di.nc file"), extension="nc")
        )
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_FILENAME,
                self.tr("Destination CSV file path"),
                fileFilter="*.csv",
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Create the water depth raster with the provided user inputs
        """
        gridadmin_path = parameters[self.GRIDADMIN_INPUT]
        results_3di_path = parameters[self.SCA_INPUT]
        csv_output_file = parameters[self.OUTPUT_FILENAME]

        if not csv_output_file:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT_FILENAME))

        # https://threedigrid.readthedocs.io/en/latest/structure_control.html
        gst = GridH5StructureControl(gridadmin_path, results_3di_path)
        try:
            structure_control_actions_to_csv(gst, csv_output_file)
        except Exception as e:
            return {"result": False, "error": str(e)}

        return {"result": True}
