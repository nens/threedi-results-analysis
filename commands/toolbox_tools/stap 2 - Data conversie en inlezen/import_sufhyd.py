"""This script calculates statistics on the selected layer for manholes and
connection nodes and outputs it to csv.
"""
import csv
import inspect
import os

from ThreeDiToolbox.stats.ncstats import NcStats, NcStatsAgg
from ThreeDiToolbox.utils.user_messages import (
    pop_up_info, log, pop_up_question)
from ThreeDiToolbox.views.import_sufhyd_dialog import (
    ImportSufhydDialogWidget)
from ThreeDiToolbox.commands.base.custom_command import (
    CustomCommandBase, join_stats)



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


    def run(self):
        self.show_gui()

    def show_gui(self):

        # sufhyd_file


        # import into:


        self.tool_dialog_widget = ImportSufhydDialogWidget(
            iface=self.iface, ts_datasource=self.ts_datasource, command=self)
        self.tool_dialog_widget.exec_()  # block execution


    def run_it(self):
        

        pass
