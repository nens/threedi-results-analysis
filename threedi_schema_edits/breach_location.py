# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

from builtins import str
from builtins import zip
from builtins import object
import logging
import itertools
import collections

from qgis.core import QgsFeatureRequest
from qgis.core import QgsFeature
from qgis.core import QgsGeometry
from qgis.core import QgsVectorLayer
from qgis.core import QgsPointXY
from qgis.core import QgsField

from qgis.PyQt.QtCore import QVariant

from ThreeDiToolbox.utils.geo_utils import calculate_perpendicular_line
from ThreeDiToolbox.utils.geo_utils import get_distance
from ThreeDiToolbox.utils.geo_utils import get_epsg_code_from_layer
from ThreeDiToolbox.utils.geo_utils import get_extrapolated_point

from ThreeDiToolbox.utils.utils import parse_db_source_info

from ThreeDiToolbox.threedi_schema_edits.predictions import Predictor
from ThreeDiToolbox.utils import constants
from ThreeDiToolbox.utils import utils

logger = logging.getLogger(__name__)

EXTRAPLORATION_RATIO = 20


class BreachLocation(object):
    """
    Class to determine and create possible breach locations. For (selected)
    connected points it finds intersections with levees that are within the
    user defined search distance. It then can move the points across that
    levee. Not only the geometry will be updated but also the levee_id
    attribute. When using the 'is_dry_run' option the database table will
    not yet be updated. Instead a memory layer with the possible locations
    will created.
    """

    def __init__(
        self,
        search_distance,
        distance_to_levee,
        use_selection,
        is_dry_run,
        connected_pnt_lyr,
    ):
        """
        :param search_distance: the distance to search for a levee intersection
        :param distance_to_levee: the distance from the levee to place the
            point at
        :param use_selection: use the selected features
        :param is_dry_run: do not save the outcome of the tool to the DB yet.
            Will produce two memory layers to visualize the results
        :param connected_pnt_lyr: the connected point layer

        """
        # QgsMapLayer.dataProvider()
        self.search_distance = search_distance
        self.distance_to_levee = distance_to_levee
        self.use_selection = use_selection
        self.is_dry_run = is_dry_run

        self.selected_pnt_ids = collections.defaultdict(list)

        self.connected_pnt_lyr = connected_pnt_lyr
        self.fnames_conn_pnt = {
            field.name(): i for i, field in enumerate(self.connected_pnt_lyr.fields())
        }
        if not self.is_dry_run:
            self.connected_pnt_lyr.startEditing()
        source_info = self.connected_pnt_lyr.dataProvider().dataSourceUri()
        source_info_dict = parse_db_source_info(source_info)
        predictor = Predictor(source_info_dict["db_type"])
        uri = predictor.get_uri(**source_info_dict)
        self.calc_pnt_lyr = predictor.get_layer_from_uri(
            uri, constants.TABLE_NAME_CALC_PNT, "the_geom"
        )
        self.levee_lyr = predictor.get_layer_from_uri(
            uri, constants.TABLE_NAME_LEVEE, "the_geom"
        )

        self.epsg_code = get_epsg_code_from_layer(self.connected_pnt_lyr)

        if self.is_dry_run:
            self.create_tmp_layers()
        if self.use_selection:
            self.set_selected_pnt_ids()

        if self.epsg_code == constants.EPSG_WGS84:
            self.search_distance /= constants.DEGREE_IN_METERS
            self.distance_to_levee /= constants.DEGREE_IN_METERS

        # used for user feedback
        self.cnt_moved_pnts = 0

    @property
    def has_valid_selection(self):
        if self.selected_pnt_ids or not self.use_selection:
            return True
        return False

    def set_selected_pnt_ids(self):
        """
        Populates the dict ``self.selected_pnt_ids`` of the selected connected
        and calculation point features.

            {connected point id:
                [calculation point id, ...],
            }
        """
        user_selection = self.connected_pnt_lyr.selectedFeatures()

        for item in user_selection:
            # combine feature with field names
            conn_pnt = dict(zip(item.fields().names(), item.attributes()))
            self.selected_pnt_ids[item.id()].append(conn_pnt["calculation_pnt_id"])

    def get_connected_points(self, ids, calc_type):
        """

        :param ids: a list of connected point ids
        :param calc_type: the calculation type of the calculation point
            the ids relate to

        :returns a dict of lists of tuples with xy's
             {<feature id>: [(<x, y>), (<x, y>),... ],...}
        """
        INDEX_MAP = {
            constants.NODE_CALC_TYPE_CONNECTED: -2,
            constants.NODE_CALC_TYPE_DOUBLE_CONNECTED: -3,
        }
        selected_points = []

        id_str = ",".join([str(x) for x in ids])

        # request object that will filter the connected points by its
        # source object (e.g. all points originating from a specific pipe)
        connected_pnt_request = QgsFeatureRequest().setFilterExpression(
            '"calculation_pnt_id" IN ({ids})'.format(ids=id_str)
        )
        connected_points = self.connected_pnt_lyr.getFeatures(connected_pnt_request)
        selected_connected_pnt_ids = list(self.selected_pnt_ids.keys())
        for feature in connected_points:
            if self.use_selection:
                if feature.id() in selected_connected_pnt_ids:
                    selected_points.append({feature.id(): feature.geometry().asPoint()})
            else:
                selected_points.append({feature.id(): feature.geometry().asPoint()})
        if len(selected_points) < abs(INDEX_MAP[calc_type]):
            return []
        # add a dummy point to be able to draw a line for the
        # last point
        extrapolated_point = get_extrapolated_point(
            list(selected_points[INDEX_MAP[calc_type]].values())[0],
            list(selected_points[-1].values())[0],
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
        fnames_calc_pnt = [field.name() for field in self.calc_pnt_lyr.fields()]

        calc_type_filter = [2, 5]
        # request object to filter the features by
        calc_pnt_request = QgsFeatureRequest().setFilterExpression(
            '"calc_type" = {} OR "calc_type" = {}'.format(*calc_type_filter)
        )
        calc_pnt_features = self.calc_pnt_lyr.getFeatures(calc_pnt_request)
        selected_calc_pnt_ids = list(
            itertools.chain(*list(self.selected_pnt_ids.values()))
        )
        for calc_pnt_feature in calc_pnt_features:
            if any(
                [calc_pnt_feature.id() in selected_calc_pnt_ids, not self.use_selection]
            ):
                # combine feature with field names
                calc_pnt = dict(
                    list(zip(fnames_calc_pnt, calc_pnt_feature.attributes()))
                )
                user_ref = calc_pnt["user_ref"]
                calc_type = calc_pnt["calc_type"]
                code, src_id, src_tbl, calc_nr = user_ref.split("#")
                source_info = "{src_id}{src_table}".format(
                    src_id=src_id, src_table=src_tbl
                )
                calc_points_dict[(source_info, calc_type)].append(calc_pnt["id"])
        return calc_points_dict

    def move_points_behind_levee(self, points, calc_type):
        """
        :param points: a list of tuple containing xy coordinates
        :param calc_type: the the calculation type for the points
        """

        # calc type 2 does not have an orientation, that means the
        # perpendicular line will be drawn to both sides from teh point
        # calc type 5 will first look on the left side of the point,
        # then on the right side
        ORIENTATION_MAP = {
            constants.NODE_CALC_TYPE_CONNECTED: [None],
            constants.NODE_CALC_TYPE_DOUBLE_CONNECTED: ["left", "right"],
        }

        _connected_pnt_ids = None

        # we're looping pairwise to be able to draw a line between
        # the two points. The last point has been extrapolated, hence
        # it is not of interest here
        for start_pnt, nxt_pnt in utils.pairwise(points):

            connected_pnt_ids = list(start_pnt.keys())
            start_pnt_xy = list(start_pnt.values())[0]
            nxt_pnt_xy = list(nxt_pnt.values())[0]
            # skip this iteration, double connected point exists twice
            if start_pnt_xy == nxt_pnt_xy:
                # we do need both ids for updating the geometry
                _connected_pnt_ids = list(
                    itertools.chain(*(list(start_pnt.keys()), list(nxt_pnt.keys())))
                )
                continue

            coords = list(itertools.chain(*(start_pnt_xy, nxt_pnt_xy)))

            new_positions = []
            orientation = ORIENTATION_MAP[calc_type]
            for i, item in enumerate(orientation):
                perpendicular_line = calculate_perpendicular_line(
                    coords, distance=self.search_distance, orientation=item
                )
                if not perpendicular_line:
                    continue
                line_start = QgsPointXY(perpendicular_line[0], perpendicular_line[1])
                line_end = QgsPointXY(perpendicular_line[2], perpendicular_line[3])

                org_start = QgsPointXY(coords[0], coords[1])
                org_end = QgsPointXY(coords[2], coords[3])

                if self.is_dry_run:
                    org_line = QgsGeometry.fromPolylineXY([org_start, org_end])
                    feat = QgsFeature()
                    feat.setGeometry(org_line)
                    self.provider_line.addFeatures([feat])

                levee_intersections = self.find_levee_intersections(
                    line_start, line_end, org_start
                )
                if levee_intersections:
                    new_position, levee_id = self.calculate_new_position(
                        levee_intersections, line_start, line_end, calc_type
                    )
                    new_positions.append((new_position, levee_id))

            if new_positions:
                self.add_to_tmp_connected_point_layer(new_positions)

                # should always be of length 2 if defined
                if _connected_pnt_ids is not None:
                    # new_position can contain just one entry if there
                    # wasn't an intersection on one side
                    to_update = dict(
                        itertools.zip_longest(
                            _connected_pnt_ids, new_positions, fillvalue=(None, None)
                        )
                    )
                else:
                    to_update = dict(list(zip(connected_pnt_ids, new_positions)))

                self.update_connected_point_layer(to_update)
            _connected_pnt_ids = None

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

        levee_field_names = [field.name() for field in self.levee_lyr.fields()]

        virtual_line = QgsGeometry.fromPolylineXY([start_point, end_point])
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
        for levee_feat in levee_features:
            # combine feature with field names
            levee = dict(list(zip(levee_field_names, levee_feat.attributes())))
            levee_id = levee["id"]
            if levee_feat.geometry().intersects(virtual_line):
                intersection_pnt = levee_feat.geometry().intersection(virtual_line)
                intersection_pnt.convertToSingleType()
                g = intersection_pnt.constGet()
                pnt = QgsPointXY(g.x(), g.y())
                dist = get_distance(centroid, pnt, epsg_code=self.epsg_code)
                levee_intersections[levee_id].append((dist, pnt, levee_id))
        return levee_intersections

    def calculate_new_position(
        self, levee_intersections, start_point, end_point, calc_type
    ):
        """
        :param levee_intersections: a dict containing intersections
            key: levee id that intersects
            value:
                tuple of:
                    - distance of levee intersection to centroid,
                    - QgsPoint object of the intersection,
                    - levee id
        :param start_point: start point of the search path
        :param end_point: end point of the search path
        :param calc_type: the calculation type of the underlying
            calculation point
        :returns the point geom of the closest intersection
        """

        # sort by distance
        intersections = sorted(list(levee_intersections.values()), key=lambda x: (x[0]))
        dist, pnt, levee_id = intersections[0][0]

        pnt_to_use = end_point
        if calc_type == constants.NODE_CALC_TYPE_CONNECTED:
            # find out which point is closer to the intersection
            end_pnt_dist = get_distance(pnt, end_point, epsg_code=self.epsg_code)
            start_pnt_dist = get_distance(pnt, start_point, epsg_code=self.epsg_code)
            pnt_dict = {end_pnt_dist: end_point, start_pnt_dist: start_point}
            pnt_to_use = pnt_dict[min(end_pnt_dist, start_pnt_dist)]
        line_from_intersect = QgsGeometry.fromPolylineXY([pnt, pnt_to_use])
        line_length_from_intersect = line_from_intersect.length()

        # elongate the perpendicular line if it is too short to
        # calculate the new position
        if line_length_from_intersect < self.distance_to_levee:
            extrapolated_point = get_extrapolated_point(
                pnt, end_point, EXTRAPLORATION_RATIO
            )
            exp_end_pnt = QgsPointXY(extrapolated_point[0], extrapolated_point[1])
            line_from_intersect = QgsGeometry.fromPolylineXY([pnt, exp_end_pnt])
        new_position = line_from_intersect.interpolate(self.distance_to_levee)
        return new_position, levee_id

    def add_to_tmp_connected_point_layer(self, new_positions):
        """
        add features to the temporary point layer. Adds geometry and
        levee_id of the intersection

        :param new_positions: list of tuples like so
            [(<geometry>, <levee id>), ...]
        """
        if not self.is_dry_run:
            return

        if not isinstance(new_positions, list):
            new_positions = [new_positions]
        new_features = []

        for geom, levee_id in new_positions:
            new_feat = QgsFeature()
            new_feat.setGeometry(geom)
            new_feat.setAttributes([int(levee_id)])
            new_features.append(new_feat)
        succces, features = self.provider_pnt.addFeatures(new_features)
        cnt_feat = len(features)
        if succces:
            logger.info("[*] Successfully added {} features to the layer".format(cnt_feat))
        else:
            logger.error("[-] Could not add features to the layer")

    def update_connected_point_layer(self, to_update):
        """
        update the database table 'v2_connected_pnt'. Adds the levee_id and
        changes the geometry

        :param to_update: dict like so
            {<connection point id>:
                (new geometry, levee id),
             ...
            }
        """
        if self.is_dry_run:
            return
        for conn_pnt_id, (geom, levee_id) in to_update.items():
            if any([geom is None, conn_pnt_id is None]):
                continue
            req = QgsFeatureRequest().setFilterFid(conn_pnt_id)
            feat = next(self.connected_pnt_lyr.getFeatures(req))
            feat["levee_id"] = levee_id
            feat.setGeometry(geom)
            self.connected_pnt_lyr.updateFeature(feat)
            self.cnt_moved_pnts += 1

    def create_tmp_layers(self):
        """
        creates two qgis "memory" layers: "temp_connected_pnt"
        and "temp_connected_line"
        """
        crs = "EPSG:{}".format(self.epsg_code)
        self.pnt_layer = QgsVectorLayer(
            "Point?crs=" + crs, "temp_connected_pnt", "memory"
        )
        self.line_layer = QgsVectorLayer(
            "LineString?crs=" + crs, "temp_connected_line", "memory"
        )
        self.provider_pnt = self.pnt_layer.dataProvider()
        self.pnt_layer.startEditing()
        self.provider_pnt.addAttributes([QgsField("levee_id", QVariant.Int)])
        self.provider_line = self.line_layer.dataProvider()
