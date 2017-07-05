"""
Test utils.
"""
import unittest

from qgis.core import QgsVectorLayer

from PyQt4.QtCore import QVariant

from ThreeDiToolbox.utils.layer_from_netCDF import make_flowline_layer
from ThreeDiToolbox.utils.utils import parse_db_source_info


class TestLayerFuncs(unittest.TestCase):
    def test_smoke(self):
        make_flowline_layer


class TestDBSourceInfoParser(unittest.TestCase):

    def test_it_can_parse_sqlite_info(self):
        info_string = 'dbname=\'/home/test_user/v2_bergermeer/test_plugin/v2_bergermeer.sqlite\' table="v2_connected_pnt" (the_geom) sql='  # noqa
        s_info = parse_db_source_info(info_string)
        expected = {
            'database': '/home/test_user/v2_bergermeer/test_plugin/v2_bergermeer.sqlite',  # noqa
            'host': '/home/test_user/v2_bergermeer/test_plugin/v2_bergermeer.sqlite',  # noqa,
            'password': '',
            'port': '',
            'srid': '',
            'table_name': 'v2_connected_pnt',
            'schema': '',
            'type': '',
            'username': '',
            'db_type': 'spatialite',
        }
        self.assertDictEqual(s_info, expected)

    def test_it_can_parse_postgres_info(self):
        info_string = u'dbname=\'work_test\' host=localhost port=54324 user=\'tester\' password=\'test_pw\' sslmode=disable key=\'id\' srid=28992 type=LineString table="public"."v2_levee" (the_geom) sql='  # noqa
        expected = {
            'database': u'work_test',
            'host': 'localhost',
            'password': u'test_pw',
            'port': '54324',
            'schema': 'public',
            'srid': '28992',
            'table_name': 'v2_levee',
            'type': 'LineString',
            'username': 'tester',
            'db_type': 'postgres',
        }
        s_info = parse_db_source_info(info_string)
        self.assertDictEqual(s_info, expected)
