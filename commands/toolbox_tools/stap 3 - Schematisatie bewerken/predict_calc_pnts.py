from PyQt4.QtCore import QVariant
from qgis.core import (QgsFeature, QgsGeometry,
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
    def get_postgis_uri(**kwargs):
        uri = QgsDataSourceURI()
        address = kwargs['address']
        port = kwargs['port']
        name = kwargs['name']
        user_name = kwargs['user_name']
        password = kwargs['password']
        schema = kwargs['schema']
        table_name = kwargs['table_name']
        geom_column = kwargs['geom_column']
        uri.setConnection(address, port, name, user_name, password)
        uri.setDataSource(schema, table_name, geom_column)
        return uri
    def get_layer_from_uri(self, uri, layer_name):
        vlayer = QgsVectorLayer(uri.uri(), layer_name, "postgres")
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)
        return vlayer
    def create_query_obj_from_uri(self, uri, db_type='QPSQL'):
        db = QtSql.QSqlDatabase.addDatabase(db_type)
        db.setHostName(uri.host())
        db.setPort(int(uri.port()))
        db.setDatabaseName(uri.database())
        db.setUserName(uri.username())
        db.setPassword(uri.password())
        ok = db.open()
        if ok:
            self.query = QtSql.QSqlQuery(db)
        else:
            raise RuntimeError('Failed to open database connection: {}'.format(db.lastError().driverText()))
    def get_epsg_code(self):
        self.query.exec_('''SELECT epsg_code FROM v2_global_settings;''')
        self.query.next()
        return query.value(0)
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
uri = pal.get_postgis_uri(**test_kwargs)
channel_layer = pal.get_layer_from_uri(uri, layer_name=test_kwargs['layer_name'])
features = channel_layer.getFeatures()
pal.create_query_obj_from_uri(uri)
epsg_code = pal.get_epsg_code()
pal.query.exec_('''SELECT id, dist_calc_points, ST_AsText(ST_Transform(the_geom, {epsg_code}}) as the_geom FROM {table_name};'''.format(epsg_code=epsg_code, table_name=test_kwargs['table_name']))
while pal.query.next():
    geom_txt = pal.query.value(2)
    dist_calc_pnts= pal.query.value(1)
    geom = QgsGeometry.fromWkt(geom_txt)
    pal.create_pnts_at(geom, dist_calc_pnts)


start = timeit.timeit()
for channel in features:
    pal.create_pnts_at(channel.geometry(), channel['dist_calc_points'])
end = timeit.timeit()
print end - start

pal.add_mem_layer()







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





spatilite_dialect = "ST_Line_Interpolate_Point"
postgres_dialect = "ST_LineInterpolatePoint"



from qgis.core import *

from PyQt4 import QtSql

database = 'yourdatabase'
username = 'youruser'
table = 'testing'
srid = 4326
dimension = 2
typmod = 'POINT'


sec = PointsAlongLine()
uri = sec.get_postgis_uri(**test_kwargs)

db = QtSql.QSqlDatabase.addDatabase('QPSQL')

db.setHostName(uri.host())
db.setPort(int(uri.port()))
db.setDatabaseName(uri.database())
db.setUserName(uri.username())
db.setPassword(uri.password())

ok = db.open()
if ok:
    query = QtSql.QSqlQuery(db)
    if not query.exec_('''SELECT id, ST_AsText(the_geom) as the_geom FROM {};'''.format(test_kwargs['table_name'])):

        raise RuntimeError('Failed to create table')
    if not query.exec_('''SELECT AddGeometryColumn('public', '{table}', 'the_geom', {srid}, '{typmod}', {dimension})'''.format(table=table, srid=srid, typmod=typmod, dimension=dimension)):
        raise RuntimeError('Failed to add geometry column to table')
    layer = QgsVectorLayer(uri.uri(), table, 'postgres')
    if layer.isValid():
        QgsMapLayerRegistry().instance().addMapLayer(layer)
else:
    raise RuntimeError('Failed to open database connection: {}'.format(db.lastError().driverText()))



query.exec_('''SELECT id, ST_AsText(the_geom) as the_geom FROM {};'''.format(test_kwargs['table_name']))
while query.next():
    geom_txt = query.value(1)
    geom = QgsGeometry.fromWkt(query.value(1))
    point = geom.interpolate(2)


query.next()
query.value(0)
130

	while query.next():
		table = query.value(0).toString()


QSQLITE 	SQLite version 3 or above
QSQLITE2 	SQLite version 2



CREATE TABLE recur AS
WITH RECURSIVE dist(id, x, the_geom, d) AS (
    SELECT
       id,
       1::double precision,
       the_geom,
       0::double precision
    FROM v2_channel
       UNION ALL
    SELECT
      dist.id,
      x+1,
      v2_channel.the_geom AS gm,
      d+(1/round(ST_Length(v2_channel.the_geom)/v2_channel.dist_calc_points)) AS dist_calc_pnts
    FROM v2_channel JOIN dist
        ON  dist.x  < ST_Length(v2_channel.the_geom)/v2_channel.dist_calc_points
        AND dist.id = v2_channel.id
)
SELECT *, ST_LineInterpolatePoint(the_geom, d) FROM dist;




WITH RECURSIVE dist(id, calculation_type, x, the_geom, d) AS (
    SELECT
       id,
       calculation_type,
       1::double precision,
       the_geom,
       0::double precision
    FROM v2_channel
       UNION ALL
    SELECT
      dist.id,
      dist.calculation_type,
      x+1,
      v2_channel.the_geom AS gm,
      d+(1/round(ST_Length(v2_channel.the_geom)/v2_channel.dist_calc_points)) AS dist_calc_pnts
    FROM v2_channel JOIN dist
        ON  dist.x  < ST_Length(v2_channel.the_geom)/v2_channel.dist_calc_points
        AND dist.id = v2_channel.id
)
INSERT INTO v2_calculation_point (content_type_id, user_ref, calc_type, the_geom)
SELECT 
  id, 
  concat_ws('-',id::char,'v2_channel',x::text), 
  calculation_type, 
  ST_LineInterpolatePoint(the_geom, d) AS the_geom 
FROM dist ORDER BY id, x ASC;
