import glob
import logging
import os

import numpy as np
import h5py

from threedigrid.admin.constants import NO_DATA_VALUE

from .base import BaseDataSource
from ..utils import cached_property
from .netcdf import (
    SUBGRID_MAP_VARIABLES,
    AGG_Q_TYPES,
    AGG_H_TYPES,
    Q_TYPES,
    H_TYPES,
    POSSIBLE_AGG_VARS,
    find_h5_file,
)
from ..utils.user_messages import messagebar_message
from ThreeDiToolbox.utils.patched_threedigrid import GridH5Admin
from ThreeDiToolbox.utils.patched_threedigrid import GridH5ResultAdmin
from ThreeDiToolbox.utils.patched_threedigrid import GridH5AggregateResultAdmin

# all possible var names from regular netcdf AND agg netcdf
ALL_Q_TYPES = Q_TYPES + AGG_Q_TYPES
ALL_H_TYPES = H_TYPES + AGG_H_TYPES

logger = logging.getLogger(__name__)

layer_information = [
    # object_type, model_instance, model_instance_subset, qgis_layer_source
    ("v2_connection_nodes", "nodes", "connectionnodes", "schematized"),
    ("v2_pipe_view", "lines", "pipes", "schematized"),
    ("v2_channel", "lines", "channels", "schematized"),
    ("v2_culvert_view", "lines", "culverts", "schematized"),
    ("v2_manhole_view", "nodes", "manholes", "schematized"),
    # Todo:
    # 'v2_manhole_view', 'nodes', 'manholes', 'schematized'),
    ("v2_pumpstation_view", "pumps", "pumps", "schematized"),
    ("v2_weir_view", "lines", "weirs", "schematized"),
    ("v2_orifice_view", "lines", "orifices", "schematized"),
    ("flowlines", "lines", "lines", "result"),
    ("nodes", "nodes", "nodes", "result"),
    ("pumplines", "pumps", "pumps", "result"),
    ("node_results", "nodes", "nodes", "result"),
    ("node_results_groundwater", "nodes", "nodes", "result"),
    ("line_results", "lines", "lines", "result"),
    ("line_results_groundwater", "lines", "lines", "result"),
]

object_type_model_instance = dict([(a[0], a[1]) for a in layer_information])
object_type_model_instance_subset = dict([(a[0], a[2]) for a in layer_information])
object_type_layer_source = dict([(a[0], a[3]) for a in layer_information])


def find_aggregation_netcdf_gw(netcdf_file_path):
    """An ad-hoc way to find the aggregation netcdf file for groundwater
    results.

    Args:
        netcdf_file_path: path to the result netcdf

    Returns:
        the aggregation netcdf path

    Raises:
        IndexError if nothing is found
    """
    pattern = "aggregate_results_3di.nc"
    result_dir = os.path.dirname(netcdf_file_path)
    return glob.glob(os.path.join(result_dir, pattern))[0]


