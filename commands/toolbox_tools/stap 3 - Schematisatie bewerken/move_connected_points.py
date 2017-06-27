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
from qgis.core import QgsDistanceArea
from qgis.core import QgsCoordinateReferenceSystem

from PyQt4.QtCore import QPyNullVariant

from ThreeDiToolbox.utils.user_messages import messagebar_message
from ThreeDiToolbox.utils.geo_utils import get_extrapolated_point

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
        self.search_distance = None
        self.distance_to_levee = None

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


        # TODO let the user load the layers
        if all([self.connected_pnt_lyr, self.calc_pnt_lyr, self.levee_lyr]):
            msg = 'Auto detected loaded connected_pnt layer!'
            self.show_gui()

    def show_gui(self):
        self.tool_dialog_widget = MoveConnectedPointsDialogWidget(command=self)
        self.tool_dialog_widget.exec_()  # block execution

    def run_it(self, search_distance, distance_to_levee):
        # get data that already has been pre-calculated
        # calculation points
        # TODO get epsg_code
        epsg_code = 4326

        self.search_distance = search_distance
        self.distance_to_levee = distance_to_levee

        if epsg_code == 4326:
            self.search_distance /= constants.DEGREE_IN_METERS
            self.distance_to_levee /= constants.DEGREE_IN_METERS

        calc_points_dict = self.get_calc_points_by_content()
        print("calc_points_dict ", calc_points_dict)
        i = 1
        for key, values in calc_points_dict.iteritems():
            calc_type = key[1]
            if i == 0:
                i += 1
                continue
            connected_points_selection = self.get_connected_points(
                values, calc_type
            )
            # sel_connected_pnts = [feature.geometry().asPoint() for feature in connected_pnt_iter]
            # extrapolated_line = self.get_extrapolated_line(sel_connected_pnts[-2], sel_connected_pnts[-1])
            # sel_connected_pnts.extend(extrapolated_line)
            print("connected_points_selection ", connected_points_selection)
            self.move_points_behind_levee(connected_points_selection, calc_type)

    def get_connected_points(self, ids, calc_type):
        """

        :param ids: a list of connected point ids
        :param calc_type: the calculation type

        :returns a list of tuples with xy's
             [(<x, y>), (<x, y>),... ]
        """
        # TODO see how we can do this better
        pick_by_calc_type = {
            2: 1,
            5: 2
        }
        selected_points = []

        id_str = ','.join([str(x) for x in ids])

        # request object that will filter the connected points by its
        # source object (e.g. all points originating from a specific pipe)
        connected_pnt_request = QgsFeatureRequest().setFilterExpression(
            '"calculation_pnt_id" IN ({ids})'.format(ids=id_str)
        )
        connected_points = self.connected_pnt_lyr.getFeatures(
            connected_pnt_request
        )
        for i, feature in enumerate(connected_points):
            if i % pick_by_calc_type[calc_type] == 0:
                selected_points.append(feature.geometry().asPoint())

        extrapolated_point = get_extrapolated_point(
            selected_points[-2], selected_points[-1]
        )
        selected_points.extend(
            (extrapolated_point, selected_points[-2])
        )
        return selected_points

    def get_calc_points_by_content(self):
        """
        group the calculation points by the content object the originate from
        :returns a dict like
            {('<source id><source table>', calculation type):
                [<calculation point id>,
                <calculation point id>, ...
                ], ...
            }
        """

        calc_points_dict = collections.defaultdict(list)
        # get the field names for easier lookup
        fnames_calc_pnt = [
            field.name() for field in self.calc_pnt_lyr.pendingFields()
        ]

        # request object to filter the features by
        calc_pnt_request = QgsFeatureRequest().setFilterExpression(
            '"calc_type" = 2 OR "calc_type" = 5')

        # getFeatures returns an iterator
        calc_pnt_features = self.calc_pnt_lyr.getFeatures(calc_pnt_request)
        for calc_pnt_feature in calc_pnt_features:
            # combine feature with field names
            calc_pnt = dict(
                zip(
                    fnames_calc_pnt, calc_pnt_feature.attributes()
                )
            )
            user_ref = calc_pnt['user_ref']
            calc_type = calc_pnt['calc_type']
            code, src_id, src_tbl, calc_nr = user_ref.split('#')
            source_info = '{src_id}{src_table}'.format(
                src_id=src_id, src_table=src_tbl
            )
            calc_points_dict[(source_info, calc_type)].append(
                calc_pnt['id']
            )
        return calc_points_dict

    def move_points_behind_levee(self, points, calc_type):
        """
        Temporarily adds the points as a layer called "pnt"

        :param points: a list of tuple containing xy coordinates
        :param calc_type: the the calculation type for the points
        """
        # --- for testing purposes -------------------------------- #
        v_layer = QgsVectorLayer("Point", "pnt", "memory")
        l_layer = QgsVectorLayer("LineString", "line", "memory")
        self.pr = v_layer.dataProvider()
        self.pr_l = l_layer.dataProvider()
        # ---------------------------------------------------------- #

        # TODO rename
        pm = PointMover()

        # we're looping pairwise to be able to draw a line between
        # the two points. The last point has been extrapolated, hence
        # it is not of interest here
        for start_pnt, nxt_pnt in utils.pairwise(points[:-1]):
            # convert to flat list
            coords = list(itertools.chain(*(start_pnt, nxt_pnt)))

            m_pnts = pm.move(coords, distance=self.search_distance)
            if not m_pnts:
                print("no m_pnts!!")
                continue
            line_start = QgsPoint(m_pnts[0], m_pnts[1])
            line_end = QgsPoint(m_pnts[2], m_pnts[3])

            org_start = QgsPoint(coords[0], coords[1])
            org_end = QgsPoint(coords[2], coords[3])

            # --- for testing purposes -------------------------------- #
            org_line = QgsGeometry.fromPolyline([org_start, org_end])
            feat2 = QgsFeature()
            feat2.setGeometry(org_line)
            self.pr_l.addFeatures([feat2])
            # ---------------------------------------------------------- #

            levee_intersections = self.find_levee_intersections(
                line_start, line_end, org_start
            )
            new_positions = self.calculate_new_positions(
                levee_intersections, calc_type, line_end
            )
            # TODO implementation is temporarily
            self.add_to_connected_point_layer(new_positions)
        v_layer.updateExtents()
        QgsMapLayerRegistry.instance().addMapLayers([v_layer, l_layer])

    def find_levee_intersections(self, start_point, end_point, centroid):
        """

        :param start_point: start point of the line that will be used for
            the intersection calculation
        :param end_point: end point of the line that will be used for
            the intersection calculation
        :param centroid: centroid  of the line that will be used for
            the intersection calculation

        :returns a defaultdict(list)
            key: levee id that intersects
            value:
                tuple of:
                    - distance of levee intersection to centroid,
                    - QgsPoint object of the intersection,
                    - levee id
        """

        virtual_line = QgsGeometry.fromPolyline([start_point, end_point])
        # filter levees by bbox of the virtual line
        virtual_line_bbox = virtual_line.boundingBox()
        levee_features = self.levee_lyr.getFeatures(
            QgsFeatureRequest().setFilterRect(virtual_line_bbox)
        )

        # --- for testing purposes -------------------------------- #
        feat = QgsFeature()
        feat.setGeometry(virtual_line)
        self.pr_l.addFeatures([feat])
        # ---------------------------------------------------------- #

        # before we move the points get all matches because
        # they need to be sorted first (we want the closest
        # intersection)
        levee_intersections = collections.defaultdict(list)
        for levee in levee_features:
            levee_id = levee.attributes()[4]
            print("levee ", levee_id)
            if levee.geometry().intersects(virtual_line):
                intersection_pnt = levee.geometry().intersection(virtual_line)
                print("intersection ", intersection_pnt)
                print("intersection geom", intersection_pnt.geometry())
                g = intersection_pnt.geometry()
                pnt = QgsPoint(g.x(), g.y())
                dist = self.get_distance(centroid, pnt)
                print('---! dist ', dist)
                levee_intersections[levee_id].append((dist, pnt, levee_id))

        return levee_intersections

    def calculate_new_positions(self, levee_intersections, calc_type, end_point):
        """

        :param levee_intersections: a dict containing intersections
            key: levee id that intersects
            value:
                tuple of:
                    - distance of levee intersection to centroid,
                    - QgsPoint object of the intersection,
                    - levee id

        :param calc_type: calculation type of the points
        :param end_point: end point of the search path
        :return:
        """
        new_positions = []
        # start and end slices for calc type 2 and 5
        SLICE_MAP = {
            constants.NODE_CALC_TYPE_CONNECTED: {
                'start': 0,
                'end': 1
            },
            constants.NODE_CALC_TYPE_DOUBLE_CONNECTED: {
                'start': 0,
                'end': 2
            },
        }

        # sort by distance
        match = sorted(levee_intersections.values(), key=lambda x: (x[0]))
        print("************* matches.values() ", levee_intersections.values())

        print("&&&&&&&&&&&&&&&&&&&&&&& match ", match)
        start_pos = SLICE_MAP[calc_type]['start']
        end_pos = SLICE_MAP[calc_type]['end']
        for m in match[start_pos:end_pos]:
            dist, pnt, levee_id = m[0]
            print('--------------- dist, pnt, levee_id', dist, pnt, levee_id)
            line_from_intersect = QgsGeometry.fromPolyline([pnt, end_point])
            print("levee_id ", levee_id)
            new_position = line_from_intersect.interpolate(self.distance_to_levee)
            new_positions.append(new_position)
        return new_positions

    def add_to_connected_point_layer(self, geoms):
        # TODO update the original layer
        if not isinstance(geoms, (list, tuple)):
            geoms = [geoms]
        new_features = []
        for geom in geoms:
            new_feat = QgsFeature()
            new_feat.setGeometry(geom)
            new_features.append(new_feat)

        # --- for testing purposes -------------------------------- #
        self.pr.addFeatures(new_features)

    @staticmethod
    def get_distance(pnt1, pnt2):
        """
        :param pnt1: QgsPoint object
        :param pnt2: QgsPoint object

        :returns the distance between pnt1 and pnt2 in meters
        """
        # Create a measure object
        distance = QgsDistanceArea()
        crs = QgsCoordinateReferenceSystem()
        # TODO make srid dynamic
        crs.createFromSrsId(3452)  # EPSG:4326
        distance.setSourceCrs(crs)
        distance.setEllipsoidalMode(True)
        distance.setEllipsoid('WGS84')
        m = distance.measureLine(pnt1, pnt2) # ~322.48m.
        return m
