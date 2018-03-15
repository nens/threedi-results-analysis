from collections import OrderedDict
import os

from osgeo import ogr

from threedigrid.admin.constants import TYPE_FUNC_MAP
from threedigrid.admin.constants import OGR_FIELD_TYPE_MAP
from threedigrid.orm.base.exporters import BaseOgrExporter
from threedigrid.admin.utils import get_spatial_reference
from threedigrid.admin.utils import KCUDescriptor

ogr.UseExceptions()  # fail fast

SPATIALITE_DRIVER_NAME = 'SQLite'

from ..utils.user_messages import log


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
            SPATIALITE_DRIVER_NAME,
        }

    def save(
            self, file_name, layer_name, node_data, target_epsg_code,
            **kwargs):
        """
        save to file format specified by the driver, e.g. shapefile

        :param file_name: name of the outputfile
        :param node_data: dict of node data
        """
        assert self.driver is not None
        sr = get_spatial_reference(target_epsg_code)
        if not os.path.exists(file_name):
            data_source = self.driver.CreateDataSource(
                file_name, ["SPATIALITE=YES"])
        else:
            data_source = self.driver.Open(file_name, update=1)

        layer = data_source.CreateLayer(
            layer_name,
            sr,
            geom_type=ogr.wkbPoint,
            options=['FORMAT=SPATIALITE']
        )
        fields = self.QGIS_NODE_FIELDS
        for field_name, field_type in fields.iteritems():
            layer.CreateField(ogr.FieldDefn(
                    str(field_name), OGR_FIELD_TYPE_MAP[field_type])
            )
        _definition = layer.GetLayerDefn()

        for i in xrange(node_data['id'].size):
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint_2D(
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
                # Using ['FID=id'] in CreateLayer doesn't work on GDAL < 2.0,
                # thus FID defaults to 'OGC_FID', which sucks.
                # See: http://www.gdal.org/drv_sqlite.html
                # To circumvent this, we set 'OGC_FID' to 'id', so we can do
                # feature.id() in QGIS and get the node index without having
                # to specify that we need the use the 'id' column
                feature.SetFID(node_data['id'][i])
            layer.CreateFeature(feature)
            feature.Destroy()
        data_source = None


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
            SPATIALITE_DRIVER_NAME,
        }
        self.driver = None

    def save(
            self, file_name, layer_name, line_data, target_epsg_code,
            **kwargs):
        """
        save to file format specified by the driver, e.g. shapefile

        :param file_name: name of the outputfile
        :param line_data: dict of line data
        """
        assert self.driver is not None

        kcu_dict = QgisKCUDescriptor()
        sr = get_spatial_reference(target_epsg_code)
        if not os.path.exists(file_name):
            data_source = self.driver.CreateDataSource(
                file_name, ["SPATIALITE=YES"])
        else:
            data_source = self.driver.Open(file_name, update=1)

        layer = data_source.CreateLayer(
            layer_name,
            sr,
            geom_type=ogr.wkbLineString,
            options=['FORMAT=SPATIALITE'],
        )
        fields = self.LINE_FIELDS
        for field_name, field_type in fields.iteritems():
            layer.CreateField(ogr.FieldDefn(
                    str(field_name), OGR_FIELD_TYPE_MAP[field_type])
            )
        _definition = layer.GetLayerDefn()

        node_a = line_data['line'][0]
        node_b = line_data['line'][1]
        for i in xrange(node_a.size):
            line = ogr.Geometry(ogr.wkbLineString)
            line.AddPoint_2D(line_data['line_coords'][0][i],
                             line_data['line_coords'][1][i])
            line.AddPoint_2D(line_data['line_coords'][2][i],
                             line_data['line_coords'][3][i])

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
                # Using ['FID=id'] in CreateLayer doesn't work on GDAL < 2.0,
                # thus FID defaults to 'OGC_FID', which sucks.
                # See: http://www.gdal.org/drv_sqlite.html
                # To circumvent this, we set 'OGC_FID' to our 'id', so we
                # can do feature.id() in QGIS and get the line index without
                # having to specify the 'id' column.
                feature.SetFID(line_data['id'][i])

            layer.CreateFeature(feature)
            feature.Destroy()
        data_source = None


class QgisPumpsOgrExporter(BaseOgrExporter):
    """
    Exports to ogr formats. You need to set the driver explicitly
    before calling save()
    """
    FIELDS = OrderedDict([
        ('id', 'int'),
        ('node_idx1', 'int'),
        ('node_idx2', 'int'),
    ])

    FIELD_NAME_MAP = OrderedDict([
        ('id', 'id'),
        ('node_idx1', 'node1_id'),
        ('node_idx2', 'node2_id'),
    ])

    def __init__(self, node_data):
        self.node_data = node_data
        self.driver = None

    def save(
            self, file_name, layer_name, pump_data, target_epsg_code,
            **kwargs):
        """
        save to file format specified by the driver, e.g. shapefile

        :param file_name: name of the outputfile
        :param line_data: dict of line data
        """
        assert self.driver is not None

        sr = get_spatial_reference(target_epsg_code)
        if not os.path.exists(file_name):
            data_source = self.driver.CreateDataSource(
                file_name, ["SPATIALITE=YES"])
        else:
            data_source = self.driver.Open(file_name, update=1)

        layer = data_source.CreateLayer(
            layer_name,
            sr,
            geom_type=ogr.wkbLineString,
            options=['FORMAT=SPATIALITE'],
        )

        for field_name, field_type in self.FIELDS.iteritems():
            layer.CreateField(ogr.FieldDefn(
                    str(field_name), OGR_FIELD_TYPE_MAP[field_type])
            )
        _definition = layer.GetLayerDefn()

        for i in xrange(pump_data['id'].size):
            line = ogr.Geometry(ogr.wkbLineString)
            node1_id = pump_data['node1_id'][i]
            node2_id = pump_data['node2_id'][i]

            for node_id in [node1_id, node2_id]:
                try:
                    line.AddPoint_2D(
                        self.node_data['coordinates'][0][node_id],
                        self.node_data['coordinates'][1][node_id],
                    )
                except IndexError:
                    log("Invalid node id: %s" % node_id)

            feature = ogr.Feature(_definition)
            feature.SetGeometry(line)
            for field_name, field_type in self.FIELDS.iteritems():
                fname = self.FIELD_NAME_MAP[field_name]
                raw_value = pump_data[fname][i]
                value = TYPE_FUNC_MAP[field_type](raw_value)
                feature.SetField(str(field_name), value)
                # Using ['FID=id'] in CreateLayer doesn't work on GDAL < 2.0,
                # thus FID defaults to 'OGC_FID', which sucks.
                # See: http://www.gdal.org/drv_sqlite.html
                # To circumvent this, we set 'OGC_FID' to our 'id', so we
                # can do feature.id() in QGIS and get the line index without
                # having to specify the 'id' column.
                feature.SetFID(pump_data['id'][i])

            layer.CreateFeature(feature)
            feature.Destroy()
        data_source = None
