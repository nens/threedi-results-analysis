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
        self.nMesh2D_nodes = self.ds.dimensions['nMesh2D_nodes'].size
        self.nMesh1D_nodes = self.ds.dimensions['nMesh1D_nodes'].size
        self.nMesh2D_lines = self.ds.dimensions['nMesh2D_lines'].size
        self.nMesh1D_lines = self.ds.dimensions['nMesh1D_lines'].size

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
        known_subgrid_map_vars = set([v.name for v in SUBGRID_MAP_VARIABLES])
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

    def get_available_variables(self):
        return self.available_subgrid_map_vars

    def node_type_of(self, node_idx):
        pass

    def line_type_of(self, line_idx):
        pass

    @cached_property
    def timestamps(self):
        return self.get_timestamps()

    def get_timeseries(
            self, object_type, object_id, nc_variable, fill_value=None):
        return self.temporary_get_timeseries_impl(
            object_type, object_id, nc_variable, fill_value)

    def temporary_get_timeseries_impl(
            self, object_type, object_id, nc_variable, fill_value=None):
        # TODO: this is a crappy but working implementation, replace it by a
        # better one in the future (e.g. using threedigrid)!
        import numpy as np
        if object_type in ['nodes', 'flowlines', 'pumplines']:
            object_id -= 1
        if object_type == 'nodes':
            if object_id < self.nMesh2D_nodes:
                # it's 2d
                nc_variable = self.PREFIX_2D + nc_variable
                netcdf_id = object_id
            else:
                # it's 1d
                nc_variable = self.PREFIX_1D + nc_variable
                netcdf_id = object_id - self.nMesh2D_nodes
        elif object_type == 'flowlines':
            if object_id < self.nMesh2D_lines:
                # it's 2d
                nc_variable = self.PREFIX_2D + nc_variable
                netcdf_id = object_id
            else:
                # it's 1d
                nc_variable = self.PREFIX_1D + nc_variable
                netcdf_id = object_id - self.nMesh2D_lines
        elif object_type == 'pumplines':
            nc_variable = self.PREFIX_1D + nc_variable
            netcdf_id = object_id
        else:
            raise NotImplementedError("TODO")

        vals = self.ds.variables[nc_variable][:, netcdf_id]

        # Zip timeseries together in (n,2) array
        if fill_value is not None and type(vals) == np.ma.core.MaskedArray:
            vals = vals.filled(fill_value)
        return np.vstack((self.timestamps, vals)).T

    def get_timestamps(self, object_type=None, parameter=None):
        # TODO: use cached property to limit file access
        return self.ds.variables['time'][:]

    # used in map_animator
    def get_values_by_timestep_nr(self, variable, timestamp_idx, index=None):
        return self.temp_get_values_by_timestep_nr_impl(
            variable, timestamp_idx, index)

    def temp_get_values_by_timestep_nr_impl(
            self, variable, timestamp_idx, index=None):
        import numpy as np
        from .netcdf import Q_TYPES, H_TYPES
        var_2d = self.PREFIX_2D + variable
        var_1d = self.PREFIX_1D + variable

        if index is not None:
            # a new array is created, thus safe
            index = index - 1

            # hacky object_type checking mechanism, sinds we don't have
            # that information readily available
            if variable == 'q_pump':
                return self.ds.variables[var_1d][timestamp_idx, index]
            elif variable in Q_TYPES:
                threshold = self.nMesh2D_lines
            elif variable in H_TYPES:
                threshold = self.nMesh2D_nodes
            else:
                raise ValueError(variable)
            # find indices of 2d and 1d components
            idx_2d = np.where(index < threshold)[0]
            idx_1d = np.where(index >= threshold)[0]
            # make index arrays that can be used on the nc variables
            iarr_2d = index[idx_2d]
            iarr_1d = index[idx_1d] - threshold
            res = np.zeros(index.shape)
            # Note sure if a netCDF bug or a known difference in behavior.
            # Indexing a numpy array using [], or np.array([], dtype=int)
            # works, but on a netCDF Variable it doesn't. Therefore we must
            # explicitly check if the list is empty.
            if iarr_2d.size > 0:
                res[idx_2d] = self.ds.variables[var_2d][timestamp_idx, iarr_2d]
            if iarr_1d.size > 0:
                res[idx_1d] = self.ds.variables[var_1d][timestamp_idx, iarr_1d]
            return res
        else:
            if variable == 'q_pump':
                return self.ds.variables[var_1d][timestamp_idx, index]
            # TODO: pumps won't work
            vals_2d = self.ds.variables[var_2d][timestamp_idx, :]
            vals_1d = self.ds.variables[var_1d][timestamp_idx, :]
            # order is: 2D, then 1D
            return np.hstack((vals_2d, vals_1d))

    @property
    def gridadmin(self):
        if not self._ga:
            import os
            from ..utils.patched_threedigrid import GridH5Admin
            d = os.path.dirname(self.file_path)
            f = os.path.join(d, 'gridadmin.h5')
            self._ga = GridH5Admin(f)

        return self._ga
