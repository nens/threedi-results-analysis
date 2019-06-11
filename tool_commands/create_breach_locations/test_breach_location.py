"""
Test breach locations.
"""
from qgis._core import QgsPointXY
from qgis._core import QgsVectorLayer
from qgis.core import QgsFeatureRequest
from qgis.core import QgsPointXY
from ThreeDiToolbox.test.test_init import TEST_DATA_DIR
from ThreeDiToolbox.test.utilities import ensure_qgis_app_is_initialized
from ThreeDiToolbox.tool_commands.create_breach_locations.breach_location import (
    BreachLocation,
)
from ThreeDiToolbox.tool_commands.create_breach_locations.breach_location_utils import (
    calculate_perpendicular_line,
)
from ThreeDiToolbox.tool_commands.create_breach_locations.breach_location_utils import (
    get_distance,
)
from ThreeDiToolbox.tool_commands.create_breach_locations.breach_location_utils import (
    get_epsg_code_from_layer,
)
from ThreeDiToolbox.tool_commands.create_breach_locations.breach_location_utils import (
    set_layer_crs,
)
from ThreeDiToolbox.utils import constants
from ThreeDiToolbox.utils.predictions import Predictor

import collections
import os
import shutil
import tempfile
import unittest


class TestBreachLocationDryRun(unittest.TestCase):
    """
    Tests all functionality but does not update the test db.
    Uses a memory layer instead
    """

    def setUp(self):
        ensure_qgis_app_is_initialized()

        sqlite_path = TEST_DATA_DIR / "simple_breach_test.sqlite"
        assert sqlite_path.is_file(), "test data does not exist.."
        sqlite_path = str(sqlite_path)  # otherwise we get an TypeError below at
        # "self.predictor.get_uri(**db_kwargs)" arg. 1 has unexpected type 'PosixPath'

        db_kwargs = {
            "database": sqlite_path,
            "host": sqlite_path,
            "db_path": sqlite_path,
            "password": "",
            "port": "",
            "srid": "",
            "table_name": "v2_connected_pnt",
            "schema": "",
            "type": "",
            "username": "",
            "db_type": "spatialite",
        }
        self.predictor = Predictor(db_kwargs["db_type"])
        self.predictor.start_sqalchemy_engine(db_kwargs)
        self.uri = self.predictor.get_uri(**db_kwargs)
        self.conn_pnt_lyr = self.predictor.get_layer_from_uri(
            self.uri, constants.TABLE_NAME_CONN_PNT, "the_geom"
        )
        set_layer_crs(self.conn_pnt_lyr, "4326")
        search_distance = 20
        distance_to_levee = 5
        use_selection = False
        is_dry_run = True
        self.breach_location = BreachLocation(
            search_distance=search_distance,
            distance_to_levee=distance_to_levee,
            use_selection=use_selection,
            is_dry_run=is_dry_run,
            connected_pnt_lyr=self.conn_pnt_lyr,
        )

    def test_has_valid_selection(self):
        self.assertTrue(self.breach_location.has_valid_selection)

    def test_it_can_get_calc_points_by_content(self):
        # we expect a pipe of calc type 2 and of calc type 5
        expected_keys = [("1v2_pipe", 2), ("4v2_pipe", 5)]
        expected_calc_point_ids = [
            [2, 3, 4, 5, 6, 7, 8],  # belongs to pipe 1
            [26, 27, 28, 29, 30, 31, 32],  # belongs to pipe 4
        ]
        calc_points_dict = self.breach_location.get_calc_points_by_content()
        self.assertSetEqual(set(calc_points_dict.keys()), set(expected_keys))
        self.assertListEqual(
            sorted(list(calc_points_dict.values())), sorted(expected_calc_point_ids)
        )

    def test_it_can_get_connected_points(self):
        # let's get the connected points for pipe 1
        connected_points_selection = self.breach_location.get_connected_points(
            [2, 3, 4, 5, 6, 7, 8], calc_type=2  # ids of the calculation points
        )
        expected_connected_points = [
            {1: (3.31369, 47.9748)},
            {2: (3.31376, 47.9748)},
            {3: (3.31382, 47.9748)},
            {4: (3.31389, 47.9748)},
            {5: (3.31396, 47.9748)},
            {6: (3.31402, 47.9748)},
            {7: (3.31409, 47.9748)},
            # extrapolated point, does not have an id
            {None: (3.3142242860395994, 47.974823241109604)},
        ]
        self.assertListEqual(
            list(expected_connected_points[0].keys()),
            list(connected_points_selection[0].keys()),
        )

    def test_it_wont_move_points_behind_levee(self):
        connected_points_selection = self.breach_location.get_connected_points(
            [2, 3, 4, 5, 6, 7, 8], calc_type=2  # ids of the calculation points
        )
        self.breach_location.move_points_behind_levee(
            connected_points_selection, calc_type=2
        )
        req = QgsFeatureRequest().setFilterExpression('"levee_id" = 3')
        f_iter = self.conn_pnt_lyr.getFeatures(req)
        levee_ids = [f["levee_id"] for f in f_iter]
        self.assertEqual(len(levee_ids), 0)

    def test_it_can_create_tmp_layers(self):
        # we are in dry run mode so the temp layers shoul have been created
        # already on init
        self.assertTrue(hasattr(self.breach_location, "pnt_layer"))
        self.assertTrue(hasattr(self.breach_location, "line_layer"))

    def test_we_can_add_to_tmp_connected_point_layer(self):
        connected_points_selection = self.breach_location.get_connected_points(
            [2, 3, 4, 5, 6, 7, 8], calc_type=2  # ids of the calculation points
        )
        self.breach_location.move_points_behind_levee(
            connected_points_selection, calc_type=2
        )
        self.breach_location.pnt_layer.commitChanges()
        self.breach_location.pnt_layer.updateExtents()

        req = QgsFeatureRequest().setFilterExpression('"levee_id" = 3')
        f_iter = self.breach_location.pnt_layer.getFeatures(req)
        levee_ids = [f["levee_id"] for f in f_iter]
        self.assertEqual(len(levee_ids), 7)
        self.assertTrue(all([x == 3 for x in levee_ids]))

    def test_we_can_add_double_connected_points_to_layer(self):
        connected_points_selection = self.breach_location.get_connected_points(
            [26, 27, 28, 29, 30, 31, 32],  # ids of calculation points
            calc_type=5,  # double connected
        )
        self.breach_location.move_points_behind_levee(
            connected_points_selection, calc_type=5
        )
        self.breach_location.pnt_layer.commitChanges()
        self.breach_location.pnt_layer.updateExtents()

        req = QgsFeatureRequest().setFilterExpression('"levee_id" IN (4,5)')
        f_iter = self.breach_location.pnt_layer.getFeatures(req)
        levee_ids = [f["levee_id"] for f in f_iter]
        self.assertEqual(len(levee_ids), 14)
        self.assertTrue(all([x in (4, 5) for x in levee_ids]))

    def test_it_can_set_selected_pnt_ids(self):
        expected = collections.defaultdict(
            list, {1: [2], 2: [3], 3: [4], 4: [5], 5: [6], 6: [7], 7: [8]}
        )
        self.breach_location.connected_pnt_lyr.selectByIds([1, 2, 3, 4, 5, 6, 7])
        self.breach_location.set_selected_pnt_ids()
        self.assertDictEqual(expected, self.breach_location.selected_pnt_ids)

    def test_it_can_find_levee_intersections(self):

        perp_line = calculate_perpendicular_line(
            [3.31369, 47.9748, 3.31376, 47.9748],
            distance=self.breach_location.search_distance,
        )
        org_start = QgsPointXY(3.31369, 47.9748)

        line_start = QgsPointXY(perp_line[0], perp_line[1])
        line_end = QgsPointXY(perp_line[2], perp_line[3])
        # line_start, line_end, org_start
        levee_intersections = self.breach_location.find_levee_intersections(
            line_start, line_end, org_start
        )

        # should find two intersection
        self.assertEqual(len(levee_intersections), 2)

        # one with levee 2, another with levee 3
        self.assertListEqual(list(levee_intersections.keys()), [2, 3])

    def test_it_can_calculate_new_positions(self):
        perp_line = calculate_perpendicular_line(
            [3.31369, 47.9748, 3.31376, 47.9748],
            distance=self.breach_location.search_distance,
        )

        line_start = QgsPointXY(perp_line[0], perp_line[1])
        line_end = QgsPointXY(perp_line[2], perp_line[3])
        levee_intersections = collections.defaultdict()
        levee_intersections[2] = [(12.0, QgsPointXY(3.31369, 47.9747), 2)]
        levee_intersections[3] = [(3.0, QgsPointXY(3.31369, 47.9748), 3)]
        new_position, levee_id = self.breach_location.calculate_new_position(
            levee_intersections, line_start, line_end, 2
        )
        self.assertEqual(levee_id, 3)

    def test_it_can_elongate_perpendicular_line(self):
        perp_line = calculate_perpendicular_line(
            [3.31369, 47.9748, 3.31376, 47.9748],
            distance=self.breach_location.search_distance,
        )

        line_start = QgsPointXY(perp_line[0], perp_line[1])
        line_end = QgsPointXY(perp_line[2], perp_line[3])
        levee_intersections = collections.defaultdict()
        levee_intersections[2] = [(12.0, QgsPointXY(3.31369, 47.9747), 2)]
        levee_intersections[3] = [(3.0, QgsPointXY(3.31369, 47.9748), 3)]
        new_position, _ = self.breach_location.calculate_new_position(
            levee_intersections, line_start, line_end, 2
        )
        xy = new_position.constGet().x(), new_position.constGet().y()

        # set the distance to levee attribute to a high number
        self.breach_location.distance_to_levee = (
            self.breach_location.distance_to_levee * 2
        )
        new_position2, _ = self.breach_location.calculate_new_position(
            levee_intersections, line_start, line_end, 2
        )
        xy2 = new_position2.constGet().x(), new_position2.constGet().y()
        self.assertNotEqual(xy, xy2)


