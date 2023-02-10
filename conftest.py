"""Main pytest configuration file: fixtures + a qgis import mechanism fix.

Pytest automatically uses a ``conftest.py`` file, when found. Note that you
can have also have such files in subdirectories. The fixtures in this file
*stay* available there, except when you override them.

"""

from threedi_results_analysis import PLUGIN_DIR

import os
import pytest
import shutil


def fix_import_mechanism():
    """Make pytest work in combination with qgis.

    We prevent Qgis from grabbing python's import mechanism. Qgis overrides
    something, which breaks pytest by causing an infinite import loop.

    """
    os.environ["QGIS_NO_OVERRIDE_IMPORT"] = "KEEPYOURPAWSOFF"


fix_import_mechanism()  # Needs to be called right away.

data_dir = PLUGIN_DIR / "tests" / "data"
bergermeer_dir = data_dir / "testmodel" / "v2_bergermeer"
results_3di_path = bergermeer_dir / "results_3di.nc"


@pytest.fixture()
def threedi_result():
    """Fixture: return a instance of ThreediResult

    The instance contains result data of the model 'v2_bergermeer'. It
    contains both results and aggregate result data.

    """
    # Late import, otherwise we get circular import errors.
    from threedi_results_analysis.datasource.threedi_results import ThreediResult

    return ThreediResult(file_path=results_3di_path)


@pytest.fixture()
def ts_datasources(tmp_path):
    """Fixture: return ts_datasources with one threedi_result (the one above) preloaded.

    Note that the test data is first copied, so it is safe to modify.

    """
    # Late import, otherwise we get circular import errors.
    from threedi_results_analysis.tool_result_selection.models import TimeseriesDatasourceModel

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
