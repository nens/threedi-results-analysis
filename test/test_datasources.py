from distutils.version import LooseVersion
import mock
import os
import platform
import unittest
import tempfile
import shutil
import sys

try:
    from qgis.core import (
        QgsVectorLayer, QgsFeature, QgsPoint, QgsField, QgsGeometry)
except ImportError:
    pass

from PyQt4.QtCore import QVariant

try:
    from ThreeDiToolbox.datasource.spatialite import Spatialite
except ImportError:
    # Linux specific
    sys.path.append('/usr/share/qgis/python/plugins/')
    try:
        from ThreeDiToolbox.datasource.spatialite import Spatialite
    except ImportError:
        print("Can't import Spatialite.")
        Spatialite = None
from ThreeDiToolbox.datasource.netcdf import (
    NetcdfDataSource,
    normalized_object_type,
    find_id_mapping_file,
    find_aggregation_netcdf,
)
from ThreeDiToolbox.datasource.netcdf_groundwater import (
    NetcdfGroundwaterDataSource,
)
from .utilities import get_qgis_app

QGIS_APP = get_qgis_app()
linux_dist, ubuntu_version, _ = platform.linux_distribution()
spatialite_datasource_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data', 'test_spatialite.sqlite')
netcdf_datasource_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data', 'testmodel', 'results', 'subgrid_map.nc')


def result_data_is_available(flow_agg_must_exist=False):
    """Check if we have the necessary result data for the tests."""
    if not os.path.exists(netcdf_datasource_path):
        return False
    try:
        find_id_mapping_file(netcdf_datasource_path)
    except IndexError:
        return False
    if flow_agg_must_exist:
        try:
            find_aggregation_netcdf(netcdf_datasource_path)
        except IndexError:
            return False
    return True


@unittest.skipIf(not result_data_is_available(),
                 "Result data doesn't exist or is incomplete.")
class TestNetcdfDatasource(unittest.TestCase):

    def setUp(self):
        self.ncds = NetcdfDataSource(netcdf_datasource_path,
                                     load_properties=False)

        # cherry picked id and object type that exist in this
        # test set
        self.cherry_picked_object_id = 114
        self.cherry_picked_object_type = 'v2_weir_view'
        # the inp id the cherry picked object id maps to (look in
        # id_mapping.json)
        self.complementary_inp_id_of_object_id = 5472

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

    def test_available_vars(self):
        """Test getting variable names out of netCDF datasource."""
        all_vars = self.ncds.get_available_variables()
        subgrid_vars = self.ncds.get_available_variables(only_subgrid_map=True)
        agg_vars = self.ncds.get_available_variables(only_aggregation=True)
        self.assertTrue(len(all_vars) > 0)
        self.assertEqual(len(subgrid_vars) + len(agg_vars), len(all_vars))

    def test_load_properties(self):
        """Test loading properties works with a netcdf file."""
        self.ncds.load_properties()

    def test_node_mapping(self):
        self.ncds.node_mapping

    def test_get_ids_memory_layers(self):
        """test memory layers that are not mapped."""
        object_id = 42
        for object_type in ['flowline', 'node', 'pumpline']:
            ncid = self.ncds.obj_to_netcdf_id(object_id, object_type)
            self.assertEqual(ncid, object_id)

    def test_get_ids_spatialite_layers(self):
        """NOTE: this test will fail if you the object types cannot be found
        in the id_mapping json. You might need to fix this when renewing
        the model.

        Furthermore, this tests a feature (the channel_mapping) that is a bit
        iffy in the sense that its correctness can be debated owning to the
        fact that for channel mappings multiple links can belong to one inp
        id which leads to all sorts of problems.
        """
        norm_obj_type = normalized_object_type(self.cherry_picked_object_type)
        inp_id = self.ncds.inp_id_from(
            self.cherry_picked_object_id, norm_obj_type)
        self.assertEqual(inp_id, self.complementary_inp_id_of_object_id)

        ncid = self.ncds.netcdf_id_from(inp_id, norm_obj_type)
        self.assertEqual(
            ncid,
            self.ncds.obj_to_netcdf_id(
                self.cherry_picked_object_id,
                norm_obj_type
            )
        )

    def test_get_timeseries(self):
        """Test get_timeseries from datasource."""
        # q exists
        self.assertTrue(
            'q' in self.ncds.available_subgrid_map_vars
        )
        ts = self.ncds.get_timeseries(
            'flowlines',
            # We assume there is at least one timestep of data that we can
            # slice
            0,
            'q',
        )
        self.assertEqual(ts.shape[1], 2)  # timeseries has two columns

    @unittest.skipIf(
        not result_data_is_available(flow_agg_must_exist=True),
        "No flow aggregate found.")
    def test_flow_aggregate(self):
        """Simple flow aggregate checks."""
        self.assertTrue(self.ncds.ds_aggregation)
        self.assertTrue(self.ncds.get_agg_var_timestamps('s1_max').size > 0)
        ts = self.ncds.get_timeseries(
            'nodes',
            0,
            's1_max',
        )
        self.assertEqual(ts.shape[1], 2)  # timeseries has two columns


