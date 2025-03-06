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

from pathlib import Path
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QCoreApplication
from sqlalchemy.exc import DatabaseError
from sqlalchemy.exc import OperationalError
from threedi_modelchecker import ThreediModelChecker
from threedi_results_analysis.utils.utils import backup_sqlite
from threedi_schema import errors
from threedi_schema import ThreediDatabase
from threedi_schema.migrations.exceptions import InvalidSRIDException

import csv
import os
import shutil


def get_threedi_database(filename, feedback):
    try:
        threedi_db = ThreediDatabase(Path(filename))
        threedi_db.check_connection()
        return threedi_db
    except (OperationalError, DatabaseError):
        feedback.pushWarning("Invalid schematisation file")
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

            srid, _ = schema._get_epsg_data()
            if srid is None:
                try:
                    srid = schema._get_dem_epsg()
                except InvalidSRIDException:
                    srid = None
            if srid is None:
                feedback.pushWarning(
                    "Could not fetch valid EPSG code from database or DEM; aborting database migration."
                )
                return {self.OUTPUT: None}

            try:
                schema.upgrade(backup=False, upgrade_spatialite_version=True, epsg_code_override=srid)
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


class CheckSchematisationAlgorithm(QgsProcessingAlgorithm):
    """
    Run the schematisation checker
    """

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    ADD_TO_PROJECT = "ADD_TO_PROJECT"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT, self.tr("3Di Schematisation"), fileFilter="Spatialite (*.sqlite);;GeoPackage (*.gpkg)"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT, self.tr("Output"), fileFilter="csv"
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ADD_TO_PROJECT, self.tr("Add result to project"), defaultValue=True
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        self.add_to_project = self.parameterAsBoolean(
            parameters, self.ADD_TO_PROJECT, context
        )
        self.output_file_path = None
        input_filename = self.parameterAsFile(parameters, self.INPUT, context)
        threedi_db = get_threedi_database(filename=input_filename, feedback=feedback)
        if not threedi_db:
            return {self.OUTPUT: None}
        try:
            model_checker = ThreediModelChecker(threedi_db)
        except errors.MigrationMissingError:
            feedback.pushWarning(
                "The selected 3Di model does not have the latest migration. Please "
                "migrate your model to the latest version."
            )
            return {self.OUTPUT: None}
        schema = threedi_db.schema
        schema.set_spatial_indexes()
        generated_output_file_path = self.parameterAsFileOutput(
            parameters, self.OUTPUT, context
        )
        self.output_file_path = f"{os.path.splitext(generated_output_file_path)[0]}.csv"
        session = model_checker.db.get_session()
        session.model_checker_context = model_checker.context
        total_checks = len(model_checker.config.checks)
        progress_per_check = 100.0 / total_checks
        checks_passed = 0
        try:
            with open(self.output_file_path, "w", newline="") as output_file:
                writer = csv.writer(output_file)
                writer.writerow(
                    [
                        "level",
                        "error_code",
                        "id",
                        "table",
                        "column",
                        "value",
                        "description",
                    ]
                )
                for i, check in enumerate(model_checker.checks(level="info")):
                    model_errors = check.get_invalid(session)
                    for error_row in model_errors:
                        writer.writerow(
                            [
                                check.level.name,
                                check.error_code,
                                error_row.id,
                                check.table.name,
                                check.column.name,
                                getattr(error_row, check.column.name),
                                check.description(),
                            ]
                        )
                    checks_passed += 1
                    feedback.setProgress(int(checks_passed * progress_per_check))
        except PermissionError:
            # PermissionError happens for example when a user has the file already open
            # with Excel on Windows, which locks the file.
            feedback.pushWarning(
                f"Not enough permissions to write the file '{self.output_file_path}'.\n\n"
                "The file may be used by another program. Please close all "
                "other programs using the file or select another output "
                "file."
            )
            return {self.OUTPUT: None}

        return {self.OUTPUT: self.output_file_path}

    def postProcessAlgorithm(self, context, feedback):
        if self.add_to_project:
            if self.output_file_path:
                result_layer = QgsVectorLayer(
                    self.output_file_path, "3Di schematisation errors"
                )
                QgsProject.instance().addMapLayer(result_layer)
        return {self.OUTPUT: self.output_file_path}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "check_schematisation"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Check Schematisation")

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
        return CheckSchematisationAlgorithm()
