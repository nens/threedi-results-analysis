from ThreeDiToolbox import misc_tools
import mock


def test_show_logfile():
    iface = mock.Mock()
    show_logfile_action = misc_tools.ShowLogfile(iface)
    with mock.patch.object(misc_tools, "pop_up_info") as mock_pop_up_info:
        show_logfile_action.run()
        args, kwargs = mock_pop_up_info.call_args
        assert "threedi-qgis-log.txt" in args[0]
