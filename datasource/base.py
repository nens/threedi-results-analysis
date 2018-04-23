from abc import (
    ABCMeta,
    abstractmethod,
    abstractproperty,
)


class BaseDataSource(object):
    # NOTE: methods used in ncstats methods are ignored for now to keep
    # things more manageable....
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractproperty
    def available_subgrid_map_vars(self):
        pass

    @abstractproperty
    def available_aggregation_vars(self):
        pass

    @abstractmethod
    def node_type_of(self, node_idx):
        pass

    @abstractmethod
    def line_type_of(self, line_idx):
        pass

    @abstractmethod
    def get_timeseries(
            self, object_type, object_id, nc_variable, fill_value=None):
        pass

    @abstractmethod
    def get_timestamps(self, object_type=None, parameter=None):
        pass

    # used in map_animator
    @abstractmethod
    def get_values_by_timestep_nr(self, variable, timestamp_idx, index=None):
        pass

    # TODO: not sure if needed, used in creating layers
    # @abstractmethod
    # def channel_mapping(self):
    #     pass

    # TODO: not sure if needed, used in creating layer
    # @abstractmethod
    # def node_mapping(self):
    #     pass

    # TODO: used in creating layer in NetcdfDataSource, but should be
    # refactored out because the new DataSource uses hdf5
    # @abstractmethod
    # def id_mapping(self):
    #     pass
