"""Plugin initialization module

Qgis automatically calls an installed plugin's :py:func:`classFactory` to
actually load the plugin.

Note: beforehand we call our dependency mechanism (see
:doc:`linked_external_dependencies_readme`) to ensure all dependencies are
there.

"""
from pathlib import Path
from ThreeDiToolbox import dependencies

import faulthandler
import sys


#: Handy constant for building relative paths.
PLUGIN_DIR = Path(__file__).parent


# sys.stderr is not available under Windows in Qgis, which is what the faulthandler
# uses by default.
if sys.stderr is not None:
    faulthandler.enable()
dependencies.ensure_everything_installed()


def classFactory(iface):
    """Return ThreeDiToolbox class from file ThreeDiToolbox.

    In addition, we set up python logging (see
    :py:mod:`ThreeDiToolbox.utils.qlogging`).

    args:
        iface (QgsInterface): A QGIS interface instance.

    """
    from ThreeDiToolbox.utils.qlogging import setup_logging

    setup_logging()
    dependencies.check_importability()

    from .threedi_plugin import ThreeDiPlugin

    return ThreeDiPlugin(iface)