class TestBresLocation(unittest.TestCase):
    """
    Basically tests if the database table can be updated with the results
    """

    def setUp(self):
        ensure_qgis_app_is_initialized()
        test_db_orig = TEST_DATA_DIR / "simple_breach_test.sqlite"
        assert test_db_orig.is_file(), "test data does not exist.."
        test_db_orig = str(test_db_orig)  # otherwise we get an TypeError below at
        # "self.predictor.get_uri(**db_kwargs)" arg. 1 has unexpected type 'PosixPath'

        tmp_test_file_dir = tempfile.mkdtemp(prefix="breach_location_test")
        test_db_dest = os.path.join(tmp_test_file_dir, "simple_breach_test.sqlite")
        shutil.copyfile(test_db_orig, test_db_dest)

        db_kwargs = {
            "database": test_db_dest,
            "host": test_db_dest,
            "db_path": test_db_dest,
            "password": "",
            "port": "",
            "srid": "",
            "table_name": "v2_connected_pnt",
            "schema": "",
            "type": "",
            "username": "",
            "db_type": "spatialite",
        }
        self.predictor = Predictor(db_kwargs["db_type"])
        self.predictor.start_sqalchemy_engine(db_kwargs)
        self.uri = self.predictor.get_uri(**db_kwargs)
        self.conn_pnt_lyr = self.predictor.get_layer_from_uri(
            self.uri, constants.TABLE_NAME_CONN_PNT, "the_geom"
        )
        set_layer_crs(self.conn_pnt_lyr, "4326")
        search_distance = 20
        distance_to_levee = 5
        use_selection = False
        is_dry_run = False
        self.breach_location = BreachLocation(
            search_distance=search_distance,
            distance_to_levee=distance_to_levee,
            use_selection=use_selection,
            is_dry_run=is_dry_run,
            connected_pnt_lyr=self.conn_pnt_lyr,
        )
        self.test_db = test_db_dest

    def test_it_can_move_points_behind_levee(self):
        connected_points_selection = self.breach_location.get_connected_points(
            [2, 3, 4, 5, 6, 7, 8], calc_type=2  # ids of the calculation points
        )
        self.breach_location.move_points_behind_levee(
            connected_points_selection, calc_type=2
        )
        req = QgsFeatureRequest().setFilterExpression('"levee_id" = 3')
        f_iter = self.conn_pnt_lyr.getFeatures(req)
        # should all have been moved across the first levee (id 3)
        levee_ids = [f["levee_id"] for f in f_iter]
        self.assertEqual(len(levee_ids), 7)
        self.assertTrue(all([x == 3 for x in levee_ids]))

    def tearDown(self):
        os.remove(self.test_db)


