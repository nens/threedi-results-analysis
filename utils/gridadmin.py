from collections import OrderedDict
import os

from osgeo import ogr
from shapely.geometry import LineString  # TODO: should not be an dependency

from threedi_gridadmin.constants import SHP_DRIVER_NAME
from threedi_gridadmin.constants import GEO_PACKAGE_DRIVER_NAME
from threedi_gridadmin.constants import TYPE_FUNC_MAP
from threedi_gridadmin.constants import OGR_FIELD_TYPE_MAP
from threedi_gridadmin.orm import BaseOgrExporter
from threedi_gridadmin.utils import get_spatial_reference
from threedi_gridadmin.utils import KCUDescriptor

SPATIALITE_DRIVER_NAME = 'SQLite'


class QgisNodesOgrExporter(BaseOgrExporter):
    """
    Exports to ogr formats. You need to set the driver explicitly
    before calling save()
    """

    QGIS_NODE_FIELDS = OrderedDict([
        ('id', 'int'),
        ('inp_id', 'int'),
        ('spatialite_id', 'int'),
        # TODO: feat_type is not yet implemented
        ('feature_type', 'str'),  # e.g. v2_connection_nodes
        ('type', 'str'),  # 1d, 2d, etc.
    ])

    QGIS_NODE_FIELD_NAME_MAP = OrderedDict([
        ('id', 'id'),
        ('inp_id', 'seq_id'),
        ('spatialite_id', 'content_pk'),
        ('feature_type', 'node_type'),
        ('type', 'node_type'),
    ])

    INT_TO_TYPE_STR = {
        '1': '2d',
        '2': '2d_groundwater',
        '3': '1d',
        '4': '1d',
        '5': '2d_bound',
        '6': '2d_groundwater_bound',
        '7': '1d_bound',
    }

    def __init__(self, nodes):
        """
        :param lines: lines.models.Lines instance
        """
        self._nodes = nodes
        self.supported_drivers = {
            GEO_PACKAGE_DRIVER_NAME,
            SHP_DRIVER_NAME,
            SPATIALITE_DRIVER_NAME,
        }

    def save(self, file_name, node_data, target_epsg_code, **kwargs):
        """
        save to file format specified by the driver, e.g. shapefile

        :param file_name: name of the outputfile
        :param node_data: dict of node data
        """
        assert self.driver is not None
        geomtype = 0
        sr = get_spatial_reference(target_epsg_code)
        self.del_datasource(file_name)
        data_source = self.driver.CreateDataSource(file_name)
        layer = data_source.CreateLayer(
            str(os.path.basename(file_name)),
            sr,
            geomtype
        )
        fields = self.QGIS_NODE_FIELDS
        # if self._nodes.has_1d:
        #     fields.update(QGIS_NODE_1D_FIELDS)

        for field_name, field_type in fields.iteritems():
            layer.CreateField(ogr.FieldDefn(
                    str(field_name), OGR_FIELD_TYPE_MAP[field_type])
            )
        _definition = layer.GetLayerDefn()

        for i in xrange(node_data['id'].size):
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(
                node_data['coordinates'][0][i],
                node_data['coordinates'][1][i]
            )
            feature = ogr.Feature(_definition)
            feature.SetGeometry(point)
            for field_name, field_type in fields.iteritems():
                fname = self.QGIS_NODE_FIELD_NAME_MAP[field_name]
                if field_name == 'type':
                    raw_value = node_data[fname][i]
                    _value = TYPE_FUNC_MAP[field_type](raw_value)
                    try:
                        value = self.INT_TO_TYPE_STR[_value]
                    except KeyError:
                        value = _value
                    # OGR dislikes unicode for some reason...
                    value = str(value)
                else:
                    raw_value = node_data[fname][i]
                    value = TYPE_FUNC_MAP[field_type](raw_value)
                feature.SetField(str(field_name), value)
            layer.CreateFeature(feature)


class QgisKCUDescriptor(KCUDescriptor):
    def __init__(self, *args, **kwargs):
        super(QgisKCUDescriptor, self).__init__(*args, **kwargs)

        self._descr = {
            0: '1d',
            1: '1d',
            2: '1d',
            3: '1d',
            4: '1d',
            5: '1d',
            51: '1d_2d',
            52: '1d_2d',
            53: '1d_2d',
            54: '1d_2d',
            55: '1d_2d',
            56: '1d_2d',
            57: '1d_2d_groundwater',
            58: '1d_2d_groundwater',
            100: '2d',
            101: '2d',
            150: '2d',
            -150: '2d_groundwater',
            200: '2d_bound',
            300: '2d_bound',
            400: '2d_bound',
            500: '2d_bound',
        }

    def get(self, item):
        return self.__getitem__(item)

    def values(self):
        v = self._descr.values()
        v.extend(['2d_bound', '2d_groundwater_bound'])
        return v

    def keys(self):
        k = self._descr.keys()
        k += self.bound_keys_2d
        k += self.bound_keys_groundwater
        return k

    def __getitem__(self, item):
        if item in self.bound_keys_2d:
            return '2d_bound'
        elif item in self.bound_keys_groundwater:
            return '2d_groundwater_bound'
        v = self._descr.get(item)
        if not v:
            raise KeyError(item)
        return v


