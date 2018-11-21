"""This script calculates statistics on the selected layer for structures and
outputs it to csv.
"""
from builtins import object
import inspect
import os

from ThreeDiToolbox.utils.user_messages import pop_up_info, pop_up_question
from ThreeDiToolbox.stats.utils import (
    generate_structure_stats, get_structure_layer_id_name, csv_join)
from ThreeDiToolbox.views.tool_dialog import ToolDialogWidget
from ThreeDiToolbox.commands.base.custom_command import (
    CustomCommandBase)


class CustomCommand(CustomCommandBase):
    """
    Things to note:

    If you select a memory layer the behaviour will be different from clicking
    on a normal spatialite view. For example, NcStatsAgg will be used instead
    of NcStats.
    """

    class Fields(object):
        name = "Test script"
        value = 1

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._fields = sorted(
            [(name, cl) for name, cl in
             inspect.getmembers(self.Fields,
                                lambda a: not(inspect.isroutine(a)))
             if not name.startswith('__') and not name.startswith('_')])
        self.iface = kwargs.get('iface')
        self.ts_datasource = kwargs.get('ts_datasource')

        # These will be dynamically set:
        self.layer = None
        self.datasource = None

    def run(self):
        self.show_gui()

    def show_gui(self):
        self.tool_dialog_widget = ToolDialogWidget(
            iface=self.iface, ts_datasource=self.ts_datasource, command=self)
        self.tool_dialog_widget.exec_()  # block execution

    def run_it(self, layer=None, datasource=None, add_to_legend=True,
               interactive=True):
        if layer:
            self.layer = layer
        if datasource:
            self.datasource = datasource
        if not self.layer:
            pop_up_info("No layer selected, aborting", title='Error')
            return
        if not self.datasource:
            pop_up_info("No datasource found, aborting.", title='Error')
            return
        if interactive:
            include_2d = pop_up_question("Include 2D?")
        else:
            include_2d = True

        result_dir = os.path.dirname(self.datasource.file_path.value)
        nds = self.datasource.datasource()  # the netcdf datasource

        layer_id_name = get_structure_layer_id_name(self.layer.name())
        try:
            filepath = generate_structure_stats(
                nds, result_dir, self.layer, layer_id_name,
                include_2d=include_2d)
        except ValueError as e:
            if interactive:
                pop_up_info(e, title='Error')
            return

        join_it = True

        if interactive:
            pop_up_info("Generated: %s" % filepath, title='Finished')
            join_it = pop_up_question(
                msg="Do you want to join the CSV with the view layer?",
                title="Join")

        if join_it:
            csv_layer = csv_join(filepath, self.layer, layer_id_name,
                                 add_to_legend=add_to_legend)
            if interactive:
                pop_up_info("Finished joining '%s' with '%s'." % (
                    csv_layer.name(), self.layer.name()),
                    title='Join finished')
            return csv_layer
