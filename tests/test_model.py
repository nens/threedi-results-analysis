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


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.model = ThreeDiPluginModel()
        self.path = Path("c:/test/gridadmin.h5")

    def test_creation(self):
        item = ThreeDiGridItem("", "text")
        self.assertTrue(item)

    def test_adding(self):
        item = ThreeDiGridItem(self.path, "text")
        self.assertTrue(self.model.add_grid(item))

    def test_contains_path_check(self):
        item = ThreeDiGridItem(self.path, "text")
        self.assertTrue(self.model.add_grid(item))
        item2 = ThreeDiGridItem(self.path, "text")
        self.assertFalse(self.model.add_grid(item2))


class TestResult(unittest.TestCase):
    def setUp(self):
        self.model = ThreeDiPluginModel()
        self.path = Path("c:/test/results_3di.nc")

    def test_creation(self):
        item = ThreeDiResultItem(self.path, "text")
        self.assertTrue(item)
