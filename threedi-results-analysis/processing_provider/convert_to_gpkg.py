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
from collections import OrderedDict

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFolderDestination,
    QgsProcessingException,
    QgsProcessingContext,
    QgsProcessingParameterFile,
    QgsSettings,
    QgsVectorLayer,
)
from qgis.utils import iface
from ..user_communication import UserCommunication
from ..utils import safe_join

try:
    from threedigrid.admin.exporters.geopackage import GeopackageExporter
except (ImportError, ModuleNotFoundError):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(this_dir)
    whl_path = os.path.join(parent_dir, "deps", "threedigrid-1.2.3-py2.py3-none-any.whl")
    sys.path.append(whl_path)
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
    """ Convert gridadmin.h5 to GeoPackage with vector layers """

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def flags(self):
        return super().flags()  # | QgsProcessingAlgorithm.FlagNoThreading

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ThreeDiConvertToGpkgAlgorithm()

    def name(self):
        return 'threedi_convert_gridadmin_to_gpkg'

    def displayName(self):
        return self.tr('Convert gridadmin to GeoPackage')

    def group(self):
        return self.tr('')

    def groupId(self):
        return ''

    def shortHelpString(self):
        return self.tr("Convert gridadmin.h5 to GeoPackage")

    def initAlgorithm(self, config=None):

        self.uc = UserCommunication(iface, "3Di Results Analysis")
        s = QgsSettings()
        last_input_dir = s.value("threedi-results-analysis/gridadmin_to_gpkg/last_input", None)
        last_output_gpkg = s.value("threedi-results-analysis/gridadmin_to_gpkg/last_output_gpkg", None)

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr("Input gridadmin.h5 file"),
                behavior=QgsProcessingParameterFile.Folder,
                defaultValue=last_input_dir
            )
        )

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT,
                self.tr("Output folder"),
                defaultValue=last_output_gpkg
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        gridadmin_folder = self.parameterAsString(parameters, self.INPUT, context)
        if gridadmin_folder is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        input_gridadmin = os.path.join(gridadmin_folder, "gridadmin.h5")

        gpkg_path = self.parameterAsString(parameters, self.OUTPUT, context)
        if gpkg_path is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT))
        gpkg_path = os.path.join(gpkg_path, "out.gpkg")

        s = QgsSettings()
        s.setValue("threedi-results-analysis/gridadmin_to_gpkg/last_input", gridadmin_folder)
        s.setValue("threedi-results-analysis/gridadmin_to_gpkg/last_output_gpkg", os.path.dirname(gpkg_path))
        plugin_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        styles_dir = os.path.join(plugin_dir, "styles")

        progress = Progress(feedback)
        exporter = GeopackageExporter(input_gridadmin, gpkg_path)
        exporter.export(progress.update)
        feedback.pushInfo("Export done!")

        # Unfortunately, temporaryLayerStore keeps layers to be added as a dictionary, so the order is lost
        data_srcs = OrderedDict([
            ("Obstacle", "obstacle"),
            ("Cell", "cell"),
            ("Pump (point)", "pump"),
            ("Pump (line)", "pump_linestring"),
            ("Node", "node"),
            ("Flowline", "flowline")
        ])

        layers = dict()
        empty_layers = []
        epsg_codes = set()
        for layer_name, table_name in data_srcs.items():
            uri = gpkg_path + f"|layername={table_name}"
            self.uc.log_info(f"uri:{uri}")
            layers[layer_name] = QgsVectorLayer(uri, layer_name, "ogr")

            # only load layers that contain some features
            if not layers[layer_name].featureCount():
                empty_layers.append(layer_name)
                continue

            # apply the style and add for loading when alg is completed
            qml_path = safe_join(styles_dir, f"{table_name}.qml")
            if os.path.exists(qml_path):
                layers[layer_name].loadNamedStyle(qml_path)
            context.temporaryLayerStore().addMapLayer(layers[layer_name])
            context.addLayerToLoadOnCompletion(
                layers[layer_name].id(),
                QgsProcessingContext.LayerDetails(layers[layer_name].id(), context.project(), layer_name)
            )

        # Empty layers info
        if empty_layers:
            empty_info = "\n\nThe following layers contained no feature:\n * " + "\n * ".join(empty_layers) + "\n\n"
            feedback.pushInfo(empty_info)
            self.uc.log_info(empty_info)

        # Set project CRS only if all source layers have the same CRS
        if len(epsg_codes) == 1:
            code_int = int(list(epsg_codes)[0])
            crs = QgsCoordinateReferenceSystem.fromEpsgId(code_int)
            if crs.isValid():
                context.project().setCrs(crs)
                crs_info = f"Setting project CRS according to the source gridadmin file."
            else:
                crs_info = "Skipping setting project CRS - does gridadmin file contains a valid EPSG code?"
        else:
            crs_info = f"Skipping setting project CRS - the source file {input_gridadmin}"\
                       " contained data with various CRS."
        feedback.pushInfo(crs_info)
        self.uc.log_info(crs_info)

        return {}
