"""This script calculates statistics on the selected layer for manholes and
connection nodes and outputs it to csv.
"""
import csv
import inspect
import os

from ThreeDiToolbox.stats.ncstats import NcStats
from ThreeDiToolbox.utils.user_messages import (
    pop_up_info, log, pop_up_question)
from ThreeDiToolbox.views.tool_dialog import ToolDialogWidget
from ThreeDiToolbox.commands.base.custom_command import (
    CustomCommandBase, join_stats)


class CustomCommand(CustomCommandBase):

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

        self.derived_parameters = ['wos_height', 'water_depth']
        # All the NcStats parameters we want to calculate.
        self.parameters = NcStats.AVAILABLE_MANHOLE_PARAMETERS + \
            self.derived_parameters

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
        if 'manhole' not in layer_name and 'connection_node' not in layer_name:
            pop_up_info(
                "%s doesn't contain manholes or connection nodes" % layer_name,
                title='Error')
            return

        result_dir = os.path.dirname(self.datasource.file_path.value)
        nds = self.datasource.datasource()  # the netcdf datasource
        ncstats = NcStats(datasource=nds)

        # Generate data
        result = dict()
        for feature in self.layer.getFeatures():
            # fid = feature.id()  # = ROWID
            fid = feature['id']  # more explicit
            result[fid] = dict()
            result[fid]['id'] = fid
            for param_name in self.parameters:
                # Water op straat berekening (wos_height):
                if param_name == 'wos_height':
                    try:
                        result[fid][param_name] = ncstats.s1_max(
                            layer_name, fid) - feature['surface_level']
                    except (ValueError, TypeError):
                        result[fid][param_name] = None
                    except KeyError:
                        log("Feature doesn't have surface level")
                        result[fid][param_name] = None
                # Waterdiepte berekening:
                elif param_name == 'water_depth':
                    try:
                        result[fid][param_name] = ncstats.s1_max(
                            layer_name, fid) - feature['bottom_level']
                    except (ValueError, TypeError):
                        result[fid][param_name] = None
                    except KeyError:
                        log("Feature doesn't have bottom level")
                        result[fid][param_name] = None
                # Business as usual (NcStats method)
                else:
                    method = getattr(ncstats, param_name)
                    try:
                        result[fid][param_name] = method(layer_name, fid)
                    except ValueError:
                        result[fid][param_name] = None

        # Write to csv file
        filename = layer_name + '_stats.csv'
        filepath = os.path.join(result_dir, filename)
        with open(filepath, 'wb') as csvfile:
            fieldnames = ['id'] + self.parameters
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                    delimiter=',')
            writer.writeheader()
            for fid, val_dict in result.items():
                writer.writerow(val_dict)

        pop_up_info("Generated: %s" % filepath, title='Finished')

        if pop_up_question(
                msg="Do you want to join the CSV with the view layer?",
                title="Join"):
            join_stats(filepath, self.layer, 'id')
