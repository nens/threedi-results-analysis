from qgis.gui import QgsRubberBand, QgsVertexMarker
from qgis.core import QgsDistanceArea, QgsProject, QgsCoordinateTransform, QgsWkbTypes, QgsPointXY, QgsUnitTypes
from qgis.PyQt.QtCore import Qt


class SideViewMapVisualisation(object):
    """
    Class managing the rubber band and vertex marker indicating the route of the
    sideview.
    """

    def __init__(self, iface, source_crs):
        self.iface = iface

        self.source_crs = source_crs

        self.rb = QgsRubberBand(self.iface.mapCanvas(), QgsWkbTypes.LineGeometry)
        self.rb.setColor(Qt.red)
        self.rb.setWidth(2)

        self.point_markers = []
        self.active_route = None

        self.hover_marker = QgsVertexMarker(self.iface.mapCanvas())
        self.hover_marker.setIconType(QgsVertexMarker.ICON_X)
        self.hover_marker.setColor(Qt.red)
        self.hover_marker.setPenWidth(6)

        self.dist_calc = QgsDistanceArea()

    def close(self):
        self.reset()
        self.iface.mapCanvas().scene().removeItem(self.hover_marker)

    def set_sideview_route(self, route):

        self.reset()

        self.active_route = route
        transform = QgsCoordinateTransform(
            self.source_crs, QgsProject.instance().crs(), QgsProject.instance()
        )

        for pnt in route.path_vertexes:
            t_pnt = transform.transform(pnt)
            self.rb.addPoint(t_pnt)

        for point, point_id, dist in route.path_points:

            marker = QgsVertexMarker(self.iface.mapCanvas())
            marker.setIconType(QgsVertexMarker.ICON_CIRCLE)
            marker.setColor(Qt.red)
            marker.setPenWidth(4)
            marker.setCenter(transform.transform(point))
            self.point_markers.append(marker)

    def reset(self):
        self.rb.reset()
        self.active_route = None

        for marker in self.point_markers:
            self.iface.mapCanvas().scene().removeItem(marker)

        self.point_markers = []

        self.hover_marker.setCenter(QgsPointXY(0.0, 0.0))

    def hover_graph(self, meters_from_start):

        transform = QgsCoordinateTransform(
            self.source_crs, QgsProject.instance().crs(), QgsProject.instance()
        )

        if self.active_route is None:
            return

        if meters_from_start < 0.0:
            meters_from_start = 0.0
        elif (
            len(self.active_route.path) > 0
            and meters_from_start > self.active_route.path[-1][-1][1]
        ):
            meters_from_start = self.active_route.path[-1][-1][1]

        for route_part in self.active_route.path:
            if meters_from_start <= route_part[-1][1]:
                for part in route_part:
                    if meters_from_start <= part[1]:
                        if part[3] == 1:
                            distance_on_line = meters_from_start - part[0]
                        else:
                            distance_on_line = part[1] - meters_from_start

                        conversion_factor = QgsUnitTypes.fromUnitToUnitFactor(
                            QgsUnitTypes.DistanceMeters, QgsUnitTypes.DistanceDegrees
                        )
                        length = distance_on_line * conversion_factor
                        point = part[4].geometry().interpolate(length)
                        if point.isEmpty():
                            return
                        self.hover_marker.setCenter(
                            transform.transform(point.asPoint())
                        )
                        return

    def hover_map(self, point_geometry):
        pass

    def show_selectable_points(self, graph_tree):
        pass

    def hide_selectable_points(self):
        pass
