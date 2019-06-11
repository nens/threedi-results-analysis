# (c) Nelen & Schuurmans, see LICENSE.rst.
from qgis.core import Qgis
from qgis.core import QgsProject
from ThreeDiToolbox.tool_commands.create_breach_locations import breach_location_dialog
from ThreeDiToolbox.tool_commands.custom_command_base import CustomCommandBase
from ThreeDiToolbox.utils.user_messages import messagebar_message
from ThreeDiToolbox.utils.user_messages import progress_bar

import logging


logger = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):
    """
    Move connected points across the nearest levee.
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
        self.tool_dialog_widget = \
            breach_location_dialog.CreateBreachLocationsDialogWidget(command=self)
        self.tool_dialog_widget.exec_()  # block execution

    def run_it(self, breach_loc, auto_commit):
        """
        execute the tool

        :param breach_loc: threedi_schema_edits.breach_location.BresLocation
            instance
        :param auto_commit: save the potential breach location directly to
            the database (only in case the dry-run option has not been
            selected)
        """

        breach_location = breach_loc
        if not breach_location.has_valid_selection:
            msg = "You need to select at least two connection points"
            messagebar_message("Error", msg, level=Qgis.Critical, duration=5)
            return

        calc_points_dict = breach_location.get_calc_points_by_content()

        cnt_iterations = len(calc_points_dict)
        cnt = 1

        with progress_bar(self.iface) as pb:
            for key, values in calc_points_dict.items():
                calc_type = key[1]
                connected_points_selection = breach_location.get_connected_points(
                    values, calc_type
                )
                breach_location.move_points_behind_levee(
                    connected_points_selection, calc_type
                )
                current = (cnt / float(cnt_iterations)) * 100
                pb.setValue(current)
                cnt += 1

        if breach_location.is_dry_run:
            breach_location.pnt_layer.commitChanges()
            breach_location.pnt_layer.updateExtents()
            breach_location.line_layer.updateExtents()
            QgsProject.instance().addMapLayers(
                [breach_location.pnt_layer, breach_location.line_layer]
            )

        if auto_commit:
            breach_location.connected_pnt_lyr.commitChanges()
        breach_location.connected_pnt_lyr.updateExtents()
        self.iface.mapCanvas().refresh()
        breach_location.connected_pnt_lyr.triggerRepaint()
        if not breach_location.is_dry_run:
            msg = "Created {} potential breach locations".format(
                breach_location.cnt_moved_pnts
            )
            messagebar_message("Finished", msg, level=Qgis.Success, duration=8)
