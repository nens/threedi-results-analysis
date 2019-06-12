from ThreeDiToolbox.tool_commands.command_model import CommandModel
from ThreeDiToolbox.tool_commands.constants import COMMANDS
from ThreeDiToolbox.tool_commands.constants import COMMANDS_DIR
from ThreeDiToolbox.tool_commands.custom_command_base import CustomCommandBase

import pytest


@pytest.mark.parametrize("method_name", ["run_it", "show_gui", "run"])
def test_signature(method_name):
    """The base class has three methods that raise NotImplementedError."""
    sample_object = CustomCommandBase()
    with pytest.raises(NotImplementedError):
        getattr(sample_object, method_name)()


def test_get_command_structure():
    commandboxmodel = CommandModel()
    command_structure = commandboxmodel.get_command_structure()
    expected = {
        "Step 1 - Check data": {
            "raster_checker.py": None,
            "schematisation_checker.py": None,
        },
        "Step 2 - Convert and import data": {"import_sufhyd.py": None},
        "Step 3 - Modify schematisation": {
            "control_structures.py": None,
            "guess_indicators.py": None,
            "create_breach_locations.py": None,
            "add_connected_points.py": None,
            "predict_calc_points.py": None,
        },
        "Step 4 - Convert schematisation": {},
        "Step 5 - Post-process results": {},
    }
    assert command_structure == expected


def test_command_modules_exists():
    for command in COMMANDS:
        module = COMMANDS_DIR / command.package_name / command.command_name
        assert module.is_file()


def test_raster_checker_can_be_called():
    # TODO: create a test for each command and try to call run() method of command
    pass
