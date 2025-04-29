import pyqtgraph as pg


pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")
from PyQt5.QtCore import Qt
from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel
from threedi_results_analysis.tool_fraction_analysis.fraction_model import FractionModel

import logging


logger = logging.getLogger(__name__)

class FractionPlot(pg.PlotWidget):
    def __init__(self, parent, result_model: ThreeDiPluginModel, fraction_model: FractionModel):
        super().__init__(parent)
        self.showGrid(True, True, 0.5)
        self.fraction_model = fraction_model
        self.result_model = result_model
        self.item_map = {}
        self.setLabel("bottom", "Time", "hrs")
        self.setLabel("left", "Concentration", "")
        self.getAxis("left").enableAutoSIPrefix(False)

    def clear_plot(self):
        self.clear()
        self.item_map.clear()
        self.setLabel("left", "Concentration", "")

    def item_changed(self, model_item):
        substance = model_item.data()
        self.item_map[substance].setVisible(model_item.checkState() == Qt.Checked)

    def fraction_selected(self, feature_id, substance_unit: str, time_unit: str):
        """
        Retrieve info from model and create plots
        """
        self.clear_plot()
        plots = self.fraction_model.create_plots(feature_id, time_unit, stacked=False)
        for substance, plot in plots:
            self.item_map[substance] = plot
            self.addItem(plot)

        self.setLabel("left", "Concentration", substance_unit)
        self.plotItem.vb.menu.viewAll.triggered.emit()
