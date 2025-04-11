from qgis.core import QgsWkbTypes
from qgis.gui import QgsMapToolIdentify
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QActionGroup
from qgis.PyQt.QtWidgets import QDockWidget
from qgis.PyQt.QtWidgets import QHBoxLayout
from qgis.PyQt.QtWidgets import QMenu
from qgis.PyQt.QtWidgets import QSizePolicy
from qgis.PyQt.QtWidgets import QSpacerItem
from qgis.PyQt.QtWidgets import QTabWidget
from qgis.PyQt.QtWidgets import QToolButton
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.PyQt.QtWidgets import QWidget
from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem
from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem
from threedi_results_analysis.tool_fraction_analysis.fraction_graph_view import (
    FractionWidget,
)
from threedi_results_analysis.tool_fraction_analysis.fraction_map_tool import (
    AddNodeCellMapTool,
)
from threedi_results_analysis.utils.user_messages import messagebar_message
from threedi_results_analysis.utils.utils import generate_parameter_config
from typing import List

import logging


logger = logging.getLogger(__name__)

class FractionDockWidget(QDockWidget):
    closingWidget = pyqtSignal(int)

    def __init__(self, iface, nr, model: ThreeDiPluginModel):
        super().__init__()

        self.iface = iface
        self.nr = nr
        self.model = model

        self.setup_ui()

        parameter_config = self._get_active_parameter_config()

        # add graph widgets
        self.fraction_widget = FractionWidget(
            self,
            self.model,
            parameter_config["h"],
            "Nodes && cells",
            QgsWkbTypes.Point,
        )
        
        self.graphTabWidget.addTab(self.fraction_widget, self.fraction_widget.name)

        # add listeners
        self.addNodeCellButton.clicked.connect(self.add_node_cell_button_clicked)

        # add map tools
        self.map_tool_add_node_cell = AddNodeCellMapTool(
            widget=self, canvas=self.iface.mapCanvas(),
        )
        self.map_tool_add_node_cell.setButton(self.addNodeCellButton)
        self.map_tool_add_node_cell.setCursor(Qt.CrossCursor)

        # In case this dock widget becomes (in)visible, we disable the route tools
        self.visibilityChanged.connect(self.unset_map_tools)

    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """
        self.addFlowlinePumpButton.clicked.disconnect(self.add_flowline_pump_button_clicked)
        self.addNodeCellButton.clicked.disconnect(self.add_node_cell_button_clicked)

        self.map_tool_add_flowline_pump = None
        self.map_tool_add_node_cell = None

        # self.q_graph_widget.close()

    def closeEvent(self, event):
        """
        overwrite of QDockWidget class to emit signal
        :param event: QEvent
        """
        self.on_close()
        self.closingWidget.emit(self.nr)
        event.accept()

    def _get_active_parameter_config(self, result_item_ignored: ThreeDiResultItem = None):
        """
        Generates a parameter dict based on results, takes union of parameters from results.
        """
        q_vars = []
        h_vars = []

        for result in self.model.get_results(checked_only=False):
            if result is result_item_ignored:  # about to be deleted
                continue

            threedi_result = result.threedi_result
            available_subgrid_vars = threedi_result.available_subgrid_map_vars
            available_agg_vars = threedi_result.available_aggregation_vars[:]  # a copy
            available_wq_vars = threedi_result.available_water_quality_vars[:]  # a copy
            available_sca_vars = threedi_result.available_structure_control_actions_vars[:]  # a copy
            if not available_agg_vars:
                messagebar_message("Warning", "No aggregation netCDF was found.", level=1, duration=5)

            parameter_config = generate_parameter_config(
                available_subgrid_vars, agg_vars=available_agg_vars, wq_vars=available_wq_vars, sca_vars=available_sca_vars
            )

            def _union(a: List, b: List):
                if not a:
                    return b

                for param in b:
                    # Check whether a contains param with same name, if so, don't add
                    if not [x for x in a if x["name"] == param["name"]]:
                        a.append(param)

                return a

            q_vars = _union(q_vars, parameter_config["q"])
            h_vars = _union(h_vars, parameter_config["h"])

        return {"q": q_vars, "h": h_vars}

    def result_added(self, _: ThreeDiResultItem):
        parameter_config = self._get_active_parameter_config()
        # self.q_graph_widget.set_parameter_list(parameter_config["q"])
        # self.h_graph_widget.set_parameter_list(parameter_config["h"])

    def result_removed(self, result_item: ThreeDiResultItem):
        parameter_config = self._get_active_parameter_config(result_item)
        # self.q_graph_widget.result_removed(result_item)
        # self.h_graph_widget.result_removed(result_item)
        # self.q_graph_widget.set_parameter_list(parameter_config["q"])
        # self.h_graph_widget.set_parameter_list(parameter_config["h"])

    def result_changed(self, _: ThreeDiResultItem):
        # self.q_graph_widget.refresh_table()
        # self.h_graph_widget.refresh_table()
        pass

    def grid_changed(self, result_item: ThreeDiGridItem):
        # self.q_graph_widget.refresh_table()
        # self.h_graph_widget.refresh_table()
        pass

    def setup_ui(self):

        self.setObjectName("dock_widget")
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.dockWidgetContent = QWidget(self)
        self.dockWidgetContent.setObjectName("dockWidgetContent")

        self.mainVLayout = QVBoxLayout(self.dockWidgetContent)
        self.dockWidgetContent.setLayout(self.mainVLayout)

        self.buttonBarHLayout = QHBoxLayout(self)

        self.buttonBarHLayout.setSpacing(10)


        selection_node_cell_menu = QMenu(self)
        action_group = QActionGroup(self)
        action_group.setExclusive(True)
        self.node_single_pick = selection_node_cell_menu.addAction("Pick single node/cell")
        self.node_single_pick.setCheckable(True)
        self.node_single_pick.setChecked(True)
        self.node_single_pick.toggled.connect(self._changeNodeCellSelectionMode)
        action_group.addAction(self.node_single_pick)
        selected_pick = selection_node_cell_menu.addAction("Add all selected nodes/cells")
        selected_pick.setCheckable(True)
        action_group.addAction(selected_pick)

        self.addNodeCellButton = QToolButton(parent=self.dockWidgetContent)
        self.addNodeCellButton.setText("Pick nodes/cells")
        self.addNodeCellButton.setCheckable(True)
        self.addNodeCellButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.addNodeCellButton.setMenu(selection_node_cell_menu)
        self.buttonBarHLayout.addWidget(self.addNodeCellButton)

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.buttonBarHLayout.addItem(spacerItem)

        self.mainVLayout.addItem(self.buttonBarHLayout)

        # add tabWidget for graphWidgets
        self.graphTabWidget = QTabWidget(self.dockWidgetContent)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(6)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graphTabWidget.sizePolicy().hasHeightForWidth()
        )
        self.graphTabWidget.setSizePolicy(sizePolicy)
        self.graphTabWidget.setObjectName("graphTabWidget")
        self.mainVLayout.addWidget(self.graphTabWidget)

        # add dockwidget
        self.setWidget(self.dockWidgetContent)
        self.setWindowTitle("3Di Time series plot %i" % self.nr)


    def _changeNodeCellSelectionMode(self, single_pick_selected: bool) -> None:
        if not single_pick_selected:
            if self.iface.mapCanvas().mapTool() is self.map_tool_add_node_cell:
                self.iface.mapCanvas().unsetMapTool(self.map_tool_add_node_cell)
            self.addNodeCellButton.setCheckable(False)
            self.addNodeCellButton.setText("Add nodes/cells")
        else:
            self.addNodeCellButton.setCheckable(True)
            self.addNodeCellButton.setText("Pick nodes/cells")


    def add_node_cell_button_clicked(self):
        if self.node_single_pick.isChecked():
            self.iface.mapCanvas().setMapTool(self.map_tool_add_node_cell)
        else:
            current_layer = self.iface.mapCanvas().currentLayer()

            if not current_layer or current_layer.objectName() not in ['node', 'cell']:
                logger.error("Select features from node or cell layer first.")
                return

            self.add_results([QgsMapToolIdentify.IdentifyResult(current_layer, f, dict()) for f in current_layer.selectedFeatures()], feature_type="node_or_cell")

    def unset_map_tools(self):
        if self.iface.mapCanvas().mapTool() is self.map_tool_add_node_cell:
            self.iface.mapCanvas().unsetMapTool(self.map_tool_add_node_cell)
        elif self.iface.mapCanvas().mapTool() is self.map_tool_add_flowline_pump:
            self.iface.mapCanvas().unsetMapTool(self.map_tool_add_flowline_pump)

    def add_results(self, results, feature_type, single_feature_per_layer=False):
        """
        Add results for features of specific types.
        """
        if feature_type == "node_or_cell":
            layer_keys = ['node', 'cell']
            graph_widget = self.h_graph_widget
        item = self.model.invisibleRootItem()

        relevant_grid_layer_ids = []
        for layer_key in layer_keys:
            for i in range(item.rowCount()):
                if layer_key in item.child(i).layer_ids:
                    relevant_grid_layer_ids.append(item.child(i).layer_ids[layer_key])

        layers_added = set()
        for result in results:
            layer_id = result.mLayer.id()
            if layer_id not in relevant_grid_layer_ids:
                continue
            if single_feature_per_layer and layer_id in layers_added:
                continue
            graph_widget.add_objects(result.mLayer, [result.mFeature])
            layers_added.add(layer_id)

        if layers_added:
            tab_index = self.graphTabWidget.indexOf(graph_widget)
            self.graphTabWidget.setCurrentIndex(tab_index)
            graph_widget.graph_plot.plotItem.vb.menu.viewAll.triggered.emit()