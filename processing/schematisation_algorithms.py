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
import shutil

# from hydxlib.scripts import run_import_export
# from hydxlib.scripts import write_logging_to_file
# from pathlib import Path
from sqlalchemy.exc import OperationalError, DatabaseError
# from threedi_results_analysis.processing.deps.sufhyd.import_sufhyd_main import Importer
# from threedi_results_analysis.processing.deps.guess_indicator import guess_indicators_utils

from threedi_schema import ThreediDatabase
# from threedi_modelchecker import ThreediModelChecker
from threedi_schema import errors
# from threedi_results_analysis.processing.download_hydx import download_hydx

from threedi_results_analysis.utils.utils import backup_sqlite
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingAlgorithm,
    # QgsProcessingException,
    QgsProcessingParameterFile,
    # QgsProcessingParameterFolderDestination,
    # QgsProcessingParameterString,
)


def get_threedi_database(filename, feedback):
    try:
        threedi_db = ThreediDatabase(filename)
        threedi_db.check_connection()
        return threedi_db
    except (OperationalError, DatabaseError):
        feedback.pushWarning("Invalid spatialite file")
        return None


class MigrateAlgorithm(QgsProcessingAlgorithm):
    """
    Migrate 3Di model schema to the current version
    """

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT, self.tr("3Di Spatialite"), extension="sqlite"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        filename = self.parameterAsFile(parameters, self.INPUT, context)
        threedi_db = get_threedi_database(filename=filename, feedback=feedback)
        if not threedi_db:
            return {self.OUTPUT: None}
        schema = threedi_db.schema
        try:
            schema.validate_schema()
            schema.set_spatial_indexes()
        except errors.MigrationMissingError:
            backup_filepath = backup_sqlite(filename)
            schema.upgrade(backup=False, upgrade_spatialite_version=True)
            schema.set_spatial_indexes()
            shutil.rmtree(os.path.dirname(backup_filepath))
        except errors.UpgradeFailedError:
            feedback.pushWarning(
                "The spatialite database schema cannot be migrated to the current version. Please contact the service desk for assistance."
            )
            return {self.OUTPUT: None}
        success = True
        return {self.OUTPUT: success}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "migrate"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Migrate Spatialite")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "Schematisation"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return MigrateAlgorithm()
