from ThreeDiToolbox.datasource.threedi_results import ThreediResult
from ThreeDiToolbox.tests.test_datasources import THREEDI_RESULTS_PATH
from ThreeDiToolbox.tool_result_selection import models

import mock
import pytest
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
    # Smoke test, just initialize a few.
    downloadable_results = models.DownloadableResultModel()
    for i in range(8):
        test_values = {
            "name": "name-%s" % i,
            "size_mebibytes": i,
            "url": "http://reinout/%s" % i,
            "results": "",
        }
        downloadable_results.insertRows([test_values])
    assert downloadable_results.rowCount() == 8


def test_get_line_pattern():
    ts_datasources = models.TimeseriesDatasourceModel()
    for i in range(8):
        test_values = {
            "active": False,
            "name": "jaa",
            "file_path": THREEDI_RESULTS_PATH,
            "type": "netcdf-groundwater",
            # Note: pattern is not set, we want the default.
        }
        ts_datasources.insertRows([test_values])
    first_pattern = ts_datasources.rows[0].pattern.value
    second_pattern = ts_datasources.rows[1].pattern.value
    last_pattern = ts_datasources.rows[-1].pattern.value
    # Different styles, if possible:
    assert first_pattern != second_pattern
    # If they're all used up, use the first one as fallback.
    assert first_pattern == last_pattern


def test_pop_up_unkown_datasource_type():
    with mock.patch(
        "ThreeDiToolbox.tool_result_selection.models.pop_up_info"
    ) as mock_pop_up_info:
        models.pop_up_unkown_datasource_type()
        assert mock_pop_up_info.called


def test_value_with_change_signal():
    class Person(object):
        age_changed_signal = mock.Mock()
        age = models.ValueWithChangeSignal("age_changed_signal", "age_changed")

    person = Person()
    # No default value, so None:
    assert person.age is None
    person.age = 42
    # The setter/getter mechanism works:
    assert person.age == 42
    # And yes, we emitted the signal:
    assert Person.age_changed_signal.emit.called


def test_datasource_layer_manager_init():
    with mock.patch(
        "ThreeDiToolbox.tool_result_selection.models.pop_up_unkown_datasource_type"
    ) as mock_pop_up:
        with pytest.raises(AssertionError):
            models.DatasourceLayerManager("unknown_type", "")
            assert mock_pop_up.called
