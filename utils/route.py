# -*- coding: utf-8 -*-
from builtins import str
from builtins import object
from qgis.PyQt.QtCore import QVariant

from qgis.analysis import (
    QgsGraphBuilder,
    QgsNetworkDistanceStrategy,
    QgsGraphAnalyzer,
    QgsNetworkStrategy,
)

from qgis.core import (
    QgsVectorLayer,
    QgsField,
    QgsFeature,
    QgsGeometry,
    QgsFeatureRequest,
    QgsPoint,
)


class AttributeProperter(QgsNetworkStrategy):
    """custom properter"""

    def __init__(self, attribute, attribute_index):
        QgsNetworkStrategy.__init__(self)
        self.attribute = attribute
        self.attribute_index = attribute_index

    def cost(self, distance, feature):
        if self.attribute == "ROWID":
            value = feature.id()
        else:
            value = feature[self.attribute]
        return value

    def requiredAttributes(self):
        # Must be a list of the attribute indexes (int), not strings:
        attributes = [self.attribute_index]
        return attributes


class Route(object):
    def __init__(
        self,
        line_layer,
        director,
        weight_properter=QgsNetworkDistanceStrategy(),
        distance_properter=QgsNetworkDistanceStrategy(),
        id_field="ROWID",
    ):

        self.line_layer = line_layer
        self.director = director
        self.id_field = id_field
        self.id_field_index = self.line_layer.fields().lookupField(self.id_field)

        # build graph for network
        properter_1 = weight_properter
        properter_2 = distance_properter
        properter_3 = AttributeProperter(self.id_field, self.id_field_index)
        self.director.addStrategy(properter_1)
        self.director.addStrategy(properter_2)
        self.director.addStrategy(properter_3)
        # self.director.addStrategy(QgsNetworkDistanceStrategy())
        crs = self.line_layer.crs()
        self.builder = QgsGraphBuilder(crs)
        self.director.makeGraph(self.builder, [])
        self.graph = self.builder.graph()

        # init class attributes
        self.start_point_tree = None
        self.has_path = False
        self.cost = []
        self.tree = []
        self.path = []
        self.path_vertexes = []
        self.point_path = []
        self.tree_layer_up_to_date = False
        self._virtual_tree_layer = None

        self.path_points = []

    def add_point(self, qgs_point):
        """

        :param qgs_point: QgsPoint instances, additional point
        :return: tuple (boolean: successful added to path,
                        string: message)
        """
        id_point = self.graph.findVertex(qgs_point)
        if not id_point:
            return False, "point is not on a vertex of the route graph"
        else:
            distance = 0
            if len(self.path_points) > 0:
                # not first point, get path between previous point and point
                success, path, p = self.get_path(
                    self.id_start_tree, id_point, self.path_points[-1][2]
                )

                if not success:
                    # not path found between previous point and point
                    msg = path
                    return False, msg

                self.path.append(path)
                distance = path[-1][1]

                self.path_vertexes.extend(p)
                self.has_path = True

            self.path_points.append((qgs_point, id_point, distance))

            # set (new) tree from last point
            self.set_tree_startpoint(id_point)

            return True, "point found and added to path"

    def scan_point(self, qgs_point):

        # returns path, without adding point to path
        pass

    def get_id_of_point(self, qgs_point):

        return self.graph.findVertex(qgs_point)

    def set_tree_startpoint(self, id_start_point):
        """
        set point (initial or next point) for expending path
        :param qgs_start_point: QgsPoint instance, start point of tree for
                (extension) of path
        :return:
        """
        if id_start_point == -1:
            return False, "No valid point found"

        # else create tree from this tree startpoint
        self.id_start_tree = id_start_point
        self.start_point_tree = self.graph.vertex(id_start_point).point()

        (self.tree, self.cost) = QgsGraphAnalyzer.dijkstra(
            self.graph, self.id_start_tree, 0
        )
        self.tree_layer_up_to_date = False
        if self._virtual_tree_layer:
            self.update_virtual_tree_layer()

    def get_path(self, id_start_point, id_end_point, begin_distance=0):
        """
        get path between the to graph points
        :param id_start_point: graph identifier of start point of (sub)path
        :param id_end_point: graph identifier of end point of (sub) path
        :param begin_distance: start distance of cumulative path distance
        :return: tuple with 3 values:
                 - successful found a path
                 - Message in case of not succesful found a path or
                   a list of path line elements, represent as a tuple, with:
                   - begin distance of part (from initial start_point),
                   - end distance of part
                   - direction of path equal to direction of feature definition
                     1 in case ot is, -1 in case it is the opposite direction
                   - feature
                 - list of vertexes (graph nodes)
        """

        # check if end_point is connected to start point
        if self.tree[id_end_point] == -1:
            return False, "Path not found", None

        # else continue finding path
        p = []
        path_props = []
        cum_dist = begin_distance
        cur_pos = id_end_point
        while cur_pos != id_start_point:
            point = self.graph.vertex(
                self.graph.edge(self.tree[cur_pos]).toVertex()
            ).point()
            p.append(point)

            dist = self.graph.edge(self.tree[cur_pos]).strategies()[1]

            id_line = self.graph.edge(self.tree[cur_pos]).strategies()[2]

            filt = u'"%s" = %s' % (self.id_field, str(id_line))
            request = QgsFeatureRequest().setFilterExpression(filt)
            feature = next(self.line_layer.getFeatures(request))

            if QgsPoint(point.x(), point.y()) == feature.geometry().vertexAt(0):
                # current point on tree (end point of this line) is equal to
                # begin of original feature, so direction is opposite: -1
                route_direction_feature = -1
            else:
                route_direction_feature = 1

            path_props.insert(0, [None, None, dist, route_direction_feature, feature])

            cur_pos = self.graph.edge(self.tree[cur_pos]).fromVertex()

        for path in path_props:
            path[0] = cum_dist
            cum_dist += path[2]
            path[1] = cum_dist

        p.append(self.start_point_tree)

        return True, path_props, reversed(p)

    def update_virtual_tree_layer(self):
        """
        update virtual layer with latest tree
        :return: boolean, successful updated
        """

        if not self._virtual_tree_layer:
            # not yet created
            return True

        if self.tree_layer_up_to_date:
            # layer already up to date
            return True

        ids = [feat.id() for feat in self._virtual_tree_layer.getFeatures()]
        self._virtual_tree_layer.dataProvider().deleteFeatures(ids)

        features = []
        for branch in self.tree:
            # make int, compare with long doesn't work (?!)
            if int(branch) >= 0:
                # add a feature
                feat = QgsFeature()
                a = self.graph.vertex(self.graph.edge(branch).fromVertex()).point()
                b = self.graph.vertex(self.graph.edge(branch).toVertex()).point()
                feat.setGeometry(QgsGeometry.fromPolylineXY([a, b]))

                feat.setAttributes(
                    [
                        float(self.graph.edge(branch).strategies()[1]),
                        int(self.graph.edge(branch).strategies()[2]),
                    ]
                )
                features.append(feat)

        self._virtual_tree_layer.dataProvider().addFeatures(features)
        self._virtual_tree_layer.commitChanges()
        self._virtual_tree_layer.updateExtents()
        self._virtual_tree_layer.triggerRepaint()
        return True

    def get_virtual_tree_layer(self):
        """
        return a (link to) an in memory QgsVectorLayer of the current active
        tree. The layer will be updated during when the tree (or tree start
        point) changes
        :return: QgsVectorLayer in memory.
        """
        # Enter editing mode

        if not self._virtual_tree_layer:
            # create_layer
            self._virtual_tree_layer = QgsVectorLayer(
                "linestring?crs=epsg:4326", "temporary_lines", "memory"
            )

            self._virtual_tree_layer.dataProvider().addAttributes(
                [
                    QgsField("weight", QVariant.Double),
                    QgsField("line_id", QVariant.LongLong),
                ]
            )

            self._virtual_tree_layer.commitChanges()

        if not self.tree_layer_up_to_date:
            self.update_virtual_tree_layer()

        return self._virtual_tree_layer

    def reset(self):
        """
        reset found route
        :return:
        """

        self.id_start_tree = None
        # self.id_end = None
        self.start_point_tree = None
        self.cost = []
        self.tree = []
        self.has_path = False
        self.path_points = []
        self.path = []
        self.path_vertexes = []
