# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import logging
import itertools
import collections

from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsFeatureRequest
from qgis.core import QgsFeature
from qgis.core import QgsGeometry
from qgis.core import QgsVectorLayer
from qgis.core import QgsCoordinateTransform
from qgis.core import QgsCoordinateReferenceSystem

from qgis.core import QgsPoint
from qgis.core import QgsDistanceArea
from qgis.core import QgsCoordinateReferenceSystem

from PyQt4.QtCore import QPyNullVariant

from ThreeDiToolbox.utils.user_messages import messagebar_message
from ThreeDiToolbox.utils.geo_utils import get_extrapolated_point
from ThreeDiToolbox.utils.geo_utils import calculate_perpendicular_line

from ThreeDiToolbox.utils.progress import progress_bar

from ThreeDiToolbox.views.predict_calc_points_dialog import (
    MoveConnectedPointsDialogWidget)
from ThreeDiToolbox.commands.base.custom_command import (
    CustomCommandBase)
from ThreeDiToolbox.utils.predictions import Predictor
from ThreeDiToolbox.utils import constants
from ThreeDiToolbox.utils import utils

log = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):
    """
    Move connected points across the nearest levee.
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
        self.selected_pnt_ids = collections.defaultdict(list)

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

    def set_selected_pnt_ids(self):

        user_selection = self.connected_pnt_lyr.selectedFeatures()

        fnames_conn_pnt = [
            field.name() for field in self.connected_pnt_lyr.pendingFields()
        ]

        for item in user_selection:
            # combine feature with field names
            conn_pnt = dict(
                zip(
                    fnames_conn_pnt, item.attributes()
                )
            )
            self.selected_pnt_ids[item.id()].append(
                conn_pnt['calculation_pnt_id']
            )
        print("self.selected_pnt_ids -----", self.selected_pnt_ids)

    def run_it(self, search_distance, distance_to_levee, use_selection,
               is_dry_run):
        # get data that already has been pre-calculated
        # calculation points
        # TODO get epsg_code
        epsg_code = 4326

        self.search_distance = search_distance
        self.distance_to_levee = distance_to_levee
        self.use_selection = use_selection
        self.is_dry_run = is_dry_run

        if self.is_dry_run:
            self.create_tmp_layers()
        if self.use_selection:
            self.set_selected_pnt_ids()

        if epsg_code == 4326:
            self.search_distance /= constants.DEGREE_IN_METERS
            self.distance_to_levee /= constants.DEGREE_IN_METERS

        calc_points_dict = self.get_calc_points_by_content()
        print("calc_points_dict ---", calc_points_dict)

        cnt_iterations = len(calc_points_dict)
        cnt = 1
        with progress_bar(self.iface) as pb:
            for key, values in calc_points_dict.iteritems():
                calc_type = key[1]
                connected_points_selection = self.get_connected_points(
                    values, calc_type
                )
                self.move_points_behind_levee(
                    connected_points_selection, calc_type
                )
                current = (cnt/float(cnt_iterations)) * 100
                pb.setValue(current)
                cnt += 1

        self.connected_pnt_lyr.updateExtents()
        self.iface.mapCanvas().refresh()
        self.connected_pnt_lyr.triggerRepaint()

    def get_connected_points(self, ids, calc_type):
        """

        :param ids: a list of connected point ids

        :returns a dict of lists of tuples with xy's
             {<feature id>: [(<x, y>), (<x, y>),... ],...}
        """
        INDEX_MAP = {
            constants.NODE_CALC_TYPE_CONNECTED: -2,
            constants.NODE_CALC_TYPE_DOUBLE_CONNECTED: -3
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
        selected_connected_pnt_ids = self.selected_pnt_ids.keys()
        for feature in connected_points:
            if self.use_selection:
                if feature.id() in selected_connected_pnt_ids:
                    selected_points.append(
                        {feature.id(): feature.geometry().asPoint()}
                    )
            else:
                selected_points.append(
                    {feature.id(): feature.geometry().asPoint()}
                )
        if len(selected_points) < abs(INDEX_MAP[calc_type]):
            return []
        # add a dummy point to be able to draw a line for the
        # last point
        extrapolated_point = get_extrapolated_point(
            selected_points[INDEX_MAP[calc_type]].values()[0],  # xy tuple
            selected_points[-1].values()[0],                    # xy tuple
        )
        selected_points.append({None: extrapolated_point})
        return selected_points

    def get_calc_points_by_content(self):
        """
        group the calculation points by the content object they
        originate from

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

        calc_type_filter = [2, 5]
        # request object to filter the features by
        calc_pnt_request = QgsFeatureRequest().setFilterExpression(
            '"calc_type" = {} OR "calc_type" = {}'.format(*calc_type_filter)
        )
        calc_pnt_features = self.calc_pnt_lyr.getFeatures(calc_pnt_request)
        selected_calc_pnt_ids = list(itertools.chain(*self.selected_pnt_ids.values()))
        for calc_pnt_feature in calc_pnt_features:
            if any([calc_pnt_feature.id() in selected_calc_pnt_ids,
                    not self.use_selection]):
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

        # calc type 2 does not have an orientation, that means the
        # perpendicular line will be drawn to both sides from teh point
        # calc type 5 will first look on the left side of the point,
        # then on the right side
        ORIENTATION_MAP = {
            constants.NODE_CALC_TYPE_CONNECTED:
                [None],
            constants.NODE_CALC_TYPE_DOUBLE_CONNECTED:
                ['left', 'right']
        }

        _connected_pnt_ids = None

        # we're looping pairwise to be able to draw a line between
        # the two points. The last point has been extrapolated, hence
        # it is not of interest here
        for start_pnt, nxt_pnt in utils.pairwise(points):

            connected_pnt_ids = start_pnt.keys()
            start_pnt_xy = start_pnt.values()[0]
            nxt_pnt_xy = nxt_pnt.values()[0]
            # skip this iteration, double connected point exists twice
            if start_pnt_xy == nxt_pnt_xy:
                # we do need both ids for updating the geometry
                _connected_pnt_ids = list(
                    itertools.chain(
                        *(start_pnt.keys(), nxt_pnt.keys())
                    )
                )
                continue

            coords = list(
                itertools.chain(
                    *(start_pnt_xy, nxt_pnt_xy)
                )
            )

            new_positions = []
            orientation = ORIENTATION_MAP[calc_type]
            for i, item in enumerate(orientation):
                perpendicular_line = calculate_perpendicular_line(
                    coords, distance=self.search_distance,
                    orientation=item
                )
                if not perpendicular_line:
                    continue
                line_start = QgsPoint(
                    perpendicular_line[0], perpendicular_line[1]
                )
                line_end = QgsPoint(
                    perpendicular_line[2], perpendicular_line[3]
                )

                org_start = QgsPoint(coords[0], coords[1])
                org_end = QgsPoint(coords[2], coords[3])

                if self.is_dry_run:
                    org_line = QgsGeometry.fromPolyline([org_start, org_end])
                    feat = QgsFeature()
                    feat.setGeometry(org_line)
                    self.provider_line.addFeatures([feat])

                levee_intersections = self.find_levee_intersections(
                    line_start, line_end, org_start
                )
                if levee_intersections:
                    new_position = self.calculate_new_position(
                        levee_intersections, line_start, line_end, calc_type
                    )
                    new_positions.append(new_position)

            if new_positions:
                self.add_to_tmp_connected_point_layer(new_positions)

                # should always be of length 2 if defined
                if _connected_pnt_ids is not None:
                    # new_position can contain just one entry if there
                    # wasn't an intersection on one side
                    to_update = dict(itertools.izip_longest(
                        _connected_pnt_ids, new_positions)
                    )
                else:
                    to_update = dict(zip(connected_pnt_ids, new_positions))

                self.update_connected_point_layer(to_update)
            _connected_pnt_ids = None

        if self.is_dry_run:
            self.pnt_layer.updateExtents()
            self.line_layer.updateExtents()
            QgsMapLayerRegistry.instance().addMapLayers(
                [self.pnt_layer, self.line_layer]
            )

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

        if self.is_dry_run:
            feat = QgsFeature()
            feat.setGeometry(virtual_line)
            self.provider_line.addFeatures([feat])

        # before we move the points get all matches because
        # they need to be sorted first (we want the closest
        # intersection)
        levee_intersections = collections.defaultdict(list)
        for levee in levee_features:
            levee_id = levee.attributes()[4]
            if levee.geometry().intersects(virtual_line):
                intersection_pnt = levee.geometry().intersection(virtual_line)
                intersection_pnt.convertToSingleType()
                g = intersection_pnt.geometry()
                pnt = QgsPoint(g.x(), g.y())
                dist = self.get_distance(centroid, pnt)
                levee_intersections[levee_id].append((dist, pnt, levee_id))
        return levee_intersections

    def calculate_new_position(self, levee_intersections, start_point, end_point, calc_type):
        """

        :param levee_intersections: a dict containing intersections
            key: levee id that intersects
            value:
                tuple of:
                    - distance of levee intersection to centroid,
                    - QgsPoint object of the intersection,
                    - levee id

        :param end_point: end point of the search path
        :returns the point geom of the closest intersection
        """

        # sort by distance
        intersections = sorted(levee_intersections.values(), key=lambda x: (x[0]))
        dist, pnt, levee_id = intersections[0][0]

        pnt_to_use = end_point
        if calc_type == constants.NODE_CALC_TYPE_CONNECTED:
            # find out which point is closer to the intersection
            end_pnt_dist = self.get_distance(pnt, end_point)
            start_pnt_dist = self.get_distance(pnt, start_point)
            pnt_dict = {
                end_pnt_dist: end_point,
                start_pnt_dist: start_point
            }
            pnt_to_use = pnt_dict[
                min(end_pnt_dist, start_pnt_dist)
            ]
        line_from_intersect = QgsGeometry.fromPolyline([pnt, pnt_to_use])
        line_length_from_intersect = line_from_intersect.length()

        if line_length_from_intersect < self.distance_to_levee:
            extrapolated_point = get_extrapolated_point(pnt, end_point)
            exp_end_pnt = QgsPoint(
                extrapolated_point[0], extrapolated_point[1]
            )
            line_from_intersect = QgsGeometry.fromPolyline([pnt, exp_end_pnt])
        new_position = line_from_intersect.interpolate(self.distance_to_levee)
        return new_position

    def add_to_tmp_connected_point_layer(self, geoms):
        if not self.is_dry_run:
            return

        if not isinstance(geoms, (list, tuple)):
            geoms = [geoms]
        new_features = []
        for geom in geoms:
            new_feat = QgsFeature()
            new_feat.setGeometry(geom)
            new_features.append(new_feat)

        self.provider_pnt.addFeatures(new_features)

    def update_connected_point_layer(self, to_update):

        if self.is_dry_run:
            return

        for conn_pnt_id, geom in to_update.iteritems():
            # req = QgsFeatureRequest().setFilterFid(conn_pnt_id)
            # self.connected_pnt_lyr.getFeatures(req)
            if any([geom is None, conn_pnt_id is None]):
                continue
            self.connected_pnt_lyr.dataProvider().changeGeometryValues(
                {conn_pnt_id: geom}
            )

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

    def create_tmp_layers(self):
        self.pnt_layer = QgsVectorLayer(
            "Point", "temp_connected_pnt", "memory"
        )
        self.line_layer = QgsVectorLayer(
            "LineString", "temp_connected_line", "memory"
        )
        self.provider_pnt = self.pnt_layer.dataProvider()
        self.provider_line = self.line_layer.dataProvider()
