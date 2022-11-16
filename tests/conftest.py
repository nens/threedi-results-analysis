import pytest

from ThreeDiToolbox.tests.utilities import ensure_qgis_app_is_initialized


@pytest.fixture(autouse=True)
def qgis_app_initialized():
    ensure_qgis_app_is_initialized()
