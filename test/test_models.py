from builtins import range
import unittest
from qgis.PyQt.QtCore import Qt

from ThreeDiToolbox.models.graph import LocationTimeseriesModel
from ThreeDiToolbox.models.datasources import (
    TimeseriesDatasourceModel,
    DataSourceLayerManager,
)
from ThreeDiToolbox.datasource.netcdf import NetcdfDataSource
from ThreeDiToolbox.test.test_datasources import (
    netcdf_datasource_path,
    result_data_is_available,
)


class TestLocationTimeseriesModelItem(unittest.TestCase):
    """ Test LocationTimeseriesModelItem created by LocationTimeseriesModel"""

    test_values = {
        "active": False,
        "color": [10, 20, 30],
        "object_id": 40,
        "object_name": "test_name",
    }

    def setUp(self):
        """Runs before each test."""
        pass

    def test_init_with_defaults(self):
        """test default values after initialisation"""
        model = LocationTimeseriesModel()
        item = model._create_item()

        self.assertEqual(item.active.value, True)
        self.assertEqual(item.object_id.value, None)

    def test_init_with_values(self):
        """test values after initialisation"""
        model = LocationTimeseriesModel()
        item = model._create_item(**self.test_values)

        self.assertEqual(item.active.value, self.test_values["active"])
        self.assertEqual(item.color.value, self.test_values["color"])
        self.assertEqual(item.object_id.value, self.test_values["object_id"])
        self.assertEqual(item.object_name.value, self.test_values["object_name"])

    def test_set_values(self):
        """test setting properties"""
        model = LocationTimeseriesModel(
            initial_data=[{"object_id": 1, "object_name": "object_1", "active": True}]
        )
        item = model.rows[0]

        item.active.value = False
        item.color.value = [30, 40, 50]
        item.object_name.value = "changed_name"

        self.assertEqual(item.active.value, False)
        self.assertEqual(item.color.value, [30, 40, 50])
        self.assertEqual(item.object_name.value, "changed_name")

    def test_get_field_settings(self):
        """test setting properties"""
        model = LocationTimeseriesModel()
        item = model._create_item(**self.test_values)

        self.assertEqual(item.active.default_value, True)
        self.assertEqual(item.active.column_width, 20)
        self.assertEqual(item.active.column_name, "")

        # todo: test column, get_fields
        # todo: test plots, get_timetables

    def tearDown(self):
        """Runs after each test."""
        pass


class TestLocationTimeseriesModel(unittest.TestCase):
    """ Test LocationTimeseriesModel functions"""

    datasource = "bla"

    initial_data = [
        {"object_id": 1, "object_name": "object_1", "active": True},
        {"object_id": 2, "object_name": "object_2", "active": True},
        {"object_id": 3, "object_name": "object_3", "active": False},
        {"object_id": 4, "object_name": "object_4", "active": False},
    ]

    additional_data = [
        {"object_id": 5, "object_name": "object_5", "active": True},
        {"object_id": 6, "object_name": "object_6", "active": True},
        {"object_id": 7, "object_name": "object_7", "active": False},
        {"object_id": 8, "object_name": "object_8", "active": False},
    ]

    def setUp(self):
        """Runs before each test."""
        pass

    def test_init(self):
        """test default values after initialisation"""
        collection = LocationTimeseriesModel(datasource=self.datasource)

        self.assertEqual(collection.rowCount(), 0)
        self.assertEqual(collection.columnCount(), 7)

        headers = [collection.headerData(i) for i in range(0, collection.columnCount())]

        self.assertListEqual(
            headers,
            # display column names
            ["", "", "id", "name", "object_type", "hover", "file_path"],
        )

    def test_init_with_initial_data(self):
        """test default values after initialisation"""
        collection = LocationTimeseriesModel(
            datasource=self.datasource, initial_data=self.initial_data
        )

        self.assertEqual(collection.rowCount(), 4)
        self.assertEqual(collection.columnCount(), 7)
        self.assertEqual(
            collection.data(collection.createIndex(0, 0, None), role=Qt.DisplayRole),
            None,
        )

        self.assertEqual(
            collection.data(collection.createIndex(0, 1, None), role=Qt.DisplayRole),
            None,
        )

        self.assertEqual(
            collection.data(collection.createIndex(0, 2, None), role=Qt.DisplayRole), 1
        )

        self.assertEqual(
            collection.data(collection.createIndex(0, 3, None), role=Qt.DisplayRole),
            "object_1",
        )

    def test_insert_remove_rows(self):
        """ test insertRows and removeRows function"""

        collection = LocationTimeseriesModel(
            datasource=self.datasource, initial_data=self.initial_data
        )

        collection.insertRows(self.additional_data)

        self.assertEqual(collection.rowCount(), 8)
        self.assertEqual(collection.columnCount(), 7)

        self.assertEqual(
            collection.data(collection.createIndex(7, 3, None), role=Qt.DisplayRole),
            "object_8",
        )

        collection.removeRows(2, 4)

        self.assertEqual(collection.rowCount(), 4)

        self.assertEqual(
            collection.data(collection.createIndex(1, 3, None), role=Qt.DisplayRole),
            "object_2",
        )

        self.assertEqual(
            collection.data(collection.createIndex(2, 3, None), role=Qt.DisplayRole),
            "object_7",
        )

    def test_set_get_data(self):
        """ test insertRows and removeRows function"""

        collection = LocationTimeseriesModel(
            datasource=self.datasource, initial_data=self.initial_data
        )

        # first test checkField
        collection.setData(
            collection.createIndex(0, 0), Qt.Unchecked, Qt.CheckStateRole
        )

        self.assertEqual(collection.rows[0].active.value, False)
        self.assertEqual(
            collection.data(collection.createIndex(0, 0, None), role=Qt.CheckStateRole),
            Qt.Unchecked,
        )

        collection.setData(collection.createIndex(0, 0), Qt.Checked, Qt.CheckStateRole)

        self.assertEqual(collection.rows[0].active.value, True)
        self.assertEqual(
            collection.data(collection.createIndex(0, 0, None), role=Qt.CheckStateRole),
            Qt.Checked,
        )

        # test valueField
        collection.setData(collection.createIndex(0, 2), 8, Qt.DisplayRole)

        self.assertEqual(collection.rows[0].object_id.value, 8)
        self.assertEqual(
            collection.data(collection.createIndex(0, 2, None), role=Qt.DisplayRole), 8
        )

    def tearDown(self):
        """Runs after each test."""
        pass


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

    @unittest.skip("want to work only with netcdf-groundwater, not netcdf")
    def test_datasource(self):
        """Test the datasource() method with netcdf file."""
        test_values = {
            "active": False,
            "name": "jaa",
            "file_path": netcdf_datasource_path,
            "type": "netcdf",
            "pattern": "line pattern?",
        }
        tds = TimeseriesDatasourceModel()
        item = tds._create_item(**test_values)
        ncds = item.datasource()
        self.assertTrue(isinstance(ncds, NetcdfDataSource))
        self.assertTrue(ncds.ds)


class TestDataSourceLayerManager(unittest.TestCase):
    def test_smoke(self):
        DataSourceLayerManager("a type", "/tmp/to/some/where")

    def test_datasource_failure(self):
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
