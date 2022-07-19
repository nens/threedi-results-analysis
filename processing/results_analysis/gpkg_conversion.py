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
from ThreeDiToolbox.utils.utils import safe_join
from threedigrid.admin.exporters.geopackage import GeopackageExporter


class Progress(object):
    def __init__(self, feedback):
        self.percentage = 0
        self.feedback = feedback

    def update(self, count, total):
        if (count * 100) // total > self.percentage:
            self.percentage = (count * 100) // total
            self.feedback.setProgress(int(self.percentage))


class ThreeDiConvertToGpkgAlgorithm(QgsProcessingAlgorithm):
    """Convert gridadmin.h5 to GeoPackage with vector layers and add subset of those layers to the map canvas."""

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    GPKG_NAME = "GPKG_NAME"
    LAYERS_TO_ADD = OrderedDict()

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return ThreeDiConvertToGpkgAlgorithm()

    def name(self):
        return "threedi_convert_gridadmin_to_gpkg"

    def displayName(self):
        return self.tr("Convert gridadmin to GeoPackage")

    def group(self):
        return self.tr("Computational Grid")

    def groupId(self):
        return "computational_grid"

    def shortHelpString(self):
        return self.tr("Convert gridadmin.h5 to GeoPackage")

    def initAlgorithm(self, config=None):
        s = QgsSettings()
        last_input_dir = s.value("threedi-results-analysis/gridadmin_to_gpkg/last_input", None)
        last_output_gpkg = s.value("threedi-results-analysis/gridadmin_to_gpkg/last_output_gpkg", None)

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr("Folder containing input gridadmin.h5"),
                behavior=QgsProcessingParameterFile.Folder,
                defaultValue=last_input_dir,
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT, self.tr("Output GeoPackage file"), fileFilter="*.gpkg", defaultValue=last_output_gpkg
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        gridadmin_folder = self.parameterAsString(parameters, self.INPUT, context)
        if gridadmin_folder is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        input_gridadmin = os.path.join(gridadmin_folder, "gridadmin.h5")

        gpkg_path = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        if gpkg_path is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT))
        if gpkg_path.endswith(".file"):
            gpkg_path = gpkg_path.rsplit(".", 1)[0] + ".gpkg"

        s = QgsSettings()
        s.setValue("threedi-results-analysis/gridadmin_to_gpkg/last_input", gridadmin_folder)
        s.setValue("threedi-results-analysis/gridadmin_to_gpkg/last_output_gpkg", gpkg_path)
        plugin_dir = os.path.dirname(os.path.realpath(__file__))
        styles_dir = os.path.join(plugin_dir, "styles")

        progress = Progress(feedback)
        exporter = GeopackageExporter(input_gridadmin, gpkg_path)
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
            uri = gpkg_path + f"|layername={table_name}"
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
            crs_info = f"Skipping setting project CRS - the source file {input_gridadmin} EPSG codes are inconsistent."
        feedback.pushInfo(crs_info)

        return {}

    def postProcessAlgorithm(self, context, feedback):
        project = context.project()
        root = project.instance().layerTreeRoot()
        group = root.addGroup("Computational grid")
        for index, (layer_name, layer) in enumerate(self.LAYERS_TO_ADD.items()):
            project.addMapLayer(layer, False)
            group.insertLayer(int(index), layer)
        self.LAYERS_TO_ADD.clear()
        return {}
