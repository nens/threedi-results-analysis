# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import logging
import math
import itertools
import collections

from qgis.core import (
    QgsMapLayerRegistry,
    QgsFeatureRequest,
    QgsFeature,
    QgsGeometry,
    QgsVectorLayer,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem
)
from qgis.core import QgsPoint
from PyQt4.QtCore import QPyNullVariant

from ThreeDiToolbox.utils.user_messages import messagebar_message
from ThreeDiToolbox.views.predict_calc_points_dialog import (
    MoveConnectedPointsDialogWidget)
from ThreeDiToolbox.commands.base.custom_command import (
    CustomCommandBase)
from ThreeDiToolbox.utils.predictions import Predictor
from ThreeDiToolbox.utils import constants
from ThreeDiToolbox.utils import utils

log = logging.getLogger(__name__)


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
        if dist <= 0:
            return
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


class CustomCommand(CustomCommandBase):
    """
    command to that will load and start an edit session for the connected
    point layer and verify the data added to that layer
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.iface = kwargs.get('iface')
        self.ts_datasource = kwargs.get('ts_datasource')
        self.tool_dialog_widget = None
        self.connected_pnt_lyr = None
        self.calc_pnt_lyr = None
        self.levee_lyr = None

    def run(self):
        self.table_name_connected = "v2_connected_pnt"
        self.table_name_calc_pnt = "v2_calculation_point"
        self.table_name_levees = "v2_levee"
        connected_pnt_lyr = QgsMapLayerRegistry.instance().mapLayersByName(
            self.table_name_connected
        )
        calc_pnt_lyr = QgsMapLayerRegistry.instance().mapLayersByName(
            self.table_name_calc_pnt
        )
        levee_lyr = QgsMapLayerRegistry.instance().mapLayersByName(
            self.table_name_levees
        )
        if connected_pnt_lyr:
            self.connected_pnt_lyr = connected_pnt_lyr[0]
        if calc_pnt_lyr:
            self.calc_pnt_lyr = calc_pnt_lyr[0]
        if levee_lyr:
            self.levee_lyr = levee_lyr[0]

        if all([self.connected_pnt_lyr, self.calc_pnt_lyr, self.levee_lyr]):
            msg = 'Auto detected loaded connected_pnt layer!'
            self.show_gui()
            # self.supervising_user_input(msg)
        # else:
        #     rm_list = [
        #         lyr.id() for lyr in (
        #             self.calc_pnt_lyr, self.connected_pnt_lyr
        #         ) if lyr is not None
        #     ]
        #     QgsMapLayerRegistry.instance().removeMapLayers(rm_list)
        #     self.show_gui()

    def show_gui(self):
        self.tool_dialog_widget = MoveConnectedPointsDialogWidget(command=self)
        self.tool_dialog_widget.exec_()  # block execution

    def get_calc_pnts_hash_table(self):
        fnames_calc_pnt = [
            field.name() for field in self.calc_pnt_lyr.pendingFields()
        ]

        calc_pnt_request = QgsFeatureRequest().setFilterExpression(
            '"calc_type" != 1')

        calc_pnts_hash = collections.defaultdict(list)
        calc_pnt_features = self.calc_pnt_lyr.getFeatures(calc_pnt_request)
        for calc_pnt_feature in calc_pnt_features:
            calc_pnt = dict(
                zip(
                    fnames_calc_pnt, calc_pnt_feature.attributes()
                )
            )
            user_ref = calc_pnt['user_ref']
            code, src_id, src_tbl, calc_nr = user_ref.split('#')
            key = '{src_id}{src_table}'.format(src_id=src_id, src_table=src_tbl)
            calc_pnts_hash[key].append(str(calc_pnt['id']))
        return calc_pnts_hash

    def run_it(self, search_distance, distance_to_levee):
        # get data that already has been pre-calculated
        # calculation points
        calc_pnts_hash = self.get_calc_pnts_hash_table()
        print("calc_pnts_hash ", calc_pnts_hash)
        # connected_pnt_iter = self.connected_pnt_lyr.getFeatures()
        # all_points = [feature.geometry().asPoint() for feature in connected_pnt_iter]
        # print("all_points ", all_points)
        # pairwise loop
        # TODO implement
        for values in calc_pnts_hash.values():
            id_str = ','.join(values)
            connected_pnt_request = QgsFeatureRequest().setFilterExpression(
                '"calculation_pnt_id" IN ({ids})'.format(ids=id_str))
            connected_pnt_iter = self.connected_pnt_lyr.getFeatures(connected_pnt_request)
            sel_connected_pnts = [feature.geometry().asPoint() for feature in connected_pnt_iter]
            print("sel_connected_pnts ", sel_connected_pnts)
            self.ppp(sel_connected_pnts, search_distance, distance_to_levee)


    def ppp(self, pnts, search_distance, distance_to_levee):
        v_layer = QgsVectorLayer("Point", "pnt", "memory")
        l_layer = QgsVectorLayer("LineString", "line", "memory")
        pr = v_layer.dataProvider()
        pr_l = l_layer.dataProvider()
        pm = PointMover()

        for xy, xy1 in utils.pairwise(pnts):

            # convert to flat list
            coords = list(itertools.chain(*(xy, xy1)))

            m_pnts = pm.move(coords, distance=search_distance/111325.0)
            if not m_pnts:
                continue
            line_start = QgsPoint(m_pnts[0], m_pnts[1])
            line_end = QgsPoint(m_pnts[2], m_pnts[3])

            org_start = QgsPoint(coords[0], coords[1])
            org_end = QgsPoint(coords[2], coords[3])

            virtual_line = QgsGeometry.fromPolyline([line_start, line_end])
            org_line = QgsGeometry.fromPolyline([org_start, org_end])
            feat = QgsFeature()
            feat.setGeometry(virtual_line)
            feat2 = QgsFeature()
            feat2.setGeometry(org_line)
            pr_l.addFeatures([feat, feat2])

            # virtual_line_bbox = virtual_line.boundingBox()
            # levee_features = self.levee_lyr.getFeatures(
            #     QgsFeatureRequest().setFilterRect(virtual_line_bbox)
            # )
            #
            # for levee in levee_features:
            #     print("levee ", levee.attributes()[0])
            #
            #     if levee.geometry().intersects(virtual_line):
            #         intersection_pnt =  levee.geometry().intersection(virtual_line)
            #         print("intersection ", intersection_pnt)
            #         print("intersection geom", intersection_pnt.geometry())
            #         g = intersection_pnt.geometry()
            #         # print("pnt geom", pnt.x())
            #         # print("pnt geom", pnt.y())
            #         pnt = QgsPoint(g.x(), g.y())
            #         line_from_intersect = QgsGeometry.fromPolyline([pnt, line_end])
            #         moved = line_from_intersect.interpolate(distance_to_levee)
            #         print("---------- ", moved)
            #         print("------ geom ", moved.geometry())
            #         print("------ dir geom ", dir(moved.geometry()))
            #         seg = QgsFeature()
            #         seg.setGeometry(moved)
            #         pr.addFeatures([seg])
            #         # levee_id = levee.attributes()[0]
            #         break
        v_layer.updateExtents()
        # l_layer.updateExtents()
        # show the line
        QgsMapLayerRegistry.instance().addMapLayers([v_layer, l_layer])

    # def run_it(self, search_distance, distance_to_levee):
    #     # get data that already has been pre-calculated
    #     # calculation points
    #     v_layer = QgsVectorLayer("Point", "pnt", "memory")
    #     l_layer = QgsVectorLayer("LineString", "line", "memory")
    #     pr = v_layer.dataProvider()
    #     pr_l = l_layer.dataProvider()
    #     transf = QgsCoordinateTransform(QgsCoordinateReferenceSystem(4326), QgsCoordinateReferenceSystem(int(28992)))
    #     connected_pnt_iter = self.connected_pnt_lyr.getFeatures()
    #     all_points = [transf.transform(feature.geometry().asPoint()) for feature in connected_pnt_iter]
    #     print("all_points ", all_points)
    #     # pairwise loop
    #     # TODO implement
    #     pm = PointMover()
    #     for xy, xy1 in utils.pairwise(all_points):
    #
    #         # convert to flat list
    #         coords = list(itertools.chain(*(xy,xy1)))
    #         # org_pnt = QgsPoint(coords[0], coords[1])
    #
    #         m_pnts = pm.move(coords, distance=search_distance)
    #         if not m_pnts:
    #             continue
    #         line_start = QgsPoint(m_pnts[0], m_pnts[1])
    #         line_end = QgsPoint(m_pnts[2], m_pnts[3])
    #
    #         virtual_line = QgsGeometry.fromPolyline([line_start, line_end])
    #         feat = QgsFeature()
    #         feat.setGeometry(virtual_line)
    #         pr_l.addFeatures([feat])
    #
    #         virtual_line_bbox = virtual_line.boundingBox()
    #         levee_features = self.levee_lyr.getFeatures(
    #             QgsFeatureRequest().setFilterRect(virtual_line_bbox)
    #         )
    #
    #         for levee in levee_features:
    #             print("levee ", levee.attributes()[0])
    #
    #             if levee.geometry().intersects(virtual_line):
    #                 intersection_pnt =  levee.geometry().intersection(virtual_line)
    #                 print("intersection ", intersection_pnt)
    #                 print("intersection geom", intersection_pnt.geometry())
    #                 g = intersection_pnt.geometry()
    #                 # print("pnt geom", pnt.x())
    #                 # print("pnt geom", pnt.y())
    #                 pnt = QgsPoint(g.x(), g.y())
    #                 line_from_intersect = QgsGeometry.fromPolyline([pnt, line_end])
    #                 moved = line_from_intersect.interpolate(distance_to_levee)
    #                 print("---------- ", moved)
    #                 print("------ geom ", moved.geometry())
    #                 print("------ dir geom ", dir(moved.geometry()))
    #                 seg = QgsFeature()
    #                 seg.setGeometry(moved)
    #                 pr.addFeatures([seg])
    #                 # levee_id = levee.attributes()[0]
    #                 break
    #     v_layer.updateExtents()
    #     l_layer.updateExtents()
    #     # show the line
    #     QgsMapLayerRegistry.instance().addMapLayers([v_layer, l_layer])

