from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel, ThreeDiGridItem, ThreeDiResultItem
from qgis.PyQt.QtCore import Qt
import unittest
from pathlib import Path


class TestModel(unittest.TestCase):
    def test_creation(self):
        model = ThreeDiPluginModel()
        self.assertTrue(model)

    def test_created_model_has_zero_grids(self):
        model = ThreeDiPluginModel()
        self.assertEqual(model.number_of_grids(), 0)

    def test_created_model_has_zero_results(self):
        model = ThreeDiPluginModel()
        self.assertEqual(model.number_of_results(), 0)

    def test_clear_1(self):
        model = ThreeDiPluginModel()
        self.grid_item = ThreeDiGridItem("c:/test/gridadmin.h5", "text")
        self.assertTrue(model.add_grid(self.grid_item))
        self.assertEqual(model.number_of_grids(), 1)
        model.clear()
        self.assertEqual(model.number_of_grids(), 0)


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.model = ThreeDiPluginModel()
        self.grid_path = Path("c:/test/gridadmin.h5")

    def test_creation(self):
        item = ThreeDiGridItem(self.grid_path, "text")
        self.assertTrue(item)

    def test_adding(self):
        item = ThreeDiGridItem(self.grid_path, "text")
        self.assertTrue(self.model.add_grid(item))

    def test_removal(self):
        item = ThreeDiGridItem(self.grid_path, "text")
        self.assertTrue(self.model.add_grid(item))
        self.assertEqual(self.model.number_of_grids(), 1)
        self.assertTrue(self.model.remove_grid(item))
        self.assertEqual(self.model.number_of_grids(), 0)

    def test_contains_path_check(self):
        item = ThreeDiGridItem(self.grid_path, "text")
        self.assertTrue(self.model.add_grid(item))
        item2 = ThreeDiGridItem(self.grid_path, "text")
        self.assertFalse(self.model.add_grid(item2))

    def test_contains_path_check_extension_ignored(self):
        item = ThreeDiGridItem(self.grid_path, "text")
        self.assertTrue(self.model.add_grid(item))
        item2 = ThreeDiGridItem(self.grid_path.with_suffix('.gpkg'), "text")
        self.assertFalse(self.model.add_grid(item2))

    def test_grid_can_be_retrieved_via_id(self):
        item = ThreeDiGridItem(self.grid_path, "text")
        self.assertTrue(self.model.add_grid(item))
        retrieved_item = self.model.get_grid(item.id)
        self.assertTrue(item is retrieved_item)

        nonexisting_item = self.model.get_grid("thisidprobablydoesntexist")
        self.assertTrue(nonexisting_item is None)

    def test_id_can_be_set(self):
        item = ThreeDiGridItem(self.grid_path, "text", "anewid")
        self.assertTrue(self.model.add_grid(item))
        self.assertEqual(item.id, "anewid")

    def test_id_will_be_set(self):
        item = ThreeDiGridItem(self.grid_path, "text")
        self.assertTrue(self.model.add_grid(item))
        self.assertIsNotNone(item.id)


