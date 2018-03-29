from abc import (
    ABCMeta,
    abstractmethod,
    abstractproperty,
)

from ..utils import cached_property


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


class DummyDataSource(BaseDataSource):
    def __init__(self, file_path=None, *args, **kwargs):
        self.file_path = file_path
        self._ga = None

    @cached_property
    def available_subgrid_map_vars(self):
        return []

    @cached_property
    def available_aggregation_vars(self):
        return []

    def node_type_of(self, node_idx):
        pass

    def line_type_of(self, line_idx):
        pass

    def get_timeseries(
            self, object_type, object_id, nc_variable, fill_value=None):
        pass

    def get_timestamps(self, object_type=None, parameter=None):
        return range(10)

    # used in map_animator
    def get_values_by_timestep_nr(self, variable, timestamp_idx, index=None):
        pass

    @property
    def gridadmin(self):
        if not self._ga:
            import os
            from threedigrid.admin.gridadmin import GridH5Admin
            d = os.path.dirname(self.file_path)
            f = os.path.join(d, 'gridadmin.h5')
            self._ga = GridH5Admin(f)

        return self._ga
