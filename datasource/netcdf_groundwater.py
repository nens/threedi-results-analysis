from .base import BaseDataSource
from ..utils import cached_property
import logging
import numpy as np

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
    ('v2_weir_view', 'weirs', 'lines', 'schematized'),
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

        >>> from ThreeDiToolbox.datasource.netcdf_groundwater import NetcdfDataSourceGroundwater  # noqa
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
        available_vars = (
            self.gridadmin_result.nodes._field_names |
            self.gridadmin_result.lines._field_names |
            self.gridadmin_result.pumps._field_names
        )
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
            self, object_type, object_id, nc_variable, timeseries=None,
            only=None, data=None):
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
        gr_model_instance = getattr(self.gridadmin_result, model_instance)

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
            filter_timeseries_ncvar = getattr(
                filter_timeseries, nc_variable)
            # this could return multiple timeseries, since a v2_channel can
            # be splitted up in multiple flowlines. For now, we pick first:
            pick_only_first_of_element = 0
            vals = filter_timeseries_ncvar[:, pick_only_first_of_element]

        elif model_instance == 'pumps':
            # one example for v2_pumpstation =
            # gr.pumps.filter(id=3).timeseries(indexes=slice(
                # None)).Mesh1D_q_pump
            # gr.pumps.timeseries(indexes=slice(None))
            gr_model_instance_subset = \
                gr_model_instance.timeseries(indexes=slice(None))

            # tijdelijke hack omdat threedigrid indexerrors geeft op pumps
            # normaalgesproken zou dit werken:
            # gr.pumps.filter(id=1).timeseries(indexes=slice(None)).q_pump
            # echter, dit geeft nu een: "IndexError: boolean index did not
            # match indexed array along dimension 1; dimension is 20 but
            # corresponding boolean dimension is 19"

            # ter achtergrond info:
            # v2_bergermeer heeft 18 v2_pumpstations
            # v2_bergermeer heeft 19 pumplines (export functie is goed!)

            # vanwege indexerror daarom tijdelijke hack:
            # dit werkt: gr.pumps.q_pump[:,1:].shape --> (10, 19)
            # echter dit werkt niet: gr.pumps.filter(id=1).q_pump[:,1:]
            # dus de id array moeten we ook gaan slicen
            # ff nieuwe array bouwen (v2_bergermeer id = {1, 2, .., 18, 19}
            id_array = gr_model_instance_subset.id
            # dan kunnen we vervolgens bijv doen:
            # gr.pumps.timeseries(indexes=slice(None)).q_pump
            subset_ncvar = getattr(gr_model_instance_subset, nc_variable)

            # gr.pumps.timeseries(indexes=slice(None)).q_pump[:, 1:][:,
            # id_array == 3]
            ncvar_filter = subset_ncvar[:, 1:][:, id_array == object_id]
            # flatten numpyarray
            vals = ncvar_filter.flatten()
            # Todo:
            # wait for Jelle/Lars to fix this IndexError in threedigrid,
            # so that we can do the normal way (maybe also using content_pk
            # instead of id?
        else:
            raise ValueError('object_type not available')
        return vals

    def _get_timeseries_result_layer(self, object_type, object_id,
                                     nc_variable):
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
        gr_model_instance = getattr(self.gridadmin_result, model_instance)

        if model_instance in ['nodes', 'lines']:
            # gr.nodes.filter(id=100).timeseries(indexes=slice(None))
            filter_timeseries = gr_model_instance.filter(
                id=object_id).timeseries(indexes=slice(None))
            # gr.nodes.filter(id=100).timeseries(indexes=slice(None)).vol
            filter_timeseries_ncvar = getattr(filter_timeseries, nc_variable)
            # flatten numpyarray
            vals = filter_timeseries_ncvar.flatten()
        elif model_instance == 'pumps':
            # gr.pumps.timeseries(indexes=slice(None))
            timeseries = gr_model_instance.timeseries(
                indexes=slice(None))

            # tijdelijke hack omdat threedigrid indexerrors geeft op pumps
            # --------------------------------------------------
            # normaalgesproken zou dit werken:
            # gr.pumps.filter(id=1).timeseries(indexes=slice(None)).q_pump
            # echter, dit geeft nu een: "IndexError: boolean index did not
            # match indexed array along dimension 1; dimension is 20 but
            # corresponding boolean dimension is 19"

            # ter achtergrond info:
            # v2_bergermeer heeft 18 v2_pumpstations
            # v2_bergermeer heeft 19 pumplines (export functie is goed!)

            # vanwege indexerror daarom tijdelijke hack:
            # dit werkt: gr.pumps.q_pump[:,1:].shape --> (10, 19)
            # echter dit werkt niet: gr.pumps.filter(id=1).q_pump[:,1:]
            # dus de id array moeten we ook gaan slicen
            # ff nieuwe array bouwen
            # id_array = gr.pumps.id # --> is id 1 tm 19
            id_array = gr_model_instance.id
            # dan kunnen we vervolgens bijv doen:
            # gr.pumps.timeseries(indexes=slice(None)).q_pump
            timeseries_ncvar = getattr(timeseries, nc_variable)
            # gr.pumps.timeseries(indexes=slice(None)).q_pump[:, 1:][:,
            # id_array == 3]
            filter = timeseries_ncvar[:, 1:][:, id_array == object_id]
            # flatten numpyarray
            vals = filter.flatten()
            # Todo:
            # wait for Jelle/Lars to fix this IndexError in threedigrid,
            # so that we can do the normal way (maybe also using content_pk
            # instead of id?
        else:
            raise ValueError('object_type not available')
        return vals

    def get_timeseries(
            self, object_type, object_id, nc_variable, fill_value=None):

        # determine if layer is a not_schematized (e.g nodes, pumps)
        if object_type_layer_source[object_type] == 'result':
            values = self._get_timeseries_result_layer(
                object_type, object_id, nc_variable)
        elif object_type_layer_source[object_type] == 'schematized':
            values = self._get_timeseries_schematisation_layer(
                object_type, object_id, nc_variable)

        msg = "{object_id} object_id and {object_type} object_type and " \
              "{nc_variable} nc_variable".format(object_id=object_id,
                                                 object_type=object_type,
                                                 nc_variable=nc_variable)
        log.debug(msg)

        # Zip timeseries together in (n,2) array
        if fill_value is not None and type(values) == \
                np.ma.core.MaskedArray:
            filled_vals = values.filled(fill_value)
            return np.vstack((self.timestamps, filled_vals)).T
        else:
            return np.vstack((self.timestamps, values)).T

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

    @cached_property
    def gridadmin_aggregate_result(self):
        from ..datasource.netcdf import find_h5_file, find_aggregation_netcdf
        from ..utils.patched_threedigrid import GridH5AggregateResultAdmin
        try:
            agg_path = find_aggregation_netcdf(self.file_path)
            h5 = find_h5_file(self.file_path)
            return GridH5AggregateResultAdmin(h5, agg_path)
        except IndexError:
            return None
