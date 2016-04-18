"""This script calculates statistics on the current layer and outputs it to
csv.
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
        self.feature_ids = [i.id() for i in self.current_layer.getFeatures()]

        # The NcStats parameter we want to calculate
        self.PARAMETER = 'tot_vol'  # TODO: still hardcoded for now


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

        # Generate data
        result = dict()
        param_name = self.PARAMETER
        method = getattr(ncstats, param_name)
        for fid in self.feature_ids:
            result[fid] = method(layer_name, fid)

        # Write to csv file
        filename = layer_name + '_' + param_name + '.csv'
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')

            header = ['id', param_name]
            writer.writerow(header)

            for fid, val in result.items():
                writer.writerow([fid, val])

        pop_up_info("Generated %s" % filename)