class NetcdfGroundwaterDataSource(BaseDataSource):
    """NetcdfGroundwaterDatasource provides an abstraction layer to query
    result data from a 3Di simulation stored in a netcdf

    It provides an abstraction so you don't need to worry about whether the
    data is stored in the results_3di.nc or aggregate_results_3di.nc
    """

    PREFIX_1D = "Mesh1D_"
    PREFIX_2D = "Mesh2D_"
    PREFIX_1D_LENGTH = 7  # just so we don't have to recalculate
    PREFIX_2D_LENGTH = 7  # just so we don't have to recalculate

    def __init__(self, file_path=None):
        self.file_path = file_path
        self._ga = None
        self._ga_result = None
        self._ds = None
        self._cache = {}

    @property
    def ds(self):
        if self._ds is None:
            try:
                self._ds = h5py.File(self.file_path, "r")
            except IOError as e:
                logger.error(e)
                raise e
        return self._ds

    @property
    def nMesh2D_nodes(self):
        return self.gridadmin.nodes.subset("2D_ALL").count

    @property
    def nMesh1D_nodes(self):
        return self.gridadmin.nodes.subset("1D_ALL").count

    @property
    def nMesh2D_lines(self):
        return self.gridadmin.lines.subset("2D_ALL").count

    @property
    def nMesh1D_lines(self):
        return self.gridadmin.lines.subset("1D_ALL").count

    @cached_property
    def available_subgrid_map_vars(self):
        """Return a list of available variables from 'results_3di.nc'."""
        known_subgrid_map_vars = set([v.name for v in SUBGRID_MAP_VARIABLES])
        if self.gridadmin_result.has_pumpstations:
            available_vars = (
                self.gridadmin_result.nodes._field_names
                | self.gridadmin_result.lines._field_names
                | self.gridadmin_result.pumps._field_names
            )
        else:
            available_vars = (
                self.gridadmin_result.nodes._field_names
                | self.gridadmin_result.lines._field_names
            )
        # filter using a hardcoded 'whitelist'
        available_known_vars = available_vars & known_subgrid_map_vars
        return list(available_known_vars)

    @cached_property
    def available_aggregation_vars(self):
        """Return a list of available variables in the 'aggregate_results_3di.nc"""
        agg = self.gridadmin_aggregate_result
        if not agg:
            return []
        # hardcoded whitelist
        if agg.has_pumpstations:
            known_vars = set(
                list(agg.lines.Meta.composite_fields.keys())
                + list(agg.lines.Meta.subset_fields.keys())
                + list(agg.nodes.Meta.composite_fields.keys())
                + list(agg.nodes.Meta.subset_fields.keys())
                + list(agg.pumps.Meta.composite_fields.keys())
            )

            # all available fields, including hdf5 fields
            available_vars = (
                agg.nodes._field_names | agg.lines._field_names | agg.pumps._field_names
            )
        else:
            known_vars = set(
                list(agg.lines.Meta.composite_fields.keys())
                + list(agg.lines.Meta.subset_fields.keys())
                + list(agg.nodes.Meta.composite_fields.keys())
                + list(agg.nodes.Meta.subset_fields.keys())
            )

            # all available fields, including hdf5 fields
            available_vars = agg.nodes._field_names | agg.lines._field_names

        available_known_vars = available_vars & known_vars
        return list(available_known_vars)

    def get_available_variables(self):
        """Return a list of all available variables"""
        return self.available_subgrid_map_vars + self.available_aggregation_vars

    @cached_property
    def timestamps(self):
        """Return the timestamps of the 'results_3di.nc'

        All variables in the 'results_3di.nc' have the same timestamps.
        The 'aggregate_results_3di.nc' can have different number of timestamps
        for each variable.

        :return np.array containing the timestamps in seconds.
        """
        return self.get_timestamps()

    def get_timeseries(
        self, nc_variable, node_id=None, content_pk=None, fill_value=None
    ):
        """Return a time series array of the given variable

        A 2d array is given, with first column being the timestamps in seconds.
        The next columns are the values of the nodes of the given variable.
        You can also filter on a specific node using node_id or content_pk,
        in which case only the timeseries of the given node is returned.

        If there is no data of the given variable, only the timestamps are
        returned, i.e. an array of shape (n, 1) with n being the timestamps.

        :param nc_variable:
        :param node_id:
        :param content_pk:
        :param fill_value:
        :return: 2D array, first column being the timestamps
        """
        gr = self.get_gridadmin(nc_variable)

        result_filter = gr.get_model_instance_by_field_name(nc_variable).timeseries(
            indexes=slice(None)
        )
        if node_id:
            result_filter = result_filter.filter(id=node_id)
        elif content_pk:
            result_filter = result_filter.filter(content_pk=content_pk)

        data = result_filter.get_filtered_field_value(nc_variable)

        if fill_value is not None:
            data[data == NO_DATA_VALUE] = fill_value

        timestamps = self.get_timestamps(nc_variable)
        timestamps = timestamps.reshape(-1, 1)
        return np.hstack([timestamps, data])

    def get_gridadmin(self, variable=None):
        """Return the gridadmin where the variable is stored. If no variable is
        given, a gridadmin without results is returned.

        Results are either stored in the 'results_3di.nc' or the
        'aggregate_results_3di.nc'. These make use of the GridH5ResultAdmin and
        GridH5AggregateResultAdmin to query the data respectively.

        :param variable: str of the variable name, e.g. 's1', 'q_pump'
        :return: handle to GridAdminResult or AggregateGridAdminResult
        """
        if variable is None:
            return self.gridadmin
        elif variable in self.available_subgrid_map_vars:
            return self.gridadmin_result
        elif variable in self.available_aggregation_vars:
            return self.gridadmin_aggregate_result
        else:
            raise AttributeError("Parameter %s unknown")

    def _is_aggregation_parameter(self, parameter):
        """Return if the parameter is an aggregation parameter

        Aggregation parameters are variables which are stored inside the
        aggregation-result-netcdf.
        """
        return parameter in POSSIBLE_AGG_VARS

    def get_timestamps(self, parameter=None):
        """Returns an array of timestamps of the given parameter.

        The timestamps are in seconds after the simulation has started.

        All variables in the result_netcdf share the same timestamps.
        Variables of the result_aggregation_netcdf can have varying number of
        timestamps and their step size can differ.

        if no parameter is given, returns the timestamps of the result-netcdf.

        :return: (np.array)
        """
        if parameter is None or parameter in [v[0] for v in SUBGRID_MAP_VARIABLES]:
            return self.gridadmin_result.nodes.timestamps
        else:
            ga = self.get_gridadmin(variable=parameter)
            return ga.get_model_instance_by_field_name(parameter).get_timestamps(
                parameter
            )

    def get_values_by_timestep_nr_simple_no_caching(
        self, variable, timestamp_idx, node_ids=None
    ):
        """Return an array of values of the given variable on the specified timestamp(s)

        If an array of timestamps is given, a 2d numpy array is returned.
        If index is specified, only the node_ids specified in the index will
        be returned.

        :param variable: (str) variable name, e.g. 's1', 'q_pump'
        :param timestamp_idx: int or 1d numpy.array of indexes of timestamps
        :param node_ids: 1d numpy.array of node_ids
        :return: 1d/2d numpy.array
        """
        ga = self.get_gridadmin(variable)
        model = ga.get_model_instance_by_field_name(variable)

        time_slice = None
        if isinstance(timestamp_idx, int):
            time_slice = slice(timestamp_idx, timestamp_idx+1)
            time_index_filter = 0
        elif isinstance(timestamp_idx, np.ndarray):
            # ga.timeseries unfortunately does not allow for index filter on
            # aggregate results, only a slice filter. Thus we load a bit more
            # in memory and apply the index filter at the end.
            time_slice = slice(min(timestamp_idx), max(timestamp_idx) + 1)
            if len(timestamp_idx) == 1:
                time_index_filter = 0
            else:
                time_index_filter = timestamp_idx - min(timestamp_idx)
        result_filter = model.timeseries(indexes=time_slice)

        if node_ids is None:
            result_filter = result_filter.filter(id__gt=0)
        result = result_filter.get_filtered_field_value(variable)

        if node_ids is not None:
            # Unfortunately h5py/threedigrid indexing is not as fancy as
            # numpy, i.e. we can't use duplicate indexes/unsorted indexes.
            # Thus we load a bit more in memory as a numpy array and then apply
            # the final indexing with numpy.
            return result[time_index_filter][node_ids]
        else:
            return result[time_index_filter]

    def get_values_by_timestep_nr_simple(
        self, variable, timestamp_idx, node_ids=None, use_cache=True
    ):
        """Return an array of values of the given variable on the specified timestamp(s)

        If only one timestamp is specified, a 1d np.array is returned.  If an
        array of multiple timestamp_idx is given, a 2d np.array is returned.

        If node_ids is specified, only the node_ids specified in the nodes will
        be returned.

        :param variable: (str) variable name, e.g. 's1', 'q_pump'
        :param timestamp_idx: int or 1d numpy.array of indexes of timestamps
        :param node_ids: 1d numpy.array of node_ids or None in which case all
            nodes are returned.
        :param use_cache: (bool)
        :return: 1d/2d numpy.array
        """
        data = self._nc_from_mem_new(variable)
        if isinstance(timestamp_idx, int):
            timestamp_idx = np.array([timestamp_idx])

        if node_ids is None:
            filter_data = data[timestamp_idx]
        else:
            filter_data = data[timestamp_idx][:, node_ids]

        if len(timestamp_idx) == 1:
            return filter_data[0]
        else:
            return filter_data

    def get_values_by_timestep_nr(
        self, variable, timestamp_idx, index=None, use_cache=True
    ):
        """

        :param variable:
        :param timestamp_idx:
        :param index:
        :param use_cache:
        :return:
        """
        result = self.get_values_by_timestep_nr_simple(
            variable, timestamp_idx, index)
        return result

    def _nc_from_mem_new(self, variable, use_cache=True):
        """Return 2d numpy array with all values of variable and cache it.

        Everyting of the variables is cached, both in time and space, i.e. all
        timesteps and all nodes of the variable.

        TODO: Saving the variables in cache is currently necessary to limit
        the amount of (slow) IO with the netcdf results. However, this also
        causes much unnecessary data to be stored in memory. This can become
        problematic with large result files.

        :param variable: (str) variable name, e.g. 's1', 'q_pump'
        :param use_cache: bool
        :return: 2d numpy array
        """
        if variable in self._cache and use_cache:
            data = self._cache[variable]
        else:
            logger.debug(
                "Variable %s not yet in cache, fetching from result files" % variable)
            ga = self.get_gridadmin(variable)
            model = ga.get_model_instance_by_field_name(variable)
            time_filter = model.timeseries(indexes=slice(None))
            data = time_filter.get_filtered_field_value(variable)
            self._cache[variable] = data
        return data

    def _nc_from_mem(self, ds, variable, use_cache=True):
        """Get netcdf data from memory if needed."""
        if use_cache:
            try:
                data = self._cache[variable]
            except KeyError:
                # Keep the whole netCDF array for a variable in memory for
                # performance
                data = ds.get(variable)[:]
                self._cache[variable] = data
        else:
            # this returns a netCDF Variable, which behaves like a np array
            data = ds.get(variable)
        return data

    def temp_get_values_by_timestep_nr_impl(
        self, variable, timestamp_idx, index=None, use_cache=True
    ):
        var_2d = self.PREFIX_2D + variable
        var_1d = self.PREFIX_1D + variable

        # determine if it's an agg var
        if variable in self.available_subgrid_map_vars:
            ds = self.ds
        elif variable in self.available_aggregation_vars:
            ds = self.ds_aggregation
        else:
            logger.error("Unsupported variable %s", variable)
            raise ValueError(variable)

        # determine appropriate fill value from netCDF
        if var_2d in ds.keys():
            fill_value_2d = ds.get(var_2d).fillvalue
            fill_value = fill_value_2d
        if var_1d in ds.keys():
            fill_value_1d = ds.get(var_1d).fillvalue
            fill_value = fill_value_1d

        if var_2d in ds.keys() and var_1d in ds.keys():
            assert (
                fill_value_1d == fill_value_2d
            ), "Difference in fill value, can't consolidate"

        if index is None:
            if variable.startswith("q_pump"):
                return self._nc_from_mem(ds, var_1d, use_cache)[timestamp_idx, :]
            elif variable in ALL_Q_TYPES:
                n2d = self.nMesh2D_lines
                n1d = self.nMesh1D_lines
            elif variable in ALL_H_TYPES:
                n2d = self.nMesh2D_nodes
                n1d = self.nMesh1D_nodes
            else:
                raise ValueError(variable)

            # Note: it's possible to only have 2D or 1D
            if var_2d in ds.keys():
                a2d = self._nc_from_mem(ds, var_2d, use_cache)[timestamp_idx, :]
            else:
                a2d = np.ma.masked_all(n2d)

            if var_1d in ds.keys():
                a1d = self._nc_from_mem(ds, var_1d, use_cache)[timestamp_idx, :]
            else:
                a1d = np.ma.masked_all(n1d)

            assert var_2d in ds.keys() or var_1d in ds.keys(), "No 2D and 1D?"

            # Note: order is: 2D, then 1D
            res = np.ma.hstack([a2d, a1d])
        else:
            # in the groundwater version, the node index starts from 1 instead
            # of 0.
            # Note: a new array is created, e.g., index doesn't get modified
            index = index - 1  # copies the array

            # hacky object_type checking mechanism, sinds we don't have
            # that information readily available
            if variable.startswith("q_pump"):
                return self._nc_from_mem(ds, var_1d, use_cache)[timestamp_idx, index]
            elif variable in ALL_Q_TYPES:
                threshold = self.nMesh2D_lines
            elif variable in ALL_H_TYPES:
                threshold = self.nMesh2D_nodes
            else:
                raise ValueError(variable)
            # find indices of 2d and 1d components
            idx_2d = np.where(index < threshold)[0]
            idx_1d = np.where(index >= threshold)[0]
            # make index arrays that can be used on the nc variables
            iarr_2d = index[idx_2d]
            iarr_1d = index[idx_1d] - threshold
            res = np.ma.zeros(index.shape, fill_value=fill_value)
            # Note sure if a netCDF bug or a known difference in behavior.
            # Indexing a numpy array using [], or np.array([], dtype=int)
            # works, but on a netCDF Variable it doesn't. Therefore we must
            # explicitly check if the list is empty.
            if iarr_2d.size > 0:
                res[idx_2d] = self._nc_from_mem(ds, var_2d, use_cache)[
                    timestamp_idx, iarr_2d
                ]
            if iarr_1d.size > 0:
                res[idx_1d] = self._nc_from_mem(ds, var_1d, use_cache)[
                    timestamp_idx, iarr_1d
                ]
        # note: res is a masked array
        return res

    @property
    def gridadmin(self):
        if not self._ga:
            h5 = find_h5_file(self.file_path)
            self._ga = GridH5Admin(h5)
        return self._ga

    @property
    def gridadmin_result(self):
        if not self._ga_result:
            h5 = find_h5_file(self.file_path)
            self._ga_result = GridH5ResultAdmin(h5, self.file_path)
        return self._ga_result

    @cached_property
    def gridadmin_aggregate_result(self):
        try:
            agg_path = find_aggregation_netcdf_gw(self.file_path)
            h5 = find_h5_file(self.file_path)
            return GridH5AggregateResultAdmin(h5, agg_path)
        except IndexError:
            return None

    @cached_property
    def ds_aggregation(self):
        """The aggregation netcdf dataset."""
        # Note: we don't want module level imports of dynamically loaded
        # libraries because importing them will cause files to be held open
        # which cause trouble when updating the plugin. Therefore we delay
        # the import as much as possible.

        # Load aggregation netcdf
        try:
            aggregation_netcdf_file = find_aggregation_netcdf_gw(self.file_path)
        except IndexError:
            logger.error("Could not find the aggregation netcdf.")
            return None
        else:
            logger.info("Opening aggregation netcdf: %s" % aggregation_netcdf_file)
            return h5py.File(aggregation_netcdf_file, mode="r")
