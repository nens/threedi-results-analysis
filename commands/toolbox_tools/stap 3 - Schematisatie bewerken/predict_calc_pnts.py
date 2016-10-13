from PyQt4.QtCore import QVariant
from PyQt4 import QtSql
from qgis.core import (QgsFeature, QgsGeometry,
                       QgsVectorLayer, QgsMapLayerRegistry,
                       QgsField, QgsExpression, QgsFeatureRequest)

from ThreeDiToolbox.utils.raw_sql import (
    boundary_query_str,
    manhole_query_str,
    pipe_query_str,
    culvert_query_str,
    channel_query_str
)


from collections import namedtuple
EPSILON = 0.000001

def float_equals(f1, f2):
    return abs(f1 - f2) < EPSILON


# connection node constants
NODE_CALC_TYPE_BOUNDARY = -1
NODE_CALC_TYPE_ISOLATED = 1
NODE_CALC_TYPE_CONNECTED = 2
NODE_CALC_TYPE_EMBEDDED = 0
NODE_CALC_TYPE_BROAD_CRESTED = 3
NODE_CALC_TYPE_SHORT_CRESTED = 4
NODE_CALC_TYPE_DOUBLE_CONNECTED = 5

custom_order = (
    NODE_CALC_TYPE_BOUNDARY,          # -1
    NODE_CALC_TYPE_EMBEDDED,          # 0
    NODE_CALC_TYPE_ISOLATED,          # 1
    NODE_CALC_TYPE_DOUBLE_CONNECTED,  # 5
    NODE_CALC_TYPE_CONNECTED,         # 2
    NODE_CALC_TYPE_BROAD_CRESTED,     # 3
    NODE_CALC_TYPE_SHORT_CRESTED      # 4
)




