from pathlib import Path


COMMANDS_DIR = Path(__file__).parent

modulename_packagename_mapping = {
    "raster_checker.py": "raster_checker",
    "schematisation_checker.py": "schematisation_checker",
    "import_sufhyd.py": "import_sufhyd",
    "control_structures.py": "control_structures",
    "guess_indicators.py": "guess_indicators",
    "create_breach_locations.py": "create_breach_locations",
    "add_connected_points.py": "add_connected_points",
    "predict_calc_points.py": "predict_calc_points",
}

step_modulename_mapping = {
    "Step 1 - Check data": ["raster_checker.py", "schematisation_checker.py"],
    "Step 2 - Convert and import data": ["import_sufhyd.py"],
    "Step 3 - Modify schematisation": [
        "control_structures.py",
        "guess_indicators.py",
        "create_breach_locations.py",
        "add_connected_points.py",
        "predict_calc_points.py",
    ],
    "Step 4 - Convert schematisation": [],
    "Step 5 - Post-process results": [],
}
