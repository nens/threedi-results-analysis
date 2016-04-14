import inspect

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


    def run_it(self):
        print(self.args)
        print(self.kwargs)
        print(self._fields)
        print("We ran the script!")


        # For now just get the first datasource
        # TODO: improve this
        tds = self.ts_datasources.rows[0]
        nds = tds.datasource()  # the netcdf datasource

        # from ThreeDiToolbox.qdebug import pyqt_set_trace; pyqt_set_trace()

