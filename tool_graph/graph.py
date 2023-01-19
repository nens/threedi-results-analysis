from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtCore import QObject
from ThreeDiToolbox.tool_graph.graph_view import GraphDockWidget
from ThreeDiToolbox.threedi_plugin_model import ThreeDiResultItem
from qgis.PyQt.QtCore import pyqtSlot
import qgis
import os


class ThreeDiGraph(QObject):

    def __init__(self, iface, model):
        QObject.__init__(self)

        self.iface = iface
        self.model = model

        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons", "icon_graph.png")
        self.menu_text = "Show 3Di results in Graph"

        self.dock_widgets = []
        self.widget_nr = 0

    def on_unload(self):
        """
        on close of graph plugin
        """
        for widget in self.dock_widgets:
            widget.close()  # TODO: delete as well?

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

    @pyqtSlot(ThreeDiResultItem)
    def result_added(self, _: ThreeDiResultItem):
        self.action_icon.setEnabled(self.model.number_of_results() > 0)

    @pyqtSlot(ThreeDiResultItem)
    def result_removed(self, _: ThreeDiResultItem):
        self.action_icon.setEnabled(self.model.number_of_results() > 0)

    @pyqtSlot(ThreeDiResultItem)
    def result_activated(self, _: ThreeDiResultItem):
        for dock_widget in self.dock_widgets:
            dock_widget.on_active_ts_datasource_change()

    @pyqtSlot(ThreeDiResultItem)
    def result_deactivated(self, _: ThreeDiResultItem):
        for dock_widget in self.dock_widgets:
            dock_widget.on_active_ts_datasource_change()

    def run(self):
        """
        Run method that loads and starts the plugin (docked graph widget)
        """
        # create the dockwidget
        self.widget_nr += 1
        new_widget = GraphDockWidget(
            iface=self.iface,
            nr=self.widget_nr,
            model=self.model,
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

        new_widget.show()
