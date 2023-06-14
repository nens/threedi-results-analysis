from functools import reduce
from qgis.core import QgsPointXY
from qgis.core import QgsProject
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtGui import QStandardItemModel, QStandardItem
from qgis.PyQt.QtWidgets import QAbstractItemView
from qgis.PyQt.QtWidgets import QDockWidget, QSplitter
from qgis.PyQt.QtWidgets import QHBoxLayout
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtWidgets import QLabel
from qgis.PyQt.QtWidgets import QSizePolicy
from qgis.PyQt.QtWidgets import QSpacerItem
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.PyQt.QtWidgets import QTableView
from qgis.PyQt.QtWidgets import QWidget
from threedi_results_analysis.tool_sideview.route import Route, RouteMapTool
from threedi_results_analysis.tool_sideview.sideview_visualisation import SideViewMapVisualisation
from threedi_results_analysis.tool_sideview.utils import LineType
from threedi_results_analysis.tool_sideview.utils import available_styles
from threedi_results_analysis.utils.user_messages import statusbar_message, messagebar_message, messagebar_pop_message
from threedi_results_analysis.utils.widgets import PenStyleWidget
from threedi_results_analysis.tool_sideview.sideview_graph_generator import SideViewGraphGenerator
from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem, ThreeDiResultItem
from qgis.utils import iface
from bisect import bisect_left
import logging
import numpy as np
import os
import pyqtgraph as pg

logger = logging.getLogger(__name__)

UPPER_LIMIT = 10000
LOWER_LIMIT = -10000


