from ..config.waterbalance.sum_configs import serie_settings
from ..models.wb_item import WaterbalanceItemModel
from ..utils.maptools.polygon_draw import PolygonDrawTool
from qgis.core import QgsCoordinateTransform
from qgis.core import QgsFeatureRequest
from qgis.core import QgsGeometry
from qgis.core import QgsProject
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import QEvent
from qgis.PyQt.QtCore import QMetaObject
from qgis.PyQt.QtCore import QSize
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QBrush
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtGui import QPalette
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtGui import QTransform
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtWidgets import QDockWidget
from qgis.PyQt.QtWidgets import QHBoxLayout
from qgis.PyQt.QtWidgets import QLabel
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtWidgets import QSizePolicy
from qgis.PyQt.QtWidgets import QSpacerItem
from qgis.PyQt.QtWidgets import QTableView
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.PyQt.QtWidgets import QWidget
from ThreeDiToolbox import PLUGIN_DIR
from ThreeDiToolbox.datasource.threedi_results import find_h5_file
from ThreeDiToolbox.tool_water_balance.views.custom_pg_Items import RotateLabelAxisItem
from threedigrid.admin.gridadmin import GridH5Admin

import copy
import functools
import logging
import numpy as np
import pyqtgraph as pg


logger = logging.getLogger(__name__)


serie_settings = {s["name"]: s for s in serie_settings}

# serie_name, index, modelpart for bars, modelpart for graph
INPUT_SERIES = [
    ("2d_in", 0, "2d", "2d"),
    ("2d_out", 1, "2d", "2d"),
    ("1d_in", 2, "1d", "1d"),
    ("1d_out", 3, "1d", "1d"),
    ("2d_bound_in", 4, "2d", "2d"),
    ("2d_bound_out", 5, "2d", "2d"),
    ("1d_bound_in", 6, "1d", "1d"),
    ("1d_bound_out", 7, "1d", "1d"),
    ("1d__1d_2d_flow_in", 8, "1d", "1d2d"),
    ("1d__1d_2d_flow_out", 9, "1d", "1d2d"),
    ("1d__1d_2d_exch_in", 10, "1d", "1d2d"),
    ("1d__1d_2d_exch_out", 11, "1d", "1d2d"),
    ("pump_in", 12, "1d", "1d"),
    ("pump_out", 13, "1d", "1d"),
    ("rain", 14, "2d", "2d"),
    ("infiltration_rate_simple", 15, "2d", "2d"),
    ("lat_2d", 16, "2d", "2d"),
    ("lat_1d", 17, "1d", "1d"),
    ("d_2d_vol", 18, "2d", "2d"),
    ("d_1d_vol", 19, "1d", "1d"),
    ("error_2d", 20, "error_2d", "2d"),
    ("error_1d", 21, "error_1d", "2d"),
    ("error_1d_2d", 22, "error_1d_2d", "2d"),
    ("2d_groundwater_in", 23, "2d", "2d"),
    ("2d_groundwater_out", 24, "2d", "2d"),
    ("d_2d_groundwater_vol", 25, "2d", "2d"),
    ("leak", 26, "2d", "2d"),
    ("inflow", 27, "1d", "1d"),
    ("2d_vertical_infiltration_pos", 28, "2d_vert", "2d_vert"),
    ("2d_vertical_infiltration_neg", 29, "2d_vert", "2d_vert"),
    ("2d__1d_2d_flow_in", 30, "2d", "1d2d"),
    ("2d__1d_2d_flow_out", 31, "2d", "1d2d"),
    ("2d__1d_2d_exch_in", 32, "2d", "1d2d"),
    ("2d__1d_2d_exch_out", 33, "2d", "1d2d"),
    ("intercepted_volume", 34, "2d", "2d"),
    ("q_sss", 35, "2d", "2d"),
]


# some helper functions
#######################


def _get_request_filter(ids):
    ids_flat = list(set([i for j in list(ids.values()) for i in j]))
    return QgsFeatureRequest().setFilterFids(ids_flat)


def _get_feature_iterator(layer, request_filter):
    # mainly pumps are often not present
    if layer:
        return layer.getFeatures(request_filter)
    else:
        return []


#######################


@functools.total_ordering
class Bar(object):
    """Bar for waterbalance barchart with positive and negative components."""

    SERIES_NAME_TO_INDEX = {name: idx for (name, idx, _, part) in INPUT_SERIES}

    def __init__(self, label_name, in_series, out_series, type):
        self.label_name = label_name
        self.in_series = in_series
        self.out_series = out_series
        self.type = type
        self._balance_in = None
        self._balance_out = None

    @staticmethod
    def _get_time_indices(ts, t1, t2):
        """Time series indices in range t1-t2."""
        idx_x1 = np.searchsorted(ts, t1)
        if not t2:
            idx_x2 = len(ts)
        else:
            idx_x2 = np.searchsorted(ts, t2)
        return np.arange(idx_x1, idx_x2)

    @property
    def end_balance_in(self):
        return self._balance_in

    def set_end_balance_in(self, ts, ts_series, t1=0, t2=None):
        idxs = [self.SERIES_NAME_TO_INDEX[name] for name in self.in_series]
        ts_indices_sliced = self._get_time_indices(ts, t1, t2)
        ts_deltas = np.concatenate(([0], np.diff(ts)))
        # shape = (N_idxs, len(ts))
        balance_tmp = (ts_deltas * ts_series[:, idxs].T).clip(min=0)
        self._balance_in = balance_tmp[:, ts_indices_sliced].sum()

    @property
    def end_balance_out(self):
        return self._balance_out

    def set_end_balance_out(self, ts, ts_series, t1=0, t2=None):
        idxs = [self.SERIES_NAME_TO_INDEX[name] for name in self.out_series]
        ts_indices_sliced = self._get_time_indices(ts, t1, t2)
        ts_deltas = np.concatenate(([0], np.diff(ts)))
        balance_tmp = (ts_deltas * ts_series[:, idxs].T).clip(max=0)
        self._balance_out = balance_tmp[:, ts_indices_sliced].sum()

    def calc_balance(self, ts, ts_series, t1=0, t2=None):
        """Calculate balance values."""
        self.set_end_balance_in(ts, ts_series, t1, t2)
        self.set_end_balance_out(ts, ts_series, t1, t2)
        if self.is_storage_like:
            self.convert_to_net()

    def convert_to_net(self):
        """Make a bar that contains the net value (positive or negative)."""
        # NOTE: use addition because out is negative
        net_val = self._balance_in + self._balance_out
        if net_val > 0:
            self._balance_in = net_val
            self._balance_out = 0
        else:
            self._balance_in = 0
            self._balance_out = net_val

    def invert(self):
        """Flip positive to negative and vice versa."""
        self._balance_in, self._balance_out = (
            -1 * self._balance_out,
            -1 * self._balance_in,
        )

    @property
    def is_storage_like(self):
        return "storage" in self.label_name

    # add sorting
    def __lt__(self, other):
        # TODO: label_names are not unique, should add 'type' to make a
        # primary key
        if not self.is_storage_like and other.is_storage_like:
            return True
        elif self.is_storage_like and not other.is_storage_like:
            return False
        return self.label_name < other.label_name


