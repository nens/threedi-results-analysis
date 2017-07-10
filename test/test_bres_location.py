"""
Test geo utils.
"""
import unittest
import os
import collections

from qgis.core import QgsFeatureRequest
from qgis.core import QgsPoint

from ThreeDiToolbox.threedi_schema_edits.bres_location import BresLocation
from ThreeDiToolbox.threedi_schema_edits.bres_location import Predictor
from ThreeDiToolbox.utils import constants


from ThreeDiToolbox.utils.geo_utils import get_epsg_code_from_layer
from ThreeDiToolbox.utils.geo_utils import set_layer_crs
from ThreeDiToolbox.utils.geo_utils import calculate_perpendicular_line
from ThreeDiToolbox.utils.geo_utils import get_distance


class TestBresLocationDryRun(unittest.TestCase):

    def setUp(self):

        # os.path.abspath(__file__)
        here = os.path.split(os.path.abspath(__file__))[0]
        test_db = os.path.join(here, 'data', 'simple_bres_test.sqlite')
        db_kwargs = {
            'database': test_db,
            'host': test_db,
            'db_path': test_db,
            'password': '',
            'port': '',
            'srid': '',
            'table_name': 'v2_connected_pnt',
            'schema': '',
            'type': '',
            'username': '',
            'db_type': 'spatialite',
        }
        self.predictor = Predictor(db_kwargs['db_type'])
        self.predictor.start_sqalchemy_engine(db_kwargs)
        self.uri = self.predictor.get_uri(**db_kwargs)
        self.conn_pnt_lyr = self.predictor.get_layer_from_uri(
            self.uri, constants.TABLE_NAME_CONN_PNT, 'the_geom')
        set_layer_crs(self.conn_pnt_lyr, '4326')
        search_distance = 20
        distance_to_levee = 5
        use_selection = False
        is_dry_run = True
        self.bres_location = BresLocation(
            search_distance=search_distance,
            distance_to_levee=distance_to_levee,
            use_selection=use_selection,
            is_dry_run=is_dry_run,
            connected_pnt_lyr=self.conn_pnt_lyr
        )

    # def tearDown(self):
    #
    #     self.predictor.threedi_db.delete_from(constants.TABLE_NAME_CALC_PNT)
    #     self.predictor.threedi_db.delete_from(constants.TABLE_NAME_CONN_PNT)
    #
    #     self.predictor.build_calc_type_dict(epsg_code='4326')
    #     transform = '{epsg_code}:4326'.format(epsg_code='4326')
    #     calc_pnt_lyr = self.predictor.get_layer_from_uri(
    #         self.uri, constants.TABLE_NAME_CALC_PNT, 'the_geom')
    #     self.predictor.predict_points(
    #         output_layer=calc_pnt_lyr, transform=transform)
    #
    #     self.predictor.fill_connected_pnts_table(
    #         calc_pnts_lyr=calc_pnt_lyr,
    #         connected_pnts_lyr=self.conn_pnt_lyr)

    def test_has_valid_selection(self):
        self.assertTrue(self.bres_location.has_valid_selection)

    def test_it_can_get_calc_points_by_content(self):
        # we expect a pipe of calc type 2 and of calc type 5
        expected_keys = [('1v2_pipe', 2), ('4v2_pipe', 5)]
        expected_calc_point_ids = [
            [2L, 3L, 4L, 5L, 6L, 7L, 8L],  # belongs to pipe 1
            [26L, 27L, 28L, 29L, 30L, 31L, 32L]  # belongs to pipe 4
        ]
        calc_points_dict = self.bres_location.get_calc_points_by_content()
        self.assertListEqual(calc_points_dict.keys(), expected_keys)
        self.assertListEqual(
            calc_points_dict.values(), expected_calc_point_ids
        )

    def test_it_can_get_connected_points(self):
        # let's get the connected points for pipe 1
        connected_points_selection = self.bres_location.get_connected_points(
            [2L, 3L, 4L, 5L, 6L, 7L, 8L],  # ids of the calculation points
            calc_type=2
        )
        expected_connected_points = [
            {1L: (3.31369, 47.9748)},
            {2L: (3.31376, 47.9748)},
            {3L: (3.31382, 47.9748)},
            {4L: (3.31389, 47.9748)},
            {5L: (3.31396, 47.9748)},
            {6L: (3.31402, 47.9748)},
            {7L: (3.31409, 47.9748)},
            # extrapolated point, does not have an id
            {None: (3.3142242860395994, 47.974823241109604)}
        ]
        self.assertListEqual(
            expected_connected_points[0].keys(),
            connected_points_selection[0].keys()
        )

    def test_it_wont_move_points_behind_levee(self):
        connected_points_selection = self.bres_location.get_connected_points(
            [2L, 3L, 4L, 5L, 6L, 7L, 8L],  # ids of the calculation points
            calc_type=2
        )
        self.bres_location.move_points_behind_levee(
            connected_points_selection, calc_type=2
        )
        req = QgsFeatureRequest().setFilterExpression(
            '"levee_id" = 3'
        )
        f_iter = self.conn_pnt_lyr.getFeatures(req)
        levee_ids = [f['levee_id'] for f in f_iter]
        self.assertEqual(len(levee_ids), 0)

    def test_it_can_create_tmp_layers(self):
        # we are in dry run mode so the temp layers shoul have been created
        # already on init
        self.assertTrue(hasattr(self.bres_location, "pnt_layer"))
        self.assertTrue(hasattr(self.bres_location, "line_layer"))

    def test_we_can_add_to_tmp_connected_point_layer(self):
        connected_points_selection = self.bres_location.get_connected_points(
            [2L, 3L, 4L, 5L, 6L, 7L, 8L],  # ids of the calculation points
            calc_type=2
        )
        self.bres_location.move_points_behind_levee(
            connected_points_selection, calc_type=2
        )
        self.bres_location.pnt_layer.commitChanges()
        self.bres_location.pnt_layer.updateExtents()

        req = QgsFeatureRequest().setFilterExpression(
            '"levee_id" = 3'
        )
        f_iter = self.bres_location.pnt_layer.getFeatures(req)
        levee_ids = [f['levee_id'] for f in f_iter]
        self.assertEqual(len(levee_ids), 7)
        self.assertTrue(all([x == 3 for x in levee_ids]))

    def test_we_can_add_double_connected_points_to_layer(self):
        connected_points_selection = self.bres_location.get_connected_points(
            [26L, 27L, 28L, 29L, 30L, 31L, 32L],  # ids of calculation points
            calc_type=5  # double connected
        )
        self.bres_location.move_points_behind_levee(
            connected_points_selection, calc_type=5
        )
        self.bres_location.pnt_layer.commitChanges()
        self.bres_location.pnt_layer.updateExtents()

        req = QgsFeatureRequest().setFilterExpression(
            '"levee_id" IN (4,5)'
        )
        f_iter = self.bres_location.pnt_layer.getFeatures(req)
        levee_ids = [f['levee_id'] for f in f_iter]
        self.assertEqual(len(levee_ids), 14)
        self.assertTrue(all([x in (4, 5) for x in levee_ids]))

    def test_it_can_set_selected_pnt_ids(self):
        expected = {
            1: [2],
            2: [3],
            3: [4],
            4: [5],
            5: [6],
            6: [7],
            7: [8]
        }
        self.bres_location.connected_pnt_lyr.setSelectedFeatures(
            [1, 2, 3, 4, 5, 6, 7]
        )
        self.bres_location.set_selected_pnt_ids()
        self.assertDictEqual(expected, self.bres_location.selected_pnt_ids)

    def test_it_can_find_levee_intersections(self):

        perp_line = calculate_perpendicular_line(
            [3.31369, 47.9748, 3.31376, 47.9748],
            distance=self.bres_location.search_distance,
        )
        org_start = QgsPoint(3.31369, 47.9748)

        line_start = QgsPoint(
            perp_line[0], perp_line[1]
        )
        line_end = QgsPoint(
            perp_line[2], perp_line[3]
        )
        # line_start, line_end, org_start
        levee_intersections = self.bres_location.find_levee_intersections(
            line_start, line_end, org_start)

        # should find two intersection
        self.assertEqual(len(levee_intersections), 2)

        # one with levee 2, another with levee 3
        self.assertListEqual(levee_intersections.keys(), [2, 3])

    def test_it_can_calculate_new_positions(self):
        perp_line = calculate_perpendicular_line(
            [3.31369, 47.9748, 3.31376, 47.9748],
            distance=self.bres_location.search_distance,
        )

        line_start = QgsPoint(
            perp_line[0], perp_line[1]
        )
        line_end = QgsPoint(
            perp_line[2], perp_line[3]
        )
        levee_intersections = collections.defaultdict()
        levee_intersections[2] = [(12., QgsPoint(3.31369,47.9747), 2)]
        levee_intersections[3] = [(3., QgsPoint(3.31369,47.9748), 3)]
        new_position, levee_id = self.bres_location.calculate_new_position(
            levee_intersections, line_start, line_end, 2
        )
        self.assertEqual(levee_id, 3)

    def test_it_can_elongate_perpendicular_line(self):
        perp_line = calculate_perpendicular_line(
            [3.31369, 47.9748, 3.31376, 47.9748],
            distance=self.bres_location.search_distance,
        )

        line_start = QgsPoint(
            perp_line[0], perp_line[1]
        )
        line_end = QgsPoint(
            perp_line[2], perp_line[3]
        )
        levee_intersections = collections.defaultdict()
        levee_intersections[2] = [(12., QgsPoint(3.31369,47.9747), 2)]
        levee_intersections[3] = [(3., QgsPoint(3.31369,47.9748), 3)]
        new_position, _ = self.bres_location.calculate_new_position(
            levee_intersections, line_start, line_end, 2
        )
        xy = new_position.geometry().x(), new_position.geometry().y()

        # set the distance to levee attribute to a high number
        self.bres_location.distance_to_levee = 20
        new_position2, _ = self.bres_location.calculate_new_position(
            levee_intersections, line_start, line_end, 2
        )
        xy2 = new_position2.geometry().x(), new_position2.geometry().y()
        self.assertNotEqual(xy, xy2)


