import glob
import json
import os

from netCDF4 import Dataset
import numpy as np

from ..utils.user_messages import log
from .spatialite import get_object_type, layer_qh_type_mapping


def get_id_mapping_file(netcdf_file_path):
    """An ad-hoc way to get the id_mapping file.

    We assume the id_mapping file is always in ../input_generated
    relative to the netcdf file and that it always starts with
    'id_mapping'.

    Returns: id_mapping file path
    """
    pattern = 'id_mapping*'
    inpdir = os.path.join(os.path.dirname(netcdf_file_path),
                          '..', 'input_generated')
    return glob.glob(os.path.join(inpdir, pattern))[0]


def get_channel_mapper(ds):
    """Map inp ids to flowline ids. Note that you need to subtract 1 from
    the resulting flowline id because of Python's 0-based indexing array
    (versus Fortran's 1-based indexing). These flowline ids are used for
    pipes, weirs and orifices.
    """
    cm = np.copy(ds.variables['channel_mapping'])
    cm[:, 1] = cm[:, 1] - 1  # the index transformation
    return dict(cm)


def get_timesteps(ds):
    """Timestep determination using consecutive element difference"""
    return np.ediff1d(ds.variables['time'])


class NetcdfDataSource(object):

    def __init__(self, file_path):
        """
        Args:
            file_path: path to netcdf
        """
        self.file_path = file_path
        # Load netcdf
        self.ds = Dataset(self.file_path, mode='r', format='NETCDF4')
        log("Opened netcdf: %s" % self.file_path)

        self.channel_mapper = get_channel_mapper(self.ds)

        self.id_mapping_file = get_id_mapping_file(file_path)
        # Load id mapping
        with open(self.id_mapping_file) as f:
            self.id_mapping = json.load(f)

    @property
    def metadata(self):

        pass

    def get_object_types(self, parameter=None):

        pass

    def get_objects(self, object_type):

        pass

    def get_object_count(self, object_type):

        pass

    def get_timestamps(self, object_type=None, parameter=None):
        return self.ds.variables['time'][:]

    def get_parameters(self, object_type=None, parameters=[]):
        # TODO: this whole block is ugly as sin, needs better logic for the
        # pumpstations....
        if 'pump' in object_type:
            # Pump is a special case and has its own netcdf array
            return ['q_pump']
        elif 'q_pump' in parameters:
            # Don't mutate parameters, we need to clone the list:
            new_params = list(parameters)
            new_params.pop(new_params.index('q_pump'))
            return new_params
        return parameters

    def get_object(self, object_type, object_id):

        pass

    def get_timeseries(self, object_type, object_id, parameters, start_ts=None,
                       end_ts=None):
        """Get a list of time series from netcdf.

        Note: if there are multiple parameters, all result values are just
        lumped together and returned

        Args:
            object_type: e.g. 'v2_weir'
            object_id: spatialite id?
            parameters: a list of params, e.g.: ['q', 'q_pump']

        Returns: a list of 2-tuples (time, value)
        """
        log(str(locals()))

        # Normalize the name
        _object_type = get_object_type(object_type)

        # Mapping: spatialite id -> inp id -> flowline_id
        obj_id_mapping = self.id_mapping[_object_type]
        inp_id = obj_id_mapping[str(object_id)]  # strings because: JSON
        flowline_id = self.channel_mapper[inp_id]

        _parameters = self.get_parameters(object_type, parameters)

        # Get data from all parameters and just put them in the same list:
        result = []
        for p in _parameters:
            vals = self.ds.variables[p][:, flowline_id]
            timestamps = self.get_timestamps(self.ds)
            result += zip(timestamps, vals)

        # from ..qdebug import pyqt_set_trace; pyqt_set_trace()
        return result
