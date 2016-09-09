import os
import csv
import logging
from .ncstats import NcStats, NcStatsAgg
from ..utils.user_messages import log

log = logging.getLogger(__name__)


def get_default_csv_path(layer_name, result_dir):
    """The default file path the stats generating functions in this module
    write to."""
    filename = layer_name + '_stats.csv'
    return os.path.join(result_dir, filename)


def _calc_results(
        ncstats, parameters, layer_name, feature_id,
        surface_level=None, bottom_level=None):
    """Calcs results for all parameters and puts them in a dict (used in
    generate_manhole_stats)

    Args:
        ncstats: NcStats instance
        parameters: a list of (netCDF) parameters
        layer_name: the name of the layer we want to query results for
        feature_id: feature id (is related to the layer_name)
        surface_level: an additional parameter that is needed for
            calculating 'wos_height'
        bottom_level: an additional parameter that is needed for calculing
            'water_depth'

    Note: when the last two kwargs are missing, the results cannot be
    calculated and are simply set to None

    Returns:
        a dictionary {param_name: result_value, ...}
    """
    result = dict()
    for param_name in parameters:
        # Business as usual (NcStats method)
        try:
            result[param_name] = \
                ncstats.get_value_from_parameter(
                    layer_name, feature_id, param_name,
                    surface_level=surface_level,
                    bottom_level=bottom_level)
        except (ValueError, IndexError, AttributeError):
            result[param_name] = None
        except TypeError:
            # Probably an error with wos_duration, which
            # will ONLY work for structures with a surface_level (
            # i.e. manholes).
            result[param_name] = None
    return result


def get_manhole_layer_id_name(layer_name):
    """Get the primary key name of the layer (only node layers!)"""
    if layer_name == 'nodes':
        # It's a memory layer
        layer_id_name = 'id'
    elif 'v2' in layer_name:
        # It's a v2 spatialite layer
        layer_id_name = 'id'
    else:
        # It's sewerage spatialite (no agg. netcdf)
        layer_id_name = 'id'
    return layer_id_name


def get_structure_layer_id_name(layer_name):
    """Get the primary key name of the layer (only line/structure layers!)"""
    if layer_name == 'flowlines':
        layer_id_name = 'id'
    else:
        # It's a view
        layer_id_name = 'ROWID'
    return layer_id_name


def get_pump_layer_id_name(layer_name):
    """Get the primary key name of the layer (only pump layers!)"""
    if layer_name == 'pumplines':
        layer_id_name = 'id'
    else:
        # It's a view
        layer_id_name = 'ROWID'
    return layer_id_name


def generate_manhole_stats(nds, result_dir, layer, layer_id_name,
                           include_2d=True):
    """Generate stats for manhole like objects and write to csv.

    Args:
        nds: NetcdfDataSource
        result_dir: output directory
        layer: qgis layer
        layer_id_name: the pk of the layer
        include_2d: include 2d features (only applicable for lines)

    Returns:
        filepath generated csv
    """

    # node-like layers for which this script works (without the 'v2_' or
    # 'sewerage_' prefix)
    NODE_OBJECTS = ['manhole', 'connection_node', 'node']

    layer_name = layer.name()
    if not any(s in layer_name for s in NODE_OBJECTS):
        raise ValueError("%s is not a valid node layer" % layer_name)

    # Caution: approaching HACK territory!
    # Motivation: This is a hack for v2_manholes. Manholes just have a
    # foreign key to v2_connection_nodes and aren't a thing in itself.
    # So all v2_manhole stuff should be delegated to the way
    # v2_connection_nodes works.
    old_layer_name = layer_name
    if layer_name == 'v2_manhole':
        layer_name = 'v2_connection_nodes'

    # TODO: not sure if we want to make ncstats distinction based on
    # the layer type
    if layer_name == 'nodes':
        try:
            ncstats = NcStatsAgg(datasource=nds)
        except IndexError:
            log.error('No aggregation netcdf available for statistics')
            ncstats = NcStats(datasource=nds)

    elif 'v2' in layer_name:
        # It's a v2 spatialite layer
        try:
            ncstats = NcStatsAgg(datasource=nds)
        except IndexError:
            log.error('No aggregation netcdf available for statistics')
            ncstats = NcStats(datasource=nds)
    else:
        # It's sewerage spatialite (no agg. netcdf)
        ncstats = NcStats(datasource=nds)

    parameters = ncstats.AVAILABLE_MANHOLE_PARAMETERS

    # Generate data
    result = dict()
    for feature in layer.getFeatures():

        # skip 2d stuff
        if not include_2d:
            try:
                if feature['type'] == '2d':
                    continue
            except KeyError:
                pass

        fid = feature[layer_id_name]
        result[fid] = dict()
        result[fid]['id'] = fid  # normalize layer id name

        try:
            surface_level = feature['surface_level']
        except KeyError:
            log.error("Feature doesn't have surface level")
            surface_level = None
        try:
            bottom_level = feature['bottom_level']
        except KeyError:
            log.error("Feature doesn't have bottom level")
            bottom_level = None

        # There are two hacks:
        # Hack for v2_manhole, see previous comment.
        if old_layer_name == 'v2_manhole':
            hack_fid = feature['connection_node_id']
        else:
            hack_fid = feature[layer_id_name]

        results_from_params = _calc_results(
            ncstats,
            parameters,
            layer_name,
            hack_fid,
            surface_level=surface_level,
            bottom_level=bottom_level)
        result[fid].update(results_from_params)

    # Write to csv file
    filepath = get_default_csv_path(old_layer_name, result_dir)
    with open(filepath, 'wb') as csvfile:
        fieldnames = ['id'] + parameters

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                delimiter=',')
        writer.writeheader()
        for fid, val_dict in result.items():
            writer.writerow(val_dict)
    return filepath


