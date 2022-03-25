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

from qgis.PyQt.QtCore import QCoreApplication, QSettings
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingContext,
    QgsProcessingParameterFile,
    QgsProcessingParameterFolderDestination,
    QgsSettings,
    QgsVectorLayer,
)
from qgis.utils import iface
from ..user_communication import UserCommunication
from ..utils import safe_join


try:
    from threedigrid.admin.gridresultadmin import GridH5Admin
    from threedigrid.admin.breaches.exporters import BreachesOgrExporter
    from threedigrid.admin.levees.exporters import LeveeOgrExporter
    from threedigrid.admin.lines.exporters import LinesOgrExporter
    from threedigrid.admin.nodes.exporters import NodesOgrExporter
    from threedigrid.admin.nodes.exporters import CellsOgrExporter
    from threedigrid.orm.constants import GEO_PACKAGE_DRIVER_NAME
except (ImportError, ModuleNotFoundError):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(this_dir)
    whl_path = os.path.join(parent_dir, "deps", "threedigrid-1.2.0-py2.py3-none-any.whl")
    sys.path.append(whl_path)
    from threedigrid.admin.gridresultadmin import GridH5Admin
    from threedigrid.admin.breaches.exporters import BreachesOgrExporter
    from threedigrid.admin.levees.exporters import LeveeOgrExporter
    from threedigrid.admin.lines.exporters import LinesOgrExporter
    from threedigrid.admin.nodes.exporters import NodesOgrExporter
    from threedigrid.admin.nodes.exporters import CellsOgrExporter
    from threedigrid.orm.constants import GEO_PACKAGE_DRIVER_NAME


class ThreeDiConvertToGpkgAlgorithm(QgsProcessingAlgorithm):
    """ Convert gridadmin.h5 to GeoPackage with vector layers """

    INPUT = "INPUT"
    EPSG = "EPSG"
    OUTPUT_DIR = "OUTPUT_DIR"

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
        last_input_dir = s.value("threedi-results-analysis/last_input_dir", None)
        last_output_dir = s.value("threedi-results-analysis/last_output_dir", None)

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr("Input gridadmin.h5 file"),
                behavior=QgsProcessingParameterFile.File,
                extension="h5",
                defaultValue=last_input_dir
            )
        )

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT_DIR,
                self.tr("Output folder"),
                defaultValue=last_output_dir
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        input_gridadmin = self.parameterAsFile(parameters, self.INPUT, context)
        if input_gridadmin is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        gpkgs_dir = self.parameterAsString(parameters, self.OUTPUT_DIR, context)
        if gpkgs_dir is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT_DIR))

        s = QSettings()
        s.setValue("threedi-results-analysis/last_input_dir", input_gridadmin)
        s.setValue("threedi-results-analysis/last_output_dir", gpkgs_dir)
        plugin_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        ga = GridH5Admin(input_gridadmin)
        feedback.pushInfo(f"Opened gridadmin:\n{ga.model_name}\n\n")

        self.uc.start_timer("exports")
        layers = dict()
        empty_layers = []
        epsg_codes = set()
        models = {
            # model description -> (model part, model exporter)
            "Node": (ga.nodes, NodesOgrExporter),
            "Cell": (ga.cells, CellsOgrExporter),
            "Flowline": (ga.lines, LinesOgrExporter),
            "Linear obstacle": (ga.levees, LeveeOgrExporter),
        }
        for model_name in models.keys():
            model, exporter_class = models[model_name]
            layer_name = f"{model_name}"
            gpkg_path = os.path.join(gpkgs_dir, f"{layer_name}.gpkg")
            feedback.pushInfo(f"Converting {layer_name}")
            exporter = exporter_class(model)
            exporter.set_driver(driver_name=GEO_PACKAGE_DRIVER_NAME)
            exporter.save(gpkg_path, model.data, model.epsg_code)
            epsg_codes.add(model.epsg_code)
            info_done = f"done in {round(self.uc.read_timer('exports'), 1)} sec"
            feedback.pushInfo(info_done)
            self.uc.log_info(info_done)

            # create output layer
            uri = gpkg_path + f"|layername={layer_name}.gpkg"  # TODO: gridadmin exporter saves layers with extention
            self.uc.log_info(f"uri:{uri}")
            layers[layer_name] = QgsVectorLayer(uri, layer_name, "ogr")

            # only load layers that contain some features
            if not layers[layer_name].featureCount():
                empty_layers.append(layer_name)
                continue

            qml_path = safe_join(plugin_dir, "styles", f"{layer_name}.qml")
            if os.path.exists(qml_path):
                layers[layer_name].loadNamedStyle(qml_path)
            context.temporaryLayerStore().addMapLayer(layers[layer_name])
            context.addLayerToLoadOnCompletion(
                layers[layer_name].id(),
                QgsProcessingContext.LayerDetails(layers[layer_name].id(), context.project(), layer_name)
            )

        # Empty layers info
        if empty_layers:
            empty_info = "\n\nThe following layers contained no feature:\n *" + "\n * ".join(empty_layers) + "\n\n"
            feedback.pushInfo(empty_info)
            self.uc.log_info(empty_info)

        # Set project CRS
        if len(epsg_codes) == 1:
            code_int = int(list(epsg_codes)[0])
            crs = QgsCoordinateReferenceSystem.fromEpsgId(code_int)
            if crs.isValid():
                context.project().setCrs(crs)
                crs_info = f"Setting project CRS according to the source file {input_gridadmin}."
            else:
                crs_info = "Skipping setting project CRS - invalid code"
        else:
            crs_info = f"Skipping setting project CRS - the source file {input_gridadmin}"\
                       " contained data with different CRS."
        feedback.pushInfo(crs_info)
        self.uc.log_info(crs_info)

        return {}
