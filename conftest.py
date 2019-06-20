# Pytest configuration file. The sole purpose is to prevent Qgis from grabbing
# python's import mechanism (which breaks pytest).
from ThreeDiToolbox import PLUGIN_DIR

import os
import pytest
import shutil


# Make pytest work in combination with qgis.
os.environ["QGIS_NO_OVERRIDE_IMPORT"] = "KEEPYOURPAWSOFF"


data_dir = PLUGIN_DIR / "tests" / "data"
bergermeer_dir = data_dir / "testmodel" / "v2_bergermeer"
results_3di_path = bergermeer_dir / "results_3di.nc"


@pytest.fixture()
def threedi_result():
    """Return a instance of ThreediResult

    The instance contains result data of the model 'v2_bergermeer'. It contains
    both results and aggregate result data.
    """
    # Late import, otherwise we get circular import errors.
    from ThreeDiToolbox.datasource.threedi_results import ThreediResult

    return ThreediResult(file_path=results_3di_path)


@pytest.fixture()
def ts_datasources(tmp_path):
    """Return ts_datasources with one threedi_result (the one above) preloaded.

    Note that the test data is first copied, so it is safe to modify.

    """
    # Late import, otherwise we get circular import errors.
    from ThreeDiToolbox.tool_result_selection.models import TimeseriesDatasourceModel

    shutil.copytree(bergermeer_dir, tmp_path / "v2_bergermeer")
    copied_results_3di_path = tmp_path / "v2_bergermeer" / "results_3di.nc"
    result = TimeseriesDatasourceModel()
    test_values = {
        "active": False,
        "name": "bergermeer v2 from main conftest.py",
        "file_path": copied_results_3di_path,
        "type": "netcdf-groundwater",
    }
    result.insertRows([test_values])
    return result
