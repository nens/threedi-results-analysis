from ThreeDiToolbox.threedi_plugin import CommandBox
from ThreeDiToolbox.tool_result_selection.models import TimeseriesDatasourceModel

import mock


def test_smoke():
    """Test whether ThreeDiAnimation can be instantiated """
    ts_datasources = TimeseriesDatasourceModel()
    iface = mock.Mock()
    tdi_root_tool = CommandBox(iface, ts_datasources)
    toolbar_animation = iface.addToolBar("ThreeDiAnimation")
    toolbar_animation.setObjectName("ThreeDiAnimation")
