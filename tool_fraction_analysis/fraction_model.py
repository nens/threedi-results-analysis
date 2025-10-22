from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtGui import QStandardItem
from qgis.PyQt.QtGui import QStandardItemModel
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem
from threedi_results_analysis.utils.color import increase_value
import logging
import numpy as np
import pyqtgraph as pg


logger = logging.getLogger(__name__)

FRACTION_COLOR_LIST = [
    (135, 86, 146),  # paars
    (243, 132, 0),  # oranje
    (190, 0, 50),  # rood
    (194, 178, 128),  # beige
    (0, 136, 86),  # groen
    (161, 202, 241),  # lichtblauw
    (230, 143, 172),
    (0, 103, 165),
    (249, 147, 121),
    (96, 78, 151),
    (246, 166, 0),
    (179, 68, 108),
    (220, 211, 0),
    (136, 45, 23),
    (141, 182, 0),
    (101, 69, 34),
    (226, 88, 34),
    (43, 61, 38),
]


class FractionModel(QStandardItemModel):

    def __init__(self, parent, result_model):
        super().__init__(parent)
        self.result_model = result_model
        self.setHorizontalHeaderLabels(["active", "pattern", "substance"])
        self.result_item = None
        # To prevent tedious updates in model
        self.highlighted_row = None

    def clear(self):
        self.result_item = None
        self.none_highlighted = True
        super().clear()

    @pyqtSlot(str)
    def highlight_substance(self, substance_name: str):
        if not substance_name and self.highlighted_row is None:
            # Nothing needs to be highlight, and nothing needs to be reset
            return
        if not substance_name:
            self.highlighted_row = None

        # First do quick check whether something needs to be updated at all
        for row in range(self.rowCount()):
            substance_checked_item = self.item(row, 0)
            substance = substance_checked_item.data()
            if substance == substance_name and self.highlighted_row == row:
                # The highlighting did not change
                return

        for row in range(self.rowCount()):
            substance_checked_item = self.item(row, 0)
            substance = substance_checked_item.data()
            self._highlight(row, substance == substance_name)
            if substance == substance_name:
                self.highlighted_row = row

    @pyqtSlot(str)
    def highlight_row(self, row: int):
        for row_idx in range(self.rowCount()):
            if row_idx == row:
                self.highlighted_row = row
            self._highlight(row_idx, row_idx == row)

    def _highlight(self, row, highlight: bool):
        substance_name_item = self.item(row, 2)
        font = substance_name_item.font()

        # Set to highlight color or original color and width
        hovered_color_item = self.item(row, 1)
        if not highlight:
            style, color, _ = hovered_color_item.data()[1]
            hovered_color_item.setData(((style, color, 2), (style, color, 2)))
            font.setBold(False)
            substance_name_item.setFont(font)
        else:
            style, color, _ = hovered_color_item.data()[1]
            highlight_color = increase_value(QColor(*color))
            highlight_color = (highlight_color.red(), highlight_color.green(), highlight_color.blue())
            hovered_color_item.setData(((style, highlight_color, 4), (style, color, 2)))
            font.setBold(True)
            substance_name_item.setFont(font)

    def set_fraction(self, item: ThreeDiResultItem, substance: str):
        self.clear()

        self.setHorizontalHeaderLabels(["active", "pattern", "substance"])
        self.result_item = item

        # Retrieve the substances
        threedi_result = self.result_item.threedi_result
        water_quality_vars = threedi_result.available_water_quality_vars

        # We'll alphabetically sort them
        water_quality_vars = sorted(water_quality_vars, key=lambda x: x["name"] or x["parameters"])
        for wq_var in water_quality_vars:
            if wq_var["unit"] != substance:
                continue
            color_item = QStandardItem()
            # store current and original color and width
            color_item.setData(((Qt.PenStyle.SolidLine, self.get_new_color(), 2), (Qt.PenStyle.SolidLine, self.get_new_color(), 2)))
            color_item.setEditable(False)
            # Display the "name" if present, otherwise parameter name
            substance_name = wq_var["name"] or wq_var["parameters"]
            substance_item = QStandardItem(substance_name)
            substance_item.setEditable(False)
            check_item = QStandardItem("")
            check_item.setCheckable(True)
            check_item.setEditable(False)
            check_item.setCheckState(Qt.CheckState.Checked)
            check_item.setData(wq_var["parameters"])
            self.appendRow([check_item, color_item, substance_item])

    def get_new_color(self) -> QColor:
        return FRACTION_COLOR_LIST[self.rowCount() % len(FRACTION_COLOR_LIST)]

    def create_plots(self, feature_id, time_units, stacked, volume, unit_conversion):
        plots = []
        cumulative_ts_table = None

        if volume:
            volume_series = self.timeseries_table("vol", feature_id, time_units=time_units)

        for row in range(self.rowCount()):
            style, color, width = self.item(row, 1).data()[0]  # current
            pen = pg.mkPen(color=QColor(*color), width=width, style=style)
            substance = self.item(row, 0).data()
            visible = (self.item(row, 0).checkState() == Qt.CheckState.Checked)
            ts_table = self.timeseries_table(substance, feature_id, time_units=time_units)

            if volume:
                # Some conversion for convenient volume units
                ts_table = ts_table * unit_conversion
                # multiply with nodes' volume when volume_mode is selected
                ts_table[:, 1] = np.multiply(ts_table[:, 1], volume_series[:, 1])

            if stacked:
                if cumulative_ts_table is not None:
                    ts_table[:, 1] = np.add(ts_table[:, 1], cumulative_ts_table)
                cumulative_ts_table = ts_table[:, 1]  # Don't sum the timekeys

            plot = pg.PlotDataItem(ts_table, pen=pen)
            plots.append((substance, plot, visible))

        return plots

    def timeseries_table(self, substance, id, time_units):
        timeseries = self.result_item.threedi_result.get_timeseries(
            substance, node_id=id, fill_value=np.NaN
        )
        if timeseries.shape[1] == 1:
            logger.error("1-element timeserie, plotting empty serie")
            return np.array([], dtype=float)
        if time_units == "hrs":
            vector = np.array([3600, 1])
        elif time_units == "mins":
            vector = np.array([60, 1])
        else:
            vector = np.array([1, 1])
        return timeseries / vector
