from collections import namedtuple
from pathlib import Path

"""
All commands can be devided into 5 steps. COMMAND_STRUCTURE is a nested dict that
contains """

COMMAND_STRUCTURE = {
    # stepname <-- step names will be displayed in tree
    "Step 1 - Check data": {
        # module name:  package name <-- module names will be displayed in tree
        "raster_checker.py": "raster_checker",
        "schematisation_checker.py": "schematisation_checker",
    },
    "Step 2 - Convert and import data": {"import_sufhyd.py": "import_sufhyd"},
    "Step 3 - Modify schematisation": {
        "control_structures.py": "control_structures",
        "guess_indicators.py": "guess_indicators",
        "create_breach_locations.py": "create_breach_locations",
        "add_connected_points.py": "add_connected_points",
        "predict_calc_points.py": "predict_calc_points",
    },
    "Step 4 - Convert schematisation": {},
    "Step 5 - Post-process results": {},
}

COMMANDS_DIR = Path(__file__).parent
