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
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.PyQt.QtWidgets import QWidget
from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem
from threedi_results_analysis.threedi_plugin_tool import ThreeDiPluginTool
from threedi_results_analysis.tool_flow_summary.variable_table import VariableTable
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import json
import logging
import os


logger = logging.getLogger(__name__)

INTERESTING_HEADERS = ["general_information", "volume_balance", "volume_balance_of_0d_model"]


class FlowSummaryTool(ThreeDiPluginTool):

    def __init__(self, parent, iface, model):
        super().__init__(parent)
        self.iface = iface
        self.model = model

        # The list of shown results in the summary, idx+1 corresponding to column idx in the table
        self.result_ids : List[int] = []
        # The list of parameters shown in the summary, idx corresponding to row idx in the table
        self.param_names : List[str] = []

        self.setup_ui()

    def setup_ui(self) -> None:
        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons", "icon_watershed.png")
        self.menu_text = "Flow summary tool"
        self.main_widget = QDialog(None)
        self.main_widget.setWindowTitle("Flow summary")
        self.main_widget.setLayout(QGridLayout())

        # TODO: add other tables and move logic
        self.general_info_table = VariableTable(self.main_widget)

        self.main_widget.layout().addWidget(self.general_info_table)
        self.main_widget.setEnabled(True)
        self.main_widget.hide()
        self.main_widget.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Add ok button
        button_widget = QWidget(self.main_widget)
        button_widget.setLayout(QHBoxLayout(button_widget))
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_widget.layout().addItem(spacer_item)
        ok_button = QPushButton("Ok", button_widget)
        button_widget.layout().addWidget(ok_button, alignment=Qt.AlignRight)
        self.main_widget.layout().addWidget(button_widget)
        ok_button.clicked.connect(self.main_widget.hide)

    def _format_variable(self, param_name: str, param_data: dict) -> Tuple[str, Union[str, int]]:

        # TODO: remove underscores from param names
        if type(param_data) is dict:
            name = f'{param_name} [{param_data["units"]}]'
            value = param_data["value"]
            return name, value
        else:
            return param_name, param_data

    def show_summary_grid(self, item: ThreeDiGridItem) -> None:
        results = []
        self.model.get_results_from_item(item=item, checked_only=False, results=results)
        for result in results:
            self.show_summary_result(result)

    def show_summary_result(self, item: ThreeDiResultItem) -> None:

        if item.id in self.result_ids:
            logger.warning("Result already added to flow summary, ignoring...")
            return

        header_item = QTableWidgetItem(item.text())
        self.result_ids.append(item.id)
        self.general_info_table.insertColumn(len(self.result_ids))
        self.general_info_table.setHorizontalHeaderItem(self.general_info_table.columnCount()-1, header_item)

        # find and parse the result files
        flow_summary_path = item.path.parent / "flow_summary.json"
        if not flow_summary_path.exists():
            logger.warning(f"Flow summary file from Result {item.text()} cannot be found.")
            # TODO: make red, but unclear how to style individual items in header
            return

        # retrieve all the entries in this file
        with flow_summary_path.open() as file:
            data = json.load(file)

            for interesting_header in INTERESTING_HEADERS:
                if interesting_header in data:
                    for param in data[interesting_header]:
                        param_name, param_value = self._format_variable(param, data[interesting_header][param])

                        # Check if we've added this parameter before, then use that row idx,
                        # otherwise append to bottom of table
                        try:
                            param_index = self.param_names.index(param)
                        except ValueError:
                            param_index = len(self.param_names)
                            self.param_names.append(param)
                            # Add a new row and set the parameter name
                            assert param_index == self.general_info_table.rowCount()
                            self.general_info_table.insertRow(param_index)
                            self.general_info_table.setItem(param_index, 0, QTableWidgetItem(param_name))

                        self.general_info_table.setItem(param_index, len(self.result_ids), QTableWidgetItem(str(param_value)))

        self.general_info_table.resizeColumnsToContents()
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
        self.general_info_table.removeColumn(idx+1)

        # TODO: if empty: fully clean table?

    @pyqtSlot(ThreeDiResultItem)
    def result_changed(self, result_item: ThreeDiResultItem):
        try:
            idx = self.result_ids.index(result_item.id)
        except ValueError:
            return  # result not in summary

        self.general_info_table.setHorizontalHeaderItem(idx+1, QTableWidgetItem(result_item.text()))

    def run(self) -> None:
        self.main_widget.show()
