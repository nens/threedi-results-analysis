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
import warnings

from pathlib import Path

from hydxlib.scripts import run_import_export
from hydxlib.scripts import write_logging_to_file

from osgeo import ogr, osr
from osgeo import gdal
from qgis.core import Qgis
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingException
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsProcessingParameterFolderDestination
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QCoreApplication
from shapely import wkb  # Import Shapely wkb for geometry handling
from sqlalchemy.exc import DatabaseError
from sqlalchemy.exc import OperationalError

from threedi_modelchecker import ThreediModelChecker
from threedi_modelchecker.exporters import export_with_geom
from threedi_results_analysis.processing.download_hydx import download_hydx
from threedi_results_analysis.utils.utils import backup_sqlite
from threedi_schema import errors
from threedi_schema import ThreediDatabase

STYLE_DIR = Path(__file__).parent / "styles"


def get_threedi_database(filename, feedback):
    try:
        threedi_db = ThreediDatabase(filename)
        threedi_db.check_connection()
        return threedi_db
    except (OperationalError, DatabaseError):
        feedback.pushWarning("Invalid schematisation file")
        return None


def feedback_callback_factory(feedback):
    """Callback function to track schematisation migration progress."""

    def feedback_callback(progres_value, message):
        feedback.setProgress(progres_value)
        feedback.setProgressText(message)

    return feedback_callback


