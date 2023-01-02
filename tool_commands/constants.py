from pathlib import Path


COMMANDS_DIR = Path(__file__).parent

# STEP_MODULENAME_MAPPING that contains the display names of commands (
# right side of QGIS screen) the nested values (e.g. 'raster checker')
# with space replaced by underscore are also packages (e.g. 'ThreeDiToolbox.tool_commands.raster_checker')
STEP_MODULENAME_MAPPING = {
    "Step 1 - Check data": [],
    "Step 2 - Convert and import data": [],
    "Step 3 - Modify schematisation": [
        "control structures",
    ],
    "Step 4 - Convert schematisation": [],
    "Step 5 - Post-process results": [],
}
