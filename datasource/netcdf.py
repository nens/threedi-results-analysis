from collections import namedtuple
import glob
from itertools import (starmap, product)
import json
import os

import numpy as np

from .base import BaseDataSource
from ..utils.user_messages import log
from ..utils import cached_property

# Explanation: aggregation using the cumulative method integrates the variable
# over time. Therefore the units must be multiplied by the time also.
CUMULATIVE_AGGREGATION_UNITS = {
    's1': 'm MSL',
    'q': 'm3',
    'u1': 'm',
    'vol': 'm3',
    'q_pump': 'm3',
    'qp': 'm3',
    'up1': 'm',
    'qlat': 'm3',
    'vol1': 'm3',
    'rain': 'm3',
    'infiltration_rate': 'm3',
    'su': '',
    'au': '',
}


# NetCDF variable information
NcVar = namedtuple('NcVar', ['name', 'verbose_name', 'unit'])

WATERLEVEL = NcVar('s1', 'waterlevel', 'm MSL')
DISCHARGE = NcVar('q', 'discharge', 'm3/s')
VELOCITY = NcVar('u1', 'velocity', 'm/s')
# Volume is called 'vol' in subgrid_map.nc but 'vol1' in the aggregation
# netcdf
VOLUME = NcVar('vol', 'volume', 'm3')
VOLUME_AGG = NcVar('vol1', 'volume', 'm3')
DISCHARGE_PUMP = NcVar('q_pump', 'discharge pump', 'm3/s')
DISCHARGE_INTERFLOW = NcVar('qp', 'discharge interflow', 'm3/s')
DISCHARGE_LATERAL = NcVar('q_lat', 'discharge lateral', 'm3/s')
VELOCITY_INTERFLOW = NcVar('up1', 'velocity interflow', 'm/s')
RAIN_INTENSITY = NcVar('rain', 'rain intensity', 'm3/s')
WET_SURFACE_AREA = NcVar('su', 'wet surface area', 'm2')
INFILTRATION = NcVar('infiltration_rate', 'infiltration rate', 'm3/s')
WET_CROSS_SECTION_AREA = NcVar('au', 'wet cross section area', 'm2')

_Q_TYPES = [
    DISCHARGE,
    DISCHARGE_INTERFLOW,
    DISCHARGE_PUMP,
    VELOCITY,
    VELOCITY_INTERFLOW,
    WET_CROSS_SECTION_AREA,
]

_H_TYPES = [
    WATERLEVEL,
    VOLUME,
    RAIN_INTENSITY,
    WET_SURFACE_AREA,
    INFILTRATION,
    DISCHARGE_LATERAL,
]

Q_TYPES = [v.name for v in _Q_TYPES]
H_TYPES = [v.name for v in _H_TYPES]

SUBGRID_MAP_VARIABLES = _Q_TYPES + _H_TYPES  # just take all variables..
AGGREGATION_VARIABLES = [
    DISCHARGE,
    DISCHARGE_INTERFLOW,
    DISCHARGE_PUMP,
    VELOCITY,
    VELOCITY_INTERFLOW,
    WATERLEVEL,
    VOLUME_AGG,  # this is the only difference with SUBGRID_MAP_VARIABLES
    RAIN_INTENSITY,
    WET_SURFACE_AREA,
    INFILTRATION,
    DISCHARGE_LATERAL,
]

AGGREGATION_OPTIONS = {
    'min', 'max', 'avg', 'med', 'cum', 'cum_positive', 'cum_negative'}


