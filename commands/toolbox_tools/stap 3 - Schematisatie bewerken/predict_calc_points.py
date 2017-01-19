# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import logging

from qgis.core import QgsMapLayerRegistry, QgsFeatureRequest
from PyQt4.QtCore import QPyNullVariant

from ThreeDiToolbox.utils.user_messages import messagebar_message
from ThreeDiToolbox.views.predict_calc_points_dialog import (
    PredictCalcPointsDialogWidget)
from ThreeDiToolbox.commands.base.custom_command import (
    CustomCommandBase)
from ThreeDiToolbox.utils.predictions import Predictor

from ThreeDiToolbox.utils import constants
log = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):
    """
    command to predict the threedicore calculation points based on
    calculation type, geometry and the attribute dist_calc_points

    The results will be written to the database table v2_calculation_point.
    When running the command, the table must be empty!
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.iface = kwargs.get('iface')
        self.ts_datasource = kwargs.get('ts_datasource')
        self.tool_dialog_widget = None

    def run(self):
        self.show_gui()

    def show_gui(self):
        self.tool_dialog_widget = PredictCalcPointsDialogWidget(command=self)
        self.tool_dialog_widget.exec_()  # block execution

    def run_it(self, db_set, db_type):

        pal = Predictor(db_type)
        uri = pal.get_uri(**db_set)
        calc_pnts_lyr = pal.get_layer_from_uri(
            uri, 'v2_calculation_point', 'the_geom')
        self.connected_pnts_lyr = pal.get_layer_from_uri(
            uri, 'v2_connected_pnt', 'the_geom')
        pal.start_sqalchemy_engine(db_set)
        default_epsg_code = 28992
        epsg_code = pal.get_epsg_code() or default_epsg_code
        log.info(
            "[*] Using epsg code {} to build the calc_type_dict".format(
                epsg_code)
        )
        pal.build_calc_type_dict(epsg_code=epsg_code)
        transform = None
        # spatialites are in WGS84 so we need a tranformation
        if db_type == 'spatialite':
            transform='{epsg_code}:4326'.format(epsg_code=epsg_code)
        succces, features = pal.predict_points(
            output_layer=calc_pnts_lyr, transform=transform)

        if succces:
            msg = 'Predicted {} calculation points'.format(len(features))
            level = 3
            QgsMapLayerRegistry.instance().addMapLayer(calc_pnts_lyr)
        else:
            msg = 'Predicted calculation points failed! ' \
                  'Are you sure the table "v2_calculation_point" ' \
                  'is empty?'.format(len(features))
            level = 1
        messagebar_message("Finished",  msg, level=level, duration=12)
        cp_succces, cp_features = pal.fill_connected_pnts_table(
            calc_pnts_lyr=calc_pnts_lyr,
            connected_pnts_lyr=self.connected_pnts_lyr)
        if cp_succces:
            cp_msg = 'Created {} connected points template'.format(len(cp_features))
            cp_level = 3
            QgsMapLayerRegistry.instance().addMapLayer(self.connected_pnts_lyr)
        else:
            cp_msg = 'Creating connected points failed!'
            cp_level = 1
        messagebar_message("Finished",  cp_msg, level=cp_level, duration=12)
        log.info('Done predicting calcualtion points.\n' + msg)
