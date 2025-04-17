from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtWidgets import QDockWidget
from qgis.PyQt.QtWidgets import QHBoxLayout
from qgis.PyQt.QtWidgets import QLabel
from qgis.PyQt.QtWidgets import QSizePolicy
from qgis.PyQt.QtWidgets import QSpacerItem
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

        self.map_tool_add_node_cell = AddNodeCellMapTool(
            widget=self, canvas=self.iface.mapCanvas(),
        )
        self.map_tool_add_node_cell.setButton(self.addNodeCellButton)
        self.map_tool_add_node_cell.setCursor(Qt.CrossCursor)

        # In case this dock widget becomes (in)visible, we disable the map tools
        self.visibilityChanged.connect(self.unset_map_tools)

    def on_close(self):
        self.addNodeCellButton.clicked.disconnect(self.add_node_cell_button_clicked)
        self.map_tool_add_node_cell = None

    def closeEvent(self, event):
        self.on_close()
        self.closingWidget.emit(self.nr)
        event.accept()

    def result_added(self, result: ThreeDiResultItem):
        currentIndex = self.simulationCombobox.currentIndex()
        self.simulationCombobox.addItem(f"{result.text()} ({result.parent().text()})", result.id)
        self.simulationCombobox.setCurrentIndex(currentIndex)

    def result_removed(self, result_item: ThreeDiResultItem):
        pass

    def result_changed(self, _: ThreeDiResultItem):
        pass

    def grid_changed(self, result_item: ThreeDiGridItem):
        pass

    def current_result(self):
        current_index = self.simulationCombobox.currentIndex()                
        if current_index == -1:
            return None
        
        item_id = self.simulationCombobox.itemData(current_index)
        return self.model.get_result(item_id)

    def result_selected(self, result_index: int):
        # Because we connected the "activated" signal instead of the "currentIndexChanged" signal,
        # programmatically changing the index does not emit a signal
        self.simulationCombobox.setCurrentIndex(result_index)
        item_id = self.simulationCombobox.itemData(result_index)
        result = self.model.get_result(item_id)
        self.setWindowTitle(f"3Di Substance comparison {self.nr}: {result.text()} ({result.parent().text()})")

    def setup_ui(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.dockWidgetContent = QWidget(self)
        self.mainVLayout = QVBoxLayout(self.dockWidgetContent)
        self.dockWidgetContent.setLayout(self.mainVLayout)
        self.buttonBarHLayout = QHBoxLayout(self)
        self.addNodeCellButton = QToolButton(self.dockWidgetContent)
        self.addNodeCellButton.setText("Pick node/cell")
        self.addNodeCellButton.setCheckable(True)
        self.addNodeCellButton.clicked.connect(self.add_node_cell_button_clicked)
        self.buttonBarHLayout.addWidget(self.addNodeCellButton)

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.buttonBarHLayout.addItem(spacerItem)
        result_label = QLabel("Simulation result:", self.dockWidgetContent)
        self.buttonBarHLayout.addWidget(result_label)
        self.simulationCombobox = QComboBox(self.dockWidgetContent)
        self.buttonBarHLayout.addWidget(self.simulationCombobox)

        self.mainVLayout.addItem(self.buttonBarHLayout)
        self.mainVLayout.setContentsMargins(0, 10, 0, 10)

        # populate the combobox, with results, but select None
        for result in self.model.get_results(checked_only=False):
            self.simulationCombobox.addItem(f"{result.text()} ({result.parent().text()})", result.id)
        self.simulationCombobox.setCurrentIndex(-1)
        self.simulationCombobox.activated.connect(self.result_selected)
        
        self.fraction_widget = FractionWidget(
            self.dockWidgetContent,
            self.model,
            self.iface
        )
        self.mainVLayout.addWidget(self.fraction_widget)
        self.setWidget(self.dockWidgetContent)
        self.setWindowTitle("3Di Substance comparison %i" % self.nr)

    def add_node_cell_button_clicked(self):
        self.iface.mapCanvas().setMapTool(self.map_tool_add_node_cell)

    def unset_map_tools(self):
        if self.iface.mapCanvas().mapTool() is self.map_tool_add_node_cell:
            self.iface.mapCanvas().unsetMapTool(self.map_tool_add_node_cell)

    def add_results(self, results):
        current_result = self.current_result()        
        if current_result == None:
            logger.warning("First select a result")
            return
        
        for result in results:
            # Check whether the selected layer belongs to the selected grid/result AND is a node/cell layer
            for layer_type, layer_id in current_result.parent().layer_ids.items():
                if layer_type in ['node', 'cell'] and layer_id == result.mLayer.id():
                    self.fraction_widget.set_fraction(result.mLayer, result.mFeature)
                    self.fraction_widget.fraction_plot.plotItem.vb.menu.viewAll.triggered.emit()
                    return  # Only add a single item
