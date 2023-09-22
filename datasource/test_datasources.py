from qgis.core import QgsFeature
from qgis.core import QgsField
from qgis.core import QgsGeometry
from qgis.core import QgsPointXY
from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QVariant
from threedigrid.admin import gridresultadmin
from threedigrid.admin.constants import NO_DATA_VALUE
from ThreeDiToolbox.datasource import base
from ThreeDiToolbox.datasource.spatialite import Spatialite
from ThreeDiToolbox.tests.utilities import ensure_qgis_app_is_initialized
from ThreeDiToolbox.tests.utilities import TemporaryDirectory

import h5py
import mock
import numpy as np
import os
import pytest
import shutil
import tempfile
import unittest


spatialite_datasource_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "data", "test_spatialite.sqlite"
)


class TestSpatialiteDataSource(unittest.TestCase):
    def setUp(self):
        ensure_qgis_app_is_initialized()
        self.tmp_directory = tempfile.mkdtemp()
        self.spatialite_path = os.path.join(self.tmp_directory, "test.sqlite")

    def tearDown(self):
        shutil.rmtree(self.tmp_directory)

    def test_create_empty_table(self):
        spl = Spatialite(self.spatialite_path + "1")

        layer = spl.create_empty_layer(
            "table_one", fields=["id INTEGER", "name TEXT NULLABLE"]
        )
        # test table is created
        self.assertIsNotNone(layer)

        self.assertTrue("table_one" in [c[1] for c in spl.getTables()])
        self.assertFalse("table_two" in spl.getTables())

        # test adding data
        self.assertEqual(layer.featureCount(), 0)
        pr = layer.dataProvider()

        feat = QgsFeature()
        feat.setAttributes([1, "test"])
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(1.0, 2.0)))

        pr.addFeatures([feat])
        self.assertEqual(layer.featureCount(), 1)

    def test_import_layer(self):
        spl = Spatialite(self.spatialite_path + "3")

        # create memory layer
        uri = "Point?crs=epsg:4326&index=yes"
        layer = QgsVectorLayer(uri, "test_layer", "memory")
        pr = layer.dataProvider()

        # add fields
        pr.addAttributes(
            [
                QgsField("id", QVariant.Int),
                QgsField("col2", QVariant.Double),
                QgsField("col3", QVariant.String, None, 20),
                QgsField("col4", QVariant.TextFormat),
            ]
        )
        # tell the vector layer to fetch changes from the provider
        layer.updateFields()
        pr = layer.dataProvider()
        feat = QgsFeature()
        feat.setAttributes([1, "test"])
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(1.0, 2.0)))
        pr.addFeatures([feat])

        spl_layer = spl.import_layer(layer, "table_one", "id")

        self.assertIsNotNone(spl_layer)
        self.assertTrue("table_one" in [c[1] for c in spl.getTables()])
        # TODO 2021-03-31: re-enable the following line and fix the test!
        # self.assertEqual(layer.featureCount(), 1)

