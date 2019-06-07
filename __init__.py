"""This script initializes the plugin, making it known to QGIS."""
from ThreeDiToolbox import dependencies

import faulthandler


faulthandler.enable()
dependencies.ensure_everything_installed()


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ThreeDiToolbox class from file ThreeDiToolbox.

    :param iface: QgsInterface. A QGIS interface instance.
    """
    from .utils.qlogging import setup_logging

    setup_logging()
    dependencies.check_importability()

    from .threedi_tools import ThreeDiPlugin

    return ThreeDiPlugin(iface)