class MigrateAlgorithm(QgsProcessingAlgorithm):
    """
    Migrate 3Di model schema to the current version
    """

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                "3Di schematisation database",
                fileFilter="3Di schematisation database (*.gpkg *.sqlite)"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        filename = self.parameterAsFile(parameters, self.INPUT, context)
        threedi_db = get_threedi_database(filename=filename, feedback=feedback)
        if not threedi_db:
            return {self.OUTPUT: None}
        schema = threedi_db.schema

        # Check whether is it not an intermediate legacy geopackage created by
        # the schematisation editor
        if filename.endswith(".gpkg"):
            if schema.get_version() < 300:
                warn_msg = "The selected file is not a valid 3Di schematisation database.\n\nYou may have selected a geopackage that was created by an older version of the 3Di Schematisation Editor (before version 2.0). In that case, there will probably be a Spatialite (*.sqlite) in the same folder. Please use that file instead."
                feedback.pushWarning(warn_msg)
                return {self.OUTPUT: None}

        try:
            schema.validate_schema()
            schema.set_spatial_indexes()
        except errors.MigrationMissingError:
            backup_filepath = backup_sqlite(filename)

            srid, _ = schema._get_epsg_data()
            if srid is None:
                try:
                    srid = schema._get_dem_epsg()
                except errors.InvalidSRIDException:
                    srid = None
            if srid is None:
                feedback.pushWarning(
                    "Could not fetch valid EPSG code from database or DEM; aborting database migration."
                )
                return {self.OUTPUT: None}

            try:
                feedback_callback = feedback_callback_factory(feedback)
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always", UserWarning)
                    schema.upgrade(backup=False, epsg_code_override=srid, progress_func=feedback_callback)
                if w:
                    for warning in w:
                        feedback.pushWarning(f'{warning._category_name}: {warning.message}')
                schema.set_spatial_indexes()
                shutil.rmtree(os.path.dirname(backup_filepath))
            except errors.UpgradeFailedError:
                feedback.pushWarning(
                    "The schematisation database cannot be migrated to the current version. Please contact the service desk for assistance."
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
        return self.tr("Migrate schematisation database")

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
                self.INPUT, self.tr("3Di Schematisation"), fileFilter="GeoPackage (*.gpkg)"
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
        feedback.setProgress(0)
        self.add_to_project = self.parameterAsBoolean(
            parameters, self.ADD_TO_PROJECT, context
        )
        feedback.pushInfo("Loading schematisation...")
        self.output_file_path = None
        input_filename = self.parameterAsFile(parameters, self.INPUT, context)
        self.schema_name = Path(input_filename).stem
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
        srid, _ = schema._get_epsg_data()
        generated_output_file_path = self.parameterAsFileOutput(
            parameters, self.OUTPUT, context
        )
        self.output_file_path = f"{os.path.splitext(generated_output_file_path)[0]}.gpkg"
        session = model_checker.db.get_session()
        session.model_checker_context = model_checker.context
        total_checks = len(model_checker.config.checks)
        progress_per_check = 80.0 / total_checks
        checks_passed = 0
        error_list = []
        feedback.pushInfo("Checking schematisation...")
        for i, check in enumerate(model_checker.checks(level="info")):
            model_errors = check.get_invalid(session)
            error_list += [[check, error_row] for error_row in model_errors]
            checks_passed += 1
            feedback.setProgress(int(checks_passed * progress_per_check))
        error_details = export_with_geom(error_list)

        # Create an output GeoPackage
        feedback.pushInfo("Writing checker results to geopackage...")
        gdal.UseExceptions()
        driver = ogr.GetDriverByName("GPKG")
        data_source = driver.CreateDataSource(self.output_file_path)
        if data_source is None:
            feedback.pushWarning(
                f"Unable to create the GeoPackage '{self.output_file_path}', check the directory permissions."
            )
            return {self.OUTPUT: None}

        # Loop through the error_details and group by geometry type
        grouped_errors = {'Point': [], 'LineString': [], 'Polygon': [], 'Table': []}
        for error in error_details:
            geom = wkb.loads(error.geom.data) if error.geom is not None else None
            if geom is None or geom.geom_type not in grouped_errors.keys():
                feature_type = 'Table'
            else:
                feature_type = geom.geom_type
            grouped_errors[feature_type].append(error)
        group_name_map = {'LineString': 'Line'}
        for i, (feature_type, errors_group) in enumerate(grouped_errors.items()):
            group_name = f'{group_name_map.get(feature_type, feature_type)} features'
            feedback.pushInfo(f"Adding layer '{group_name}' to geopackage...")
            feedback.setProgress(85+5*i)
            if feature_type == 'Table':
                # Create a table for non-geometry errors
                layer = data_source.CreateLayer(
                    group_name, None, ogr.wkbNone, options=["OVERWRITE=YES"]
                )
            else:
                # Create a layer for each type of geometry
                spatial_ref = osr.SpatialReference()
                spatial_ref.ImportFromEPSG(srid)
                layer = data_source.CreateLayer(
                    group_name,
                    srs=spatial_ref,
                    geom_type=getattr(ogr, f"wkb{feature_type}"),
                    options=["OVERWRITE=YES"],
                    )

            # Add fields
            layer.CreateField(ogr.FieldDefn("level", ogr.OFTString))
            layer.CreateField(ogr.FieldDefn("error_code", ogr.OFTString))
            layer.CreateField(ogr.FieldDefn("id", ogr.OFTString))
            layer.CreateField(ogr.FieldDefn("table", ogr.OFTString))
            layer.CreateField(ogr.FieldDefn("column", ogr.OFTString))
            layer.CreateField(ogr.FieldDefn("value", ogr.OFTString))
            layer.CreateField(ogr.FieldDefn("description", ogr.OFTString))

            defn = layer.GetLayerDefn()
            for error in errors_group:
                feat = ogr.Feature(defn)
                feat.SetField("level", error.name)
                feat.SetField("error_code", error.code)
                feat.SetField("id", error.id)
                feat.SetField("table", error.table)
                feat.SetField("column", error.column)
                feat.SetField("value", error.value)
                feat.SetField("description", error.description)
                if feature_type != 'Table':
                    geom = wkb.loads(error.geom.data)  # Convert WKB to a Shapely geometry object
                    feat.SetGeometry(ogr.CreateGeometryFromWkb(geom.wkb))  # Convert back to OGR-compatible WKB
                layer.CreateFeature(feat)
        feedback.pushInfo(f"GeoPackage successfully written to file")
        return {self.OUTPUT: self.output_file_path}

    def postProcessAlgorithm(self, context, feedback):
        if self.add_to_project and self.output_file_path:
            feedback.pushInfo("Adding results to project...")
            # Create a group for the GeoPackage layers
            group = QgsProject.instance().layerTreeRoot().insertGroup(0, f'Check results: {self.schema_name}')
            # Add all layers in the geopackage to the group
            conn = ogr.Open(self.output_file_path)
            if conn:
                for i in range(conn.GetLayerCount()):
                    layer_name = conn.GetLayerByIndex(i).GetName()
                    layer_uri = f"{self.output_file_path}|layername={layer_name}"
                    layer = QgsVectorLayer(layer_uri, layer_name.replace('errors_', '', 1), "ogr")
                    if layer.isValid():
                        added_layer = QgsProject.instance().addMapLayer(layer, False)
                        if added_layer.geometryType() in [
                            Qgis.GeometryType.Point,
                            Qgis.GeometryType.Line,
                            Qgis.GeometryType.Polygon,
                        ]:
                            added_layer.loadNamedStyle(
                                str(STYLE_DIR / f"checker_{added_layer.geometryType().name.lower()}.qml")
                            )
                        group.addLayer(added_layer)
                    else:
                        feedback.reportError(f"Layer {layer_name} is not valid")
                conn = None  # Close the connection
            else:
                feedback.reportError(f"Could not open GeoPackage file: {self.output_file_path}")
            feedback.pushInfo(f"Added results to layer 'Check results: {self.schema_name}'")
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


class ImportHydXAlgorithm(QgsProcessingAlgorithm):
    """
    Import data from GWSW HydX to a 3Di Schematisation
    """

    INPUT_DATASET_NAME = "INPUT_DATASET_NAME"
    HYDX_DOWNLOAD_DIRECTORY = "HYDX_DOWNLOAD_DIRECTORY"
    INPUT_HYDX_DIRECTORY = "INPUT_HYDX_DIRECTORY"
    TARGET_SCHEMATISATION = "TARGET_SCHEMATISATION"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFile(
                self.TARGET_SCHEMATISATION, "Target 3Di Schematisation", fileFilter="GeoPackage (*.gpkg)"
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_HYDX_DIRECTORY,
                "GWSW HydX directory (local)",
                behavior=QgsProcessingParameterFile.Folder,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT_DATASET_NAME, "GWSW dataset name (online)", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.HYDX_DOWNLOAD_DIRECTORY,
                "Destination directory for GWSW HydX dataset download",
                optional=True,
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
        out_path = self.parameterAsFile(parameters, self.TARGET_SCHEMATISATION, context)
        threedi_db = get_threedi_database(filename=out_path, feedback=feedback)
        if not threedi_db:
            raise QgsProcessingException(
                f"Unable to connect to 3Di schematisation '{out_path}'"
            )
        try:
            schema = threedi_db.schema
            schema.validate_schema()

        except errors.MigrationMissingError:
            raise QgsProcessingException(
                "The selected 3Di schematisation does not have the latest database schema version. Please migrate this "
                "schematisation and try again: Processing > Toolbox > 3Di > Schematisation > Migrate schematisation database"
            )
        if not (hydx_dataset_name or hydx_path):
            raise QgsProcessingException(
                "Either 'GWSW HydX directory (local)' or 'GWSW dataset name (online)' must be filled in!"
            )
        if hydx_dataset_name and hydx_path:
            feedback.pushWarning(
                "Both 'GWSW dataset name (online)' and 'GWSW HydX directory (local)' are filled in. "
                "'GWSW dataset name (online)' will be ignored. This dataset will not be downloaded."
            )
        elif hydx_dataset_name:
            try:
                hydx_download_path = Path(hydx_download_dir)
                hydx_download_dir_is_valid = hydx_download_path.is_dir()
            except TypeError:
                hydx_download_dir_is_valid = False
            if parameters[self.HYDX_DOWNLOAD_DIRECTORY] == "TEMPORARY_OUTPUT":
                hydx_download_dir_is_valid = True
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
            if hydx_path is None:
                raise QgsProcessingException("Error in retrieving dataset (note case-sensitivity)")
        feedback.pushInfo(f"Starting import of {hydx_path} to {out_path}")
        log_path = Path(out_path).parent / "import_hydx.log"
        write_logging_to_file(log_path)
        feedback.pushInfo(f"Logging will be written to {log_path}")
        run_import_export(hydx_path=hydx_path, out_path=out_path)
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

    def shortHelpString(self):
        return """
        <h3>Introduction</h3>
        <p>Use this processing algorithm to import data in the format of the Dutch "Gegevenswoordenboek Stedelijk Water (GWSW)". Either select a previously downloaded local dataset, or download a dataset directly from the server.</p>
        <p>A log file will be created in the same directory as the Target 3Di schematisation. Please check this log file after the import has completed.&nbsp;&nbsp;</p>
        <h3>Parameters</h3>
        <h4>Target 3Di Schematisation</h4>
        <p>GeoPackage (.gpkg) file that contains the layers required by 3Di. Imported data will be added to any data already contained in the 3Di schematisation.</p>
        <h4>GWSW HydX directory (local)</h4>
        <p>Use this option if you have already downloaded a GWSW HydX dataset to a local directory.</p>
        <h4>GWSW dataset name (online)</h4>
        <p>Use this option if you want to download a GWSW HydX dataset.</p>
        <h4>Destination directory for GWSW HydX dataset download</h4>
        <p>If you have chosen to download a GWSW HydX dataset, this is the directory it will be downloaded to.</p>
        """

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