class QgisLinesOgrExporter(BaseOgrExporter):
    """
    Exports to ogr formats. You need to set the driver explicitly
    before calling save()
    """
    LINE_FIELDS = OrderedDict([
        ('id', 'int'),
        ('kcu', 'int'),  # unused in plugin
        # type is a combination of 'kcu' and 'cont_type'
        ('type', 'str'),
        ('start_node_idx', 'int'),
        ('end_node_idx', 'int'),
        ('content_type', 'str'),  # unused in plugin
        ('spatialite_id', 'int'),
        ('inp_id', 'int'),
    ])

    # maps the fields names of grid line objects
    # to their external representation
    LINE_FIELD_NAME_MAP = OrderedDict([
        ('id', 'id'),
        ('kcu', 'kcu'),
        ('type', 'does not matter'),
        ('start_node_idx', 'does not matter'),
        ('end_node_idx', 'does not matter'),
        ('inp_id', 'lik'),
        ('content_type', 'content_type'),
        ('spatialite_id', 'content_pk'),
    ])

    def __init__(self, lines):
        """
        :param lines: lines.models.Lines instance
        """
        self._lines = lines
        self.supported_drivers = {
            GEO_PACKAGE_DRIVER_NAME,
            SHP_DRIVER_NAME,
            SPATIALITE_DRIVER_NAME,
        }
        self.driver = None

    def save(self, file_name, line_data, target_epsg_code, **kwargs):
        """
        save to file format specified by the driver, e.g. shapefile

        :param file_name: name of the outputfile
        :param line_data: dict of line data
        """
        assert self.driver is not None

        kcu_dict = QgisKCUDescriptor()
        geomtype = 0
        sr = get_spatial_reference(target_epsg_code)

        geom_source = 'from_threedicore'
        if kwargs:
            geom_source = kwargs['geom']

        self.del_datasource(file_name)
        data_source = self.driver.CreateDataSource(file_name)
        layer = data_source.CreateLayer(
            str(os.path.basename(file_name)),
            sr,
            geomtype
        )
        fields = self.LINE_FIELDS
        # if self._lines.has_1d:
        #     fields.update(LINE_1D_FIELDS)
        for field_name, field_type in fields.iteritems():
            layer.CreateField(ogr.FieldDefn(
                    str(field_name), OGR_FIELD_TYPE_MAP[field_type])
            )
        _definition = layer.GetLayerDefn()

        node_a = line_data['line'][0]
        node_b = line_data['line'][1]
        for i in xrange(node_a.size):
            if geom_source == 'from_threedicore':
                line = ogr.Geometry(ogr.wkbLineString)
                line.AddPoint(line_data['line_coords'][0][i],
                              line_data['line_coords'][1][i])
                line.AddPoint(line_data['line_coords'][2][i],
                              line_data['line_coords'][3][i])
            elif geom_source == 'from_spatialite':
                linepoints = line_data['line_geometries'][i].reshape(2, -1).T
                line_geom = LineString(linepoints)
                line = ogr.CreateGeometryFromWkt(line_geom.wkt)

            feature = ogr.Feature(_definition)
            feature.SetGeometry(line)
            for field_name, field_type in fields.iteritems():
                fname = self.LINE_FIELD_NAME_MAP[field_name]
                if field_name == 'type':
                    value = None
                    # TODO: first try to find a mapping with kcu, then find
                    # a mapping using cont_type. If cont_type is not None,
                    # then use the cont_type, else use kcu
                    cont_type_raw_value = line_data['content_type'][i]
                    if cont_type_raw_value:
                        value = \
                            TYPE_FUNC_MAP[field_type](cont_type_raw_value)
                    else:
                        try:
                            value = str(kcu_dict[int(line_data['kcu'][i])])
                        except KeyError:
                            pass
                elif field_name == 'start_node_idx':
                    value = TYPE_FUNC_MAP[field_type](node_a[i])
                elif field_name == 'end_node_idx':
                    value = TYPE_FUNC_MAP[field_type](node_b[i])
                else:
                    raw_value = line_data[fname][i]
                    value = TYPE_FUNC_MAP[field_type](raw_value)
                feature.SetField(str(field_name), value)

            layer.CreateFeature(feature)
            feature.Destroy()