class BarManager(object):
    def __init__(self, series):
        self.series = series
        self.bars = sorted(
            [
                Bar(
                    label_name=x["label_name"],
                    in_series=x["in"],
                    out_series=x["out"],
                    type=x["type"],
                )
                for x in series
            ]
        )

    def calc_balance(self, ts, ts_series, t1, t2, net=False, invert=[]):
        for b in self.bars:
            b.calc_balance(ts, ts_series, t1=t1, t2=t2)
            if net:
                b.convert_to_net()
            if b.label_name in invert:
                b.invert()

    @property
    def x(self):
        return np.arange(len(self.bars))

    @property
    def xlabels(self):
        return [b.label_name for b in self.bars]

    @property
    def end_balance_in(self):
        return [b.end_balance_in for b in self.bars]

    @property
    def end_balance_out(self):
        return [b.end_balance_out for b in self.bars]


class WaterbalanceItemTable(QTableView):
    hoverExitRow = pyqtSignal(int)
    hoverExitAllRows = pyqtSignal()  # exit the whole widget
    hoverEnterRow = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QTreeView::item:hover{background-color:#FFFF00;}")
        self.setMouseTracking(True)
        self.model = None

        self._last_hovered_row = None
        self.viewport().installEventFilter(self)

    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """
        self.setMouseTracking(False)
        self.viewport().removeEventFilter(self)

    def closeEvent(self, event):
        """
        overwrite of QDockWidget class to emit signal
        :param event: QEvent
        """
        self.on_close()
        event.accept()

    def eventFilter(self, widget, event):
        if widget is self.viewport():

            if event.type() == QEvent.MouseMove:
                row = self.indexAt(event.pos()).row()
                if row == 0 and self.model and row > self.model.rowCount():
                    row = None

            elif event.type() == QEvent.Leave:
                row = None
                self.hoverExitAllRows.emit()
            else:
                row = self._last_hovered_row

            if row != self._last_hovered_row:
                if self._last_hovered_row is not None:
                    try:
                        self.hover_exit(self._last_hovered_row)
                    except IndexError:
                        logger.warning(
                            "Hover row index %s out of range", self._last_hovered_row
                        )
                        # self.hoverExitRow.emit(self._last_hovered_row)
                # self.hoverEnterRow.emit(row)
                if row is not None:
                    try:
                        self.hover_enter(row)
                    except IndexError:
                        logger.warning("Hover row index %s out of range", row),
                self._last_hovered_row = row
                pass
        return QTableView.eventFilter(self, widget, event)

    def hover_exit(self, row_nr):
        if row_nr >= 0:
            item = self.model.rows[row_nr]
            name = item.name.value

            if name in [
                "volume change",
                "volume change 2D",
                "volume change groundwater",
                "volume change 1D",
            ]:
                item.fill_color.value = item.fill_color.value[:3] + [0]
                item.pen_color.value = item.pen_color.value[:3] + [180]
            else:
                item.fill_color.value = item.fill_color.value[:3] + [150]
                item.pen_color.value = item.pen_color.value[:3] + [180]

            item.hover.value = False

    def hover_enter(self, row_nr):
        if row_nr >= 0:
            item = self.model.rows[row_nr]
            name = item.name.value
            self.hoverEnterRow.emit(name)

            if name in [
                "volume change",
                "volume change 2D",
                "volume change groundwater",
                "volume change 1D",
            ]:
                item.fill_color.value = item.fill_color.value[:3] + [0]
                item.pen_color.value = item.pen_color.value[:3] + [255]
            else:
                item.fill_color.value = item.fill_color.value[:3] + [220]
                item.pen_color.value = item.pen_color.value[:3] + [255]

            item.hover.value = True

    def setModel(self, model):
        super().setModel(model)

        self.model = model

        self.resizeColumnsToContents()
        self.model.set_column_sizes_on_view(self)


class WaterBalancePlotWidget(pg.PlotWidget):
    def __init__(self, parent=None, name=""):

        super().__init__(parent)
        self.name = name
        self.showGrid(True, True, 0.5)
        self.setLabel("bottom", "time", "hrs")
        self.setLabel("left", "flow", "m3/s")
        # Auto SI prefix scaling doesn't work properly with m3, m2 etc.
        self.getAxis("left").enableAutoSIPrefix(False)
        self.series = {}

    def setModel(self, model):
        self.model = model
        self.model.dataChanged.connect(self.data_changed)
        self.model.rowsInserted.connect(self.on_insert)
        self.model.rowsAboutToBeRemoved.connect(self.on_remove)

    def on_remove(self):
        self.draw_timeseries()

    def on_insert(self):
        self.draw_timeseries()

    def draw_timeseries(self):

        self.clear()

        ts = self.model.ts
        zeros = np.zeros(shape=(np.size(ts, 0),))
        zero_serie = pg.PlotDataItem(
            x=ts,
            y=zeros,
            connect="finite",
            pen=pg.mkPen(color=QColor(0, 0, 0, 200), width=1),
        )
        self.addItem(zero_serie, ignoreBounds=True)

        # all item.name.value (e.g. '1d-2d flow', 'pumps', 'rain') have both a
        # 'in' and 'out' flow: so two lines that together form a graph.
        # However the volume change lines in item.name.value ('volume change',
        # 'volume change 2d', 'volume change groundwater', and
        # 'volume change 1d' are summed into 1 line (so no out and in)
        for dir in ["in", "out"]:
            prev_serie = zeros
            prev_pldi = zero_serie
            for item in self.model.rows:
                if item.active.value and item.name.value in [
                    "volume change",
                    "volume change 2D",
                    "volume change groundwater",
                    "volume change 1D",
                ]:
                    pen_color = item.pen_color.value
                    not_cum_serie = (
                        item.ts_series.value["in"] + item.ts_series.value["out"]
                    )
                    plot_item = pg.PlotDataItem(
                        x=ts,
                        y=not_cum_serie,
                        connect="finite",
                        pen=pg.mkPen(
                            color=QColor(*pen_color), width=4, style=Qt.DashDotLine
                        ),
                    )
                    # only get 1 line (the sum of 'in' and 'out')
                    item._plots["sum"] = plot_item

                if item.active.value and item.name.value not in [
                    "volume change",
                    "volume change 2D",
                    "volume change groundwater",
                    "volume change 1D",
                ]:
                    pen_color = item.pen_color.value
                    fill_color = item.fill_color.value
                    cum_serie = prev_serie + item.ts_series.value[dir]
                    plot_item = pg.PlotDataItem(
                        x=ts,
                        y=cum_serie,
                        connect="finite",
                        pen=pg.mkPen(color=QColor(*pen_color), width=1),
                    )
                    fill = pg.FillBetweenItem(
                        prev_pldi, plot_item, pg.mkBrush(*fill_color)
                    )
                    # keep reference
                    item._plots[dir] = plot_item
                    item._plots[dir + "fill"] = fill
                    prev_serie = cum_serie
                    prev_pldi = plot_item

        # add PlotItems to graph
        y_min = 0
        y_max = 0
        x_min = 0
        x_max = 0
        for dir in ["in", "out"]:
            for item in reversed(self.model.rows):
                if item.active.value:
                    if item.name.value in [
                        "volume change",
                        "volume change 2D",
                        "volume change groundwater",
                        "volume change 1D",
                    ]:
                        self.addItem(item._plots["sum"], ignoreBounds=True)

                        # determine PlotItem min and max for display range
                        y_min = min(y_min, min(item._plots["sum"].yData))
                        y_max = max(y_max, max(item._plots["sum"].yData))
                        x_min = min(x_min, min(item._plots["sum"].xData))
                        x_max = max(x_max, max(item._plots["sum"].xData))
                    else:
                        self.addItem(item._plots[dir], ignoreBounds=True)
                        self.addItem(item._plots[dir + "fill"], ignoreBounds=True)

                        y_min = min(y_min, min(item._plots[dir].yData))
                        y_max = max(y_max, max(item._plots[dir].yData))
                        x_min = min(x_min, min(item._plots[dir].xData))
                        x_max = max(x_max, max(item._plots[dir].xData))
        # http://www.pyqtgraph.org/documentation/graphicsItems/viewbox.html
        # for some reason shows 'self.autoRange()' some weird behavior (each
        # time draw_timeseries() is called, the x-axis is extended by a factor
        # 4. With 'self.getPlotItem().viewRect()' one can follow this. So,
        # instead of self.autoRange(), we set the min,max of the X- and YRange
        # TODO: find out why autoRange() extends the x-axis by factor 4
        # self.autoRange()
        self.setYRange(y_min, y_max, padding=None, update=True)
        self.setXRange(x_min, x_max, padding=None, update=True)

    def data_changed(self, index):
        """
        change graphs based on changes in locations
        :param index: index of changed field
        """
        if self.model.columns[index.column()].name == "active":
            self.draw_timeseries()

        elif self.model.columns[index.column()].name == "hover":
            item = self.model.rows[index.row()]

            if item.hover.value:
                if item.active.value:
                    if "in" in item._plots:
                        item._plots["in"].setPen(color=item.pen_color.value, width=1)
                        item._plots["infill"].setBrush(
                            pg.mkBrush(item.fill_color.value)
                        )
                    if "out" in item._plots:
                        item._plots["out"].setPen(color=item.pen_color.value, width=1)
                        item._plots["outfill"].setBrush(
                            pg.mkBrush(item.fill_color.value)
                        )
                    if "sum" in item._plots:
                        item._plots["sum"].setPen(
                            color=item.pen_color.value, width=4, style=Qt.DashDotLine
                        )
            else:
                if item.active.value:
                    if "in" in item._plots:
                        item._plots["in"].setPen(color=item.pen_color.value, width=1)
                        item._plots["infill"].setBrush(
                            pg.mkBrush(item.fill_color.value)
                        )
                    if "out" in item._plots:
                        item._plots["out"].setPen(color=item.pen_color.value, width=1)
                        item._plots["outfill"].setBrush(
                            pg.mkBrush(item.fill_color.value)
                        )
                    if "sum" in item._plots:
                        item._plots["sum"].setPen(
                            color=item.pen_color.value, width=4, style=Qt.DashDotLine
                        )


class WaterBalanceWidget(QDockWidget):
    closingWidget = pyqtSignal()

    INPUT_SERIES = INPUT_SERIES

    IN_OUT_SERIES = [
        {
            # 'label_name': '1D: 1D-2D flow',
            "label_name": "1D: 2D flow to 1D",
            "in": ["1d__1d_2d_flow_in"],
            "out": ["1d__1d_2d_flow_out"],
            "type": "1d",
        },
        {
            # 'label_name': '2D: 1D-2D flow',
            "label_name": "2D: 2D flow to 1D",
            "in": ["2d__1d_2d_flow_in"],
            "out": ["2d__1d_2d_flow_out"],
            "type": "2d",
        },
        {
            # 'label_name': '1D-2D flow (all domains)',
            "label_name": "2D flow to 1D (all domains)",
            # does this make sense?
            "in": ["1d__1d_2d_flow_in", "2d__1d_2d_flow_in"],
            "out": ["1d__1d_2d_flow_out", "2d__1d_2d_flow_out"],
            "type": "NETVOL",
        },
        {
            # 'label_name': '1D: 1D-2D exchange',
            "label_name": "1D: 2D flow to 1D (domain exchange)",
            "in": ["1d__1d_2d_exch_in"],
            "out": ["1d__1d_2d_exch_out"],
            "type": "1d",
        },
        {
            # 'label_name': '2D: 1D-2D exchange',
            "label_name": "2D: 2D flow to 1D (domain exchange)",
            "in": ["2d__1d_2d_exch_in"],
            "out": ["2d__1d_2d_exch_out"],
            "type": "2d",
        },
        {
            "label_name": "net change in storage",
            "in": ["d_2d_vol"],
            "out": ["d_2d_vol"],
            "type": "2d",
        },
        {
            "label_name": "net change in storage",
            "in": ["d_1d_vol"],
            "out": ["d_1d_vol"],
            "type": "1d",
        },
        {
            "label_name": "net change in storage",
            "in": ["d_2d_groundwater_vol"],
            "out": ["d_2d_groundwater_vol"],
            "type": "2d_groundwater",
        },
        {
            "label_name": "leakage",
            "in": ["leak"],
            "out": ["leak"],
            "type": "2d_groundwater",
        },
        {
            "label_name": "constant infiltration",
            "in": ["infiltration_rate_simple"],
            "out": ["infiltration_rate_simple"],
            "type": "2d",
        },
        {"label_name": "2D flow", "in": ["2d_in"], "out": ["2d_out"], "type": "2d"},
        {"label_name": "1D flow", "in": ["1d_in"], "out": ["1d_out"], "type": "1d"},
        {
            "label_name": "groundwater flow",
            "in": ["2d_groundwater_in"],
            "out": ["2d_groundwater_out"],
            "type": "2d_groundwater",
        },
        {
            "label_name": "lateral flow to 2D",
            "in": ["lat_2d"],
            "out": ["lat_2d"],
            "type": "2d",
        },
        {
            "label_name": "lateral flow to 1D",
            "in": ["lat_1d"],
            "out": ["lat_1d"],
            "type": "1d",
        },
        {
            "label_name": "2D boundary flow",
            "in": ["2d_bound_in"],
            "out": ["2d_bound_out"],
            "type": "2d",
        },
        {
            "label_name": "1D boundary flow",
            "in": ["1d_bound_in"],
            "out": ["1d_bound_out"],
            "type": "1d",
        },
        {
            "label_name": "0D rainfall runoff on 1D",
            "in": ["inflow"],
            "out": ["inflow"],
            "type": "1d",
        },
        {
            "label_name": "in/exfiltration (domain exchange)",
            # NOTE: for the argument why pos is out and neg is in, see the
            # comment in ``WaterBalanceCalculation.get_aggregated_flows``
            "in": ["2d_vertical_infiltration_neg"],
            "out": ["2d_vertical_infiltration_pos"],
            "type": "2d_vert",
        },
        {
            "label_name": "change in storage",
            "in": ["d_2d_vol", "d_2d_groundwater_vol", "d_1d_vol"],
            "out": ["d_2d_vol", "d_2d_groundwater_vol", "d_1d_vol"],
            "type": "NETVOL",
        },
        {"label_name": "pump", "in": ["pump_in"], "out": ["pump_out"], "type": "1d"},
        {"label_name": "rain on 2D", "in": ["rain"], "out": ["rain"], "type": "2d"},
        {
            "label_name": "interception",
            "in": ["intercepted_volume"],
            "out": ["intercepted_volume"],
            "type": "2d",
        },
        {
            "label_name": "surface sources and sinks",
            "in": ["q_sss"],
            "out": ["q_sss"],
            "type": "2d",
        },
    ]

    def __init__(self, parent=None, iface=None, ts_datasources=None, wb_calc=None):
        """Constructor."""
        super().__init__(parent)

        self.iface = iface
        self.ts_datasources = ts_datasources
        self.calc = wb_calc

        # setup ui
        self.setup_ui(self)

        self.model = WaterbalanceItemModel()
        self.wb_item_table.setModel(self.model)
        self.plot_widget.setModel(self.model)

        # link tool
        self.polygon_tool = PolygonDrawTool(
            self.iface.mapCanvas(), self.select_polygon_button, self.on_polygon_ready
        )

        # fill comboboxes with selections
        self.modelpart_combo_box.insertItems(0, ["1d and 2d", "1d", "2d"])
        self.sum_type_combo_box.insertItems(0, list(serie_settings.keys()))
        self.agg_combo_box.insertItems(0, ["m3/s", "m3 cumulative"])
        self.ts_units_combo_box.insertItems(0, ["hrs", "mins", "s"])

        # add listeners
        self.select_polygon_button.toggled.connect(self.toggle_polygon_button)
        self.reset_waterbalans_button.clicked.connect(self.reset_waterbalans)
        self.chart_button.clicked.connect(self.show_barchart)
        # self.polygon_tool.deactivated.connect(self.update_wb)
        self.modelpart_combo_box.currentIndexChanged.connect(self.update_wb)
        self.sum_type_combo_box.currentIndexChanged.connect(self.update_wb)
        self.agg_combo_box.currentIndexChanged.connect(self.update_wb)
        self.ts_units_combo_box.currentIndexChanged.connect(self.update_wb)
        self.wb_item_table.hoverEnterRow.connect(self.hover_enter_map_visualization)
        self.wb_item_table.hoverExitAllRows.connect(self.hover_exit_map_visualization)
        self.activate_all_button.clicked.connect(self.activate_layers)
        self.deactivate_all_button.clicked.connect(self.deactivate_layers)

        # TODO: is this a good default?
        # initially turn on tool
        self.select_polygon_button.toggle()
        self.__current_calc = None  # cache the results of calculation

    def _get_io_series_net(self):
        io_series_net = [
            x
            for x in self.IN_OUT_SERIES
            if (
                x["type"] in ["2d", "2d_vert", "2d_groundwater", "1d"]
                and "storage" not in x["label_name"]
                and "exchange" not in x["label_name"]
                and x["label_name"] != "1D: 2D flow to 1D"
                and x["label_name"] != "2D: 2D flow to 1D"
                and x["label_name"] != "1D: 2D flow to 1D (domain exchange)"
                and x["label_name"] != "2D: 2D flow to 1D (domain exchange)"
            )
            or x["type"] == "NETVOL"
        ]
        return io_series_net

    def _get_io_series_2d(self):
        io_series_2d = [
            x
            for x in self.IN_OUT_SERIES
            if x["type"] in ["2d", "2d_vert"]
            and x["label_name"] != "1D: 2D flow to 1D"
            and x["label_name"] != "1D: 2D flow to 1D (domain exchange)"
        ]
        return io_series_2d

    def _get_io_series_2d_groundwater(self):
        io_series_2d_groundwater = [
            x for x in self.IN_OUT_SERIES if x["type"] in ["2d_groundwater", "2d_vert"]
        ]
        return io_series_2d_groundwater

    def _get_io_series_1d(self):
        io_series_1d = [
            x
            for x in self.IN_OUT_SERIES
            if x["type"] == "1d"
            and x["label_name"] != "2D: 2D flow to 1D"
            and x["label_name"] != "2D: 2D flow to 1D (domain exchange)"
        ]
        return io_series_1d

    def show_barchart(self):

        # only possible to calculate bars when a polygon has been drawn
        if self.select_polygon_button.text() == "Finalize polygon":
            return

        # always use domain '1d and 2d' to get all flows in the barchart
        wb_barchart_modelpart = "1d and 2d"
        ts, ts_series = self.calc_wb_barchart(wb_barchart_modelpart)

        io_series_net = self._get_io_series_net()
        io_series_2d = self._get_io_series_2d()
        io_series_2d_groundwater = self._get_io_series_2d_groundwater()
        io_series_1d = self._get_io_series_1d()

        # get timeseries x range in plot widget
        viewbox_state = self.plot_widget.getPlotItem().getViewBox().getState()
        view_range = viewbox_state["viewRange"]
        t1, t2 = view_range[0]

        bm_net = BarManager(io_series_net)
        bm_2d = BarManager(io_series_2d)
        bm_2d_groundwater = BarManager(io_series_2d_groundwater)
        bm_1d = BarManager(io_series_1d)

        bm_net.calc_balance(ts, ts_series, t1, t2, net=True)
        bm_2d.calc_balance(ts, ts_series, t1, t2)
        bm_2d_groundwater.calc_balance(
            ts, ts_series, t1, t2, invert=["in/exfiltration (domain exchange)"]
        )
        bm_1d.calc_balance(ts, ts_series, t1, t2)

        nc_path = self.ts_datasources.rows[0].threedi_result().file_path
        h5 = find_h5_file(nc_path)
        ga = GridH5Admin(h5)

        t_start = max(0, t1)
        try:
            short_model_slug = ga.model_slug.rsplit("-", 1)[0]
        except Exception:
            logger.exception(
                "TODO: overly broad exception while splitting model_slug. "
                "Using model_name"
            )
            short_model_slug = ga.model_name

        self.wb_barchart_widget = pg.GraphicsView()
        layout = pg.GraphicsLayout()
        self.wb_barchart_widget.setCentralItem(layout)
        text = "Water balance from t=%.2f to t=%.2f \n Model name: %s" % (
            t_start,
            t2,
            short_model_slug,
        )
        layout.addLabel(text, row=0, col=0, colspan=3)

        self.wb_barchart_widget.setWindowTitle("Waterbalance")
        self.wb_barchart_widget.resize(1000, 600)
        self.wb_barchart_widget.show()

        def get_keyword_indexes(input_list, keyword):
            """Return a list of indexes from `input_list` which contain the
            `keyword`"""
            bar_indexes_to_mark = []
            for index, label in enumerate(input_list):
                if keyword in label:
                    bar_indexes_to_mark.append(index)
            return bar_indexes_to_mark

        # We want to mark some bars with a different color. Labels with the key
        # 'domain exchange' and the last label ('change in storage').
        domain_exchange_key = "(domain exchange)"
        standard_in_brush = QBrush(QColor(0, 122, 204))
        standard_out_brush = QBrush(QColor(255, 128, 0))

        domain_exchange_in_brush = QBrush(
            QColor(0, 122, 204), style=Qt.BDiagPattern
        )  # Qt.BDiagPattern
        domain_exchange_in_brush.setTransform(QTransform().scale(0.01, 0.01))
        domain_exchange_out_brush = QBrush(QColor(255, 128, 0), style=Qt.BDiagPattern)
        domain_exchange_out_brush.setTransform(QTransform().scale(0.01, 0.01))
        change_storate_brush = QBrush(QColor("grey"))

        # #####
        # Net #
        # #####

        domain_exchange_indexes = get_keyword_indexes(
            bm_net.xlabels, domain_exchange_key
        )
        in_brushes = [standard_in_brush] * (len(bm_net.xlabels) - 1)
        for i in domain_exchange_indexes:
            in_brushes[i] = domain_exchange_in_brush
        in_brushes.append(change_storate_brush)
        out_brushes = [standard_out_brush] * (len(bm_net.xlabels) - 1)
        for i in domain_exchange_indexes:
            out_brushes[i] = domain_exchange_out_brush
        out_brushes.append(change_storate_brush)

        bg_net_in = pg.BarGraphItem(
            x=bm_net.x, height=bm_net.end_balance_in, width=0.6, brushes=in_brushes
        )
        bg_net_out = pg.BarGraphItem(
            x=bm_net.x, height=bm_net.end_balance_out, width=0.6, brushes=out_brushes
        )
        axis_net = RotateLabelAxisItem(25, "bottom")
        net_plot = layout.addPlot(
            row=1, col=0, colspan=2, axisItems={"bottom": axis_net}
        )
        net_plot.addItem(bg_net_in)
        net_plot.addItem(bg_net_out)
        axis_net.setHeight(100)
        axis_net.setTicks([list(zip(bm_net.x, bm_net.xlabels))])

        net_plot.setTitle("Net water balance")
        y_axis = net_plot.getAxis("left")
        y_axis.setLabel("volume (m³)")
        net_plot.getViewBox().setLimits(xMin=-1, xMax=max(bm_net.x) + 2)

        # # ######
        # # Logo #
        # # ######

        path_3di_logo = str(PLUGIN_DIR / "icons" / "icon.png")
        logo_3di = QPixmap(path_3di_logo)
        logo_3di = logo_3di.scaledToHeight(40)
        label_3di = QLabel()
        label_3di.setPixmap(logo_3di)

        path_topsector_logo = str(PLUGIN_DIR / "icons" / "topsector_small.png")
        logo_topsector = QPixmap(path_topsector_logo)
        logo_topsector = logo_topsector.scaledToHeight(40)
        label_topsector = QLabel()
        label_topsector.setPixmap(logo_topsector)

        path_deltares_logo = str(PLUGIN_DIR / "icons" / "deltares_small.png")
        logo_deltares = QPixmap(path_deltares_logo)
        logo_deltares = logo_deltares.scaledToHeight(40)
        label_deltares = QLabel()
        label_deltares.setPixmap(logo_deltares)

        logo_label_text = QLabel("Powered by 3Di, Topsector Water and Deltares")

        powered_by_widget = QWidget()
        pallete = QPalette(QColor("white"))
        powered_by_widget.setAutoFillBackground(True)
        powered_by_widget.setPalette(pallete)
        powered_by_layout = QVBoxLayout()
        powered_by_widget.setMaximumHeight(130)

        logo_container = QWidget()
        logo_container.setMaximumWidth(300)
        logo_container_layout = QHBoxLayout()
        logo_container_layout.addWidget(label_3di)
        logo_container_layout.addWidget(label_topsector)
        logo_container_layout.addWidget(label_deltares)
        logo_container.setLayout(logo_container_layout)

        powered_by_layout.addWidget(logo_label_text)
        powered_by_layout.addWidget(logo_container)

        powered_by_widget.setLayout(powered_by_layout)
        logo_ProxyWidget = layout.scene().addWidget(powered_by_widget)
        layout.addItem(logo_ProxyWidget, row=1, col=2)

        # # ####
        # # 2D #
        # # ####

        domain_exchange_indexes = get_keyword_indexes(
            bm_2d.xlabels, domain_exchange_key
        )
        in_brushes = [standard_in_brush] * (len(bm_2d.xlabels) - 1)
        for i in domain_exchange_indexes:
            in_brushes[i] = domain_exchange_in_brush
        in_brushes.append(change_storate_brush)
        out_brushes = [standard_out_brush] * (len(bm_2d.xlabels) - 1)
        for i in domain_exchange_indexes:
            out_brushes[i] = domain_exchange_out_brush
        out_brushes.append(change_storate_brush)

        surface_in = pg.BarGraphItem(
            x=bm_2d.x, height=bm_2d.end_balance_in, width=0.6, brushes=in_brushes
        )
        surface_out = pg.BarGraphItem(
            x=bm_2d.x, height=bm_2d.end_balance_out, width=0.6, brushes=out_brushes
        )
        axis_surface = RotateLabelAxisItem(25, "bottom")
        surface_plot = layout.addPlot(row=2, col=0, axisItems={"bottom": axis_surface})
        surface_plot.addItem(surface_in)
        surface_plot.addItem(surface_out)
        axis_surface.setHeight(100)
        axis_surface.setTicks([list(zip(bm_net.x, bm_2d.xlabels))])

        surface_plot.setTitle("2D surface water domain")
        y_axis = surface_plot.getAxis("left")
        y_axis.setLabel("volume (m³)")
        surface_plot.getViewBox().setLimits(xMin=-1, xMax=max(bm_2d.x) + 2)

        # # ################
        # # 2D groundwater #
        # # ################

        domain_exchange_indexes = get_keyword_indexes(
            bm_2d_groundwater.xlabels, domain_exchange_key
        )
        in_brushes = [standard_in_brush] * (len(bm_2d_groundwater.xlabels) - 1)
        for i in domain_exchange_indexes:
            in_brushes[i] = domain_exchange_in_brush
        in_brushes.append(change_storate_brush)
        out_brushes = [standard_out_brush] * (len(bm_2d_groundwater.xlabels) - 1)
        for i in domain_exchange_indexes:
            out_brushes[i] = domain_exchange_out_brush
        out_brushes.append(change_storate_brush)

        groundwater_in = pg.BarGraphItem(
            x=bm_2d_groundwater.x,
            height=bm_2d_groundwater.end_balance_in,
            width=0.6,
            brushes=in_brushes,
        )
        groundwater_out = pg.BarGraphItem(
            x=bm_2d_groundwater.x,
            height=bm_2d_groundwater.end_balance_out,
            width=0.6,
            brushes=out_brushes,
        )
        axis_groundwater = RotateLabelAxisItem(25, "bottom")
        groundwater_plot = layout.addPlot(
            row=2, col=1, axisItems={"bottom": axis_groundwater}
        )
        groundwater_plot.addItem(groundwater_in)
        groundwater_plot.addItem(groundwater_out)
        axis_groundwater.setHeight(100)
        axis_groundwater.setTicks(
            [list(zip(bm_2d_groundwater.x, bm_2d_groundwater.xlabels))]
        )

        groundwater_plot.setTitle("2D groundwater domain")
        y_axis = groundwater_plot.getAxis("left")
        y_axis.setLabel("volume (m³)")
        groundwater_plot.getViewBox().setLimits(
            xMin=-1, xMax=max(bm_2d_groundwater.x) + 2
        )

        # # ####
        # # 1D #
        # # ####

        domain_exchange_indexes = get_keyword_indexes(
            bm_1d.xlabels, domain_exchange_key
        )
        in_brushes = [standard_in_brush] * (len(bm_1d.xlabels) - 1)
        for i in domain_exchange_indexes:
            in_brushes[i] = domain_exchange_in_brush
        in_brushes.append(change_storate_brush)
        out_brushes = [standard_out_brush] * (len(bm_1d.xlabels) - 1)
        for i in domain_exchange_indexes:
            out_brushes[i] = domain_exchange_out_brush
        out_brushes.append(change_storate_brush)

        network1d_in = pg.BarGraphItem(
            x=bm_1d.x, height=bm_1d.end_balance_in, width=0.6, brushes=in_brushes
        )
        network1d_out = pg.BarGraphItem(
            x=bm_1d.x, height=bm_1d.end_balance_out, width=0.6, brushes=out_brushes
        )
        axis_network1d = RotateLabelAxisItem(25, "bottom")
        network1d_plot = layout.addPlot(
            row=2, col=2, axisItems={"bottom": axis_network1d}
        )
        network1d_plot.addItem(network1d_in)
        network1d_plot.addItem(network1d_out)
        axis_network1d.setHeight(100)
        axis_network1d.setTicks([list(zip(bm_1d.x, bm_1d.xlabels))])

        network1d_plot.setTitle("1D network domain")
        y_axis = network1d_plot.getAxis("left")
        y_axis.setLabel("volume (m³)")
        network1d_plot.getViewBox().setLimits(xMin=-1, xMax=max(bm_1d.x) + 2)

        # Link y-axes
        surface_plot.setYLink(groundwater_plot)
        surface_plot.setYLink(network1d_plot)
        network1d_plot.setYLink(groundwater_plot)

        # Set y-range so all bars are visible
        y_min = min(
            bm_2d.end_balance_out
            + bm_2d_groundwater.end_balance_out
            + bm_1d.end_balance_out
        )
        y_max = max(
            bm_2d.end_balance_in
            + bm_2d_groundwater.end_balance_in
            + bm_1d.end_balance_in
        )
        network1d_plot.setYRange(min=y_min, max=y_max)

    def hover_enter_map_visualization(self, name):
        """On hover rubberband visualisation using the table item name.

        Uses the cached self.qgs_lines/self.qgs_points.
        """
        if self.select_polygon_button.isChecked():
            # highlighting when drawing the polygon doesn't look right.
            # this is the best solution I can think of atm...
            return

        # TODO 1: generate this dict

        # TODO 2: using the name as key is INCREDIBLY error prone: one
        # spelling mistake or a change in sum_configs and it doesn't work
        # anymore, and because we also catch the KeyErrors you won't even
        # notice. NEEDS TO BE FIXED

        NAME_TO_LINE_TYPES_SHOW_ALL = {
            "2D flow": ["2d"],
            "2D boundary flow": ["2d_bound"],
            "1D flow": ["1d"],
            "1D boundary flow": ["1d_bound"],
            "2D flow to 1D (domain exchange)": ["1d_2d_exch"],
            "2D flow to 1D": ["1d__1d_2d_flow", "2d__1d_2d_flow"],
            # TODO: 'pumps_hoover' is a magic string that we ad-hoc created
            # in the 'prepare_and_visualize_selection' function.
            # A better solution would be nice...
            "pumps": ["pumps_hoover"],
            "groundwater flow": ["2d_groundwater"],
            "in/exfiltration (domain exchange)": [
                "2d_vertical_infiltration_pos",
                "2d_vertical_infiltration_neg",
            ],
        }
        NAME_TO_LINE_TYPES_SHOW_MAIN_FLOW = {
            "2D flow": ["2d", "2d_bound"],
            "1D flow": ["1d", "pumps_hoover", "1d_bound"],
            "2D flow to 1D": ["1d__1d_2d_flow", "2d__1d_2d_flow"],
            "2D flow to 1D (domain exchange)": ["1d_2d_exch"],
            "groundwater flow": ["2d_groundwater"],
        }
        NAME_TO_NODE_TYPES = {
            "volume change": ["1d", "2d", "2d_groundwater"],
            "volume change 2D": ["2d"],
            "volume change 1D": ["1d"],
            "volume change groundwater": ["2d_groundwater"],
            "rain on 2D": ["2d"],
            "0D rainfall runoff on 1D": ["1d"],
            "lateral flow to 1D": ["1d"],
            "lateral flow to 2D": ["2d"],
            "leakage": ["2d"],
            "interception": ["2d"],
            "constant infiltration": ["2d"],
            "external (rain and laterals)": ["1d", "2d"],
            "surface sources and sinks": ["2d"],
        }

        # more hackery to fix keys defined in both 'show main flow' and
        # 'show all'
        sum_type = self.sum_type_combo_box.currentText()
        assert sum_type in ["show main flow", "show all"]
        if sum_type == "show main flow":
            name_to_line_type = NAME_TO_LINE_TYPES_SHOW_MAIN_FLOW
        elif sum_type == "show all":
            name_to_line_type = NAME_TO_LINE_TYPES_SHOW_ALL
        else:
            raise ValueError("Unknown type %s" % sum_type)

        line_geoms = []
        if name in name_to_line_type:
            types_line = name_to_line_type[name]
            for t in types_line:
                if t in self.qgs_lines:
                    geoms = self.qgs_lines[t]
                    line_geoms.extend(geoms)

        point_geoms = []
        if name in NAME_TO_NODE_TYPES:
            types_node = NAME_TO_NODE_TYPES[name]
            for t in types_node:
                if t in self.qgs_points:
                    geoms = self.qgs_points[t]
                    point_geoms.extend(geoms)

        self.polygon_tool.selection_vis.update(line_geoms, point_geoms)

    def hover_exit_map_visualization(self, *args):
        self.polygon_tool.selection_vis.reset()

    def on_polygon_ready(self, points):
        self.iface.mapCanvas().unsetMapTool(self.polygon_tool)

    def reset_waterbalans(self):
        self.polygon_tool.reset()

    def toggle_polygon_button(self):

        if self.select_polygon_button.isChecked():
            self.reset_waterbalans()

            self.iface.mapCanvas().setMapTool(self.polygon_tool)

            self.select_polygon_button.setText("Finalize polygon")
        else:
            self.iface.mapCanvas().unsetMapTool(self.polygon_tool)
            self.update_wb()
            self.select_polygon_button.setText("Draw new polygon")

    def activate_layers(self):
        for item in self.model.rows:
            item.active.value = True

    def deactivate_layers(self):
        for item in self.model.rows:
            item.active.value = False

    def get_modelpart_graph_layers(self, graph_layers):
        modelpart_graph_series = [
            x for x in graph_layers if x["layer_in_table"] is True
        ]
        return modelpart_graph_series

    def update_wb(self):
        ts, graph_series = self.calc_wb_graph(
            self.modelpart_combo_box.currentText(),
            self.agg_combo_box.currentText(),
            serie_settings[self.sum_type_combo_box.currentText()],
        )

        self.model.removeRows(0, len(self.model.rows))
        time_units = self.ts_units_combo_box.currentText()
        if time_units == "hrs":
            time_divisor = 3600
        elif time_units == "mins":
            time_divisor = 60
        else:
            time_divisor = 1
        self.model.ts = ts / time_divisor

        # self.layers_in_table = self.get_modelpart_graph_layers(
        #     graph_series['items'])

        self.model.insertRows(self.get_modelpart_graph_layers(graph_series["items"]))
        if self.agg_combo_box.currentText() == "m3/s":
            self.plot_widget.setLabel("left", "Flow", "m3/s")
            self.plot_widget.setLabel("bottom", "time", time_units)
        elif self.agg_combo_box.currentText() == "m3 cumulative":
            self.plot_widget.setLabel("left", "Cumulative flow", "m3")
            self.plot_widget.setLabel("bottom", "time", time_units)
        else:
            self.plot_widget.setLabel("left", "-", "-")
            self.plot_widget.setLabel("bottom", "-", "-")

        # set labels for in and out fluxes
        text_upper = pg.TextItem(text="out", anchor=(0, 1), angle=-90)
        text_upper.setPos(0, 0)
        text_lower = pg.TextItem(text="in", anchor=(1, 1), angle=-90)
        text_lower.setPos(0, 0)
        self.plot_widget.addItem(text_upper)
        self.plot_widget.addItem(text_lower)

    def get_wb_result_layers(self):
        lines, points, cells, pumps = self.ts_datasources.rows[0].get_result_layers()
        return lines, points, pumps

    def get_wb_polygon(self):
        lines, points, pumps = self.get_wb_result_layers()
        poly_points = self.polygon_tool.points
        self.wb_polygon = QgsGeometry.fromPolygonXY([poly_points])
        tr = QgsCoordinateTransform(
            self.iface.mapCanvas().mapSettings().destinationCrs(),
            lines.crs(),
            QgsProject.instance(),
        )
        self.wb_polygon.transform(tr)

    def calc_wb_graph(self, model_part, aggregation_type, settings):
        lines, points, pumps = self.get_wb_result_layers()
        self.get_wb_polygon()
        link_ids, pump_ids = self.calc.get_incoming_and_outcoming_link_ids(
            self.wb_polygon, model_part
        )
        node_ids = self.calc.get_nodes(self.wb_polygon, model_part)
        ts, total_time = self.calc.get_aggregated_flows(
            link_ids, pump_ids, node_ids, model_part
        )
        graph_series = self.make_graph_series(
            ts, total_time, model_part, aggregation_type, settings
        )
        self.prepare_and_visualize_selection(
            link_ids, pump_ids, node_ids, lines, pumps, points
        )
        return ts, graph_series

    def calc_wb_barchart(self, bc_model_part):
        bc_link_ids, bc_pump_ids = self.calc.get_incoming_and_outcoming_link_ids(
            self.wb_polygon, bc_model_part
        )
        bc_node_ids = self.calc.get_nodes(self.wb_polygon, bc_model_part)
        bc_ts, bc_total_time = self.calc.get_aggregated_flows(
            bc_link_ids, bc_pump_ids, bc_node_ids, bc_model_part
        )
        return bc_ts, bc_total_time

    def prepare_and_visualize_selection(
        self, link_ids, pump_ids, node_ids, lines, pumps, points, draw_it=False
    ):
        """Prepare dictionaries with geometries categorized by type and
        save it on self.qgs_lines and self.qgs_points.
        """
        req_filter_links = _get_request_filter(link_ids)
        req_filter_pumps = _get_request_filter(pump_ids)
        req_filter_nodes = _get_request_filter(node_ids)

        line_id_to_type = {}
        for _type, id_list in list(link_ids.items()):
            for i in id_list:
                t = _type.rsplit("_out")[0].rsplit("_in")[0]
                if i not in line_id_to_type:
                    # business as usual
                    line_id_to_type[i] = t
                else:
                    # NOTE: awful hack for links that have multiple types
                    val = line_id_to_type[i]
                    if isinstance(val, list):
                        val.append(t)
                    else:
                        line_id_to_type[i] = [val, t]

        node_id_to_type = {}
        for _type, id_list in list(node_ids.items()):
            for i in id_list:
                node_id_to_type[i] = _type

        qgs_lines = {}
        qgs_points = {}
        tr_reverse = QgsCoordinateTransform(
            lines.crs(),
            self.iface.mapCanvas().mapSettings().destinationCrs(),
            QgsProject.instance(),
        )

        # NOTE: getting all features again isn't efficient because they're
        # already calculated in WaterBalanceCalculation, but w/e
        for feat in _get_feature_iterator(lines, req_filter_links):
            geom = feat.geometry()
            geom.transform(tr_reverse)
            _type = line_id_to_type[feat["id"]]

            if isinstance(_type, list):
                # NOTE: this means there are multiple types for one link
                for t in _type:
                    qgs_lines.setdefault(t, []).append(geom.asPolyline())
            else:
                # one type only, business as usual
                qgs_lines.setdefault(_type, []).append(geom.asPolyline())
        for feat in _get_feature_iterator(pumps, req_filter_pumps):
            geom = feat.geometry()
            geom.transform(tr_reverse)
            qgs_lines.setdefault("pumps_hoover", []).append(geom.asPolyline())
        for feat in _get_feature_iterator(points, req_filter_nodes):
            geom = feat.geometry()
            geom.transform(tr_reverse)
            _type = node_id_to_type[feat["id"]]
            qgs_points.setdefault(_type, []).append(geom.asPoint())

        self.qgs_lines = qgs_lines
        self.qgs_points = qgs_points

        # draw the lines/points immediately
        # TODO: probably need to throw this code away since we won't use it
        if draw_it:
            qgs_lines_all = [j for i in list(qgs_lines.values()) for j in i]
            qgs_points_all = [j for i in list(qgs_points.values()) for j in i]

            self.polygon_tool.update_line_point_selection(qgs_lines_all, qgs_points_all)

    def make_graph_series(self, ts, total_time, model_part, aggregation_type, settings):
        settings = copy.deepcopy(settings)

        if model_part == "1d and 2d":
            input_series = dict(
                [
                    (x, y)
                    for (x, y, z, part) in self.INPUT_SERIES
                    if part in ["1d", "2d", "2d_vert", "1d2d"]
                ]
            )
        elif model_part == "2d":
            input_series = dict(
                [
                    (x, y)
                    for (x, y, z, part) in self.INPUT_SERIES
                    if part in ["2d", "2d_vert", "1d2d"]
                ]
            )
        elif model_part == "1d":
            input_series = dict(
                [
                    (x, y)
                    for (x, y, z, part) in self.INPUT_SERIES
                    if part in ["1d", "1d2d"]
                ]
            )

        # set layers to True (layer is tickled in wb_item_table (right box
        # where one can tickle layer(s), but more important: based on this we
        # add layer to to wb_item_table in get_modelpart_graph_layers()
        input_series_copy = copy.deepcopy(input_series)
        for serie_setting in settings.get("items", []):
            serie_setting["layer_in_table"] = False
            for serie in serie_setting["series"]:
                if serie in input_series_copy:
                    # serie will be displayed in wb_item_table
                    serie_setting["layer_in_table"] = True
                    serie_setting["active"] = True
                    break

            serie_setting["method"] = serie_setting["default_method"]
            serie_setting["fill_color"] = [
                int(c) for c in serie_setting["def_fill_color"].split(",")
            ]
            serie_setting["pen_color"] = [
                int(c) for c in serie_setting["def_pen_color"].split(",")
            ]
            serie_setting["ts_series"] = {}
            nrs_input_series = []
            for serie in serie_setting["series"]:
                if serie in input_series:
                    nrs_input_series.append(input_series[serie])
                    del input_series[serie]
                else:
                    # throw good error message
                    logger.warning(
                        "serie config error: %s is an unknown "
                        "serie or is doubled in the config.",
                        serie,
                    )
            if serie_setting["default_method"] == "net":
                sum = total_time[:, nrs_input_series].sum(axis=1)
                serie_setting["ts_series"]["in"] = sum.clip(min=0)
                serie_setting["ts_series"]["out"] = sum.clip(max=0)
            elif serie_setting["default_method"] == "gross":
                sum_pos = np.zeros(shape=(np.size(ts, 0),))
                sum_neg = np.zeros(shape=(np.size(ts, 0),))
                for nr in nrs_input_series:
                    sum_pos += total_time[:, nr].clip(min=0)
                    sum_neg += total_time[:, nr].clip(max=0)
                serie_setting["ts_series"]["in"] = sum_pos
                serie_setting["ts_series"]["out"] = sum_neg
            else:
                # throw config error
                logger.warning(
                    "aggregation %s method unknown.", serie_setting["default_method"]
                )

            if aggregation_type == "m3 cumulative":

                logger.debug("aggregate")
                diff = np.append([0], np.diff(ts))

                serie_setting["ts_series"]["in"] = (
                    serie_setting["ts_series"]["in"] * diff
                )
                serie_setting["ts_series"]["in"] = np.cumsum(
                    serie_setting["ts_series"]["in"], axis=0
                )

                serie_setting["ts_series"]["out"] = (
                    serie_setting["ts_series"]["out"] * diff
                )
                serie_setting["ts_series"]["out"] = np.cumsum(
                    serie_setting["ts_series"]["out"], axis=0
                )

        if model_part == "1d":
            total_time[:, (10, 11)] = total_time[:, (10, 11)] * -1

        settings["items"] = sorted(settings["items"], key=lambda item: item["order"])

        return settings

    def unset_tool(self):
        pass

    def accept(self):
        pass

    def reject(self):
        self.close()

    def closeEvent(self, event):
        self.select_polygon_button.toggled.disconnect(self.toggle_polygon_button)
        self.reset_waterbalans_button.clicked.disconnect(self.reset_waterbalans)
        self.chart_button.clicked.disconnect(self.show_barchart)
        # self.polygon_tool.deactivated.disconnect(self.update_wb)
        self.iface.mapCanvas().unsetMapTool(self.polygon_tool)
        self.polygon_tool.close()

        self.modelpart_combo_box.currentIndexChanged.disconnect(self.update_wb)
        self.sum_type_combo_box.currentIndexChanged.disconnect(self.update_wb)
        self.wb_item_table.hoverEnterRow.disconnect(self.hover_enter_map_visualization)
        self.wb_item_table.hoverExitAllRows.disconnect(
            self.hover_exit_map_visualization
        )
        self.activate_all_button.clicked.disconnect(self.activate_layers)
        self.deactivate_all_button.clicked.disconnect(self.deactivate_layers)

        self.closingWidget.emit()
        event.accept()

    def setup_ui(self, dock_widget):
        """
        initiate main Qt building blocks of interface
        :param dock_widget: QDockWidget instance
        """

        dock_widget.setObjectName("dock_widget")
        dock_widget.setAttribute(Qt.WA_DeleteOnClose)

        self.dock_widget_content = QWidget(self)
        self.dock_widget_content.setObjectName("dockWidgetContent")

        self.main_vlayout = QVBoxLayout(self)
        self.dock_widget_content.setLayout(self.main_vlayout)

        # add button to add objects to graphs
        self.button_bar_hlayout = QHBoxLayout(self)
        self.select_polygon_button = QPushButton(self)
        self.select_polygon_button.setCheckable(True)
        self.select_polygon_button.setObjectName("SelectedSideview")
        self.button_bar_hlayout.addWidget(self.select_polygon_button)
        self.reset_waterbalans_button = QPushButton(self)
        self.reset_waterbalans_button.setObjectName("ResetSideview")
        self.button_bar_hlayout.addWidget(self.reset_waterbalans_button)
        self.chart_button = QPushButton(self)
        self.button_bar_hlayout.addWidget(self.chart_button)

        self.modelpart_combo_box = QComboBox(self)
        self.button_bar_hlayout.addWidget(self.modelpart_combo_box)
        self.sum_type_combo_box = QComboBox(self)
        self.button_bar_hlayout.addWidget(self.sum_type_combo_box)

        self.agg_combo_box = QComboBox(self)
        self.button_bar_hlayout.addWidget(self.agg_combo_box)
        self.ts_units_combo_box = QComboBox(self)
        self.button_bar_hlayout.addWidget(self.ts_units_combo_box)

        # now first add a QSpacerItem so that the QPushButton (added sub-
        # sequently) are aligned on the right-side of the button_bar_hlayout
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_bar_hlayout.addItem(spacer_item)

        self.activate_all_button = QPushButton(self)
        self.button_bar_hlayout.addWidget(
            self.activate_all_button, alignment=Qt.AlignRight
        )

        self.deactivate_all_button = QPushButton(self)
        self.button_bar_hlayout.addWidget(
            self.deactivate_all_button, alignment=Qt.AlignRight
        )

        self.main_vlayout.addLayout(self.button_bar_hlayout)

        # add tabWidget for graphWidgets
        self.contentLayout = QHBoxLayout(self)

        # Graph
        self.plot_widget = WaterBalancePlotWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.plot_widget.sizePolicy().hasHeightForWidth())
        self.plot_widget.setSizePolicy(sizePolicy)
        self.plot_widget.setMinimumSize(QSize(240, 250))

        self.contentLayout.addWidget(self.plot_widget)

        # table
        self.wb_item_table = WaterbalanceItemTable(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.wb_item_table.sizePolicy().hasHeightForWidth()
        )
        self.wb_item_table.setSizePolicy(sizePolicy)
        self.wb_item_table.setMinimumSize(QSize(300, 0))
        self.wb_item_table.resizeColumnsToContents()
        self.contentLayout.addWidget(self.wb_item_table)
        self.main_vlayout.addLayout(self.contentLayout)

        # add dockwidget
        dock_widget.setWidget(self.dock_widget_content)
        self.retranslate_ui(dock_widget)
        QMetaObject.connectSlotsByName(dock_widget)

    def retranslate_ui(self, dock_widget):
        dock_widget.setWindowTitle("3Di water balance")
        self.select_polygon_button.setText("Draw new polygon")
        self.chart_button.setText("Show total balance")
        self.reset_waterbalans_button.setText("Hide on map")
        self.activate_all_button.setText("activate all")
        self.deactivate_all_button.setText("deactivate all")
