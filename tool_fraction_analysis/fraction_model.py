from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtGui import QStandardItem
from qgis.PyQt.QtGui import QStandardItemModel
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem
from threedi_results_analysis.utils.color import COLOR_LIST

import logging
import numpy as np
import pyqtgraph as pg


logger = logging.getLogger(__name__)

EMPTY_TIMESERIES = np.array([], dtype=float)

class FractionModel(QStandardItemModel):

    def __init__(self, parent, result_model):
        super().__init__(parent)
        self.result_model = result_model
        self.setHorizontalHeaderLabels(["active", "pattern", "substance", "id"])
        self.result_item = None

    def set_fraction(self, id, item: ThreeDiResultItem):
        self.clear()
        self.setHorizontalHeaderLabels(["active", "pattern", "substance", "id"])
        self.result_item = item

        # Retrieve the substances (TODO: filter on right unit)
        threedi_result = self.result_item.threedi_result
        water_quality_vars = threedi_result.available_water_quality_vars
        for substance in water_quality_vars:
            color_item = QStandardItem()
            color_item.setData((Qt.SolidLine, self.get_color()))
            color_item.setEditable(False)
            substance_item = QStandardItem(substance["parameters"])
            substance_item.setEditable(True)
            id_item = QStandardItem(QStandardItem(str(id)))
            id_item.setEditable(True)
            self.appendRow([QStandardItem(True), color_item, substance_item, id_item])

    def get_color(self) -> QColor:
        return COLOR_LIST[self.rowCount() % len(COLOR_LIST)]

    def create_plots(self, time_units, substance_unit, stacked):
        plots = []
        for index in range(self.rowCount()):
            style, color = self.item(index, 1).data()
            substance = self.item(index, 2).text()
            id = int(self.item(index, 3).text())
            
            ts_table = self.timeseries_table(substance, id, time_units=time_units)
            pen = pg.mkPen(color=QColor(*color), width=2, style=style)
            plots.append(pg.PlotDataItem(ts_table, pen=pen))

        return plots
    
    def timeseries_table(self, substance, id, time_units):
        timeseries = self.result_item.threedi_result.get_timeseries(
            substance, node_id=id, fill_value=np.NaN
        )
        if timeseries.shape[1] == 1:
            logger.info("1-element timeserie, plotting empty serie")
            return EMPTY_TIMESERIES
        if time_units == "hrs":
            vector = np.array([3600, 1])
        elif time_units == "mins":
            vector = np.array([60, 1])
        else:
            vector = np.array([1, 1])
        return timeseries / vector
    
    def has_wq_results(self, result_item: ThreeDiResultItem):
        return len(result_item.threedi_result.available_water_quality_vars) != 0
