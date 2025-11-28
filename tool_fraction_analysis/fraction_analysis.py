from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtCore import Qt
from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem
from threedi_results_analysis.threedi_plugin_tool import ThreeDiPluginTool
from threedi_results_analysis.tool_fraction_analysis.fraction_dock_view import (
    FractionDockWidget,
)
from threedi_results_analysis.tool_fraction_analysis.fraction_utils import (
    has_wq_results,
)

import os
import qgis


class FractionAnalysis(ThreeDiPluginTool):

    def __init__(self, iface, model):
        super().__init__()

        self.iface = iface
        self.model = model
        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons", "icon_fat.svg")
        self.menu_text = "Fraction analysis tool"

        self.dock_widgets = []
        self.widget_nr = 0

    def on_unload(self):
        """
        on close of graph plugin
        """
        for widget in self.dock_widgets:
            widget.close()
            del widget
        self.dock_widgets = []

    def on_close_child_widget(self, widget_nr):
        """Cleanup necessary items here when plugin dockwidget is closed"""
        for i in range(0, len(self.dock_widgets)):
            widget = self.dock_widgets[i]
            if widget.nr == widget_nr:
                widget.closingWidget.disconnect(self.on_close_child_widget)
                del self.dock_widgets[i]
                return

    @pyqtSlot(ThreeDiResultItem)
    def result_added(self, result_item: ThreeDiResultItem):
        if has_wq_results(result_item):
            self.action_icon.setEnabled(True)

        for dock_widget in self.dock_widgets:
            dock_widget.result_added(result_item)

    @pyqtSlot(ThreeDiResultItem)
    def result_removed(self, removed_result: ThreeDiResultItem):
        for dock_widget in self.dock_widgets:
            dock_widget.result_removed(removed_result)

        for result_item in self.model.get_results(checked_only=False):
            if has_wq_results(result_item) and removed_result.id != result_item.id:
                self.action_icon.setEnabled(True)
                return
        self.action_icon.setEnabled(False)

    @pyqtSlot(ThreeDiResultItem)
    def result_changed(self, result_item: ThreeDiResultItem):
        for dock_widget in self.dock_widgets:
            dock_widget.result_changed(result_item)

    @pyqtSlot(ThreeDiGridItem)
    def grid_changed(self, grid_item: ThreeDiGridItem):
        for dock_widget in self.dock_widgets:
            dock_widget.grid_changed(grid_item)

    def run(self):
        new_widget = FractionDockWidget(
            iface=self.iface,
            nr=self.widget_nr,
            model=self.model,
        )
        self.dock_widgets.append(new_widget)

        self.widget_nr += 1

        # connect cleanup on closing of dockwidget
        new_widget.closingWidget.connect(self.on_close_child_widget)

        # show the dockwidget
        self.iface.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, new_widget)

        # make stack of graph widgets (instead of next to each other)
        if len(self.dock_widgets) > 1:
            window = qgis.core.QgsApplication.activeWindow()
            window.tabifyDockWidget(self.dock_widgets[0], new_widget)

        new_widget.show()
