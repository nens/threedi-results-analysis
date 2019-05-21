from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsCoordinateTransform
from qgis.core import QgsFeature
from qgis.core import QgsGeometry
from qgis.core import QgsPoint
from qgis.core import QgsProject

import math


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    Source: http://gis.stackexchange.com/a/56589
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = list(map(math.radians, [lon1, lat1, lon2, lat2]))
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km


def split_line_at_points(
    polyline_input,
    point_features,
    point_feature_id_field="id",
    start_node_id=None,
    end_node_id=None,
):
    """
        Split line at points
    Args
        polyline (QgsPolyline):
        point_features (iteratable object of QgsFeature or
                        list of dictonaries with id and geometry ('geom'):
        point_feature_id_field (str): fieldname if the id field of the
                                      point_features
        start_node_id (str or int): node id of point at begin of polyline
        end_node_id (str or int): node id of point at end of polyline
    Returns:
         (list of dict): Splitted polyline into parts as dictonary with:
                        geom: Polyline geometry
                        start_node_id: id of node at starting point of line
                        end_node_id: id of node at end point of line
                        distance at line: is distance of original line at
                                the begin of this line part
    """

    snap_points = []

    source_crs = QgsCoordinateReferenceSystem(4326)
    dest_crs = QgsCoordinateReferenceSystem(3857)

    transform = QgsCoordinateTransform(source_crs, dest_crs, QgsProject.instance())
    transform_back = QgsCoordinateTransform(dest_crs, source_crs, QgsProject.instance())

    polyline = QgsGeometry(polyline_input)
    polyline.transform(transform)

    for point in point_features:
        if type(point) == QgsFeature:
            point = {
                point_feature_id_field: point[point_feature_id_field],
                "geom": point.geometry(),
            }

        if hasattr(point["geom"], "asPoint"):
            geom = point["geom"].asPoint()
        else:
            geom = point["geom"]

        geom = QgsGeometry.fromPointXY(geom)
        geom.transform(transform)
        geom = geom.asPoint()

        closest_seg = polyline.closestSegmentWithContext(geom)
        # get nearest point (related to the point) on the line
        point_on_line = closest_seg[1]
        point_geom_on_line = QgsPoint(point_on_line[0], point_on_line[1])

        # get nr of vertex (at the end of the line where the closest point is
        # found
        end_vertex_nr = closest_seg[2]
        start_vertex_nr = end_vertex_nr - 1

        p1 = polyline.asPolyline()[start_vertex_nr]  # first vertex
        p2 = point_geom_on_line

        distance_on_subline = math.hypot(p2.x() - p1.x(), p2.y() - p1.y())

        snap_points.append(
            (
                start_vertex_nr,
                distance_on_subline,
                point_geom_on_line,
                point[point_feature_id_field],
            )
        )

    # order on vertex nr and if same vertex nr on distance
    snap_points.sort(key=lambda x: x[1])
    snap_points.sort(key=lambda x: x[0])

    # create line parts
    line_parts = []
    line_points = []
    start_point_id = start_node_id
    total_line_distance = 0

    for i, vertex in enumerate(polyline.asPolyline()):
        line_points.append(QgsPoint(vertex[0], vertex[1]))

        # get points after this vertex
        split_points_on_segment = [p for p in snap_points if p[0] == i]
        for point in split_points_on_segment:
            # only add another point if point is not equal to last vertex
            # todo: throw error when at begin or end vertex of original line?
            # todo: what to do of multiple points on same location?
            line_points.append(point[2])
            geom = QgsGeometry.fromPolyline(line_points)

            # length, unit_type = d.convertMeasurement(
            #     d.computeDistance(line_points),
            #     Qgis.Meters, Qgis.Meters, False)  # Qgis.Degrees

            length = geom.length()

            # add line parts
            line_parts.append(
                {
                    "geom": geom.transform(transform_back),
                    "start_point_id": start_point_id,
                    "end_point_id": point[3],
                    "distance_at_line": total_line_distance,
                    "length": length,
                }
            )
            # create starting point of new line
            line_points = [point[2]]
            start_point_id = point[3]
            total_line_distance += length

    # last part of the line
    geom = QgsGeometry.fromPolyline(line_points)
    length = geom.length()
    # length, something = d.convertMeasurement(
    #     d.computeDistance(line_points),
    #     Qgis.Meters, Qgis.Meters, False)

    line_parts.append(
        {
            "geom": geom,
            "start_point_id": start_point_id,
            "end_point_id": end_node_id,
            "distance_at_line": total_line_distance,
            "length": length,
        }
    )

    return line_parts
