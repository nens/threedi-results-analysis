# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtCore import Qt
from .watershed_analysis_dockwidget import WatershedAnalystDockWidget
from threedi_results_analysis.threedi_plugin_tool import ThreeDiPluginTool
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem, ThreeDiGridItem
from qgis.PyQt.QtXml import QDomElement, QDomDocument
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal
import logging

logger = logging.getLogger(__name__)


class ThreeDiWatershedAnalyst(ThreeDiPluginTool):
    closing = pyqtSignal(ThreeDiGridItem)

    def __init__(self, iface, model):
        super().__init__()
        self.iface = iface
        self.model = model

        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons", "icon_watershed.png")
        self.menu_text = "Watershed Tool"

        self.dock_widget = None
        self._active = False

    def read(self, xml_elem: QDomElement) -> bool:
        logger.error("READ")
        tool_node = xml_elem.firstChildElement("water_shed")
        if not tool_node:
            logger.error("Unable to read XML (no dedicated watershed node)")
            return False
        return True

    def write(self, doc: QDomDocument, xml_elem: QDomElement) -> bool:
        results_node = doc.createElement("water_shed")
        xml_elem.appendChild(results_node)

        if self.dock_widget.gq.grid_id is not None:
            layer_element = doc.createElement("layer")
            layer_element.setAttribute("id", self.dock_widget.gq.result_cell_layer.id())
            layer_element.setAttribute("table_name", "cell")
            results_node.appendChild(layer_element)

            layer_element = doc.createElement("layer")
            layer_element.setAttribute("id", self.dock_widget.gq.result_flowline_layer.id())
            layer_element.setAttribute("table_name", "flowline")
            results_node.appendChild(layer_element)

            layer_element = doc.createElement("layer")
            layer_element.setAttribute("id", self.dock_widget.gq.result_catchment_layer.id())
            layer_element.setAttribute("table_name", "catchment")
            results_node.appendChild(layer_element)

            # layer_element = doc.createElement("layer")
            # layer_element.setAttribute("id", self.dock_widget.gq.impervious_surface_layer.id())
            # layer_element.setAttribute("table_name", "surface")
            # results_node.appendChild(layer_element)
        return True

    @property
    def active(self):
        return self._active

    def on_unload(self):
        if self.dock_widget is not None:
            self.dock_widget.close()

    def on_close_child_widget(self, last_grid_item: ThreeDiGridItem):
        """Cleanup necessary items here when plugin dock widget is closed"""
        self.dock_widget.closingWidget.disconnect(self.on_close_child_widget)
        if last_grid_item:
            self.closing.emit(last_grid_item)
        self.dock_widget = None
        self._active = False

    def run(self):
        """Run method that loads and starts the tool"""
        if not self.active:
            if self.dock_widget is None:
                self.dock_widget = WatershedAnalystDockWidget(self.iface, self.model)
            self.dock_widget.closingWidget.connect(self.on_close_child_widget)
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

        self.dock_widget.show()
        self._active = True

    @pyqtSlot(ThreeDiResultItem)
    def result_added(self, result_item: ThreeDiResultItem) -> None:
        self.action_icon.setEnabled(self.model.number_of_results() > 0)
        if not self.active:
            return

        self.dock_widget.add_result(result_item)

    @pyqtSlot(ThreeDiResultItem)
    def result_removed(self, result_item: ThreeDiResultItem) -> None:
        self.action_icon.setEnabled(self.model.number_of_results() > 0)
        if not self.active:
            return

        self.dock_widget.remove_result(result_item)

    @pyqtSlot(ThreeDiGridItem)
    def grid_removed(self, grid_item: ThreeDiGridItem) -> None:
        if not self.active:
            return

        self.dock_widget.remove_grid(grid_item)

    @pyqtSlot(ThreeDiResultItem)
    def result_changed(self, result_item: ThreeDiResultItem) -> None:
        if not self.active:
            return

        self.dock_widget.change_result(result_item)
