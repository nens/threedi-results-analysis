"""This script calculates statistics on the current layer and outputs it to
csv.
"""

import csv
import inspect
from ThreeDiToolbox.stats.ncstats import NcStats

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
        self.PARAMTER = 'tot_vol'  # TODO: still hardcoded for now


    def run_it(self):
        print(self.args)
        print(self.kwargs)
        print(self._fields)
        print("We ran the script!")


        # For now just get the first datasource
        # TODO: improve this
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
        with open(layer_name + '_' + param_name + '.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')

            header = ['id', param_name]
            writer.writerow(header)

            for fid, val in result.items():
                writer.writerow([fid, val])
