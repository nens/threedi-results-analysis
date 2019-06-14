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


def test_command_modules_exist():
    for step, display_names in STEP_MODULENAME_MAPPING.items():
        for display_name in display_names:
            module_full_path = CommandBox.get_module_path(display_name)
            assert module_full_path.is_file(), "command cannot be found"
