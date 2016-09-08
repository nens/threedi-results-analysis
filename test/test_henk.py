import os
import unittest
import tempfile
import shutil
import sys

try:
    from qgis.core import (
        QgsVectorLayer, QgsFeature, QgsPoint, QgsField, QgsGeometry)
except ImportError:
    pass


from ThreeDiToolbox.datasource.netcdf import NetcdfDataSource

netcdf_datasource_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data', 'testmodel', 'results', 'subgrid_map.nc')


class TestNetcdfDatasourceBasic(unittest.TestCase):
    """Some basic tests without needing an actual netCDF file."""

    def setUp(self):
        mock = lambda x: 'mock'  # Mock the netCDF Dataset
        self.ncds = NetcdfDataSource(netcdf_datasource_path,
                                     load_properties=False,
                                     ds=mock)

    def test_load_properties(self):
        """Test getting attributes from netCDF."""
        self.ncds.ds.nFlowElem = 41
        self.ncds.ds.nFlowElem2d = 3
        self.ncds.ds.nFlowElem1d = 7
        self.ncds.ds.nFlowLine = 42
        self.ncds.load_properties()
        self.assertEqual(self.ncds.nFlowLine, 42)
        self.assertEqual(self.ncds.nodall, 41)
        self.assertEqual(self.ncds.end_n1dtot, 3+7)

    def test_load_properties_default_values(self):
        """Test the default value when attribute isn't present."""
        # just cherry-picked a few attributes in this test
        self.ncds.load_properties()
        self.assertEqual(self.ncds.nodall, 0)
        self.assertEqual(self.ncds.n2dtot, 0)
        self.assertEqual(self.ncds.n1dtot, 0)
        self.assertEqual(self.ncds.nFlowLine, 0)
        self.assertEqual(self.ncds.nFlowLine2d, 0)
        self.assertEqual(self.ncds.nFlowLine1dBounds, 0)
        self.assertEqual(self.ncds.nFlowLine2dBounds, 0)
