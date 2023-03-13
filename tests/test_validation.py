from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel, ThreeDiGridItem
from threedi_results_analysis.threedi_plugin_model_validation import ThreeDiPluginModelValidator
import unittest
from pathlib import Path


class TestModelValidator(unittest.TestCase):
    def setUp(self):
        self.model = ThreeDiPluginModel()
        self.grid_item = ThreeDiGridItem(Path("c:/test/gridadmin.h5"), "text")

    def test_creation(self):
        validator = ThreeDiPluginModelValidator(self.model)
        self.assertTrue(validator)

    def test_invalid_result_filename(self):
        validator = ThreeDiPluginModelValidator(self.model)
        self.assertFalse(validator.validate_result("c:/test/incorrectfilename_3di.nc", self.grid_item))
