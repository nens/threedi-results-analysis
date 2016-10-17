# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import logging

from qgis.core import QgsMapLayerRegistry

from ThreeDiToolbox.utils.user_messages import messagebar_message
from ThreeDiToolbox.views.predict_calc_points_dialog import (
    PredictCalcPointsDialogWidget)
from ThreeDiToolbox.commands.base.custom_command import (
    CustomCommandBase)
from ThreeDiToolbox.utils.threedi_database import (
    ThreediDatabase)
from ThreeDiToolbox.utils.predict_calc_points import Predictor


log = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):
    """
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

        # postgres
        pal = Predictor(flavor=db_type)
        print db_set
        uri = pal.get_uri(**db_set)
        calc_pnts_lyr = pal.get_layer_from_uri(uri, 'v2_calculation_point', 'the_geom')
        pal.create_query_obj_from_uri(uri)
        pal.build_calc_type_dict(epsg_code=28992)
        pal.predict_points(output_layer=calc_pnts_lyr)
        QgsMapLayerRegistry.instance().addMapLayer(calc_pnts_lyr)

        # # spatialite
        # pal = PointsAlongLine(flavor='spatialite')
        # uri = pal.get_uri(**sqlite_kwargs)
        # calc_pnts_lyr = pal.get_layer_from_uri(uri, 'v2_calculation_point', 'the_geom')
        # pal.create_query_obj_from_uri(uri)
        # pal.build_calc_type_dict(epsg_code=28992)
        # pal.predict_points(output_layer=calc_pnts_lyr, transform='28992:4326')
        #
        #
        # db = ThreediDatabase(db_set, db_type)
        # guesser = Guesser(db)
        # msg = guesser.run(action_list, only_empty_fields)
        msg = 'here goes custom message'
        messagebar_message('Guess indicators ready',
                           msg,
                           duration=20)
        log.info('Guess indicators ready.\n' + msg)


        # martijn_kwargs = {
        #     'flavor': 'postgres',
        #     'address': '10.0.3.111',
        #     'port': '5432',
        #     'name': 'work_martijn',
        #     'user_name':'buildout',
        #     'password': 'buildout',
        #     'schema': 'public',
        #     'table_name': 'v2_channel',
        #     'geom_column': 'the_geom',
        #     'layer_name': 'channel_new',
        # }
        # viewtest_kwargs = {
        #     'flavor': 'postgres',
        #     'address': '10.0.3.111',
        #     'port': '5432',
        #     'name': 'work_viewtest',
        #     'user_name':'buildout',
        #     'password': 'buildout',
        #     'schema': 'public',
        # }
        # sqlite_kwargs = {
        #     'address': '/home/lars_claussen/Development/model_data/v2_bergermeer/4c8a2e214a954a0f3a870888ac9e368233fc00b9/v2_bergermeer.sqlite',
        #     'port': '',
        #     'name': '',
        #     'user_name':'',
        #     'password': '',
        #     'schema': '',
        #     'table_name': 'v2_channel',
        #     'geom_column': 'the_geom',
        #     'layer_name': 'channel_sqlite',
        # }


