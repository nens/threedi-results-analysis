from ThreeDiToolbox.tool_result_selection import login_dialog
from ThreeDiToolbox.tool_result_selection import result_downloader
from ThreeDiToolbox.tool_result_selection import result_selection
from ThreeDiToolbox.tool_result_selection.models import TimeseriesDatasourceModel

import mock


def test_login_dialog(qtbot):
    # Smoke test: just call it.
    login_dialog.LoginDialog()


def test_get_valid_filename():
    assert "johns_portrait_in_2004.jpg" == result_selection.get_valid_filename(
        "john's portrait in 2004.jpg"
    )


def test_download_result_model():
    # Smoke test, just initialize it.
    result_downloader.DownloadResultModel()


def test_result_selection_tool_init():
    iface = mock.Mock()
    ts_datasources = TimeseriesDatasourceModel()
    result_selection_tool = result_selection.ThreeDiResultSelection(
        iface, ts_datasources
    )
    assert "icon_add_datasource.png" in result_selection_tool.icon_path
