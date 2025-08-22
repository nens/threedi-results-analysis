from collections import OrderedDict
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingException
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QCoreApplication
from threedi_results_analysis.processing.processing_utils import gridadmin2geopackage
from threedi_results_analysis.processing.processing_utils import (
    load_computational_layers,
)
from threedigrid_builder import make_gridadmin

import io
import logging
import os


class ThreeDiGenerateCompGridAlgorithm(QgsProcessingAlgorithm):
    """
    Generate a gridadmin.h5 file out of schematisation database and convert it to GeoPackage.
    Created layers will be added to the map canvas after successful conversion.
    """

    INPUT_SCHEMATISATION = "INPUT_SCHEMATISATION"
    OUTPUT = "OUTPUT"
    LAYERS_TO_ADD = OrderedDict()

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return ThreeDiGenerateCompGridAlgorithm()

    def name(self):
        return "threedi_generate_computational_grid"

    def displayName(self):
        return self.tr("Computational grid from schematisation")

    def group(self):
        return self.tr("Computational Grid")

    def groupId(self):
        return "computational_grid"

    def shortHelpString(self):
        return self.tr("Generate computational grid from schematization")

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_SCHEMATISATION,
                self.tr("Input schematisation file"),
                behavior=QgsProcessingParameterFile.File,
                fileFilter="GeoPackage (*.gpkg);;Spatialite (*.sqlite)",
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT, self.tr("Output computational grid file"), fileFilter="*.gpkg",
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_schematisation = self.parameterAsString(parameters, self.INPUT_SCHEMATISATION, context)
        if not input_schematisation:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_SCHEMATISATION))

        set_dem_rel_path = self._get_rel_dem_path(input_schematisation, feedback)
        if set_dem_rel_path:
            input_schematisation_dir = os.path.dirname(input_schematisation)
            set_dem_path = os.path.join(input_schematisation_dir, set_dem_rel_path)
            feedback.pushInfo(f"DEM raster referenced in schematisation settings:\n{set_dem_path}")
            if not os.path.exists(set_dem_path):
                set_dem_path = None
                info = "The DEM referenced in the schematisation settings doesn't exist - skipping."
                feedback.pushInfo(info)
        else:
            set_dem_path = None
            info = "There is no DEM file referenced in the schematisation settings - skipping."
            feedback.pushInfo(info)
        output_gpkg_file = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        if output_gpkg_file is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT))
        # If user is writing to the temporary file then QGIS adds '.file' extension, so we need to change it.
        output_file_without_extension = output_gpkg_file.rsplit(".", 1)[0]
        gridadmin_file = f"{output_file_without_extension}.h5"
        if output_gpkg_file.endswith(".file"):
            output_gpkg_file = f"{output_file_without_extension}.gpkg"

        def progress_rep(progress, info):
            feedback.setProgress(int(progress * 100))
            feedback.pushInfo(info)

        # Capture threedigridbuilder logging
        logger = logging.getLogger("threedigrid_builder.grid.connection_nodes")
        assert logger.hasHandlers()  # Check whether we have the right one
        log_capture_string = io.StringIO()
        ch = logging.StreamHandler(log_capture_string)
        ch.setFormatter(logging.Formatter(fmt='%(levelname)-8s :: %(message)s'))
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)
        try:
            make_gridadmin(input_schematisation, set_dem_path, gridadmin_file, progress_callback=progress_rep)
        except Exception as e:
            err = (
                f"Creating grid file failed with the following error: {repr(e)}\n"
                "This error is likely caused by errors in the schematisation.\n"
                "Run the schematisation checker, correct any errors that are reported, and try again."
            )
            raise QgsProcessingException(err)
        finally:
            # Pull the contents back into a string and close the stream
            log_contents = log_capture_string.getvalue()
            log_capture_string.close()
            logger.removeHandler(ch)
            if log_contents:
                feedback.pushWarning("3Di gridbuilder log:")
                feedback.pushWarning(log_contents)

        feedback.setProgress(0)
        gpkg_layers = gridadmin2geopackage(gridadmin_file, output_gpkg_file, context, feedback)
        self.LAYERS_TO_ADD.update(gpkg_layers)

        return {self.OUTPUT: output_gpkg_file}

    def postProcessAlgorithm(self, context, feedback):
        project = context.project()
        load_computational_layers(self.LAYERS_TO_ADD, project)
        self.LAYERS_TO_ADD.clear()
        return {}

    def _get_schematisation_version(self, input_schematisation: str) -> int:
        uri = input_schematisation + "|layername=schema_version"
        schema_lyr = QgsVectorLayer(uri, "schema_version", "ogr")
        if schema_lyr.isValid() and schema_lyr.featureCount() == 1:
            # Take first (and only)
            meta = next(schema_lyr.getFeatures())
            return int(meta["version_num"])
        else:
            return None

    def _get_rel_dem_path(self, input_schematisation: str, feedback) -> str:

        schematisation_version = self._get_schematisation_version(input_schematisation)
        setting_uri = None
        if schematisation_version < 222:
            setting_uri = input_schematisation + "|layername=v2_global_settings"
        else:
            setting_uri = input_schematisation + "|layername=model_settings"

        feedback.pushInfo(f"Reading DEM file from: {setting_uri}")
        settings_lyr = QgsVectorLayer(setting_uri, "settings", "ogr")
        if settings_lyr.isValid() and settings_lyr.featureCount() == 1:
            settings_feat = next(settings_lyr.getFeatures())
            set_dem_rel_path = settings_feat["dem_file"]
        else:
            err = f"No (or multiple) global settings entries in {setting_uri}" "Check your schematisation file."
            raise QgsProcessingException(f"Incorrect input schematisation file:\n{err}")

        if schematisation_version >= 222:
            set_dem_rel_path = os.path.join("rasters", str(set_dem_rel_path))

        return set_dem_rel_path