layer_information = [
    # layer name, (normalized) object_type, q/h type

    # Note: the reason why this is plural is because this is (inconsistently)
    # also plural in the id mapping json, in contrast to all other object
    # types
    ('v2_connection_nodes', 'connection_nodes', 'h'),
    ('v2_pipe_view', 'pipe', 'q'),
    ('v2_channel', 'channel', 'q'),
    ('v2_culvert_view', 'culvert', 'q'),
    ('v2_pumpstation', 'pumpstation', 'q'),
    ('v2_pumpstation_view', 'pumpstation', 'q'),
    ('v2_weir_view', 'weir', 'q'),
    ('v2_orifice_view', 'orifice', 'q'),
    ('sewerage_manhole', 'manhole', 'h'),
    ('sewerage_pipe_view', 'pipe', 'q'),
    ('sewerage_pumpstation', 'pumpstation', 'q'),
    ('sewerage_pumpstation_view', 'pumpstation', 'q'),
    ('sewerage_weir_view', 'weir', 'q'),
    ('sewerage_orifice_view', 'orifice', 'q'),
    ('flowlines', 'flowline', 'q'),
    ('nodes', 'node', 'h'),
    ('pumplines', 'pumpline', 'q'),
    ('line_results', 'flowline', 'q'),
    ('node_results', 'node', 'h'),

]

layer_object_type_mapping = dict([(a[0], a[1]) for a in layer_information])
layer_qh_type_mapping = dict([(a[0], a[2]) for a in layer_information])


def normalized_object_type(current_layer_name):
    """Get a normalized object type for internal purposes."""
    if current_layer_name in layer_object_type_mapping.keys():
        return layer_object_type_mapping[current_layer_name]
    else:
        msg = "Unsupported layer: %s." % current_layer_name
        log(msg, level='WARNING')
        return None


def find_id_mapping_file(netcdf_file_path):
    """An ad-hoc way to get the id_mapping file.

    We assume the id_mapping file is in on of the following locations (note:
    this order is also the searching order):

    1) . (in the same dir as the netcdf)
    2) ../input_generated

    relative to the netcdf file and that it starts with 'id_mapping'.

    Args:
        netcdf_file_path: path to the result netcdf

    Returns:
        id_mapping file path

    Raises:
        IndexError if nothing is found
    """
    pattern = 'id_mapping*'
    inpdir = os.path.join(os.path.dirname(netcdf_file_path),
                          '..', 'input_generated')
    resultdir = os.path.dirname(netcdf_file_path)

    from_inpdir = glob.glob(os.path.join(inpdir, pattern))
    from_resultdir = glob.glob(os.path.join(resultdir, pattern))

    inpfiles = from_resultdir + from_inpdir
    return inpfiles[0]

def find_h5_file(netcdf_file_path):
    """An ad-hoc way to get the h5_file.

    We assume the h5_file file is in on of the following locations (note:
    this order is also the searching order):

    1) . (in the same dir as the netcdf)
    2) ../preprocessed

    relative to the netcdf file and has extension '.h5'

    Args:
        netcdf_file_path: path to the result netcdf

    Returns:
        h5_file path

    Raises:
        IndexError if nothing is found
    """
    pattern = '*.h5'
    inpdir = os.path.join(os.path.dirname(netcdf_file_path),
                          '..', 'preprocessed')
    resultdir = os.path.dirname(netcdf_file_path)

    from_inpdir = glob.glob(os.path.join(inpdir, pattern))
    from_resultdir = glob.glob(os.path.join(resultdir, pattern))

    inpfiles = from_resultdir + from_inpdir
    return inpfiles[0]


def find_aggregation_netcdf(netcdf_file_path):
    """An ad-hoc way to find the aggregation netcdf file.

    It is assumed that the file is called 'flow_aggregate.nc' and in the same
    directory as the 'regular' result netcdf.

    Args:
        netcdf_file_path: path to the result netcdf

    Returns:
        the aggregation netcdf path

    Raises:
        IndexError if nothing is found
    """
    pattern = 'flow_aggregate.nc'
    result_dir = os.path.dirname(netcdf_file_path)
    return glob.glob(os.path.join(result_dir, pattern))[0]


