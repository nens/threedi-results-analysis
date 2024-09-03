# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAbstractItemView
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QGridLayout
from qgis.PyQt.QtWidgets import QGroupBox
from qgis.PyQt.QtWidgets import QTableWidget
from qgis.PyQt.QtWidgets import QTableWidgetItem
from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem
from threedi_results_analysis.threedi_plugin_tool import ThreeDiPluginTool
from typing import Callable
from typing import Dict
from typing import Tuple

import json
import logging
import os


logger = logging.getLogger(__name__)


class FlowSummaryTool(ThreeDiPluginTool):

    def __init__(self, parent, iface, model):
        super().__init__(parent)
        self.iface = iface
        self.model = model
        self.setup_ui()

    def setup_ui(self) -> None:
        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons", "icon_watershed.png")
        self.menu_text = "Flow summary tool"

        self.main_widget = QGroupBox("Flow summary", None)
        self.main_widget.setLayout(QGridLayout())
        self.table_widget = QTableWidget(0, 2, self.main_widget)
        self.table_widget.setHorizontalHeaderLabels(["Parameter", "Value"])
        self.table_widget.resizeColumnsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.verticalHeader().hide()
        self.table_widget.setSortingEnabled(False)
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.main_widget.layout().addWidget(self.table_widget)
        self.main_widget.setEnabled(True)
        self.main_widget.hide()
        self.main_widget.setWindowFlags(Qt.WindowStaysOnTopHint)

    def show_summary_grid(self, item: ThreeDiGridItem) -> None:
        results = []
        self.model.get_results_from_item(item=item, checked_only=False, results=results)
        for result in results:
            self.show_summary_result(result)

    def show_summary_result(self, item: ThreeDiResultItem) -> None:
        # find and parse the result files
        logger.error(f"result {item.id}")
        flow_summary_path = item.path.parent / "flow_summary.json"
        if not flow_summary_path.exists():
            logger.warning(f"Flow summary file from Result {item.text()} cannot be found.")

        self.result_count = 0

        # TODO: keep track of existing params

        # retrieve all the entries in this file
        with flow_summary_path.open() as file:
            data = json.load(file)
            interesting_headers = ["volume_balance", "volume_balance_of_0d_model"]
            row_count = 0
            for interesting_header in interesting_headers:
                if interesting_header in data:
                    for param in data[interesting_header]:
                        self.table_widget.insertRow(self.table_widget.rowCount())
                        self.table_widget.setItem(row_count, 0, QTableWidgetItem(f'{param} [{data[interesting_header][param]["units"]}]'))
                        self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(data[interesting_header][param]["value"])))
                        row_count += 1

        self.table_widget.resizeColumnsToContents()
        self.result_count += 1

    def get_custom_actions(self) -> Dict[QAction, Tuple[Callable[[ThreeDiGridItem], None], Callable[[ThreeDiResultItem], None]]]:
        return {QAction("Show flow summary"): (self.show_summary_grid, self.show_summary_result)}

    def on_unload(self) -> None:
        del self.main_widget
        self.main_widget = None

    @pyqtSlot(ThreeDiResultItem)
    def result_added(self, result_item: ThreeDiResultItem) -> None:
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

    def run(self) -> None:
        self.main_widget.show()
