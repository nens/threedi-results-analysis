from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel, ThreeDiGridItem, ThreeDiResultItem
from threedi_results_analysis.threedi_plugin_model_validation import ThreeDiPluginModelValidator
from threedi_results_analysis.tests.utilities import ensure_qgis_app_is_initialized
import unittest
from pathlib import Path
from mock import patch


@patch("threedi_results_analysis.threedi_plugin_model_validation.ThreeDiResultItem")
@patch("threedi_results_analysis.threedi_plugin_model_validation.h5py.File")
class TestResultValidation(unittest.TestCase):
    def setUp(self):
        ensure_qgis_app_is_initialized()
        self.model = ThreeDiPluginModel()
        self.grid_item = ThreeDiGridItem(Path("c:/test/gridadmin.h5"), "text")
        self.model.add_grid(self.grid_item)

    def test_creation(self, *args):
        validator = ThreeDiPluginModelValidator(self.model)
        self.assertTrue(validator)

    def test_invalid_result_filename(self, test_h5, result_item_mock):
        validator = ThreeDiPluginModelValidator(self.model)
        with patch.object(validator, "result_invalid") as result_invalid:
            self.assertFalse(validator._validate_result("c:/test/incorrectfilename_3di.nc", self.grid_item))
            result_invalid.emit.assert_called_once_with(result_item_mock.return_value, self.grid_item)

    def test_missing_threedicore_function(self, test_h5, result_item_mock):
        test_h5.return_value.attrs = ["no_threedicore_version"]
        result_item_mock.return_value.path.name = "results_3di.nc"

        validator = ThreeDiPluginModelValidator(self.model)
        with patch.object(validator, "result_invalid") as result_invalid:
            self.assertFalse(validator._validate_result("c:/test/results_3di.nc", self.grid_item))
            result_invalid.emit.assert_called_once_with(result_item_mock.return_value, self.grid_item)

    def test_unknown_slug_function(self, test_h5, result_item_mock):
        test_h5.return_value.attrs = {"threedicore_version": "", "model_slug": "result_slug".encode()}
        result_item_mock.return_value.path.name = "results_3di.nc"

        validator = ThreeDiPluginModelValidator(self.model)
        with patch.object(validator, "result_invalid") as result_invalid, patch.object(
                ThreeDiPluginModelValidator, "get_grid_slug") as grid_slug:
            grid_slug.return_value = "bla_slug"
            self.assertFalse(validator._validate_result("c:/test/results_3di.nc", self.grid_item))
            result_invalid.emit.assert_called_once_with(result_item_mock.return_value, self.grid_item)

    def test_result_item_is_valid(self, test_h5, result_item_mock):
        test_h5.return_value.attrs = {"threedicore_version": "", "model_slug": "result_slug".encode()}
        result_item_mock.return_value.path.name = "results_3di.nc"

        validator = ThreeDiPluginModelValidator(self.model)
        with patch.object(validator, "result_valid") as result_valid, patch.object(
                ThreeDiPluginModelValidator, "get_grid_slug") as grid_slug:
            grid_slug.return_value = "result_slug"
            self.assertTrue(validator._validate_result("c:/test/results_3di.nc", self.grid_item))
            result_valid.emit.assert_called_once_with(result_item_mock.return_value, self.grid_item)

    def test_result_item_is_reparented(self, test_h5, result_item_mock):
        test_h5.return_value.attrs = {"threedicore_version": "", "model_slug": "result_slug".encode()}
        result_item_mock.return_value.path.name = "results_3di.nc"

        # add a second grid which will have the right slug
        right_grid_item = ThreeDiGridItem(Path("c:/otherfolder/gridadmin.h5"), "text2")
        self.model.add_grid(right_grid_item)

        validator = ThreeDiPluginModelValidator(self.model)
        with patch.object(validator, "result_valid") as result_valid, patch.object(
                ThreeDiPluginModelValidator, "get_grid_slug") as grid_slug:
            grid_slug.side_effect = ["bla", "bla", "result_slug"]
            self.assertTrue(validator._validate_result("c:/test/results_3di.nc", self.grid_item))
            result_valid.emit.assert_called_once_with(result_item_mock.return_value, right_grid_item)

    def test_result_item_is_already_present(self, test_h5, result_item_mock):
        test_h5.return_value.attrs = {"threedicore_version": "", "model_slug": "result_slug".encode()}
        result_item_mock.return_value.path.name = "results_3di.nc"

        self.model.add_result(ThreeDiResultItem(Path("c:/test/results_3di.nc"), "text"), self.grid_item)

        validator = ThreeDiPluginModelValidator(self.model)
        with patch.object(validator, "result_invalid") as result_invalid, patch.object(
                ThreeDiPluginModelValidator, "get_grid_slug") as grid_slug:
            grid_slug.return_value = "result_slug"
            self.assertFalse(validator._validate_result("c:/test/results_3di.nc", self.grid_item))
            result_invalid.emit.assert_called_once_with(result_item_mock.return_value, self.grid_item)


