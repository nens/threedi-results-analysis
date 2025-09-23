# (c) Nelen & Schuurmans, see LICENSE.rst.

from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsCoordinateTransform
from qgis.core import QgsProject
import numpy as np


def get_coord_transformation_instance(src_epsg, dest_epsg):
    """
    :param src_epsg: epsg code of the source geometry
    :param dest_epsg: epsg code to transform to
    """
    src_crs = QgsCoordinateReferenceSystem(int(src_epsg))
    dest_crs = QgsCoordinateReferenceSystem(int(dest_epsg))
    return QgsCoordinateTransform(src_crs, dest_crs, QgsProject.instance())


def closest_point_on_segment(p, a, b):
    ap = p - a
    ab = b - a
    ab_squared = np.dot(ab, ab)
    # Length ab vector is zero, or: segment is a point
    if ab_squared == 0:
        return a
    # https://en.wikipedia.org/wiki/Scalar_projection
    t = max(min(np.dot(ap, ab) / ab_squared, 1), 0)
    return a + t * ab


def distance_to_polyline(px, py, x_data, y_data):
    # Closest projected point
    min_dist = float('inf')
    # Closest data point
    closest = None
    point = np.array([px, py])
    for i in range(len(x_data) - 1):
        a = np.array([x_data[i], y_data[i]])
        b = np.array([x_data[i+1], y_data[i+1]])
        proj = closest_point_on_segment(point, a, b)
        dist = np.linalg.norm(proj - point)
        if dist < min_dist:
            min_dist = dist
            closest = a if np.linalg.norm(point-a) < np.linalg.norm(point-b) else b
    return min_dist, closest
