from ThreeDiToolbox.tool_commands.constants import COMMANDS_DIR
from ThreeDiToolbox.tool_commands.constants import modulename_packagename_mapping
from ThreeDiToolbox.tool_commands.custom_command_base import CustomCommandBase

import pytest


@pytest.mark.parametrize("method_name", ["run_it", "show_gui", "run"])
def test_signature(method_name):
    """The base class has three methods that raise NotImplementedError."""
    sample_object = CustomCommandBase()
    with pytest.raises(NotImplementedError):
        getattr(sample_object, method_name)()


def test_commands_modules_exists():
    for modulename, packagename in modulename_packagename_mapping.items():
        module_full_path = COMMANDS_DIR / packagename / modulename
        assert module_full_path.is_file()
