




class TdiDatasourceManager(object):

    def __init__(self, spatialite_datasource, netcdf_datasources=[]):

        #test and set spatialite_datasource



        pass


    @property
    def metadata(self):

        pass


    def add_netcdf_datasource(self):

        pass

    def remove_netcdf_datasource(self):

        pass


    def use_spatialite_results(self, active=True):

        pass


    def get_object_types(self, parameter=None):

        pass

    def get_objects(self, object_type=None, filter=None):

        pass


    def get_object_count(self, object_type=None, filter=None):

        pass


    def get_parameters(self, object_type=None):

        pass

    def get_timestamps(self, object_type=None, parameter=None):

        pass

    def get_timestamp_count(self, object_type=None, parameter=None):

        pass

    def get_object(self, object_type, object_id):

        pass


    def get_timeseries(self, object_type, object_id, parameter, start_ts=None, end_ts=None):

        pass


    def get_ts_timeserie_source(self, nr):

        pass