# TODO: this function doesn't work correctly because multiple links can
# belong to one inp id.
# I.e.: dict(cm) is wrong, because len(dict(cm)) != len(cm)
def construct_channel_mapping(ds):
    """Map inp ids to flowline ids.

    Note that you need to subtract 1 from the resulting flowline id because of
    Python's 0-based indexing array (versus Fortran's 1-based indexing). These
    flowline ids are used for  pipes, weirs and orifices.
    """
    cm = np.copy(ds.variables['channel_mapping'])
    cm[:, 1] = cm[:, 1] - 1  # the index transformation
    # TODO: not a dict anymore, needs changing other places
    return dict(cm)
    # return cm


def construct_node_mapping(ds):
    """Map inp ids to node ids.

    Note that you need to subtract 1 from the resulting node id because of
    Python's 0-based indexing array (versus Fortran's 1-based indexing). These
    node ids are used for manholes.
    """
    cm = np.copy(ds.variables['node_mapping'])
    cm[:, 1] = cm[:, 1] - 1  # the index transformation
    return dict(cm)


def get_timesteps(ds):
    """Timestep determination using consecutive element difference"""
    return np.ediff1d(ds.variables['time'])


# Note: copied from threedi codebase
def product_and_concat(variables, aggregation_options=AGGREGATION_OPTIONS):
    """Make combinatons with cartesian product and concatenate the pairs
    with an underscore.

    Returns:
        the combinations as an iterable

    >>> sorted(list(product_and_concat(['a'], ['b'])))
    ['a_b']
    >>> sorted(product_and_concat(['a', 'b'], ['c']))
    ['a_c', 'b_c']
    >>> sorted(product_and_concat(['a'], ['b', 'c']))
    ['a_b', 'a_c']
    >>> sorted(product_and_concat(['a', 'b'], ['c', 'd']))
    ['a_c', 'a_d', 'b_c', 'b_d']
    >>> sorted(product_and_concat('q'))
    ['q_avg', 'q_cum', 'q_cum_negative', 'q_cum_positive', 'q_max', 'q_med',\
 'q_min']
    """
    prods = product(variables, aggregation_options)
    nc_vars = starmap(lambda x, y: '%s_%s' % (x, y), prods)
    return nc_vars


