# (c) Nelen & Schuurmans, see LICENSE.rst.
"""
Miscellaneous tools.
"""
from qgis.PyQt.QtCore import pyqtSignal
from threedi_results_analysis.utils.qlogging import FileHandler
from threedi_results_analysis.utils.user_messages import pop_up_info
from threedi_results_analysis.threedi_plugin_tool import ThreeDiPluginTool

import logging
import os


logger = logging.getLogger(__name__)


class ShowLogfile(ThreeDiPluginTool):
    """Show link to the logfile."""

    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.icon_path = os.path.join(os.path.dirname(__file__), "icons", "icon_logfile.png")
        # ^^^ logo: LGPL, made by Oxygen Team, see
        # http://www.iconarchive.com/show/oxygen-icons-by-oxygen-icons.org/
        self.menu_text = "Show Rana Results Analysis log file (for debugging purposes)"

    def run(self):
        """Show dialog with a simple clickable link to the logfile.

        Later on, we could also show the entire logfile inside the dialog. Or
        suggest an email. The clickable link is OK for now.

        Note: such a link does not work within the development docker.

        """
        title = "Show Rana Results Analysis log file (for debugging purposes)"
        location = FileHandler.get_filename()
        message = "Log file location: <a href='file:///%s'>%s</a>" % (location, location)
        pop_up_info(message, title, self.iface.mainWindow())


class ToggleResultsManager(ThreeDiPluginTool):
    """Add Rana logo and about info."""
    triggered = pyqtSignal()

    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.icon_path = os.path.join(os.path.dirname(__file__), "icons", "icon_panel.svg")
        self.menu_text = "Simulation Results Manager"

    def run(self):
        """Shows dialog with version information."""
        self.triggered.emit()
