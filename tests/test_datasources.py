from qgis.core import QgsFeature
from qgis.core import QgsField
from qgis.core import QgsGeometry
from qgis.core import QgsPointXY
from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QVariant
from threedigrid.admin import gridresultadmin
from ThreeDiToolbox.datasource.spatialite import Spatialite
from ThreeDiToolbox.datasource.threedi_results import find_aggregation_netcdf
from ThreeDiToolbox.datasource.threedi_results import ThreediResult
from ThreeDiToolbox.tests.utilities import ensure_qgis_app_is_initialized
from ThreeDiToolbox.tests.utilities import TemporaryDirectory

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

THREEDI_RESULTS_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "data",
    "testmodel",
    "v2_bergermeer",
    "results_3di.nc",
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
        self.assertEqual(layer.featureCount(), 1)


class TestNetcdfGroundwaterDataSource(unittest.TestCase):
    def test_constructor(self):
        """Test empty constructor."""
        ThreediResult()

    @mock.patch(
        "ThreeDiToolbox.datasource.threedi_results.ThreediResult.available_subgrid_map_vars",
        ["s1"],
    )
    @mock.patch("ThreeDiToolbox.datasource.threedi_results.ThreediResult.result_admin")
    def test_get_timeseries(self, result_admin_mock):
        threedi_result = ThreediResult()
        threedi_result._datasource = mock.MagicMock()
        threedi_result.get_timeseries("s1", 3)

    def test_find_agg_fail(self):
        with TemporaryDirectory() as tempdir:
            nc_path = os.path.join(tempdir, "bla.nc")
            with self.assertRaises(FileNotFoundError):
                find_aggregation_netcdf(nc_path)

    def test_find_agg_success(self):
        with TemporaryDirectory() as tempdir:
            nc_path = os.path.join(tempdir, "bla.nc")
            agg_path = os.path.join(tempdir, "aggregate_results_3di.nc")
            with open(agg_path, "w") as aggfile:
                aggfile.write("doesnt matter")
            agg_path_found = find_aggregation_netcdf(nc_path)
            self.assertEqual(agg_path, agg_path_found)


def test_get_timestamps_shape(threedi_result):
    timestamps = threedi_result.get_timestamps()
    assert timestamps.shape == (32,)


def test_get_timestamps_last_timestep(threedi_result):
    timestamps = threedi_result.get_timestamps()
    assert timestamps[-1] == 1863.5643704609731


def test_get_timestamps_with_agg_parameter_q_cum(threedi_result):
    timestamps_q_cum = threedi_result.get_timestamps(parameter="q_cum")
    assert timestamps_q_cum.shape == (7,)
    assert timestamps_q_cum[-1] == 1801.2566835460611


def test_get_timestamps_with_agg_parameter_vol_current(threedi_result):
    timestamps_vol_current = threedi_result.get_timestamps(parameter="vol_current")
    assert timestamps_vol_current.shape == (7,)
    assert timestamps_vol_current[-1] == 1801.2566835460611


def test_get_gridadmin(threedi_result):
    ga = threedi_result.get_gridadmin(variable=None)
    assert isinstance(ga, gridresultadmin.GridH5Admin)


def test_get_gridadmin_result_var(threedi_result):
    ga = threedi_result.get_gridadmin(variable="s1")
    assert isinstance(ga, gridresultadmin.GridH5ResultAdmin)


def test_get_gridadmin_agg_result_var(threedi_result):
    ga = threedi_result.get_gridadmin(variable="q_cum")
    assert isinstance(ga, gridresultadmin.GridH5AggregateResultAdmin)


def test_get_gridadmin_agg_result_var_not_available(threedi_result):
    with pytest.raises(AttributeError):
        threedi_result.get_gridadmin(variable="u1_max")


def test_get_gridadmin_unknown_var(threedi_result):
    with pytest.raises(AttributeError):
        threedi_result.get_gridadmin(variable="unknown")


def test_get_timeseries(threedi_result):
    time_series = threedi_result.get_timeseries("s1")
    np.testing.assert_equal(time_series[:, 0], threedi_result.get_timestamps())
    assert time_series.shape[1] == threedi_result.get_gridadmin("s1").nodes.count + 1


def test_get_timeseries_filter_node(threedi_result):
    with mock.patch(
        "threedigrid.orm.base.models.Model.get_filtered_field_value"
    ) as data:
        data.return_value = np.ones((len(threedi_result.timestamps), 1))
        time_series = threedi_result.get_timeseries("s1", node_id=5)
        np.testing.assert_equal(time_series[:, 0], threedi_result.get_timestamps())
        np.testing.assert_equal(time_series[:, 1], data.return_value[:, 0])


def test_get_model_instance_by_field_name(threedi_result):
    """A bug in threedigrid <= 1.0.12

    Note that querying these variables, ('s1' in the gridresultadmin and
    'q_cum' in the gridaggregateresultadmin) should not fail.

    Will be fixed in threedigrid >= 1.0.13"""
    gr = threedi_result.get_gridadmin("s1")
    gr.get_model_instance_by_field_name("s1")

    gr = threedi_result.get_gridadmin("q_cum")
    gr.get_model_instance_by_field_name("q_cum")


