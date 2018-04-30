from .base import BaseDataSource
from ..utils import cached_property
import logging
import numpy as np

log = logging.getLogger(__name__)


layer_information = [
    # layer object_type, gridadmin_name , gridadmin_type, qgis layer_source
    ('v2_connection_nodes', 'v2_connection_nodes', 'nodes', 'schematized'),
    ('v2_pipe_view', 'v2_pipe', 'lines', 'schematized'),
    ('v2_channel', 'v2_channel', 'lines', 'schematized'),
    ('v2_culvert_view', 'v2_culvert', 'lines', 'schematized'),
    ('v2_pumpstation', 'v2_pumpstation', 'pumps', 'schematized'),
    # deze niet nodig toch?
    #  ('v2_pumpstation_view', 'pumpstation', 'q', 'schematized'),
    ('v2_weir_view', 'v2_weir', 'lines', 'schematized'),
    ('v2_orifice_view', 'v2_orifice', 'lines', 'schematized'),
    # ('sewerage_manhole', 'manhole', 'h', 'schematized'),
    # ('sewerage_pipe_view', 'pipe', 'q', 'schematized'),
    # ('sewerage_pumpstation', 'pumpstation', 'q', 'schematized'),
    # ('sewerage_pumpstation_view', 'pumpstation', 'q', 'schematized'),
    # ('sewerage_weir_view', 'weir', 'q', 'schematized'),
    # ('sewerage_orifice_view', 'orifice', 'q', 'schematized'),
    ('flowlines', 'lines', 'lines', 'result'),
    ('nodes', 'nodes', 'nodes', 'result'),
    ('pumplines', 'pumps', 'pumps', 'result'),
    ('node_results', 'nodes', 'nodes', 'result'),
    ('node_results_groundwater', 'nodes', 'h', 'result'),
    ('line_results', 'lines', 'lines', 'result'),
    ('line_results_groundwater', 'lines', 'lines', 'result'),
]

object_type_gr_name = dict(
    [(a[0], a[1]) for a in layer_information])
object_type_gr_type = dict(
    [(a[0], a[2]) for a in layer_information])
object_type_layer_source = dict(
    [(a[0], a[3]) for a in layer_information])


def get_gr_name(current_layer_name):
    # Get the gridadmin name (v2_weir, v2_channel, etc) for internal purposes
    if current_layer_name in object_type_gr_name.keys():
        return object_type_gr_name[current_layer_name]
    else:
        msg = "Unsupported layer: %s." % current_layer_name
        log.warning(msg)
        return None
assert get_gr_name('v2_weir_view') == 'v2_weir'


def get_gr_type(current_layer_name):
    # Get the gridadmin type (nodes, lines, pumps) for internal purposes
    if current_layer_name in object_type_gr_type.keys():
        return object_type_gr_type[current_layer_name]
    else:
        msg = "Unsupported layer: %s." % current_layer_name
        log.warning(msg)
        return None
assert get_gr_type('v2_weir_view') == 'lines'


def get_layer_source(current_layer_name):
    # Get the layer source (schematized, result) for internal purposes
    if current_layer_name in object_type_layer_source.keys():
        return object_type_layer_source[current_layer_name]
    else:
        msg = "Unsupported layer: %s." % current_layer_name
        log.warning(msg)
        return None
assert get_layer_source('v2_weir_view') == 'schematized'
assert get_layer_source('pumplines') == 'result'


