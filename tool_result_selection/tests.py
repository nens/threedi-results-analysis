from ThreeDiToolbox.tool_result_selection import log_in_dialog


def test_log_in_dialog(qtbot):
    # Smoke test: just call it.
    result = log_in_dialog.LoginDialog()
