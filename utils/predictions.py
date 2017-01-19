from PyQt4.QtCore import QVariant, QPyNullVariant

from PyQt4 import QtSql
from qgis.core import (
    QgsFeature, QgsGeometry,
    QgsVectorLayer, QgsMapLayerRegistry,
    QgsField, QgsDataSourceURI,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform
)

from sqlalchemy.exc import ResourceClosedError

from ThreeDiToolbox.utils.raw_sql import get_query_strings
from ThreeDiToolbox.utils import constants

from ThreeDiToolbox.utils.threedi_database import ThreediDatabase

import logging

logger = logging.getLogger(__name__)


class Predictor(object):
    _QUERY_TYPE_DICT = {
        'postgres': 'QPSQL',
        'spatialite': 'QSQLITE',
        'spatialite2': 'QSQLITE2'
    }

    def __init__(self, flavor, lyr_name=""):
        self.flavor = flavor
        self.lyr_name = lyr_name
        if not self.lyr_name:
            self.lyr_name = "temporary_lyr"
        self.data_provider = None
        self.mem_layer = None
        self._schema = None  # will passed to get_uri()
        self.query = None
        self.network_dict = {}
        self._calc_pnt_features = []
        self._connected_pnt_features = []
        self._trans = None

    def get_uri(self, **kwargs):
        """
        :returns an QgsDataSourceURI() instance

        kwargs :
            'host' --> network address (postgres) or
                file path location (spatialite)
            'port' --> port for the network address. Can
                be omitted for spatialite
            'user_name' --> database credential. Can
                be omitted for spatialite
            'password' --> database credential. Can
                be omitted for spatialite
            'schema' --> database schema name

         """

        self._uri = QgsDataSourceURI()
        host = kwargs['host']
        port = kwargs['port']
        database = kwargs['database']
        username = kwargs['username']
        password = kwargs['password']
        self._schema = kwargs['schema']
        if self.flavor == 'spatialite':
            self._uri.setDatabase(host)
        elif self.flavor == 'postgres':
            self._uri.setConnection(host, port, database, username, password)
        return self._uri

    def start_sqalchemy_engine(self, kwargs):
        """
        kwargs :
            'host' --> network address (postgres) or
                file path location (spatialite)
            'port' --> port for the network address. Can
                be omitted for spatialite
            'user_name' --> database credential. Can
                be omitted for spatialite
            'password' --> database credential. Can
                be omitted for spatialite
            'schema' --> database schema name
        """
        threedi_db = ThreediDatabase(kwargs, db_type=self.flavor)
        self.engine = threedi_db.get_engine()

    def get_layer_from_uri(self, uri, table_name, geom_column='',
                           display_name=''):
        """
        :returns a vector layer instance of the given
        :param table_name in combination with the
        :param geom_column
        :param uri: QgsDataSourceURI() instance
        :param display_name: defaults to ``table_name``
        """
        if not display_name:
            display_name = table_name
        uri.setDataSource(self._schema, table_name, geom_column)
        vlayer = QgsVectorLayer(uri.uri(), display_name, self.flavor)
        return vlayer

    def create_query_obj_from_uri(self, uri):
        """
        creates an QtSql.QSqlQuery(db) instance with the database
        information stored in uri-object
        """
        db_type_identifier = self._QUERY_TYPE_DICT[self.flavor]
        db = QtSql.QSqlDatabase.addDatabase(db_type_identifier)
        db.setHostName(uri.host())
        try:
            db.setPort(int(uri.port()))
        except ValueError:
            pass
        db.setDatabaseName(uri.database())
        db.setUserName(uri.username())
        db.setPassword(uri.password())
        ok = db.open()
        if ok:
            self.query = QtSql.QSqlQuery(db)
        else:
            raise RuntimeError(
                'Failed to open database connection: {}'.format(
                    db.lastError().driverText())
            )

    def run_qtsql_query(self, query_str):
        """
        execute a sql query. If the execution was successful the
        result rows can retrieved by ``query.next()``
        """
        if self.query is None:
            self.create_query_obj_from_uri(self._uri)
        if not self.query.exec_(query_str):
            raise RuntimeError(
                'Could not execute the query {}. '
                'Error message {}'.format(
                    query_str, self.query.lastError().text())
            )

    def run_sqalchemy_query(self, query_str):
        with self.engine.connect() as con:
            res = con.execute(query_str)
            try:
                rows = res.fetchall()
            except ResourceClosedError:
                logger.warning(
                    '[!] The proxy object has been consumed because the '
                    'query has returned no results.')
                rows = None
        con.close()
        return rows

    def build_calc_type_dict(self, epsg_code):
        """
        The network dict contains all connection nodes as keys.
        The node itself has attributes that define its calculation type
        and the source of the calculation type definition. That is the
        object it has been derived from.
        While building the network dictionary the calculation type
        of every object (boundary point, manhole, channel,
        culvert, pipe) are tested against the defined
        ranking (-1 --> 0 --> 1 --> 5 --> 2). Whenever a object
        is ranked higher, the calculation type attributes
        will be overwritten. Furthermore all 1D objects that
        have their own geometry with their starting point on
        the connection node are attached in a list (pipes, culverts,
        channels).  Like this the calculation points can later be
        computed per dictionary entry. The last point of the line
        geometry, however,  should not be computed when predicting
        the calculation points because end points are listed
        separately to make sure they can be tested against the
        calculation type ranking, as well.
        <instance>.network_dict will look something like this::

            {1: {'calc_type': -1,
                 'content_type': 'v2_1d_boundary_conditions',
                 'content_type_id': 1,
                 'end_point': '',
                 'object_id': 1,
                 'start_points': [{'calc_type': 1,
                                   'cnt_segments': 8,
                                   'content_type': 'v2_pipe',
                                   'content_type_id': 1,
                                   'dist_calc_pnts': 5.0,
                                   'line_length': 40.0,
                                   'the_geom': u'LINESTRING(5 5,45 5)'}]},
             2: {'calc_type': 1,
                 'content_type': 'v2_pipe',
                 'content_type_id': 1,
                 'end_point': {'cnt_segments': 8,
                               'content_type': 'v2_pipe',
                               'content_type_id': 1,
                               'dist_calc_pnts': 5.0,
                               'the_geom_end': u'POINT(45 5)'},
                 'start_points': [{'calc_type': 1,
                                   'cnt_segments': 8,
                                   'content_type': 'v2_channel',
                                   'content_type_id': 1,
                                   'dist_calc_pnts': 5.0,
                                   'line_length': 40.0,
                                   'the_geom': u'LINESTRING(45 5,45 25,45 45)'}]},
        }
        """
        query_data = self._get_query_data(epsg_code)
        for name, d in query_data.iteritems():
            logger.info("processing {}".format(name))
            rows = self.run_sqalchemy_query(d['query'])
            if rows is None:
                continue
            for row in rows:
                # distinguish between start- and endpoints
                start_point = {}
                end_point = {}
                object_id = row[d['id']]
                # geometries can only be present for objects that have
                # both a start- and endpoint (culverts, pipes and channels)
                the_geom = None
                if d['the_geom'] is not None:
                    the_geom = row[d['the_geom']]
                the_geom_end = None
                if d['the_geom_end'] is not None:
                    the_geom_end = row[d['the_geom_end']]
                line_length = None
                if d['line_length'] is not None:
                    line_length = row[d['line_length']]
                dist_calc_points = None
                if d['dist_calc_points'] is not None:
                    dist_calc_points = row[d['dist_calc_points']]
                code = ''
                if d['code'] is not None:
                    code = row[d['code']] or ''
                connection_node_end = None
                if d['node_id_end'] is not None:
                    connection_node_end = row[d['node_id_end']]
                connection_node_start = None
                if d['node_id_start'] is not None:
                    connection_node_start = row[
                        d['node_id_start']
                    ]
                # not all objects must have a calculation type defined.
                # If the database field is empty the query will return NULL
                # N.B the operator has to be ``==``!
                _calc_type = row[d['calc_type']]
                calc_type = constants.CALC_TYPE_MAP.get(
                    _calc_type)
                if calc_type is None:
                    calc_type = _calc_type
                logger.debug(
                    "calc_type is ", calc_type, "type ", type(calc_type)
                )
                if calc_type is None:
                    logger.warning(
                        "WARNING: no calc_type for {name} {id}".format(
                            name=name, id=object_id)
                    )
                    continue
                # objects with a geometry have both a start- and endpoint
                if the_geom is not None:
                    # embedded channels usually do not have a
                    # dist_calc_points attribute
                    if dist_calc_points is None:
                        dist_calc_points = line_length

                    # define in how many segments the line geometry will
                    # be divided my the threedicore
                    cnt_segments = max(
                        int(round(
                            line_length / (dist_calc_points * 1.0))), 1
                    )
                    start_point['calc_type'] = calc_type
                    start_point['content_type'] = name
                    start_point['content_type_id'] = object_id
                    start_point['code'] = code
                    start_point['dist_calc_pnts'] = dist_calc_points
                    start_point['line_length'] = line_length
                    start_point['the_geom'] = the_geom
                    start_point['cnt_segments'] = cnt_segments
                    end_point = self._fill_end_pnt_dict(
                        end_point, name, object_id, code, the_geom_end,
                        dist_calc_points, cnt_segments
                    )

                entry_start = self.network_dict.get(connection_node_start)
                if entry_start is None:
                    try:
                        # a brand new entry
                        self.network_dict[connection_node_start] = {
                            'calc_type': calc_type,
                            'content_type_id': object_id,
                            'code': code,
                            'content_type': name,
                            'start_points': [],
                            'end_point': '',
                        }
                    except KeyError:
                        logger.debug(
                            "KeyError, connection_node_start is None."
                            "This is fine for manholes, the current "
                            "content type is {}".format(name)
                        )
                        pass
                else:
                    # already entry for this connection node, we need to
                    # check if the current calculation type is
                    # ranked higher
                    self._elect_new_leader(
                        entry_start, calc_type, object_id, name, code
                    )
                # there should never be a start point entry for
                # boundaries and manholes as they don't have geometries.
                if start_point:
                    self.network_dict[
                        connection_node_start]['start_points'].append(
                        start_point
                    )
                if connection_node_end is not None:
                    end_point = self._fill_end_pnt_dict(
                        end_point, name, object_id, code, the_geom_end)

                    entry_end = self.network_dict.get(connection_node_end)
                    if entry_end is None:
                        # a brand new entry
                        self.network_dict[connection_node_end] = {
                            'calc_type': calc_type,
                            'content_type_id': object_id,
                            'code': code,
                            'content_type': name,
                            'start_points': [],
                            'end_point': end_point,
                        }
                    else:
                        # already entry for this connection node, we
                        # need to check if the current calculation type
                        # is ranked higher
                        elected = self._elect_new_leader(
                            entry_end, calc_type, object_id, name, code
                        )
                        if elected:
                            self.network_dict[
                                connection_node_end]['end_point'] = end_point

    @staticmethod
    def _fill_end_pnt_dict(end_pnt_dict, name, object_id, code, the_geom_end,
                           dist_calc_points=None, cnt_segments=1):
        """
        All object with a line geometry have a complete set of end point
        attributes. This is the default. Because manholes have to be
        treated in a special manner this functions provides defaults
        for the attributes dist_calc_points and cnt_segments.
        """
        if not end_pnt_dict:
            end_pnt_dict['content_type'] = name
            end_pnt_dict['code'] = code
            end_pnt_dict['content_type_id'] = object_id
            end_pnt_dict['dist_calc_pnts'] = dist_calc_points
            end_pnt_dict['the_geom_end'] = the_geom_end
            end_pnt_dict['cnt_segments'] = cnt_segments
        return end_pnt_dict

    def _elect_new_leader(self, entry, calc_type, object_id, name, code):
        """
        compares the stored calculation type information with the current
        :param calc_type and updates the information whenever the calcualtion
        type is ranked higher
        :returns True if a new leader has been elected, False otherwise
        """
        _current_content_type = entry.get('content_type')
        # manhole is already the lead. Only a boundary can surpass him
        if all([_current_content_type == 'v2_manhole',
                name != 'v2_1d_boundary_conditions']):
            return False

        # make manhole the leader in case a boundary isn't
        # leading at the moment
        if all([name == 'v2_manhole',
                _current_content_type != 'v2_1d_boundary_conditions',
                calc_type is not None]):
            entry['calc_type'] = calc_type
            entry['content_type_id'] = object_id
            entry['code'] = code
            entry['content_type'] = name
            return True

        current_leader = entry.get('calc_type')
        unranked_calc_types = [current_leader, calc_type]
        ranked_calc_type = min(
            unranked_calc_types, key=constants.CALC_TYPE_RANKING.index
        )
        # we have a new leader
        if ranked_calc_type != current_leader:
            logger.debug(
                "we have a new leader: calc_type was {} ({}) "
                "is now {} ({})".format(
                    current_leader, _current_content_type,
                    ranked_calc_type, name)
            )
            entry['calc_type'] = ranked_calc_type
            entry['content_type_id'] = object_id
            entry['code'] = code
            entry['content_type'] = name
            return True
        return False

    def _get_query_data(self, with_epsg_code):
        """
        :param with_epsg_code: the epsg_code to load the data with
        """
        query_strings_dict = get_query_strings(
            flavor=self.flavor, epsg_code=with_epsg_code
        )
        # keys are the database table names.
        # query value --> database query string as plain text
        # all other values --> index of the attribute in the result collection
        query_data = {
            'v2_1d_boundary_conditions': {
                'query': query_strings_dict['v2_1d_boundary_conditions'],
                'node_id_start': 0,
                'node_id_end': None,
                'calc_type': 1,
                'the_geom': None,
                'line_length': None,
                'id': 2,
                'dist_calc_points': None,
                'the_geom_end': None,
                'code': None,
                },
            'v2_manhole': {
                'query': query_strings_dict['v2_manhole'],
                'node_id_start': None,
                'node_id_end': 0,
                'calc_type': 1,
                'the_geom': None,
                'line_length': None,
                'id': 2,
                'dist_calc_points': None,
                'the_geom_end': 3,
                'code': 4,
                },
            'v2_pipe': {
                'query': query_strings_dict['v2_pipe'],
                'node_id_start': 0,
                'node_id_end': 1,
                'calc_type': 2,
                'the_geom_end': 4,
                'the_geom': 5,
                'line_length': 6,
                'id': 7,
                'dist_calc_points': 8,
                'code': 9,
                },
            'v2_culvert': {
                'query': query_strings_dict['v2_culvert'],
                'node_id_start': 0,
                'node_id_end': 1,
                'calc_type': 2,
                'the_geom': 3,
                'line_length': 4,
                'id': 5,
                'dist_calc_points': 6,
                'the_geom_end': 7,
                'code': 8,
            },
            'v2_channel': {
                'query': query_strings_dict['v2_channel'],
                'node_id_start': 0,
                'node_id_end': 1,
                'calc_type': 2,
                'the_geom': 5,
                'line_length': 6,
                'id': 7,
                'dist_calc_points': 8,
                'the_geom_end': 4,
                'code': 9,
            },
        }
        return query_data

    def get_epsg_code(self):
        """
        get the epsg_code entry from v2_global_settings table (first row)
        """
        with self.engine.connect() as con:
            rs = con.execute('''SELECT epsg_code FROM v2_global_settings;''')
            row = rs.fetchone()
            if row:
                return row[0]
        con.close()

    def create_memory_layer(self, epsg_code, lyr_type="Point", fields=None):
        """
        create a QgsVectorLayer in memory
        """
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
        self.data_provider = self.mem_layer.dataProvider()
        # add fields
        if fields is None:
            _fields = [QgsField("id", QVariant.Int)]
        else:
            _fields = [
                (QgsField(field_name, _type_map[field_type]))
                for field_name, field_type in fields
            ]
        self.data_provider.addAttributes(_fields)
        # tell the vector layer to fetch changes from the provider
        self.mem_layer.updateFields()

    def remove_mem_layer(self):
        QgsMapLayerRegistry.instance().removeMapLayers([self.mem_layer.id()])

    def add_mem_layer(self):
        QgsMapLayerRegistry.instance().addMapLayer(self.mem_layer)

    def get_distances_on_line(self, distance, line_length, include_dest=False):
        cnt_segs = max(int(round(line_length / (distance * 1.0))), 1)
        dists = [0]
        current_dist = 0
        corrected_distance = float(line_length) / float(cnt_segs)
        logger.debug("corrected_distance ", corrected_distance)
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

    def predict_points(self, output_layer, transform=''):
        """
        Case connection node entry knows an endpoint
        --------------------------------------------
        Whenever an endpoint entry is present the current connection
        node is either a network endpoint or the endpoint belongs to the
        highest ranking calculation type. Either way, it has to be added to
        the feature collection.

        Once it is known that the starting point has been added, the objects
        with their own geometry (culverts, channels, pipes) for which
        the calculation points have to be predicted, do not need to add
        their starting point to the collection anymore.

        Case connection node entry doesn't know of an endpoint
        ------------------------------------------------------
        The starting point will be calculated based on start point
        of the first line geometry in combination with the calculation
        type attributes for the connection node of the current iteration.
        The object, that belongs to the line geometry will be matched
        against the calculation type information of the connection node.
        The outcome of the match is important to be able to produce
        correct ``user_ref_ids`` because they contain a substring based
        on the count of the calculation points belonging to the same object.
        """
        self._feat_id = 1
        data_provider = output_layer.dataProvider()
        self._set_coord_transformation(transform)
        for node_id, node_info in self.network_dict.iteritems():
            logger.debug("processing node_id {}".format(node_id))

            # for the first point we need the network calc_type
            node_calc_type = node_info['calc_type']
            # an entry for end_point means we have to use this his information
            # over other information for the node
            end_point = node_info.get('end_point')
            node_has_been_added = False
            start_id = 1
            if end_point:
                content_type = end_point['content_type']
                content_type_id = end_point['content_type_id']
                code = end_point['code']
                pnt_geom = QgsGeometry.fromWkt(
                    end_point['the_geom_end']
                )
                last_seq_id = end_point['cnt_segments']
                # if the same objects will used elsewhere as starting point
                # the sequence of calculation points will be longer (by one)
                if any([
                    self._obj_leads(node_id, content_type, content_type_id),
                        last_seq_id == 1]):
                    last_seq_id += 1
                self._add_calc_pnt_feature(
                    calc_type=node_calc_type, pnt_geom=pnt_geom,
                    content_type_id=content_type_id, content_type=content_type,
                    code=code, id=last_seq_id
                )
                node_has_been_added = True
                start_id = 2
            start_points = node_info.get('start_points')
            for i, start_point in enumerate(start_points):
                content_type = start_point['content_type']
                content_type_id = start_point['content_type_id']
                code = start_point['code']
                # the calculation type for the interpolated points
                calc_type = start_point['calc_type']
                distances = self.get_distances_on_line(
                    start_point['dist_calc_pnts'],
                    start_point['line_length']
                )
                logger.debug("processing start point {}".format(i))
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
                    self._add_calc_pnt_feature(
                        calc_type=node_calc_type,
                        pnt_geom=start_pnt,
                        content_type_id=node_info['content_type_id'],
                        content_type=node_info['content_type'],
                        code=node_info['code'],
                        id=1
                    )
                    node_has_been_added = True
                    start_id = 2
                    logger.debug(
                        "node has been added {} {}".format(
                            content_type, content_type_id)
                    )
                else:
                    distances = distances[1:]

                for i, dist in enumerate(distances, start=start_id):
                    # Get a point along the line at the current distance
                    point_on_line = line_geom.interpolate(dist)
                    # add start and endpoint
                    self._add_calc_pnt_feature(
                        calc_type=calc_type,
                        pnt_geom=point_on_line,
                        content_type_id=content_type_id,
                        content_type=content_type,
                        code=code,
                        id=i
                    )
        succces, features = data_provider.addFeatures(self._calc_pnt_features)
        cnt_feat = len(features)
        if succces:
            logger.info(
                "[*] Successfully saved {} features to the database".format(
                    cnt_feat)
            )
            output_layer.updateExtents()
        else:
            logger.error(
                'Error while saving {} feaures to database.'.format(cnt_feat)
            )
        return succces, features

    def _add_calc_pnt_feature(
            self, calc_type, pnt_geom, content_type_id,
            content_type, code, id):
        # Create a new QgsFeature and assign it the new geometry
        # add a feature
        f = QgsFeature()
        if self._trans:
            pnt_geom.transform(self._trans)
        f.setGeometry(pnt_geom)
        if calc_type < 0:
            content_type = 'v2_1d_boundary_conditions'
            id = 1
        ref_id = '{code}#{obj_id}#{table_name}#{seq_id}'.format(
            code=code,
            obj_id=content_type_id,
            table_name=content_type,
            seq_id=id
        )

        f.setAttributes(
            [self._feat_id, content_type_id, ref_id, calc_type]
        )
        self._calc_pnt_features.append(f)
        self._feat_id += 1

    def _add_connected_pnt_feature(self, the_geom, calc_pnt_id, field_names):
        # Create a new QgsFeature and assign it the new geometry
        # add a feature
        connected_pnt_data = {
            'id': self._connect_pnt_id,
            'exchange_level': -9999,
            'calculation_pnt_id': calc_pnt_id,
            'levee_id': None
        }
        f = QgsFeature()
        f.setGeometry(the_geom)
        fn_sorted = sorted(field_names, key=field_names.__getitem__)
        attributes = [connected_pnt_data[fn] for fn in fn_sorted]
        f.setAttributes(
            attributes
        )
        self._connected_pnt_features.append(f)
        self._connect_pnt_id += 1

    def _set_coord_transformation(self, transform):
        if not transform:
            return
        src_epsg, dest_epsg = transform.split(':')
        src_crs = QgsCoordinateReferenceSystem(int(src_epsg))
        dest_crs = QgsCoordinateReferenceSystem(int(dest_epsg))
        self._trans = QgsCoordinateTransform(src_crs, dest_crs)

    def fill_connected_pnts_table(self, calc_pnts_lyr, connected_pnts_lyr):
        data_provider = connected_pnts_lyr.dataProvider()
        connected_pnts_lyr_fields = connected_pnts_lyr.pendingFields()
        field_names_connected_pnts_lyr = [
            field.name() for field in connected_pnts_lyr_fields
        ]
        fn_dict_connected_pnts_lyr = {
            fn: connected_pnts_lyr_fields.indexFromName(fn)
            for fn in field_names_connected_pnts_lyr
        }

        field_names_calc_pnts = [
            field.name() for field in calc_pnts_lyr.pendingFields()
        ]
        self._connect_pnt_id = 1
        for feat in calc_pnts_lyr.getFeatures():
            calc_pnt = dict(zip(field_names_calc_pnts, feat.attributes()))
            calc_type = calc_pnt['calc_type']
            if calc_type < 2:
                continue
            self._add_connected_pnt_feature(
                feat.geometry(), calc_pnt_id=calc_pnt['id'],
                field_names=fn_dict_connected_pnts_lyr,
            )

        succces, features = data_provider.addFeatures(
            self._connected_pnt_features
        )
        cnt_feat = len(features)
        if succces:
            logger.info(
                "[*] Successfully saved {} features to the database".format(
                    cnt_feat)
            )
            connected_pnts_lyr.updateExtents()
        else:
            logger.error(
                'Error while saving {} feaures to database.'.format(cnt_feat)
            )
        return succces, features
