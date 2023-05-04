from functools import reduce
from qgis.core import QgsPointXY
from qgis.core import QgsProject
from qgis.core import QgsDateTimeRange
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtCore import QMetaObject
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QDockWidget, QSplitter
from qgis.PyQt.QtWidgets import QHBoxLayout
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtWidgets import QSizePolicy
from qgis.PyQt.QtWidgets import QSpacerItem
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.PyQt.QtWidgets import QTableView
from qgis.PyQt.QtWidgets import QWidget
from threedi_results_analysis.tool_sideview.route import Route, RouteMapTool
from threedi_results_analysis.tool_sideview.sideview_visualisation import SideViewMapVisualisation
from threedi_results_analysis.tool_sideview.utils import haversine
from threedi_results_analysis.tool_sideview.utils import LineType
from threedi_results_analysis.utils.user_messages import statusbar_message
from threedi_results_analysis.tool_sideview.sideview_graph_generator import SideViewGraphGenerator
from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem
from qgis.utils import iface
from bisect import bisect_left
import logging
import numpy as np
import os
from datetime import datetime as Datetime
import pyqtgraph as pg

logger = logging.getLogger(__name__)


class SideViewPlotWidget(pg.PlotWidget):
    """Side view plot element"""

    profile_route_updated = pyqtSignal()
    profile_hovered = pyqtSignal(float)

    def __init__(
        self,
        parent,
        model,
    ):
        """

        :param parent: Qt parent widget
        """
        super().__init__(parent)

        self.model = model
        self.sideview_nodes = []

        self.showGrid(True, True, 0.5)
        self.setLabel("bottom", "Distance", "m")
        self.setLabel("left", "Height", "mNAP")

        pen = pg.mkPen(color=QColor(200, 200, 200), width=1)
        self.bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(0, 0, 0), width=2, style=Qt.DashLine)
        self.node_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(100, 100, 100), width=2)
        self.sewer_bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.sewer_upper_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.sewer_top_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(50, 50, 50), width=2)
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

        pen = pg.mkPen(color=QColor(0, 200, 0), width=2, style=Qt.DashLine)
        self.exchange_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        # Required for fill in bottom of graph
        pen = pg.mkPen(color=QColor(0, 0, 0), width=1)
        self.absolute_bottom = pg.PlotDataItem(np.array([(0.0, -10000), (10000, -10000)]), pen=pen)
        self.bottom_fill = pg.FillBetweenItem(
            self.bottom_plot, self.absolute_bottom, pg.mkBrush(200, 200, 200)
        )

        pen = pg.mkPen(color=QColor(0, 255, 255), width=2)
        self.water_level_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.water_fill = pg.FillBetweenItem(
            self.water_level_plot, self.absolute_bottom, pg.mkBrush(0, 255, 255)
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
            self.exchange_plot, self.sewer_top_plot, pg.mkBrush(200, 200, 200)
        )

        self.addItem(self.water_fill)
        self.addItem(self.bottom_fill)
        self.addItem(self.sewer_top_fill)
        self.addItem(self.bottom_plot)
        self.addItem(self.sewer_bottom_plot)
        self.addItem(self.sewer_upper_plot)
        self.addItem(self.sewer_top_plot)
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
        self.addItem(self.water_level_plot)
        self.addItem(self.node_plot)

        self.addItem(self.orifice_full_fill)
        self.addItem(self.orifice_opening_fill)
        self.addItem(self.weir_full_fill)
        self.addItem(self.weir_opening_fill)

        self.addItem(self.exchange_plot)

        # Set the z-order of the curves (note that fill take minimum of its two defining curve as z-value)
        self.water_level_plot.setZValue(100)  # always visible
        self.exchange_plot.setZValue(100)
        self.node_plot.setZValue(60)
        self.orifice_full_fill.setZValue(20)
        self.orifice_opening_fill.setZValue(21)
        self.weir_full_fill.setZValue(20)
        self.weir_opening_fill.setZValue(21)
        self.bottom_fill.setZValue(3)
        self.sewer_top_fill.setZValue(3)
        self.water_fill.setZValue(0)

        # set listeners to signals
        self.profile_route_updated.connect(self.update_water_level_cache)

        # set code for hovering
        self.vb = self.plotItem.vb
        self.proxy = pg.SignalProxy(
            self.scene().sigMouseMoved, rateLimit=10, slot=self.mouse_hover
        )

    def mouse_hover(self, evt):
        mouse_point_x = self.plotItem.vb.mapSceneToView(evt[0]).x()
        self.profile_hovered.emit(mouse_point_x)

    def set_sideprofile(self, route_path):

        self.sideview_nodes = []  # Required to plot nodes and water level
        bottom_line = []  # Bottom of structures
        upper_line = []  # Top of structures
        middle_line = []  # Typically crest-level
        exchange_line = []  # exchange level
        upper_limit_line = []  # For top fill of weirs and orifices

        h5_file = self.model.get_results(checked_only=False)[0].parent().path

        for route_part in route_path:
            logger.error("NEW ROUTE PART")
            first_node = True

            for (begin_dist, end_dist, direction, feature) in Route.aggregate_route_parts(route_part):

                begin_dist = float(begin_dist)
                end_dist = float(end_dist)

                begin_node_id = feature["calculation_node_id_start"]
                end_node_id = feature["calculation_node_id_end"]
                if direction != 1:
                    begin_node_id, end_node_id = end_node_id, begin_node_id

                begin_level, end_level, begin_height, end_height, crest_level, ltype = SideViewGraphGenerator.retrieve_profile_info_from_flowline(h5_file, feature["id"])
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
                            upper_limit_line.append((begin_dist, 10000.0, ltype))
                            upper_limit_line.append((end_dist, 10000.0, ltype))
                    else:
                        upper_line.append((begin_dist, begin_level + begin_height, ltype))
                        upper_line.append((end_dist, end_level + end_height, ltype))

                else:
                    logger.error(f"Unknown line type: {ltype}")
                    return

                node_level_1, node_height_1 = SideViewGraphGenerator.retrieve_profile_info_from_node(h5_file, begin_node_id)
                node_level_2, node_height_2 = SideViewGraphGenerator.retrieve_profile_info_from_node(h5_file, end_node_id)

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
            self.absolute_bottom.setData(np.array([(b[0], -10000) for b in bottom_line], dtype=float), connect="pairs")

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
            for point_index in range(0, len(tables[LineType.PIPE]), 2):
                point_1 = tables[LineType.PIPE][point_index]
                point_2 = tables[LineType.PIPE][point_index+1]
                # find the corresponding exchange height at this distance
                for exchange_point_index in range(0, len(ts_exchange_table), 2):
                    exchange_point_1 = ts_exchange_table[exchange_point_index]
                    exchange_point_2 = ts_exchange_table[exchange_point_index+1]
                    if exchange_point_1[0] == point_1[0] and exchange_point_2[0] == point_2[0]:
                        logger.error(f"Appending {(point_1[0], point_1[1])} and {(point_2[0], point_2[1])}to sewer_top_table")
                        sewer_top_table.append((point_1[0], point_1[1]))
                        sewer_top_table.append((point_2[0], point_2[1]))
                        break

            self.sewer_top_plot.setData(np.array(sewer_top_table, dtype=float), connect="pairs")

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

            # reset water level line
            ts_table = np.array(np.array([(0.0, np.nan)]), dtype=float)
            self.water_level_plot.setData(ts_table)

            # Only let specific set of plots determine range
            self.autoRange(items=[self.bottom_plot, self.water_level_plot, self.exchange_plot])

            self.profile_route_updated.emit()
        else:
            # reset sideview
            ts_table = np.array(np.array([(0.0, np.nan)]), dtype=float)
            self.bottom_plot.setData(ts_table)
            self.sewer_top_plot.setData(ts_table)
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
            self.water_level_plot.setData(ts_table)

            # Clear node list used to draw results
            self.sideview_nodes = []

    def update_water_level_cache(self):
        if len(self.model.get_results(False)) == 0:
            return

        ds_item = self.model.get_results(False)[0]  # TODO: PLOT MULTIPLE RESULTS
        if ds_item:
            logger.info("Updating water level cache")
            ds = ds_item.threedi_result
            for node in self.sideview_nodes:
                node["timeseries"] = ds.get_timeseries("s1", node_id=int(node["id"]), fill_value=np.NaN)

            tc = iface.mapCanvas().temporalController()
            self.update_waterlevel(tc.dateTimeRangeForFrameNumber(tc.currentFrameNumber()))
        else:
            # reset water level line
            logger.error("No DS_ITEM!")
            self.water_level_plot.setData(np.array(np.array([(0.0, np.nan)]), dtype=float))

    @pyqtSlot(QgsDateTimeRange)
    def update_waterlevel(self, qgs_dt_range: QgsDateTimeRange):

        result_item = self.model.get_results(False)[0]  # TODO: PLOT MULTIPLE RESULTS?
        if not result_item:
            return

        threedi_result = result_item.threedi_result
        # TODO: refactor the following to an util function and check (first datetime yields idx 1)
        current_datetime = qgs_dt_range.begin().toPyDateTime()
        begin_datetime = Datetime.fromisoformat(threedi_result.dt_timestamps[0])
        end_datetime = Datetime.fromisoformat(threedi_result.dt_timestamps[-1])
        current_datetime = max(begin_datetime, min(current_datetime, end_datetime))
        current_delta = (current_datetime - begin_datetime)
        current_seconds = current_delta.total_seconds()
        parameter_timestamps = threedi_result.get_timestamps("s1")
        timestamp_nr = bisect_left(parameter_timestamps, current_seconds)
        timestamp_nr = min(timestamp_nr, parameter_timestamps.size - 1)

        # timestamp_nr = 1
        logger.info(f"Drawing result for nr {timestamp_nr}")

        water_level_line = []
        for node in self.sideview_nodes:
            water_level = node["timeseries"][timestamp_nr][1]
            water_level_line.append((node["distance"], water_level))
            # logger.error(f"Node shape {node['timeseries'].shape}, distance {node['distance']} and level {water_level}")

        ts_table = np.array(water_level_line, dtype=float)
        self.water_level_plot.setData(ts_table)

        self.autoRange(items=[self.bottom_plot, self.water_level_plot, self.exchange_plot])

    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """
        self.profile_route_updated.disconnect(self.update_water_level_cache)

    def closeEvent(self, event):
        """
        overwrite of QDockWidget class to emit signal
        :param event: QEvent
        """
        self.on_close()
        event.accept()


class SideViewDockWidget(QDockWidget):
    """Main Dock Widget for showing 3Di results in Graphs"""

    # todo:
    # detecteer dichtsbijzijnde punt in plaats van willekeurige binnen gebied
    # let op CRS van vreschillende lagen en CRS changes

    closingWidget = pyqtSignal(int)

    def __init__(
        self, iface, nr, model, datasources, parent=None
    ):
        super().__init__(parent)

        self.iface = iface
        self.nr = nr
        self.model = model

        self.setup_ui()

        return

        # init class attributes
        self.route_tool_active = False

        layer_id = self.model.get_results(checked_only=False)[0].parent().layer_ids["flowline"]
        self.graph_layer = QgsProject.instance().mapLayer(layer_id)

        # Init route (for shortest path)
        self.route = Route(self.graph_layer)

        # Link route map tool (allows node selection)
        self.route_tool = RouteMapTool(
            self.iface.mapCanvas(), self.graph_layer, self.on_route_point_select
        )
        self.route_tool.deactivated.connect(self.unset_route_tool)

        self.map_visualisation = SideViewMapVisualisation(self.iface, self.graph_layer.crs())

        # connect graph hover to point visualisation on map
        self.side_view_plot_widget.profile_hovered.connect(self.map_visualisation.hover_graph)

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

    @pyqtSlot(QgsDateTimeRange)
    def update_waterlevel(self, qgs_dt_range: QgsDateTimeRange):
        self.side_view_plot_widget.update_waterlevel(qgs_dt_range)

    @pyqtSlot(ThreeDiGridItem)
    def grid_changed(self, item: ThreeDiGridItem):
        self.setWindowTitle(f"3Di Sideview Plot: {item.text()}")

    def unset_route_tool(self):
        if self.route_tool_active:
            self.route_tool_active = False
            self.iface.mapCanvas().unsetMapTool(self.route_tool)

    def toggle_route_tool(self):
        if self.route_tool_active:
            self.route_tool_active = False
            self.iface.mapCanvas().unsetMapTool(self.route_tool)
        else:
            self.route_tool_active = True
            self.iface.mapCanvas().setMapTool(self.route_tool)

    def on_route_point_select(self, selected_features, clicked_coordinate):
        """Select and add the closest point from the list of selected features.

        Args:
            selected_features: list of features selected by click
            clicked_coordinate: (lon, lat) (transformed) of the click
        """

        # TODO: is this still required?
        def haversine_clicked(coordinate):
            """Calculate the distance w.r.t. the clicked location."""
            lon1, lat1 = clicked_coordinate
            lon2, lat2 = coordinate.x(), coordinate.y()
            return haversine(lon1, lat1, lon2, lat2)

        # Only look at first and last vertex
        selected_coordinates = reduce(
            lambda accum, f: accum
            + [f.geometry().vertexAt(0), f.geometry().vertexAt(len(f.geometry().asPolyline())-1)],
            selected_features,
            [],
        )

        if len(selected_coordinates) == 0:
            return

        closest_point = min(selected_coordinates, key=haversine_clicked)
        next_point = QgsPointXY(closest_point)

        success, msg = self.route.add_point(next_point)

        if not success:
            statusbar_message(msg)
            return

        self.side_view_plot_widget.set_sideprofile(self.route.path)
        self.map_visualisation.set_sideview_route(self.route)

    def reset_sideview(self):
        self.route.reset()
        self.map_visualisation.reset()

        self.side_view_plot_widget.set_sideprofile([])

    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """
        QgsProject.instance().removeMapLayer(self.vl_tree_layer.id())

        self.select_sideview_button.clicked.disconnect(self.toggle_route_tool)
        self.reset_sideview_button.clicked.disconnect(self.reset_sideview)

        self.route_tool.deactivated.disconnect(self.unset_route_tool)

        self.unset_route_tool()

        self.side_view_plot_widget.profile_hovered.disconnect(
            self.map_visualisation.hover_graph
        )
        self.map_visualisation.close()

        self.side_view_plot_widget.on_close()

    def closeEvent(self, event):
        """
        overwrite of QDockWidget class to emit signal
        :param event: QEvent
        """
        self.on_close()
        self.closingWidget.emit(self.nr)
        event.accept()

    def setup_ui(self):

        self.setObjectName("dock_widget")
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(f"3Di Sideview Plot {self.nr}: ")

        self.dock_widget_content = QWidget(self)

        self.main_vlayout = QVBoxLayout(self)
        self.dock_widget_content.setLayout(self.main_vlayout)

        self.button_bar_hlayout = QHBoxLayout(self)
        self.select_sideview_button = QPushButton("Choose sideview trajectory", self.dock_widget_content)
        self.select_sideview_button.setObjectName("SelectedSideview")
        self.button_bar_hlayout.addWidget(self.select_sideview_button)
        self.reset_sideview_button = QPushButton("Reset sideview trajectory", self.dock_widget_content)
        self.reset_sideview_button.setObjectName("ResetSideview")
        self.button_bar_hlayout.addWidget(self.reset_sideview_button)
        spacer_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_bar_hlayout.addItem(spacer_item)
        self.main_vlayout.addItem(self.button_bar_hlayout)

        plotContainerWidget = QSplitter(self)
        self.side_view_plot_widget = SideViewPlotWidget(plotContainerWidget, self.model)
        plotContainerWidget.addWidget(self.side_view_plot_widget)
        plotContainerWidget.addWidget(QTableView(self))
        plotContainerWidget.setStretchFactor(0, 8)
        plotContainerWidget.setStretchFactor(1, 1)
        self.main_vlayout.addWidget(plotContainerWidget)

        self.setWidget(self.dock_widget_content)
        QMetaObject.connectSlotsByName(self)

        # add listeners
        self.select_sideview_button.clicked.connect(self.toggle_route_tool)
        self.reset_sideview_button.clicked.connect(self.reset_sideview)
