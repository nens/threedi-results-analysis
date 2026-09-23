from unittest.mock import Mock

from threedi_results_analysis import threedi_plugin
from threedi_results_analysis.threedi_plugin import ThreeDiPlugin


def test_smoke():
    # We just import it. There used to be some import errors
    assert threedi_plugin


def test_load_result_forwards_group_path():
    plugin = ThreeDiPlugin(None)
    plugin.validator = Mock()

    plugin.load_result(
        "c:/test/results_3di.nc",
        "c:/test/gridadmin.h5",
        "project",
        ["project", "files", "result"],
    )

    plugin.validator.validate_result_grid.assert_called_once_with(
        "c:/test/results_3di.nc",
        "c:/test/gridadmin.h5",
        project="project",
        group_path=["project", "files", "result"],
    )
