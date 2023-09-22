"""Main pytest configuration file: fixtures + a qgis import mechanism fix.

Pytest automatically uses a ``conftest.py`` file, when found. Note that you
can have also have such files in subdirectories. The fixtures in this file
*stay* available there, except when you override them.

"""

from ThreeDiToolbox import PLUGIN_DIR

import os


def fix_import_mechanism():
    """Make pytest work in combination with qgis.

    We prevent Qgis from grabbing python's import mechanism. Qgis overrides
    something, which breaks pytest by causing an infinite import loop.

    """
    os.environ["QGIS_NO_OVERRIDE_IMPORT"] = "KEEPYOURPAWSOFF"


fix_import_mechanism()  # Needs to be called right away.

data_dir = PLUGIN_DIR / "tests" / "data"
bergermeer_dir = data_dir / "testmodel" / "v2_bergermeer"
