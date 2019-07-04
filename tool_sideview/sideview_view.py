from collections import Counter
from functools import reduce
from qgis.analysis import QgsNetworkStrategy
from qgis.analysis import QgsVectorLayerDirector
from qgis.core import QgsCoordinateTransform
from qgis.core import QgsDataSourceUri
from qgis.core import QgsDistanceArea
from qgis.core import QgsFeature
from qgis.core import QgsFeatureRequest
from qgis.core import QgsField
from qgis.core import QgsGeometry
from qgis.core import QgsPointXY
from qgis.core import QgsProject
from qgis.core import QgsRectangle
from qgis.core import QgsUnitTypes
from qgis.core import QgsVectorLayer
from qgis.core import QgsWkbTypes
from qgis.gui import QgsMapTool
from qgis.gui import QgsRubberBand
from qgis.gui import QgsVertexMarker
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import QMetaObject
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtWidgets import QDockWidget
from qgis.PyQt.QtWidgets import QHBoxLayout
from qgis.PyQt.QtWidgets import QLabel
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtWidgets import QSizePolicy
from qgis.PyQt.QtWidgets import QSpacerItem
from qgis.PyQt.QtWidgets import QTabWidget
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.PyQt.QtWidgets import QWidget
from ThreeDiToolbox.tool_sideview.route import Route
from ThreeDiToolbox.tool_sideview.utils import haversine
from ThreeDiToolbox.tool_sideview.utils import split_line_at_points
from ThreeDiToolbox.utils.user_messages import statusbar_message

import logging
import numpy as np
import os
import pyqtgraph as pg


logger = logging.getLogger(__name__)


# GraphDockWidget labels related parameters.
parameter_config = {
    "q": [
        {"name": "Discharge", "unit": "m3/s", "parameters": ["q"]},
        {"name": "Velocity", "unit": "m/s", "parameters": ["u1"]},
    ],
    "h": [
        {"name": "Waterlevel", "unit": "mNAP", "parameters": ["s1"]},
        {"name": "Volume", "unit": "m3", "parameters": ["vol"]},
    ],
}


def python_value(value, default_value=None, func=None):
    """
    help function for translating QVariant Null values into None
    value: QVariant value or python value
    default_value: value in case provided value is None
    func (function): function for transforming value
    :return: python value
    """

    # check on QVariantNull... type
    if hasattr(value, "isNull") and value.isNull():
        return default_value
    else:
        if default_value is not None and value is None:
            return default_value
        else:
            if func is not None:
                return func(value)
            else:
                return value


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)


except AttributeError:

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


INTERPOLATION_PHYSICAL = 0  # interpolation based on all profiles
# interpolation as the 3Di calculation core is
# performing the interpolation. for bottom
# and surface level use profiles close to
# calculation points. For height (profile) first
# get heigth on centerpoints at links
INTERPOLATION_CALCULATION = 1


