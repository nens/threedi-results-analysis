import os
import unittest

from ..datasource.spatialite import TdiSpatialite
from ..datasource.netcdf import NetcdfDataSource

spatialite_datasource_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data', 'test_spatialite.sqlite')

netcdf_datasource_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data', 'testmodel', 'results', 'subgrid_map.nc')


@unittest.skipIf(not os.path.exists(spatialite_datasource_path),
                 "Path to test spatialite doesn't exist.")
class TestSpatialiteDatasource(unittest.TestCase):
    """ Test spatialite datasource"""

    def setUp(self):
        """Runs before each test."""
        self.ds = TdiSpatialite(self.spatialite_datasource_path)

    def test_init(self):
        """test initialisation and access to database"""

        # request spatialite version to trigger query to check init worked
        self.assertIsNotNone(self.ds.get_db_cursor())

    def test_metadata(self):
        """test metadata request"""
        self.assertEqual(self.ds.metadata['3di_script_version'], 56)

    def test_get_parameters(self):
        """ test get_parameter function"""

        self.assertListEqual(
            sorted(self.ds.get_parameters()),
            sorted(['s1', 'q', 'unorm', 'vol', 'q_pump'])
        )

        self.assertListEqual(
            sorted(self.ds.get_parameters('sewerage_manhole')),
            sorted(['s1', 'vol'])
        )

        self.assertListEqual(
            sorted(self.ds.get_parameters('sewerage_pipe')),
            sorted(['q', 'unorm'])
        )

        self.assertListEqual(
            sorted(self.ds.get_parameters('sewerage_pumpstation')),
            sorted(['q_pump'])
        )

        self.assertListEqual(
            sorted(self.ds.get_parameters(['sewerage_weir', 'sewerage_pumpstation'])),
            sorted(['q', 'unorm', 'q_pump'])
        )

    def test_object_types(self):
        """ test get_object_types function"""

        self.assertListEqual(
            sorted(self.ds.get_object_types()),
            sorted(['sewerage_manhole',
                    'sewerage_orifice',
                    'sewerage_pipe',
                    'sewerage_pumpstation',
                    'sewerage_weir']))

        self.assertListEqual(
            sorted(self.ds.get_object_types('q')),
            sorted(['sewerage_orifice',
                    'sewerage_pipe',
                    'sewerage_weir']))

        self.assertListEqual(
            sorted(self.ds.get_object_types('s1')),
            sorted(['sewerage_manhole']))

        self.assertListEqual(
            sorted(self.ds.get_object_types('q_pump')),
            sorted(['sewerage_pumpstation']))

        self.assertListEqual(
            sorted(self.ds.get_object_types(['q_pump', 's1'])),
            sorted(['sewerage_pumpstation',
                   'sewerage_manhole']))

    def test_object_count(self):
        """ test get_object_types function"""

        self.assertEqual(self.ds.get_object_count('sewerage_pumpstation'), 2)
        self.assertEqual(self.ds.get_object_count('sewerage_manhole'), 1260)
        self.assertEqual(self.ds.get_object_count('sewerage_orifice'), 3)
        self.assertEqual(self.ds.get_object_count('sewerage_pipe'), 1253)
        self.assertEqual(self.ds.get_object_count('sewerage_weir'), 23)

    #todo: get_objects
    #todo: get_object
    #todo: get_timestamps
    #todo: get_timestamp_count
    #todo: get_timeseries


@unittest.skipIf(not os.path.exists(netcdf_datasource_path),
                 "Path to test netcdf doesn't exist.")
class TestNetcdfDatasource(unittest.TestCase):

    def setUp(self):
        self.ncds = NetcdfDataSource(netcdf_datasource_path)

    def test_netcdf_loaded(self):
        """We can open the Netcdf file"""
        self.assertTrue(self.ncds.ds is not None)

    def test_id_mapping_loaded(self):
        """The datasource correctly finds the id_mapping.json."""
        self.assertTrue(self.ncds.id_mapping is not None)

    def test_timestamps(self):
        """We'll asume there are always some time steps"""
        ts = self.ncds.get_timestamps(object_type="doesn't matter")
        self.assertTrue(len(ts) > 0)
        self.assertEqual(ts[0], 0.0)
        self.assertNotEqual(ts[1], 0.0)
