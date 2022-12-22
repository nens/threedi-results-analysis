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

from hydxlib.scripts import run_import_export
from hydxlib.scripts import write_logging_to_file
from pathlib import Path
from sqlalchemy.exc import OperationalError, DatabaseError
from threedi_modelchecker.threedi_database import ThreediDatabase
from threedi_modelchecker.threedi_model.models import GlobalSetting
from threedi_modelchecker.model_checks import ThreediModelChecker
from threedi_modelchecker.schema import ModelSchema
from threedi_modelchecker import errors
from ThreeDiToolbox.processing.download_hydx import download_hydx
from ThreeDiToolbox.tool_commands.raster_checker.raster_checker_main import (
    RasterChecker,
)
from ThreeDiToolbox.utils.utils import backup_sqlite
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterString,
    QgsVectorLayer,
    QgsWkbTypes,
)


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
        schema = ModelSchema(threedi_db)
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
                "There are errors in the spatialite. Please re-open this file in QGIS 3.16, run the model checker and "
                "fix error messages. Then attempt to upgrade again. For questions please contact the servicedesk."
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
                self.INPUT, self.tr("3Di Spatialite"), extension="sqlite"
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
        schema = ModelSchema(threedi_db)
        schema.set_spatial_indexes()
        generated_output_file_path = self.parameterAsFileOutput(
            parameters, self.OUTPUT, context
        )
        self.output_file_path = f"{os.path.splitext(generated_output_file_path)[0]}.csv"
        session = model_checker.db.get_session()
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


class CheckRastersAlgorithm(QgsProcessingAlgorithm):
    """
    Run the raster checker
    """

    INPUT = "INPUT"
    OUTPUT_CSV = "OUTPUT_CSV"
    OUTPUT_POINTS = "OUTPUT_POINTS"
    ADD_TO_PROJECT = "ADD_TO_PROJECT"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT, self.tr("3Di Spatialite"), extension="sqlite"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_CSV, self.tr("CSV Output"), fileFilter="csv"
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_POINTS, self.tr("3Di raster errors - wrong pixels")
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
            return {self.OUTPUT_CSV: None}
        try:
            schema = ModelSchema(threedi_db)
            schema.validate_schema()
            schema.set_spatial_indexes()
            checker = RasterChecker(threedi_db)
            checker.run_all_checks(feedback=feedback)
            checker.close_session()

        except errors.MigrationMissingError:
            feedback.pushWarning(
                "The selected 3Di model does not have the latest migration. Please "
                "migrate your model to the latest version."
            )
            return {self.OUTPUT_CSV: None}

        generated_output_file_path = self.parameterAsFileOutput(
            parameters, self.OUTPUT_CSV, context
        )
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
                    if list_row[0] in ["warning", "error"]:
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
            crs=QgsCoordinateReferenceSystem.fromEpsgId(epsg_code),
        )
        for feat in wrong_pixels:
            point_sink.addFeature(feat)

        return {
            self.OUTPUT_CSV: self.output_file_path,
            self.OUTPUT_POINTS: point_sink_dest_id,
        }

    def postProcessAlgorithm(self, context, feedback):
        if self.add_to_project:
            if self.output_file_path:
                result_layer = QgsVectorLayer(
                    self.output_file_path, "3Di raster errors"
                )
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
        return "check_rasters"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Check Rasters")

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
        return CheckRastersAlgorithm()


class ImportHydXAlgorithm(QgsProcessingAlgorithm):
    """
    Import data from GWSW HydX to a 3Di Spatialite
    """

    INPUT_DATASET_NAME = "INPUT_DATASET_NAME"
    HYDX_DOWNLOAD_DIRECTORY = "HYDX_DOWNLOAD_DIRECTORY"
    INPUT_HYDX_DIRECTORY = "INPUT_HYDX_DIRECTORY"
    TARGET_SQLITE = "TARGET_SQLITE"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT_DATASET_NAME, "GWSW Dataset name (online)", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.HYDX_DOWNLOAD_DIRECTORY,
                "Destination directory for HydX dataset download",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_HYDX_DIRECTORY,
                "Directory containing input HydX dataset",
                behavior=QgsProcessingParameterFile.Folder,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.TARGET_SQLITE, "Target 3Di Sqlite", extension="sqlite"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        hydx_dataset_name = self.parameterAsString(
            parameters, self.INPUT_DATASET_NAME, context
        )
        hydx_download_dir = self.parameterAsString(
            parameters, self.HYDX_DOWNLOAD_DIRECTORY, context
        )
        hydx_path = self.parameterAsString(
            parameters, self.INPUT_HYDX_DIRECTORY, context
        )
        out_path = self.parameterAsFile(parameters, self.TARGET_SQLITE, context)
        if not (hydx_dataset_name or hydx_path):
            raise QgsProcessingException(
                "Either 'GWSW Dataset name (online)' or 'Directory containing input HydX dataset' must be filled in!"
            )
        if hydx_dataset_name and hydx_path:
            feedback.pushWarning(
                "Both 'GWSW Dataset name (online)' and 'Directory containing input HydX dataset' are filled in. "
                "'GWSW Dataset name (online)' will be ignored. This dataset will not be downloaded."
            )
        elif hydx_dataset_name:
            try:
                hydx_download_path = Path(hydx_download_dir)
                hydx_download_dir_is_valid = hydx_download_path.is_dir()
            except TypeError:
                hydx_download_dir_is_valid = False
            if not hydx_download_dir_is_valid:
                raise QgsProcessingException(
                    f"'Destination directory for HydX dataset download' ({hydx_download_path}) is not a valid directory"
                )
            hydx_path = download_hydx(
                dataset_name=hydx_dataset_name,
                target_directory=hydx_download_path,
                wait_times=[0.1, 1, 2, 3, 4, 5, 10],
                feedback=feedback,
            )
            # hydx_path will be None if user has canceled the process during download
            if feedback.isCanceled():
                raise QgsProcessingException("Process canceled")
        threedi_db = get_threedi_database(filename=out_path, feedback=feedback)
        if not threedi_db:
            raise QgsProcessingException(
                f"Unable to connect to 3Di spatialite '{out_path}'"
            )
        try:
            schema = ModelSchema(threedi_db)
            schema.validate_schema()

        except errors.MigrationMissingError:
            raise QgsProcessingException(
                "The selected 3Di spatialite does not have the latest database schema version. Please migrate this "
                "spatialite and try again: Processing > Toolbox > 3Di > Schematisation > Migrate spatialite"
            )
        feedback.pushInfo(f"Starting import of {hydx_path} to {out_path}")
        log_path = Path(out_path).parent / "import_hydx.log"
        write_logging_to_file(log_path)
        feedback.pushInfo(f"Logging will be written to {log_path}")
        run_import_export(export_type="threedi", hydx_path=hydx_path, out_path=out_path)
        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "import_hydx"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Import GWSW HydX")

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
        return ImportHydXAlgorithm()