class TestBreachLocationUtils(unittest.TestCase):
    def setUp(self):
        ensure_qgis_app_is_initialized()

    def test_it_can_get_epsg_code_from_layer(self):
        crs = "EPSG:28992"
        pnt_layer = QgsVectorLayer("Point?crs=" + crs, "temp_connected_pnt", "memory")
        epsg_code = get_epsg_code_from_layer(pnt_layer)
        self.assertEqual(epsg_code, 28992)

    def test_it_can_get_distance_between_points(self):
        pnt, pnt1 = QgsPointXY(0, 0), QgsPointXY(0, 10)
        dist = get_distance(pnt, pnt1, 4326)
        self.assertEqual(dist, 1105854.8332357334)
        dist = get_distance(pnt, pnt1, 28992)
        self.assertEqual(dist, 10.0)

    def test_it_can_calculate_perpendicular_line(self):
        line_coords = [0, 5, 0, 10]
        expected = (-20.0, 5.0, 20.0, 5.0)
        perpendicular_line = calculate_perpendicular_line(line_coords, 20)
        self.assertEqual(expected, perpendicular_line)
        perpendicular_line_left = calculate_perpendicular_line(line_coords, 20, "left")
        expected_left = (0, 5, -20.0, 5.0)
        self.assertEqual(expected_left, perpendicular_line_left)
        expected_right = (0, 5, 20.0, 5.0)
        perpendicular_line_right = calculate_perpendicular_line(
            line_coords, 20, "right"
        )
        self.assertEqual(expected_right, perpendicular_line_right)

        # should return None when the distance between the points <= 0
        line_coords = [0, 0, 0, 0]
        L = calculate_perpendicular_line(line_coords, 20)
        self.assertIsNone(L)