class TestBresLocation(unittest.TestCase):

    def setUp(self):

        # os.path.abspath(__file__)
        here = os.path.split(os.path.abspath(__file__))[0]
        test_db = os.path.join(here, 'data', 'simple_bres_test.sqlite')
        db_kwargs = {
            'database': test_db,
            'host': test_db,
            'db_path': test_db,
            'password': '',
            'port': '',
            'srid': '',
            'table_name': 'v2_connected_pnt',
            'schema': '',
            'type': '',
            'username': '',
            'db_type': 'spatialite',
        }
        self.predictor = Predictor(db_kwargs['db_type'])
        self.predictor.start_sqalchemy_engine(db_kwargs)
        self.uri = self.predictor.get_uri(**db_kwargs)
        self.conn_pnt_lyr = self.predictor.get_layer_from_uri(
            self.uri, constants.TABLE_NAME_CONN_PNT, 'the_geom')
        set_layer_crs(self.conn_pnt_lyr, '4326')
        search_distance = 20
        distance_to_levee = 5
        use_selection = False
        is_dry_run = False
        self.bres_location = BresLocation(
            search_distance=search_distance,
            distance_to_levee=distance_to_levee,
            use_selection=use_selection,
            is_dry_run=is_dry_run,
            connected_pnt_lyr=self.conn_pnt_lyr
        )

    def test_it_can_move_points_behind_levee(self):
        connected_points_selection = self.bres_location.get_connected_points(
            [2L, 3L, 4L, 5L, 6L, 7L, 8L],  # ids of the calculation points
            calc_type=2
        )
        self.bres_location.move_points_behind_levee(
            connected_points_selection, calc_type=2
        )
        req = QgsFeatureRequest().setFilterExpression(
            '"levee_id" = 3'
        )
        f_iter = self.conn_pnt_lyr.getFeatures(req)
        # should all have been moved across the first levee (id 3)
        levee_ids = [f['levee_id'] for f in f_iter]
        self.assertEqual(len(levee_ids), 7)
        self.assertTrue(all([x == 3 for x in levee_ids]))
