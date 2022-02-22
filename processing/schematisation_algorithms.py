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

import csv
import os
import shutil
from uuid import uuid4

from sqlalchemy.exc import OperationalError, DatabaseError
from threedi_modelchecker.threedi_database import ThreediDatabase
from threedi_modelchecker.threedi_model.models import GlobalSetting
from threedi_modelchecker.model_checks import ThreediModelChecker
from threedi_modelchecker.schema import ModelSchema
from threedi_modelchecker import errors
from ThreeDiToolbox.tool_commands.raster_checker.raster_checker_main import RasterChecker
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsProcessingAlgorithm,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsVectorLayer,
    QgsWkbTypes
)


def backup_sqlite(filename):
    """Make a backup of the sqlite database."""
    backup_folder = os.path.join(os.path.dirname(os.path.dirname(filename)), "_backup")
    os.makedirs(backup_folder, exist_ok=True)
    prefix = str(uuid4())[:8]
    backup_sqlite_path = os.path.join(backup_folder, f"{prefix}_{os.path.basename(filename)}")
    shutil.copyfile(filename, backup_sqlite_path)
    return backup_sqlite_path


def get_threedi_database(filename, feedback):
    try:
        db_type = "spatialite"
        db_settings = {"db_path": filename}
        threedi_db = ThreediDatabase(db_settings, db_type=db_type)
        threedi_db.check_connection()
        return threedi_db
    except (OperationalError, DatabaseError):
        feedback.pushWarning("Invalid spatialite file")
        return None


class MigrateAlgorithm(QgsProcessingAlgorithm):
    """
    Migrate 3Di model schema to the current version
    """
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr('3Di Spatialite'),
                extension="sqlite"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        filename = self.parameterAsFile(parameters, self.INPUT, context)
        threedi_db = get_threedi_database(filename=filename, feedback=feedback)
        if not threedi_db:
            return {self.OUTPUT: None}
        schema = ModelSchema(threedi_db)
        try:
            schema.validate_schema()
        except errors.MigrationMissingError:
            backup_filepath = backup_sqlite(filename)
            schema.upgrade(backup=False)
            shutil.rmtree(os.path.dirname(backup_filepath))
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
        return 'migrate'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Migrate Spatialite')

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
        return 'Schematisation'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return MigrateAlgorithm()


class CheckSchematisationAlgorithm(QgsProcessingAlgorithm):
    """
    Run the schematisation checker
    """
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    ADD_TO_PROJECT = 'ADD_TO_PROJECT'

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr('3Di Spatialite'),
                extension="sqlite"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr('Output'),
                fileFilter="csv"
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ADD_TO_PROJECT,
                self.tr('Add result to project'),
                defaultValue=True
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        self.add_to_project = self.parameterAsBoolean(parameters, self.ADD_TO_PROJECT, context)
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

        generated_output_file_path = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        self.output_file_path = f"{os.path.splitext(generated_output_file_path)[0]}.csv"
        session = model_checker.db.get_session()
        total_checks = len(model_checker.config.checks)
        progress_per_check = 100.0 / total_checks
        checks_passed = 0
        try:
            with open(self.output_file_path, "w", newline="") as output_file:
                writer = csv.writer(output_file)
                writer.writerow(
                    ["level", "error_code", "id", "table", "column", "value", "description"]
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
                result_layer = QgsVectorLayer(self.output_file_path, '3Di schematisation errors')
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
        return 'check_schematisation'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Check Schematisation')

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
        return 'Schematisation'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CheckSchematisationAlgorithm()


class CheckRastersAlgorithm(QgsProcessingAlgorithm):
    """
    Run the raster checker
    """
    INPUT = 'INPUT'
    OUTPUT_CSV = 'OUTPUT_CSV'
    OUTPUT_POINTS = 'OUTPUT_POINTS'
    ADD_TO_PROJECT = 'ADD_TO_PROJECT'

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr('3Di Spatialite'),
                extension="sqlite"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_CSV,
                self.tr('CSV Output'),
                fileFilter="csv"
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_POINTS,
                self.tr('3Di raster errors - wrong pixels')
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ADD_TO_PROJECT,
                self.tr('Add result to project'),
                defaultValue=True
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        self.add_to_project = self.parameterAsBoolean(parameters, self.ADD_TO_PROJECT, context)
        self.output_file_path = None
        input_filename = self.parameterAsFile(parameters, self.INPUT, context)
        threedi_db = get_threedi_database(filename=input_filename, feedback=feedback)
        if not threedi_db:
            return {self.OUTPUT_CSV: None}
        try:
            schema = ModelSchema(threedi_db)
            schema.validate_schema()
            checker = RasterChecker(threedi_db)
            checker.run_all_checks(feedback=feedback)
            checker.close_session()

        except errors.MigrationMissingError:
            feedback.pushWarning(
                "The selected 3Di model does not have the latest migration. Please "
                "migrate your model to the latest version."
            )
            return {self.OUTPUT_CSV: None}

        generated_output_file_path = self.parameterAsFileOutput(parameters, self.OUTPUT_CSV, context)
        self.output_file_path = f"{os.path.splitext(generated_output_file_path)[0]}.csv"
        try:
            with open(self.output_file_path, "w", newline="") as output_file:
                writer = csv.writer(output_file)
                writer.writerow(
                    ["level", "global_settings_id", "error_code", "description"]
                )
                checker.results.sort_results()
                for result_row in checker.results.result_per_check:
                    str_row = checker.results.result_per_check_to_msg(result_row)
                    list_row = str_row.split(",")
                    if list_row[0] in ['warning', 'error']:
                        list_row[0] = list_row[0].upper()
                        writer.writerow(list_row)

        except PermissionError:
            # PermissionError happens for example when a user has the file already open
            # with Excel on Windows, which locks the file.
            feedback.pushWarning(
                f"Not enough permissions to write the file '{self.output_file_path}'.\n\n"
                "The file may be used by another program. Please close all "
                "other programs using the file or select another output "
                "file."
            )
            return {self.OUTPUT_CSV: None}

        wrong_pixels_fields, wrong_pixels = checker.wrong_pixels_as_features()
        session = threedi_db.get_session()
        epsg_code = session.query(GlobalSetting).first().epsg_code
        session.close()
        (point_sink, point_sink_dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT_POINTS,
            context,
            fields=wrong_pixels_fields,
            geometryType=QgsWkbTypes.Point,
            crs=QgsCoordinateReferenceSystem.fromEpsgId(epsg_code)
        )
        for feat in wrong_pixels:
            point_sink.addFeature(feat)

        return {self.OUTPUT_CSV: self.output_file_path, self.OUTPUT_POINTS: point_sink_dest_id}

    def postProcessAlgorithm(self, context, feedback):
        if self.add_to_project:
            if self.output_file_path:
                result_layer = QgsVectorLayer(self.output_file_path, '3Di raster errors')
                QgsProject.instance().addMapLayer(result_layer)
        return {self.OUTPUT_CSV: self.output_file_path}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'check_rasters'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Check Rasters')

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
        return 'Schematisation'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CheckRastersAlgorithm()