def generate_structure_stats(nds, result_dir, layer, layer_id_name,
                             include_2d=True):
    """Generate stats for structure objects and write to csv.

    Args:
        nds: NetcdfDataSource
        result_dir: output directory
        layer: qgis layer
        layer_id_name: the pk of the layer
        include_2d: include 2d features (only applicable for lines)

    Returns:
        filepath generated csv
    """
    layer_name = layer.name()
    structures = ['weir', 'pumpstation', 'pipe', 'orifice', 'culvert',
                  'flowline']
    if not any(s in layer_name for s in structures):
        raise ValueError(
            "%s is not a valid structure layer. Valid layers are: %s" %
            (layer_name, structures))

    if layer_name == 'flowlines':
        # TODO: not sure if we want to make ncstats distinction based on
        # the layer type
        try:
            ncstats = NcStatsAgg(datasource=nds)
        except IndexError:
            log.error('No aggregation netcdf available for statistics')
            ncstats = NcStats(datasource=nds)
    else:
        # It's a view
        try:
            ncstats = NcStatsAgg(datasource=nds)
        except IndexError:
            log.error('No aggregation netcdf available for statistics')
            ncstats = NcStats(datasource=nds)

    # Generate data
    result = dict()
    for feature in layer.getFeatures():
        # skip 2d stuff
        if not include_2d:
            try:
                if feature['type'] == '2d':
                    continue
            except KeyError:
                pass

        fid = feature[layer_id_name]
        result[fid] = dict()
        result[fid]['id'] = fid  # normalize layer id name to 'id' in csv
        for param_name in ncstats.AVAILABLE_STRUCTURE_PARAMETERS:
            try:
                result[fid][param_name] = \
                    ncstats.get_value_from_parameter(
                        layer_name, feature[layer_id_name], param_name)
            except (ValueError, IndexError, AttributeError):
                # AttributeError: is raised in NcStats because in case of
                # KeyErrors in get_value_from_parameter the method finding
                # is propagated to NcStats and when the method doesn't
                # exist AttributeError is raised. A better solution is to
                # filter AVAILABLE_STRUCTURE_PARAMETERS beforehand.
                result[fid][param_name] = None

    # Write to csv file
    filepath = get_default_csv_path(layer_name, result_dir)
    with open(filepath, 'wb') as csvfile:
        fieldnames = ['id'] + ncstats.AVAILABLE_STRUCTURE_PARAMETERS
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                delimiter=',')
        writer.writeheader()
        for fid, val_dict in result.items():
            writer.writerow(val_dict)
    return filepath


def generate_pump_stats(nds, result_dir, layer, layer_id_name,
                        include_2d=True):
    """Generate stats for structure objects and write to csv.

    Args:
        nds: NetcdfDataSource
        result_dir: output directory
        layer: qgis layer
        layer_id_name: the pk of the layer
        include_2d: include 2d features (only applicable for lines)

    Returns:
        filepath generated csv
    """
    layer_name = layer.name()
    structures = ['pumpstation', 'pumplines']
    if not any(s in layer_name for s in structures):
        raise ValueError(
            "%s is not a valid structure layer. Valid layers are: %s" %
            (layer_name, structures))

    if layer_name == 'pumplines':
        # TODO: not sure if we want to make ncstats distinction based on
        # the layer type
        try:
            ncstats = NcStatsAgg(datasource=nds)
        except IndexError:
            ncstats = NcStats(datasource=nds)
    else:
        # It's a view
        ncstats = NcStats(datasource=nds)

    # Generate data
    result = dict()
    for feature in layer.getFeatures():
        # skip 2d stuff
        if not include_2d:
            try:
                if feature['type'] == '2d':
                    continue
            except KeyError:
                pass

        fid = feature[layer_id_name]
        result[fid] = dict()
        result[fid]['id'] = fid  # normalize layer id name to 'id' in csv

        try:
            capacity = feature['pump_capacity']
        except KeyError:
            log.error("Feature doesn't have pump_capacity")
            capacity = None

        for param_name in ncstats.AVAILABLE_PUMP_PARAMETERS:
            try:
                result[fid][param_name] = \
                    ncstats.get_value_from_parameter(
                        layer_name, feature[layer_id_name], param_name,
                        capacity=capacity)
            except (ValueError, IndexError, AttributeError):
                # AttributeError: is raised in NcStats because in case of
                # KeyErrors in get_value_from_parameter the method finding
                # is propagated to NcStats and when the method doesn't
                # exist AttributeError is raised. A better solution is to
                # filter AVAILABLE_STRUCTURE_PARAMETERS beforehand.
                result[fid][param_name] = None
            except TypeError:
                # Error with pump_duration, likely an invalid capacity
                result[fid][param_name] = None

    # Write to csv file
    filepath = get_default_csv_path(layer_name, result_dir)
    with open(filepath, 'wb') as csvfile:
        fieldnames = ['id'] + ncstats.AVAILABLE_PUMP_PARAMETERS
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                delimiter=',')
        writer.writeheader()
        for fid, val_dict in result.items():
            writer.writerow(val_dict)
    return filepath
