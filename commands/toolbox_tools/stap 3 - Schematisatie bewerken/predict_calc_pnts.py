from PyQt4.QtCore import QVariant
from qgis.core import (QgsFeature, QgsPoint,
                       QgsVectorLayer, QgsMapLayerRegistry,
                       QgsField)

EPSILON = 0.000001

def float_equals(f1, f2):
    return abs(f1 - f2) < EPSILON


class PointsAlongLine(object):
    def __init__(self, lyr_name="", fields=None):
        self.lyr_name = lyr_name
        if not self.lyr_name:
            self.lyr_name = "temporary_lyr"
        self.fields = fields
        self.data_provider = None
        self.mem_layer = None
        self._create_mem_layer()
        self.known_pnts = set()
    @staticmethod
    def get_postgis_layer(**kwargs):
        uri = QgsDataSourceURI()
        address = kwargs['address']
        port = kwargs['port']
        name = kwargs['name']
        user_name = kwargs['user_name']
        password = kwargs['password']
        schema = kwargs['schema']
        table_name = kwargs['table_name']
        geom_column = kwargs['geom_column']
        layer_name = kwargs['layer_name']
        uri.setConnection(address, port, name, user_name, password)
        uri.setDataSource(schema, table_name, geom_column)
        vlayer = QgsVectorLayer(uri.uri(), layer_name, "postgres")
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)
        return vlayer
    def _create_mem_layer(self, lyr_type="Point"):
        _type_map = {
            'str': QVariant.String,
            'int': QVariant.Int,
            'float': QVariant.Double
        }
        # create layer
        self.mem_layer = QgsVectorLayer(lyr_type, self.lyr_name, "memory")
        self.data_provider = self.mem_layer.dataProvider()
        # add fields
        if self.fields is None:
            _fields = [QgsField("id", QVariant.Int)]
        else:
            _fields = [
                (QgsField(field_name, _type_map[field_type]))
                for field_name, field_type in self.fields.iteritems()
            ]
        self.data_provider.addAttributes(_fields)
        self.mem_layer.updateFields() # tell the vector layer to fetch changes from the provider
    def create_pnts_at(self, geom, distance, attributes=None):
        # TODO incorperate Attributes
        line_length = geom.length()
        dists = self.get_cnt_for_line(distance, line_length)
        # start_point = QgsPoint(geom[0])
        # end_point = QgsPoint(geom[-1])
        # self.known_pnts.add(start_point)
        # self.known_pnts.add(end_point)
        for i, dist in enumerate(dists, start=1):
            # Get a point along the line at the current distance
            point = geom.interpolate(dist)
            # add start and endpoint
            if i == 1 or i == len(dists):
                print "start or endpoint [{}]".format(i)
                # print "seen point {} before ".format(point.exportToWkt())
                xy = (point.asPoint().x(), point.asPoint().y())
                print "xy ", xy
                if xy in self.known_pnts:
                    print "seen point {} before ".format(xy)
                    continue
                self.known_pnts.add(xy)
            print 'step ', i, 'point ', point
            # Create a new QgsFeature and assign it the new geometry
            # add a feature
            f = QgsFeature()
            f.setGeometry(point)
            f.setAttributes([i])
            self.data_provider.addFeatures([f])
            # update layer's extent when new features have been added
            # because change of extent in provider is not propagated to the layer
            self.mem_layer.updateExtents()
    def remove_mem_layer(self):
        QgsMapLayerRegistry.instance().removeMapLayers( [self.mem_layer.id()] )
    def add_mem_layer(self):
        QgsMapLayerRegistry.instance().addMapLayer(self.mem_layer)
    def get_cnt_for_line(self, distance, line_length):
        segs = line_length/distance
        dists = [0]
        current_dist = 0
        for seg in xrange(int(segs)):
            current_dist += distance
            dists.append(current_dist)
        return dists





test_kwargs = {
    'address': '10.0.3.111',
    'port': '5432',
    'name': 'work_martijn',
    'user_name':'buildout',
    'password': 'buildout',
    'schema': 'public',
    'table_name': 'v2_channel',
    'geom_column': 'the_geom',
    'layer_name': 'channel_new',
}

pal = PointsAlongLine()
channel_layer = pal.get_postgis_layer(**test_kwargs)
features = channel_layer.getFeatures()
for channel in features:
    pal.create_pnts_at(channel.geometry(), channel['dist_calc_points'])
pal.add_mem_layer()


for channel in features4:
    pal.create_pnts_at(channel.geometry(), channel['dist_calc_points'])

features = vlayer.getFeatures()
for f in features:
    geom = f.geometry()
    l = geom.length()
    idx = f.fieldNameIndex('dist_calc_points')
    dist_calc_pnt = f['dist_calc_points']
    dest = [l/dist_calc_pnt]
    # example with geometry
    wkt = geom.exportToWkt()
    print wkt













vl = QgsVectorLayer("Point", "distance nodes", "memory")
pr = vl.dataProvider()
pr.addAttributes( [ QgsField("distance", QVariant.Int) ] )

_l = 0
features = vlayer.getFeatures()
for f in features:
    geom = f.geometry()
    l = geom.length()
    if not _l:
        _l += l
    point = geom.interpolate(_l)
    wkt = point.exportToWkt()
    print wkt
    fet = QgsFeature()
    fet.setGeometry(point)
    pr.addFeatures(fet)
    vl.updateExtents()
QgsMapLayerRegistry.instance().addMapLayer(vl)



