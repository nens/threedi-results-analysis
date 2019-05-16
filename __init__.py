"""This script initializes the plugin, making it known to QGIS."""
import faulthandler


faulthandler.enable()


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ThreeDiToolbox class from file ThreeDiToolbox.

    :param iface: QgsInterface. A QGIS interface instance.
    """
    from .utils.qlogging import setup_logging
    from .dependencies import ensure_everything_installed

    setup_logging()
    ensure_everything_installed()

    from .threedi_tools import ThreeDiTools
    return ThreeDiTools(iface)
