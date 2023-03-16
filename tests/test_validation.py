from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel, ThreeDiGridItem
from threedi_results_analysis.threedi_plugin_model_validation import ThreeDiPluginModelValidator
import unittest
from pathlib import Path
from mock import patch


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

    @patch("threedi_results_analysis.threedi_plugin_model_validation.ThreeDiResultItem")
    @patch("threedi_results_analysis.threedi_plugin_model_validation.h5py.File")
    def test_missing_threedicore_function(self, test_h5, test_mock):
        test_h5.return_value.attrs = ["no_threedicore_version"]
        test_mock.return_value.path.name = "results_3di.nc"

        validator = ThreeDiPluginModelValidator(self.model)
        with patch.object(validator, "result_invalid") as result_invalid:
            self.assertFalse(validator.validate_result("c:/test/results_3di.nc", self.grid_item))
            result_invalid.emit.assert_called_once()
            result_invalid.emit.assert_called_once_with(test_mock.return_value, self.grid_item)
