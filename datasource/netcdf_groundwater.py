import glob
import logging
import os
import numpy as np

from .base import BaseDataSource
from ..utils import cached_property
from .netcdf import (
    SUBGRID_MAP_VARIABLES, AGG_Q_TYPES, AGG_H_TYPES, Q_TYPES, H_TYPES,
    find_h5_file
)
from ..utils.user_messages import messagebar_message

# all possible var names from regular netcdf AND agg netcdf
ALL_Q_TYPES = Q_TYPES + AGG_Q_TYPES
ALL_H_TYPES = H_TYPES + AGG_H_TYPES

log = logging.getLogger(__name__)

layer_information = [
    # object_type, model_instance, model_instance_subset, qgis_layer_source
    ('v2_connection_nodes', 'nodes', 'connectionnodes', 'schematized'),
    ('v2_pipe_view', 'lines', 'pipes', 'schematized'),
    ('v2_channel', 'lines', 'channels', 'schematized'),
    ('v2_culvert_view', 'lines', 'culverts', 'schematized'),
    # Todo:
    # 'v2_manhole_view', 'nodes', 'manholes', 'schematized'),
    ('v2_pumpstation_view', 'pumps', 'pumps', 'schematized'),
    ('v2_weir_view', 'lines', 'weirs', 'schematized'),
    ('v2_orifice_view', 'lines', 'orifices', 'schematized'),
    ('flowlines', 'lines', 'lines', 'result'),
    ('nodes', 'nodes', 'nodes', 'result'),
    ('pumplines', 'pumps', 'pumps', 'result'),
    ('node_results', 'nodes', 'nodes', 'result'),
    ('node_results_groundwater', 'nodes', 'nodes', 'result'),
    ('line_results', 'lines', 'lines', 'result'),
    ('line_results_groundwater', 'lines', 'lines', 'result')
    ]

object_type_model_instance = dict(
    [(a[0], a[1]) for a in layer_information])
object_type_model_instance_subset = dict(
    [(a[0], a[2]) for a in layer_information])
object_type_layer_source = dict(
    [(a[0], a[3]) for a in layer_information])


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
    pattern = 'aggregate_results_3di.nc'
    result_dir = os.path.dirname(netcdf_file_path)
    return glob.glob(os.path.join(result_dir, pattern))[0]


