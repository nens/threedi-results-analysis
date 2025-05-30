from qgis.PyQt.QtGui import QColor

import pyqtgraph as pg


pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")
from PyQt5.QtCore import Qt
from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel
from threedi_results_analysis.tool_fraction_analysis.fraction_model import FractionModel


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
        for plot in self.item_map[substance]:
            plot.setVisible(model_item.checkState() == Qt.Checked)

    def fraction_selected(self, feature_id, substance_unit: str, time_unit: str, stacked: bool):
        """
        Retrieve info from model and create plots
        """
        self.clear_plot()
        plots = self.fraction_model.create_plots(feature_id, time_unit, stacked)
        prev_plot = None
        for substance, plot in plots:
            self.item_map[substance] = [plot]
            plot.setZValue(100)
            self.addItem(plot)

            if stacked:
                # Add fill between consecutive plots
                plot_color = plot.opts['pen'].color()
                # Reduce saturation for fill
                fill_color = self.reduce_saturation(plot_color)
                if not prev_plot:
                    # this is the first, just fill downward to axis
                    plot.setFillLevel(0)
                    plot.setFillBrush(pg.mkBrush(fill_color))
                else:
                    fill = pg.FillBetweenItem(plot, prev_plot, pg.mkBrush(fill_color))
                    fill.setZValue(20)
                    self.addItem(fill)
                    self.item_map[substance].append(fill)

            prev_plot = plot

        self.setLabel("left", "Concentration", substance_unit)
        self.plotItem.vb.menu.viewAll.triggered.emit()

    def reduce_saturation(self, plot_color):
        return QColor.fromHsvF(plot_color.hueF(), plot_color.saturationF()/2.0, plot_color.valueF())
