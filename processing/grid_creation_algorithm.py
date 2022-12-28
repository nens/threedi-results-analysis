import os
from collections import OrderedDict
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsSettings,
    QgsVectorLayer,
)
from threedigrid_builder import make_gridadmin, SchematisationError
from ThreeDiToolbox.processing.utils import gridadmin2geopackage, load_computational_layers


class ThreeDiGenerateCompGridAlgorithm(QgsProcessingAlgorithm):
    """
    Generate a gridadmin.h5 file out of Spatialite database and convert it to GeoPackage.
    Created layers will be added to the map canvas after successful conversion.
    """

    INPUT_SPATIALITE = "INPUT_SPATIALITE"
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

        s = QgsSettings()
        last_input_sqlite = s.value("threedi-results-analysis/generate_computational_grid/last_input_sqlite", None)
        last_output = s.value("threedi-results-analysis/generate_computational_grid/last_output", None)

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_SPATIALITE,
                self.tr("Input SpatiaLite file"),
                behavior=QgsProcessingParameterFile.File,
                defaultValue=last_input_sqlite,
                extension="sqlite",
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT, self.tr("Output computational grid file"), fileFilter="*.gpkg", defaultValue=last_output
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_spatialite = self.parameterAsString(parameters, self.INPUT_SPATIALITE, context)
        if not input_spatialite:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_SPATIALITE))

        uri = input_spatialite + "|layername=v2_global_settings"
        feedback.pushInfo(f"Reading DEM settings from: {uri}")
        settings_lyr = QgsVectorLayer(uri, "glob_settings", "ogr")
        if not settings_lyr.isValid():
            err = f"Global Spatialite settings table could not be loaded from {uri}\n" "Check your Spatialite file."
            raise QgsProcessingException(f"Incorrect input Spatialite file:\n{err}")
        try:
            settings_feat = next(settings_lyr.getFeatures())
        except StopIteration:
            err = f"No global settings entries in {uri}" "Check your Spatialite file."
            raise QgsProcessingException(f"Incorrect input Spatialite file:\n{err}")
        set_dem_rel_path = settings_feat["dem_file"]
        if set_dem_rel_path:
            input_spatialite_dir = os.path.dirname(input_spatialite)
            set_dem_path = os.path.join(input_spatialite_dir, set_dem_rel_path)
            feedback.pushInfo(f"DEM raster referenced in Spatialite settings:\n{set_dem_path}")
            if not os.path.exists(set_dem_path):
                set_dem_path = None
                info = "The DEM referenced in the Spatialite settings doesn't exist - skipping."
                feedback.pushInfo(info)
        else:
            set_dem_path = None
            info = "There is no DEM file referenced in the Spatialite settings - skipping."
            feedback.pushInfo(info)
        output_gpkg_file = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        if output_gpkg_file is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT))
        # If user is writing to the temporary file then QGIS adds '.file' extension, so we need to change it.
        output_file_without_extension = output_gpkg_file.rsplit(".", 1)[0]
        gridadmin_file = f"{output_file_without_extension}.h5"
        if output_gpkg_file.endswith(".file"):
            output_gpkg_file = f"{output_file_without_extension}.gpkg"

        s = QgsSettings()
        s.setValue("threedi-results-analysis/generate_computational_grid/last_input_sqlite", input_spatialite)
        s.setValue("threedi-results-analysis/generate_computational_grid/last_output", output_gpkg_file)

        def progress_rep(progress, info):
            feedback.setProgress(int(progress * 100))
            feedback.pushInfo(info)

        try:
            make_gridadmin(input_spatialite, set_dem_path, gridadmin_file, progress_callback=progress_rep)
        except SchematisationError as e:
            err = f"Creating grid file failed with the following error: {repr(e)}"
            raise QgsProcessingException(err)

        feedback.setProgress(0)
        gpkg_layers = gridadmin2geopackage(gridadmin_file, output_gpkg_file, context, feedback)
        self.LAYERS_TO_ADD.update(gpkg_layers)

        return {self.OUTPUT: output_gpkg_file}

    def postProcessAlgorithm(self, context, feedback):
        project = context.project()
        load_computational_layers(self.LAYERS_TO_ADD, project)
        self.LAYERS_TO_ADD.clear()
        return {}