class PointsAlongLine(object):
    _QUERY_TYPE_DICT = {
        'postgres': 'QPSQL',
        'spatialite': 'QSQLITE',
        'spatialite2': 'QSQLITE2'
    }
    def __init__(self, flavor, lyr_name="", fields=None, epsg_code=None):
        self.epsg_code = epsg_code
        self.flavor = flavor
        self.lyr_name = lyr_name
        if not self.lyr_name:
            self.lyr_name = "temporary_lyr"
        self.fields = fields
        self.data_provider = None
        self.mem_layer = None
        self._create_mem_layer(self.epsg_code)
        # xy as key, bound as value
        # self.known_pnts = defaultdict(list)
        self.known_pnts = set()
        self._schema = None  # will passed to get_uri()
        self.query = None
        self.network_dict = {}
        self._features = []
    def get_uri(self, **kwargs):
        self._uri = QgsDataSourceURI()
        address = kwargs['address']
        port = kwargs['port']
        name = kwargs['name']
        user_name = kwargs['user_name']
        password = kwargs['password']
        self._schema = kwargs['schema']
        if self.flavor == 'spatialite':
            self._uri.setDatabase(address)
        elif self.flavor == 'postgres':
            self._uri.setConnection(address, port, name, user_name, password)
        return self._uri
    def get_layer_from_uri(self, uri, table_name, geom_column='', display_name=''):
        """
        "spatialite/postgres"
        """
        if not display_name:
            display_name = table_name
        uri.setDataSource(self._schema, table_name, geom_column)
        vlayer = QgsVectorLayer(uri.uri(), display_name, self.flavor)
        # crs = vlayer.crs()
        # if not crs.createFromId(int(epsg_code)):
        #     raise RuntimeError("Could not create crs from EPSG code {}".format(epsg_code))
        # vlayer.setCrs(crs)
        return vlayer
    def create_query_obj_from_uri(self, uri):
        db_type_identifier = self._QUERY_TYPE_DICT[self.flavor]
        db = QtSql.QSqlDatabase.addDatabase(db_type_identifier)
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
    def run_query(self, query_str):
        if self.query is None:
            self.create_query_obj_from_uri(self._uri)
        self.query.exec_(query_str)
    def build_calc_type_dict(self):
        # channel/culvert cal type map
        calc_type_map = {
            101: 1,
            105: 5,
            102: 2,
            100: 0,
        }
        query_objects = {
            'v2_1d_boundary_conditions': {
                'query': boundary_query_str,
                'node_id_start': 0,
                'node_id_end': None,
                'calc_type': 1,
                'the_geom': None,
                'line_length': None,
                'id': 2,
                'dist_calc_points': None,
                'the_geom_end': None,
                },
            'v2_manhole': {
                'query': manhole_query_str,
                'node_id_start': 0,
                'node_id_end': None,
                'calc_type': 1,
                'the_geom': None,
                'line_length': None,
                'id': 2,
                'dist_calc_points': None,
                'the_geom_end': None,
                },
            'v2_pipe': {
                'query': pipe_query_str,
                'node_id_start': 0,
                'node_id_end': 1,
                'calc_type': 2,
                'the_geom_end': 4,
                'the_geom': 5,
                'line_length': 6,
                'id': 7,
                'dist_calc_points': 8,
                },
            'v2_culvert': {
                'query': culvert_query_str,
                'node_id_start': 0,
                'node_id_end': 1,
                'calc_type': 2,
                'the_geom': 3,
                'line_length': 4,
                'id': 5,
                'dist_calc_points': 6,
                'the_geom_end': 7,
            },
            'v2_channel': {
                'query': channel_query_str,
                'node_id_start': 0,
                'node_id_end': 1,
                'calc_type': 2,
                'the_geom': 5,
                'line_length': 6,
                'id': 7,
                'dist_calc_points': 8,
                'the_geom_end': 4,
            },
        }
        for name, d in query_objects.iteritems():
            print "processing {}".format(name)
            self.run_query(d['query'])
            while self.query.next():
                start_point = {}
                end_point = {}
                the_geom = None
                if d['the_geom'] is not None:
                    the_geom = self.query.value(d['the_geom'])
                the_geom_end = None
                if d['the_geom_end'] is not None:
                    the_geom_end =  self.query.value(d['the_geom_end'])
                line_length = None
                if d['line_length'] is not None:
                    line_length = self.query.value(d['line_length'])
                dist_calc_points = None
                if d['dist_calc_points'] is not None:
                    dist_calc_points =  self.query.value(d['dist_calc_points'])
                connection_node_end = None
                if d['node_id_end'] is not None:
                    connection_node_end = self.query.value(d['node_id_end'])
                object_id = self.query.value(d['id'])
                connection_node_start = self.query.value(d['node_id_start'])
                _calc_type = self.query.value(d['calc_type'])
                calc_type = calc_type_map.get(_calc_type) or _calc_type
                print "calc_type is ", calc_type, "type ", type(calc_type)
                if calc_type == NULL:
                    print "WARNING: no calc_type for {name} {id}".format(name=name, id=object_id)
                    continue
                if the_geom is not None:
                    cnt_segments = max(
                        int(round(line_length / (dist_calc_points * 1.0))), 1
                    )
                    start_point['calc_type'] = calc_type
                    start_point['content_type'] = name
                    start_point['content_type_id'] = object_id
                    start_point['dist_calc_pnts'] = dist_calc_points
                    start_point['line_length'] = line_length
                    start_point['the_geom'] = the_geom
                    start_point['cnt_segments'] = cnt_segments
                    end_point['content_type'] = name
                    end_point['content_type_id'] = object_id
                    end_point['dist_calc_pnts'] = dist_calc_points
                    end_point['the_geom_end'] = the_geom_end
                    end_point['cnt_segments'] = cnt_segments
                entry_start = self.network_dict.get(connection_node_start)
                if entry_start is None:
                    self.network_dict[connection_node_start] = {
                        'calc_type': calc_type,
                        'content_type_id': object_id,
                        'content_type': name,
                        'start_points': [],
                        'end_point': '',
                    }
                else:
                    self._elect_new_leader(entry_start, calc_type, object_id, name)
                # boundary and manhole are just points.
                if start_point:
                    self.network_dict[connection_node_start]['start_points'].append(start_point)
                if connection_node_end is not None:
                    entry_end = self.network_dict.get(connection_node_end)
                    if entry_end is None:
                        self.network_dict[connection_node_end] = {
                            'calc_type': calc_type,
                            'content_type_id': object_id,
                            'content_type': name,
                            'start_points': [],
                            'end_point': end_point,
                        }
                    else:
                        elected = self._elect_new_leader(entry_end, calc_type, object_id, name)
                        if elected:
                            self.network_dict[connection_node_end]['end_point'] = end_point
    def _elect_new_leader(self, entry, calc_type, object_id, name):
        """
        :returns True if a new leader has been elected, False otherwise
        """
        current_leader = entry.get('calc_type')
        _current_content_type = entry.get('content_type')
        unranked_calc_types = [current_leader, calc_type]
        ranked_calc_type = min(unranked_calc_types, key=custom_order.index)
        # we have a new leader
        if ranked_calc_type != current_leader:
            print "we have a new leader: calc_type was {} ({}) is now {} ({})".format(current_leader, _current_content_type, ranked_calc_type, name)
            entry['calc_type'] = ranked_calc_type
            entry['object_id'] = object_id
            entry['content_type'] = name
            return True
        return False
    def get_epsg_code(self):
        try:
            self.query.exec_('''SELECT epsg_code FROM v2_global_settings;''')
            self.query.next()
            return query.value(0)
        except AttributeError:
            self._uri.setDataSource(self._schema, 'v2_global_settings', '')
            vlayer = QgsVectorLayer(uri.uri(), '__none__', self.flavor)
            f = vlayer.getFeatures().next()
            return f['epsg_code']
    def _create_mem_layer(self, epsg_code, lyr_type="Point"):
        _type_map = {
            'str': QVariant.String,
            'int': QVariant.Int,
            'float': QVariant.Double
        }
        # create layer
        lyr_def_str = lyr_type
        if epsg_code:
            lyr_def_str = "{lyr_type}?crs=EPSG:{epsg_code}".format(
                lyr_type=lyr_type, epsg_code=epsg_code
            )
        self.mem_layer = QgsVectorLayer(lyr_def_str, self.lyr_name, "memory")
        # crs = self.mem_layer.crs()
        # if not crs.createFromId(int(epsg_code)):
        #     raise RuntimeError("Could not create crs from EPSG code {}".format(epsg_code))
        # self.mem_layer.setCrs(crs)
        self.data_provider = self.mem_layer.dataProvider()
        # add fields
        if self.fields is None:
            _fields = [QgsField("id", QVariant.Int)]
        else:
            _fields = [
                (QgsField(field_name, _type_map[field_type]))
                for field_name, field_type in self.fields
            ]
        self.data_provider.addAttributes(_fields)
        self.mem_layer.updateFields() # tell the vector layer to fetch changes from the provider
    def create_pnts_at(self, channel, table_name="", metric_epsg=None):
        geom = channel.geometry()
        # d = QgsDistanceArea()
        # d.setEllipsoidalMode(True)
        # geom_length = d.measureLine(geom.asPolyline())
        # # 2=degrees; 0=meters; False=isArea
        # line_length = d.convertMeasurement(geom_length, 2, 0, False)[0]
        if metric_epsg is not None:
            source_crs = QgsCoordinateReferenceSystem(4326)
            dest_crs = QgsCoordinateReferenceSystem(28992)
            trans = QgsCoordinateTransform(source_crs, dest_crs)
            trans_back = QgsCoordinateTransform(dest_crs, source_crs)
            geom.transform(trans)
        current_calc_type = channel['calculation_type']
        distance = channel['dist_calc_points']
        line_length = geom.length()
        print("line length   ", line_length)
        # TODO incorperate Attributes
        # line_length = geom.length()
        dists = self.get_distances_on_line(distance, line_length)
        # start_point = QgsPoint(geom[0])
        # end_point = QgsPoint(geom[-1])
        # self.known_pnts.add(start_point)
        # self.known_pnts.add(end_point)
        print('dists   ', dists)
        for i, dist in enumerate(dists, start=1):
            # Get a point along the line at the current distance
            point = geom.interpolate(dist)
            # add start and endpoint
            if i == 1 or i == len(dists):
                print "start or endpoint [{}]".format(i)
                # print "seen point {} before ".format(point.exportToWkt())
                xy = (point.asPoint().x(), point.asPoint().y())
                print "xy ", xy
                # known_calc_types = self.known_pnts.get(xy)
                # _known_calc_types = known_calc_types + [current_calc_type]
                # ranked_calc_type = min(_known_calc_types, key=custom_order.index)
                # if known_calc_types is not None and ranked_calc_type != current_calc_type:
                if xy in self.known_pnts:
                    print "seen point {} before ".format(xy)
                    continue
                # self.known_pnts[xy] = _known_calc_types
                self.known_pnts.add(xy)
            print 'step ', i, 'point ', point
            # Create a new QgsFeature and assign it the new geometry
            # add a feature
            f = QgsFeature()
            if metric_epsg is not None:
                point.transform(trans_back)
            f.setGeometry(point)
            ref_id = '{obj_id}-{table_name}-{calc_pnt}'.format(obj_id=channel['id'], table_name=table_name, calc_pnt=i)
            f.setAttributes([ref_id, channel['id'], current_calc_type])
            self.data_provider.addFeatures([f])
            # update layer's extent when new features have been added
            # because change of extent in provider is not propagated to the layer
        self.mem_layer.updateExtents()
    def remove_mem_layer(self):
        QgsMapLayerRegistry.instance().removeMapLayers( [self.mem_layer.id()] )
    def add_mem_layer(self):
        QgsMapLayerRegistry.instance().addMapLayer(self.mem_layer)
    def get_distances_on_line(self, distance, line_length, include_dest=False):
        cnt_segs = max(int(round(line_length / (distance * 1.0))), 1)
        dists = [0]
        current_dist = 0
        corrected_distance = float(line_length) / float(cnt_segs)
        print "corrected_distance ", corrected_distance
        if not include_dest:
            cnt_segs -= 1
        for seg in xrange(int(cnt_segs)):
            current_dist += corrected_distance
            dists.append(current_dist)
        return dists
    def _obj_leads(self, current_node_id, content_type, content_type_id):
        """
        :returns True if the the given object with
        :param content_type_id of
        :param content_type somewhere in the network has the lead
        False otherwise
        """
        for node_id, leader in self.network_dict.iteritems():
            if all([leader['content_type'] == content_type,
                    leader['content_type_id'] == content_type_id,
                    node_id != current_node_id]):
                return True
        return False
    def predict_points(self):
        for node_id, node_info in self.network_dict.iteritems():
            print "processing node_id {}".format(node_id)
            # for the first point we need the network calc_type
            node_calc_type = node_info['calc_type']
            # an entry for end_point means we have to use this his information
            # over other information for the node
            end_point  = node_info.get('end_point')
            node_has_been_added = False
            if end_point:
                content_type = end_point['content_type']
                content_type_id = end_point['content_type_id']
                pnt_geom = QgsGeometry.fromWkt(
                    end_point['the_geom_end']
                )
                last_seq_id = end_point['cnt_segments']
                # if the same objects will used elsewhere as starting point
                # the sequence of calculation points be longer (by one)
                if self._obj_leads(node_id, content_type, content_type_id):
                    last_seq_id += 1
                self._add_feature(
                    calc_type=node_calc_type, pnt_geom=pnt_geom,
                    content_type_id=content_type_id, content_type=content_type,
                    id=last_seq_id
                )
                node_has_been_added = True
            start_points  = node_info.get('start_points')
            for i, start_point in enumerate(start_points):
                content_type = start_point['content_type']
                content_type_id = start_point['content_type_id']
                # the caluclation type for the interpolated points
                calc_type = start_point['calc_type']
                distances = self.get_distances_on_line(
                    start_point['dist_calc_pnts'],
                    start_point['line_length']
                )
                print "processing start point {}".format(i)
                line_geom = QgsGeometry.fromWkt(
                    start_point['the_geom']
                )
                if not node_has_been_added:
                    # find out if the node info has been derived
                    # from the object we are looking at right now
                    # so we can produce the corect meta data like
                    # calc_type, user-ref-id,...
                    distance = distances.pop(0)
                    start_pnt = line_geom.interpolate(distance)
                    self._add_feature(
                        calc_type=node_calc_type,
                        pnt_geom=start_pnt,
                        content_type_id=node_info['content_type_id'],
                        content_type=node_info['content_type'],
                        id=1
                    )
                    node_has_been_added = True
                    print "node has been added {} {}".format(content_type, content_type_id)
                else:
                    distances = distances[1:]
                print('distances   ', distances)
                start_id = 1
                if all([node_info['content_type'] == content_type,
                        node_info['content_type_id'] == content_type_id]):
                    start_id = 2
                for i, dist in enumerate(distances, start=start_id):


                    # Get a point along the line at the current distance
                    point_on_line = line_geom.interpolate(dist)
                    # add start and endpoint
                    print 'step ', i
                    self._add_feature(
                         calc_type=calc_type,
                         pnt_geom=point_on_line,
                         content_type_id=content_type_id,
                         content_type=content_type,
                         id=i
                    )
        self.data_provider.addFeatures(self._features)
        self.mem_layer.updateExtents()
    def _add_feature(self, calc_type, pnt_geom, content_type_id, content_type, id):
        # Create a new QgsFeature and assign it the new geometry
        # add a feature
        f = QgsFeature()
        f.setGeometry(pnt_geom)
        ref_id = '{obj_id}-{table_name}-{seq_id}'.format(
            obj_id=content_type_id,
            table_name=content_type,
            seq_id=id
        )
        f.setAttributes(
            [ref_id, content_type_id, calc_type]
        )
        self._features.append(f)