class SideViewPlotWidget(pg.PlotWidget):
    """Side view plot element"""

    profile_route_updated = pyqtSignal()
    profile_hovered = pyqtSignal(float)

    def __init__(
        self,
        parent,
        model,
        sideview_result_model,
    ):
        """

        :param parent: Qt parent widget
        """
        super().__init__(parent)

        self.model = model  # global model from result manager
        self.sideview_result_model = sideview_result_model  # Sideview model containing patterns and selections
        self.sideview_nodes = []
        self.waterlevel_plots = {}  # map from result id to (plot, fill)
        self.current_grid_id = None

        self.showGrid(False, True, 0.5)
        self.setLabel("bottom", "Distance", "m")
        self.setLabel("left", "Height", "m MSL")

        pen = pg.mkPen(color=QColor(190, 190, 190), width=1)
        self.bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(0, 0, 0), width=2, style=Qt.DashLine)
        self.node_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        pen = pg.mkPen(color=QColor(190, 190, 190))
        self.node_indicator_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(190, 190, 190), width=2)
        self.sewer_bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.sewer_upper_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        # Required for top fill of sewers
        self.sewer_top_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.sewer_exchange_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(190, 190, 190), width=2)
        self.channel_bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(150, 75, 0), width=4)
        self.culvert_bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.culvert_upper_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(255, 0, 0), width=1)
        self.weir_bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        pen = pg.mkPen(color=QColor(250, 217, 213), width=1)
        self.weir_middle_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.weir_upper_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.weir_top_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(0, 255, 0), width=1)
        self.orifice_bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        pen = pg.mkPen(color=QColor(208, 240, 192), width=1)
        self.orifice_middle_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.orifice_upper_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.orifice_top_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(200, 200, 200), width=2)
        self.exchange_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        # Required for fill in bottom of graph
        pen = pg.mkPen(color=QColor(190, 190, 190), width=1)
        self.absolute_bottom = pg.PlotDataItem(np.array([(0.0, LOWER_LIMIT), (10000, LOWER_LIMIT)]), pen=pen)
        self.bottom_fill = pg.FillBetweenItem(
            self.bottom_plot, self.absolute_bottom, pg.mkBrush(240, 240, 240)
        )

        # Add some structure specific fills
        self.orifice_opening_fill = pg.FillBetweenItem(
            self.orifice_upper_plot, self.orifice_middle_plot, pg.mkBrush(208, 240, 192)
        )
        self.orifice_full_fill = pg.FillBetweenItem(
            self.orifice_top_plot, self.orifice_bottom_plot, pg.mkBrush(0, 255, 0)
        )

        self.weir_opening_fill = pg.FillBetweenItem(
            self.weir_upper_plot, self.weir_middle_plot, pg.mkBrush(250, 217, 213)
        )
        self.weir_full_fill = pg.FillBetweenItem(
            self.weir_top_plot, self.weir_bottom_plot, pg.mkBrush(255, 0, 0)
        )

        self.sewer_top_fill = pg.FillBetweenItem(
            self.sewer_exchange_plot, self.sewer_top_plot, pg.mkBrush(240, 240, 240)
        )

        self.addItem(self.bottom_fill)
        self.addItem(self.sewer_top_fill)
        self.addItem(self.bottom_plot)
        self.addItem(self.sewer_bottom_plot)
        self.addItem(self.sewer_upper_plot)
        self.addItem(self.sewer_top_plot)
        self.addItem(self.sewer_exchange_plot)
        self.addItem(self.channel_bottom_plot)
        self.addItem(self.culvert_bottom_plot)
        self.addItem(self.culvert_upper_plot)
        self.addItem(self.weir_bottom_plot)
        self.addItem(self.weir_middle_plot)
        self.addItem(self.weir_upper_plot)
        self.addItem(self.weir_top_plot)
        self.addItem(self.orifice_bottom_plot)
        self.addItem(self.orifice_upper_plot)
        self.addItem(self.orifice_middle_plot)
        self.addItem(self.orifice_top_plot)
        self.addItem(self.node_plot)
        self.addItem(self.node_indicator_plot)
        self.addItem(self.orifice_full_fill)
        self.addItem(self.orifice_opening_fill)
        self.addItem(self.weir_full_fill)
        self.addItem(self.weir_opening_fill)
        self.addItem(self.exchange_plot)

        # Set the z-order of the curves (note that fill take minimum of its two defining curve as z-value)
        self.bottom_plot.setZValue(10)
        self.sewer_bottom_plot.setZValue(10)
        self.sewer_upper_plot.setZValue(10)
        self.sewer_top_plot.setZValue(10)
        self.sewer_exchange_plot.setZValue(10)
        self.channel_bottom_plot.setZValue(10)
        self.culvert_bottom_plot.setZValue(10)
        self.culvert_upper_plot.setZValue(10)
        self.weir_bottom_plot.setZValue(10)
        self.weir_middle_plot.setZValue(10)
        self.weir_upper_plot.setZValue(10)
        self.weir_top_plot.setZValue(10)
        self.orifice_bottom_plot.setZValue(10)
        self.orifice_upper_plot.setZValue(10)
        self.orifice_middle_plot.setZValue(10)
        self.orifice_top_plot.setZValue(10)

        self.exchange_plot.setZValue(100)
        self.node_plot.setZValue(60)
        self.node_indicator_plot.setZValue(55)
        self.orifice_full_fill.setZValue(20)
        self.orifice_opening_fill.setZValue(21)
        self.weir_full_fill.setZValue(20)
        self.weir_opening_fill.setZValue(21)
        self.bottom_fill.setZValue(3)
        self.sewer_top_fill.setZValue(3)

        # set listeners to signals
        self.profile_route_updated.connect(self.update_water_level_cache)

        # set code for hovering
        self.vb = self.plotItem.vb
        self.proxy = pg.SignalProxy(
            self.scene().sigMouseMoved, rateLimit=10, slot=self.mouse_hover
        )

        # Hijack the "A" button (it always autoscales to all plots, causing the interesting part to be flattened)
        self.getPlotItem().autoBtn.mode = ""
        self.getPlotItem().autoBtn.clicked.connect(self.auto_scale)

    def auto_scale(self, include_waterlevels: bool = True) -> None:
        range_plots = [self.bottom_plot, self.exchange_plot]
        if include_waterlevels:
            for waterlevel_plot, _ in self.waterlevel_plots.values():
                range_plots.append(waterlevel_plot)

        self.autoRange(items=range_plots)

    def mouse_hover(self, evt):
        mouse_point_x = self.plotItem.vb.mapSceneToView(evt[0]).x()
        self.profile_hovered.emit(mouse_point_x)

    def set_sideprofile(self, route_path, current_grid: ThreeDiGridItem):

        self.sideview_nodes = []  # Required to plot nodes and water level
        bottom_line = []  # Bottom of structures
        upper_line = []  # Top of structures
        middle_line = []  # Typically crest-level
        exchange_line = []  # exchange level
        upper_limit_line = []  # For top fill of weirs and orifices

        self.current_grid_id = current_grid.id if current_grid else None

        generator = SideViewGraphGenerator(current_grid.path) if current_grid else None

        for route_part in route_path:
            first_node = True
            messagebar_message("Sideview", "Profile being generated, this might take a while...", 0, 0)
            QApplication.processEvents()

            for (begin_dist, end_dist, direction, feature) in Route.aggregate_route_parts(route_part):

                begin_dist = float(begin_dist)
                end_dist = float(end_dist)

                begin_node_id = feature["calculation_node_id_start"]
                end_node_id = feature["calculation_node_id_end"]
                if direction != 1:
                    begin_node_id, end_node_id = end_node_id, begin_node_id

                begin_level, end_level, begin_height, end_height, crest_level, ltype = generator.retrieve_profile_info_from_flowline(feature["id"])
                if direction != 1:
                    begin_level, end_level = end_level, begin_level
                    begin_height, end_height = end_height, begin_height

                if (ltype == LineType.PIPE) or (ltype == LineType.CULVERT) or (ltype == LineType.ORIFICE) or (ltype == LineType.WEIR) or (ltype == LineType.CHANNEL):

                    logger.info(f"Adding line {feature['id']}, start_height: {begin_height}, end_height: {end_height}, start_level: {begin_level}, end_level: {end_level}, crest_level {crest_level}")

                    bottom_line.append((begin_dist, begin_level, ltype))
                    bottom_line.append((end_dist, end_level, ltype))

                    if (ltype == LineType.ORIFICE) or (ltype == LineType.WEIR):
                        # Orifices and weirs require different visualisation, and their height is relative to crest level
                        middle_line.append((begin_dist, crest_level, ltype))
                        middle_line.append((end_dist, crest_level, ltype))
                        upper_line.append((begin_dist, crest_level + begin_height, ltype))
                        upper_line.append((end_dist, crest_level + end_height, ltype))

                        if begin_height == 0.0 and end_height == 0.0:  # Open cross section
                            upper_limit_line.append((begin_dist, crest_level, ltype))
                            upper_limit_line.append((end_dist, crest_level, ltype))
                        else:
                            upper_limit_line.append((begin_dist, UPPER_LIMIT, ltype))
                            upper_limit_line.append((end_dist, UPPER_LIMIT, ltype))
                    else:
                        upper_line.append((begin_dist, begin_level + begin_height, ltype))
                        upper_line.append((end_dist, end_level + end_height, ltype))

                else:
                    logger.error(f"Unknown line type: {ltype}")
                    return

                node_level_1, node_height_1 = generator.retrieve_profile_info_from_node(begin_node_id)
                node_level_2, node_height_2 = generator.retrieve_profile_info_from_node(end_node_id)

                # Only draw exchange when nodes have heights
                if (node_height_1 > 0.0 and node_height_2 > 0.0):
                    exchange_line.append((begin_dist, node_level_1 + node_height_1))
                    exchange_line.append((end_dist, node_level_2 + node_height_2))

                # store node information for water level line
                if first_node:
                    self.sideview_nodes.append(
                        {"distance": begin_dist, "id": begin_node_id, "height": node_height_1, "level":  node_level_1}
                    )
                    first_node = False

                self.sideview_nodes.append(
                    {"distance": end_dist, "id": end_node_id, "height": node_height_2, "level":  node_level_2}
                )

        if len(route_path) > 0:
            # Draw data into graph, split lines into seperate parts for the different line types

            tables = {
                LineType.PIPE: [],
                LineType.CHANNEL: [],
                LineType.CULVERT: [],
                LineType.PUMP: [],
                LineType.WEIR: [],
                LineType.ORIFICE: [],
            }

            for point in bottom_line:
                tables[point[2]].append((point[0], point[1]))

            ts_table = np.array([(b[0], b[1]) for b in bottom_line], dtype=float)
            ts_exchange_table = np.array(exchange_line, dtype=float)

            self.exchange_plot.setData(ts_exchange_table, connect="pairs")
            self.bottom_plot.setData(ts_table, connect="pairs")
            self.absolute_bottom.setData(np.array([(b[0], LOWER_LIMIT) for b in bottom_line], dtype=float), connect="pairs")

            self.sewer_bottom_plot.setData(np.array(tables[LineType.PIPE], dtype=float), connect="pairs")
            self.channel_bottom_plot.setData(np.array(tables[LineType.CHANNEL], dtype=float), connect="pairs")
            self.culvert_bottom_plot.setData(np.array(tables[LineType.CULVERT], dtype=float), connect="pairs")
            self.weir_bottom_plot.setData(np.array(tables[LineType.WEIR], dtype=float), connect="pairs")
            self.orifice_bottom_plot.setData(np.array(tables[LineType.ORIFICE], dtype=float), connect="pairs")

            tables = {
                LineType.PIPE: [],
                LineType.CHANNEL: [],
                LineType.CULVERT: [],
                LineType.PUMP: [],
                LineType.WEIR: [],
                LineType.ORIFICE: [],
            }

            for point in upper_line:
                tables[point[2]].append((point[0], point[1]))

            self.sewer_upper_plot.setData(np.array(tables[LineType.PIPE], dtype=float), connect="pairs")
            self.culvert_upper_plot.setData(np.array(tables[LineType.CULVERT], dtype=float), connect="pairs")
            self.weir_upper_plot.setData(np.array(tables[LineType.WEIR], dtype=float), connect="pairs")
            self.orifice_upper_plot.setData(np.array(tables[LineType.ORIFICE], dtype=float), connect="pairs")

            # pyqtgraph has difficulties with filling between lines consisting of different
            # number of segments, therefore we need to draw a dedicated sewer-exchange line
            sewer_top_table = []
            sewer_exchange_table = []
            for point_index in range(0, len(tables[LineType.PIPE]), 2):
                point_1 = tables[LineType.PIPE][point_index]
                point_2 = tables[LineType.PIPE][point_index+1]
                # find the corresponding exchange height at this distance
                exchange_point_found = False
                for exchange_point_index in range(0, len(ts_exchange_table), 2):
                    exchange_point_1 = ts_exchange_table[exchange_point_index]
                    exchange_point_2 = ts_exchange_table[exchange_point_index+1]
                    if exchange_point_1[0] == point_1[0] and exchange_point_2[0] == point_2[0]:
                        sewer_top_table.append((point_1[0], point_1[1]))
                        sewer_top_table.append((point_2[0], point_2[1]))
                        sewer_exchange_table.append((point_1[0], exchange_point_1[1]))
                        sewer_exchange_table.append((point_2[0], exchange_point_2[1]))
                        exchange_point_found = True
                        break

                # In case no exchange level, fill to top
                if not exchange_point_found:
                    sewer_top_table.append((point_1[0], point_1[1]))
                    sewer_top_table.append((point_2[0], point_2[1]))
                    sewer_exchange_table.append((point_1[0], UPPER_LIMIT))
                    sewer_exchange_table.append((point_2[0], UPPER_LIMIT))

            self.sewer_top_plot.setData(np.array(sewer_top_table, dtype=float), connect="pairs")
            self.sewer_exchange_plot.setData(np.array(sewer_exchange_table, dtype=float), connect="pairs")

            tables = {
                LineType.PIPE: [],
                LineType.CHANNEL: [],
                LineType.CULVERT: [],
                LineType.PUMP: [],
                LineType.WEIR: [],
                LineType.ORIFICE: [],
            }

            for point in middle_line:
                tables[point[2]].append((point[0], point[1]))

            self.weir_middle_plot.setData(np.array(tables[LineType.WEIR], dtype=float), connect="pairs")
            self.orifice_middle_plot.setData(np.array(tables[LineType.ORIFICE], dtype=float), connect="pairs")

            tables = {
                LineType.PIPE: [],
                LineType.CHANNEL: [],
                LineType.CULVERT: [],
                LineType.PUMP: [],
                LineType.WEIR: [],
                LineType.ORIFICE: [],
            }

            for point in upper_limit_line:
                tables[point[2]].append((point[0], point[1]))

            self.weir_top_plot.setData(np.array(tables[LineType.WEIR], dtype=float), connect="pairs")
            self.orifice_top_plot.setData(np.array(tables[LineType.ORIFICE], dtype=float), connect="pairs")

            # draw nodes
            node_table = []
            for node in self.sideview_nodes:
                node_table.append((node["distance"], node["level"]))
                node_table.append((node["distance"], node["level"] + node["height"]))
            self.node_plot.setData(np.array(node_table, dtype=float), connect="pairs")

            node_indicator_table = []
            for node in self.sideview_nodes:
                node_indicator_table.append((node["distance"], LOWER_LIMIT))
                node_indicator_table.append((node["distance"], UPPER_LIMIT))
            self.node_indicator_plot.setData(np.array(node_indicator_table, dtype=float), connect="pairs")

            # reset water level lines
            ts_table = np.array(np.array([(0.0, np.nan)]), dtype=float)
            for plot, fill in self.waterlevel_plots.values():
                plot.setData(ts_table)

            self.auto_scale(include_waterlevels=False)

            self.profile_route_updated.emit()
        else:
            # reset sideview
            ts_table = np.array(np.array([(0.0, np.nan)]), dtype=float)
            self.bottom_plot.setData(ts_table)
            self.sewer_top_plot.setData(ts_table)
            self.sewer_exchange_plot.setData(ts_table)
            self.sewer_bottom_plot.setData(ts_table)
            self.sewer_upper_plot.setData(ts_table)
            self.channel_bottom_plot.setData(ts_table)
            self.culvert_bottom_plot.setData(ts_table)
            self.culvert_upper_plot.setData(ts_table)
            self.weir_bottom_plot.setData(ts_table)
            self.weir_upper_plot.setData(ts_table)
            self.weir_middle_plot.setData(ts_table)
            self.orifice_bottom_plot.setData(ts_table)
            self.orifice_upper_plot.setData(ts_table)
            self.orifice_middle_plot.setData(ts_table)
            self.exchange_plot.setData(ts_table)
            self.node_plot.setData(ts_table)
            self.node_indicator_plot.setData(ts_table)

            for plot, fill in self.waterlevel_plots.values():
                self.removeItem(plot)
                self.removeItem(fill)
            self.waterlevel_plots = {}

            # Clear node list used to draw results
            self.sideview_nodes = []
            messagebar_pop_message()

    def update_water_level_cache(self):

        for plot, fill in self.waterlevel_plots.values():
            self.removeItem(plot)
            self.removeItem(fill)
        self.waterlevel_plots = {}

        # Iterate through the selection model
        for row_number in range(self.sideview_result_model.rowCount()):
            # Get checkbox item (this contains result object id)
            check_item = self.sideview_result_model.item(row_number, 0)
            if check_item.checkState() != Qt.Checked:
                continue

            result_id = check_item.data()
            pattern_item = self.sideview_result_model.item(row_number, 1)
            plot_pattern = pattern_item.data()

            logger.error(f"Retrieved result: {result_id} with pattern {plot_pattern} from model")
            # Create the waterlevel plots
            pen = pg.mkPen(color=QColor(153, 214, 255), width=2, style=plot_pattern)
            water_level_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
            water_level_plot.setZValue(100)  # always visible
            water_fill = pg.FillBetweenItem(water_level_plot, self.absolute_bottom, pg.mkBrush(102, 117, 157, 127))
            water_fill.setZValue(0)
            self.addItem(water_level_plot)
            self.addItem(water_fill)
            self.waterlevel_plots[result_id] = (water_level_plot, water_fill)

            result = self.model.get_result(result_id)
            total_data = result.threedi_result.get_timeseries("s1", fill_value=np.NaN)
            for node in self.sideview_nodes:
                if "timeseries" not in node:
                    node["timeseries"] = {}
                node["timeseries"][result.id] = total_data[:, (int(node["id"])+1)]

        tc = iface.mapCanvas().temporalController()
        self.update_waterlevel(True)
        messagebar_pop_message()

    def update_waterlevel(self, update_range=False):

        if not self.waterlevel_plots:
            return

        for row_number in range(self.sideview_result_model.rowCount()):
            # Get checkbox item (this contains result object)
            check_item = self.sideview_result_model.item(row_number, 0)
            if check_item.checkState() != Qt.Checked:
                continue

            result_id = check_item.data()
            result = self.model.get_result(result_id)
            threedi_result = result.threedi_result

            current_delta = result._timedelta
            current_seconds = current_delta.total_seconds()
            parameter_timestamps = threedi_result.get_timestamps("s1")
            timestamp_nr = bisect_left(parameter_timestamps, current_seconds)
            timestamp_nr = min(timestamp_nr, parameter_timestamps.size - 1)

            logger.info(f"Drawing for result {result.id} for nr {timestamp_nr}")

            water_level_line = []
            for node in self.sideview_nodes:
                water_level = node["timeseries"][result.id][timestamp_nr]
                water_level_line.append((node["distance"], water_level))
                # logger.error(f"Node shape {node['timeseries'].shape}, distance {node['distance']} and level {water_level}")

            self.waterlevel_plots[result.id][0].setData(np.array(water_level_line, dtype=float))

        if update_range:
            self.auto_scale(include_waterlevels=True)

    def on_close(self):
        self.profile_route_updated.disconnect(self.update_water_level_cache)

    def closeEvent(self, event):
        self.on_close()
        event.accept()