class NetcdfGroundwaterDataSource(BaseDataSource):
    PREFIX_1D = 'Mesh1D_'
    PREFIX_2D = 'Mesh2D_'
    PREFIX_1D_LENGTH = 7  # just so we don't have to recalculate
    PREFIX_2D_LENGTH = 7  # just so we don't have to recalculate

    def __init__(self, file_path=None, *args, **kwargs):
        self.file_path = file_path
        self._ga = None
        self._ga_result = None
        self._ds = None
        self._cache = {}

    @property
    def ds(self):
        from netCDF4 import Dataset
        if self._ds is None:
            try:
                self._ds = Dataset(self.file_path)
            except IOError:
                pass
        return self._ds

    @property
    def nMesh2D_nodes(self):
        return self.ds.dimensions['nMesh2D_nodes'].size

    @property
    def nMesh1D_nodes(self):
        return self.ds.dimensions['nMesh1D_nodes'].size

    @property
    def nMesh2D_lines(self):
        return self.ds.dimensions['nMesh2D_lines'].size

    @property
    def nMesh1D_lines(self):
        return self.ds.dimensions['nMesh1D_lines'].size

    def _strip_prefix(self, var_name):
        """Strip away netCDF variable name prefixes.

        Example variable names: 'Mesh2D_s1', 'Mesh1D_s1'

        >>> from ThreeDiToolbox.datasource.netcdf_groundwater import NetcdfGroundwaterDataSource  # noqa
        >>> ds = NetcdfGroundwaterDataSource()
        >>> ds._strip_prefix('Mesh2D_s1')
        's1'
        >> ds._strip_prefix('Mesh1D_q')
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
        known_subgrid_map_vars = set([v.name for v in SUBGRID_MAP_VARIABLES])
        if self.gridadmin_result.has_pumpstations:
            available_vars = (
                self.gridadmin_result.nodes._field_names |
                self.gridadmin_result.lines._field_names |
                self.gridadmin_result.pumps._field_names)
        else:
            available_vars = (
                self.gridadmin_result.nodes._field_names |
                self.gridadmin_result.lines._field_names)
        # filter using a hardcoded 'whitelist'
        available_known_vars = available_vars & known_subgrid_map_vars
        return list(available_known_vars)

    @cached_property
    def available_aggregation_vars(self):
        agg = self.gridadmin_aggregate_result
        if not agg:
            return []
        # hardcoded whitelist
        known_vars = set(
            agg.lines.Meta.composite_fields.keys() +
            agg.nodes.Meta.composite_fields.keys() +
            agg.pumps.Meta.composite_fields.keys()
        )
        # all available fields, including hdf5 fields
        available_vars = (
            agg.nodes._field_names | agg.lines._field_names |
            agg.pumps._field_names
        )
        available_known_vars = available_vars & known_vars
        return list(available_known_vars)

    def get_available_variables(self):
        # This method is used by the water balance plugin (DeltaresTdiToolbox)
        return (
            self.available_subgrid_map_vars + self.available_aggregation_vars
        )

    @cached_property
    def timestamps(self):
        return self.get_timestamps()

    def _get_timeseries_schematisation_layer(
            self, gridadmin_result, object_type, object_id, nc_variable,
            timeseries=None, only=None, data=None):
        """
        -   this function retireves a timeserie when user select a
            schematization layer and e.g. 'adds' it to the graph.
        -   filtering for nodes/lines differs from filtering for pumps:
            - nodes/lines:  qgisvectorlayer object_id = gridadmin content_pk
            - pumps:        has no contect_pk, therefore we use id.
                            Qgisvectorlayer object_id = gridadmin id + 1
        -   slice(None) means we get all timesteps.
        -   get_timeseries_schematisation_layer() gets strings as arguments
            that we need to parse as atrributes
        """
        # get the gridadmin model instance (e.g. v2_pipe_view to lines)
        model_instance = object_type_model_instance[object_type]
        # get the gridadmin model instance subset (e.g. v2_pipe_view to pipes)
        model_instance_subset = object_type_model_instance_subset[object_type]

        # gr.nodes / gr.lines / gr.pumps
        gr_model_instance = getattr(gridadmin_result, model_instance)

        if model_instance in ['nodes', 'lines']:
            # one example for v2_connection_nodes =
            # gr.nodes.connectionnodes.filter(content_pk=1).timeseries(
            #   indexes=slice(None)).vol
            # one example for v2_channels =
            # gr.lines.channels.filter(content_pk=1).timeseries(
            #   indexes=slice(None)).au

            # e.g. gr.nodes.connectionnodes
            gr_model_instance_subset = getattr(
                gr_model_instance, model_instance_subset)
            # e.g. gr.nodes.connectionnodes.filter(content_pk=1).timeseries(
            #   indexes=slice(None))
            filter_timeseries = \
                gr_model_instance_subset.filter(
                    content_pk=object_id).timeseries(indexes=slice(None))
            # e.g. gr.nodes.connectionnodes.filter(content_pk=1).timeseries(
            #   indexes=slice(None)).vol
            filter_timeseries_ncvar = getattr(filter_timeseries, nc_variable)
            # this could return multiple timeseries, since a v2_channel can
            # be splitted up in multiple flowlines. For now, we pick first:
            pick_only_first_of_element = 0
            vals = filter_timeseries_ncvar[:, pick_only_first_of_element]
            return vals
        elif model_instance == 'pumps':
            # TODO
            # filtering on id still needs to be implemented in threedigrid
            # prepare. For now, users need to use pumplines qgisvectorlayer
            msg = "v2_pumpstation_view results are not implemented yet. Use " \
                  "the 'pumplines' layer to get your results"
            messagebar_message('Warning', msg, level=1, duration=6)
        else:
            raise ValueError('object_type not available')

    def _get_timeseries_result_layer(
            self, gridadmin_result, object_type, object_id, nc_variable):
        """
        -   this function retireves a timeserie when user select a
            result layer and e.g. 'adds' it to the graph
        -   to get a timeseries using threedigridadmin, we need to call e.g.
            ga.nodes.filter(id=100).timeseries(indexes=slice(None)).s1
        -   slice(None) means we get all timesteps.
        -   get_timeseries_result_layer() gets strings as arguments
            that we need to parse as atrributes
        """
        # get the gridadmin model instance (e.g. pumplines_view to pumps)
        model_instance = object_type_model_instance[object_type]

        # gr.nodes / gr.lines / gr.pumps
        gr_model_instance = getattr(gridadmin_result, model_instance)

        # gr.nodes.filter(id=100).timeseries(indexes=slice(None))
        filter_timeseries = gr_model_instance.filter(
            id=object_id).timeseries(indexes=slice(None))
        # gr.nodes.filter(id=100).timeseries(indexes=slice(None)).vol
        filter_timeseries_ncvar = getattr(filter_timeseries, nc_variable)
        # flatten numpyarray
        vals = filter_timeseries_ncvar.flatten()
        return vals

    def get_timeseries(
            self, object_type, object_id, nc_variable, fill_value=None):

        if nc_variable in self.available_subgrid_map_vars:
            gr = self.gridadmin_result
            ts = self.timestamps
        elif nc_variable in self.available_aggregation_vars:
            gr = self.gridadmin_aggregate_result
            ts = self.get_timestamps(parameter=nc_variable)
        else:
            log.error("Unsupported variable %s", nc_variable)

        # determine if layer is a not_schematized (e.g nodes, pumps)
        if object_type_layer_source[object_type] == 'result':
            values = self._get_timeseries_result_layer(
                gr, object_type, object_id, nc_variable)
        elif object_type_layer_source[object_type] == 'schematized':
            values = self._get_timeseries_schematisation_layer(
                gr, object_type, object_id, nc_variable)

        msg = "object_id={object_id} and object_type={object_type} and " \
              "nc_variable={nc_variable}".format(object_id=object_id,
                                                 object_type=object_type,
                                                 nc_variable=nc_variable)
        log.warning(msg)

        # Zip timeseries together in (n,2) array
        if fill_value is not None:
            # transform np.array into np.MaskedArray
            no_data_value = -9999
            masked_array = np.ma.masked_values(values, no_data_value)
            filled_vals = masked_array.filled(fill_value)
            return np.vstack((ts, filled_vals)).T
        else:
            # values can contain masked values from netCDF, therefore we need
            # np.ma.vstack
            return np.ma.vstack((ts, values)).T

    def get_timestamps(self, object_type=None, parameter=None):
        # TODO: use cached property to limit file access
        if parameter is None:
            return self.ds.variables['time'][:]
        elif parameter in [v[0] for v in SUBGRID_MAP_VARIABLES]:
            return self.ds.variables['time'][:]
        else:
            # determine the grid type from the parameter alone
            if parameter.startswith('q_pump'):
                object_type = 'pumplines'
            elif parameter in AGG_Q_TYPES:
                object_type = 'flowlines'
            elif parameter in AGG_H_TYPES:
                object_type = 'nodes'
            else:
                raise ValueError(parameter)
            grid_type = object_type_model_instance[object_type]
            orm_obj = getattr(self.gridadmin_aggregate_result, grid_type)
            return orm_obj.get_timestamps(parameter)

    # used in map_animator
    def get_values_by_timestep_nr(
            self, variable, timestamp_idx, index=None, use_cache=True):
        return self.temp_get_values_by_timestep_nr_impl(
            variable, timestamp_idx, index, use_cache)

    def _nc_from_mem(self, ds, variable, use_cache=True):
        """Get netcdf data from memory if needed."""
        if use_cache:
            try:
                data = self._cache[variable]
            except KeyError:
                # Keep the whole netCDF array for a variable in memory for
                # performance
                data = ds.variables[variable][:]  # make copy
                self._cache[variable] = data
        else:
            # this returns a netCDF Variable, which behaves like a np array
            data = ds.variables[variable]
        return data

    def temp_get_values_by_timestep_nr_impl(
            self, variable, timestamp_idx, index=None, use_cache=True):
        var_2d = self.PREFIX_2D + variable
        var_1d = self.PREFIX_1D + variable

        # determine if it's an agg var
        if variable in self.available_subgrid_map_vars:
            ds = self.ds
        elif variable in self.available_aggregation_vars:
            ds = self.ds_aggregation
        else:
            log.error("Unsupported variable %s", variable)
            raise ValueError(variable)

        # determine appropriate fill value from netCDF
        if var_2d in ds.variables.keys():
            fill_value_2d = ds.variables[var_2d]._FillValue
            fill_value = fill_value_2d
        if var_1d in ds.variables.keys():
            fill_value_1d = ds.variables[var_1d]._FillValue
            fill_value = fill_value_1d

        if var_2d in ds.variables.keys() and var_1d in ds.variables.keys():
            assert fill_value_1d == fill_value_2d, \
                "Difference in fill value, can't consolidate"

        if index is None:
            if variable.startswith('q_pump'):
                return self._nc_from_mem(
                    ds, var_1d, use_cache)[timestamp_idx, :]
            elif variable in ALL_Q_TYPES:
                n2d = self.nMesh2D_lines
                n1d = self.nMesh1D_lines
            elif variable in ALL_H_TYPES:
                n2d = self.nMesh2D_nodes
                n1d = self.nMesh1D_nodes
            else:
                raise ValueError(variable)

            # Note: it's possible to only have 2D or 1D
            if var_2d in ds.variables.keys():
                a2d = self._nc_from_mem(
                    ds, var_2d, use_cache)[timestamp_idx, :]
            else:
                a2d = np.ma.masked_all(n2d)

            if var_1d in ds.variables.keys():
                a1d = self._nc_from_mem(
                    ds, var_1d, use_cache)[timestamp_idx, :]
            else:
                a1d = np.ma.masked_all(n1d)

            assert (
                var_2d in ds.variables.keys() or var_1d in
                ds.variables.keys()), "No 2D and 1D?"

            # Note: order is: 2D, then 1D
            res = np.ma.hstack([a2d, a1d])
        else:
            # in the groundwater version, the node index starts from 1 instead
            # of 0.
            # Note: a new array is created, e.g., index doesn't get modified
            index = index - 1  # copies the array

            # hacky object_type checking mechanism, sinds we don't have
            # that information readily available
            if variable.startswith('q_pump'):
                return self._nc_from_mem(
                    ds, var_1d, use_cache)[timestamp_idx, index]
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
                res[idx_2d] = self._nc_from_mem(
                    ds, var_2d, use_cache)[timestamp_idx, iarr_2d]
            if iarr_1d.size > 0:
                res[idx_1d] = self._nc_from_mem(
                    ds, var_1d, use_cache)[timestamp_idx, iarr_1d]
        # note: res is a masked array
        return res

    @property
    def gridadmin(self):
        if not self._ga:
            from ..utils.patched_threedigrid import GridH5Admin
            h5 = find_h5_file(self.file_path)
            self._ga = GridH5Admin(h5)
        return self._ga

    @property
    def gridadmin_result(self):
        if not self._ga_result:
            from ..utils.patched_threedigrid import GridH5ResultAdmin
            h5 = find_h5_file(self.file_path)
            self._ga_result = GridH5ResultAdmin(h5, self.file_path)
        return self._ga_result

    @cached_property
    def gridadmin_aggregate_result(self):
        from ..utils.patched_threedigrid import GridH5AggregateResultAdmin
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
        from netCDF4 import Dataset

        # Load aggregation netcdf
        try:
            aggregation_netcdf_file = find_aggregation_netcdf_gw(
                self.file_path)
        except IndexError:
            return None
        else:
            log.info(
                "Opening aggregation netcdf: %s" % aggregation_netcdf_file)
            return Dataset(aggregation_netcdf_file, mode='r',
                           format='NETCDF4')
