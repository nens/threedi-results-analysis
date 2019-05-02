"""This script initializes the plugin, making it known to QGIS."""
import sys
import os

import faulthandler

faulthandler.enable()


sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "external")
)


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ThreeDiToolbox class from file ThreeDiToolbox.

    :param iface: QgsInterface. A QGIS interface instance.
    """
    from .threedi_tools import ThreeDiTools
    from .utils.qlogging import setup_logging
    from .dependencies import try_to_import_dependencies

    import sys; sys.path[0:0] = ['/pycharm/pycharm-debug-py3k.egg', ]; import pydevd; pydevd.settrace('10.90.16.48', port=4445, stdoutToServer=True, stderrToServer=True, suspend=False)


    setup_logging()
    try_to_import_dependencies()
    return ThreeDiTools(iface)
