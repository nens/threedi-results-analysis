import re
from qgis.PyQt.QtGui import QColor
import pyqtgraph as pg
from qgis.PyQt.QtCore import pyqtSignal

from threedi_results_analysis.utils.geo_utils import distance_to_polyline
from threedi_results_analysis.utils.color import reduce_saturation, increase_value

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")
from qgis.PyQt.QtCore import Qt
from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel
from threedi_results_analysis.tool_fraction_analysis.fraction_model import FractionModel


class FractionPlot(pg.PlotWidget):
    hover_plot = pyqtSignal(str)

    def __init__(self, parent, result_model: ThreeDiPluginModel, fraction_model: FractionModel):
        super().__init__(parent)
        self.showGrid(True, True, 0.5)
        self.proxy = pg.SignalProxy(self.scene().sigMouseMoved, rateLimit=10, slot=self.mouse_moved)
        self.fraction_model = fraction_model
        self.result_model = result_model
        # map from substance name to (list of) plot
        self.item_map = {}
        self.setLabel("bottom", "Time", "hrs")
        self.setLabel("left", "Concentration", "")
        self.getAxis("left").enableAutoSIPrefix(False)
        self.mouseLabel = pg.TextItem(text="", anchor=(1, 1), color=(0, 0, 0))

        self.mouseMarker = pg.ScatterPlotItem(
            [0], [0],
            symbol='o',
            size=12,
            brush='r',
            pen='k'
        )
        self.mouseMarker.setVisible(False)
        self.addItem(self.mouseMarker)
        self.addItem(self.mouseLabel)

    def clear_plot(self):
        self.clear()
        self.item_map.clear()
        self.setLabel("left", "Concentration", "")
        self.addItem(self.mouseMarker)
        self.addItem(self.mouseLabel)
        self.mouseLabel.setText("")
        self.mouseMarker.setVisible(False)

    def item_checked(self, model_item):
        if not self.item_map:  # No plots yet
            return
        substance = model_item.data()
        for plot in self.item_map[substance]:
            plot.setVisible(model_item.checkState() == Qt.CheckState.Checked)

    def mouse_moved(self, pos):
        # Translate scene position to plot coordinates
        # As we are using a ProxySignal, we get a list of events
        mouse_point = self.plotItem.vb.mapSceneToView(pos[0])
        x = mouse_point.x()
        y = mouse_point.y()

        # find closest plot (if any)
        min_dist = float("inf")
        closest_substance = None
        closest_data_point = None
        for item in self.plotItem.listDataItems():
            x_data, y_data = item.getData()
            dist, data_point = distance_to_polyline(x, y, x_data, y_data)
            if dist < 1:
                if dist < min_dist:
                    min_dist = dist
                    # Check which substance this plot corresponds to
                    for substance, plots in self.item_map.items():
                        for plot in plots:
                            if plot is item:
                                closest_substance = substance
                                closest_data_point = data_point
                                break
                assert closest_substance  # We should always find a plot

        if closest_substance is not None:
            self.mouseLabel.setText("(%0.1f, %0.1f)" % (closest_data_point[0], closest_data_point[1]))
            self.mouseLabel.setPos(x, y)
            self.mouseMarker.setVisible(True)
            self.mouseMarker.setData([closest_data_point[0]], [closest_data_point[1]])
        else:
            self.mouseLabel.setText("")
            self.mouseMarker.setVisible(False)

        self.hover_plot.emit(closest_substance)

    def item_color_changed(self, color_model_item):
        if not self.item_map:  # No plots yet
            return

        # Retrieve the substance name from the model
        row = color_model_item.index().row()
        selected_model_item = color_model_item.model().item(row, 0)
        substance = selected_model_item.data()

        style, color, width = color_model_item.data()[0]
        pen = pg.mkPen(color=QColor(*color), width=width, style=style)
        self.item_map[substance][0].setPen(pen)

        if len(self.item_map[substance]) == 2:
            # there is a fill, also change that color
            fill_color = reduce_saturation(QColor(*color))
            self.item_map[substance][1].setBrush(pg.mkBrush(fill_color))

    def highlight_plot(self, row):

        if not self.item_map:  # No plots yet
            return

        self.unhighlight_plots()

        hovered_model_item = self.fraction_model.item(row, 0)
        substance = hovered_model_item.data()

        hovered_color_item = self.fraction_model.item(row, 1)
        # Original color
        style, color, width = hovered_color_item.data()[1]
        highlight_color = increase_value(QColor(*color))
        pen = pg.mkPen(color=highlight_color, width=width, style=style)
        self.item_map[substance][0].setPen(pen)
        # also set fill color
        if len(self.item_map[substance]) == 2:
            self.item_map[substance][1].setBrush(pg.mkBrush(highlight_color))

    def unhighlight_plots(self):
        if not self.item_map:  # No plots yet
            return

        for row in range(self.fraction_model.rowCount()):
            substance = self.fraction_model.item(row, 0).data()
            # original color
            style, color, width = self.fraction_model.item(row, 1).data()[1]

            pen = pg.mkPen(color=QColor(*color), width=width, style=style)
            self.item_map[substance][0].setPen(pen)
            if len(self.item_map[substance]) == 2:
                fill_color = reduce_saturation(QColor(*color))
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
                fill_color = reduce_saturation(plot_color)
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
