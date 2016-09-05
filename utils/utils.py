"""Imported in __init__.py"""
import math
import os

# Workaround for Travis which doesn't have qgis
try:
    from qgis.core import (
        QgsVectorLayer, QgsMapLayerRegistry, QgsVectorJoinInfo)
except ImportError as e:
    print("Can't import one or more QGIS functions, some functions will "
          "fail: %s" % e.message)


class cached_property(object):
    """ A property that is only computed once per instance and then replaces
        itself with an ordinary attribute. Deleting the attribute resets the
        property.

        Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76

        See also: http://www.pydanny.com/cached-property.html
        """

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
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
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km


def csv_join(filepath, layer, view_layer_field, csv_field='id',
             add_to_legend=True):
    """Generate a layer from csv file and join it with another vector layer.

    Args:
        filepath: path to the csv file
        layer: the layer we want to join the csv with
        view_layer_field: the id (e.g. primary key) of layer
        csv_field: the id of the csv layer (which is always 'id' in the case
            of the CustomCommand scripts)

    Returns:
        the generated csv layer
    """
    filename = os.path.basename(filepath)
    csv_layer_name = os.path.splitext(filename)[0]
    csv_uri = "file:///" + filepath
    csv_layer = QgsVectorLayer(csv_uri, csv_layer_name, "delimitedtext")
    QgsMapLayerRegistry.instance().addMapLayer(csv_layer,
                                               addToLegend=add_to_legend)
    join_info = QgsVectorJoinInfo()
    join_info.joinLayerId = csv_layer.id()
    join_info.joinFieldName = csv_field
    join_info.targetFieldName = view_layer_field
    join_info.memoryCache = True
    layer.addJoin(join_info)
    return csv_layer
