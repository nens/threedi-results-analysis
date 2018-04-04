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
    PREFIX_1D = 'Mesh1D_'
    PREFIX_2D = 'Mesh2D_'
    PREFIX_1D_LENGTH = 7  # just so we don't have to recalculate
    PREFIX_2D_LENGTH = 7  # just so we don't have to recalculate

    def __init__(self, file_path=None, *args, **kwargs):
        from netCDF4 import Dataset
        self.file_path = file_path
        self._ga = None
        self.ds = Dataset(file_path)

    def _strip_prefix(self, var_name):
        """Strip away netCDF variable name prefixes.

        Example variable names: 'Mesh2D_s1', 'Mesh1D_s1'

        >>> from ThreeDiToolbox.datasource.base import DummyDataSource
        >>> ds = DummyDataSource()
        >>> ds._strip_prefix('Mesh2D_s1')
        's1'
        >>> ds._strip_prefix('Mesh1D_q')
        'q'
        >>> ds._strip_prefix('iets_anders')
        'iets_anders'
        """
        if var_name.startswith(self.PREFIX_1D):
            return var_name[self.PREFIX_1D_LENGTH:]
        elif var_name.startswith(self.PREFIX_2D):
            return var_name[self.PREFIX_2D_LENGTH:]
        else:
            return var_name

    @cached_property
    def available_subgrid_map_vars(self):
        """Available variables from 'subgrid_map.nc'."""
        from .netcdf import SUBGRID_MAP_VARIABLES
        known_subgrid_map_vars = set([v for v, _, _ in SUBGRID_MAP_VARIABLES])
        raw_available_vars = [
            v for v in self.ds.variables.keys() if
            v.startswith(self.PREFIX_1D) or v.startswith(self.PREFIX_2D)]
        # Convert to a set to (1) get rid of duplicate variable names, and (2)
        # to intersect with known variables
        available_vars = set(
            [self._strip_prefix(v) for v in raw_available_vars])
        # filter using a hardcoded 'whitelist'
        available_known_vars = available_vars.intersection(
            known_subgrid_map_vars)
        return list(available_known_vars)

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
        # TODO: use cached property to limit file access
        return self.ds.variables['time'][:]

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
