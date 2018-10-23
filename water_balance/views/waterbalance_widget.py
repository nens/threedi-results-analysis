import copy
import functools
import logging
import os

import matplotlib as mpl
mpl.use('Qt4Agg')  # to prevent pyplot from using Tkinter
import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
from PyQt4.QtCore import Qt, QSize, QEvent, QMetaObject
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QTableView, QWidget, QVBoxLayout, QHBoxLayout, \
    QSizePolicy, QPushButton, QSpacerItem, QApplication, QDockWidget,\
    QComboBox, QColor, QMessageBox
from qgis.core import QgsGeometry, QgsCoordinateTransform
from qgis.core import QgsFeatureRequest

from ..config.waterbalance.sum_configs import serie_settings
from ..models.wb_item import WaterbalanceItemModel
from ..utils.maptools.polygon_draw import PolygonDrawTool

log = logging.getLogger('DeltaresTdi.' + __name__)

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

serie_settings = {s['name']: s for s in serie_settings}

INPUT_SERIES = [
    ('2d_in', 0, '2d'),
    ('2d_out', 1, '2d'),
    ('1d_in', 2, '1d'),
    ('1d_out', 3, '1d'),
    ('2d_bound_in', 4, '2d'),
    ('2d_bound_out', 5, '2d'),
    ('1d_bound_in', 6, '1d'),
    ('1d_bound_out', 7, '1d'),
    ('1d__1d_2d_in', 8, '1d'),
    ('1d__1d_2d_out', 9, '1d'),
    ('2d_to_1d_pos', 10, '1d_2d'),
    ('2d_to_1d_neg', 11, '1d_2d'),
    ('pump_in', 12, '1d'),
    ('pump_out', 13, '1d'),
    ('rain', 14, '2d'),
    ('infiltration_rate_simple', 15, '2d'),
    ('lat_2d', 16, '2d'),
    ('lat_1d', 17, '1d'),
    ('d_2d_vol', 18, '2d'),
    ('d_1d_vol', 19, '1d'),
    ('error_2d', 20, 'error_2d'),
    ('error_1d', 21, 'error_1d'),
    ('error_1d_2d', 22, 'error_1d_2d'),
    ('2d_groundwater_in', 23, '2d'),
    ('2d_groundwater_out', 24, '2d'),
    ('d_2d_groundwater_vol', 25, '2d'),
    ('leak', 26, '2d'),
    ('inflow', 27, '1d'),
    ('2d_vertical_infiltration_pos', 28, '2d_vert'),
    ('2d_vertical_infiltration_neg', 29, '2d_vert'),
    ('2d__1d_2d_in', 30, '2d'),
    ('2d__1d_2d_out', 31, '2d'),
]


# some helper functions
#######################

def _get_request_filter(ids):
    ids_flat = list(set([i for j in ids.values() for i in j]))
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
    """Bar for waterbalance barchart with positive and negative components.
    """
    SERIES_NAME_TO_INDEX = {name: idx for (name, idx, _) in INPUT_SERIES}

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

    def set_end_balance_in(self, ts, ts_series, t1=0, t2=None, b_labelname=None):
        idxs = [self.SERIES_NAME_TO_INDEX[name] for name in self.in_series]

        # renier
        print 'set_end_balance_in: ' + b_labelname + ' ' + name

        ts_indices_sliced = self._get_time_indices(ts, t1, t2)
        # NOTE: we're using np.clip to determine in/out for dvol (for flows
        # /discharges this shouldn't matter I THINK)
        ts_deltas = np.concatenate(([0], np.diff(ts)))
        # shape = (N_idxs, len(ts))
        balance_tmp = (ts_deltas * ts_series[:, idxs].T).clip(min=0)
        self._balance_in = balance_tmp[:, ts_indices_sliced].sum()

    @property
    def end_balance_out(self):
        return self._balance_out

    def set_end_balance_out(self, ts, ts_series, t1=0, t2=None, b_labelname=None):
        idxs = [self.SERIES_NAME_TO_INDEX[name] for name in self.out_series]

        # renier
        print 'set_end_balance_out: ' + b_labelname + ' ' + name

        ts_indices_sliced = self._get_time_indices(ts, t1, t2)
        # NOTE: we're using np.clip to determine in/out for dvol (for flows
        # /discharges this shouldn't matter I THINK)
        ts_deltas = np.concatenate(([0], np.diff(ts)))
        balance_tmp = (ts_deltas * ts_series[:, idxs].T).clip(max=0)
        self._balance_out = balance_tmp[:, ts_indices_sliced].sum()

    def calc_balance(self, ts, ts_series, t1=0, t2=None, b_labelname=None):
        """Calculate balance values."""
        self.set_end_balance_in(ts, ts_series, t1, t2, b_labelname)
        self.set_end_balance_out(ts, ts_series, t1, t2, b_labelname)
        if self.is_storage_like:
            self.convert_to_net()

    def convert_to_net(self):
        """Make a bar that contains the net value (positive or negative).
        """
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
        self._balance_in, self._balance_out = \
            -1 * self._balance_out, -1 * self._balance_in

    @property
    def is_storage_like(self):
        return 'storage' in self.label_name

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
        self.bars = sorted([
            Bar(
                label_name=x['label_name'],
                in_series=x['in'],
                out_series=x['out'],
                type=x['type'],
            ) for x in series
        ])

    def calc_balance(
            self, ts, ts_series, t1, t2, net=False, invert=[]):
        for b in self.bars:

            # renier
            # print b.label_name
            if b.label_name == '1D-2D flow' and b.type == '2d':
                pass
            if b.label_name == '1D-2D flow' and b.type == '1d':
                pass
            if b.label_name == '1D boundaries' and b.type == '1d':
                pass
            b_labelname = b.label_name
            b.calc_balance(ts, ts_series, t1=t1, t2=t2, b_labelname=b_labelname)

            # b.calc_balance(ts, ts_series, t1=t1, t2=t2
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
        super(WaterbalanceItemTable, self).__init__(parent)
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
                        log.warning(
                            "Hover row index %s out of range",
                            self._last_hovered_row)
                        # self.hoverExitRow.emit(self._last_hovered_row)
                # self.hoverEnterRow.emit(row)
                if row is not None:
                    try:
                        self.hover_enter(row)
                    except IndexError:
                        log.warning("Hover row index %s out of range", row),
                self._last_hovered_row = row
                pass
        return QTableView.eventFilter(self, widget, event)

    def hover_exit(self, row_nr):
        if row_nr >= 0:
            item = self.model.rows[row_nr]
            name = item.name.value

            if name in [
                'volume change',
                'volume change 2d',
                'volume change 2d groundwater',
                'volume change 1d',
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
                'volume change',
                'volume change 2d',
                'volume change 2d groundwater',
                'volume change 1d',
            ]:
                item.fill_color.value = item.fill_color.value[:3] + [0]
                item.pen_color.value = item.pen_color.value[:3] + [255]
            else:
                item.fill_color.value = item.fill_color.value[:3] + [220]
                item.pen_color.value = item.pen_color.value[:3] + [255]

            item.hover.value = True

    def setModel(self, model):
        super(WaterbalanceItemTable, self).setModel(model)

        self.model = model

        self.resizeColumnsToContents()
        self.model.set_column_sizes_on_view(self)


