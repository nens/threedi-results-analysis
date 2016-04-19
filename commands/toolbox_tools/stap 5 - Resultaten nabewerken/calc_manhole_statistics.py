"""This script calculates statistics on the current layer for structures and
outputs it to csv.
"""

import csv
import inspect

from ThreeDiToolbox.stats.ncstats import NcStats
from ThreeDiToolbox.utils.user_messages import pop_up_info

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
        self.ts_datasources = kwargs.get('ts_datasource')

        # Current layer information
        self.current_layer = self.iface.mapCanvas().currentLayer()
        if not self.current_layer:
            pop_up_info("No layer selected, things will not go well..",
                        title='Error')
            return

        # All the NcStats parameters we want to calculate.
        self.parameters = NcStats.AVAILABLE_MANHOLE_PARAMETERS


    def run_it(self):
        print(self.args)
        print(self.kwargs)
        print(self._fields)
        print("We ran the script!")


        # For now just get the first datasource
        # TODO: improve this
        if len(self.ts_datasources.rows) <= 0:
            pop_up_info("No datasource found. Aborting.", title='Error')
            return
        if len(self.ts_datasources.rows) > 1:
            pop_up_info("More than one datasource found, only the first one "
                        "will be used", title='Warning')
        tds = self.ts_datasources.rows[0]
        nds = tds.datasource()  # the netcdf datasource
        ncstats = NcStats(datasource=nds)
        layer_name = self.current_layer.name()
        filenames = []

        # MANHOLE SPECIFIC CALCULATION:
        # #############################
        # Generate data
        wos_height = dict()
        water_depth = dict()
        param_name = 's1_max'
        method = getattr(ncstats, param_name)
        # Using the getFeatures iterator should be more efficient
        for feature in self.current_layer.getFeatures():
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
        filenames.append(filename)
        with open(filename, 'wb') as csvfile:
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
            for feature in self.current_layer.getFeatures():
                fid = feature.id()
                try:
                    result[fid] = method(layer_name, fid)
                except ValueError:
                    result[fid] = None

            # Write to csv file
            filename = layer_name + '_' + param_name + '.csv'
            filenames.append(filename)
            with open(filename, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')

                header = ['id', param_name]
                writer.writerow(header)

                for fid, val in result.items():
                    writer.writerow([fid, val])

        pop_up_info("Generated: %s" % ', '.join(filenames))
