from ThreeDiToolbox.datasource.threedi_results import ThreediResult
from ThreeDiToolbox.tests.test_datasources import THREEDI_RESULTS_PATH
from ThreeDiToolbox.tool_result_selection import models

import unittest


class TestTimeseriesDatasourceModel(unittest.TestCase):
    test_values = {
        "active": False,
        "name": "jaa",
        "file_path": "/dev/random/",
        "type": "a type",
        "pattern": "line pattern?",
    }

    def test_init_with_values(self):
        ts_datasources = models.TimeseriesDatasourceModel()
        item = ts_datasources._create_item(**self.test_values)
        for k, v in list(self.test_values.items()):
            itemvalue = getattr(item, k).value
            self.assertEqual(itemvalue, v)

    def test_datasource_threedi_results(self):
        """Test the datasource() method with netcdf file."""
        test_values = {
            "active": False,
            "name": "jaa",
            "file_path": THREEDI_RESULTS_PATH,
            "type": "netcdf-groundwater",
            "pattern": "line pattern?",
        }
        ts_datasources = models.TimeseriesDatasourceModel()
        item = ts_datasources._create_item(**test_values)
        ncds = item.datasource()
        self.assertTrue(isinstance(ncds, ThreediResult))
        self.assertTrue(ncds.datasource)


def test_downloadable_result_model():
    # Smoke test, just initialize it.
    models.DownloadableResultModel()