class NetcdfDataSource(BaseDataSource):
    """This netCDF datasource combines three things:

    1. the regular 3Di result netcdf: subgrid_map.nc
    2. the spatialite mappings from id_mapping.json
    3. the aggregation netcdf flow_aggregate.nc

    To initialize this class only the subgrid_map.nc netcdf is required though,
    the locations of the other two files can be derived from it. Furthermore,
    the other files should be lazily loaded because they are not required in
    all use cases and/or they are not always available. In the latter case you
    will still want the parts of your program to work that DO NOT require the
    additional files. However, if you DO want to enforce these files to be
    required, you can do so by checking them using the helper functions
    'find_id_mapping_file' and 'find_aggregation_netcdf'.
    """

    def __init__(self, file_path, load_properties=True, ds=None):
        """
        Args:
            file_path: path to result netcdf
            load_properties: call load_properties
            ds: netCDF4.Dataset, optional (useful for tests)
        """
        # Note: we don't want module level imports of dynamically loaded
        # libraries because importing them will cause files to be held open
        # which cause trouble when updating the plugin. Therefore we delay
        # the import as much as possible.
        from netCDF4 import Dataset

        self.file_path = file_path
        # Load netcdf
        if not ds:
            self.ds = Dataset(self.file_path, mode='r', format='NETCDF4')
            log("Opened netcdf: %s" % self.file_path)
        else:
            self.ds = ds
        self.cache = dict()

        if load_properties:
            self.load_properties()

    def load_properties(self):
        """Load and pre-calculate some properties.

        Note: these properties are required for node_type_of and
        line_type_of to work.
        """
        # Nodes
        self.n2dtot = getattr(self.ds, 'nFlowElem2d', 0)
        self.n1dtot = getattr(self.ds, 'nFlowElem1d', 0)
        self.n2dobc = getattr(self.ds, 'nFlowElem2dBounds', 0)
        self.end_n1dtot = self.n2dtot + self.n1dtot
        self.end_n2dobc = self.n2dtot + self.n1dtot + self.n2dobc
        self.nodall = getattr(self.ds, 'nFlowElem', 0)
        # Links
        self.nFlowLine2d = getattr(self.ds, 'nFlowLine2d', 0)
        self.nFlowLine = getattr(self.ds, 'nFlowLine', 0)
        self.nFlowLine1dBounds = getattr(self.ds, 'nFlowLine1dBounds', 0)
        self.nFlowLine2dBounds = getattr(self.ds, 'nFlowLine2dBounds', 0)
        self.end_2d_bound_line = self.nFlowLine - self.nFlowLine1dBounds
        self.end_1d_line = (self.nFlowLine - self.nFlowLine2dBounds -
                            self.nFlowLine1dBounds)
        assert (
            self.end_n1dtot <= self.end_n2dobc <= self.nodall
        ), "Inconsistent node attribute values in netCDF"
        assert (
            self.end_1d_line <= self.end_2d_bound_line <= self.nFlowLine
        ), "Inconsistent line attribute values in netCDF"

    @cached_property
    def id_mapping(self):
        # Load id mapping
        with open(find_id_mapping_file(self.file_path)) as f:
            return json.load(f)

    @cached_property
    def ds_aggregation(self):
        """The aggregation netcdf dataset."""
        # Note: we don't want module level imports of dynamically loaded
        # libraries because importing them will cause files to be held open
        # which cause trouble when updating the plugin. Therefore we delay
        # the import as much as possible.
        from netCDF4 import Dataset

        # Load aggregation netcdf
        aggregation_netcdf_file = find_aggregation_netcdf(self.file_path)
        log("Opening aggregation netcdf: %s" % aggregation_netcdf_file)
        return Dataset(aggregation_netcdf_file, mode='r',
                       format='NETCDF4')

    @cached_property
    def channel_mapping(self):
        return construct_channel_mapping(self.ds)

    @cached_property
    def node_mapping(self):
        return construct_node_mapping(self.ds)

    @cached_property
    def timesteps(self):
        return get_timesteps(self.ds)

    @cached_property
    def timestamps(self):
        return self.get_timestamps()

    @cached_property
    def available_subgrid_map_vars(self):
        return self.get_available_variables(only_subgrid_map=True)

    @cached_property
    def available_aggregation_vars(self):
        return self.get_available_variables(only_aggregation=True)

    @property
    def metadata(self):
        pass

    def get_timestamps(self, object_type=None, parameter=None):
        # todo: object_type can be removed
        if parameter is None:
            return self.ds.variables['time'][:]
        elif parameter in [v[0] for v in SUBGRID_MAP_VARIABLES]:
            return self.ds.variables['time'][:]
        else:
            return self.get_agg_var_timestamps(parameter)

    def get_agg_var_timestamps(self, aggregation_variable_name):
        """Get timestamps for aggregation variables.

        Example: for 's1_max' the time variable name is 'time_s1_max'.
        """
        time_var_name = 'time_%s' % aggregation_variable_name
        return self.ds_aggregation.variables[time_var_name][:]

    def get_available_variables(self, only_subgrid_map=False,
                                only_aggregation=False):
        """Query the netCDF files and get all variables which we can retrieve
        data for.

        Returns:
            a dict with entries for subgrid_map and aggregation vars
        """
        do_all = not any([only_subgrid_map, only_aggregation])
        available_vars = []

        if do_all or only_subgrid_map:
            possible_subgrid_map_vars = [v for v, _, _ in
                                         SUBGRID_MAP_VARIABLES]
            subgrid_map_vars = self.ds.variables.keys()
            available_subgrid_map_vars = [v for v in possible_subgrid_map_vars
                                          if v in subgrid_map_vars]
            available_vars += available_subgrid_map_vars
        if do_all or only_aggregation:
            possible_agg_vars = [product_and_concat([v]) for v, _, _ in
                                 AGGREGATION_VARIABLES]
            # This flattens the list of lists
            possible_agg_vars = [item for sublist in possible_agg_vars for
                                 item in sublist]
            try:
                agg_vars = self.ds_aggregation.variables.keys()
                available_agg_vars = [v for v in possible_agg_vars if v in
                                      agg_vars]
                available_vars += available_agg_vars
            except IndexError:
                # If we're here it means no agg. netCDF was found. Fail without
                # error, but do log it.
                log("No aggregation netCDF was found, only the data from the "
                    "regular netCDF will be used.", level='WARNING')
        return available_vars

    def get_object(self, object_type, object_id):
        pass

    def inp_id_from(self, object_id, normalized_object_type):
        """Get the id mapping dict correctly and then return the mapped id,
        aka: the inp_id"""
        try:
            # This is the v2 situation
            v2_object_type = 'v2_%s' % normalized_object_type
            obj_id_mapping = self.id_mapping[v2_object_type]
        except KeyError:
            # This is the sewerage situation
            obj_id_mapping = self.id_mapping[normalized_object_type]
        return obj_id_mapping[str(object_id)]  # strings because JSON

    def netcdf_id_from(self, inp_id, object_type):
        """Get the node or flow link id needed to get data from netcdf."""
        # Note: because pumpstation uses q_pump it also has a special way of
        # accessing that array.
        if object_type in ['pumpstation']:
            return inp_id - 1
        elif object_type in ['manhole', 'connection_nodes']:
            return self.node_mapping[inp_id]
        else:
            return self.channel_mapping[inp_id]

    def node_type_of(self, node_idx):
        """Get the node type based on its index."""
        # Order of nodes in netCDF is:
        # 1. nFlowElem2d
        # 2. nFlowElem1d
        # 3. nFlowElem2dBounds
        # 4. nFlowElem1dBounds
        #    ----------------- +
        #    nFlowElem
        if node_idx < self.n2dtot:
            return '2d'
        elif node_idx < self.end_n1dtot:
            return '1d'
        elif node_idx < self.end_n2dobc:
            return '2d_bound'
        elif node_idx < self.nodall:
            return '1d_bound'
        else:
            raise ValueError(
                "Index %s is not smaller than the number of nodes (%s)" %
                (node_idx, self.nodall))

    def line_type_of(self, line_idx):
        """Get line type based on its index."""
        # Order of links in netCDF is:
        # - 2d links (x and y) (nr: part of ds.ds.nFlowLine2d)
        # - 1d links (nr: ds.ds.nFlowLine1d)
        # - 1d-2d links (nr: part of ds.ds.nFlowLine2d)
        # - 2d bound links (nr: ds.ds.nFlowLine2dBounds)
        # - 1d bound links (nr: ds.ds.nFlowLine1dBounds)
        if line_idx < self.nFlowLine2d:
            return '2d'
        elif line_idx < self.end_1d_line:
            return '1d'
        elif line_idx < self.end_2d_bound_line:
            return '2d_bound'
        elif line_idx < self.nFlowLine:
            return '1d_bound'
        else:
            raise ValueError(
                "Index %s is not smaller than the number of lines (%s)" %
                (line_idx, self.nFlowLine))

    def obj_to_netcdf_id(self, object_id, normalized_object_type):
        # Here we map the feature ids (== object ids) to internal netcdf ids.
        # Note: 'flowline' and 'node' are memory layers that are made from the
        # netcdf, so they don't need an id mapping or netcdf mapping
        if normalized_object_type in ['flowline', 'node', 'pumpline']:
            # TODO: need to test this id to make sure (-1/+1??)!!
            netcdf_id = object_id
        else:
            # Mapping: spatialite id -> inp id -> netcdf id
            inp_id = self.inp_id_from(object_id, normalized_object_type)
            netcdf_id = self.netcdf_id_from(inp_id, normalized_object_type)
        return netcdf_id

    def get_timeseries(self, object_type, object_id, variable, start_ts=None,
                       end_ts=None, fill_value=None):
        """Get a list of time series from netcdf.

        Args:
            object_type: e.g. 'v2_weir'
            object_id: spatialite id
            variable: variable name e.g.: 'q', 'q_pump', etc.
            fill_value: value returned for masked values

        Returns:
            a (n,2) array; with in the first column the timestamps and second
            column the values
        """
        # Normalize the name
        n_object_type = normalized_object_type(object_type)
        # Derive the netcdf id
        netcdf_id = self.obj_to_netcdf_id(object_id, n_object_type)

        # Get values
        if variable in self.available_subgrid_map_vars:
            ds = self.ds
            timestamps = self.timestamps
        elif variable in self.available_aggregation_vars:
            ds = self.ds_aggregation
            timestamps = self.get_agg_var_timestamps(variable)
        else:
            raise ValueError("Invalid variable: %s" % variable)

        try:
            vals = ds.variables[variable][:, netcdf_id]
        except KeyError:
            log("Variable not in netCDF: %s" % variable)
            raise
        except IndexError:
            log("Id %s not found for %s" % (netcdf_id, variable))
            raise

        # Zip timeseries together in (n,2) array
        if fill_value is not None and type(vals) == np.ma.core.MaskedArray:
            vals = vals.filled(fill_value)
        return np.vstack((timestamps, vals)).T

    def get_values_by_ids(self, variable, object_type, object_ids,
                          caching=True):
        """Get timeseries values by one or more object ids.

        Args:
            object_type: e.g. 'v2_weir'
            object_ids: a list of spatialite ids
            variable: variable name, e.g.: 'q', 'q_pump'
            caching: if True, keep netcdf array in memory

        Important note: using True instead of False as a default for the
        'caching' kwarg makes this method much faster. Branch prediction?

        Returns:
            a (t, n) array, with t=number of timestamps, and n=number of
            object ids. For just one object_id n=1. For multiple object
            ids the array selection is in the same order as the order of
            the object ids, i.e., no sorting takes place before slicing.
        """
        # Normalize the name
        n_object_type = normalized_object_type(object_type)

        # Derive the netcdf id
        netcdf_ids = range(len(object_ids))  # init a list
        for i, obj_id in enumerate(object_ids):
            netcdf_ids[i] = self.obj_to_netcdf_id(obj_id, n_object_type)
        # netcdf_id = self.obj_to_netcdf_id(object_id, n_object_type)

        # Select the source netcdf:
        if variable in self.available_subgrid_map_vars:
            ds = self.ds
        elif variable in self.available_aggregation_vars:
            ds = self.ds_aggregation
        else:
            raise ValueError("Invalid variable: %s" % variable)

        # Keep the netCDF array in memory for performance
        if caching:
            try:
                data = self.cache[variable]
            except KeyError:
                data = ds.variables[variable][:]  # make copy
                self.cache[variable] = data
        else:
            data = ds.variables[variable][:]

        try:
            # shape ds.variables['q'] array = (t, number of ids)
            vals = data[:, netcdf_ids]
        except KeyError:
            log("Variable not in netCDF: %s" % variable)
            raise
        except IndexError:
            log("Id %s not found for %s" % (netcdf_ids, variable))
            raise
        return vals

    def get_values_by_id(self, variable, object_type, object_id, caching=True):
        """Convenience method to get a regular array if only one ID is needed.
        """
        vals = self.get_values_by_ids(variable=variable,
                                      object_type=object_type,
                                      object_ids=[object_id],
                                      caching=caching)
        # Convert row array to regular array.
        return vals[:, 0]

    def get_values_by_timestep_nr(self, variable, timestamp_idx, index=None):
        """Horizontal slice over the element indices, i.e., get all values for
        all nodes or flowlines for a specific timestamp.

        Args:
            variable: the netCDF variable name
            timestamp_idx: timestamp index
            index: array of elements to be read
        """
        if variable in self.available_subgrid_map_vars:
            ds = self.ds
        elif variable in self.available_aggregation_vars:
            ds = self.ds_aggregation
        else:
            # todo: warning
            return
        if index is not None:
            return ds.variables[variable][timestamp_idx, index]
        else:
            return ds.variables[variable][timestamp_idx, :]
