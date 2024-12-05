"""Imported in __init__.py"""
from itertools import tee
from threedi_results_analysis.datasource.result_constants import AGGREGATION_VARIABLES
from threedi_results_analysis.datasource.result_constants import (
    CUMULATIVE_AGGREGATION_UNITS,
)
from threedi_results_analysis.datasource.result_constants import H_TYPES
from threedi_results_analysis.datasource.result_constants import Q_TYPES
from threedi_results_analysis.datasource.result_constants import SUBGRID_MAP_VARIABLES
from typing import List
from typing import Sequence
from uuid import uuid4

import logging
import numpy as np
import os
import shutil


logger = logging.getLogger(__name__)


def python_value(value, default_value=None, func=None):
    """
    help function for translating QVariant Null values into None
    value: QVariant value or python value
    default_value: value in case provided value is None
    func (function): function for transforming value
    :return: python value
    """

    # check on QVariantNull... type
    if hasattr(value, "isNull") and value.isNull():
        return default_value
    else:
        if default_value is not None and value is None:
            return default_value
        else:
            if func is not None:
                return func(value)
            else:
                return value


def backup_sqlite(filename):
    """Make a backup of the sqlite database."""
    backup_folder = os.path.join(os.path.dirname(os.path.dirname(filename)), "_backup")
    os.makedirs(backup_folder, exist_ok=True)
    prefix = str(uuid4())[:8]
    backup_sqlite_path = os.path.join(
        backup_folder, f"{prefix}_{os.path.basename(filename)}"
    )
    shutil.copyfile(filename, backup_sqlite_path)
    return backup_sqlite_path


def listdirs(path: str) -> List[str]:
    """
    Returns a (non-recursive) list of directories in a specific path.
    """
    return [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]


def safe_join(*path):
    """
    Join path parts and replace any backslashes with slash to make QGIS happy when accessing a Windows network location.
    """
    joined = os.path.join(*path)
    return joined.replace("\\", "/")


def pairwise(iterable):
    # from https://docs.python.org/2/library/
    # itertools.html#recipes
    """s  -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


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
    #  need to be added later
    if aggvarname.endswith("cum_positive") or aggvarname.endswith("cum_negative"):
        varname, agg_method, sign = aggvarname.rsplit("_", 2)
        return varname, "_".join([agg_method, sign])

    # Works only for aggregation methods without underscores
    varname, agg_method = aggvarname.rsplit("_", 1)  # maxsplit = 1
    return varname, agg_method


def is_substance_variable(variable: str) -> bool:
    """Check if a variable is a substance variable."""
    return variable.startswith("substance")


def generate_parameter_config(subgrid_map_vars, agg_vars, wq_vars, sca_vars=None):
    """Dynamically create the parameter config

    :param subgrid_map_vars: available vars from subgrid_map.nc
    :param agg_vars: available vars from aggregation netCDF
    :param sca_vars: available vars from structure control actions netCDF (optional)
    :returns: dict with two lists of parameters for lines ('q') and nodes ('h'). Structure:
    {'q': [{"name": str, "unit": str, "parameters": (str, [str]) }], 'h': [<same structure as q>]}.
    """
    subgrid_map_vars_mapping = {
        var: (lbl, unit)
        for (var, lbl, unit, negative_possible) in SUBGRID_MAP_VARIABLES
    }
    agg_vars_mapping = {
        var: (lbl, unit)
        for (var, lbl, unit, negative_possible) in AGGREGATION_VARIABLES
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
        "current": "current",
    }

    for varname in subgrid_map_vars:
        varinfo = subgrid_map_vars_mapping[varname]
        d = {
            "name": varinfo[0].capitalize(),
            "unit": varinfo[1],
            "parameters": varname,
        }
        if varname in Q_TYPES:
            config["q"].append(d)
        elif varname in H_TYPES:
            config["h"].append(d)

    for wqvar in wq_vars:
        d = {
            "name": wqvar["name"].capitalize(),
            "unit": wqvar["unit"],
            "parameters": wqvar["parameters"],
        }
        # always node variables
        config["h"].append(d)

    if sca_vars:
        for scavar in sca_vars:
            if "lines" in scavar["types"]:
                config["q"].append(scavar)
            if "pumps" in scavar["types"]:
                config["q"].append(scavar)
            if "nodes" in scavar["types"]:
                raise NotImplementedError("Structure control action plotting not yet implemented for nodes.")

    for aggvarname in agg_vars:
        _varname, _agg_method = parse_aggvarname(aggvarname)
        varinfo = agg_vars_mapping[_varname]

        if _agg_method in verbose_agg_method:
            agg_method_display_name = verbose_agg_method[_agg_method]
        else:
            logger.info(f"Unknown agg method: {_agg_method} ({aggvarname})")
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


def pretty(x: Sequence, n: int) -> np.ndarray:
    """
    Returns a "pretty" set of bin boundaries roughly of size n
    that span x. Use, for instance, like:
      plt.hist(x, bins=pretty(x, 40))
    """
    # Python implementation of R function pretty (https://github.com/wch/r-source/blob/trunk/src/appl/pretty.c)
    # From https://stackoverflow.com/a/73990229
    h = 1.5
    h5 = .5 + 1.5 * h
    lo = np.nanmin(x)
    up = np.nanmax(x)
    if not up > lo:
        raise ValueError("All values are the same.")
    c = (up - lo) / n
    b = 10 ** np.floor(np.log10(c))
    m = [1, (2+h)/(1+h), (5+2*h5)/(1+h5), (10+5*h)/(1+h), 10]
    k = np.digitize(c/b, m)
    u = b * [1, 2, 5, 10][k-1]
    ns = np.floor(lo / u + 1e-10)
    nu = np.ceil(up / u - 1e-10)
    return np.arange(ns * u, (nu + 1) * u, u)
