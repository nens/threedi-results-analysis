"""Plugin initialization module

Qgis automatically calls an installed plugin's :py:func:`classFactory` to
actually load the plugin.

"""
import pyplugin_installer
from qgis.core import QgsSettings
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.utils import isPluginLoaded, startPlugin
from .utils.qlogging import setup_logging
from pathlib import Path
import platform
import faulthandler
import sys


def check_dependency_loader():
    required_plugin = "nens_dependency_loader"
    if not isPluginLoaded(required_plugin):
        if (
            QMessageBox.question(
                None,
                "N&S Dependency Loader",
                "N&S Dependency Loader is required, but not loaded. Would you like to load it?",
            )
            == QMessageBox.StandardButton.Yes
        ):
            try:  # This is basically what qgis.utils.loadPlugin() does, but that also shows errors, so we need to do it explicitly
                __import__(required_plugin)
                plugin_loadable = True
            except:  # NOQA
                plugin_loadable = False

            if plugin_loadable:
                if not startPlugin(required_plugin):
                    QMessageBox.warning(
                        None,
                        "N&S Dependency Loader",
                        "Unable to start N&S Dependency Loader, please enable the plugin manually",
                    )
                    return
            else:
                pyplugin_installer.instance().fetchAvailablePlugins(True)
                pyplugin_installer.instance().installPlugin(required_plugin)

            QgsSettings().setValue("/PythonPlugins/" + required_plugin, True)
            QgsSettings().remove("/PythonPlugins/watchDogTimestamp/" + required_plugin)


#: Handy constant for building relative paths.
PLUGIN_DIR = Path(__file__).parent


# sys.stderr is not available under Windows in Qgis, which is what the faulthandler
# uses by default.
if sys.stderr is not None and hasattr(sys.stderr, "fileno"):
    faulthandler.enable()


def enable_high_dpi_scaling():
    """Enable High DPI scaling."""
    from qgis.PyQt.QtCore import Qt
    from qgis.PyQt.QtWidgets import QApplication

    if hasattr(Qt, "HighDpiScaleFactorRoundingPolicy"):
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)


def classFactory(iface):
    """Return plugin class.

    In addition, we set up python logging (see
    :py:mod:`threedi_results_analysis.utils.qlogging`).

    args:
        iface (QgsInterface): A QGIS interface instance.

    """
    if platform.system() == "Windows":
        check_dependency_loader()
    setup_logging()
    enable_high_dpi_scaling()

    from .threedi_plugin import ThreeDiPlugin
    return ThreeDiPlugin(iface)
