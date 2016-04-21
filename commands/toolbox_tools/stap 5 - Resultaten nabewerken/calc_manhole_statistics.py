"""This script calculates statistics on the current layer for structures and
outputs it to csv.
"""
import csv
import inspect
import os

from ThreeDiToolbox.stats.ncstats import NcStats
from ThreeDiToolbox.utils.user_messages import pop_up_info
from ThreeDiToolbox.views.tool_dialog import ToolDialogWidget


class CustomCommand(object):

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

        # All the NcStats parameters we want to calculate.
        self.parameters = NcStats.AVAILABLE_MANHOLE_PARAMETERS

        # These will be dynamically set:
        self.layer = None
        self.datasource = None

    def load_defaults(self):
        """If you only want to use run_it without show_gui, you can try calling
        this method first to set some defaults.

        This method will try to load the first datasource and the current QGIS
        layer.
        """
        try:
            self.datasource = self.ts_datasource.rows[0]
        except IndexError:
            pop_up_info("No datasource found. Aborting.", title='Error')
            return

        # Current layer information
        self.layer = self.iface.mapCanvas().currentLayer()
        if not self.layer:
            pop_up_info("No layer selected, things will not go well..",
                        title='Error')
            return

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
        filenames = []

        # MANHOLE SPECIFIC CALCULATION:
        # #############################
        # Generate data
        wos_height = dict()
        water_depth = dict()
        param_name = 's1_max'
        method = getattr(ncstats, param_name)
        # Using the getFeatures iterator should be more efficient
        for feature in self.layer.getFeatures():
            fid = feature.id()
            try:
                s1_max = method(layer_name, fid)
            except ValueError:
                s1_max = None
            # Water op straat berekening (wos_height):
            try:
                wos_height[fid] = s1_max - feature['surface_level']
            except TypeError:
                wos_height[fid] = None
            # Waterdiepte berekening:
            try:
                water_depth[fid] = s1_max - feature['bottom_level']
            except TypeError:
                water_depth[fid] = None

        # Write to csv file
        filename = layer_name + '_' + 'water_op_straat' + '.csv'
        filepath = os.path.join(result_dir, filename)
        filenames.append(filename)
        with open(filepath, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')

            header = ['id', 'wos_height', 'waterdiepte']
            writer.writerow(header)

            # TODO: ugly, can be rewritten in terms of dicts and using the
            # DictWriter
            for fid, wos in wos_height.items():
                depth = water_depth.get(fid)
                writer.writerow([fid, wos, depth])
        # ################################

        for param_name in self.parameters:
            # Generate data
            result = dict()
            wos_height = dict()
            water_depth = dict()
            method = getattr(ncstats, param_name)
            # Using the getFeatures iterator should be more efficient
            for feature in self.layer.getFeatures():
                fid = feature.id()
                try:
                    result[fid] = method(layer_name, fid)
                except ValueError:
                    result[fid] = None

            # Write to csv file
            filename = layer_name + '_' + param_name + '.csv'
            filepath = os.path.join(result_dir, filename)
            filenames.append(filename)
            with open(filepath, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')

                header = ['id', param_name]
                writer.writerow(header)

                for fid, val in result.items():
                    writer.writerow([fid, val])

        pop_up_info("Generated: %s inside: %s" %
                    (', '.join(filenames), result_dir))
