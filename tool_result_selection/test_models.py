from ThreeDiToolbox.datasource.threedi_results import ThreediResult
from ThreeDiToolbox.tool_result_selection.models import TimeseriesDatasourceModel
from ThreeDiToolbox.test.test_datasources import THREEDI_RESULTS_PATH

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
        tds = TimeseriesDatasourceModel()
        item = tds._create_item(**self.test_values)
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
        tds = TimeseriesDatasourceModel()
        item = tds._create_item(**test_values)
        ncds = item.datasource()
        self.assertTrue(isinstance(ncds, ThreediResult))
        self.assertTrue(ncds.datasource)
