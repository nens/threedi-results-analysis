from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QCheckBox
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
from threedi_results_analysis.tool_fraction_analysis.fraction_map_tool import AddMapTool
from threedi_results_analysis.tool_fraction_analysis.fraction_utils import (
    has_wq_results,
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

        self.map_tool_add_node_cell = AddMapTool(
            widget=self, canvas=self.iface.mapCanvas(),
        )
        self.map_tool_add_node_cell.setButton(self.addNodeCellButton)
        self.map_tool_add_node_cell.setCursor(Qt.CursorShape.CrossCursor)

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
        if not has_wq_results(result):
            return

        self.simulationCombobox.addItem(f"{result.text()} ({result.parent().text()})", result.id)

    def result_removed(self, removed_result: ThreeDiResultItem):
        current_result_removed = False
        if self.fraction_widget.current_result_id == removed_result.id:
            # This is the currently loaded result, so unload
            self.fraction_widget.clear()
            # Also remove retrieved units
            self.substanceUnitsCombobox.clear()
            self.volumeCheckbox.setChecked(False)
            self.stackedCheckbox.setChecked(False)
            current_result_removed = True
            self._update_widget_title()

        # Remove from result combobox
        for i in range(self.simulationCombobox.count()):
            item_id = self.simulationCombobox.itemData(i)
            if self.model.get_result(item_id).id == removed_result.id:
                self.simulationCombobox.blockSignals(True)
                self.simulationCombobox.removeItem(i)
                self.simulationCombobox.blockSignals(False)
                break

        # select top result
        if current_result_removed:
            if self.simulationCombobox.count() > 0:
                self.result_selected(0)

    def result_changed(self, result_item: ThreeDiResultItem):
        self._update_widget_title()

        # Update result combobox
        for i in range(self.simulationCombobox.count()):
            item_id = self.simulationCombobox.itemData(i)
            if self.model.get_result(item_id).id == result_item.id:
                self.simulationCombobox.setItemText(i, f"{result_item.text()} ({result_item.parent().text()})")
                break

    def grid_changed(self, grid_item: ThreeDiGridItem):
        self._update_widget_title()

        # Update result combobox
        for i in range(self.simulationCombobox.count()):
            item_id = self.simulationCombobox.itemData(i)
            result_item = self.model.get_result(item_id)
            if result_item.parent().id == grid_item.id:
                self.simulationCombobox.setItemText(i, f"{result_item.text()} ({result_item.parent().text()})")

    def current_result(self):
        current_index = self.simulationCombobox.currentIndex()
        if current_index == -1:
            return None

        item_id = self.simulationCombobox.itemData(current_index)
        return self.model.get_result(item_id)

    def result_selected(self, result_index: int):
        if result_index == -1:
            return

        item_id = self.simulationCombobox.itemData(result_index)
        result_item = self.model.get_result(item_id)

        # Retrieve the units of the substances
        wq_vars = result_item.threedi_result.available_water_quality_vars
        wq_units = {wq_var["unit"] for wq_var in wq_vars}
        self.substanceUnitsCombobox.clear()
        self.substanceUnitsCombobox.insertItems(0, list(wq_units))
        self.fraction_widget.result_selected(result_item, self.substanceUnitsCombobox.currentText())
        self._update_widget_title()

    def setup_ui(self):
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.dockWidgetContent = QWidget(self)
        self.mainVLayout = QVBoxLayout(self.dockWidgetContent)
        self.dockWidgetContent.setLayout(self.mainVLayout)
        self.buttonBarHLayout = QHBoxLayout(self)
        self.addNodeCellButton = QToolButton(self.dockWidgetContent)
        self.addNodeCellButton.setText("Pick node/cell")
        self.addNodeCellButton.setCheckable(True)
        self.addNodeCellButton.clicked.connect(self.add_node_cell_button_clicked)
        self.buttonBarHLayout.addWidget(self.addNodeCellButton)
        self.stackedCheckbox = QCheckBox("Stacked plot", self.dockWidgetContent)
        self.buttonBarHLayout.addWidget(self.stackedCheckbox)
        self.volumeCheckbox = QCheckBox("Volume mode", self.dockWidgetContent)
        self.volumeCheckbox.setToolTip("Multiply concentrations by volume.")
        self.buttonBarHLayout.addWidget(self.volumeCheckbox)

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.buttonBarHLayout.addItem(spacerItem)
        result_label = QLabel("Simulation result:", self.dockWidgetContent)
        self.buttonBarHLayout.addWidget(result_label)
        self.simulationCombobox = QComboBox(self.dockWidgetContent)
        self.buttonBarHLayout.addWidget(self.simulationCombobox)

        self.buttonBarHLayout.addWidget(QLabel("Substance unit filter:", self.dockWidgetContent))
        self.substanceUnitsCombobox = QComboBox(self.dockWidgetContent)
        self.buttonBarHLayout.addWidget(self.substanceUnitsCombobox)
        self.buttonBarHLayout.setSpacing(10)

        self.mainVLayout.addItem(self.buttonBarHLayout)
        self.mainVLayout.setContentsMargins(0, 10, 0, 10)

        self.fraction_widget = FractionWidget(
            self.dockWidgetContent,
            self.model,
            self.iface
        )
        self.mainVLayout.addWidget(self.fraction_widget)
        self.setWidget(self.dockWidgetContent)
        self._update_widget_title()

        self.substanceUnitsCombobox.currentTextChanged.connect(self.substance_units_change)
        self.stackedCheckbox.stateChanged.connect(self.fraction_widget.stacked_changed)
        self.volumeCheckbox.stateChanged.connect(self.fraction_widget.volume_changed)

        # populate the combobox, with wq results, select first
        for result in self.model.get_results(checked_only=False):
            if has_wq_results(result):
                self.simulationCombobox.addItem(f"{result.text()} ({result.parent().text()})", result.id)

        self.simulationCombobox.currentIndexChanged.connect(self.result_selected)
        if self.simulationCombobox.count() > 0:
            # trigger only emitted when changed
            self.simulationCombobox.setCurrentIndex(-1)
            self.simulationCombobox.setCurrentIndex(0)

    def add_node_cell_button_clicked(self):
        self.iface.mapCanvas().setMapTool(self.map_tool_add_node_cell)

    def unset_map_tools(self):
        if self.iface.mapCanvas().mapTool() is self.map_tool_add_node_cell:
            self.iface.mapCanvas().unsetMapTool(self.map_tool_add_node_cell)

    def substance_units_change(self, substance_unit):
        if substance_unit == "%":
            self.volumeCheckbox.setText("Volume mode")
        else:
            self.volumeCheckbox.setText("Load mode")
        self.fraction_widget.substance_units_change(substance_unit)

    def add_results(self, results):
        current_result = self.current_result()
        if current_result is None:
            logger.warning("First select a result")
            return

        for result in results:
            # Check whether the selected layer belongs to the selected grid/result AND is a node/cell layer
            for layer_type, layer_id in current_result.parent().layer_ids.items():
                if layer_type in ['node', 'cell'] and layer_id == result.mLayer.id():
                    self.fraction_widget.feature_selected(result.mLayer, result.mFeature)
                    self.fraction_widget.fraction_plot.plotItem.vb.menu.viewAll.triggered.emit()
                    self._update_widget_title()
                    return  # Only add a single item

    def _update_widget_title(self):
        title = f"3Di Fraction analysis {self.nr}: "
        if self.fraction_widget.current_result_id:
            result = self.model.get_result(self.fraction_widget.current_result_id)
            title += f"{result.text()} ({result.parent().text()})"
        if self.fraction_widget.current_feature_id:
            title += f" - Node {self.fraction_widget.current_feature_id}"
        self.setWindowTitle(title)