class SideViewDockWidget(QDockWidget):
    """Main Dock Widget for showing 3Di results in Graphs"""

    # todo:
    # detecteer dichtsbijzijnde punt in plaats van willekeurige binnen gebied
    # let op CRS van vreschillende lagen en CRS changes

    closingWidget = pyqtSignal(int)

    def __init__(
        self, iface, nr, model, parent=None
    ):
        super().__init__(parent)

        self.iface = iface
        self.nr = nr
        self.model = model  # Global Result manager model
        self.sideview_result_model = QStandardItemModel(self)  # Specific sideview model to store loaded results
        self.sideview_result_model.setHorizontalHeaderLabels(["active", "pattern", "result"])
        self.sideview_result_model.itemChanged.connect(self.result_item_toggled)
        # Also used to check whether we have a current grid
        self.current_grid_id = None

        # In case this dock widget becomes (in)visible, we disable the route tool
        self.visibilityChanged.connect(self.unset_route_tool)

        self.setup_ui()

    def update_waterlevel(self):
        self.side_view_plot_widget.update_waterlevel()

    @pyqtSlot(ThreeDiResultItem)
    def result_added(self, item: ThreeDiResultItem):
        if item.parent().id != self.current_grid_id:
            return

        # Update table and redraw sideview
        self._add_result_to_table(item)
        self.side_view_plot_widget.update_water_level_cache()

    @pyqtSlot(ThreeDiResultItem)
    def result_changed(self, item: ThreeDiResultItem):
        if item.parent().id != self.current_grid_id:
            return

        # Update table, no need to redraw anything
        for row_number in range(self.sideview_result_model.rowCount()):
            # Get checkbox item (this contains result object id)
            check_item = self.sideview_result_model.item(row_number, 0)
            result_id = check_item.data()
            if item.id == result_id:
                name_item = self.sideview_result_model.item(row_number, 2)
                name_item.setText(item.text())
                return

        # We should never reach this
        raise Exception("Result should be in sideview model!")

    @pyqtSlot(ThreeDiResultItem)
    def result_removed(self, item: ThreeDiResultItem):
        if item.parent().id != self.current_grid_id:
            return

        # Update table and redraw sideview
        for row_number in range(self.sideview_result_model.rowCount()):
            # Get checkbox item (this contains result object id)
            check_item = self.sideview_result_model.item(row_number, 0)
            result_id = check_item.data()
            if item.id == result_id:
                self.sideview_result_model.removeRow(row_number)
                self.side_view_plot_widget.update_water_level_cache()
                return

        # We should never reach this
        raise Exception("Result should be in sideview model!")

    @pyqtSlot(ThreeDiGridItem)
    def grid_changed(self, item: ThreeDiGridItem):
        idx = self.select_grid_combobox.findData(item.id)
        assert idx != -1
        # Change name in combobox
        self.select_grid_combobox.setItemText(idx, item.text())
        item_id = self.select_grid_combobox.itemData(idx)
        if self.current_grid_id == item_id:
            self.setWindowTitle(f"3Di Sideview Plot {self.nr}: {item.text()}")

    @pyqtSlot(ThreeDiGridItem)
    def grid_added(self, item: ThreeDiGridItem):
        assert item.id != self.current_grid_id
        currentIndex = self.select_grid_combobox.currentIndex()
        self.select_grid_combobox.addItem(item.text(), item.id)
        self.select_grid_combobox.setCurrentIndex(currentIndex)

    @pyqtSlot(ThreeDiGridItem)
    def grid_removed(self, item: ThreeDiGridItem):
        idx = self.select_grid_combobox.findData(item.id)
        assert idx != -1
        item_id = self.select_grid_combobox.itemData(idx)
        if self.current_grid_id == item_id:
            # Also removes all waterlevel plots
            self.deinitialize_route()
            # Removes all plots from table
            self.sideview_result_model.clear()
            self.setWindowTitle(f"3Di Sideview Plot {self.nr}:")

        self.select_grid_combobox.removeItem(idx)

    @pyqtSlot(int)
    def grid_selected(self, grid_index: int):
        # Because we connected the "activated" signal instead of the "currentIndexChanged" signal,
        # programmatically changing the index does not emit a signal
        self.select_grid_combobox.setCurrentIndex(grid_index)

        item_id = self.select_grid_combobox.itemData(grid_index)
        grid = self.model.get_grid(item_id)
        assert grid
        self.initialize_route(grid)
        self.setWindowTitle(f"3Di Sideview Plot {self.nr}: {grid.text()}")

    def result_item_toggled(self, _: QStandardItem):
        # For now, just rebuild and redraw the whole sideview, taking into account new checks
        self.side_view_plot_widget.update_water_level_cache()

    def unset_route_tool(self):
        if self.current_grid_id is None:
            return

        if self.iface.mapCanvas().mapTool() is self.route_tool:
            self.iface.mapCanvas().unsetMapTool(self.route_tool)
            self.select_sideview_button.setChecked(False)

            # Route tool is unset, clean up virtual tree and current route
            self.route.reset()
            self.map_visualisation.reset()
            self.select_sideview_button.setText("Choose sideview trajectory")

    def toggle_route_tool(self):
        if self.current_grid_id is None:
            return

        if self.iface.mapCanvas().mapTool() is self.route_tool:
            self.iface.mapCanvas().unsetMapTool(self.route_tool)
            self.select_sideview_button.setChecked(False)
        else:
            self.iface.mapCanvas().setMapTool(self.route_tool)
            self.select_sideview_button.setChecked(True)

    def initialize_route(self, grid_item: ThreeDiGridItem):
        if self.current_grid_id is not None:
            self.deinitialize_route()

        self.current_grid_id = grid_item.id
        layer_id = grid_item.layer_ids["flowline"]
        # Note that we are NOT owner of this layer (that is results manager)
        self.graph_layer = QgsProject.instance().mapLayer(layer_id)

        # Init route (for shortest path)
        self.route = Route(self.graph_layer)

        # Retrieve relevant results and put in table
        self._populate_result_table(grid_item)

        # Add (internal) graph layer to canvas for testing
        # QgsProject.instance().addMapLayer(self.route.get_graph_layer(), True)

        # Link route map tool (allows node selection)
        self.route_tool = RouteMapTool(
            self.iface.mapCanvas(), self.graph_layer, self.on_route_point_select
        )
        self.route_tool.deactivated.connect(self.unset_route_tool)

        self.map_visualisation = SideViewMapVisualisation(self.iface, self.graph_layer.crs())

        # connect graph hover to point visualisation on map
        self.side_view_plot_widget.profile_hovered.connect(self.map_visualisation.hover_graph)

        # Enable buttons
        self.select_sideview_button.setEnabled(True)
        self.reset_sideview_button.setEnabled(True)

        # Add tree layer to map (service area, for fun and testing purposes)
        self.vl_tree_layer = self.route.get_virtual_tree_layer()
        self.vl_tree_layer.loadNamedStyle(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "layer_styles",
                "tree.qml",
            )
        )
        QgsProject.instance().addMapLayer(self.vl_tree_layer)

    def deinitialize_route(self):
        self.reset_sideview()
        self.unset_route_tool()

        self.current_grid_id = None
        self.select_sideview_button.setEnabled(False)
        self.reset_sideview_button.setEnabled(False)

        self.graph_layer = None  # We are not owner of this layer

        # Note that route.graph_layer is an interal layer used to build the graph,
        # only added to canvas for testing purposes
        # QgsProject.instance().removeMapLayer(self.route.get_graph_layer())

        self.route = None
        self.route_tool = None
        self.map_visualisation = None
        QgsProject.instance().removeMapLayer(self.vl_tree_layer)
        self.vl_tree_layer = None
        self.iface.mapCanvas().refreshAllLayers()

    def _populate_result_table(self, grid_item: ThreeDiGridItem):
        self.sideview_result_model.clear()
        self.sideview_result_model.setHorizontalHeaderLabels(["active", "pattern", "result"])

        results = []
        self.model.get_results_from_item(grid_item, False, results)

        for result in results:
            self._add_result_to_table(result)

    def _add_result_to_table(self, result_item: ThreeDiResultItem):
        checkbox_table_item = QStandardItem("")
        checkbox_table_item.setData(result_item.id)
        checkbox_table_item.setCheckable(True)
        checkbox_table_item.setCheckState(Qt.Checked)
        checkbox_table_item.setEditable(False)

        result_table_item = QStandardItem(result_item.text())
        result_table_item.setEditable(False)

        # pick new pattern
        pattern = available_styles[self.sideview_result_model.rowCount() % 5]
        pattern_table_item = QStandardItem("")
        pattern_table_item.setEditable(False)
        pattern_table_item.setData(pattern)
        self.sideview_result_model.appendRow([checkbox_table_item, pattern_table_item, result_table_item])

        # Add a PenStyle display in the table
        index = self.sideview_result_model.index(self.sideview_result_model.rowCount()-1, 1)
        self.table_view.setIndexWidget(index, PenStyleWidget(pattern, QColor(153, 214, 255), self.table_view))

    def on_route_point_select(self, selected_features, clicked_coordinate):
        """Select and add the closest point from the list of selected features.

        Args:
            selected_features: list of features selected by click
            clicked_coordinate: (transformed) of the click
        """
        assert not self.graph_layer.crs().isGeographic()

        def squared_distance_clicked(coordinate):
            """Calculate the squared distance w.r.t. the clicked location."""
            x1, y1 = clicked_coordinate
            x2, y2 = coordinate.x(), coordinate.y()
            return ((x1-x2)**2 + (y1-y2)**2)

        # Only look at first and last vertex
        selected_coordinates = reduce(
            lambda accum, f: accum
            + [f.geometry().vertexAt(0), f.geometry().vertexAt(len(f.geometry().asPolyline())-1)],
            selected_features,
            [],
        )

        if len(selected_coordinates) == 0:
            return

        closest_point = min(selected_coordinates, key=squared_distance_clicked)
        next_point = QgsPointXY(closest_point)

        success, msg = self.route.add_point(next_point)

        self.select_sideview_button.setText("Continue sideview trajectory")
        if not success:
            statusbar_message(msg)
            return

        self.side_view_plot_widget.set_sideprofile(self.route.path, self.model.get_grid(self.current_grid_id))
        self.map_visualisation.set_sideview_route(self.route)

    def reset_sideview(self):
        self.route.reset()
        self.map_visualisation.reset()
        # Also removes all waterlevel plots
        self.side_view_plot_widget.set_sideprofile([], None)
        self.select_sideview_button.setText("Choose sideview trajectory")

    def on_close(self):
        """
        unloading widget
        """
        if self.current_grid_id is not None:
            self.route_tool.deactivated.disconnect(self.unset_route_tool)
            self.unset_route_tool()
            self.map_visualisation.close()
            self.side_view_plot_widget.profile_hovered.disconnect(self.map_visualisation.hover_graph)
            QgsProject.instance().removeMapLayer(self.vl_tree_layer.id())

        self.select_sideview_button.clicked.disconnect(self.toggle_route_tool)
        self.reset_sideview_button.clicked.disconnect(self.reset_sideview)
        self.side_view_plot_widget.on_close()

    def closeEvent(self, event):
        self.on_close()
        self.closingWidget.emit(self.nr)
        event.accept()

    def setup_ui(self):

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(f"3Di Sideview Plot {self.nr}: ")

        self.dock_widget_content = QWidget(self)

        self.main_vlayout = QVBoxLayout(self)
        self.dock_widget_content.setLayout(self.main_vlayout)

        self.button_bar_hlayout = QHBoxLayout(self)
        self.select_sideview_button = QPushButton("Choose sideview trajectory", self.dock_widget_content)
        self.button_bar_hlayout.addWidget(self.select_sideview_button)
        self.reset_sideview_button = QPushButton("Reset sideview trajectory", self.dock_widget_content)
        self.select_sideview_button.setEnabled(False)
        self.reset_sideview_button.setEnabled(False)
        self.button_bar_hlayout.addWidget(self.reset_sideview_button)
        spacer_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_bar_hlayout.addItem(spacer_item)
        self.button_bar_hlayout.addWidget(QLabel("Grid: ", self.dock_widget_content))
        self.select_grid_combobox = QComboBox(self.dock_widget_content)
        self.button_bar_hlayout.addWidget(self.select_grid_combobox)
        self.main_vlayout.addItem(self.button_bar_hlayout)

        # populate the combobox, but select none
        for grid in self.model.get_grids():
            self.select_grid_combobox.addItem(grid.text(), grid.id)
        self.select_grid_combobox.setCurrentIndex(-1)
        self.select_grid_combobox.activated.connect(self.grid_selected)

        plotContainerWidget = QSplitter(self)
        self.side_view_plot_widget = SideViewPlotWidget(plotContainerWidget, self.model, self.sideview_result_model)
        plotContainerWidget.addWidget(self.side_view_plot_widget)
        self.table_view = QTableView(self)
        self.table_view.setModel(self.sideview_result_model)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.verticalHeader().hide()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.resizeColumnsToContents()
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        plotContainerWidget.addWidget(self.table_view)
        plotContainerWidget.setStretchFactor(0, 8)
        plotContainerWidget.setStretchFactor(1, 1)
        self.main_vlayout.addWidget(plotContainerWidget)

        self.setWidget(self.dock_widget_content)

        self.select_sideview_button.setCheckable(True)
        self.select_sideview_button.clicked.connect(self.toggle_route_tool)
        self.reset_sideview_button.clicked.connect(self.reset_sideview)
