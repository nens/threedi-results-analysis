from ThreeDiToolbox.tool_result_selection import log_in_dialog
from ThreeDiToolbox.tool_result_selection import result_selection


def test_log_in_dialog(qtbot):
    # Smoke test: just call it.
    log_in_dialog.LoginDialog()


def test_get_valid_filename():
    assert "johns_portrait_in_2004.jpg" == result_selection.get_valid_filename(
        "john's portrait in 2004.jpg"
    )
