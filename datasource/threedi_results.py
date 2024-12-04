from functools import cached_property
from threedi_results_analysis.datasource.result_constants import (
    ACTION_TYPE_ATTRIBUTE_MAP,
)
from threedi_results_analysis.datasource.result_constants import (
    LAYER_OBJECT_TYPE_MAPPING,
)
from threedi_results_analysis.datasource.result_constants import SUBGRID_MAP_VARIABLES
from threedigrid.admin.constants import NO_DATA_VALUE
from threedigrid.admin.gridadmin import GridH5Admin
from threedigrid.admin.gridresultadmin import GridH5AggregateResultAdmin
from threedigrid.admin.gridresultadmin import GridH5ResultAdmin
from threedigrid.admin.gridresultadmin import GridH5StructureControl
from threedigrid.admin.gridresultadmin import GridH5WaterQualityResultAdmin
from threedigrid.admin.structure_controls.models import StructureControlSourceTypes
from threedigrid.admin.structure_controls.models import StructureControlTypes

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
        return None


class ThreediResult():
    """Provides access to result data of a 3Di simulation

    Result data of 3di is stored in netcdf4. Two types of result data
    exists: normal results and aggregated results. Usually the files are named
    'results_3di.nc' and 'aggregate_results_3di.nc' respectively.

    This class allows access to the results via threedigrid:

    - GridH5ResultAdmin
    - GridH5AggregateResultAdmin
    - GridH5WaterQualityResultAdmin
    - GridH5StructureControl

    For more information about threedigrid see
    https://threedigrid.readthedocs.io/en/latest/

    Some helper methods are available query the result data using a variable
    name (example of variable names: 's1', 'q_cum', 'vol', etc)

    However, it is recommended to use threedigrid instead.

    """

    def __init__(self, file_path, h5_path):
        self.file_path = file_path
        self.h5_path = h5_path
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

    @cached_property
    def available_water_quality_vars(self):
        """Return a list of available variables from 'water_quality_results_3di.nc'."""
        ga = self.water_quality_result_admin
        if not ga:
            return []
        available_vars = []
        substances = ga.substances
        for substance_id in substances:
            substance = ga.get_model_instance_by_field_name(substance_id)
            if substance:
                units = substance.units
                var = {
                    "name": substance.name,
                    "unit": "-" if not units or isinstance(units, h5py.Empty) else units,
                    "parameters": substance_id,
                }
                available_vars.append(var)
        return available_vars

    @property
    def available_vars(self):
        """Return a list of all available variables"""
        return self.available_subgrid_map_vars + self.available_aggregation_vars + self.available_water_quality_vars + self.available_structure_control_actions_vars

    @property
    def available_structure_control_actions_vars(self):
        """Return a list of all structure control actions variables"""
        ga = self.structure_control_actions_result_admin
        if not ga:
            return []
        available_vars = []
        for control_type in StructureControlTypes.__members__.values():
            control_type_data = getattr(ga, control_type.name)
            action_types = np.unique(control_type_data.action_type)
            for action_type in action_types:
                source_types = [cta.source_type.value for cta in control_type_data.group_by_action_type(action_type)]
                var = {
                    "name": action_type[4:].replace("_", " ").capitalize(),  # sanitize
                    "unit": ACTION_TYPE_ATTRIBUTE_MAP[action_type]["unit"],
                    "parameters": action_type,
                    "types": source_types
                }
                if var not in available_vars:
                    available_vars.append(var)

        return available_vars

    @cached_property
    def timestamps(self):
        """Return the timestamps of the 'results_3di.nc'

        All variables in the 'results_3di.nc' have the same timestamps.
        The 'aggregate_results_3di.nc' can have different number of timestamps
        for each variable.

        :return 1d np.array containing the timestamps in seconds.
        """
        return self.get_timestamps()

    @cached_property
    def dt_timestamps(self):
        """Return the datetime timestamps of the 'results_3di.nc'

        :return 1d np.array containing the timestamps in seconds.
        """
        return self.result_admin.nodes.dt_timestamps  # after bug fix

    def get_timeseries_values(self, ts, variable):
        if variable in [v["parameters"] for v in self.available_water_quality_vars]:
            # use "concentration" field for water quality variables
            return ts.get_filtered_field_value("concentration")
        else:
            return ts.get_filtered_field_value(variable)

    def get_timestamps(self, parameter=None):
        """Return an array of timestamps for the given parameter

        The timestamps are in seconds after the start of the simulation.

        All variables in the result_netcdf and water_quality_netcdf share the
        same timestamps.
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
        elif parameter in [v["parameters"] for v in self.available_water_quality_vars]:
            ga = self.get_gridadmin(variable=parameter)
            return ga.get_model_instance_by_field_name(parameter).timestamps
        else:
            ga = self.get_gridadmin(variable=parameter)
            return ga.get_model_instance_by_field_name(parameter).get_timestamps(
                parameter
            )

    def get_gridadmin(self, variable=None):
        """Return the gridadmin where the variable is stored. If no variable is
        given, a gridadmin without results is returned.

        Results are either stored in the 'results_3di.nc', 'aggregate_results_3di.nc',
        'water_quality_results_3di.nc' or 'structure_control_actions_3di.nc'. These make use of the GridH5ResultAdmin,
        GridH5AggregateResultAdmin, GridH5WaterQualityResultAdmin or GridH5StructureControl to query the data
        respectively.

        :param variable: str of the variable name, e.g. 's1', 'q_pump'
        :return: handle to GridAdminResult, AggregateGridAdminResult, GridH5WaterQualityResultAdmin or GridH5StructureControl
        """
        if variable is None:
            return self.gridadmin
        elif variable in self.available_subgrid_map_vars:
            return self.result_admin
        elif variable in self.available_aggregation_vars:
            return self.aggregate_result_admin
        elif variable in [v["parameters"] for v in self.available_water_quality_vars]:
            return self.water_quality_result_admin
        elif variable in [v["parameters"] for v in self.available_structure_control_actions_vars]:
            return self.structure_control_actions_result_admin
        else:
            raise AttributeError(f"Unknown subgrid or aggregate or water quality variable: {variable}")

    def get_timeseries(
        self, nc_variable, node_id=None, fill_value=None, selected_object_type=None
    ):
        """Return a time series array of the given variable

        A 2d array is given, with first column being the timestamps in seconds.
        The next columns are the values of the nodes of the given variable.
        You can also filter on a specific node using node_id,
        in which case only the timeseries of the given node is returned.

        If there is no values of the given variable, only the timestamps are
        returned, i.e. an array of shape (n, 1) with n being the timestamps.

        :param nc_variable:
        :param node_id:
        :param fill_value:
        :param selected_object_type: layer type of selected feature
        :return: 2D array, first column being the timestamps
        """
        ga = self.get_gridadmin(nc_variable)

        if isinstance(ga, GridH5StructureControl):
            # GridH5StructureControl has a different interface compared to the other GridAdmin structures
            return self.get_structure_control_action_timeseries(ga, nc_variable, node_id, selected_object_type, fill_value)
        else:
            filtered_result = ga.get_model_instance_by_field_name(nc_variable).timeseries(
                indexes=slice(None)
            )
            if node_id:
                filtered_result = filtered_result.filter(id=node_id)
            values = self.get_timeseries_values(filtered_result, nc_variable)
            if fill_value is not None:
                values[values == NO_DATA_VALUE] = fill_value

            timestamps = self.get_timestamps(nc_variable)
            timestamps = timestamps.reshape(-1, 1)  # reshape (n,) to (n, 1)

            return np.hstack([timestamps, values])

    def get_structure_control_action_timeseries(self, ga, nc_variable, node_id, selected_object_type, fill_value):
        assert nc_variable
        assert node_id
        timestamps = []
        values = []
        for control_type in StructureControlTypes.__members__.values():
            control_type_data = getattr(ga, control_type.name)
            structure_controls_for_id = control_type_data.group_by_grid_id(node_id)
            structure_controls = [sc for sc in structure_controls_for_id if sc.action_type == nc_variable]

            #  It could be that the same action is applied on nodes, lines and pumps, we need to find the right one.
            desired_type = StructureControlSourceTypes.LINES if selected_object_type == "flowline" else StructureControlSourceTypes.PUMPS
            structure_controls = [sc for sc in structure_controls_for_id if sc.source_type == desired_type]

            for structure_control in structure_controls:
                timestamps += list(structure_control.time)
                values += list(structure_control.action_value_1)

        # Retrieve gridadmin structure
        if selected_object_type == "flowline":
            structure = self.gridadmin.lines.filter(id=node_id)
        elif selected_object_type == "pump":
            structure = self.gridadmin.pumps.filter(id=node_id)
        else:
            raise NotImplementedError("Plotting node control actions is not yet implemented")

        # Check whether this object's content type is applicable for this control action
        applicable_structures = ACTION_TYPE_ATTRIBUTE_MAP[nc_variable]["applicable_structures"]
        if applicable_structures:
            content_type = structure.content_type[0].decode()
            if content_type not in applicable_structures:
                #  This action is not applicable to this object
                logger.info(f"Parameter {nc_variable} not applicable for type {str(content_type)}")
                return np.column_stack(([], []))

        affected_nc_variable = ACTION_TYPE_ATTRIBUTE_MAP[nc_variable]["variable"]
        if affected_nc_variable:
            # Check if we need to prepend and append the plot with non-controlled (static) values
            orig_timestamps = self.get_timestamps()
            orig_value = getattr(structure, affected_nc_variable)[0]
            if not timestamps:
                # No actions at all, take original value to plot
                assert not values
                values = [orig_value] * len(orig_timestamps)
                timestamps = orig_timestamps
            else:
                # find all timestamps before and after structure control timestamps
                min_time_stamp_structure = min(timestamps)
                max_time_stamp_structure = max(timestamps)
                for timestamp in orig_timestamps:
                    if timestamp < min_time_stamp_structure:
                        values.insert(0, orig_value)
                        timestamps.insert(0, timestamps)
                    if timestamp > max_time_stamp_structure:
                        values.append(orig_value)
                        timestamps.append(timestamp)

        if not values:
            return np.column_stack(([], []))

        if fill_value is not None:
            values[values == NO_DATA_VALUE] = fill_value

        return np.column_stack((timestamps, values))

    def get_values_by_timestep_nr(self, variable, timestamp_idx, node_ids):
        """Return an array of values of the given variable on the specified
        timestamp(s)

        :param variable: (str) variable name, e.g. 's1', 'q_pump'
        :param timestamp_idx: int or 1d numpy.array of indexes of timestamps
        :param node_ids: 1d numpy.array of node_ids or None in which case all
            nodes are returned.
        :return: 1d/2d numpy.array

        If only one timestamp is specified, a 1d np.array is returned.  If an
        array of multiple timestamp_idx is given, a 2d np.array is returned.

        If node_ids is specified, only the values corresponding to the
        specified node_ids will be returned.

        A note about the implementation: 3Di ids start at 1. The numpy array
        from the GridResultAdmin starts with an extra, meaningless element
        along the node dimension, so that the node_ids can be used as an index.
        """
        values = self._nc_from_mem(variable)
        if isinstance(timestamp_idx, int):
            timestamp_idx = np.array([timestamp_idx])

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
            values = self.get_timeseries_values(unfiltered_timeseries, variable)
            logger.debug(
                "Caching additional {:.3f} MB of data".format(
                    values.nbytes / 1000 / 1000
                )
            )
            self._cache[variable] = values
        return values

    @cached_property
    def gridadmin(self):
        h5 = self.h5_path
        return GridH5Admin(open(h5, 'rb'))

    @cached_property
    def result_admin(self):
        h5 = self.h5_path
        # TODO: there's no FileNotFound try/except here like for
        # aggregates. Richard says that a missing regular result file is just
        # as likely.
        # Note: passing a file-like object due to an issue in threedigrid
        # https://github.com/nens/threedigrid/issues/183
        file_like_object_h5 = open(h5, 'rb')
        file_like_object_h5.startswith = lambda x: False
        file_like_object_nc = open(self.file_path, 'rb')
        return GridH5ResultAdmin(file_like_object_h5, file_like_object_nc)

    @cached_property
    def aggregate_result_admin(self):
        try:
            # Note: both of these might raise the FileNotFoundError
            agg_path = find_aggregation_netcdf(self.file_path)
            h5 = self.h5_path
        except FileNotFoundError:
            logger.exception("Aggregate result not found")
            return None
        # Note: passing a file-like object due to an issue in threedigrid
        # https://github.com/nens/threedigrid/issues/183
        file_like_object_h5 = open(h5, 'rb')
        file_like_object_h5.startswith = lambda x: False
        file_like_object_nc = open(agg_path, 'rb')
        return GridH5AggregateResultAdmin(file_like_object_h5, file_like_object_nc)

    @cached_property
    def water_quality_result_admin(self):
        try:
            # Note: both of these might raise the FileNotFoundError
            wq_path = find_water_quality_netcdf(self.file_path)
            h5 = self.h5_path
        except FileNotFoundError:
            logger.exception("Water quality result not found")
            return None
        # Note: passing a file-like object due to an issue in threedigrid
        # https://github.com/nens/threedigrid/issues/183
        file_like_object_h5 = open(h5, 'rb')
        file_like_object_h5.startswith = lambda x: False
        file_like_object_nc = open(wq_path, 'rb')
        return GridH5WaterQualityResultAdmin(file_like_object_h5, file_like_object_nc)

    @cached_property
    def structure_control_actions_result_admin(self):
        try:
            # Note: both of these might raise the FileNotFoundError
            sca_path = find_structure_control_actions_netcdf(self.file_path)
            h5 = self.h5_path
        except FileNotFoundError:
            logger.exception("Structure control actions result not found")
            return None
        # Note: passing a file-like object due to an issue in threedigrid
        # https://github.com/nens/threedigrid/issues/183
        file_like_object_h5 = open(h5, 'rb')
        file_like_object_h5.startswith = lambda x: False
        file_like_object_nc = open(sca_path, 'rb')
        return GridH5StructureControl(file_like_object_h5, file_like_object_nc)

    @property
    def short_model_slug(self):
        model_slug = self.gridadmin.model_slug
        try:
            return model_slug.rsplit("-", 1)[0]
        except Exception:
            logger.exception(
                "TODO: overly broad exception while splitting model_slug. "
                "Using model_name"
            )
            return self.gridadmin.model_name


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


def find_structure_control_actions_netcdf(netcdf_file_path):
    """An ad-hoc way to find the structure control actions netcdf file

    Args:
        netcdf_file_path: path to the result netcdf

    Returns:
        the structure control actions netcdf path

    Raises:
        FileNotFoundError if nothing is found
    """
    pattern = "structure_control_actions_3di.nc"
    result_dir = os.path.dirname(netcdf_file_path)
    sca_result_files = glob.glob(os.path.join(result_dir, pattern))
    if sca_result_files:
        return sca_result_files[0]
    raise FileNotFoundError(
        "'structure_control_actions_3di.nc' file not found relative to %s" % result_dir
    )


def find_water_quality_netcdf(netcdf_file_path):
    """An ad-hoc way to find the water quality netcdf file

    Args:
        netcdf_file_path: path to the result netcdf

    Returns:
        the water quality netcdf path

    Raises:
        FileNotFoundError if nothing is found
    """
    pattern = "water_quality_results_3di.nc"
    result_dir = os.path.dirname(netcdf_file_path)
    water_quality_result_files = glob.glob(os.path.join(result_dir, pattern))
    if water_quality_result_files:
        return water_quality_result_files[0]
    raise FileNotFoundError(
        "'water_quality_results_3di.nc' file not found relative to %s" % result_dir
    )
