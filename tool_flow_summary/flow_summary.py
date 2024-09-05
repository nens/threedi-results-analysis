# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QGridLayout
from qgis.PyQt.QtWidgets import QHBoxLayout
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtWidgets import QSizePolicy
from qgis.PyQt.QtWidgets import QSpacerItem
from qgis.PyQt.QtWidgets import QWidget
from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem
from threedi_results_analysis.threedi_plugin_tool import ThreeDiPluginTool
from threedi_results_analysis.tool_flow_summary.variable_table import VariableTable
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple

import json
import logging
import os


logger = logging.getLogger(__name__)

GROUP_NAMES = ["general_information", "volume_balance", "volume_balance_of_0d_model"]


class FlowSummaryTool(ThreeDiPluginTool):

    def __init__(self, parent, iface, model):
        super().__init__(parent)
        self.iface = iface
        self.model = model

        # The list of shown results in the summary, idx+1 corresponding to column idx in the table
        self.result_ids : List[int] = []
        # The map of group name to table
        self.tables: Dict[str, VariableTable] = {}

        self.setup_ui()

    def setup_ui(self) -> None:
        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons", "icon_summary.png")
        self.menu_text = "Flow summary tool"
        self.main_widget = QDialog(None)
        self.main_widget.setWindowTitle("Flow summary")
        self.main_widget.setLayout(QGridLayout())

        for group_name in GROUP_NAMES:
            self.tables[group_name] = VariableTable(group_name, self.main_widget)
            self.main_widget.layout().addWidget(self.tables[group_name])

        self.main_widget.setEnabled(True)
        self.main_widget.hide()
        self.main_widget.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Add Ok button
        button_widget = QWidget(self.main_widget)
        button_widget.setLayout(QHBoxLayout(button_widget))
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_widget.layout().addItem(spacer_item)
        ok_button = QPushButton("Ok", button_widget)
        button_widget.layout().addWidget(ok_button, alignment=Qt.AlignRight)
        self.main_widget.layout().addWidget(button_widget)
        ok_button.clicked.connect(self.main_widget.hide)

    def show_summary_grid(self, item: ThreeDiGridItem) -> None:
        results = []
        self.model.get_results_from_item(item=item, checked_only=False, results=results)
        for result in results:
            self.show_summary_result(result)

    def show_summary_result(self, item: ThreeDiResultItem) -> None:

        if item.id in self.result_ids:
            logger.warning("Result already added to flow summary, ignoring...")
            return

        self.result_ids.append(item.id)

        # find and parse the result files
        flow_summary_path = item.path.parent / "flow_summary.json"
        if not flow_summary_path.exists():
            logger.warning(f"Flow summary file from Result {item.text()} cannot be found.")
            # TODO: make red, but unclear how to style individual items in header
            for group_name in GROUP_NAMES:
                self.tables[group_name].add_summary_results(item, dict())
            return

        # retrieve all the entries in this file
        with flow_summary_path.open() as file:
            data = json.load(file)

            for group_name in GROUP_NAMES:
                assert group_name in self.tables
                if group_name in data:
                    group_data = data[group_name]
                else:
                    group_data = {}
                self.tables[group_name].add_summary_results(item, group_data)

        self.main_widget.show()

    def get_custom_actions(self) -> Dict[QAction, Tuple[Callable[[ThreeDiGridItem], None], Callable[[ThreeDiResultItem], None]]]:
        return {QAction("Show flow summary"): (self.show_summary_grid, self.show_summary_result)}

    def on_unload(self) -> None:
        del self.main_widget
        self.main_widget = None

    @pyqtSlot(ThreeDiResultItem)
    def result_removed(self, result_item: ThreeDiResultItem):
        # Remove column if required, pop from self.result_ids
        try:
            idx = self.result_ids.index(result_item.id)
        except ValueError:
            return  # result not in summary

        self.result_ids.pop(idx)
        for table in self.tables:
            self.tables[table].remove_result(idx+1)

        # if empty: fully clean tables
        if len(self.result_ids) == 0:
            for table in self.tables:
                self.tables[table].clean_results()

    @pyqtSlot(ThreeDiResultItem)
    def result_changed(self, result_item: ThreeDiResultItem):
        try:
            idx = self.result_ids.index(result_item.id)
        except ValueError:
            return  # result not in summary

        for table in self.tables:
            self.tables[table].change_result(idx+1, result_item.text())

    def run(self) -> None:
        self.main_widget.show()
