
from qgis.PyQt.QtCore import QLocale
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAbstractItemView
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtWidgets import QHeaderView
from qgis.PyQt.QtWidgets import QTableWidget
from qgis.PyQt.QtWidgets import QTableWidgetItem
from typing import List
from typing import Tuple


class VariableTable(QTableWidget):
    def __init__(self, variable_alignment, parent):
        super().__init__(0, 1, parent)
        self.variable_alignment = variable_alignment
        self.setHorizontalHeaderLabels([""])
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)

        self.verticalHeader().hide()
        self.setSortingEnabled(False)
        self.setSelectionMode(QAbstractItemView.ContiguousSelection)

        # for proper aligning, we always need to reserve space for the scrollbar
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.horizontalHeader().setStretchLastSection(True)

        # The list of parameters shown in the summary, idx corresponding to row idx in the table
        self.param_names : List[str] = []

    def add_summary_results(self, result_text: str, group_data):
        header_item = QTableWidgetItem(result_text)
        self.insertColumn(self.columnCount())
        self.setHorizontalHeaderItem(self.columnCount()-1, header_item)

        for param in group_data:
            param_name, param_value = self._format_variable(param, group_data[param])

            # Check if we've added this parameter before, then use that row idx,
            # otherwise append to bottom of table
            try:
                param_index = self.param_names.index(param_name)
            except ValueError:
                param_index = len(self.param_names)
                self.param_names.append(param_name)
                # Add a new row and set the parameter name
                assert param_index == self.rowCount()
                self.insertRow(param_index)
                item = QTableWidgetItem(param_name)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignLeft)
                self.setItem(param_index, 0, item)

            item = QTableWidgetItem(param_value)
            item.setTextAlignment(self.variable_alignment)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.setItem(param_index, self.columnCount()-1, item)

        for idx in range(0, self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(idx, QHeaderView.Interactive)

    def resizeEvent(self, event):
        self.resizeRowsToContents()
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        # https://stackoverflow.com/questions/1230222/selected-rows-in-qtableview-copy-to-qclipboard/24133289#24133289
        if event.key() == Qt.Key_C and event.modifiers() & Qt.ControlModifier:

            indexes = self.selectedIndexes()
            current_text = ""
            current_row = 0  # To determine when to insert newlines

            indexes = sorted(indexes)  # Necessary, otherwise they are in column order

            for index in indexes:
                if current_text == "":  # first line
                    pass
                elif index.row() != current_row:  # new row
                    current_text += "\n"
                else:
                    current_text += "\t"

                current_row = index.row()
                current_item = self.item(index.row(), index.column())
                if current_item:
                    current_text += str(self.item(index.row(), index.column()).text())

            QApplication.clipboard().setText(current_text)
            return

        super().keyPressEvent(event)

    def clean_results(self) -> None:
        self.clearContents()
        self.setColumnCount(1)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels([""])
        self.param_names.clear()

    def remove_result(self, idx: int) -> None:
        self.removeColumn(idx)

    def get_preferred_variable_column_width(self) -> int:
        # iterate over the texts and determine the max width when resized to contents
        self.resizeColumnToContents(0)
        max_width = 0
        for r in range(self.rowCount()):
            width = self.columnWidth(0)
            if width > max_width:
                max_width = width

        return max_width

    def change_result(self, idx: int, text: str) -> None:
        self.setHorizontalHeaderItem(idx, QTableWidgetItem(text))

    def _format_variable(self, param_name: str, param_data: dict) -> Tuple[str, str]:

        param_name = param_name.replace("_", " ")
        if type(param_data) is dict:
            param_name = f'{param_name} [{param_data["units"]}]'
            param_data = param_data["value"]

        locale = QLocale()

        # numbers in 4 decimals, or scientific notation when not possible
        if isinstance(param_data, float):
            if param_data < 0.0001:
                param_data = locale.toString(param_data, "g", 5)
            else:
                param_data = locale.toString(param_data, "f", 4)
        elif isinstance(param_data, int):
            param_data = locale.toString(param_data)
        else:
            param_data = str(param_data)

        param_name = param_name[0].capitalize() + param_name[1:]
        return param_name, param_data