class SideViewPlotWidget(pg.PlotWidget):
    """Side view plot element"""

    profile_route_updated = pyqtSignal()
    profile_hovered = pyqtSignal(float)

    def __init__(
        self,
        parent=None,
        nr=0,
        line_layer=None,
        point_dict=None,
        channel_profiles=None,
        tdi_root_tool=None,
        name="",
    ):
        """

        :param parent: Qt parent widget
        """
        super().__init__(parent)

        self.name = name
        self.nr = nr
        self.node_dict = point_dict
        self.line_layer = line_layer
        self.channel_profiles = channel_profiles
        self.time_slider = tdi_root_tool.timeslider_widget

        self.profile = []
        self.sideview_nodes = []

        self.showGrid(True, True, 0.5)
        self.setLabel("bottom", "Distance", "m")
        self.setLabel("left", "Height", "mNAP")

        pen = pg.mkPen(color=QColor(200, 200, 200), width=1)
        self.bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.upper_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(100, 100, 100), width=2)
        self.sewer_bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.sewer_upper_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(50, 50, 50), width=2)
        self.channel_bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.channel_upper_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(150, 75, 0), width=4)
        self.culvert_bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.culvert_upper_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(200, 30, 30), width=4)
        self.weir_bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.weir_upper_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(200, 30, 30), width=4, style=Qt.DashLine)
        self.orifice_bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.orifice_upper_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(200, 200, 0), width=4)
        self.pump_bottom_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)
        self.pump_upper_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(0, 255, 0), width=2, style=Qt.DashLine)
        self.drain_level_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(0, 255, 0), width=2)
        self.surface_level_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        self.fill = pg.FillBetweenItem(
            self.bottom_plot, self.upper_plot, pg.mkBrush(200, 200, 200)
        )

        pen = pg.mkPen(color=QColor(0, 255, 255), width=2)
        self.water_level_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        self.addItem(self.drain_level_plot)
        self.addItem(self.surface_level_plot)

        self.addItem(self.fill)

        self.addItem(self.bottom_plot)
        self.addItem(self.upper_plot)
        self.addItem(self.sewer_bottom_plot)
        self.addItem(self.sewer_upper_plot)
        self.addItem(self.channel_bottom_plot)
        self.addItem(self.channel_upper_plot)
        self.addItem(self.culvert_bottom_plot)
        self.addItem(self.culvert_upper_plot)
        self.addItem(self.weir_bottom_plot)
        self.addItem(self.weir_upper_plot)
        self.addItem(self.orifice_bottom_plot)
        self.addItem(self.orifice_upper_plot)
        self.addItem(self.pump_bottom_plot)
        self.addItem(self.pump_upper_plot)

        self.addItem(self.water_level_plot)

        # set listeners to signals
        self.profile_route_updated.connect(self.update_water_level_cache)
        self.time_slider.valueChanged.connect(self.draw_waterlevel_line)
        self.time_slider.datasource_changed.connect(self.update_water_level_cache)

        # set code for hovering
        self.vb = self.plotItem.vb
        self.proxy = pg.SignalProxy(
            self.scene().sigMouseMoved, rateLimit=10, slot=self.mouse_hover
        )
        # self.scene().sigMouseMoved.connect(self.mouse_hover)

    def mouse_hover(self, evt):
        mouse_point = self.plotItem.vb.mapSceneToView(evt[0]).x()
        self.profile_hovered.emit(mouse_point)

    def set_sideprofile(self, profile, route_points):

        self.profile = profile
        self.sideview_nodes = []

        bottom_line = []
        upper_line = []
        drain_level = []
        surface_level = []

        first = True
        last_channel_id = None

        for route_part in profile:
            sub_first = True
            last_channel_id = None
            route_part_total_distance = float(route_part[-1][1])
            for begin_dist, end_dist, distance, direction, feature in route_part:

                begin_dist = float(begin_dist)
                end_dist = float(end_dist)

                if direction == 1:
                    begin_node_id = feature["start_node"]
                    end_node_id = feature["end_node"]
                    begin_node_idx = feature["start_node_idx"]
                    end_node_idx = feature["end_node_idx"]
                else:
                    begin_node_id = feature["end_node"]
                    end_node_id = feature["start_node"]
                    end_node_idx = feature["start_node_idx"]
                    begin_node_idx = feature["end_node_idx"]

                ltype = feature["type"]

                begin_node = self.node_dict[begin_node_id]
                end_node = self.node_dict[end_node_id]

                # 1. add manhole if needed
                if first and begin_node["type"] == SideViewDockWidget.MANHOLE:
                    # add contours of first manhole
                    bottom_line.append(
                        (
                            begin_dist - 0.5 * float(begin_node["length"]),
                            begin_node["surface_level"],
                            SideViewDockWidget.PIPE,
                        )
                    )
                    bottom_line.append(
                        (
                            begin_dist - 0.5 * float(begin_node["length"]),
                            float(begin_node["bottom_level"]),
                            SideViewDockWidget.PIPE,
                        )
                    )
                    bottom_line.append(
                        (
                            begin_dist + 0.5 * float(begin_node["length"]),
                            float(begin_node["bottom_level"]),
                            SideViewDockWidget.PIPE,
                        )
                    )

                    upper_line.append(
                        (
                            begin_dist - 0.5 * float(begin_node["length"]),
                            float(begin_node["surface_level"]),
                            SideViewDockWidget.PIPE,
                        )
                    )
                    upper_line.append(
                        (
                            begin_dist + 0.5 * float(begin_node["length"]),
                            float(begin_node["surface_level"]),
                            SideViewDockWidget.PIPE,
                        )
                    )

                # 2. add contours (bottom, upper, drain and surface lines)
                if (
                    python_value(last_channel_id) is not None
                    and last_channel_id == feature["channel_id"]
                ):
                    # 2a. contours based on cross section lines already added,
                    # skip for this line element based on sideview
                    logger.info("skip channel part")
                    pass
                elif ltype == SideViewDockWidget.CHANNEL:
                    # 2b. add all information of channel based on cross section
                    # do this for the relevant part of the channel at once

                    # get cross section channel information
                    profile_links = self.channel_profiles[feature["channel_id"]]

                    max_length_on_channel = route_part_total_distance - begin_dist

                    # 2b.1 get relevant channel_profiles and sort based on
                    # direction
                    if direction == 1:
                        # get start distance from (selected) calc node layer
                        channel_length = (
                            profile_links[-1]["real_length"]
                            + profile_links[-1]["start_channel_distance"]
                        )

                        dist_from_begin = feature["start_channel_distance"]
                        end_dist_from_begin = min(
                            channel_length, dist_from_begin + max_length_on_channel
                        )
                        length_on_channel = end_dist_from_begin - dist_from_begin

                        profile_links = [
                            link
                            for link in profile_links
                            if link["start_channel_distance"] + link["real_length"]
                            >= dist_from_begin
                            and link["start_channel_distance"] <= end_dist_from_begin
                        ]
                        profile_links = sorted(
                            profile_links, key=lambda x: x["start_channel_distance"]
                        )
                    else:
                        # get start distance from (selected) calc node layer
                        dist_from_begin = (
                            feature["start_channel_distance"] + feature["real_length"]
                        )
                        end_dist_from_begin = max(
                            dist_from_begin - max_length_on_channel, 0.0
                        )
                        length_on_channel = dist_from_begin - end_dist_from_begin

                        profile_links = [
                            link
                            for link in profile_links
                            if link["start_channel_distance"]
                            <= (dist_from_begin + 0.01)
                            and (link["start_channel_distance"] + link["real_length"])
                            >= (end_dist_from_begin - 0.01)
                        ]
                        profile_links = sorted(
                            profile_links,
                            key=lambda x: x["start_channel_distance"],
                            reverse=True,
                        )

                    # 2b.2 get data for contours from relevant profile
                    sub_distance = begin_dist
                    for i, link in enumerate(profile_links):
                        sub_begin_dist = sub_distance
                        # get information of nodes and profiles and links
                        # between profiles
                        if direction == 1:
                            link_left = max(
                                link["start_channel_distance"], dist_from_begin
                            )
                            link_right = min(
                                link["start_channel_distance"] + link["real_length"],
                                end_dist_from_begin,
                            )
                            link_length = link_right - link_left
                            sub_begin_node_id = link["start_node"]
                            sub_end_node_id = link["end_node"]

                        else:
                            link_left = max(
                                link["start_channel_distance"], end_dist_from_begin
                            )
                            link_right = min(
                                link["start_channel_distance"] + link["real_length"],
                                dist_from_begin,
                            )
                            link_length = link_right - link_left
                            sub_begin_node_id = link["end_node"]
                            sub_end_node_id = link["start_node"]

                        length_on_channel -= link_length
                        sub_distance += link_length
                        sub_end_dist = sub_distance

                        sub_begin_node = self.node_dict[sub_begin_node_id]
                        sub_end_node = self.node_dict[sub_end_node_id]

                        if sub_begin_node["type"] != SideViewDockWidget.CROSS_SECTION:
                            # only level is known at cross_section. For other
                            # nodes, the profile is the same as their nearest
                            # cross-section on the link
                            begin_level = sub_end_node["bottom_level"]
                            if sub_end_node["height"] is not None:
                                begin_upper_level = sub_end_node["height"] + begin_level
                            else:
                                begin_upper_level = begin_level
                            begin_surface = sub_end_node["surface_level"]
                            begin_drain = sub_end_node["drain_level"]
                        elif (
                            sub_first
                            and sub_end_node["type"] == SideViewDockWidget.CROSS_SECTION
                        ):
                            # if end en begin are crosssections and the
                            # sideview starts in between cross sections
                            begin_weight = link_length / link["real_length"]
                            end_weight = 1 - begin_weight
                            begin_level = (
                                begin_weight * sub_begin_node["bottom_level"]
                                + end_weight * sub_end_node["bottom_level"]
                            )
                            if (
                                sub_begin_node["height"] is not None
                                and sub_end_node["height"] is not None
                            ):
                                begin_upper_level = (
                                    begin_weight * sub_begin_node["height"]
                                    + end_weight * sub_end_node["height"]
                                    + begin_level
                                )
                            else:
                                begin_upper_level = begin_level
                            if (
                                sub_begin_node["surface_level"] is not None
                                and sub_end_node["surface_level"] is not None
                            ):
                                begin_surface = (
                                    begin_weight * sub_begin_node["surface_level"]
                                    + end_weight * sub_end_node["surface_level"]
                                )
                            if (
                                sub_begin_node["drain_level"] is not None
                                and sub_end_node["drain_level"] is not None
                            ):
                                begin_drain = (
                                    begin_weight * sub_begin_node["drain_level"]
                                    + end_weight * sub_end_node["drain_level"]
                                )
                        else:
                            begin_level = sub_begin_node["bottom_level"]
                            if sub_begin_node["height"] is not None:
                                begin_upper_level = (
                                    sub_begin_node["height"] + begin_level
                                )
                            else:
                                begin_upper_level = begin_level
                            begin_surface = sub_begin_node["surface_level"]
                            begin_drain = sub_begin_node["drain_level"]

                        if sub_end_node["type"] != SideViewDockWidget.CROSS_SECTION:
                            end_level = sub_begin_node["bottom_level"]
                            if sub_begin_node["height"] is not None:
                                end_upper_level = sub_begin_node["height"] + end_level
                            else:
                                end_upper_level = end_level
                            end_surface = sub_begin_node["surface_level"]
                            end_drain = sub_begin_node["drain_level"]
                        elif (
                            i == len(profile_links) - 1
                            and sub_begin_node["type"]
                            == SideViewDockWidget.CROSS_SECTION
                        ):
                            # interpolate based on starting point

                            end_weight = link_length / link["real_length"]
                            begin_weight = 1 - end_weight
                            end_level = (
                                begin_weight * sub_begin_node["bottom_level"]
                                + end_weight * sub_end_node["bottom_level"]
                            )

                            if (
                                sub_begin_node["height"] is not None
                                and sub_end_node["height"] is not None
                            ):
                                end_upper_level = (
                                    begin_weight * sub_begin_node["height"]
                                    + end_weight * sub_end_node["height"]
                                    + end_level
                                )
                            else:
                                end_upper_level = end_level

                            if (
                                sub_begin_node["surface_level"] is not None
                                and sub_end_node["surface_level"] is not None
                            ):
                                end_surface = (
                                    begin_weight * sub_begin_node["surface_level"]
                                    + end_weight * sub_end_node["surface_level"]
                                )
                            else:
                                end_surface = np.nan

                            if (
                                sub_begin_node["drain_level"] is not None
                                and sub_end_node["drain_level"] is not None
                            ):
                                end_drain = (
                                    begin_weight * sub_begin_node["drain_level"]
                                    + end_weight * sub_end_node["drain_level"]
                                )
                            else:
                                end_drain = np.nan

                        else:
                            end_level = sub_end_node["bottom_level"]
                            if sub_end_node["height"] is not None:
                                end_upper_level = sub_end_node["height"] + end_level
                            else:
                                end_upper_level = np.nan
                            end_surface = sub_end_node["surface_level"]
                            end_drain = sub_end_node["drain_level"]

                        bottom_line.append(
                            (
                                sub_begin_dist + 0.5 * float(sub_begin_node["length"]),
                                begin_level,
                                ltype,
                            )
                        )
                        bottom_line.append(
                            (
                                sub_end_dist - 0.5 * float(sub_end_node["length"]),
                                end_level,
                                ltype,
                            )
                        )
                        upper_line.append(
                            (
                                sub_begin_dist + 0.5 * float(sub_begin_node["length"]),
                                begin_upper_level,
                                ltype,
                            )
                        )
                        upper_line.append(
                            (
                                sub_end_dist - 0.5 * float(sub_end_node["length"]),
                                end_upper_level,
                                ltype,
                            )
                        )

                        if (
                            sub_first
                            or sub_begin_node["type"]
                            != SideViewDockWidget.CALCULATION_NODE
                        ):
                            drain_level.append((sub_begin_dist, begin_drain))
                            surface_level.append((sub_begin_dist, begin_surface))

                        drain_level.append((sub_end_dist, end_drain))
                        surface_level.append((sub_end_dist, end_surface))

                        sub_first = False
                else:
                    # 2.c contours based on structure or pipe
                    if direction == 1:
                        begin_level = float(feature["start_level"])
                        end_level = float(feature["end_level"])
                        begin_height = feature["start_height"]
                        end_height = feature["end_height"]
                    else:
                        begin_level = float(feature["end_level"])
                        end_level = float(feature["start_level"])
                        begin_height = feature["end_height"]
                        end_height = feature["start_height"]

                    if python_value(begin_height) is not None:
                        begin_upper_level = begin_level + begin_height
                    else:
                        begin_upper_level = begin_level

                    if python_value(end_height) is not None:
                        end_upper_level = end_level + end_height
                    else:
                        end_upper_level = end_level

                    bottom_line.append(
                        (
                            begin_dist + 0.5 * float(begin_node["length"]),
                            begin_level,
                            ltype,
                        )
                    )
                    bottom_line.append(
                        (end_dist - 0.5 * float(end_node["length"]), end_level, ltype)
                    )

                    # upper line
                    upper_line.append(
                        (
                            begin_dist + 0.5 * float(begin_node["length"]),
                            begin_upper_level,
                            ltype,
                        )
                    )
                    upper_line.append(
                        (
                            end_dist - 0.5 * float(end_node["length"]),
                            end_upper_level,
                            ltype,
                        )
                    )

                    if first:
                        drain_level.append((begin_dist, begin_node["drain_level"]))
                        surface_level.append((begin_dist, begin_node["surface_level"]))

                    drain_level.append((end_dist, end_node["drain_level"]))
                    surface_level.append((end_dist, end_node["surface_level"]))

                last_channel_id = feature["channel_id"]

                if end_node["type"] == SideViewDockWidget.MANHOLE:
                    bottom_line.append(
                        (
                            end_dist - 0.5 * float(end_node["length"]),
                            float(end_node["bottom_level"]),
                            SideViewDockWidget.PIPE,
                        )
                    )
                    bottom_line.append(
                        (
                            end_dist + 0.5 * float(end_node["length"]),
                            float(end_node["bottom_level"]),
                            SideViewDockWidget.PIPE,
                        )
                    )
                    # todo last: bottom_line.append((float(begin_dist)+0,5*
                    # float(end_node['length']), float(
                    # begin_node['surface_level'])))

                if end_node["type"] == SideViewDockWidget.MANHOLE:
                    upper_line.append(
                        (
                            end_dist - 0.5 * float(end_node["length"]),
                            float(end_node["surface_level"]),
                            SideViewDockWidget.PIPE,
                        )
                    )
                    upper_line.append(
                        (
                            end_dist + 0.5 * float(end_node["length"]),
                            float(end_node["surface_level"]),
                            SideViewDockWidget.PIPE,
                        )
                    )

                # store node information for water level line
                if first:
                    self.sideview_nodes.append(
                        {
                            "distance": begin_dist,
                            "id": begin_node_id,
                            "idx": begin_node_idx,
                        }
                    )
                    first = False

                self.sideview_nodes.append(
                    {"distance": end_dist, "id": end_node_id, "idx": end_node_idx}
                )

        if len(profile) > 0:
            # Draw data into graph
            # split lines into seperate parts for the different line types
            # (channel, structure, etc.)

            tables = {
                SideViewDockWidget.PIPE: [],
                SideViewDockWidget.CHANNEL: [],
                SideViewDockWidget.CULVERT: [],
                SideViewDockWidget.PUMP: [],
                SideViewDockWidget.WEIR: [],
                SideViewDockWidget.ORIFICE: [],
            }
            last_type = None
            for point in bottom_line:
                ptype = point[2]

                if ptype != last_type:
                    if last_type is not None:
                        # add nan point to make gap in line
                        tables[ptype].append((point[0], np.nan))
                    last_type = ptype

                tables[ptype].append((point[0], point[1]))

            ts_table = np.array([(b[0], b[1]) for b in bottom_line], dtype=float)
            self.bottom_plot.setData(ts_table, connect="finite")

            ts_table = np.array(tables[SideViewDockWidget.PIPE], dtype=float)
            self.sewer_bottom_plot.setData(ts_table, connect="finite")

            ts_table = np.array(tables[SideViewDockWidget.CHANNEL], dtype=float)
            self.channel_bottom_plot.setData(ts_table, connect="finite")

            ts_table = np.array(tables[SideViewDockWidget.CULVERT], dtype=float)
            self.culvert_bottom_plot.setData(ts_table, connect="finite")

            ts_table = np.array(tables[SideViewDockWidget.WEIR], dtype=float)
            self.weir_bottom_plot.setData(ts_table, connect="finite")

            ts_table = np.array(tables[SideViewDockWidget.ORIFICE], dtype=float)
            self.orifice_bottom_plot.setData(ts_table, connect="finite")

            ts_table = np.array(tables[SideViewDockWidget.PUMP], dtype=float)
            self.pump_bottom_plot.setData(ts_table, connect="finite")

            tables = {
                SideViewDockWidget.PIPE: [],
                SideViewDockWidget.CHANNEL: [],
                SideViewDockWidget.CULVERT: [],
                SideViewDockWidget.PUMP: [],
                SideViewDockWidget.WEIR: [],
                SideViewDockWidget.ORIFICE: [],
            }
            last_type = None
            for point in upper_line:
                ptype = point[2]

                if ptype != last_type:
                    if last_type is not None:
                        tables[ptype].append((point[0], np.nan))
                    last_type = ptype

                tables[ptype].append((point[0], point[1]))

            ts_table = np.array([(b[0], b[1]) for b in upper_line], dtype=float)
            self.upper_plot.setData(ts_table, connect="finite")

            ts_table = np.array(tables[SideViewDockWidget.PIPE], dtype=float)
            self.sewer_upper_plot.setData(ts_table, connect="finite")

            ts_table = np.array(tables[SideViewDockWidget.CHANNEL], dtype=float)
            self.channel_upper_plot.setData(ts_table, connect="finite")

            ts_table = np.array(tables[SideViewDockWidget.CULVERT], dtype=float)
            self.culvert_upper_plot.setData(ts_table, connect="finite")

            ts_table = np.array(tables[SideViewDockWidget.WEIR], dtype=float)
            self.weir_upper_plot.setData(ts_table, connect="finite")

            ts_table = np.array(tables[SideViewDockWidget.ORIFICE], dtype=float)
            self.orifice_upper_plot.setData(ts_table, connect="finite")

            ts_table = np.array(tables[SideViewDockWidget.PUMP], dtype=float)
            self.pump_upper_plot.setData(ts_table, connect="finite")

            ts_table = np.array(drain_level, dtype=float)
            self.drain_level_plot.setData(ts_table, connect="finite")

            ts_table = np.array(surface_level, dtype=float)
            self.surface_level_plot.setData(ts_table, connect="finite")

            # reset water level line
            ts_table = np.array(np.array([(0.0, np.nan)]), dtype=float)
            self.water_level_plot.setData(ts_table)

            self.autoRange()

            self.profile_route_updated.emit()
        else:
            # reset sideview
            ts_table = np.array(np.array([(0.0, np.nan)]), dtype=float)

            self.bottom_plot.setData(ts_table)
            self.upper_plot.setData(ts_table)
            self.sewer_bottom_plot.setData(ts_table)
            self.sewer_upper_plot.setData(ts_table)
            self.channel_bottom_plot.setData(ts_table)
            self.channel_upper_plot.setData(ts_table)
            self.culvert_bottom_plot.setData(ts_table)
            self.culvert_upper_plot.setData(ts_table)
            self.weir_bottom_plot.setData(ts_table)
            self.weir_upper_plot.setData(ts_table)
            self.orifice_bottom_plot.setData(ts_table)
            self.orifice_upper_plot.setData(ts_table)
            self.pump_bottom_plot.setData(ts_table)
            self.pump_upper_plot.setData(ts_table)

            self.drain_level_plot.setData(ts_table)
            self.surface_level_plot.setData(ts_table)
            self.water_level_plot.setData(ts_table)

            self.profile = []
            self.sideview_nodes = []

    def update_water_level_cache(self):
        ds_item = self.time_slider.active_ts_datasource
        if ds_item:
            ds = ds_item.threedi_result()
            for node in self.sideview_nodes:
                try:
                    if python_value(node["idx"]) is not None:
                        ts = ds.get_timeseries(
                            "s1", node_id=int(node["nr"]), fill_value=np.NaN
                        )
                    else:
                        ts = ds.get_timeseries(
                            "s1", content_pk=node["id"], fill_value=np.NaN
                        )
                except KeyError:
                    # This can be "idx", "nr" or "id": are both equally
                    # innocent?  TODO check if an `if "nr" not in node`-like
                    # condition is nicer/friendlier/cleaner.
                    logger.exception(
                        "node has no ids/nr/id key, setting timeries to None"
                    )
                    ts = None
                node["timeseries"] = ts

            self.draw_waterlevel_line()

        else:
            # reset water level line
            ts_table = np.array(np.array([(0.0, np.nan)]), dtype=float)
            self.water_level_plot.setData(ts_table)

    def draw_waterlevel_line(self):

        timestamp_nr = self.time_slider.value()

        water_level_line = []
        for node in self.sideview_nodes:
            if node["timeseries"] is not None:
                water_level = node["timeseries"][timestamp_nr][1]
                water_level_line.append((node["distance"], water_level))
            else:
                # todo: check this is required behavior
                water_level = None

        ts_table = np.array(water_level_line, dtype=float)
        self.water_level_plot.setData(ts_table)

    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """
        logger.info("close sideview graph")
        self.profile_route_updated.disconnect(self.update_water_level_cache)
        self.time_slider.valueChanged.disconnect(self.draw_waterlevel_line)
        self.time_slider.datasource_changed.disconnect(self.update_water_level_cache)

    def closeEvent(self, event):
        """
        overwrite of QDockWidget class to emit signal
        :param event: QEvent
        """
        self.on_close()
        event.accept()


class RouteTool(QgsMapTool):
    def __init__(self, canvas, line_layer, callback_on_select):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.line_layer = line_layer
        self.callback_on_select = callback_on_select

    def canvasPressEvent(self, event):
        pass

    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        # Get the click
        x = event.pos().x()
        y = event.pos().y()

        # use 5 pixels for selecting
        point_ll = self.canvas.getCoordinateTransform().toMapCoordinates(x - 5, y - 5)
        point_ru = self.canvas.getCoordinateTransform().toMapCoordinates(x + 5, y + 5)
        rect = QgsRectangle(
            min(point_ll.x(), point_ru.x()),
            min(point_ll.y(), point_ru.y()),
            max(point_ll.x(), point_ru.x()),
            max(point_ll.y(), point_ru.y()),
        )

        transform = QgsCoordinateTransform(
            self.canvas.mapSettings().destinationCrs(),
            self.line_layer.crs(),
            QgsProject.instance(),
        )

        rect = transform.transform(rect)
        filter = QgsFeatureRequest().setFilterRect(rect)
        selected = self.line_layer.getFeatures(filter)

        clicked_point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        # transform to wgs84 (lon, lat) if not already:
        transformed_point = transform.transform(clicked_point)

        selected_points = [s for s in selected]
        if len(selected_points) > 0:
            self.callback_on_select(selected_points, transformed_point)

    def activate(self):
        self.canvas.setCursor(QCursor(Qt.CrossCursor))

    def deactivate(self):
        self.deactivated.emit()
        self.canvas.setCursor(QCursor(Qt.ArrowCursor))

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return False


class CustomDistancePropeter(QgsNetworkStrategy):
    """custom properter for graph layer"""

    def __init__(self):
        QgsNetworkStrategy.__init__(self)

    def cost(self, distance, feature):
        value = feature["real_length"]
        if python_value(value) is None:
            # provided distance is not correct, so do a correct calculation
            value = distance
        return value

    def requiredAttributes(self):
        # Must be a list of the attribute indexes (int), not strings:
        attributes = []
        return attributes


class SideViewMapVisualisation(object):
    # self.line_layer.crs()
    def __init__(self, iface, source_crs):
        self.iface = iface

        self.source_crs = source_crs

        # temp layer for side profile trac
        self.rb = QgsRubberBand(self.iface.mapCanvas(), QgsWkbTypes.LineGeometry)
        self.rb.setColor(Qt.red)
        self.rb.setWidth(2)

        # temp layer for last selected point
        self.point_markers = []
        self.active_route = None

        self.hover_marker = QgsVertexMarker(self.iface.mapCanvas())
        self.hover_marker.setIconType(QgsVertexMarker.ICON_X)
        self.hover_marker.setColor(Qt.red)
        self.hover_marker.setPenWidth(6)

        self.dist_calc = QgsDistanceArea()

    def close(self):
        self.reset()
        self.iface.mapCanvas().scene().removeItem(self.hover_marker)

    def set_sideview_route(self, route):

        self.reset()

        self.active_route = route
        transform = QgsCoordinateTransform(
            self.source_crs, QgsProject.instance().crs(), QgsProject.instance()
        )

        for pnt in route.path_vertexes:
            t_pnt = transform.transform(pnt)
            self.rb.addPoint(t_pnt)

        for point, point_id, dist in route.path_points:

            marker = QgsVertexMarker(self.iface.mapCanvas())
            marker.setIconType(QgsVertexMarker.ICON_CIRCLE)
            marker.setColor(Qt.red)
            marker.setPenWidth(4)
            marker.setCenter(transform.transform(point))
            self.point_markers.append(marker)

    def reset(self):
        self.rb.reset()
        self.active_route = None

        for marker in self.point_markers:
            self.iface.mapCanvas().scene().removeItem(marker)

        self.point_markers = []

        self.hover_marker.setCenter(QgsPointXY(0.0, 0.0))

    def hover_graph(self, meters_from_start):

        transform = QgsCoordinateTransform(
            self.source_crs, QgsProject.instance().crs(), QgsProject.instance()
        )

        if self.active_route is None:
            return

        if meters_from_start < 0.0:
            meters_from_start = 0.0
        elif (
            len(self.active_route.path) > 0
            and meters_from_start > self.active_route.path[-1][-1][1]
        ):
            meters_from_start = self.active_route.path[-1][-1][1]

        for route_part in self.active_route.path:
            if meters_from_start <= route_part[-1][1]:
                for part in route_part:
                    if meters_from_start <= part[1]:
                        if part[3] == 1:
                            distance_on_line = meters_from_start - part[0]
                        else:
                            distance_on_line = part[1] - meters_from_start

                        conversion_factor = QgsUnitTypes.fromUnitToUnitFactor(
                            QgsUnitTypes.DistanceMeters, QgsUnitTypes.DistanceDegrees
                        )
                        length = distance_on_line * conversion_factor
                        point = part[4].geometry().interpolate(length)
                        if point.isEmpty():
                            return
                        self.hover_marker.setCenter(
                            transform.transform(point.asPoint())
                        )
                        return

    def hover_map(self, point_geometry):
        pass

    def show_selectable_points(self, graph_tree):
        pass

    def hide_selectable_points(self):
        pass


class SideViewDockWidget(QDockWidget):
    """Main Dock Widget for showing 3Di results in Graphs"""

    # todo:
    # punten verplaatsen
    # als op lijn wordt gedrukt en vastgehouden
    # detecteer dichtsbijzijnde punt in plaats van willekeurige binnen gebied
    # let op CRS van vreschillende lagen en CRS changes

    closingWidget = pyqtSignal(int)

    CONNECTION_NODE = 1
    MANHOLE = 2
    BOUNDARY = 3
    CROSS_SECTION = 4
    CALCULATION_NODE = 5
    PIPE = 11
    WEIR = 12
    CULVERT = 13
    ORIFICE = 14
    PUMP = 15
    CHANNEL = 16

    def __init__(
        self, iface, parent_widget=None, parent_class=None, nr=0, tdi_root_tool=None
    ):
        """Constructor"""
        super().__init__(parent_widget)

        self.iface = iface
        self.parent_class = parent_class
        self.nr = nr
        self.tdi_root_tool = tdi_root_tool

        # setup ui
        self.setup_ui(self)

        # add listeners
        self.select_sideview_button.clicked.connect(self.toggle_route_tool)
        self.reset_sideview_button.clicked.connect(self.reset_sideview)

        # init class attributes
        self.route_tool_active = False

        # create point and line layer out of spatialite layers
        if self.tdi_root_tool.timeslider_widget.active_ts_datasource is not None:
            line, node, pump = (
                self.tdi_root_tool.timeslider_widget.active_ts_datasource.get_result_layers()
            )
        else:
            line = None

        self.line_layer, self.point_dict, self.channel_profiles = self.create_combined_layers(
            self.tdi_root_tool.ts_datasources.model_spatialite_filepath, line
        )

        self.sideviews = []
        widget = SideViewPlotWidget(
            self,
            0,
            self.line_layer,
            self.point_dict,
            self.channel_profiles,
            self.tdi_root_tool,
            "name",
        )
        self.active_sideview = widget
        self.sideviews.append((0, widget))
        self.side_view_tab_widget.addTab(widget, widget.name)

        # init route graph
        # QgsLineVectorLayerDirector
        director = QgsVectorLayerDirector(
            self.line_layer, -1, "", "", "", QgsVectorLayerDirector.DirectionBoth
        )

        self.route = Route(
            self.line_layer,
            director,
            id_field="nr",
            weight_properter=CustomDistancePropeter(),
            distance_properter=CustomDistancePropeter(),
        )

        # link route map tool
        self.route_tool = RouteTool(
            self.iface.mapCanvas(), self.line_layer, self.on_route_point_select
        )

        self.route_tool.deactivated.connect(self.unset_route_tool)

        self.map_visualisation = SideViewMapVisualisation(
            self.iface, self.line_layer.crs()
        )

        # connect graph hover to point visualisation on map
        self.active_sideview.profile_hovered.connect(self.map_visualisation.hover_graph)

        # add tree layer to map (for fun and testing purposes)
        self.vl_tree_layer = self.route.get_virtual_tree_layer()

        self.vl_tree_layer.loadNamedStyle(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                os.pardir,
                "layer_styles",
                "tools",
                "tree.qml",
            )
        )

        QgsProject.instance().addMapLayer(self.vl_tree_layer)

    def create_combined_layers(self, spatialite_path, model_line_layer):

        # if model_line_layer is None:
        #     canvas = self.tdi_root_tool.iface.mapCanvas()
        #     model_line_layer = canvas.currentLayer()

        def get_layer(spatialite_path, table_name, geom_column=""):
            uri2 = QgsDataSourceUri()
            uri2.setDatabase(spatialite_path)
            uri2.setDataSource("", table_name, geom_column)

            return QgsVectorLayer(uri2.uri(), table_name, "spatialite")

        # connection node layer
        profile_layer = get_layer(spatialite_path, "v2_cross_section_definition")

        cross_section_location_layer = get_layer(
            spatialite_path, "v2_cross_section_location", "the_geom"
        )

        connection_node_layer = get_layer(
            spatialite_path, "v2_connection_nodes", "the_geom"
        )
        manhole_layer = get_layer(spatialite_path, "v2_manhole")
        boundary_layer = get_layer(spatialite_path, "v2_1d_boundary_conditions")
        pipe_layer = get_layer(spatialite_path, "v2_pipe")
        channel_layer = get_layer(spatialite_path, "v2_channel", "the_geom")
        weir_layer = get_layer(spatialite_path, "v2_weir")
        orifice_layer = get_layer(spatialite_path, "v2_orifice")
        pump_layer = get_layer(spatialite_path, "v2_pumpstation")
        culvert_layer = get_layer(spatialite_path, "v2_culvert")

        lines = []
        points = {}
        profiles = {}
        for profile in profile_layer.getFeatures():
            # todo: add support for other definitions
            rel_bottom_level = 0.0
            open = False
            height_was_none = False

            if profile["shape"] in (1, 2, 3):
                height = python_value(profile["height"], func=float)
                width = python_value(profile["width"], func=float)
                if profile["shape"] == 1:
                    # rectangle
                    if height is None:
                        # square
                        height_was_none = True
                        if width is not None:
                            height = width
                elif profile["shape"] == 2:
                    # round
                    height = width
            elif profile["shape"] in (5, 6):
                # tabulated and tabulated interpolated
                height_list = profile["height"].split(" ")
                # The calculation core automagically move the lowest point of
                # a profile to 0, so this is not correct:
                # rel_bottom_level = float(height_list[0])
                # height = float(height_list[-1]) - rel_bottom_level
                # but this:
                rel_bottom_level = 0.0
                # todo: catch and warn of values are incorrect
                height = float(height_list[-1]) - float(height_list[0])

                if float(profile["width"].split(" ")[-1]) > 0.01:
                    open = True

            profiles[profile["id"]] = {
                "height": height,
                "rel_bottom_level": rel_bottom_level,
                "open": open,
                "height_was_none": height_was_none,
            }

        for cn in connection_node_layer.getFeatures():
            points[cn["id"]] = {
                "point": cn.geometry().asPoint(),
                "type": self.CONNECTION_NODE,
                "surface_level": None,
                "drain_level": None,
                "bottom_level": None,
                "length": 0.0,
            }
        for manhole in manhole_layer.getFeatures():
            p = points[manhole["connection_node_id"]]
            p["type"] = self.MANHOLE
            p["surface_level"] = python_value(manhole["surface_level"])
            p["drain_level"] = python_value(manhole["drain_level"], p["surface_level"])
            p["bottom_level"] = python_value(manhole["bottom_level"])
            p["length"] = python_value(manhole["width"], 0.0)

        for bound in boundary_layer.getFeatures():
            p = points[bound["connection_node_id"]]
            p["type"] = self.BOUNDARY
            p["surface_level"] = None
            p["drain_level"] = None
            p["bottom_level"] = None
            p["length"] = 0.0

        for pipe in pipe_layer.getFeatures():
            # note: no support of calculation nodes on pipes
            profile = profiles[pipe["cross_section_definition_id"]]
            pipe_def = {
                "id": "pipe_" + str(pipe["id"]),
                "type": self.PIPE,
                "start_node": pipe["connection_node_start_id"],
                "end_node": pipe["connection_node_end_id"],
                "start_level": pipe["invert_level_start_point"]
                + profile["rel_bottom_level"],
                "end_level": pipe["invert_level_end_point"]
                + profile["rel_bottom_level"],
                "start_height": profile["height"],
                "end_height": profile["height"],
            }

            lines.append(pipe_def)

        for orifice in orifice_layer.getFeatures():
            profile = profiles[orifice["cross_section_definition_id"]]
            orifice_def = {
                "id": "orifice_" + str(orifice["id"]),
                "type": self.ORIFICE,
                "start_node": orifice["connection_node_start_id"],
                "end_node": orifice["connection_node_end_id"],
                "start_level": orifice["crest_level"],
                "end_level": orifice["crest_level"],
                "start_height": profile["height"],
                "end_height": profile["height"],
            }
            lines.append(orifice_def)

        for weir in weir_layer.getFeatures():
            profile = profiles[weir["cross_section_definition_id"]]

            # weirs without height are not square, but open
            if profile["height_was_none"]:
                height = None
            else:
                height = profile["height"]

            weir_def = {
                "id": "weir_" + str(weir["id"]),
                "type": self.WEIR,
                "start_node": weir["connection_node_start_id"],
                "end_node": weir["connection_node_end_id"],
                "start_level": weir["crest_level"],
                "end_level": weir["crest_level"],
                "start_height": height,
                "end_height": height,
            }
            lines.append(weir_def)

        for culvert in culvert_layer.getFeatures():
            profile = profiles[culvert["cross_section_definition_id"]]

            culvert_def = {
                "id": "culvert_" + str(culvert["id"]),
                "type": self.CULVERT,
                "start_node": culvert["connection_node_start_id"],
                "end_node": culvert["connection_node_end_id"],
                "start_level": culvert["invert_level_start_point"]
                + profile["rel_bottom_level"],
                "end_level": culvert["invert_level_end_point"]
                + profile["rel_bottom_level"],
                "start_height": profile["height"],
                "end_height": profile["height"],
            }
            lines.append(culvert_def)

        for pump in pump_layer.getFeatures():

            try:
                start_upper_level = pump["start_level_suction_side"]
                end_upper_level = pump["start_level_delivery_side"]
                start_lower_level = pump["stop_level_suction_side"]
                end_lower_level = pump["stop_level_delivery_side"]
            except KeyError:
                logger.exception(
                    "Pump is missing one of the suction/delivery side levels: "
                    "using start_level and lower_stop_level instead"
                )
                start_upper_level = pump["start_level"]
                end_upper_level = start_upper_level
                start_lower_level = pump["lower_stop_level"]
                end_lower_level = start_lower_level

            start_height = None
            end_height = None

            # default values from each other
            # QpyNullVariant is behaving strange,
            if hasattr(start_lower_level, "isNull") and start_lower_level.isNull():
                if not hasattr(end_lower_level, "isNull"):
                    start_lower_level = end_lower_level
            else:
                if hasattr(end_lower_level, "isNull") and end_lower_level.isNull():
                    end_lower_level = start_lower_level

            if hasattr(start_upper_level, "isNull") and start_upper_level.isNull():
                if not hasattr(end_upper_level, "isNull"):
                    start_upper_level = end_upper_level
            else:
                if hasattr(end_upper_level, "isNull") and end_upper_level.isNull():
                    end_upper_level = start_upper_level

            if start_upper_level is not None and start_lower_level is not None:
                start_height = float(start_upper_level) - float(start_lower_level)
                end_height = float(end_upper_level) - float(end_lower_level)

            # TODO: ^^^ perhaps add some logger.debug() to those 20 lines
            # above? It smells to me like there could possibly be some
            # unintended side effects.

            pump_def = {
                "id": "pump_" + str(pump["id"]),
                "type": self.PUMP,
                "start_node": pump["connection_node_start_id"],
                "end_node": pump["connection_node_end_id"],
                "start_level": start_lower_level,
                "end_level": end_lower_level,
                "start_height": start_height,
                "end_height": end_height,
            }
            lines.append(pump_def)

        channel_profiles = {}
        channel_calc_points = {}
        channel_cs_locations = {}

        for cs in cross_section_location_layer.getFeatures():

            ids = cs["channel_id"]
            if ids not in channel_cs_locations:
                channel_cs_locations[ids] = []

            channel_cs_locations[ids].append(cs)

        if model_line_layer is not None:
            # create indexed sets of calculation points
            request = QgsFeatureRequest().setFilterExpression(u"type='v2_channel'")
            for line in model_line_layer.getFeatures(request):
                ids = line["spatialite_id"]
                if ids not in channel_calc_points:
                    channel_calc_points[ids] = []
                channel_calc_points[ids].append(line)

        for channel in channel_layer.getFeatures():
            channel_profiles[channel["id"]] = []
            # prepare profile information of channel
            if channel["id"] in channel_cs_locations:
                crs_points = channel_cs_locations[channel["id"]]
            else:
                crs_points = []

            profile_channel_parts = split_line_at_points(
                channel.geometry(),
                crs_points,
                point_feature_id_field="id",
                start_node_id=None,
                end_node_id=None,
            )

            # split on cross section locations
            for i, part in enumerate(profile_channel_parts):

                if part["start_point_id"] is not None:
                    start_id = "crs_" + str(part["start_point_id"])
                else:
                    start_id = channel["connection_node_start_id"]

                if part["end_point_id"] is not None:
                    end_id = "crs_" + str(part["end_point_id"])
                else:
                    end_id = channel["connection_node_end_id"]

                channel_part = {
                    "id": "subch_" + str(channel["id"]) + "_" + str(i),
                    "type": self.CHANNEL,
                    "start_node": start_id,
                    "end_node": end_id,
                    "real_length": part["length"],
                    "sub_channel_nr": i,
                    "channel_id": channel["id"],
                    "start_channel_distance": part["distance_at_line"],
                }
                if model_line_layer is None:
                    # no calc points available, use cross sections to devide
                    # graph layer in parts
                    lines.append(channel_part)
                # use cross sections part for only as info for drawing
                # sideview
                channel_profiles[channel["id"]].append(channel_part)

            for p in crs_points:
                crs_def = profiles[p["definition_id"]]
                level = p["reference_level"] + crs_def["rel_bottom_level"]
                height = crs_def["height"]
                bank_level = p["bank_level"]

                points["crs_" + str(p["id"])] = {
                    "point": p.geometry().asPoint(),
                    "type": self.CROSS_SECTION,
                    "surface_level": bank_level,
                    "drain_level": bank_level,
                    "bottom_level": level,
                    "height": height,
                    "length": 0.0,
                }

            if model_line_layer is not None:
                # create channel part for each sub link (taking calculation
                # nodes into account)

                cpoints_idx = []
                cpoints = {}
                # get calculation points on line
                for line in channel_calc_points[channel["id"]]:
                    cpoints_idx.append(line["start_node_idx"])
                    cpoints[line["start_node_idx"]] = line.geometry().asPolyline()[0]
                    cpoints_idx.append(line["end_node_idx"])
                    cpoints[line["end_node_idx"]] = line.geometry().asPolyline()[-1]

                # all calculation nodes (points in between, must be a
                # startpoint as well as an endpoint, so 2 occurances)
                cpoint_count = dict(Counter(cpoints_idx))
                calc_points = [
                    key for key, value in list(cpoint_count.items()) if value == 2
                ]

                calculation_points = [
                    {"id": key, "geom": value}
                    for key, value in list(cpoints.items())
                    if key in calc_points
                ]

                channel_parts = split_line_at_points(
                    channel.geometry(),
                    calculation_points,
                    point_feature_id_field="id",
                    start_node_id=None,
                    end_node_id=None,
                )

                for i, part in enumerate(channel_parts):
                    if i == 0:
                        start_node_id = channel["connection_node_start_id"]
                    else:
                        start_node_id = "calc_" + str(part["start_point_id"])

                    if i == len(channel_parts) - 1:
                        end_node_id = channel["connection_node_end_id"]
                    else:
                        end_node_id = "calc_" + str(part["end_point_id"])

                    channel_part = {
                        "id": "subch_" + str(channel["id"]) + "_" + str(i),
                        "type": self.CHANNEL,
                        "start_node": start_node_id,
                        "end_node": end_node_id,
                        "start_node_idx": part["start_point_id"],
                        "end_node_idx": part["end_point_id"],
                        "real_length": part["length"],
                        "sub_channel_nr": i,
                        "channel_id": channel["id"],
                        "start_channel_distance": part["distance_at_line"],
                        "geom": part["geom"],
                    }
                    lines.append(channel_part)

                for p in calculation_points:
                    points["calc_" + str(p["id"])] = {
                        "point": p["geom"],
                        "type": self.CALCULATION_NODE,
                        "surface_level": None,
                        "drain_level": None,
                        "bottom_level": None,
                        "height": None,
                        "length": 0.0,
                    }

        #  make point dict permanent
        self.point_dict = points

        # create line layer
        uri = "LineString?crs=epsg:4326&index=yes"
        vl = QgsVectorLayer(uri, "graph_layer", "memory")
        pr = vl.dataProvider()

        pr.addAttributes(
            [
                # This is the flowline index in Python (0-based indexing)
                # Important: this differs from the feature id which is flowline
                # idx+1!!
                QgsField("nr", QVariant.Int),
                QgsField("id", QVariant.String, len=25),
                QgsField("type", QVariant.Int),
                QgsField("start_node", QVariant.String),
                QgsField("end_node", QVariant.String),
                QgsField("start_node_idx", QVariant.Int),
                QgsField("end_node_idx", QVariant.Int),
                QgsField("start_level", QVariant.Double),
                QgsField("end_level", QVariant.Double),
                QgsField("start_height", QVariant.Double),
                QgsField("end_height", QVariant.Double),
                QgsField("channel_id", QVariant.String, len=25),
                QgsField("sub_channel_nr", QVariant.Int),
                QgsField("start_channel_distance", QVariant.Double),
                QgsField("real_length", QVariant.Double),
            ]
        )
        # tell the vector layer to fetch changes from the provider
        vl.updateFields()

        features = []
        i = 0
        for line in lines:
            feat = QgsFeature()

            p1 = points[line["start_node"]]["point"]
            if python_value(line["end_node"]) is not None:
                p2 = points[line["end_node"]]["point"]
            else:
                p2 = QgsPointXY(p1.x(), p1.y() + 0.0001)

            geom = QgsGeometry.fromPolylineXY([p1, p2])
            # geom = line.get('geom', QgsGeometry.fromPolyline([p1, p2]))

            feat.setGeometry(geom)

            feat.setAttributes(
                [
                    i,
                    line["id"],
                    line["type"],
                    line["start_node"],
                    line["end_node"],
                    line.get("start_node_idx", None),
                    line.get("end_node_idx", None),
                    line.get("start_level", None),
                    line.get("end_level", None),
                    line.get("start_height", None),
                    line.get("end_height", None),
                    line.get("channel_id", None),
                    line.get("sub_channel_nr", None),
                    line.get("start_channel_distance", None),
                    line.get("real_length", None),
                ]
            )
            features.append(feat)
            i += 1

        pr.addFeatures(features)
        vl.updateExtents()

        QgsProject.instance().addMapLayer(vl)

        return vl, points, channel_profiles

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

        def haversine_clicked(coordinate):
            """Calculate the distance w.r.t. the clicked location."""
            lon1, lat1 = clicked_coordinate
            lon2, lat2 = coordinate.x(), coordinate.y()
            return haversine(lon1, lat1, lon2, lat2)

        selected_coordinates = reduce(
            lambda accum, f: accum
            + [f.geometry().vertexAt(0), f.geometry().vertexAt(1)],
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

        self.active_sideview.set_sideprofile(self.route.path, self.route.path_points)

        self.map_visualisation.set_sideview_route(self.route)

    def reset_sideview(self):
        self.route.reset()
        self.map_visualisation.reset()

        self.active_sideview.set_sideprofile([], [])

    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """
        self.select_sideview_button.clicked.disconnect(self.toggle_route_tool)
        self.reset_sideview_button.clicked.disconnect(self.reset_sideview)

        self.route_tool.deactivated.disconnect(self.unset_route_tool)

        self.unset_route_tool()

        self.active_sideview.profile_hovered.disconnect(
            self.map_visualisation.hover_graph
        )
        self.map_visualisation.close()

        for sideview_plot in self.sideviews:
            sideview_plot[1].on_close()

        # todo: find out how to unload layer from memory (done automic if
        # there are no references?)
        QgsProject.instance().removeMapLayer(self.vl_tree_layer.id())
        QgsProject.instance().removeMapLayer(self.line_layer.id())

    def closeEvent(self, event):
        """
        overwrite of QDockWidget class to emit signal
        :param event: QEvent
        """
        self.on_close()
        self.closingWidget.emit(self.nr)
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

        # add title to graph
        self.title_label = QLabel(self)
        self.title_label.setObjectName("TitleLabel")
        self.button_bar_hlayout.addWidget(self.title_label)

        self.select_sideview_button = QPushButton(self)
        self.select_sideview_button.setObjectName("SelectedSideview")
        self.button_bar_hlayout.addWidget(self.select_sideview_button)

        self.reset_sideview_button = QPushButton(self)
        self.reset_sideview_button.setObjectName("ResetSideview")
        self.button_bar_hlayout.addWidget(self.reset_sideview_button)

        spacer_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_bar_hlayout.addItem(spacer_item)
        self.main_vlayout.addItem(self.button_bar_hlayout)

        # add tabWidget for graphWidgets
        self.side_view_tab_widget = QTabWidget(self)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(6)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.side_view_tab_widget.sizePolicy().hasHeightForWidth()
        )
        self.side_view_tab_widget.setSizePolicy(size_policy)
        self.side_view_tab_widget.setObjectName("sideViewTabWidget")
        self.main_vlayout.addWidget(self.side_view_tab_widget)

        # add dockwidget
        dock_widget.setWidget(self.dock_widget_content)
        self.retranslate_ui(dock_widget)
        QMetaObject.connectSlotsByName(dock_widget)

    def retranslate_ui(self, dock_widget):
        # dock_widget.setWindowTitle(_translate(
        #    "DockWidget", "3Di sideview %i" % self.nr, None))
        self.title_label.setText(
            _translate("DockWidget", "3Di sideview nr. %i " % self.nr, None)
        )
        self.select_sideview_button.setText(
            _translate("DockWidget", "Choose sideview trajectory", None)
        )
        self.reset_sideview_button.setText(
            _translate("DockWidget", "Reset sideview trajectory", None)
        )
