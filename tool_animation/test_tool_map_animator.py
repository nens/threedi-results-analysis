from ThreeDiToolbox.models.datasources import TimeseriesDatasourceModel
from ThreeDiToolbox.tool_animation.map_animator import MapAnimator
from ThreeDiToolbox.threedi_tools import ThreeDiToolbox

import mock
import unittest


class TestMapAnimator(unittest.TestCase):
    def setUp(self):
        """test whether ThreeDiResultSelection can be instantiated """
        ts_datasource = TimeseriesDatasourceModel()
        self.iface = mock.Mock()
        self.tdi_root_tool = ThreeDiToolbox(self.iface, ts_datasource)
        self.toolbar_animation = self.iface.addToolBar(u"ThreeDiAnimation")
        self.toolbar_animation.setObjectName(u"ThreeDiAnimation")

    @mock.patch("ThreeDiToolbox.tool_animation.map_animator.QWidget")
    def test_instanciate_map_animator(self, qwidget_mock):
        """ parent class of MapAnimator is QWidget that we mock here """
        self.map_animator_widget = MapAnimator(
            self.toolbar_animation, self.iface, self.tdi_root_tool
        )
