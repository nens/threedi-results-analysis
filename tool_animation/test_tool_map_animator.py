from ThreeDiToolbox.threedi_toolbox import CommandBox
from ThreeDiToolbox.tool_result_selection.models import TimeseriesDatasourceModel

import mock
import unittest


class TestMapAnimator(unittest.TestCase):
    def setUp(self):
        """test whether ThreeDiAnimation can be instantiated """
        ts_datasources = TimeseriesDatasourceModel()
        self.iface = mock.Mock()
        self.tdi_root_tool = CommandBox(self.iface, ts_datasources)
        self.toolbar_animation = self.iface.addToolBar("ThreeDiAnimation")
        self.toolbar_animation.setObjectName("ThreeDiAnimation")
