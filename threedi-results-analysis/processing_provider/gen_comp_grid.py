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

import os
import sys

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsSettings,
    QgsVectorLayer,
)
from qgis.utils import iface
from ..utils import same_path

try:
    from threedigrid_builder import make_gridadmin, SchematisationError
except (ImportError, ModuleNotFoundError, FileNotFoundError):
    # TODO - adding the wheel with dlls fails - the module needs to be installed with its own deps using pip
    this_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(this_dir)
    whl_path = os.path.join(parent_dir, "deps", "threedigrid_builder-1.3.5-cp39-cp39-win_amd64.whl")
    sys.path.append(whl_path)
    from threedigrid_builder import make_gridadmin, SchematisationError


class ThreeDiGenerateCompGridAlgorithm(QgsProcessingAlgorithm):
    """ Generate a gridadmin.h5 file ot of Spatialite db and DEM """

    INPUT_SPATIALITE = "INPUT_SPATIALITE"
    INPUT_DEM = "INPUT_DEM"
    ALLOW_DIFF_DEM = "ALLOW_DIFF_DEM"
    OUTPUT = "OUTPUT"

    def flags(self):
        return super().flags()

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ThreeDiGenerateCompGridAlgorithm()

    def name(self):
        return 'threedi_generate_computational_grid'

    def displayName(self):
        return self.tr('Generate computational grid')

    def group(self):
        return self.tr('')

    def groupId(self):
        return ''

    def shortHelpString(self):
        return self.tr("Generate computational grid")

    def initAlgorithm(self, config=None):

        s = QgsSettings()
        last_input_sqlite = s.value("threedi-results-analysis/generate_computational_grid/last_input_sqlite", None)
        last_input_dem = s.value("threedi-results-analysis/generate_computational_grid/last_input_dem", None)
        last_output = s.value("threedi-results-analysis/generate_computational_grid/last_output", None)

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_SPATIALITE,
                self.tr("Input SpatiaLite file"),
                behavior=QgsProcessingParameterFile.File,
                defaultValue=last_input_sqlite
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_DEM,
                self.tr("Input DEM file"),
                behavior=QgsProcessingParameterFile.File,
                defaultValue=last_input_dem
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ALLOW_DIFF_DEM,
                self.tr("Allow to use a DEM different from Spatialite settings"),
                defaultValue=False
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr("Output computational grid file"),
                fileFilter="*.h5",
                defaultValue=last_output
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        input_slite = self.parameterAsFile(parameters, self.INPUT_SPATIALITE, context)
        if not input_slite:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_SPATIALITE))

        input_dem = self.parameterAsFile(parameters, self.INPUT_DEM, context)
        if not input_dem:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_DEM))

        allow_diff_dem = self.parameterAsBoolean(parameters, self.ALLOW_DIFF_DEM, context)

        uri = input_slite + f"|layername=v2_global_settings"
        feedback.pushInfo(f"Reading DEM settings from: {uri}")
        settings_lyr = QgsVectorLayer(uri, "glob_settings", "ogr")
        if not settings_lyr.isValid():
            err = f"Global Spatialite settings table could not be loaded from {uri}\n" \
                    "Check your Spatialite file."
            raise QgsProcessingException(f"Incorrect input Spatialite file:\n{err}")
        try:
            set_feat = next(settings_lyr.getFeatures())
        except StopIteration:
            err = f"No global settings entries in {uri}" \
                  "Check your Spatialite file."
            raise QgsProcessingException(f"Incorrect input Spatialite file:\n{err}")
        set_dem_rel_path = set_feat["dem_file"]
        input_slite_dir = os.path.dirname(input_slite)
        set_dem_path = os.path.join(input_slite_dir, set_dem_rel_path)
        feedback.pushInfo(f"DEM raster referenced in Spatialite settings:\n{set_dem_path}")
        if not same_path(set_dem_path, input_dem):
            warn = f"Warning! Selected DEM is different from the DEM referenced in the Spatialite settings."
            if not allow_diff_dem:
                raise QgsProcessingException(warn)
            else:
                feedback.reportError(warn)

        output = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        if output is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT))

        s = QgsSettings()
        s.setValue("threedi-results-analysis/generate_computational_grid/last_input_sqlite", input_slite)
        s.setValue("threedi-results-analysis/generate_computational_grid/last_input_dem", input_dem)
        s.setValue("threedi-results-analysis/generate_computational_grid/last_output", output)

        def progress_rep(progress, info):
            feedback.setProgress(int(progress * 100))
            feedback.pushInfo(info)

        # make_gridadmin(input_slite, input_dem, output, progress_callback=progress_rep)
        try:
            make_gridadmin(input_slite, input_dem, output, progress_callback=progress_rep)
        except SchematisationError as e:
            err = f"Creating grid file failed with the following error: {repr(e)}"
            raise QgsProcessingException(err)

        return {self.OUTPUT: output}
