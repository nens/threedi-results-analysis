from ThreeDiToolbox.datasource.threedi_results import ThreediResult
from ThreeDiToolbox.models.datasources import DataSourceLayerManager
from ThreeDiToolbox.models.datasources import TimeseriesDatasourceModel
from ThreeDiToolbox.test.test_datasources import THREEDI_RESULTS_PATH

import mock
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

    def test_datasource_layer_manager_smoke(self):
        """Smoke test the ``datasource_layer_manager()`` method."""
        tds = TimeseriesDatasourceModel()
        item = tds._create_item(**self.test_values)
        setattr(item, "_datasource_layer_manager", "yo")
        self.assertEqual(item.datasource_layer_manager(), "yo")

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


class TestDataSourceLayerManager(unittest.TestCase):
    def test_smoke(self):
        DataSourceLayerManager("a type", "/tmp/to/some/where")

    @mock.patch("ThreeDiToolbox.models.datasources.pop_up_unkown_datasource_type")
    def test_datasource_failure(self, mock_pop_up):
        dlm = DataSourceLayerManager("a type", "/tmp/to/some/where")
        with self.assertRaises(KeyError):
            dlm.datasource

    def test_datasource_success(self):
        dlm = DataSourceLayerManager("a type", "/tmp/to/some/where")
        setattr(dlm, "_datasource", "FOO")
        self.assertEqual(dlm.datasource, "FOO")


"""

models:

Base Model Class

Field behavior and functions insertRows, data, flags:
- Check set and get FIELD_VALUE
- Check set and get FIELD_CHECKBOX
- Check set and get FIELD_COLOR

init -->
- check default field settings are set correctly
- check data is set correclty on init
- check if errors are raised on missing inputs?

other functions-->
- setData
- data
- removeRows
- getHeader
- flags

test signals-->
- update
- remove
- etc.

combination of functions
- init, remove, add, update, remove

native QAbstractModelFunctions (what are they doing, set on NotImplemented?

Functions:




"""

if __name__ == "__main__":
    unittest.main()
