from ThreeDiToolbox.threedi_plugin import About
from ThreeDiToolbox.tool_sideview.sideview import ThreeDiSideView

import mock
import unittest


class TestThreeDiSideView(unittest.TestCase):
    def setUp(self):
        """test whether ThreeDiSideView can be instantiated"""
        iface = mock.Mock()
        # tdi_root_tool = mock.Mock()
        tdi_root_tool = About(iface)
        self.sideview = ThreeDiSideView(iface, tdi_root_tool)

    def test_icon_path_is_set(self):
        self.assertEqual(
            self.sideview.icon_path, "/root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/ThreeDiToolbox/icons/icon_route.png"
        )
