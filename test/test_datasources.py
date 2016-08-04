import os
import unittest
import tempfile
import shutil

from utilities import get_qgis_app
QGIS_APP = get_qgis_app()

from qgis.core import QgsVectorLayer, QgsFeature, QgsPoint, QgsField, QgsGeometry
from PyQt4.QtCore import QVariant

from ThreeDiToolbox.datasource.result_spatialite import (
    TdiSpatialite,
    get_datasource_variable,
    get_variables,
    )

from ThreeDiToolbox.datasource.netcdf import NetcdfDataSource

from ThreeDiToolbox.datasource.spatialite import Spatialite


spatialite_datasource_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data', 'test_spatialite.sqlite')

netcdf_datasource_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data', 'testmodel', 'results', 'subgrid_map.nc')


class TestParameters(unittest.TestCase):
    """Test functions that convert parameters to variable names in the
    datasource."""

    def test_get_datasource_variable_kunstwerk(self):
        out = get_datasource_variable('q', 'pipe')
        self.assertEqual(out, ['q'])

    def test_get_datasource_variable_pump(self):
        out = get_datasource_variable('q', 'pumpstation')
        self.assertEqual(out, ['q_pump'])

    def test_get_datasource_variable_manhole(self):
        out = get_datasource_variable('s1', 'manhole')
        self.assertEqual(out, ['s1'])

    def test_get_variables(self):
        vars = get_variables(object_type='pipe', parameters=['q'])
        self.assertEqual(vars, ['q'])

    def test_get_variables2(self):
        """Get both u variable names for backwards compatability."""
        vars = get_variables('pipe', ['u1'])
        self.assertEqual(vars, ['u1', 'unorm'])

    def test_get_variables3(self):
        vars = get_variables('pumpstation', ['q'])
        self.assertEqual(vars, ['q_pump'])


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


class TestSpatialiteDataSource(unittest.TestCase):

    def setUp(self):
        self.tmp_directory = tempfile.mkdtemp()
        self.spatialite_path = os.path.join(self.tmp_directory, 'test.sqlite')

    def tearDown(self):
        shutil.rmtree(self.tmp_directory)

    def test_create_empty_table(self):
        spl = Spatialite(self.spatialite_path + '1')

        layer = spl.create_empty_layer('table_one',
                                       fields=['id INTEGER', 'name TEXT NULLABLE'])
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