def test_get_values_by_timestep_nr(threedi_result):
    with mock.patch.object(threedi_result, "_nc_from_mem") as data:
        trash_elements = np.zeros((3, 1))
        variable_data = np.array(range(9)).reshape(3, 3)
        data.return_value = np.hstack((trash_elements, variable_data))
        values = threedi_result.get_values_by_timestep_nr("s1", 2)
        np.testing.assert_equal(values, np.array([6, 7, 8]))


def test_get_values_by_timestep_nr_with_index(threedi_result):
    with mock.patch.object(threedi_result, "_nc_from_mem") as data:
        data.return_value = np.array(range(9)).reshape(3, 3)
        values = threedi_result.get_values_by_timestep_nr(
            "s1", 2, node_ids=np.array([1, 2])
        )
        np.testing.assert_equal(values, np.array([7, 8]))


def test_get_values_by_timestep_nr_with_multipe_timestamps(threedi_result):
    with mock.patch.object(threedi_result, "_nc_from_mem") as data:
        trash_elements = np.zeros((3, 1))
        variable_data = np.array(range(9)).reshape(3, 3)
        data.return_value = np.hstack((trash_elements, variable_data))
        values = threedi_result.get_values_by_timestep_nr(
            "s1", timestamp_idx=np.array([0, 2])
        )
        np.testing.assert_equal(values, np.array([[0, 1, 2], [6, 7, 8]]))


def test_get_values_by_timestep_nr_duplicate_node_ids(threedi_result):
    with mock.patch.object(threedi_result, "_nc_from_mem") as data:
        data.return_value = np.array(range(9)).reshape(3, 3)
        values = threedi_result.get_values_by_timestep_nr(
            "s1", timestamp_idx=1, node_ids=np.array([0, 0, 2])
        )
        np.testing.assert_equal(values, np.array([3, 3, 5]))


def test_get_values_by_timestep_nr_unsorted_node_ids(threedi_result):
    with mock.patch.object(threedi_result, "_nc_from_mem") as data:
        data.return_value = np.array(range(9)).reshape(3, 3)
        values = threedi_result.get_values_by_timestep_nr(
            "s1", timestamp_idx=0, node_ids=np.array([1, 0, 2])
        )
        np.testing.assert_equal(values, np.array([1, 0, 2]))


def test_get_values_by_timestep_nr_timestamp_idx_array_one(threedi_result):
    with mock.patch.object(threedi_result, "_nc_from_mem") as data:
        data.return_value = np.array(range(9)).reshape(3, 3)
        values = threedi_result.get_values_by_timestep_nr(
            "s1", timestamp_idx=np.array([2]), node_ids=np.array([0, 1])
        )
        np.testing.assert_equal(values, np.array([6, 7]))


def test_get_values_by_timestep_nr_timestamp_and_node_ids(threedi_result):
    with mock.patch.object(threedi_result, "_nc_from_mem") as data:
        data.return_value = np.array(range(9)).reshape(3, 3)
        values = threedi_result.get_values_by_timestep_nr(
            "s1", timestamp_idx=np.array([1, 2]), node_ids=np.array([0, 1])
        )
        np.testing.assert_equal(values, np.array([[3, 4], [6, 7]]))


def test__nc_from_mem(threedi_result):
    threedi_result._nc_from_mem("s1")
    assert "s1" in threedi_result._cache.keys()


def test_available_subgrid_map_vars(threedi_result):
    actual_vars = threedi_result.available_subgrid_map_vars
    expected_vars = {
        "au",
        "q",
        "q_lat",
        "q_pump",
        "rain",
        "s1",
        "su",
        "u1",
        "vol",
        "intercepted_volume",
        "leak",
        "q_sss",
    }
    assert set(actual_vars) == expected_vars


def test_available_aggregation_vars(threedi_result):
    actual_aggregation_vars = threedi_result.available_aggregation_vars
    expected_aggregation_vars = {
        "q_cum",
        "q_cum_positive",
        "q_cum_negative",
        "q_lat_cum",
        "q_pump_cum",
        "rain_cum",
        "vol_current",
        "infiltration_rate_simple_cum",
        "intercepted_volume_current",
        "leak_cum",
        "q_sss_cum",
        "rain_cum",
        "infiltration_rate_simple_cum",
    }
    assert set(actual_aggregation_vars) == expected_aggregation_vars


def test_available_vars(threedi_result):
    actual = threedi_result.available_vars
    normal_vars = {
        "au",
        "q",
        "q_lat",
        "q_pump",
        "rain",
        "s1",
        "su",
        "u1",
        "vol",
        "intercepted_volume",
        "leak",
        "q_sss",
    }
    agg_vars = {
        "q_cum",
        "q_cum_positive",
        "q_cum_negative",
        "q_lat_cum",
        "q_pump_cum",
        "rain_cum",
        "vol_current",
        "infiltration_rate_simple_cum",
        "intercepted_volume_current",
        "leak_cum",
        "q_sss_cum",
        "rain_cum",
        "infiltration_rate_simple_cum",
    }
    expected = normal_vars | agg_vars
    assert set(actual) == expected
