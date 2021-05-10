from ThreeDiToolbox.datasource.threedi_results import ThreediResult
from ThreeDiToolbox.tests.test_init import TEST_DATA_DIR
from ThreeDiToolbox.tests.utilities import ensure_qgis_app_is_initialized
from ThreeDiToolbox.tool_result_selection import models

import mock
import pytest


THREEDI_RESULTS_PATH = TEST_DATA_DIR / "testmodel" / "v2_bergermeer" / "results_3di.nc"


def test_ts_datasource_model_threedi_results():
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
    threedi_result = item.threedi_result()
    assert isinstance(threedi_result, ThreediResult)
    assert threedi_result.datasource


def test_ts_datasource_model_init_with_values():
    test_values = {
        "active": False,
        "name": "jaa",
        "file_path": "/dev/random/",
        "type": "a type",
        "pattern": "line pattern?",
    }
    ts_datasources = models.TimeseriesDatasourceModel()
    item = ts_datasources._create_item(**test_values)
    for k, v in list(test_values.items()):
        itemvalue = getattr(item, k).value
        assert itemvalue == v


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


def test_datasource_layer_helper_datasource_dir():
    datasource_layer_helper = models.DatasourceLayerHelper("/home/pietje/iets.sqlite")
    assert str(datasource_layer_helper.datasource_dir) == "/home/pietje"


def test_datasource_layer_helper_get_result_layers():
    datasource_layer_helper = models.DatasourceLayerHelper(THREEDI_RESULTS_PATH)
    # Just call it, check if we get three layers.
    results = datasource_layer_helper.get_result_layers(progress_bar=mock.Mock())
    assert len(results) == 4


def test_datasource_layer_helper_get_result_layers_validation():
    ensure_qgis_app_is_initialized()
    datasource_layer_helper = models.DatasourceLayerHelper(THREEDI_RESULTS_PATH)
    results = datasource_layer_helper.get_result_layers(progress_bar=mock.Mock())
    lines = results[0]
    nodes = results[1]
    cells = results[2]
    pumps = results[3]
    assert lines.featureCount() == 31915
    assert nodes.isValid()
    assert pumps.name() == "pumplines"


def test_ts_datasource_model_field_models():
    """Smoke test of the three helper methods on the Fields object."""
    test_values = {
        "active": False,
        "name": "jaa",
        "file_path": THREEDI_RESULTS_PATH,
        "type": "netcdf-groundwater",
        "pattern": "line pattern?",
    }
    ts_datasources = models.TimeseriesDatasourceModel()
    ts_datasources.insertRows([test_values])
    assert ts_datasources.rows[0].threedi_result()
    assert ts_datasources.rows[0].sqlite_gridadmin_filepath()
    with mock.patch("ThreeDiToolbox.tool_result_selection.models.StatusProgressBar"):
        assert ts_datasources.rows[0].get_result_layers()


def test_ts_datasource_model_barfs_on_unkown_type():
    """Smoke test of the three helper methods on the Fields object."""
    test_values = {
        "active": False,
        "name": "jaa",
        "file_path": THREEDI_RESULTS_PATH,
        "type": "reinout-shoppinglist",
        "pattern": "line pattern?",
    }
    ts_datasources = models.TimeseriesDatasourceModel()
    ts_datasources.insertRows([test_values])
    with mock.patch(
        "ThreeDiToolbox.tool_result_selection.models.pop_up_info"
    ) as mock_pop_up_info:
        with pytest.raises(AssertionError):
            # Barfs on the unknown datasource_type
            ts_datasources.rows[0].datasource_layer_helper
            assert mock_pop_up_info.called


def test_ts_datasource_model_reset():
    test_values = {
        "active": False,
        "name": "jaa",
        "file_path": THREEDI_RESULTS_PATH,
        "type": "netcdf-groundwater",
        "pattern": "line pattern?",
    }
    ts_datasources = models.TimeseriesDatasourceModel()
    ts_datasources.insertRows([test_values])
    assert ts_datasources.rowCount() == 1
    ts_datasources.reset()
    assert ts_datasources.rowCount() == 0
