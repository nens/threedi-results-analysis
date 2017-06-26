'''
class perplines
Author: L. Claussen
Waternet, 2012

Version 1.0

Calculates on given coordinates of a start- and endpoint of a line the start- and endpoints of a perpendicular line.
The coordinates are retrieved by the method GetXY which loops through fields of a shape to get the stored xy data. This might
also be implemented differently, for example by accessing the coord by .gp methods like
feat = row.GetValue(FieldnameGeo_in)
pnt = feat.GetPart()
pnt.x, pnt.y

to do's:

* add fields to newly created shape
* populate those fields (needs new method)
* review code,
'''
import logging


import math

from PyQt4.QtCore import QVariant


logger = logging.getLogger(__name__)


class PointMover(object):
    """
    """
    def __init__(self):
        pass
    def move(self, line_coords, distance, orientation=None):
        """
        :param line_coords: list of coordinates, e.g [x1, y1, x2, y2]
        :param distance: distance in meters
        :param orientation:
            default None --> considers both sides of the line
            left --> left to drawing direction,
            right --> right to drawing direction
        """
        self.x1 = line_coords[0]
        self.y1 = line_coords[1]
        self.x2 = line_coords[2]
        self.y2 = line_coords[3]
        # desired length of the perp line
        self.distance = distance
        # calculate the distance between the xy coordinates
        dx = self.x1-self.x2
        dy = self.y1-self.y2
        dist = math.sqrt(dx*dx + dy*dy)
        print("dist ", dist)
        # the perp line needs to be inbetween those two coords,
        # so half the distance...
        dx /= dist
        dy /= dist
        # ...so this are the coords
        self.x3 = self.x1 + (self.distance * dy)
        self.y3 = self.y1 - (self.distance * dx)
        self.x4 = self.x1 - (self.distance * dy)
        self.y4 = self.y1 + (self.distance * dx)
        print("new coords ", self.x3, self.y3, self.x4, self.y4)
        # to the left or to the right?
        if orientation is None:
            return self.x3, self.y3, self.x4, self.y4
        elif orientation == 'left':
            return self.x1, self.y1, self.x3, self.y3
        elif orientation == 'right':
            return self.x1, self.y1, self.x4, self.y4


# first tests
import math
from PyQt4.QtCore import QVariant
pm = PointMover()
lines = []
channel_line = [50, 50, 100, 150]
channel_line1 = [100, 150, 100, 300]
n_lines = [pm.move(l, distance=15, orientation='left') for l in [channel_line, channel_line1]]
lines.append(channel_line)
lines.append(channel_line1)
lines.extend(n_lines)
# create layer
v_layer = QgsVectorLayer("LineString", "line", "memory")
pr = v_layer.dataProvider()
# add fields
# pr.addAttributes([QgsField("tmp_id",  QVariant.Int),])
# v_layer.updateFields() # tell the vector layer to fetch changes from the provider
for item in lines:
    line_start = QgsPoint(item[0], item[1])
    line_end = QgsPoint(item[2], item[3])
    line = QgsGeometry.fromPolyline([line_start,line_end])
    seg = QgsFeature()
    # add the geometry to the feature,
    seg.setGeometry(QgsGeometry.fromPolyline([line_start, line_end]))
    # ...it was here that you can add attributes, after having defined....
    # add the geometry to the layer
    pr.addFeatures([seg])
# update extent of the layer (not necessary)
v_layer.updateExtents()
# show the line
QgsMapLayerRegistry.instance().addMapLayers([v_layer])



# pseudo tool


## user input
search_distance = 30  # will be distance
distance_to_levee = 5
pm = PointMover()


# get data that already has been pre-calculated
# calculation points
all_points = []
# pairwise loop
# TODO implement
for xy, xy1 in pairwise(all_points):
    m_pnts = pm.move([xy, xy1], distance=search_distance)
    line_start = QgsPoint(m_pnts[0], m_pnts[1])
    line_end = QgsPoint(m_pnts[2], m_pnts[3])

    virtual_line = QgsGeometry.fromPolyline([line_start, line_end])

    virtual_line_bbox = virtual_line.boundingBox()
    levee_features = levee_lyr.getFeatures(
        QgsFeatureRequest().setFilterRect(virtual_line_bbox)
    )

    for levee in levee_features:
        if levee.geometry().intersects(virtual_line):
            intersection_pnt =  levee.geometry().intersection(virtual_line)
            line_from_intersect = QgsGeometry.fromPolyline([intersection_pnt, line_end])
            moved = line_from_intersect.interpolate(distance_to_levee)
            # levee_id = levee.attributes()[0]
            break





