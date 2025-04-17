from qgis.PyQt.QtGui import QStandardItem
from qgis.PyQt.QtGui import QStandardItemModel
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem

import logging
import numpy as np
import pyqtgraph as pg


logger = logging.getLogger(__name__)

EMPTY_TIMESERIES = np.array([], dtype=float)

class FractionModel(QStandardItemModel):
    def __init__(self, parent, result_model):
        super().__init__(parent)
        self.result_model = result_model
        self.setHorizontalHeaderLabels(["active", "pattern", "label", "id"])
        self.result_item = None

    def set_fraction(self, id, item: ThreeDiResultItem):
        self.clear()
        self.setHorizontalHeaderLabels(["active", "pattern", "label", "id"])

        self.result_item = item

        # Retrieve the substances (TODO: filter on right unit)
        self.appendRow([QStandardItem(True), QStandardItem(), QStandardItem(item.text()), QStandardItem(id)])

    def create_plots(self, id, time_units, substance_unit, stacked):
        threedi_result = self.result_item.threedi_result

        # iterate over substances        
        water_quality_vars = threedi_result.available_water_quality_vars
        logger.error(water_quality_vars)

        plots = []
        for substance in water_quality_vars:
            ts_table = self.timeseries_table(substance, id, time_units=time_units)
            pen = pg.mkPen(color=self.color.value, width=2, style=self.result.value._pattern)
            plots += pg.PlotDataItem(ts_table, pen=pen)
        
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
