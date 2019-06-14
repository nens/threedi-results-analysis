from ThreeDiToolbox.tool_commands.command_box import CommandBox
from ThreeDiToolbox.tool_commands.constants import STEP_MODULENAME_MAPPING
from ThreeDiToolbox.tool_commands.custom_command_base import CustomCommandBase

import pytest


@pytest.mark.parametrize("method_name", ["run_it", "show_gui", "run"])
def test_signature(method_name):
    """The base class has three methods that raise NotImplementedError."""
    sample_object = CustomCommandBase()
    with pytest.raises(NotImplementedError):
        getattr(sample_object, method_name)()

import mock


def test_command_modules_exist():
    iface_mock = mock.MagicMock()
    ts_datasources_mock = mock.MagicMock()
    commandbox = CommandBox(iface_mock, ts_datasources_mock)
    for step, display_names in STEP_MODULENAME_MAPPING.items():
        for display_name in display_names:
            module_full_path = commandbox.get_module_path(display_name)
            assert module_full_path.is_file(), "command cannot be found"
