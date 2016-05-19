
from qgis.core import QgsFeature, QgsGeometry, QgsPoint
import math

def split_line_at_points(polyline, points, start_node_field='',
                        end_node_field='', node_id_field='',
                        distance_field='start_distance'):
    """
        Split line at points
    Args
        channel QgsPolyline:
        points (iteratable object of QgsFeature):
        start_node_field:
        end_node_field:
        node_id_field:
        distance_field:
    Returns:
         (list of QgsFeature): Splitted polyline into parts
    """

    for point in points:


        closeSegResult = polyline.geometry().closestSegmentWithContext(
                points.asPoint())
        closePoint = closeSegResult[1]
        snapGeometry = QgsGeometry.fromPoint(
            QgsPoint(closePoint[0], closePoint[1]))

        at_vertex = closeSegResult[0]

        p1 = ptGeom.asPoint() # first vertex
        p2 = snapGeometry.asPoint()

        dist = math.hypot(p2.x() - p1.x(), p2.y() - p1.y())

    pass