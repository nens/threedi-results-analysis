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
        self.setHorizontalHeaderLabels(["active", "pattern", "substance"])
        self.result_item = None

    def set_fraction(self, item: ThreeDiResultItem, substance: str):
        self.clear()
        self.setHorizontalHeaderLabels(["active", "pattern", "substance"])
        self.result_item = item

        # Retrieve the substances
        threedi_result = self.result_item.threedi_result
        water_quality_vars = threedi_result.available_water_quality_vars
        for wq_var in water_quality_vars:
            if wq_var["unit"] != substance:
                continue
            color_item = QStandardItem()
            color_item.setData((Qt.SolidLine, self.get_color()))
            color_item.setEditable(False)
            substance_item = QStandardItem(wq_var["parameters"])
            substance_item.setEditable(False)
            check_item = QStandardItem("")
            check_item.setCheckable(True)
            check_item.setEditable(False)
            check_item.setCheckState(Qt.Checked)
            self.appendRow([check_item, color_item, substance_item])

    def get_color(self) -> QColor:
        return COLOR_LIST[self.rowCount() % len(COLOR_LIST)]

    def create_plots(self, feature_id, time_units, stacked):
        plots = []
        for row in range(self.rowCount()):
            style, color = self.item(row, 1).data()
            substance = self.item(row, 2).text()
            ts_table = self.timeseries_table(substance, feature_id, time_units=time_units)
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
