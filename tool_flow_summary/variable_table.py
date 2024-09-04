
from qgis.PyQt.QtWidgets import QAbstractItemView
from qgis.PyQt.QtWidgets import QTableWidget


class VariableTable(QTableWidget):
    def __init__(self, parent):
        super().__init__(0, 1, parent)
        self.setHorizontalHeaderLabels(["Variable"])
        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().hide()
        self.setSortingEnabled(False)
        self.setSelectionMode(QAbstractItemView.NoSelection)
