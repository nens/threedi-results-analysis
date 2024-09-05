
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAbstractItemView
from qgis.PyQt.QtWidgets import QTableWidget
from qgis.PyQt.QtWidgets import QTableWidgetItem
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem
from typing import List
from typing import Tuple
from typing import Union


class VariableTable(QTableWidget):
    def __init__(self, group_name: str, parent):
        super().__init__(0, 1, parent)
        self.group_name = group_name
        self.setHorizontalHeaderLabels([group_name])
        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().hide()
        self.setSortingEnabled(False)
        self.setSelectionMode(QAbstractItemView.NoSelection)

        # The list of parameters shown in the summary, idx corresponding to row idx in the table
        self.param_names : List[str] = []

    def add_summary_results(self, item: ThreeDiResultItem, group_data):
        header_item = QTableWidgetItem(item.text())
        self.insertColumn(self.columnCount())
        self.setHorizontalHeaderItem(self.columnCount()-1, header_item)

        for param in group_data:
            param_name, param_value = self._format_variable(param, group_data[param])

            # Check if we've added this parameter before, then use that row idx,
            # otherwise append to bottom of table
            try:
                param_index = self.param_names.index(param)
            except ValueError:
                param_index = len(self.param_names)
                self.param_names.append(param)
                # Add a new row and set the parameter name
                assert param_index == self.rowCount()
                self.insertRow(param_index)
                item = QTableWidgetItem(param_name)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.setItem(param_index, 0, item)

            item = QTableWidgetItem(str(param_value))
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.setItem(param_index, self.columnCount()-1, item)

        self.resizeColumnsToContents()

    def clean_results(self) -> None:
        self.setColumnCount(1)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels([self.group_name])
        self.resizeColumnsToContents()

    def remove_result(self, idx: int) -> None:
        self.removeColumn(idx)

    def change_result(self, idx: int, text: str) -> None:
        self.setHorizontalHeaderItem(idx, QTableWidgetItem(text))

    def _format_variable(self, param_name: str, param_data: dict) -> Tuple[str, Union[str, int]]:

        # TODO: remove underscores from param names
        if type(param_data) is dict:
            name = f'{param_name} [{param_data["units"]}]'
            value = param_data["value"]
            return name, value
        else:
            return param_name, param_data
