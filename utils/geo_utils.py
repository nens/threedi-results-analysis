# -*- coding: utf-8 -*-


def get_extrapolated_point(self, starting_pnt, end_pnt, extrapolation_ration=3):
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
