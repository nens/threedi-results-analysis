"""Imported in __init__.py"""
from builtins import map
from builtins import next
from builtins import object
from itertools import tee

import math


class cached_property(object):
    """ A property that is only computed once per instance and then replaces
        itself with an ordinary attribute. Deleting the attribute resets the
        property.

        Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76

        See also: http://www.pydanny.com/cached-property.html
        """

    def __init__(self, func):
        self.__doc__ = getattr(func, "__doc__")
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    Source: http://gis.stackexchange.com/a/56589
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = list(map(math.radians, [lon1, lat1, lon2, lat2]))
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km


def pairwise(iterable):
    # from https://docs.python.org/2/library/
    # itertools.html#recipes
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def parse_db_source_info(source_info):
    """
    parses the source info string as returned by
    <layer name>.dataProvider().dataSourceUri()

    :param source_info: source info string as returned by
        <layer name>.dataProvider().dataSourceUri()
    :returns a dict like so
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
