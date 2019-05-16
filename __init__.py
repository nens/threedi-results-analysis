"""This script initializes the plugin, making it known to QGIS."""
import faulthandler


faulthandler.enable()


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ThreeDiToolbox class from file ThreeDiToolbox.

    :param iface: QgsInterface. A QGIS interface instance.
    """
    from .threedi_tools import ThreeDiTools
    from .utils.qlogging import setup_logging
    from .dependencies import try_to_import_dependencies

    setup_logging()
    try_to_import_dependencies()
    return ThreeDiTools(iface)
