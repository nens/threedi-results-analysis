from pathlib import Path


COMMANDS_DIR = Path(__file__).parent

# STEP_MODULENAME_MAPPING that contains the display names of commands (
# right sight of QGIS screen) the nested values (e.g. 'schematisation checker')
# with space replaced by underscore are also packages (e.g. 'ThreeDiToolbox.tool_commands.schematisation_checker')
STEP_MODULENAME_MAPPING = {
    "Step 1 - Check data": ["schematisation checker"],
    "Step 2 - Convert and import data": ["import sufhyd"],
    "Step 3 - Modify schematisation": [
        "control structures",
        "guess indicators",
        "create breach locations",
        "add connected points",
        "predict calc points",
    ],
    "Step 4 - Convert schematisation": [],
    "Step 5 - Post-process results": [],
}
