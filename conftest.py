# Pytest configuration file. The sole purpose is to prevent Qgis from grabbing
# python's import mechanism (which breaks pytest).
from pathlib import Path
from ThreeDiToolbox.datasource.threedi_results import ThreediResult

import os
import pytest


# Make pytest work in combination with qgis.
os.environ["QGIS_NO_OVERRIDE_IMPORT"] = "KEEPYOURPAWSOFF"


plugin_dir = Path(__file__).parent
data_dir = plugin_dir / "tests" / "data"
bergermeer_dir = data_dir / "testmodel" / "v2_bergermeer"

gridadmin_path = bergermeer_dir / "gridadmin.h5"
results_3di_path = bergermeer_dir / "results_3di.nc"
aggregate_results_3di_path = bergermeer_dir / "aggregate_results_3di.nc"


@pytest.fixture()
def threedi_result():
    """Return a instance of ThreediResult

    The instance contains result data of the model 'v2_bergermeer'. It contains
    both results and aggregate result data.
    """
    return ThreediResult(file_path=results_3di_path)