class TestNetcdfDatasourceBasic(unittest.TestCase):
    """Some basic tests without needing an actual netCDF file."""

    def setUp(self):
        class Mock(object):
            pass
        mock = Mock()  # Mock the netCDF Dataset
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
        self.assertEqual(self.ncds.end_n1dtot, 3 + 7)

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


@unittest.skipIf(
    linux_dist == 'Ubuntu' and
    LooseVersion(ubuntu_version) < LooseVersion('16.04'),
    "Your Ubuntu version probably has a GDAL/OGR version that's too old for "
    "this test to succeed.")
@unittest.skipIf(Spatialite is None, "Can't import Spatialite datasource")
class TestSpatialiteDataSource(unittest.TestCase):

    def setUp(self):
        self.tmp_directory = tempfile.mkdtemp()
        self.spatialite_path = os.path.join(self.tmp_directory, 'test.sqlite')

    def tearDown(self):
        shutil.rmtree(self.tmp_directory)

    def test_create_empty_table(self):
        spl = Spatialite(self.spatialite_path + '1')

        layer = spl.create_empty_layer(
            'table_one', fields=['id INTEGER', 'name TEXT NULLABLE'])
        # test table is created
        self.assertIsNotNone(layer)
        self.assertTrue('table_one' in [c[1] for c in spl.getTables()])
        self.assertFalse('table_two' in spl.getTables())

        # test adding data
        self.assertEqual(layer.featureCount(), 0)
        pr = layer.dataProvider()

        feat = QgsFeature()
        feat.setAttributes([1, 'test'])
        feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(1.0, 2.0)))

        pr.addFeatures([feat])
        self.assertEqual(layer.featureCount(), 1)

    def test_import_layer(self):
        spl = Spatialite(self.spatialite_path + '3')

        # create memory layer
        uri = "Point?crs=epsg:4326&index=yes"
        layer = QgsVectorLayer(uri, "test_layer", "memory")
        pr = layer.dataProvider()

        # add fields
        pr.addAttributes([
            QgsField("id", QVariant.Int),
            QgsField("col2", QVariant.Double),
            QgsField("col3", QVariant.String, None, 20),
            QgsField("col4", QVariant.TextFormat),
        ])
        # tell the vector layer to fetch changes from the provider
        layer.updateFields()
        pr = layer.dataProvider()
        feat = QgsFeature()
        feat.setAttributes([1, 'test'])
        feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(1.0, 2.0)))
        pr.addFeatures([feat])

        spl_layer = spl.import_layer(layer, 'table_one', 'id')

        self.assertIsNotNone(spl_layer)
        self.assertTrue('table_one' in [c[1] for c in spl.getTables()])
        self.assertEqual(layer.featureCount(), 1)


class TestNetcdfGroundwaterDataSource(unittest.TestCase):
    def test_constructor(self):
        """Test empty constructor."""
        NetcdfGroundwaterDataSource()

    def test_ts(self):
        nds = NetcdfGroundwaterDataSource()
        m = mock.MagicMock()
        nds._ds = m
        # sanity test
        self.assertEqual(nds.ds, m)
