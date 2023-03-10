from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel, ThreeDiGridItem, ThreeDiResultItem
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


class TestResult(unittest.TestCase):
    def setUp(self):
        self.result_path = Path("c:/test/results_3di.nc")

        self.model = ThreeDiPluginModel()
        self.grid_item = ThreeDiGridItem("c:/test/gridadmin.h5", "text")
        self.assertTrue(self.model.add_grid(self.grid_item))

    def test_creation(self):
        item = ThreeDiResultItem(self.result_path, "text")
        self.assertTrue(item)

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

    def test_parent_should_be_provided(self):
        item = ThreeDiResultItem(self.result_path, "text")
        self.assertFalse(self.model.add_result(item, None))
