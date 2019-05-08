# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

from qgis.core import QgsProject
from ThreeDiToolbox.commands.base.custom_command import CustomCommandBase
from ThreeDiToolbox.threedi_schema_edits.predictions import Predictor
from ThreeDiToolbox.utils import constants
from ThreeDiToolbox.utils.user_messages import messagebar_message
from ThreeDiToolbox.utils.user_messages import pop_up_question
from ThreeDiToolbox.views.modify_schematisation_dialogs import \
    PredictCalcPointsDialogWidget

import logging

logger = logging.getLogger(__name__)


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
        self.iface = kwargs.get("iface")
        self.ts_datasource = kwargs.get("ts_datasource")
        self.tool_dialog_widget = None

    def run(self):
        self.show_gui()

    def show_gui(self):
        self.tool_dialog_widget = PredictCalcPointsDialogWidget(command=self)
        self.tool_dialog_widget.exec_()  # block execution

    def run_it(self, db_set, db_type):
        """
        :param db_set: dict of database settings. Expected keywords:
                'host': '',
                'port': '',
                'name': '',
                'username': '',
                'password': '',
                'schema': '',
                'database': '',
                'db_path': ,
        :param db_type: 'spatialite' or 'postgres'
        """

        predictor = Predictor(db_type)
        uri = predictor.get_uri(**db_set)
        calc_pnts_lyr = predictor.get_layer_from_uri(
            uri, constants.TABLE_NAME_CALC_PNT, "the_geom"
        )
        self.connected_pnts_lyr = predictor.get_layer_from_uri(
            uri, constants.TABLE_NAME_CONN_PNT, "the_geom"
        )
        predictor.start_sqalchemy_engine(db_set)
        if not self.fresh_start(predictor):
            return
        default_epsg_code = 28992
        epsg_code = predictor.get_epsg_code() or default_epsg_code
        logger.info(
            "[*] Using epsg code {} to build the calc_type_dict".format(epsg_code)
        )
        predictor.build_calc_type_dict(epsg_code=epsg_code)
        transform = None
        # spatialites are in WGS84 so we need a transformation
        if db_type == "spatialite":
            transform = "{epsg_code}:4326".format(epsg_code=epsg_code)
        succces, features = predictor.predict_points(
            output_layer=calc_pnts_lyr, transform=transform
        )

        if succces:
            msg = "Predicted {} calculation points".format(len(features))
            level = 3
            QgsProject.instance().addMapLayer(calc_pnts_lyr)
        else:
            msg = (
                "Predicted calculation points failed! "
                'Are you sure the table "v2_calculation_point" '
                "is empty?".format(len(features))
            )
            level = 1
        messagebar_message("Finished", msg, level=level, duration=12)
        cp_succces, cp_features = predictor.fill_connected_pnts_table(
            calc_pnts_lyr=calc_pnts_lyr, connected_pnts_lyr=self.connected_pnts_lyr
        )
        if cp_succces:
            cp_msg = "Created {} connected points template".format(len(cp_features))
            cp_level = 3
            QgsProject.instance().addMapLayer(self.connected_pnts_lyr)
        else:
            cp_msg = "Creating connected points failed!"
            cp_level = 1
        messagebar_message("Finished", cp_msg, level=cp_level, duration=12)
        logger.info("Done predicting calcualtion points.\n" + msg)

    def fresh_start(self, predictor):
        """
        Check whether we start off fresh or not. That is, if the
        calculation and connected points have been calculated before
        the stale data will be removed from the database after
        the user has confirmed to do so

        :param predictor: utils.predictions.Predictor instance

        :returns True if we start fresh. In this case all database
            tables are empty. False otherwise
        """
        fresh = True
        are_empty = []
        table_names = [constants.TABLE_NAME_CALC_PNT, constants.TABLE_NAME_CONN_PNT]
        for tn in table_names:
            are_empty.append(predictor.threedi_db.table_is_empty(tn))
        if not all(are_empty):
            fresh = False
            question = (
                "Calculation point and connected point tables are not "
                "empty! Do you want to delete all their contents?"
            )

            if pop_up_question(question, "Warning"):
                predictor.threedi_db.delete_from(constants.TABLE_NAME_CALC_PNT)
                predictor.threedi_db.delete_from(constants.TABLE_NAME_CONN_PNT)
                fresh = True
        return fresh