martijn_kwargs = {
    'flavor': 'postgres',
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
viewtest_kwargs = {
    'flavor': 'postgres',
    'address': '10.0.3.111',
    'port': '5432',
    'name': 'work_viewtest',
    'user_name':'buildout',
    'password': 'buildout',
    'schema': 'public',
}


calc_pnts_fields = (('ref_id', 'str'), ('content_type_id', 'int'), ('calc_type', 'int'))
ranks = [100, 101, 105, 102]

where_clauses = [
    u'"calculation_type" = {}'.format(rank) for rank in ranks
]

pal = PointsAlongLine(flavor='postgres', fields=calc_pnts_fields, epsg_code=28992)
uri = pal.get_uri(**viewtest_kwargs)
pal.create_query_obj_from_uri(uri)
pal.build_calc_type_dict()
pal.predict_points()
# def _obj_leads(network, content_type, content_type_id):
#     for leader in network.itervalues():
#         if all([leader['content_type'] == content_type,
#                 leader['object_id'] == content_type_id]):
#             return True
#     return False










            f.setGeometry(point)
            ref_id = '{obj_id}-{table_name}-{calc_pnt}'.format(obj_id=channel['id'], table_name=table_name, calc_pnt=i)
            f.setAttributes([ref_id, channel['id'], current_calc_type])


        geom = channel.geometry()
        # d = QgsDistanceArea()
        # d.setEllipsoidalMode(True)
        # geom_length = d.measureLine(geom.asPolyline())
        # # 2=degrees; 0=meters; False=isArea
        # line_length = d.convertMeasurement(geom_length, 2, 0, False)[0]
        if metric_epsg is not None:
            source_crs = QgsCoordinateReferenceSystem(4326)
            dest_crs = QgsCoordinateReferenceSystem(28992)
            trans = QgsCoordinateTransform(source_crs, dest_crs)
            trans_back = QgsCoordinateTransform(dest_crs, source_crs)
            geom.transform(trans)
        current_calc_type = channel['calculation_type']
        distance = channel['dist_calc_points']
        line_length = geom.length()
        print("line length   ", line_length)
        # TODO incorperate Attributes
        # line_length = geom.length()
        dists = self.get_cnt_for_line(distance, line_length)
        # start_point = QgsPoint(geom[0])
        # end_point = QgsPoint(geom[-1])
        # self.known_pnts.add(start_point)
        # self.known_pnts.add(end_point)
        print('dists   ', dists)
        for i, dist in enumerate(dists, start=1):
            # Get a point along the line at the current distance
            point = geom.interpolate(dist)
            # add start and endpoint
            if i == 1 or i == len(dists):
                print "start or endpoint [{}]".format(i)
                # print "seen point {} before ".format(point.exportToWkt())
                xy = (point.asPoint().x(), point.asPoint().y())
                print "xy ", xy
                # known_calc_types = self.known_pnts.get(xy)
                # _known_calc_types = known_calc_types + [current_calc_type]
                # ranked_calc_type = min(_known_calc_types, key=custom_order.index)
                # if known_calc_types is not None and ranked_calc_type != current_calc_type:
                if xy in self.known_pnts:
                    print "seen point {} before ".format(xy)
                    continue
                # self.known_pnts[xy] = _known_calc_types
                self.known_pnts.add(xy)
            print 'step ', i, 'point ', point
            # Create a new QgsFeature and assign it the new geometry
            # add a feature
            f = QgsFeature()
            if metric_epsg is not None:
                point.transform(trans_back)
            f.setGeometry(point)
            ref_id = '{obj_id}-{table_name}-{calc_pnt}'.format(obj_id=channel['id'], table_name=table_name, calc_pnt=i)
            f.setAttributes([ref_id, channel['id'], current_calc_type])
            self.data_provider.addFeatures([f])



# postgres testing
# ----------------
pal = PointsAlongLine(
    flavor='postgres', lyr_name="test_pnts",
    fields=calc_pnts_fields
)
pal.create_query_obj_from_uri(uri)
pal.build_calc_type_dict()

uri = pal.get_uri(**martijn_kwargs)
channel_layer = pal.get_layer_from_uri(
    uri, table_name=martijn_kwargs['table_name'],
    display_name=martijn_kwargs['layer_name'],
    geom_column=martijn_kwargs['geom_column'],
)
for expr in where_clauses:
    request = QgsFeatureRequest().setFilterExpression(expr)
    features = channel_layer.getFeatures(request)
    for channel in features:
        pal.create_pnts_at(channel, martijn_kwargs['table_name'])


features = channel_layer.getFeatures()
pal.create_query_obj_from_uri(uri)
epsg_code = pal.get_epsg_code()
pal.query.exec_('''SELECT id, dist_calc_points, ST_AsText(ST_Transform(the_geom, {epsg_code}}) as the_geom FROM {table_name};'''.format(epsg_code=epsg_code, table_name=test_kwargs['table_name']))
while pal.query.next():
    geom_txt = pal.query.value(2)
    dist_calc_pnts= pal.query.value(1)
    geom = QgsGeometry.fromWkt(geom_txt)
    pal.create_pnts_at(geom, dist_calc_pnts)


pal.add_mem_layer()




sqlite_kwargs = {
    'address': '/home/lars_claussen/Development/model_data/v2_bergermeer/4c8a2e214a954a0f3a870888ac9e368233fc00b9/v2_bergermeer.sqlite',
    'port': '',
    'name': '',
    'user_name':'',
    'password': '',
    'schema': '',
    'table_name': 'v2_channel',
    'geom_column': 'the_geom',
    'layer_name': 'channel_sqlite',
}


# sqlite testing
# --------------
pal = PointsAlongLine(
    flavor='spatialite', lyr_name="test_pnts",
    fields=calc_pnts_fields, epsg_code=4326
)
channel_layer = pal.get_layer_from_uri(
    uri, table_name=sqlite_kwargs['table_name'],
    geom_column=sqlite_kwargs['geom_column'],
    display_name=sqlite_kwargs['layer_name']
)
uri = pal.get_uri(**sqlite_kwargs)
metric_epsg = pal.get_epsg_code() or 28992
for expr in where_clauses:
    request = QgsFeatureRequest().setFilterExpression(expr)
    features = channel_layer.getFeatures(request)
    for channel in features:
        pal.create_pnts_at(channel, sqlite_kwargs['table_name'], metric_epsg)


for expr in where_clauses:
    request = QgsFeatureRequest().setFilterExpression(expr)
    features = channel_layer.getFeatures(request)
    for channel in features:
        rrr.create_pnts_at(channel, sqlite_kwargs['table_name'])

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
