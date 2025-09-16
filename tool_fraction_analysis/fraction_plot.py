import re
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

    def item_checked(self, model_item):
        if not self.item_map:  # No plots yet
            return
        substance = model_item.data()
        for plot in self.item_map[substance]:
            plot.setVisible(model_item.checkState() == Qt.Checked)

    def item_color_changed(self, color_model_item):
        if not self.item_map:  # No plots yet
            return

        # Retrieve the substance name from the model
        row = color_model_item.index().row()
        selected_model_item = color_model_item.model().item(row, 0)
        substance = selected_model_item.data()

        style, color = color_model_item.data()
        pen = pg.mkPen(color=QColor(*color), width=2, style=style)
        self.item_map[substance][0].setPen(pen)

        if len(self.item_map[substance]) == 2:
            # there is a fill, also change that color
            fill_color = self.reduce_saturation(QColor(*color))
            self.item_map[substance][1].setBrush(pg.mkBrush(fill_color))

    def fraction_selected(self, feature_id, substance_unit: str, time_unit: str, stacked: bool, volume: bool):
        """
        Retrieve info from model and create plots
        """
        self.clear_plot()

        substance_unit_conversion = 1.0

        if volume:
            # for known units, we apply basic conversion
            pattern = r"^(.*)/\s*(m3|l)\s*$"
            matches = re.findall(pattern, substance_unit, flags=re.IGNORECASE)
            if len(matches) == 1 and len(matches[0]) == 2:
                if matches[0][1].lower() == "l":
                    substance_unit_conversion = 1000.0
                    processed_substance_unit = matches[0][0].strip()
                    volume_label = "Load"
                elif matches[0][1].lower() == "m3":
                    substance_unit_conversion = 1.0
                    processed_substance_unit = matches[0][0].strip()
                    volume_label = "Load"
            elif substance_unit.strip() == "%":
                substance_unit_conversion = 1.0
                processed_substance_unit = "m<sup>3</sup>"
                volume_label = "Volume"
            else:  # unknown, take original unit as-is and append x m3
                substance_unit_conversion = 1.0
                processed_substance_unit = f"{substance_unit} · m<sup>3</sup>"
                volume_label = "Load"

        plots = self.fraction_model.create_plots(feature_id, time_unit, stacked, volume, substance_unit_conversion)
        prev_plot = None
        for substance, plot, visible in plots:
            self.item_map[substance] = [plot]
            plot.setZValue(100)
            plot.setVisible(visible)
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
                    fill.setVisible(visible)
                    self.addItem(fill)
                    self.item_map[substance].append(fill)

            prev_plot = plot

        self.setLabel("left", volume_label if volume else "Concentration", processed_substance_unit if volume else substance_unit)
        self.plotItem.vb.menu.viewAll.triggered.emit()

    def reduce_saturation(self, plot_color):
        return QColor.fromHsvF(plot_color.hueF(), plot_color.saturationF()/2.0, plot_color.valueF())
