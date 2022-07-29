import os
from collections import OrderedDict
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsSettings,
    QgsVectorLayer,
)
from threedigrid_builder import make_gridadmin, SchematisationError
from threedigrid.admin.exporters.geopackage import GeopackageExporter
from ThreeDiToolbox.processing.results_analysis.gpkg_conversion import Progress
from ThreeDiToolbox.utils.utils import safe_join


class ThreeDiGenerateCompGridAlgorithm(QgsProcessingAlgorithm):
    """Generate a gridadmin.h5 file out of Spatialite database and convert it to GeoPackage."""

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
        plugin_dir = os.path.dirname(os.path.realpath(__file__))
        styles_dir = os.path.join(plugin_dir, "styles")

        def progress_rep(progress, info):
            feedback.setProgress(int(progress * 100))
            feedback.pushInfo(info)

        try:
            make_gridadmin(input_spatialite, set_dem_path, gridadmin_file, progress_callback=progress_rep)
        except SchematisationError as e:
            err = f"Creating grid file failed with the following error: {repr(e)}"
            raise QgsProcessingException(err)

        feedback.setProgress(0)
        progress = Progress(feedback)
        exporter = GeopackageExporter(gridadmin_file, output_gpkg_file)
        exporter.export(progress.update)
        feedback.pushInfo("Export done!")

        # Unfortunately, temporaryLayerStore keeps layers to be added as a dictionary, so the order is lost
        data_srcs = OrderedDict(
            [
                ("Obstacle", "obstacle"),
                ("Cell", "cell"),
                ("Pump (point)", "pump"),
                ("Pump (line)", "pump_linestring"),
                ("Node", "node"),
                ("Flowline", "flowline"),
            ]
        )

        layers = dict()
        empty_layers = []
        epsg_codes = set()
        for layer_name, table_name in data_srcs.items():
            uri = output_gpkg_file + f"|layername={table_name}"
            layer = QgsVectorLayer(uri, layer_name, "ogr")
            layers[layer_name] = layer

            # only load layers that contain some features
            if not layers[layer_name].featureCount():
                empty_layers.append(layer_name)
                continue

            # apply the style and add for loading when alg is completed
            qml_path = safe_join(styles_dir, f"{table_name}.qml")
            if os.path.exists(qml_path):
                layer.loadNamedStyle(qml_path)
                layer.saveStyleToDatabase(table_name, "", True, "")
            self.LAYERS_TO_ADD[layer_name] = layer

        # Empty layers info
        if empty_layers:
            empty_info = "\n\nThe following layers contained no feature:\n * " + "\n * ".join(empty_layers) + "\n\n"
            feedback.pushInfo(empty_info)

        # Set project CRS only if all source layers have the same CRS
        if len(epsg_codes) == 1:
            code_int = int(list(epsg_codes)[0])
            crs = QgsCoordinateReferenceSystem.fromEpsgId(code_int)
            if crs.isValid():
                context.project().setCrs(crs)
                crs_info = "Setting project CRS according to the source gridadmin file."
            else:
                crs_info = "Skipping setting project CRS - does gridadmin file contains a valid EPSG code?"
        else:
            crs_info = f"Skipping setting project CRS - the source file {gridadmin_file} EPSG codes are inconsistent."
        feedback.pushInfo(crs_info)

        return {self.OUTPUT: output_gpkg_file}

    def postProcessAlgorithm(self, context, feedback):
        project = context.project()
        root = project.instance().layerTreeRoot()
        group = root.addGroup("Computational grid")
        for index, (layer_name, layer) in enumerate(self.LAYERS_TO_ADD.items()):
            project.addMapLayer(layer, False)
            group.insertLayer(int(index), layer)
        self.LAYERS_TO_ADD.clear()
        return {}