class WaterBalancePlotWidget(pg.PlotWidget):
    def __init__(self, parent=None, name=""):

        super(WaterBalancePlotWidget, self).__init__(parent)
        self.name = name
        self.showGrid(True, True, 0.5)
        self.setLabel("bottom", "time", "s")
        self.setLabel("left", "flow", "m3/s")
        # Auto SI prefix scaling doesn't work properly with m3, m2 etc.
        self.getAxis("left").enableAutoSIPrefix(False)
        self.series = {}

    def setModel(self, model):
        self.model = model
        self.model.dataChanged.connect(self.data_changed)
        self.model.rowsInserted.connect(self.on_insert)
        self.model.rowsAboutToBeRemoved.connect(
            self.on_remove)

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
            connect='finite',
            pen=pg.mkPen(color=QColor(0, 0, 0, 200), width=1))
        self.addItem(zero_serie, ignoreBounds=True)

        # all item.name.value (e.g. '1d-2d flow', 'pumps', 'rain') have both a
        # 'in' and 'out' flow: so two lines that together form a graph.
        # However the volume change lines in item.name.value ('volume change',
        # 'volume change 2d', 'volume change 2d groundwater', and
        # 'volume change 1d' are summed into 1 line (so no out and in)
        for dir in ['in', 'out']:
            prev_serie = zeros
            prev_pldi = zero_serie
            for item in self.model.rows:
                if item.active.value and item.name.value in [
                    'volume change',
                    'volume change 2d',
                    'volume change 2d groundwater',
                    'volume change 1d',
                ]:
                    pen_color = item.pen_color.value
                    not_cum_serie = item.ts_series.value[
                                        'in'] + item.ts_series.value['out']
                    plot_item = pg.PlotDataItem(
                        x=ts,
                        y=not_cum_serie,
                        connect='finite',
                        pen=pg.mkPen(color=QColor(
                            *pen_color), width=4, style=Qt.DashDotLine))
                    # only get 1 line (the sum of 'in' and 'out')
                    item._plots['sum'] = plot_item

                # if item.active.value and item.name.value == '1d-2d flow':
                #     print 'renier 1d-2d flow'
                #
                # if item.active.value and item.name.value == '1d flow':
                #     print 'renier 1d flow'
                #
                # if item.active.value and item.name.value == '1d boundaries':
                #     print 'renier 1d boundaries'

                if item.active.value and item.name.value not in [
                    'volume change',
                    'volume change 2d',
                    'volume change 2d groundwater',
                    'volume change 1d'
                ]:
                    pen_color = item.pen_color.value
                    fill_color = item.fill_color.value
                    cum_serie = prev_serie + item.ts_series.value[dir]
                    plot_item = pg.PlotDataItem(
                        x=ts,
                        y=cum_serie,
                        connect='finite',
                        pen=pg.mkPen(color=QColor(*pen_color),
                                     width=1))
                    fill = pg.FillBetweenItem(prev_pldi,
                                              plot_item,
                                              pg.mkBrush(*fill_color))
                    # keep reference
                    item._plots[dir] = plot_item
                    item._plots[dir + 'fill'] = fill
                    prev_serie = cum_serie
                    prev_pldi = plot_item

        # add PlotItems to graph
        y_min = 0
        y_max = 0
        x_min = 0
        x_max = 0
        for dir in ['in', 'out']:
            for item in reversed(self.model.rows):
                if item.active.value:
                    if item.name.value in [
                        'volume change',
                        'volume change 2d',
                        'volume change 2d groundwater',
                        'volume change 1d',
                    ]:
                        self.addItem(item._plots['sum'], ignoreBounds=True)

                        # determine PlotItem min and max for display range
                        y_min = min(y_min, min(item._plots['sum'].yData))
                        y_max = max(y_max, max(item._plots['sum'].yData))
                        x_min = min(x_min, min(item._plots['sum'].xData))
                        x_max = max(x_max, max(item._plots['sum'].xData))
                    else:
                        self.addItem(item._plots[dir], ignoreBounds=True)
                        self.addItem(
                            item._plots[dir + 'fill'], ignoreBounds=True)

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
        if self.model.columns[index.column()].name == 'active':
            self.draw_timeseries()

        elif self.model.columns[index.column()].name == 'hover':
            item = self.model.rows[index.row()]

            if item.hover.value:
                if item.active.value:
                    if 'in' in item._plots:
                        item._plots['in'].setPen(color=item.pen_color.value,
                                                 width=1)
                        item._plots['infill'].setBrush(
                            pg.mkBrush(item.fill_color.value))
                    if 'out' in item._plots:
                        item._plots['out'].setPen(color=item.pen_color.value,
                                                  width=1)
                        item._plots['outfill'].setBrush(
                            pg.mkBrush(item.fill_color.value))
                    if 'sum' in item._plots:
                        item._plots['sum'].setPen(color=item.pen_color.value,
                                                  width=4,
                                                  style=Qt.DashDotLine)
            else:
                if item.active.value:
                    if 'in' in item._plots:
                        item._plots['in'].setPen(color=item.pen_color.value,
                                                 width=1)
                        item._plots['infill'].setBrush(
                            pg.mkBrush(item.fill_color.value))
                    if 'out' in item._plots:
                        item._plots['out'].setPen(color=item.pen_color.value,
                                                  width=1)
                        item._plots['outfill'].setBrush(
                            pg.mkBrush(item.fill_color.value))
                    if 'sum' in item._plots:
                        item._plots['sum'].setPen(color=item.pen_color.value,
                                                  width=4,
                                                  style=Qt.DashDotLine)


