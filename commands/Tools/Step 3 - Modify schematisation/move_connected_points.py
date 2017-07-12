# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.
import logging
import collections

from qgis.core import QgsMapLayerRegistry

from ThreeDiToolbox.utils import constants
from ThreeDiToolbox.utils.user_messages import messagebar_message
from ThreeDiToolbox.widgets.progress import progress_bar
from ThreeDiToolbox.views.predict_calc_points_dialog import MoveConnectedPointsDialogWidget  # noqa
from ThreeDiToolbox.commands.base.custom_command import CustomCommandBase


log = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):
    """
    Move connected points across the nearest levee.
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
        self.tool_dialog_widget = MoveConnectedPointsDialogWidget(command=self)
        self.tool_dialog_widget.exec_()  # block execution

    def run_it(self, bres_loc, auto_commit):
        """
        execute the tool

        :param bres_loc: threedi_schema_edits.bres_location.BresLocation
            instance
        :param auto_commit: save the potential bres location directly to
            the database (only in case the dry-run option has not been
            selected)
        """

        bres_location = bres_loc
        if not bres_location.has_valid_selection:
            msg = "You need to select at least two connection points"
            messagebar_message(
                "Error", msg, level=constants.MESSAGE_LEVEL['error'],
                duration=5
            )
            return

        calc_points_dict = bres_location.get_calc_points_by_content()

        cnt_iterations = len(calc_points_dict)
        cnt = 1

        with progress_bar(self.iface) as pb:
            for key, values in calc_points_dict.iteritems():
                calc_type = key[1]
                connected_points_selection = bres_location.get_connected_points(
                    values, calc_type
                )
                bres_location.move_points_behind_levee(
                    connected_points_selection, calc_type
                )
                current = (cnt/float(cnt_iterations)) * 100
                pb.setValue(current)
                cnt += 1

        if bres_location.is_dry_run:
            bres_location.pnt_layer.commitChanges()
            bres_location.pnt_layer.updateExtents()
            bres_location.line_layer.updateExtents()
            QgsMapLayerRegistry.instance().addMapLayers(
                [bres_location.pnt_layer, bres_location.line_layer]
            )

        if auto_commit:
            bres_location.connected_pnt_lyr.commitChanges()
        bres_location.connected_pnt_lyr.updateExtents()
        self.iface.mapCanvas().refresh()
        bres_location.connected_pnt_lyr.triggerRepaint()
        if not bres_location.is_dry_run:
            msg = "Created {} potential bres locations".format(
                bres_location.cnt_moved_pnts
            )
            messagebar_message("Finished", msg, level=3, duration=8)
