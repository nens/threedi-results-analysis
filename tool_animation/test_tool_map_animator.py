from ThreeDiToolbox.threedi_plugin import CommandBox
from ThreeDiToolbox.tool_result_selection.models import TimeseriesDatasourceModel

import mock


def test_smoke():
    """Test whether ThreeDiAnimation can be instantiated.

    TODO: this was the setUp() of an otherwise empty unittest class.  It
    doesn't look like it actually tests something. Especially the
    toolbar_animation is a mock, so calling that has no use.

    """
    ts_datasources = TimeseriesDatasourceModel()
    iface = mock.Mock()
    tdi_root_tool = CommandBox(iface, ts_datasources)
    toolbar_animation = iface.addToolBar("ThreeDiAnimation")
    toolbar_animation.setObjectName("ThreeDiAnimation")
    assert tdi_root_tool