class WaterBalanceWidget(QDockWidget):
    closingWidget = pyqtSignal()

    INPUT_SERIES = INPUT_SERIES

    IN_OUT_SERIES = [
        {
            'label_name': '1D: 1D-2D flow',
            'in': ['1d__1d_2d_in'],
            'out': ['1d__1d_2d_out'],
            'type': '1d',
        }, {
            'label_name': '2D: 1D-2D flow',
            'in': ['2d__1d_2d_in'],
            'out': ['2d__1d_2d_out'],
            'type': '2d',
        }, {
            'label_name': '1D-2D flow (all domains)',
            # does this make sense?
            'in': ['1d__1d_2d_in', '2d__1d_2d_in'],
            'out': ['1d__1d_2d_out', '2d__1d_2d_out'],
            'type': 'NETVOL',
        }, {
            'label_name': 'net change in storage',
            'in': ['d_2d_vol'],
            'out': ['d_2d_vol'],
            'type': '2d',
        }, {
            'label_name': 'net change in storage',
            'in': ['d_1d_vol'],
            'out': ['d_1d_vol'],
            'type': '1d',
        }, {
            'label_name': 'net change in storage',
            'in': ['d_2d_groundwater_vol'],
            'out': ['d_2d_groundwater_vol'],
            'type': '2d_groundwater',
        }, {
            'label_name': 'leakage',
            'in': ['leak'],
            'out': ['leak'],
            'type': '2d_groundwater',
        }, {
            'label_name': 'simple infiltration',
            'in': ['infiltration_rate_simple'],
            'out': ['infiltration_rate_simple'],
            'type': '2d',
        }, {
            'label_name': '2D flow',
            'in': ['2d_in'],
            'out': ['2d_out'],
            'type': '2d',
        }, {
            'label_name': '1D flow',
            'in': ['1d_in'],
            'out': ['1d_out'],
            'type': '1d',
        }, {
            'label_name': '2D groundwater flow',
            'in': ['2d_groundwater_in'],
            'out': ['2d_groundwater_out'],
            'type': '2d_groundwater',
        }, {
            'label_name': '2D laterals',
            'in': ['lat_2d'],
            'out': ['lat_2d'],
            'type': '2d',
        }, {
            'label_name': '1D laterals',
            'in': ['lat_1d'],
            'out': ['lat_1d'],
            'type': '1d',
        }, {
            'label_name': '2D boundaries',
            'in': ['2d_bound_in'],
            'out': ['2d_bound_out'],
            'type': '2d',
        }, {
            'label_name': '1D boundaries',
            'in': ['1d_bound_in'],
            'out': ['1d_bound_out'],
            'type': '1d',
        }, {
            'label_name': '1D-2D exchange',
            'in': ['2d_to_1d_pos'],
            'out': ['2d_to_1d_neg'],
            'type': '1d_2d',
        }, {
            'label_name': '1D inflow from rain',
            'in': ['inflow'],
            'out': ['inflow'],
            'type': '1d',
        }, {
            'label_name': 'infiltration/exfiltration (domain exchange)',
            # NOTE: for the argument why pos is out and neg is in, see the
            # comment in ``WaterBalanceCalculation.get_aggregated_flows``
            'in': ['2d_vertical_infiltration_neg'],
            'out': ['2d_vertical_infiltration_pos'],
            'type': '2d_vert',
        }, {
            'label_name': 'change in storage',
            'in': ['d_2d_vol', 'd_2d_groundwater_vol', 'd_1d_vol'],
            'out': ['d_2d_vol', 'd_2d_groundwater_vol', 'd_1d_vol'],
            'type': 'NETVOL',
        }, {
            'label_name': 'pump',
            'in': ['pump_in'],
            'out': ['pump_out'],
            'type': '1d',
        }, {
            'label_name': 'rain',
            'in': ['rain'],
            'out': ['rain'],
            'type': '2d',
        }
    ]

    def __init__(
            self, parent=None, iface=None, ts_datasource=None, wb_calc=None):
        """Constructor."""
        super(WaterBalanceWidget, self).__init__(parent)

        self.iface = iface
        self.ts_datasource = ts_datasource
        self.calc = wb_calc

        # setup ui
        self.setup_ui(self)

        self.model = WaterbalanceItemModel()
        self.wb_item_table.setModel(self.model)
        self.plot_widget.setModel(self.model)

        # link tool
        self.polygon_tool = PolygonDrawTool(self.iface.mapCanvas(),
                                            self.select_polygon_button,
                                            self.on_polygon_ready)

        # fill comboboxes with selections
        self.modelpart_combo_box.insertItems(0, ['1d 2d', '1d', '2d'])
        self.sum_type_combo_box.insertItems(0, serie_settings.keys())
        self.agg_combo_box.insertItems(0, ['m3/s', 'm3 cumulative'])

        # add listeners
        self.select_polygon_button.toggled.connect(self.toggle_polygon_button)
        self.reset_waterbalans_button.clicked.connect(self.reset_waterbalans)
        self.chart_button.clicked.connect(self.show_chart)
        # self.polygon_tool.deactivated.connect(self.update_wb)
        self.modelpart_combo_box.currentIndexChanged.connect(self.update_wb)
        self.sum_type_combo_box.currentIndexChanged.connect(self.update_wb)
        self.agg_combo_box.currentIndexChanged.connect(self.update_wb)
        self.wb_item_table.hoverEnterRow.connect(
            self.hover_enter_map_visualization)
        self.wb_item_table.hoverExitAllRows.connect(
            self.hover_exit_map_visualization)

        # TODO: is this a good default?
        # initially turn on tool
        self.select_polygon_button.toggle()
        self.__current_calc = None  # cache the results of calculation

    def show_chart(self):
        if not self._current_calc:
            return
        ts, ts_series = self._current_calc

        #renier
        io_series_net = [
            x for x in self.IN_OUT_SERIES if (
                x['type'] in [
                    '2d', '1d_2d', '2d_vert', '2d_groundwater', '1d'] and
                'storage' not in x['label_name'] and
                'exchange' not in x['label_name'] and
                x['label_name'] != '1D: 1D-2D flow' and
                x['label_name'] != '2D: 1D-2D flow') or
            x['type'] == 'NETVOL'
        ]

        io_series_2d = [
            x for x in self.IN_OUT_SERIES if x['type'] in
            ['2d', '1d_2d', '2d_vert']
        ]

        io_series_2d_groundwater = [
            x for x in self.IN_OUT_SERIES if x['type'] in [
                '2d_groundwater', '2d_vert']
        ]

        io_series_1d = [
            x for x in self.IN_OUT_SERIES if x['type'] in [
                '1d', '1d_2d']
        ]

        # get timeseries x range in plot widget
        viewbox_state = self.plot_widget.getPlotItem().getViewBox().getState()
        view_range = viewbox_state['viewRange']
        t1, t2 = view_range[0]

        # renier
        # print 'break00'

        bm_net = BarManager(io_series_net)
        bm_2d = BarManager(io_series_2d)
        bm_2d_groundwater = BarManager(io_series_2d_groundwater)
        bm_1d = BarManager(io_series_1d)

        bm_net.calc_balance(ts, ts_series, t1, t2, net=True)

        # renier
        # print 'break0'
        
        bm_2d.calc_balance(ts, ts_series, t1, t2)
        bm_2d_groundwater.calc_balance(ts, ts_series, t1, t2, invert=[
            'infiltration/exfiltration (domain exchange)'])
        bm_1d.calc_balance(ts, ts_series, t1, t2, invert=['1D-2D exchange'])

        # renier
        print 'break1'

        # init figure
        plt.close()
        fig = plt.figure(1)
        plt.suptitle("Water balance from t=%.2f to t=%.2f" % (t1, t2))
        # prevent clipping of tick-labels, among others
        plt.subplots_adjust(
            bottom=.3, top=.9, left=.125, right=.9, hspace=1, wspace=.4)

        pattern = '//'

        # #####
        # Net #
        # #####

        plt.subplot(221)
        plt.axhline(color='black', lw=.5)
        bar_in = plt.bar(bm_net.x, bm_net.end_balance_in, label='In')
        bar_out = plt.bar(bm_net.x, bm_net.end_balance_out, label='Out')
        bar_in[-1].set_hatch(pattern)
        bar_out[-1].set_hatch(pattern)
        plt.xticks(bm_net.x, bm_net.xlabels, rotation=45, ha='right')
        plt.title('Net water balance')
        plt.ylabel(r'volume ($m^3$)')
        plt.legend()

        # ######
        # Logo #
        # ######

        current_dir = os.path.dirname(__file__)
        plugin_dir = os.path.join(current_dir, os.pardir, os.pardir)

        # logo 1 (TopSectorWater)
        logo1_path = os.path.join(plugin_dir, 'icons', 'topsector_small.png')
        logo1_img = plt.imread(logo1_path)
        # [left, bottom, width, height] as fractions of figure width and height
        logo1_rect = [0.83, 0.84, 0.04, 0.04]
        logo1_ax = fig.add_axes(logo1_rect, anchor='NE', zorder=-1)
        logo1_ax.imshow(logo1_img, interpolation='none')
        logo1_ax.axis('off')

        # logo 2 (Deltares)
        logo2_path = os.path.join(plugin_dir, 'icons', 'deltares_small.png')
        logo2_img = plt.imread(logo2_path)
        logo2_rect = [0.845, 0.83, 0.06, 0.06]
        logo2_ax = fig.add_axes(logo2_rect, anchor='NE', zorder=-1)
        logo2_ax.imshow(logo2_img, interpolation='none')
        logo2_ax.axis('off')

        # logo text
        text_rect = [0.905, 0.89, 0.1, 0.1]
        text_ax = fig.add_axes(text_rect, anchor='NE', zorder=-1)
        text_ax.text(0.0, 0.0, 'Powered by \n Topsector Water and Deltares',
                     verticalalignment='bottom',
                     horizontalalignment='right',
                     fontsize=9)
        text_ax.axis('off')

        # ####
        # 2D #
        # ####

        # this axes object will be shared by the other subplots to give them
        # the same y alignment
        ax1 = plt.subplot(234)

        plt.axhline(color='black', lw=.5)
        bar_in = plt.bar(bm_2d.x, bm_2d.end_balance_in, label='In')
        bar_out = plt.bar(bm_2d.x, bm_2d.end_balance_out, label='Out')
        bar_in[-1].set_hatch(pattern)
        bar_out[-1].set_hatch(pattern)
        plt.xticks(bm_2d.x, bm_2d.xlabels, rotation=45, ha='right')
        plt.title('2D surface water domain')
        plt.ylabel(r'volume ($m^3$)')
        plt.legend()

        # ################
        # 2D groundwater #
        # ################

        plt.subplot(235, sharey=ax1)
        plt.axhline(color='black', lw=.5)
        bar_in = plt.bar(
            bm_2d_groundwater.x, bm_2d_groundwater.end_balance_in, label='In')
        bar_out = plt.bar(
            bm_2d_groundwater.x, bm_2d_groundwater.end_balance_out,
            label='Out')
        bar_in[-1].set_hatch(pattern)
        bar_out[-1].set_hatch(pattern)
        plt.xticks(
            bm_2d_groundwater.x, bm_2d_groundwater.xlabels, rotation=45,
            ha='right')
        plt.title('2D groundwater domain')
        plt.ylabel(r'volume ($m^3$)')
        plt.legend()

        # ####
        # 1D #
        # ####

        plt.subplot(236, sharey=ax1)
        plt.axhline(color='black', lw=.5)
        bar_in = plt.bar(bm_1d.x, bm_1d.end_balance_in, label='In')
        bar_out = plt.bar(bm_1d.x, bm_1d.end_balance_out, label='Out')
        bar_in[-1].set_hatch(pattern)
        bar_out[-1].set_hatch(pattern)
        plt.xticks(bm_1d.x, bm_1d.xlabels, rotation=45, ha='right')
        plt.title('1D network domain')
        plt.ylabel(r'volume ($m^3$)')
        plt.legend()

        # produce the .png
        plt.show()

    def hover_enter_map_visualization(self, name):
        """On hover rubberband visualisation using the table item name.

        Uses the cached self.qgs_lines/self.qgs_points.
        """
        if self.select_polygon_button.isChecked():
            # highlighting when drawing the polygon doesn't look right.
            # this is the best solution I can think of atm...
            return
        types_2d_line = [
            '2d flow',
        ]
        types_2d_node = [
            'volume change 2d',
        ]
        # TODO 1: generate this dict

        # TODO 2: 1d-2d flow isn't completely correct for 2d
        # and 1d flow because those only only take either 1d_2d_in or
        # 1d_2d_out and we're using the aggregated 1d_2d_intersected

        # TODO 3: using the name as key is INCREDIBLY error prone: one
        # spelling mistake or a change in sum_configs and it doesn't work
        # anymore, and because we also catch the KeyErrors you won't even
        # notice. NEEDS TO BE FIXED

        NAME_TO_LINE_TYPES_EVERYTHING = {
            '2d flow': ['2d'],
            '2d boundaries': ['2d_bound'],
            '1d flow': ['1d'],
            '1d boundaries': ['1d_bound'],
            '1d-2d exchange': ['1d_2d'],
            # TODO: '1d_2d_intersected' and 'pump_or_whatever' are magic
            # strings that we ad-hoc created in the 'prepare_and_visualize_
            # selection' function. A better solution would be nice...
            '1d: 1d-2d flow': ['1d__1d_2d_intersected'],
            '2d: 1d-2d flow': ['2d__1d_2d_intersected'],
            'pumps': ['pump_or_whatever'],
            '2d groundwater flow': ['2d_groundwater'],
        }
        NAME_TO_LINE_TYPES_MAIN_FLOWS = {
            '2d flow': ['2d', '2d_bound', '2d__1d_2d_intersected'],
            '1d flow': [
                '1d', 'pump_or_whatever', '1d_bound', '1d__1d_2d_intersected'],
            '1d-2d exchange': ['1d_2d'],
            '2d groundwater flow': ['2d_groundwater'],
        }
        NAME_TO_NODE_TYPES = {
            'volume change': ['1d', '2d', '2d_groundwater'],
            'volume change 2d': ['2d'],
            'volume change 1d': ['1d'],
            'volume change 2d groundwater': ['2d_groundwater'],
            'rain': ['2d'],
            'inflow 1d from rain': ['1d'],
            'lateral 1d': ['1d'],
            'lateral 2d': ['2d'],
            'leakage': ['2d'],
            'infiltration': ['2d'],
            'ext. forcing (rain and laterals)': ['1d', '2d'],
        }

        # more hackery to fix keys defined in both 'main flows'
        # and 'everything'.
        sum_type = self.sum_type_combo_box.currentText()
        assert sum_type in ['main flows', 'everything']
        if sum_type == 'main flows':
            name_to_line_type = NAME_TO_LINE_TYPES_MAIN_FLOWS
        elif sum_type == 'everything':
            name_to_line_type = NAME_TO_LINE_TYPES_EVERYTHING
        else:
            raise ValueError("Unknown type %s" % sum_type)

        try:
            types_line = name_to_line_type[name]
        except KeyError:
            line_geoms = []
        else:
            line_geoms = []
            for t in types_line:
                try:
                    geoms = self.qgs_lines[t]
                except KeyError:
                    continue
                line_geoms.extend(geoms)
        try:
            types_node = NAME_TO_NODE_TYPES[name]
        except KeyError:
            point_geoms = []
        else:
            point_geoms = []
            for t in types_node:
                try:
                    geoms = self.qgs_points[t]
                except KeyError:
                    continue
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

            self.select_polygon_button.setText(_translate(
                "DockWidget", "Finalize polygon", None))
        else:
            self.iface.mapCanvas().unsetMapTool(self.polygon_tool)
            self.update_wb()
            self.select_polygon_button.setText(_translate(
                "DockWidget", "Draw new polygon", None))

    def redraw_wb(self):
        pass

    def update_wb(self):

        ts, graph_series = self.calc_wb(
            self.modelpart_combo_box.currentText(),
            self.agg_combo_box.currentText(),
            serie_settings[self.sum_type_combo_box.currentText()])

        self.model.removeRows(0, len(self.model.rows))
        self.model.ts = ts
        self.model.insertRows(graph_series['items'])

        if self.agg_combo_box.currentText() == 'm3/s':
            self.plot_widget.setLabel("left", "flow", "m3/s")
        elif self.agg_combo_box.currentText() == 'm3 cumulative':
            self.plot_widget.setLabel("left", "Cumulative flow", "m3")
        else:
            self.plot_widget.setLabel("left", "-", "-")

        # set labels for in and out fluxes
        text_upper = pg.TextItem(text="in", anchor=(0, 1), angle=-90)
        text_upper.setPos(0, 0)
        text_lower = pg.TextItem(text="out", anchor=(1, 1), angle=-90)
        text_lower.setPos(0, 0)
        self.plot_widget.addItem(text_upper)
        self.plot_widget.addItem(text_lower)

    @property
    def _current_calc(self):
        return self.__current_calc

    @_current_calc.setter
    def _current_calc(self, ts_total_time_tuple):
        # NOTE: flips the sign on dvol to make things more intuitive for
        # barcharts
        ts, ts_series = ts_total_time_tuple
        ts_series = ts_series.copy()
        self.__current_calc = (ts, ts_series)

    def calc_wb(self, model_part, aggregation_type, settings):
        poly_points = self.polygon_tool.points
        wb_polygon = QgsGeometry.fromPolygon([poly_points])

        lines, points, pumps = \
            self.ts_datasource.rows[0].get_result_layers()
        tr = QgsCoordinateTransform(
            self.iface.mapCanvas().mapRenderer().destinationCrs(), lines.crs())
        wb_polygon.transform(tr)

        link_ids, pump_ids = self.calc.get_incoming_and_outcoming_link_ids(
            wb_polygon, model_part)
        node_ids = self.calc.get_nodes(wb_polygon, model_part)

        # print 'break666'

        ts, total_time = self.calc.get_aggregated_flows(
            link_ids, pump_ids, node_ids, model_part)

        # cache data for barchart
        self._current_calc = (ts, total_time)

        graph_series = self.make_graph_series(
            ts, total_time, model_part, aggregation_type, settings)

        self.prepare_and_visualize_selection(
            link_ids, pump_ids, node_ids, lines, pumps, points)

        return ts, graph_series

    def prepare_and_visualize_selection(
            self, link_ids, pump_ids, node_ids, lines, pumps, points,
            draw_it=False):
        """Prepare dictionaries with geometries categorized by type and
        save it on self.qgs_lines and self.qgs_points.
        """
        req_filter_links = _get_request_filter(link_ids)
        req_filter_pumps = _get_request_filter(pump_ids)
        req_filter_nodes = _get_request_filter(node_ids)

        line_id_to_type = {}
        for _type, id_list in link_ids.items():
            for i in id_list:
                # we're not interested in in or out types, but for 1d_2d_in
                # and 1d_2d_out we need to employ this hack because these
                # types end in '_in'/'_out'
                if _type == '1d__1d_2d_in' or _type == '1d__1d_2d_out':
                    t = '1d__1d_2d_intersected'
                elif _type == '2d__1d_2d_in' or _type == '2d__1d_2d_in':
                    t = '2d__1d_2d_intersected'
                else:
                    t = _type.rsplit('_out')[0].rsplit('_in')[0]

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

        # pump_id_to_type = {}
        # for _, id_list in pump_ids.items():
        #     for i in id_list:
        #         pump_id_to_type[i] = 'all'
        node_id_to_type = {}
        for _type, id_list in node_ids.items():
            for i in id_list:
                node_id_to_type[i] = _type

        qgs_lines = {}
        qgs_points = {}
        tr_reverse = QgsCoordinateTransform(
            lines.crs(),
            self.iface.mapCanvas().mapRenderer().destinationCrs(),
        )

        # NOTE: getting all features again isn't efficient because they're
        # already calculated in WaterBalanceCalculation, but w/e
        for feat in _get_feature_iterator(lines, req_filter_links):
            geom = feat.geometry()
            geom.transform(tr_reverse)
            _type = line_id_to_type[feat['id']]

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
            qgs_lines.setdefault('pump_or_whatever', []).append(
                geom.asPolyline())
        for feat in _get_feature_iterator(points, req_filter_nodes):
            geom = feat.geometry()
            geom.transform(tr_reverse)
            _type = node_id_to_type[feat['id']]
            qgs_points.setdefault(_type, []).append(geom.asPoint())

        self.qgs_lines = qgs_lines
        self.qgs_points = qgs_points

        # draw the lines/points immediately
        # TODO: probably need to throw this code away since we won't use it
        if draw_it:
            qgs_lines_all = [j for i in qgs_lines.values() for j in i]
            qgs_points_all = [j for i in qgs_points.values() for j in i]

            self.polygon_tool.update_line_point_selection(
                qgs_lines_all, qgs_points_all)

    def make_graph_series(
            self, ts, total_time, model_part, aggregation_type, settings):
        settings = copy.deepcopy(settings)

        if model_part == '1d 2d':
            input_series = dict([
                (x, y) for (x, y, z) in self.INPUT_SERIES
                if z in ['2d', '1d', 'error_1d_2d']])
        elif model_part == '2d':
            input_series = dict([
                (x, y) for (x, y, z) in self.INPUT_SERIES
                if z in ['2d', '1d_2d', 'error_2d']])
        elif model_part == '1d':
            input_series = dict([
                (x, y) for (x, y, z) in self.INPUT_SERIES
                if z in ['1d', '1d_2d', 'error_1d']])
            idx_2d_to_1d_pos = input_series['2d_to_1d_pos']
            idx_2d_to_1d_neg = input_series['2d_to_1d_neg']
            idx_2d_to_1d = (idx_2d_to_1d_pos, idx_2d_to_1d_neg)
            total_time[:, idx_2d_to_1d] = total_time[:, idx_2d_to_1d] * -1

        # TODO: figure out why the hell np.clip is needed.
        for serie_setting in settings.get('items', []):
            serie_setting['active'] = True
            serie_setting['method'] = serie_setting['default_method']
            serie_setting['fill_color'] = [
                int(c) for c in serie_setting['def_fill_color'].split(',')]
            serie_setting['pen_color'] = [
                int(c) for c in serie_setting['def_pen_color'].split(',')]
            serie_setting['ts_series'] = {}
            nrs_input_series = []
            for serie in serie_setting['series']:
                if serie not in input_series:
                    # throw good error message
                    log.warning('serie config error: %s is an unknown '
                                'serie or is doubled in the config.', serie)
                else:
                    nrs_input_series.append(input_series[serie])
                    del input_series[serie]

            if serie_setting['default_method'] == 'net':
                sum = total_time[:, nrs_input_series].sum(axis=1)
                serie_setting['ts_series']['in'] = sum.clip(min=0)
                serie_setting['ts_series']['out'] = sum.clip(max=0)
            elif serie_setting['default_method'] == 'gross':
                sum_pos = np.zeros(shape=(np.size(ts, 0),))
                sum_neg = np.zeros(shape=(np.size(ts, 0),))
                for nr in nrs_input_series:
                    sum_pos += total_time[:, nr].clip(min=0)
                    sum_neg += total_time[:, nr].clip(max=0)
                serie_setting['ts_series']['in'] = sum_pos
                serie_setting['ts_series']['out'] = sum_neg
            else:
                # throw config error
                log.warning('aggregation %s method unknown.',
                            serie_setting['default_method'])

            if aggregation_type == 'm3 cumulative':

                log.debug('aggregate')
                diff = np.append([0], np.diff(ts))

                serie_setting['ts_series']['in'] = serie_setting['ts_series'][
                                                       'in'] * diff
                serie_setting['ts_series']['in'] = np.cumsum(
                    serie_setting['ts_series']['in'], axis=0)

                serie_setting['ts_series']['out'] = serie_setting['ts_series'][
                                                        'out'] * diff
                serie_setting['ts_series']['out'] = np.cumsum(
                    serie_setting['ts_series']['out'], axis=0)

        if model_part == '1d':
            total_time[:, (10, 11)] = total_time[:, (10, 11)] * -1

        settings['items'] = sorted(settings['items'], key=lambda item: item[
            'order'])

        return settings

    def unset_tool(self):
        pass

    def accept(self):
        pass

    def reject(self):
        self.close()

    def closeEvent(self, event):
        self.select_polygon_button.toggled.disconnect(
            self.toggle_polygon_button)
        self.reset_waterbalans_button.clicked.disconnect(
            self.reset_waterbalans)
        self.chart_button.clicked.disconnect(self.show_chart)
        # self.polygon_tool.deactivated.disconnect(self.update_wb)
        self.iface.mapCanvas().unsetMapTool(self.polygon_tool)
        self.polygon_tool.close()

        self.modelpart_combo_box.currentIndexChanged.disconnect(self.update_wb)
        self.sum_type_combo_box.currentIndexChanged.disconnect(self.update_wb)
        self.wb_item_table.hoverEnterRow.disconnect(
            self.hover_enter_map_visualization)
        self.wb_item_table.hoverExitAllRows.disconnect(
            self.hover_exit_map_visualization)

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

        spacer_item = QSpacerItem(40,
                                  20,
                                  QSizePolicy.Expanding,
                                  QSizePolicy.Minimum)
        self.button_bar_hlayout.addItem(spacer_item)
        self.main_vlayout.addLayout(self.button_bar_hlayout)

        # add tabWidget for graphWidgets
        self.contentLayout = QHBoxLayout(self)

        # Graph
        self.plot_widget = WaterBalancePlotWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.plot_widget.sizePolicy().hasHeightForWidth())
        self.plot_widget.setSizePolicy(sizePolicy)
        self.plot_widget.setMinimumSize(QSize(250, 250))

        self.contentLayout.addWidget(self.plot_widget)

        # table
        self.wb_item_table = WaterbalanceItemTable(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.wb_item_table.sizePolicy().hasHeightForWidth())
        self.wb_item_table.setSizePolicy(sizePolicy)
        self.wb_item_table.setMinimumSize(QSize(300, 0))

        self.contentLayout.addWidget(self.wb_item_table)

        self.main_vlayout.addLayout(self.contentLayout)

        # add dockwidget
        dock_widget.setWidget(self.dock_widget_content)
        self.retranslate_ui(dock_widget)
        QMetaObject.connectSlotsByName(dock_widget)

    def retranslate_ui(self, dock_widget):
        pass
        dock_widget.setWindowTitle(_translate(
            "DockWidget", "3Di water balance", None))
        self.select_polygon_button.setText(_translate(
            "DockWidget", "Draw new polygon", None))
        self.chart_button.setText(_translate(
            "DockWidget", "Show total balance", None))
        self.reset_waterbalans_button.setText(_translate(
            "DockWidget", "Hide on map", None))
