
from pathlib import Path
from .dependencies import ensure_everything_installed, check_importability

import faulthandler
import sys


#: Handy constant for building relative paths.
PLUGIN_DIR = Path(__file__).parent


# sys.stderr is not available under Windows in Qgis, which is what the faulthandler
# uses by default.
if sys.stderr is not None and hasattr(sys.stderr, "fileno"):
    faulthandler.enable()
ensure_everything_installed()


def classFactory(iface):
    check_importability()
    from .plugin import ThreediResultsAnalysisPlugin
    return ThreediResultsAnalysisPlugin(iface)


