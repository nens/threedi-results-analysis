# (c) Nelen & Schuurmans, see LICENSE.rst.
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtCore import Qt
from ThreeDiToolbox.tool_result_selection import result_selection_view
import logging

logger = logging.getLogger(__name__)

class ThreeDiResultSelection(QObject):
    """QGIS Plugin Implementation."""

    state_changed = pyqtSignal([str, str, list])
    tool_name = "result_selection"

    def __init__(self, iface, ts_datasources):

        super().__init__()
        self.iface = iface
        self.ts_datasources = ts_datasources

        self.icon_path = ":/plugins/ThreeDiToolbox/icons/icon_add_datasource.png"
        self.menu_text = u"Select 3Di results"

        self.is_active = False
        self.dialog = None

    def on_unload(self):
        # disconnects
        if self.dialog:
            self.dialog.close()

    def on_close_dialog(self):
        """Cleanup necessary items here when dialog is closed"""

        self.dialog.closingDialog.disconnect(self.on_close_dialog)
        self.dialog = None
        self.is_active = False

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.is_active:

            self.is_active = True
            if self.dialog is None:
                self.dialog = result_selection_view.ThreeDiResultSelectionWidget(
                    parent=None,
                    iface=self.iface,
                    ts_datasources=self.ts_datasources,
                    tool=self,
                )

            # connect to provide cleanup on closing of dockwidget
            self.dialog.closingDialog.connect(self.on_close_dialog)

            # show the widget
            self.dialog.show()
        else:
            self.dialog.setWindowState(
                self.dialog.windowState() & ~Qt.WindowMinimized | Qt.WindowActive
            )
            self.dialog.raise_()
