from ThreeDiToolbox.models.datasources import TimeseriesDatasourceModel
from ThreeDiToolbox.threedi_tools import CommandBox

import mock
import unittest


class TestMapAnimator(unittest.TestCase):
    def setUp(self):
        """test whether ThreeDiAnimation can be instantiated """
        ts_datasource = TimeseriesDatasourceModel()
        self.iface = mock.Mock()
        self.tdi_root_tool = CommandBox(self.iface, ts_datasource)
        self.toolbar_animation = self.iface.addToolBar("ThreeDiAnimation")
        self.toolbar_animation.setObjectName("ThreeDiAnimation")
