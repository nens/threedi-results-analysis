from qgis.PyQt.QtGui import QStandardItem
from qgis.PyQt.QtGui import QStandardItemModel
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem


class FractionModel(QStandardItemModel):
    def __init__(self, parent, result_model):
        super().__init__(parent)
        self.result_model = result_model
        self.setHorizontalHeaderLabels(["active", "pattern", "label", "id"])

    def add_fraction(self, item: ThreeDiResultItem):
        self.appendRow(QStandardItem(), QStandardItem(), item.text(), item.id)
        pass
        