class NetcdfDataSourceGroundwater(BaseDataSource):
    PREFIX_1D = 'Mesh1D_'
    PREFIX_2D = 'Mesh2D_'
    PREFIX_1D_LENGTH = 7  # just so we don't have to recalculate
    PREFIX_2D_LENGTH = 7  # just so we don't have to recalculate

    def __init__(self, file_path=None, *args, **kwargs):
        from netCDF4 import Dataset
        self.file_path = file_path
        self._ga = None
        self._ga_result = None
        self.ds = Dataset(file_path)

        self.nMesh2D_nodes = self.ds.dimensions['nMesh2D_nodes'].size
        self.nMesh1D_nodes = self.ds.dimensions['nMesh1D_nodes'].size
        self.nMesh2D_lines = self.ds.dimensions['nMesh2D_lines'].size
        self.nMesh1D_lines = self.ds.dimensions['nMesh1D_lines'].size
        self._cache = {}

    def _strip_prefix(self, var_name):
        """Strip away netCDF variable name prefixes.

        Example variable names: 'Mesh2D_s1', 'Mesh1D_s1'

        >>> from ThreeDiToolbox.datasource.netcdf_groundwater
        import NetcdfDataSourceGroundwater  # noqa
        >>> ds = NetcdfDataSourceGroundwater()
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
        # This method is used by the water balance plugin (DeltaresTdiToolbox)
        return self.available_subgrid_map_vars

    def node_type_of(self, node_idx):
        pass

    def line_type_of(self, line_idx):
        pass

    @cached_property
    def timestamps(self):
        return self.get_timestamps()

    # def get_timeseries(
    #         self, object_type, object_id, nc_variable, fill_value=None):
    #     return self.temporary_get_timeseries_impl(
    #         object_type, object_id, nc_variable, fill_value)

    def get_timeseries_schematisation_layer(
            self, object_type, object_id, nc_variable, timeseries=None,
            only=None, data=None):

        """
        -   just using a random v2_bergermeer nc and h5 file we see that:
        In [1]: gr.lines.filter(content_type='v2_channel').content_pk
        Out[1]: array([1, 1, 2, ...,  760,  851, 1090]
        In [2]: len(set(gr.lines.filter(content_type='v2_channel').content_pk))
        Out[2]: 2346
        In [3]: len(set(gr.lines.filter(content_type='v2_channel').content_pk))
        Out[3]: 1175
        -   The v2_channel QgisVectorLayer contains id 1 till 666668899 (
            1175 rows), so we can use content_pk to retrieve a timeseries
        -   to get a timeseries using threedigridadmin, we need to call e.g.
            gr.lines.filter(content_type='v2_channel', content_pk=1).
            timeseries(indexes=slice(None)).only('q').data['q']
        -   this will return multiple timeseries (since a v2_channel can be
            splitted up in multiple flowlines
        -   slice(None) means we get all timesteps.
        -   get_timeseries_schematisation_layer() gets strings as arguments
            that we need to parse as atrributes
        """

        # one example for v2_weir_view
        # gr.lines
        # determine wheter v2_weir_view is a lines, nodes or pumps
        first = getattr(self.gr, get_gr_type(object_type))
        # gr.lines.filter(content_type='v2_weir', content_pk=1)
        # we need to get de gridadminname of v2_weir_view (=v2_weir)
        second = first.filter(content_type=get_gr_name(object_type),
                              content_pk=object_id)
        # gr.lines.filter(content_type='v2_channel',content_pk=1).timeseries(
        # indexes=slice(None))
        third = second.timeseries(indexes=slice(None))
        # gr.lines.filter(content_type='v2_channel',content_pk=1).timeseries(
        # indexes=slice(None)).only('q')
        fourth = third.only(nc_variable)
        # gr.lines.filter(content_type='v2_channel',content_pk=1).timeseries(
        # indexes=slice(None)).only('q').data
        fifth = fourth.data
        # fifth is an OrderedDict:
        # OrderedDict([('q', array([  [ 0.00000000e+00,  0.00000000e+00],
        #                             [-3.27184124e-10, -7.85903914e-12],
        # to only get the array we use fifth['q']

        # for now, we just take only the timeseries of the first flowline (
        # when multiple flowlines are returned
        # TODO
        # return all timeseries are do an avg, min, max
        # e.g. self.vals = np.mean(fifth[nc_variable], axis=1)
        self.vals = fifth[nc_variable][:, 0]

    def get_timeseries_result_layer(self, object_type, object_id, nc_variable):
        """
        -   to get a timeseries using threedigridadmin, we need to call e.g.
            ga.nodes.filter(id=100).timeseries(indexes=slice(None)).s1
        -   slice(None) means we get all timesteps.
        -   get_timeseries_result_layer() gets strings as arguments
            that we need to parse as atrributes
        -   using the gridadmin in a python we see that:
        In [1]: gr.nodes.id
        Out[1]: array([0, 1, 2, ..., 15601, 15602, 15603])
        In [2]: len(gr.nodes.id)
        Out[2]: 15604
        In [3]: len(set(gr.nodes.id))
        Out[3]: 15604
        In [4]: gr.nodes.filter(id=0)
        this returns empty stuff
        -   The nodes QgisVectorLayer contains id 1 till 15603 (15603 rows),
            therefore we can use id to retrieve a timeseries
        """

        # we need the grdadmin type (e.g. rom flowlines to lines)
        object_type = get_gr_type(object_type)
        # one example for nodes
        # gr.nodes
        first = getattr(self.gr, object_type)
        # gr.nodes.filter(id=100)
        second = first.filter(id=object_id)
        # gr.nodes.filter(id=100).timeseries(indexes=slice(None))
        third = second.timeseries(indexes=slice(None))
        # get the timeserie of the nc_variable
        self.vals = getattr(third, nc_variable)
        # flatten numpyarray
        self.vals = self.vals.flatten()

    def get_timeseries(
            self, object_type, object_id, nc_variable, fill_value=None):

        self.gr = self.gridadmin_result

        # determine if layer is a not_schematized (e.g nodes, pumps)
        if get_layer_source(object_type) == 'result':
            if object_type == 'pumplines':
                nc_variable = 'Mesh1D_q_pump'
            self.get_timeseries_result_layer(
                object_type, object_id, nc_variable)
        elif get_layer_source(object_type) == 'schematized':
            if object_type == 'v2_pumpstation':
                nc_variable = 'Mesh1D_q_pump'
            self.get_timeseries_schematisation_layer(
                object_type, object_id, nc_variable)

        # Zip timeseries together in (n,2) array
        if fill_value is not None and type(self.vals) == \
                np.ma.core.MaskedArray:
            self.vals = self.vals.filled(fill_value)
        return np.vstack((self.timestamps, self.vals)).T

    def get_timestamps(self, object_type=None, parameter=None):
        # TODO: use cached property to limit file access
        return self.ds.variables['time'][:]

    # used in map_animator
    def get_values_by_timestep_nr(
            self, variable, timestamp_idx, index=None, use_cache=True):
        return self.temp_get_values_by_timestep_nr_impl(
            variable, timestamp_idx, index, use_cache)

    def _nc_from_mem(self, variable, use_cache=True):
        """Get netcdf data from memory if needed."""
        if use_cache:
            try:
                data = self._cache[variable]
            except KeyError:
                # Keep the whole netCDF array for a variable in memory for
                # performance
                data = self.ds.variables[variable][:]  # make copy
                self._cache[variable] = data
        else:
            # this returns a netCDF Variable, which behaves like a np array
            data = self.ds.variables[variable]
        return data

    def temp_get_values_by_timestep_nr_impl(
            self, variable, timestamp_idx, index=None, use_cache=True):
        import numpy as np
        from .netcdf import Q_TYPES, H_TYPES
        var_2d = self.PREFIX_2D + variable
        var_1d = self.PREFIX_1D + variable

        if index is not None:
            # in the groundwater version, the node index starts from 1 instead
            # of 0.
            # Note: a new array is created, e.g., index doesn't get modified
            index = index - 1  # copies the array

            # hacky object_type checking mechanism, sinds we don't have
            # that information readily available
            if variable == 'q_pump':
                return self._nc_from_mem(
                    var_1d, use_cache)[timestamp_idx, index]
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
                res[idx_2d] = self._nc_from_mem(
                    var_2d, use_cache)[timestamp_idx, iarr_2d]
            if iarr_1d.size > 0:
                res[idx_1d] = self._nc_from_mem(
                    var_1d, use_cache)[timestamp_idx, iarr_1d]
        else:
            if variable == 'q_pump':
                return self._nc_from_mem(var_1d, use_cache)[timestamp_idx, :]
            # TODO: pumps won't work
            vals_2d = self._nc_from_mem(var_2d, use_cache)[timestamp_idx, :]
            vals_1d = self._nc_from_mem(var_1d, use_cache)[timestamp_idx, :]
            # order is: 2D, then 1D
            res = np.hstack((vals_2d, vals_1d))

        fill_value_2d = self.ds.variables[var_2d]._FillValue
        fill_value_1d = self.ds.variables[var_1d]._FillValue
        assert fill_value_1d == fill_value_2d, \
            "Difference in fill value, can't consolidate"
        # res is a normal array, we need to mask the values again from the
        # netcdf
        masked_res = np.ma.masked_values(res, fill_value_2d)
        return masked_res

    @property
    def gridadmin(self):
        if not self._ga:
            from ..utils.patched_threedigrid import GridH5Admin
            from ..datasource.netcdf import find_h5_file
            h5 = find_h5_file(self.file_path)
            self._ga = GridH5Admin(h5)
        return self._ga

    @property
    def gridadmin_result(self):
        if not self._ga_result:
            from ..datasource.netcdf import find_h5_file
            from ..utils.patched_threedigrid import GridH5ResultAdmin
            h5 = find_h5_file(self.file_path)
            self._ga_result = GridH5ResultAdmin(h5, self.file_path)
        return self._ga_result

    def ds_aggregation(self):
        return None