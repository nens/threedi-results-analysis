from .base import BaseDataSource
from .result_constants import LAYER_OBJECT_TYPE_MAPPING
from .result_constants import SUBGRID_MAP_VARIABLES
from cached_property import cached_property
from threedigrid.admin.constants import NO_DATA_VALUE
from ThreeDiToolbox.utils.patched_threedigrid import GridH5Admin
from ThreeDiToolbox.utils.patched_threedigrid import GridH5AggregateResultAdmin
from ThreeDiToolbox.utils.patched_threedigrid import GridH5ResultAdmin

import glob
import h5py
import logging
import numpy as np
import os


logger = logging.getLogger(__name__)


def normalized_object_type(current_layer_name):
    """Get a normalized object type for internal purposes."""
    if current_layer_name in LAYER_OBJECT_TYPE_MAPPING:
        return LAYER_OBJECT_TYPE_MAPPING[current_layer_name]
    else:
        msg = "Unsupported layer: %s." % current_layer_name
        logger.warning(msg)
        return None


class ThreediResult(BaseDataSource):
    """Provides access to result data of a 3Di simulation

    Result data of 3di is stored in netcdf4. Two types of result data
    exists: normal results and aggregated results. Usually the files are named
    'results_3di.nc' and 'aggregate_results_3di.nc' respectively.

    This class allows access to the results via threedigrid:
        -  GridH5ResultAdmin
        - GridH5AggregateResultAdmin
    For more information about threedigrid see https://threedigrid.readthedocs.io/en/latest/

    Some helper methods are available query the result data using a variable
    name (example of variable names: 's1', 'q_cum', 'vol', etc)

    This class also provides for direct access to the data files via h5py.
    However, it is recommended to use threedigrid instead.
    """

    def __init__(self, file_path=None):
        self.file_path = file_path
        self._cache = {}

    @cached_property
    def available_subgrid_map_vars(self):
        """Return a list of available variables from 'results_3di.nc'."""
        known_subgrid_map_vars = set([v.name for v in SUBGRID_MAP_VARIABLES])
        if self.result_admin.has_pumpstations:
            available_vars = (
                self.result_admin.nodes._field_names
                | self.result_admin.lines._field_names
                | self.result_admin.pumps._field_names
            )
        else:
            available_vars = (
                self.result_admin.nodes._field_names
                | self.result_admin.lines._field_names
            )
        # filter using a hardcoded 'whitelist'
        available_known_vars = available_vars & known_subgrid_map_vars
        return list(available_known_vars)

    @cached_property
    def available_aggregation_vars(self):
        """Return a list of available variables in the 'aggregate_results_3di.nc"""
        ga = self.aggregate_result_admin
        if not ga:
            return []
        # hardcoded whitelist
        whitelist_vars = set(
            list(ga.lines.Meta.composite_fields.keys())
            + list(ga.lines.Meta.subset_fields.keys())
            + list(ga.nodes.Meta.composite_fields.keys())
            + list(ga.nodes.Meta.subset_fields.keys())
        )
        if ga.has_pumpstations:
            whitelist_vars |= set(list(ga.pumps.Meta.composite_fields.keys()))

        # all available fields, including hdf5 fields
        available_vars = ga.nodes._field_names | ga.lines._field_names
        if ga.has_pumpstations:
            available_vars |= ga.pumps._field_names

        available_aggregation_vars = available_vars & whitelist_vars
        return list(available_aggregation_vars)

    @property
    def available_vars(self):
        """Return a list of all available variables"""
        return self.available_subgrid_map_vars + self.available_aggregation_vars

    @cached_property
    def timestamps(self):
        """Return the timestamps of the 'results_3di.nc'

        All variables in the 'results_3di.nc' have the same timestamps.
        The 'aggregate_results_3di.nc' can have different number of timestamps
        for each variable.

        :return 1d np.array containing the timestamps in seconds.
        """
        return self.get_timestamps()

    def get_timestamps(self, parameter=None):
        """Return an array of timestamps for the given parameter

        The timestamps are in seconds after the start of the simulation.

        All variables in the result_netcdf share the same timestamps.
        Variables of the result_aggregation_netcdf can have varying number of
        timestamps and their step size can differ.

        If no parameter is given, returns the timestamps of the result-netcdf.

        :return: 1d np.array
        """
        # TODO: the property self.timestamps is cached but this method is not.
        #  This might cause performance issues. Check if these timestamps are
        #  often queried and cause performance issues.
        if parameter is None or parameter in [v[0] for v in SUBGRID_MAP_VARIABLES]:
            return self.result_admin.nodes.timestamps
        else:
            ga = self.get_gridadmin(variable=parameter)
            return ga.get_model_instance_by_field_name(parameter).get_timestamps(
                parameter
            )

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
            return self.result_admin
        elif variable in self.available_aggregation_vars:
            return self.aggregate_result_admin
        else:
            raise AttributeError("Unknown subgrid or aggregate variable: %s")

    def get_timeseries(
        self, nc_variable, node_id=None, content_pk=None, fill_value=None
    ):
        """Return a time series array of the given variable

        A 2d array is given, with first column being the timestamps in seconds.
        The next columns are the values of the nodes of the given variable.
        You can also filter on a specific node using node_id or content_pk,
        in which case only the timeseries of the given node is returned.

        If there is no values of the given variable, only the timestamps are
        returned, i.e. an array of shape (n, 1) with n being the timestamps.

        :param nc_variable:
        :param node_id:
        :param content_pk:
        :param fill_value:
        :return: 2D array, first column being the timestamps
        """
        ga = self.get_gridadmin(nc_variable)

        filtered_result = ga.get_model_instance_by_field_name(nc_variable).timeseries(
            indexes=slice(None)
        )
        if node_id:
            filtered_result = filtered_result.filter(id=node_id)
        elif content_pk:
            filtered_result = filtered_result.filter(content_pk=content_pk)

        values = filtered_result.get_filtered_field_value(nc_variable)

        if fill_value is not None:
            values[values == NO_DATA_VALUE] = fill_value

        timestamps = self.get_timestamps(nc_variable)
        timestamps = timestamps.reshape(-1, 1)  # reshape (n,) to (n, 1)
        return np.hstack([timestamps, values])

    # This method is similar as get_values_by_timestep_nr but does not cache
    # values. Moreover, it tries to only query the minimum needed data needed.
    # def get_values_by_timestep_nr_no_caching(
    #     self, variable, timestamp_idx, node_ids=None
    # ):
    #     """Return an array of values of the given variable on the specified timestamp(s)
    #
    #     If an array of timestamps is given, a 2d numpy array is returned.
    #     If index is specified, only the node_ids specified in the index will
    #     be returned.
    #
    #     :param variable: (str) variable name, e.g. 's1', 'q_pump'
    #     :param timestamp_idx: int or 1d numpy.array of indexes of timestamps
    #     :param node_ids: 1d numpy.array of node_ids
    #     :return: 1d/2d numpy.array
    #     """
    #     ga = self.get_gridadmin(variable)
    #     model = ga.get_model_instance_by_field_name(variable)
    #
    #     time_slice = None
    #     if isinstance(timestamp_idx, int):
    #         time_slice = slice(timestamp_idx, timestamp_idx+1)
    #         time_index_filter = 0
    #     elif isinstance(timestamp_idx, np.ndarray):
    #         # ga.timeseries unfortunately does not allow for index filter on
    #         # aggregate results, only a slice filter. Thus we load a bit more
    #         # in memory and apply the index filter at the end.
    #         time_slice = slice(min(timestamp_idx), max(timestamp_idx) + 1)
    #         if len(timestamp_idx) == 1:
    #             time_index_filter = 0
    #         else:
    #             time_index_filter = timestamp_idx - min(timestamp_idx)
    #     result_filter = model.timeseries(indexes=time_slice)
    #
    #     if node_ids is None:
    #         result_filter = result_filter.filter(id__gt=0)
    #     result = result_filter.get_filtered_field_value(variable)
    #
    #     if node_ids is not None:
    #         # Unfortunately h5py/threedigrid indexing is not as fancy as
    #         # numpy, i.e. we can't use duplicate indexes/unsorted indexes.
    #         # Thus we load a bit more in memory as a numpy array and then apply
    #         # the final indexing with numpy.
    #         return result[time_index_filter][node_ids]
    #     else:
    #         return result[time_index_filter]

    def get_values_by_timestep_nr(
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
        values = self._nc_from_mem(variable)
        if isinstance(timestamp_idx, int):
            timestamp_idx = np.array([timestamp_idx])

        if node_ids is None:
            # The first element is a trash element which we don't want to return
            filtered_data = values[timestamp_idx, 1:]
        else:
            # node_ids should never be 0 thus the trash element gets filtered out.
            filtered_data = values[timestamp_idx][:, node_ids]

        if len(timestamp_idx) == 1:
            # if only one timestamp is specified, an 1d array is returned
            return filtered_data[0]
        else:
            return filtered_data

    def _nc_from_mem(self, variable):
        """Return 2d numpy array with all values of variable and cache it.

        Everyting of the variables is cached, both in time and space, i.e. all
        timesteps and all nodes of the variable.

        TODO: Saving the variables in cache is currently necessary to limit
         the amount of (slow) IO with the netcdf results. However, this also
         causes many unnecessary values to be stored in memory. This can become
         problematic with large result files.

        TODO: replace by a @lru_cache?
        https://docs.python.org/3/library/functools.html#functools.lru_cache

        :param variable: (str) variable name, e.g. 's1', 'q_pump'
        :param use_cache: bool
        :return: 2d numpy array
        """
        if variable in self._cache:
            values = self._cache[variable]
        else:
            logger.debug(
                "Variable %s not yet in cache, fetching from result file", variable
            )
            ga = self.get_gridadmin(variable)
            model_instance = ga.get_model_instance_by_field_name(variable)
            unfiltered_timeseries = model_instance.timeseries(indexes=slice(None))
            values = unfiltered_timeseries.get_filtered_field_value(variable)
            logger.debug(
                "Caching additional {:.3f} MB of data".format(
                    values.nbytes / 1000 / 1000
                )
            )
            self._cache[variable] = values
        return values

    @cached_property
    def gridadmin(self):
        h5 = find_h5_file(self.file_path)
        return GridH5Admin(h5)

    @cached_property
    def result_admin(self):
        h5 = find_h5_file(self.file_path)
        # TODO: there's no FileNotFound try/except here like for
        # aggregates. Richard says that a missing regular result file is just
        # as likely.
        return GridH5ResultAdmin(h5, self.file_path)

    @cached_property
    def aggregate_result_admin(self):
        try:
            # Note: both of these might raise the FileNotFoundError
            agg_path = find_aggregation_netcdf(self.file_path)
            h5 = find_h5_file(self.file_path)
        except FileNotFoundError:
            logger.exception("Aggregate result not found")
            return None
        return GridH5AggregateResultAdmin(h5, agg_path)

    @cached_property
    def datasource(self):
        try:
            return h5py.File(self.file_path, "r")
        except IOError:
            logger.exception("Datasource %s could not be opened", self.file_path)
            raise

    @cached_property
    def ds_aggregation(self):
        """The aggregation netcdf dataset."""
        # Note: we don't want module level imports of dynamically loaded
        # libraries because importing them will cause files to be held open
        # which cause trouble when updating the plugin. Therefore we delay
        # the import as much as possible.

        # Load aggregation netcdf
        try:
            aggregation_netcdf_file = find_aggregation_netcdf(self.file_path)
        except FileNotFoundError:
            logger.error("Could not find the aggregation netcdf.")
            return None
        else:
            logger.info("Opening aggregation netcdf: %s" % aggregation_netcdf_file)
            return h5py.File(aggregation_netcdf_file, mode="r")


def find_h5_file(netcdf_file_path):
    """An ad-hoc way to get the h5_file.

    We assume the h5_file file is in one of the following locations (note:
    this order is also the searching order):

    1) . (in the same dir as the netcdf)
    2) ../preprocessed

    relative to the netcdf file and has extension '.h5'

    Args:
        netcdf_file_path: path to the result netcdf

    Returns:
        h5_file path

    Raises:
        FileNotFoundError if no file can be found
    """
    pattern = "*.h5"
    result_dir = os.path.dirname(netcdf_file_path)
    inpdir = os.path.join(result_dir, os.path.pardir, "preprocessed")

    for directory in [result_dir, inpdir]:
        h5_files = glob.glob(os.path.join(directory, pattern))
        if h5_files:
            return h5_files[0]
    raise FileNotFoundError("'.h5' file not found relative to %s." % result_dir)


def find_aggregation_netcdf(netcdf_file_path):
    """An ad-hoc way to find the aggregation netcdf file

    Args:
        netcdf_file_path: path to the result netcdf

    Returns:
        the aggregation netcdf path

    Raises:
        FileNotFoundError if nothing is found
    """
    pattern = "aggregate_results_3di.nc"
    result_dir = os.path.dirname(netcdf_file_path)
    aggregate_result_files = glob.glob(os.path.join(result_dir, pattern))
    if aggregate_result_files:
        return aggregate_result_files[0]
    raise FileNotFoundError(
        "'aggregate_results_3di.nc' file not found relative to %s" % result_dir
    )


def detect_netcdf_version(netcdf_file_path):
    """An ad-hoc way to detect whether we work with
    1. or an regular netcdf: one that has been made with on "old" calculation
    core (without groundater). This netcdf does not include an attribute
    'threedicore_version'
    2. or an groundwater netcdf: one that has been made with on "new"
    calculation core (with optional groundater calculations). This netcdf
    does include an attribute 'threedicore_version'

    Args:
        netcdf_file_path: path to the result netcdf

    Returns:
        the version (a string) of the netcdf
            - 'netcdf'
            - 'netcdf-groundwater'

    """
    try:
        dataset = h5py.File(netcdf_file_path, mode="r")
        if "threedicore_version" in dataset.attrs:
            return "netcdf-groundwater"
        else:
            return "netcdf"
    except IOError:
        # old 3Di results cannot be opened with h5py. The can be opened with
        # NetCDF4 Dataset (dataset.file_format = NETCDF3_CLASSIC). If you open
        # a new 3Di result with NetCDF4 you get dataset.file_format = NETCDF4
        return "netcdf"
