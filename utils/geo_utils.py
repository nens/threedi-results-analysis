# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import math


def get_extrapolated_point(starting_pnt, end_pnt, extrapolation_ration=3):
    """
    calculate the extrapolated line of pnt1 -> pnt2

    :param starting_pnt: starting point (x,y)
    :param end_pnt: endpoint (x,y)
    :param extrapolation_ration: ration by which the line will be extended

    :returns the start- and endpoint of the extrapolated line
    """
    extrapolated_point = (
        starting_pnt[0] + extrapolation_ration * (end_pnt[0]-starting_pnt[0]),
        starting_pnt[1] + extrapolation_ration * (end_pnt[1]-starting_pnt[1])
    )
    return extrapolated_point


def calculate_perpendicular_line(line_coords, distance, orientation=None):
    """
    :param line_coords: list of coordinates, e.g [x1, y1, x2, y2]
    :param distance: distance in meters
    :param orientation:
        default None --> considers both sides of the line
        left --> left to drawing direction,
        right --> right to drawing direction
    """
    x1 = line_coords[0]
    y1 = line_coords[1]
    x2 = line_coords[2]
    y2 = line_coords[3]
    # desired length of the perp line
    distance = distance
    # calculate the distance between the xy coordinates
    dx = x1-x2
    dy = y1-y2
    dist = math.sqrt(dx*dx + dy*dy)
    # print("dist ", dist)
    if dist <= 0:
        return
    # the perp line needs to be inbetween those two coords,
    # so half the distance...
    dx /= dist
    dy /= dist
    # ...so this are the coords
    x3 = x1 + (distance * dy)
    y3 = y1 - (distance * dx)
    x4 = x1 - (distance * dy)
    y4 = y1 + (distance * dx)
    # print("new coords ", x3, y3, x4, y4)
    # to the left or to the right?
    if orientation is None:
        return x3, y3, x4, y4
    elif orientation == 'left':
        return x1, y1, x3, y3
    elif orientation == 'right':
        return x1, y1, x4, y4
