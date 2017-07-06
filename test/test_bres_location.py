"""
Test geo utils.
"""
import unittest
import os

from ThreeDiToolbox.threedi_schema_edits.bres_location import BresLocation
from ThreeDiToolbox.threedi_schema_edits.bres_location import Predictor
from ThreeDiToolbox.utils import constants


class TestBresLocation(unittest.TestCase):

   def setUp(self):

        # os.path.abspath(__file__)
        test_db = os.path.join('data', 'simple_bres_test.sqlite')
        db_kwargs = {
            'database': test_db,
            'host': test_db,
            'password': '',
            'port': '',
            'srid': '',
            'table_name': 'v2_connected_pnt',
            'schema': '',
            'type': '',
            'username': '',
            'db_type': 'spatialite',
        }
        predictor = Predictor(db_kwargs['db_type'])
        uri = predictor.get_uri(**db_kwargs)
        self.conn_pnt_lyr = predictor.get_layer_from_uri(
            uri, constants.TABLE_NAME_CONN_PNT, 'the_geom')
        search_distance = 20
        distance_to_levee = 5
        use_selection = False
        is_dry_run = False
        self.bres_location = BresLocation(
            search_distance=search_distance,
            distance_to_levee=distance_to_levee,
            use_selection=use_selection,
            is_dry_run=is_dry_run,
            connected_pnt_lyr=self.conn_pnt_lyr)

   def test_has_valid_selection(self):
        self.assertTrue(self.bres_location.has_valid_selection)
