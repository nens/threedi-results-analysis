# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QGridLayout
from qgis.PyQt.QtWidgets import QGroupBox
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

GROUP_NAMES = [("general_information", Qt.AlignmentFlag.AlignLeft), ("volume_balance", Qt.AlignmentFlag.AlignRight), ("volume_balance_of_0d_model", Qt.AlignmentFlag.AlignRight)]


class FlowSummaryTool(ThreeDiPluginTool):

    def __init__(self, parent, iface, model):
        super().__init__(parent)
        self.iface = iface
        self.model = model
        self.first_time = True

        # The list of shown results in the summary, idx+1 corresponding to column idx in the table
        self.result_ids : List[int] = []
        # The map of group name to table
        self.tables: Dict[str, VariableTable] = {}

        self.setup_ui()

    def setup_ui(self) -> None:
        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons", "icon_summary.png")
        self.menu_text = "Flow summary tool"
        self.main_widget = QDialog(self.iface.mainWindow())
        self.main_widget.setWindowTitle("Flow summary")
        self.main_widget.setLayout(QGridLayout())

        for group_name, info_alignment in GROUP_NAMES:
            group_title = (group_name[0].capitalize() + group_name[1:]).replace("_", " ")
            group_title = group_title.replace("0d", "0D")
            variable_group = QGroupBox(group_title, self.main_widget)
            variable_group.setStyleSheet("QGroupBox { font-weight: bold; }")
            variable_group.setLayout(QGridLayout())

            self.tables[group_name] = VariableTable(info_alignment, variable_group)
            variable_group.layout().addWidget(self.tables[group_name])

            self.main_widget.layout().addWidget(variable_group)

        self.main_widget.setEnabled(True)
        self.main_widget.hide()
        self.main_widget.setWindowFlags(Qt.WindowType.Tool)

        # Add Ok button
        button_widget = QWidget(self.main_widget)
        button_widget.setLayout(QHBoxLayout(button_widget))
        reset_button = QPushButton("Reset column widths", button_widget)
        button_widget.layout().addWidget(reset_button)
        reset_button.clicked.connect(self._reset_column_widths)
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        button_widget.layout().addItem(spacer_item)
        ok_button = QPushButton("OK", button_widget)
        button_widget.layout().addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.main_widget.layout().addWidget(button_widget)
        ok_button.clicked.connect(self.main_widget.hide)

        # set comfortable start width
        self.main_widget.resize(800, self.main_widget.height())

    def _reset_column_widths(self) -> None:
        for table in self.tables.values():
            if table.columnCount() == 0:
                return

        max_width_variables = 0
        for table in self.tables.values():
            group_width = table.get_preferred_variable_column_width()
            if group_width > max_width_variables:
                max_width_variables = group_width

        for table in self.tables.values():
            table.setColumnWidth(0, max_width_variables)
            if table.columnCount() == 1:
                continue
            scrollbar_width = table.horizontalScrollBar().geometry().height()
            # evenly spread remainder of columns
            column_width = (table.width() - max_width_variables - scrollbar_width) // (table.columnCount() - 1)
            column_width -= 3  # prevent scrollbar
            for c in range(1, table.columnCount()):
                table.setColumnWidth(c, column_width)

    def add_summary_grid(self, item: ThreeDiGridItem) -> None:
        results = []
        self.model.get_results_from_item(item=item, checked_only=False, results=results)
        for result in results:
            self.add_summary_result(result)

    def add_summary_result(self, item: ThreeDiResultItem, show: bool = True) -> None:

        if item.id in self.result_ids:
            logger.warning("Result already added to flow summary, ignoring...")
            return

        self.result_ids.append(item.id)

        # find and parse the result files
        flow_summary_path = item.path.parent / "flow_summary.json"
        if not flow_summary_path.exists():
            logger.warning(f"Flow summary file from Result {item.text()} cannot be found.")
            # TODO: ideally make red, but unclear how to style individual items in header
            for group_name, _ in GROUP_NAMES:
                self.tables[group_name].add_summary_results(item.text(), dict())
        else:
            # retrieve all the entries in this file
            with flow_summary_path.open() as file:
                data = json.load(file)

                for group_name, _ in GROUP_NAMES:
                    assert group_name in self.tables
                    if group_name in data:
                        group_data = data[group_name]
                    else:
                        group_data = {}
                    self.tables[group_name].add_summary_results(item.text(), group_data)

        self._reset_column_widths()
        if show:
            self.main_widget.show()

    def remove_summary_grid(self, item: ThreeDiGridItem) -> None:
        results = []
        self.model.get_results_from_item(item=item, checked_only=False, results=results)
        for result in results:
            self.remove_summary_result(result)

    def remove_summary_result(self, item: ThreeDiResultItem) -> None:
        self.result_removed(item)

    def get_custom_actions(self) -> Dict[QAction, Tuple[Callable[[ThreeDiGridItem], None], Callable[[ThreeDiResultItem], None]]]:
        separator = QAction()
        separator.setSeparator(True)
        return {separator: (None, None),
                QAction("Add to flow summary"): (self.add_summary_grid, self.add_summary_result),
                QAction("Remove from flow summary"): (self.remove_summary_grid, self.remove_summary_result)
                }

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

        self._reset_column_widths()

    @pyqtSlot(ThreeDiResultItem)
    def result_changed(self, result_item: ThreeDiResultItem):
        try:
            idx = self.result_ids.index(result_item.id)
        except ValueError:
            return  # result not in summary

        for table in self.tables:
            self.tables[table].change_result(idx+1, result_item.text())

    @pyqtSlot(ThreeDiResultItem)
    def result_added(self, item: ThreeDiResultItem):
        self.action_icon.setEnabled(self.model.number_of_results() > 0)
        self.add_summary_result(item, False)

    def run(self) -> None:
        self.main_widget.show()
        if self.first_time:
            self._reset_column_widths()
            self.first_time = False
