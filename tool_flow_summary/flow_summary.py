# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QGridLayout
from qgis.PyQt.QtWidgets import QGroupBox
from qgis.PyQt.QtWidgets import QHBoxLayout
from qgis.PyQt.QtWidgets import QTableWidget
from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem
from threedi_results_analysis.threedi_plugin_tool import ThreeDiPluginTool


class FlowSummaryTool(ThreeDiPluginTool):

    def __init__(self, parent, iface):
        super().__init__(parent)
        self.iface = iface
        self.setup_ui()

    def setup_ui(self):
        self.icon_path = None  # No menu button
        self.main_widget = QGroupBox("Flow summary", self.parent())
        self.main_widget.setLayout(QGridLayout())
        self.table_widget = QTableWidget(3, 3, self.main_widget)
        self.main_widget.layout().addWidget(self.table_widget)
        self.parent().layout().addWidget(self.main_widget)
        self.main_widget.setEnabled(False)

    def on_unload(self):
        """
        on close of graph plugin
        """
        # for widget in self.dock_widgets:
        #     widget.close()  # TODO: delete as well?
        pass

    @pyqtSlot(ThreeDiResultItem)
    def result_added(self, result_item: ThreeDiResultItem):
        # # Assign a line pattern to this result (TODO: consider keeping track of the patterns
        # # in this plugin instead of storing in model?)
        # if not result_item._pattern:
        #     result_item._pattern = ThreeDiGraph.get_line_pattern(result_item=result_item)

        # self.action_icon.setEnabled(self.model.number_of_results() > 0)
        # for dock_widget in self.dock_widgets:
        #     dock_widget.result_added(result_item)
        pass

    @pyqtSlot(ThreeDiResultItem)
    def result_removed(self, result_item: ThreeDiResultItem):
        # self.action_icon.setEnabled(self.model.number_of_results() > 0)
        # for dock_widget in self.dock_widgets:
        #     dock_widget.result_removed(result_item)
        pass

    @pyqtSlot(ThreeDiResultItem)
    def result_changed(self, result_item: ThreeDiResultItem):
        # for dock_widget in self.dock_widgets:
        #     dock_widget.result_changed(result_item)
        pass

    @pyqtSlot(ThreeDiGridItem)
    def grid_changed(self, grid_item: ThreeDiGridItem):
        # for dock_widget in self.dock_widgets:
        #     dock_widget.grid_changed(grid_item)
        pass

    def run(self):
        """
        Run method that loads and starts the plugin (docked graph widget)
        """
        pass
        # # create the dockwidget
        # self.widget_nr += 1
        # new_widget = GraphDockWidget(
        #     iface=self.iface,
        #     nr=self.widget_nr,
        #     model=self.model,
        # )
        # self.dock_widgets.append(new_widget)

        # # connect cleanup on closing of dockwidget
        # new_widget.closingWidget.connect(self.on_close_child_widget)

        # # show the dockwidget
        # self.iface.addDockWidget(Qt.BottomDockWidgetArea, new_widget)

        # # make stack of graph widgets (instead of next to each other)
        # if len(self.dock_widgets) > 1:
        #     window = qgis.core.QgsApplication.activeWindow()
        #     window.tabifyDockWidget(self.dock_widgets[0], new_widget)

        # new_widget.show()
