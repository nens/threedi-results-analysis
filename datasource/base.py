from abc import ABCMeta
from abc import abstractmethod


class BaseDataSource(metaclass=ABCMeta):
    # NOTE: methods used in ncstats methods are ignored for now to keep
    # things more manageable....
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def available_subgrid_map_vars(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def available_aggregation_vars(self):
        pass  # pragma: no cover

    @abstractmethod
    def get_timeseries(self, object_type, object_id, nc_variable, fill_value=None):
        pass  # pragma: no cover

    @abstractmethod
    def get_timestamps(self, parameter=None):
        pass  # pragma: no cover

    # used in map_animator
    @abstractmethod
    def get_values_by_timestep_nr(self, variable, timestamp_idx, index=None):
        pass  # pragma: no cover
