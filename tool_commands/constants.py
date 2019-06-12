from collections import namedtuple
from pathlib import Path


COMMANDS_DIR = Path(__file__).parent

command_step = namedtuple("command_step", ["step_id", "display_name"])
STEP1 = command_step(1, "Step 1 - Check data")
STEP2 = command_step(2, "Step 2 - Convert and import data")
STEP3 = command_step(3, "Step 3 - Modify schematisation")
STEP4 = command_step(4, "Step 4 - Convert schematisation")
STEP5 = command_step(5, "Step 5 - Post-process results")
COMMAND_STEPS = [STEP1, STEP2, STEP3, STEP4, STEP5]
command_path = namedtuple("command_path", ["step_id", "command_name", "package_name"])
CMD_RASTER_CHECKER = command_path(1, "raster_checker.py", "raster_checker")
CMD_SCHEMATISATION_CHECKER = command_path(
    1, "schematisation_checker.py", "schematisation_checker"
)
CMD_IMPORT_SUFHYD = command_path(2, "import_sufhyd.py", "import_sufhyd")
CMD_CONTROL_STRUCTURES = command_path(3, "control_structures.py", "control_structures")
CMD_GUESS_INDICATORS = command_path(3, "guess_indicators.py", "guess_indicators")
CMD_CREATE_BREACH_LOCATIONS = command_path(
    3, "create_breach_locations.py", "create_breach_locations"
)
CMD_ADD_CONNECTED_POINTS = command_path(
    3, "add_connected_points.py", "add_connected_points"
)
CMD_PREDICT_CALC_POINTS = command_path(
    3, "predict_calc_points.py", "predict_calc_points"
)
COMMANDS = [
    CMD_RASTER_CHECKER,
    CMD_SCHEMATISATION_CHECKER,
    CMD_IMPORT_SUFHYD,
    CMD_CONTROL_STRUCTURES,
    CMD_GUESS_INDICATORS,
    CMD_CREATE_BREACH_LOCATIONS,
    CMD_ADD_CONNECTED_POINTS,
    CMD_PREDICT_CALC_POINTS,
]
