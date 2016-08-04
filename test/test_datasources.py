import os
import unittest

from ThreeDiToolbox.datasource.netcdf import NetcdfDataSource, get_variables

spatialite_datasource_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data', 'test_spatialite.sqlite')

netcdf_datasource_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data', 'testmodel', 'results', 'subgrid_map.nc')


class TestParameters(unittest.TestCase):
    """Test functions that convert parameters to variable names in the
    datasource."""

    def test_get_variables(self):
        vars = get_variables(object_type='pipe', parameters=['q'])
        self.assertEqual(vars, ['q'])

    def test_get_variables2(self):
        """Get both u variable names for backwards compatability."""
        vars = get_variables('pipe', ['u1'])
        self.assertEqual(vars, ['u1'])

    def test_get_variables3(self):
        vars = get_variables('pumpstation', ['q'])
        self.assertEqual(vars, ['q_pump'])


@unittest.skipIf(not os.path.exists(netcdf_datasource_path),
                 "Path to test netcdf doesn't exist.")
class TestNetcdfDatasource(unittest.TestCase):

    def setUp(self):
        self.ncds = NetcdfDataSource(netcdf_datasource_path,
                                     load_properties=False)

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
