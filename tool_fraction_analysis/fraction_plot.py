import pyqtgraph as pg


pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")
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
        self.setLabel("bottom", "Time", "hrs")
        self.setLabel("left", "Concentration", "")
        self.getAxis("left").enableAutoSIPrefix(False)

    def clear(self):
        self.setLabel("left", "Concentration", "")
        super().clear()

    def fraction_selected(self, feature_id, substance_unit: str, time_unit: str):
        """
        Retrieve info from model and create plots
        """
        self.clear()
        plots = self.fraction_model.create_plots(feature_id, time_unit, stacked=False)
        for plot in plots:
            self.addItem(plot)

        self.setLabel("left", "Concentration", substance_unit)
        self.plotItem.vb.menu.viewAll.triggered.emit()

    def fraction_data_changed(self, index):
        # """
        # change graphs
        # :param index: index of changed field
        # """
        # item = self.fraction_model.rows[index.row()]

        # if self.fraction_model.columns[index.column()].name == "active":
        #     if item.active.value:
        #         self.show_timeseries(index.row())
        #     else:
        #         self.hide_timeseries(index.row())

        # elif self.fraction_model.columns[index.column()].name == "hover":
        #     width = 2
        #     if item.hover.value:
        #         width = 5
        #     item.plots(self.current_parameter["parameters"], time_units=self.current_time_units).setPen(
        #         color=item.color.qvalue, width=width, style=item.result.value._pattern)

        # elif self.fraction_model.columns[index.column()].name == "color":
        #     item.plots(self.current_parameter["parameters"], time_units=self.current_time_units).setPen(
        #         color=item.color.qvalue, width=2, style=item.result.value._pattern)
            
        pass

    def hide_timeseries(self, location_nr):
        """
        hide timeseries of location in graph
        :param row_nr: integer, row number of location
        """

        plot = self.fraction_model.rows[location_nr].plots(
            self.current_parameter["parameters"], time_units=self.current_time_units)
        self.removeItem(plot)

    def show_timeseries(self, location_nr):
        """
        show timeseries of location in graph
        :param row_nr: integer, row number of location
        """

        plot = self.fraction_model.rows[location_nr].plots(
            self.current_parameter["parameters"], time_units=self.current_time_units)
        self.addItem(plot)