class TestResult(unittest.TestCase):
    def setUp(self):
        self.result_path = Path("c:/test/results_3di.nc")

        self.model = ThreeDiPluginModel()
        self.grid_item = ThreeDiGridItem("c:/test/gridadmin.h5", "text")
        self.assertTrue(self.model.add_grid(self.grid_item))

    def test_creation(self):
        item = ThreeDiResultItem(self.result_path, "text")
        self.assertTrue(item)
        self.assertIsNone(item.group_path)
        self.assertIsNone(item.layer_group)
        self.assertEqual(item.layer_ids, {})

    def test_addition(self):
        item = ThreeDiResultItem(self.result_path, "text")
        self.assertTrue(self.model.add_result(item, self.grid_item))
        self.assertTrue(self.model.number_of_results(), 1)

    def test_removal(self):
        item = ThreeDiResultItem(self.result_path, "text")
        self.assertTrue(self.model.add_result(item, self.grid_item))
        self.assertEqual(self.model.number_of_results(), 1)
        self.assertTrue(self.model.remove_result(item))
        self.assertEqual(self.model.number_of_results(), 0)

    def test_checked_results_also_removed(self):
        item = ThreeDiResultItem(self.result_path, "text")
        item.setCheckState(Qt.CheckState.Checked)
        item2 = ThreeDiResultItem(("c:/test2/results_3di.nc"), "text")

        self.assertTrue(self.model.add_result(item, self.grid_item))
        self.assertTrue(self.model.add_result(item2, self.grid_item))
        self.assertEqual(self.model.number_of_results(), 2)
        self.assertTrue(self.model.remove_result(item))
        self.assertEqual(self.model.number_of_results(), 1)

    def test_removing_grid_removes_result(self):
        item = ThreeDiResultItem(self.result_path, "text")
        self.assertTrue(self.model.add_result(item, self.grid_item))
        self.assertEqual(self.model.number_of_results(), 1)
        self.assertTrue(self.model.remove_grid(self.grid_item))
        self.assertEqual(self.model.number_of_results(), 0)

    def test_removing_by_index(self):
        item = ThreeDiResultItem(self.result_path, "text")
        self.assertTrue(self.model.add_result(item, self.grid_item))
        self.assertEqual(self.model.number_of_results(), 1)
        self.assertTrue(self.model.remove_index(item.index()))
        self.assertEqual(self.model.number_of_results(), 0)

    def test_results_can_be_retrieved(self):
        item = ThreeDiResultItem(self.result_path, "text")
        self.assertTrue(self.model.add_result(item, self.grid_item))
        results = self.model.get_results(checked_only=False)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0] is item)

    def test_result_can_be_retrieved(self):
        item = ThreeDiResultItem(self.result_path, "text")
        self.assertTrue(self.model.add_result(item, self.grid_item))
        retrieved_item = self.model.get_result(item.id)
        self.assertTrue(item is retrieved_item)

        retrieved_item = self.model.get_result("thisidisprobablynotused")
        self.assertFalse(retrieved_item)

    def test_parent_should_be_provided(self):
        item = ThreeDiResultItem(self.result_path, "text")
        self.assertFalse(self.model.add_result(item, None))

    def test_grouped_results_keep_one_logical_grid(self):
        result = ThreeDiResultItem(self.result_path, "result")
        result.group_path = ["project", "files", "result"]
        result.layer_group = object()
        result.layer_ids = {"node": "result-layer-id"}

        second_result = ThreeDiResultItem("c:/test2/results_3di.nc", "result 2")
        second_result.group_path = ["project", "files", "result-2"]
        second_result.layer_group = object()
        second_result.layer_ids = {"node": "result-2-layer-id"}

        self.assertTrue(self.model.add_result(result, self.grid_item))
        self.assertTrue(self.model.add_result(second_result, self.grid_item))

        self.assertEqual(self.model.number_of_grids(), 1)
        self.assertEqual(self.model.number_of_results(), 2)
        self.assertIs(result.parent(), self.grid_item)
        self.assertIs(second_result.parent(), self.grid_item)
        self.assertEqual(result.get_layer_ids(), {"node": "result-layer-id"})
        self.assertEqual(second_result.get_layer_ids(), {"node": "result-2-layer-id"})

    def test_legacy_results_use_parent_grid_layers(self):
        self.grid_item.layer_ids = {"node": "grid-layer-id"}
        self.grid_item.layer_group = object()
        result = ThreeDiResultItem(self.result_path, "result")

        self.assertTrue(self.model.add_result(result, self.grid_item))

        self.assertIs(result.get_layer_ids(), self.grid_item.layer_ids)
        self.assertIs(result.get_layer_group(), self.grid_item.layer_group)

    def test_result_field_names_are_scoped_to_layer(self):
        result = ThreeDiResultItem(self.result_path, "result")
        result.group_path = ["files", "result"]
        result._result_field_names["result-layer-id"] = (
            "result_value",
            "initial_value",
        )
        second_result = ThreeDiResultItem("c:/test2/results_3di.nc", "result 2")
        second_result.group_path = ["files", "result-2"]
        second_result._result_field_names["second-layer-id"] = (
            "second_result_value",
            "second_initial_value",
        )

        self.assertTrue(self.model.add_result(result, self.grid_item))
        self.assertTrue(self.model.add_result(second_result, self.grid_item))

        self.assertEqual(
            self.model.get_result_field_names("result-layer-id"),
            {"result_value", "initial_value"},
        )
        self.assertEqual(
            self.model.get_result_field_names("second-layer-id"),
            {"second_result_value", "second_initial_value"},
        )
        self.assertEqual(self.model.get_result_field_names("unknown-layer-id"), set())