class TestGridValidator(unittest.TestCase):
    def setUp(self):
        ensure_qgis_app_is_initialized()
        self.model = ThreeDiPluginModel()

    def test_grid_is_valid(self):
        validator = ThreeDiPluginModelValidator(self.model)
        with patch.object(validator, "grid_valid") as grid_valid:
            new_grid_item = validator.validate_grid("c:/test/gridadmin.h5")
            grid_valid.emit.assert_called_once_with(new_grid_item)

    def test_grid_already_present(self):
        grid_item = ThreeDiGridItem(Path("c:/test/gridadmin.h5"), "text")
        self.model.add_grid(grid_item)

        validator = ThreeDiPluginModelValidator(self.model)
        with patch.object(validator, "grid_invalid") as grid_invalid:
            existing_grid = validator.validate_grid("c:/test/gridadmin.h5")
            grid_invalid.emit.assert_called_once()
            self.assertTrue(existing_grid is grid_item)

    def test_grid_with_same_slug_as_result_is_retrieved_instead_of_created(self):
        # add a first grid which will have the right slug, this should be reused
        wrong_grid_item = ThreeDiGridItem(Path("c:/thisfolder/gridadmin.h5"), "text2")
        self.model.add_grid(wrong_grid_item)

        right_grid_item = ThreeDiGridItem(Path("c:/otherfolder/gridadmin.h5"), "text2")
        self.model.add_grid(right_grid_item)

        validator = ThreeDiPluginModelValidator(self.model)
        with patch.object(validator, "grid_valid") as grid_valid, patch.object(
                ThreeDiPluginModelValidator, "get_grid_slug") as grid_slug:
            grid_slug.side_effect = ["bah45", "result_slug"]
            selected_grid = validator.validate_grid("c:/test/gridadmin.h5", "result_slug")

            self.assertTrue(selected_grid is right_grid_item)
            grid_valid.emit.assert_not_called()

    def test_grid_with_same_slug_as_grid_is_retrieved(self):
        # add a first grid which will have the right slug
        right_grid_item = ThreeDiGridItem(Path("c:/otherfolder/gridadmin.h5"), "text2")
        self.model.add_grid(right_grid_item)

        validator = ThreeDiPluginModelValidator(self.model)
        with patch.object(validator, "grid_valid") as grid_valid, patch.object(
                ThreeDiPluginModelValidator, "get_grid_slug") as grid_slug:
            grid_slug.side_effect = ["result_slug", "result_slug"]
            self.assertTrue(validator.validate_grid("c:/test/gridadmin.h5") is right_grid_item)
            grid_valid.emit.assert_not_called()

    def test_grid_with_different_slug_is_created(self):
        # add a first grid which will have the right slug
        right_grid_item = ThreeDiGridItem(Path("c:/otherfolder/gridadmin.h5"), "text2")
        self.model.add_grid(right_grid_item)

        validator = ThreeDiPluginModelValidator(self.model)
        with patch.object(validator, "grid_valid") as grid_valid, patch.object(
                ThreeDiPluginModelValidator, "get_grid_slug") as grid_slug:
            grid_slug.side_effect = ["result_slug", "bla"]
            created_grid = validator.validate_grid("c:/test/gridadmin.h5")
            self.assertTrue(created_grid is not right_grid_item)
            grid_valid.emit.assert_called_once_with(created_grid)
