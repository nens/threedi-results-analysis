"""This script calculates statistics on the selected layer for structures and
outputs it to csv.
"""
import csv
import inspect
import os

from ThreeDiToolbox.stats.ncstats import NcStats, NcStatsAgg
from ThreeDiToolbox.utils.user_messages import pop_up_info, pop_up_question
from ThreeDiToolbox.views.tool_dialog import ToolDialogWidget
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

        # These will be dynamically set:
        self.layer = None
        self.datasource = None

    def run(self):
        self.show_gui()

    def show_gui(self):
        self.tool_dialog_widget = ToolDialogWidget(
            iface=self.iface, ts_datasource=self.ts_datasource, command=self)
        self.tool_dialog_widget.exec_()  # block execution

    def run_it(self, layer=None, datasource=None):
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
        layer_name = self.layer.name()
        structures = ['weir', 'pumpstation', 'pipe', 'orifice', 'culvert',
                      'flowline']
        if not any(s in layer_name for s in structures):
            pop_up_info("%s is not a valid structure layer. Valid layers are: "
                        "%s" % (layer_name, structures), title='Error')
            return

        include_2d = pop_up_question("Include 2D?")

        result_dir = os.path.dirname(self.datasource.file_path.value)
        nds = self.datasource.datasource()  # the netcdf datasource

        # Get the primary key of the layer, plus other specifics:
        if layer_name == 'flowlines':
            layer_id_name = 'id'
            # TODO: not sure if we want to make ncstats distinction based on
            # the layer type
            ncstats = NcStatsAgg(datasource=nds)
        else:
            # It's a view
            layer_id_name = 'ROWID'
            ncstats = NcStats(datasource=nds)

        # Generate data
        result = dict()
        for feature in self.layer.getFeatures():

            # skip 2d stuff
            if not include_2d:
                try:
                    if feature['type'] == '2d':
                        continue
                except KeyError:
                    pass

            fid = feature[layer_id_name]
            result[fid] = dict()
            result[fid]['id'] = fid  # normalize layer id name to 'id' in csv
            for param_name in ncstats.AVAILABLE_STRUCTURE_PARAMETERS:
                try:
                    result[fid][param_name] = \
                        ncstats.get_value_from_parameter(
                            layer_name, feature[layer_id_name], param_name)
                except (ValueError, IndexError, AttributeError):
                    # AttributeError: is raised in NcStats because in case of
                    # KeyErrors in get_value_from_parameter the method finding
                    # is propagated to NcStats and when the method doesn't
                    # exist AttributeError is raised. A better solution is to
                    # filter AVAILABLE_STRUCTURE_PARAMETERS beforehand.
                    result[fid][param_name] = None

        # Write to csv file
        filename = layer_name + '_stats.csv'
        filepath = os.path.join(result_dir, filename)
        with open(filepath, 'wb') as csvfile:
            fieldnames = ['id'] + ncstats.AVAILABLE_STRUCTURE_PARAMETERS
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                    delimiter=',')
            writer.writeheader()
            for fid, val_dict in result.items():
                writer.writerow(val_dict)

        pop_up_info("Generated: %s" % filepath, title='Finished')

        if pop_up_question(
                msg="Do you want to join the CSV with the view layer?",
                title="Join"):
            join_stats(filepath, self.layer, layer_id_name)
