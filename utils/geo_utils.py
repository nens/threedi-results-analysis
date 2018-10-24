# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import math

from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsCoordinateTransform
from qgis.core import QgsDistanceArea
from qgis.core import QgsProject

from ThreeDiToolbox.utils import constants


def get_extrapolated_point(starting_pnt, end_pnt, extrapolation_ration=3):
    """
    calculate the extrapolated line of pnt1 -> pnt2

    :param starting_pnt: starting point (x,y)
    :param end_pnt: endpoint (x,y)
    :param extrapolation_ration: ration by which the line will be extended

    :returns the start- and endpoint of the extrapolated line
    """
    extrapolated_point = (
        starting_pnt[0] + extrapolation_ration *
        (end_pnt[0] - starting_pnt[0]),
        starting_pnt[1] + extrapolation_ration * (end_pnt[1] - starting_pnt[1])
    )
    return extrapolated_point


def calculate_perpendicular_line(line_coords, distance, orientation=None):
    """
    calculates a perpendicular line to the line made of line_coords.
    Start point will be the first coordinate pair

    :param line_coords: list of coordinates, e.g [x1, y1, x2, y2]
    :param distance: distance in meters (desired length of the
        perpendicular line)
    :param orientation:
        default None --> considers both sides of the line
        left --> left to drawing direction,
        right --> right to drawing direction

    :returns tuple of start and end points of the perpendicular line
    """
    x1 = line_coords[0]
    y1 = line_coords[1]
    x2 = line_coords[2]
    y2 = line_coords[3]

    # calculate the distance between the xy coordinates
    dx = x1 - x2
    dy = y1 - y2
    dist = math.sqrt(dx * dx + dy * dy)
    if dist == 0:
        return

    # the perp line needs to be inbetween those two coords,
    # so half the distance...
    dx /= dist
    dy /= dist
    x3 = x1 + (distance * dy)
    y3 = y1 - (distance * dx)
    x4 = x1 - (distance * dy)
    y4 = y1 + (distance * dx)

    # to the left or to the right?
    if orientation is None:
        return x3, y3, x4, y4
    elif orientation == 'left':
        return x1, y1, x3, y3
    elif orientation == 'right':
        return x1, y1, x4, y4


def get_epsg_code_from_layer(layer_instance):
    """
    :returns the epsg code or None of the layer does not have a crs defined
    """
    epsg_info = layer_instance.crs().authid()
    try:
        return int(epsg_info.split(':')[1])
    except IndexError:
        pass


def set_layer_crs(layer_instance, epsg_code):
    """
    set the coordinate reference system of the layer to the given epsg code
    """
    qcrs = QgsCoordinateReferenceSystem("EPSG:{}".format(epsg_code))
    layer_instance.setCrs(qcrs)
    return layer_instance


def get_distance(pnt1, pnt2, epsg_code):
    """
    :param pnt1: QgsPoint object
    :param pnt2: QgsPoint object

    :returns the distance between pnt1 and pnt2
    """
    # Create a measure object
    distance = QgsDistanceArea()
    crs = QgsCoordinateReferenceSystem()
    # Sets this CRS by lookup of the given PostGIS SRID in the CRS database.
    crs.createFromSrid(epsg_code)
    context = QgsProject.instance().transformContext()
    distance.setSourceCrs(crs, context)
    if epsg_code == constants.EPSG_WGS84:
        distance.setEllipsoid('WGS84')
    return distance.measureLine(pnt1, pnt2)


def get_coord_transformation_instance(src_epsg, dest_epsg):
    """
    :param src_epsg: epsg code of the source geometry
    :param dest_epsg: epsg code to transform to
    """
    src_crs = QgsCoordinateReferenceSystem(int(src_epsg))
    dest_crs = QgsCoordinateReferenceSystem(int(dest_epsg))
    return QgsCoordinateTransform(src_crs, dest_crs, QgsProject.instance())
