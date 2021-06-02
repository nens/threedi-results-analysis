"""Imported in __init__.py"""
from itertools import tee
from ThreeDiToolbox.datasource.result_constants import AGGREGATION_VARIABLES
from ThreeDiToolbox.datasource.result_constants import CUMULATIVE_AGGREGATION_UNITS
from ThreeDiToolbox.datasource.result_constants import H_TYPES
from ThreeDiToolbox.datasource.result_constants import Q_TYPES
from ThreeDiToolbox.datasource.result_constants import SUBGRID_MAP_VARIABLES

import logging


logger = logging.getLogger(__name__)


def pairwise(iterable):
    # from https://docs.python.org/2/library/
    # itertools.html#recipes
    """s  -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def parse_db_source_info(source_info):
    """
    parses the source info string as returned by
    <layer name>.dataProvider().dataSourceUri()

    Args:
        source_info: source info string as returned by
          <layer name>.dataProvider().dataSourceUri()

    Returns:
        A dict like so::

            {
                'db_name': '',
                'host': '',
                'password': '',
                'port': '',
                'srid': '',
                'table_name': '',
                'schema_name': '',
                'type': '',
                'user': ''
            }

    """
    import re

    info_dict = {}

    if not source_info[:6] == "dbname":
        return
    layer_info = source_info.replace("'", '"')
    raw_dict = dict(re.findall(r'(\S+)="?(.*?)"? ', layer_info))
    info_dict["database"] = raw_dict.get("dbname", "")
    info_dict["username"] = raw_dict.get("user", "")
    info_dict["password"] = raw_dict.get("password", "")
    info_dict["srid"] = raw_dict.get("srid", "")
    info_dict["type"] = raw_dict.get("type", "")
    info_dict["host"] = raw_dict.get("host", "")
    info_dict["port"] = raw_dict.get("port", "")

    if info_dict["database"].endswith("sqlite"):
        info_dict["table_name"] = raw_dict["table"]
        info_dict["schema"] = ""
        info_dict["db_type"] = "spatialite"
        info_dict["host"] = info_dict["database"]
    else:
        # need some extra processing to get table name and schema
        schema_name, table_name = raw_dict["table"].split(".")
        info_dict["schema"] = schema_name.strip('"')
        info_dict["table_name"] = table_name.strip('"')
        info_dict["db_type"] = "postgres"
    return info_dict


def parse_aggvarname(aggvarname):
    """Parse a combined agg var name.

    >>> parse_aggvarname('s1_max')
    ('s1', 'max')
    >>> parse_aggvarname('s1_cum_negative')
    ('s1', 'cum_negative')
    >>> parse_aggvarname('infiltration_rate_cum_positive')
    ('infiltration_rate', 'cum_positive')
    """
    # Aggregation methods unfortunately can contain underscores; for now only
    # these two cases are known.
    # TODO: improve this, e.g., make more generic, because extra cases will
    # need to be added later
    if aggvarname.endswith("cum_positive") or aggvarname.endswith("cum_negative"):
        varname, agg_method, sign = aggvarname.rsplit("_", 2)
        return varname, "_".join([agg_method, sign])

    # Works only for aggregation methods without underscores
    varname, agg_method = aggvarname.rsplit("_", 1)  # maxsplit = 1
    return varname, agg_method


def generate_parameter_config(subgrid_map_vars, agg_vars):
    """Dynamically create the parameter config

    :param subgrid_map_vars: available vars from subgrid_map.nc
    :param agg_vars: available vars from aggregation netCDF
    :returns: dict with two lists of parameters for lines ('q') and nodes ('h'). Structure:
    {'q': [{"name": str, "unit": str, "parameters": (str, [str]) }], 'h': [<same structure as q>]}.
    """
    subgrid_map_vars_mapping = {
        var: (lbl, unit) for (var, lbl, unit, negative_possible) in SUBGRID_MAP_VARIABLES
    }
    agg_vars_mapping = {
        var: (lbl, unit) for (var, lbl, unit, negative_possible) in AGGREGATION_VARIABLES
    }
    config = {"q": [], "h": []}

    verbose_agg_method = {
        "min": "minimum",
        "max": "maximum",
        "cum": "net cumulative",
        "avg": "average",
        "med": "median",
        "cum_positive": "positive cumulative",
        "cum_negative": "negative cumulative",
    }

    for varname in subgrid_map_vars:
        varinfo = subgrid_map_vars_mapping[varname]
        d = {"name": varinfo[0].capitalize(), "unit": varinfo[1], "parameters": varname}
        if varname in Q_TYPES:
            config["q"].append(d)
        elif varname in H_TYPES:
            config["h"].append(d)

    for aggvarname in agg_vars:
        _varname, _agg_method = parse_aggvarname(aggvarname)
        varinfo = agg_vars_mapping[_varname]

        if _agg_method in verbose_agg_method:
            agg_method_display_name = verbose_agg_method[_agg_method]
        else:
            logger.critical("Unknown agg method: %s", _agg_method)
            agg_method_display_name = _agg_method

        # Adjust the unit for cumulative method
        if _agg_method.startswith("cum"):
            unit = CUMULATIVE_AGGREGATION_UNITS[_varname]
        else:
            unit = varinfo[1]

        d = {
            "name": "%s %s" % (agg_method_display_name.capitalize(), varinfo[0]),
            "unit": unit,
            "parameters": aggvarname,
        }
        if _varname in Q_TYPES:
            config["q"].append(d)
        elif _varname in H_TYPES:
            config["h"].append(d)
    return config
