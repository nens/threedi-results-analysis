"""This script calculates statistics on the selected layer for manholes and
connection nodes and outputs it to csv.
"""
import csv
import inspect
import os

from ThreeDiToolbox.stats.ncstats import NcStats, NcStatsAgg
from ThreeDiToolbox.utils.user_messages import (
    pop_up_info, log, pop_up_question)
from ThreeDiToolbox.views.tool_dialog import ToolDialogWidget
from ThreeDiToolbox.commands.base.custom_command import (
    CustomCommandBase, join_stats)

# node-like layers for which this script works (without the 'v2_' or
# 'sewerage_' prefix)
NODE_OBJECTS = ['manhole', 'connection_node', 'node']


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

        self.derived_parameters = [
            'wos_height',
            'water_depth',
            # This one isn't really derived (which means, it is calculated
            # in this script as opposed to NcStats), but this makes things
            # easier when using NcStatsAgg
            'wos_duration']

        # These will be dynamically set:
        self.layer = None
        self.datasource = None

    def run(self):
        self.show_gui()

    def show_gui(self):
        self.tool_dialog_widget = ToolDialogWidget(
            iface=self.iface, ts_datasource=self.ts_datasource, command=self)
        self.tool_dialog_widget.exec_()  # block execution

    def calc_results(
            self, ncstats, parameters, layer_name, feature_id,
            surface_level=None, bottom_level=None):
        """Calcs results for all parameters and puts them in a dict.

        Args:
            ncstats: NcStats instance
            parameters: a list of (netCDF) parameters
            layer_name: the name of the layer we want to query results for
            feature_id: feature id (is related to the layer_name)
            surface_level: an additional parameter that is needed for
                calculating 'wos_height'
            bottom_level: an additional parameter that is needed for calculing
                'water_depth'

        Note: when the last two kwargs are missing, the results cannot be
        calculated and are simply set to None

        Returns:
            a dictionary {param_name: result_value, ...}
        """
        result = dict()
        for param_name in parameters:
            # Water op straat berekening (wos_height):
            if param_name == 'wos_height':
                if surface_level is None:
                    result[param_name] = None
                try:
                    s1_max = ncstats.get_value_from_parameter(
                        layer_name, feature_id, 's1_max')
                    result[param_name] = s1_max - surface_level
                except (ValueError, TypeError, AttributeError):
                    result[param_name] = None
            # Waterdiepte berekening:
            elif param_name == 'water_depth':
                if bottom_level is None:
                    result[param_name] = None
                try:
                    s1_max = ncstats.get_value_from_parameter(
                        layer_name, feature_id, 's1_max')
                    result[param_name] = s1_max - bottom_level
                except (ValueError, TypeError, AttributeError):
                    result[param_name] = None
            # Business as usual (NcStats method)
            else:
                try:
                    result[param_name] = \
                        ncstats.get_value_from_parameter(
                            layer_name, feature_id, param_name,
                            surface_level=surface_level)
                except (ValueError, IndexError):
                    result[param_name] = None
                except TypeError:
                    # Probably an error with wos_duration, which
                    # will ONLY work for structures with a surface_level (
                    # i.e. manholes).
                    result[param_name] = None
        return result

    def run_it(self, layer=None, datasource=None, interactive=True):
        """
            Args:
                layer: qgis vector layer
                datasource: BaseModelItem from TimeseriesDatasourceModel
                interactive: if False, disable all prompts and assume the
                most logical answer to all question prompts.
        """
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

        layer_name = self.layer.name()
        if not any(s in layer_name for s in NODE_OBJECTS):
            if interactive:
                pop_up_info(
                    "%s is not a valid node layer" % layer_name,
                    title='Error')
            return

        result_dir = os.path.dirname(self.datasource.file_path.value)
        nds = self.datasource.datasource()  # the netcdf datasource

        # Caution: approaching HACK territory!
        # Motivation: This is a hack for v2_manholes. Manholes just have a
        # foreign key to v2_connection_nodes and aren't a thing in itself.
        # So all v2_manhole stuff should be delegated to the way
        # v2_connection_nodes works.
        old_layer_name = layer_name
        if layer_name == 'v2_manhole':
            layer_name = 'v2_connection_nodes'

        # Get the primary key of the layer, plus other specifics:
        # TODO: not sure if we want to make ncstats distinction based on
        # the layer type
        if layer_name == 'nodes':
            # It's a memory layer
            layer_id_name = 'id'
            ncstats = NcStatsAgg(datasource=nds)
        elif 'v2' in layer_name:
            # It's a v2 spatialite layer
            layer_id_name = 'id'
            ncstats = NcStatsAgg(datasource=nds)
        else:
            # It's sewerage spatialite (no agg. netcdf)
            layer_id_name = 'id'
            ncstats = NcStats(datasource=nds)

        # All the NcStats parameters we want to calculate (can differ per
        # NcStats version)
        parameters = ncstats.AVAILABLE_MANHOLE_PARAMETERS + \
            self.derived_parameters

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
            result[fid]['id'] = fid  # normalize layer id name

            try:
                surface_level = feature['surface_level']
            except KeyError:
                log("Feature doesn't have surface level")
                surface_level = None
            try:
                bottom_level = feature['bottom_level']
            except KeyError:
                log("Feature doesn't have bottom level")
                bottom_level = None

            # There are two hacks:
            # Hack for v2_manhole, see previous comment.
            if old_layer_name == 'v2_manhole':
                hack_fid = feature['connection_node_id']
            else:
                hack_fid = feature[layer_id_name]

            results_from_params = self.calc_results(
                ncstats,
                parameters,
                layer_name,
                hack_fid,
                surface_level=surface_level,
                bottom_level=bottom_level)
            result[fid].update(results_from_params)

        # Write to csv file
        filename = old_layer_name + '_stats.csv'
        filepath = os.path.join(result_dir, filename)
        with open(filepath, 'wb') as csvfile:
            fieldnames = ['id'] + parameters

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                    delimiter=',')
            writer.writeheader()
            for fid, val_dict in result.items():
                writer.writerow(val_dict)

        if interactive:
            pop_up_info("Generated: %s" % filepath, title='Finished')
            if pop_up_question(
                    msg="Do you want to join the CSV with the view layer?",
                    title="Join"):
                join_stats(filepath, self.layer, layer_id_name)
        else:
            join_stats(filepath, self.layer, layer_id_name, interactive=False)
