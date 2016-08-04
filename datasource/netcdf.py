import glob
import json
import os

from netCDF4 import Dataset
import numpy as np

from ..utils.user_messages import log
from ..utils import cached_property
from .result_spatialite import get_object_type, get_variables


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


class NetcdfDataSource(object):
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

    def __init__(self, file_path, load_properties=True):
        """
        Args:
            file_path: path to result netcdf
        """
        self.file_path = file_path
        # Load netcdf
        self.ds = Dataset(self.file_path, mode='r', format='NETCDF4')
        log("Opened netcdf: %s" % self.file_path)
        self.cache = dict()

        if load_properties:
            self.load_properties()

    def load_properties(self):
        """Load and pre-calculate some properties.

        Note: these properties are required for get_node_type and
        get_line_type to work.
        """
        # Nodes
        self.n2dtot = self.ds.nFlowElem2d
        self.n1dtot = self.ds.nFlowElem1d
        self.n2dobc = self.ds.nFlowElem2dBounds
        self.end_n1dtot = self.n2dtot + self.n1dtot
        self.end_n2dobc = self.n2dtot + self.n1dtot + self.n2dobc
        self.nodall = self.ds.nFlowElem
        # Links
        self.nFlowLine2d = self.ds.nFlowLine2d
        self.nFlowLine = self.ds.nFlowLine
        self.end_2d_bound_line = self.nFlowLine - self.ds.nFlowLine1dBounds
        self.end_1d_line = (self.nFlowLine - self.ds.nFlowLine2dBounds -
                            self.ds.nFlowLine1dBounds)

    @property
    def id_mapping_file(self):
        return find_id_mapping_file(self.file_path)

    @cached_property
    def id_mapping(self):
        # Load id mapping
        with open(self.id_mapping_file) as f:
            return json.load(f)

    @property
    def aggregation_netcdf_file(self):
        return find_aggregation_netcdf(self.file_path)

    @cached_property
    def ds_aggregation(self):
        """The aggregation netcdf dataset."""
        # Load aggregation netcdf
        log("Opening aggregation netcdf: %s" % self.aggregation_netcdf_file)
        return Dataset(self.aggregation_netcdf_file, mode='r',
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

    @property
    def metadata(self):
        pass

    def get_timestamps(self, object_type=None, parameter=None):
        return self.ds.variables['time'][:]

    def get_object_types(self, parameter=None):
        pass

    def get_objects(self, object_type):
        pass

    def get_object_count(self, object_type):
        pass

    def get_parameters(self, object_type=None):
        pass

    def get_object(self, object_type, object_id):
        pass

    def get_inp_id(self, object_id, normalized_object_type):
        """Get the id mapping dict correctly and then return the mapped id,
        aka: the inp_id"""
        try:
            # This is the sewerage situation
            obj_id_mapping = self.id_mapping[normalized_object_type]
        except KeyError:
            # This is the v2 situation
            # TODO: another v2 <-> sewerage difference...
            log("id_mapping json v2 <-> sewerage naming discrepancy",
                level='WARNING')
            v2_object_type = 'v2_' + normalized_object_type
            obj_id_mapping = self.id_mapping[v2_object_type]
        return obj_id_mapping[str(object_id)]  # strings because JSON

    def get_netcdf_id(self, inp_id, object_type):
        """Get the node or flow link id needed to get data from netcdf."""
        # Note: because pumpstation uses q_pump it also has a special way of
        # accessing that array.
        if object_type in ['pumpstation']:
            return inp_id - 1
        elif object_type in ['manhole', 'connection_nodes']:
            return self.node_mapping[inp_id]
        else:
            return self.channel_mapping[inp_id]

    def get_node_type(self, node_idx):
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

    def get_line_type(self, line_idx):
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
            netcdf_id = object_id - 1
        else:
            # Mapping: spatialite id -> inp id -> netcdf id
            inp_id = self.get_inp_id(object_id, normalized_object_type)
            netcdf_id = self.get_netcdf_id(inp_id, normalized_object_type)
        return netcdf_id

    def get_timeseries(self, object_type, object_id, parameters, start_ts=None,
                       end_ts=None):
        """Get a list of time series from netcdf.

        Note: if there are multiple parameters, all result values are just
        lumped together and returned. If a parameter is unknown it will be
        skipped.

        Args:
            object_type: e.g. 'v2_weir'
            object_id: spatialite id
            parameters: a list of params, e.g.: ['q', 'q_pump']

        Returns:
            a list of 2-tuples (time, value)
        """
        # Normalize the name
        n_object_type = get_object_type(object_type)

        # Derive the netcdf id
        netcdf_id = self.obj_to_netcdf_id(object_id, n_object_type)

        variables = get_variables(n_object_type, parameters)

        # Get data from all variables and just put them in the same list:
        result = []
        for v in variables:
            try:
                vals = self.ds.variables[v][:, netcdf_id]
            except KeyError:
                log("Variable not in netCDF: %s, skipping..." % v)
                continue
            except IndexError:
                log("Netcdf id %s not found for %s" % (netcdf_id, v))
                continue
            timestamps = self.get_timestamps()
            result += zip(timestamps, vals)

        return result

    def get_timeseries_values(self, object_type, object_id, parameters,
                              source='default', caching=True):
        """Get a list of time series from netcdf; only the values.

        Note: if there are multiple parameters, all result values are just
        lumped together and returned. If a parameter is unknown it will be
        skipped.

        Note 2: source defines the netcdf file source we should get our data
        from, because the NetcdfDataSource can contain the default netcdf
        but also an aggregation netcdf.

        Args:
            object_type: e.g. 'v2_weir'
            object_id: spatialite id
            parameters: a list of params, e.g.: ['q', 'q_pump']
            source: the netcdf source type, i.e., 'default' (subgrid_map.nc)
                or 'aggregation' (flow_aggregate.nc)
            caching: if True, keep netcdf array in memory

        Important note: using True instead of False as a default for the
        'caching' kwarg makes this method much faster. Branch prediction?

        Returns:
            an array of values
        """
        # TODO: remove the lumping together of arrays of multiple parameters
        # feature, because that's probably really UNWANTED
        # Just do one parameter!

        # Normalize the name
        n_object_type = get_object_type(object_type)

        # Derive the netcdf id
        netcdf_id = self.obj_to_netcdf_id(object_id, n_object_type)

        variables = get_variables(n_object_type, parameters)
        if len(variables) > 1:
            log("Warning! More than one variable used in getting the "
                "time series! Not sure if you'd want this!", level='CRITICAL')
            raise ValueError("More than one variable used, proceed with "
                             "caution!")

        # Select the source netcdf:
        if source == 'default':
            ds = self.ds
        elif source == 'aggregation':
            ds = self.ds_aggregation
        else:
            raise ValueError("Unexpected source type %s", source)

        # Get data from all variables and just put them in the same list:
        timeseries_vals = np.array([])
        for v in variables:

            # Keep the netCDF array in memory for performance
            if caching:
                try:
                    variable = self.cache[v]
                except KeyError:
                    try:
                        variable = ds.variables[v][:]  # make copy
                        self.cache[v] = variable
                    except KeyError:
                        log("Variable not in netCDF: %s, skipping..." % v)
                        continue
            else:
                variable = ds.variables[v][:]

            try:
                # shape ds.variables['q'] array = (t, number of ids)
                vals = variable[:, netcdf_id]
            except KeyError:
                log("Variable not in netCDF: %s, skipping..." % v)
                continue
            except IndexError:
                log("Id %s not found for %s" % (netcdf_id, v))
                continue
            timeseries_vals = np.hstack((timeseries_vals, vals))
        return timeseries_vals
