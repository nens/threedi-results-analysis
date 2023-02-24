from qgis.PyQt.QtCore import Qt, QObject
from threedi_results_analysis.tool_sideview.sideview_view import SideViewDockWidget
from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem
from qgis.PyQt.QtCore import pyqtSlot
import qgis
import os


class ThreeDiSideView(QObject):
    """QGIS Plugin Implementation."""

    def __init__(self, iface, tdi_root_tool, model):
        QObject.__init__(self)

        self.iface = iface
        self.tdi_root_tool = tdi_root_tool
        self.model = model

        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons", "icon_route.png")
        self.menu_text = u"Show sideview of 3Di model with results"

        self.dock_widgets = []
        self.widget_nr = 0
        self._active = False

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, activate):
        self._active = activate

    def on_unload(self):
        """
        on close of graph plugin
        """
        for widget in self.dock_widgets:
            widget.close()

    @pyqtSlot(ThreeDiGridItem)
    def grid_added(self, grid_item: ThreeDiGridItem):
        self.action_icon.setEnabled(self.model.number_of_grids() > 0)

    @pyqtSlot(ThreeDiGridItem)
    def grid_removed(self, grid_item: ThreeDiGridItem):
        self.action_icon.setEnabled(self.model.number_of_grids() > 0)

    def on_close_child_widget(self, widget_nr):
        """Cleanup necessary items here when plugin dockwidget is closed"""
        nr = None

        # find widget based on nr
        for i in range(0, len(self.dock_widgets)):
            widget = self.dock_widgets[i]
            if widget.nr == widget_nr:
                nr = i

        # close widget
        if nr is not None:
            widget = self.dock_widgets[nr]
            widget.closingWidget.disconnect(self.on_close_child_widget)

            del self.dock_widgets[nr]

        self.active = False

    def run(self):
        """
        Run method that loads and starts the plugin (docked graph widget)
        """
        # create the dockwidget
        self.widget_nr += 1
        new_widget = SideViewDockWidget(
            self.iface,
            parent_class=self,
            nr=self.widget_nr,
            tdi_root_tool=self.tdi_root_tool,
        )
        self.dock_widgets.append(new_widget)

        # connect cleanup on closing of dockwidget
        new_widget.closingWidget.connect(self.on_close_child_widget)

        # show the dockwidget
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, new_widget)

        # make stack of graph widgets (instead of next to each other)
        if len(self.dock_widgets) > 1:
            window = qgis.core.QgsApplication.activeWindow()
            window.tabifyDockWidget(self.dock_widgets[0], new_widget)

        self.active = True

        new_widget.show()
