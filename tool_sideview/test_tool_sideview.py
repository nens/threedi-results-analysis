from ThreeDiToolbox.threedi_plugin import CommandBox
from ThreeDiToolbox.tool_result_selection.models import TimeseriesDatasourceModel
from ThreeDiToolbox.tool_sideview.sideview import ThreeDiSideView

import mock
import unittest


class TestThreeDiSideView(unittest.TestCase):
    def setUp(self):
        """test whether ThreeDiSideView can be instantiated"""
        iface = mock.Mock()
        ts_datasources = TimeseriesDatasourceModel()
        # tdi_root_tool = mock.Mock()
        tdi_root_tool = CommandBox(iface, ts_datasources)
        self.sideview = ThreeDiSideView(iface, tdi_root_tool)

    def test_icon_path_is_set(self):
        self.assertEqual(
            self.sideview.icon_path, ":/plugins/ThreeDiToolbox/icons/icon_route.png"
        )
