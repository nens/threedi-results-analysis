# -*- coding: utf-8 -*-
from PyQt4.QtCore import Qt, QSize, QEvent, pyqtSignal, QMetaObject, QVariant
from PyQt4.QtGui import QTableView, QWidget, QVBoxLayout, QHBoxLayout, \
    QSizePolicy, QPushButton, QSpacerItem, QApplication, QTabWidget, \
    QDockWidget, QComboBox, QMessageBox, QColor, QCursor

import numpy as np
import os

from qgis.networkanalysis import QgsArcProperter
from qgis.networkanalysis import QgsLineVectorLayerDirector, QgsGraphBuilder,\
        QgsDistanceArcProperter, QgsGraphAnalyzer
import qgis
from qgis.core import QgsPoint, QgsRectangle, QgsCoordinateTransform, \
    QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsMapLayerRegistry, \
    QGis, QgsFeatureRequest, QgsDistanceArea, QgsCoordinateReferenceSystem
from qgis.gui import QgsRubberBand, QgsVertexMarker, QgsMapTool
from collections import Counter

from ..datasource.spatialite import get_object_type, layer_qh_type_mapping
from ..models.graph import LocationTimeseriesModel
from ..utils.user_messages import log, statusbar_message

from ..utils.route import Route
from ..utils import haversine

from ..utils.geo_processing import split_line_at_points


import pyqtgraph as pg
from qgis.core import QgsDataSourceURI

# GraphDockWidget labels related parameters.
# TODO: unorm is deprecated, now 'u1'
parameter_config = {
    'q': [{'name': 'Debiet', 'unit': 'm3/s', 'parameters': ['q']},
          {'name': 'Snelheid', 'unit': 'm/s', 'parameters': ['u1']}],
    'h': [{'name': 'Waterstand', 'unit': 'mNAP', 'parameters': ['s1']},
          {'name': 'Volume', 'unit': 'm3', 'parameters': ['vol']}]
}


def python_value(value, default_value=None):
    """
    help function for translating QVariant Null values into None
    :param value: QVariant value or python value
    :param default_value: value in case provided value is None
    :return: python value
    """

    # check on QVariantNull... type
    if hasattr(value, 'isNull') and value.isNull():
        if default_value is not None:
            return default_value
        else:
            return None
    else:
        if default_value is not None and value is None:
            return default_value
        else:
            return value


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


INTERPOLATION_PHYSICAL = 0 # interpolation based on all profiles
INTERPOLATION_CALCULATION = 1 # interpolation as the 3di calculation core is
                              # performing the interpolation. for bottom
                              # and surface level use profiles close to
                              # calculation points. For height (profile) first
                              # get heigth on centerpoints at links


class SideViewPlotWidget(pg.PlotWidget):
    """Side view plot element"""

    profile_route_updated = pyqtSignal()


    def __init__(self, parent=None, nr=0, line_layer=None, point_dict=None,
                 channel_profiles=None, tdi_root_tool=None, name=""):
        """

        :param parent: Qt parent widget
        """
        super(SideViewPlotWidget, self).__init__(parent)

        self.name = name
        self.nr = nr
        self.node_dict = point_dict
        self.line_layer = line_layer
        self.channel_profiles = channel_profiles
        self.time_slider = tdi_root_tool.timeslider_widget

        self.profile = []
        self.sideview_nodes = []

        self.showGrid(True, True, 0.5)
        self.setLabel("bottom", "Afstand", "m")
        self.setLabel("left", "Hoogte", "mNAP")

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

        pen = pg.mkPen(color=QColor(0, 255, 0), width=2,  style=Qt.DashLine)
        self.drain_level_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        pen = pg.mkPen(color=QColor(0, 255, 0), width=2)
        self.surface_level_plot = pg.PlotDataItem(np.array([(0.0, np.nan)]), pen=pen)

        self.fill = pg.FillBetweenItem(self.bottom_plot,
                                       self.upper_plot,
                                       pg.mkBrush(200, 200, 200))

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

    def set_sideprofile(self, profile, route_points):

        self.profile = profile
        self.sideview_nodes = []

        bottom_line = []
        upper_line = []
        drain_level = []
        surface_level = []

        first = True
        last_channel_id = None

        if len(profile) > 0:
            total_length = float(profile[-1][-1][1])

        for route_part in profile:
            sub_first = True
            last_channel_id = None
            route_part_total_distance = float(route_part[-1][1])
            for begin_dist, end_dist, distance, direction, feature in route_part:

                begin_dist = float(begin_dist)
                end_dist = float(end_dist)

                if direction == 1:
                    begin_node_id = feature['start_node']
                    end_node_id = feature['end_node']
                    begin_node_idx = feature['start_node_idx']
                    end_node_idx = feature['end_node_idx']
                else:
                    begin_node_id = feature['end_node']
                    end_node_id = feature['start_node']
                    end_node_idx = feature['start_node_idx']
                    begin_node_idx = feature['end_node_idx']

                ltype = feature['type']

                begin_node = self.node_dict[begin_node_id]
                end_node = self.node_dict[end_node_id]

                # 1. add manhole if needed
                if first and begin_node['type'] == SideViewDockWidget.MANHOLE:
                    # add contours of first manhole
                    bottom_line.append((begin_dist - 0.5 * float(
                                            begin_node['length']),
                                        begin_node['surface_level'],
                                        SideViewDockWidget.PIPE))
                    bottom_line.append((begin_dist - 0.5 * float(
                                            begin_node['length']),
                                        float(begin_node['bottom_level']),
                                        SideViewDockWidget.PIPE))
                    bottom_line.append((begin_dist + 0.5 * float(
                                            begin_node['length']),
                                        float(begin_node['bottom_level']),
                                        SideViewDockWidget.PIPE))

                    upper_line.append((begin_dist - 0.5 * float(
                                            begin_node['length']),
                                       float(begin_node['surface_level']),
                                       SideViewDockWidget.PIPE))
                    upper_line.append((begin_dist + 0.5 * float(
                                            begin_node['length']),
                                       float(begin_node['surface_level']),
                                       SideViewDockWidget.PIPE))

                # 2. add contours (bottom, upper, drain and surface lines)
                if (python_value(last_channel_id) is not None and
                            last_channel_id == feature['channel_id']):
                    # contours based on cross section lines already added, skip
                    # for this line element based on sideview
                    log('skip channel part')
                    pass
                elif ltype == SideViewDockWidget.CHANNEL:
                    # add all information of channel based on cross section
                    # do this for the relevant part of the channel at once

                    # get cross section channel information
                    profile_links = self.channel_profiles[feature['channel_id']]

                    max_length_on_channel = route_part_total_distance - begin_dist

                    # get relevant channel_profiles and sort based on direction
                    if direction == 1:
                        # get start distance from (selected) calc node layer 
                        channel_length = (profile_links[-1]['real_length'] +
                                 profile_links[-1]['start_channel_distance'])

                        # todo: error in this part - dist_from_begin is wrong
                        dist_from_begin = feature['start_channel_distance']
                        end_dist_from_begin = min(channel_length,
                                    dist_from_begin + max_length_on_channel)
                        length_on_channel = end_dist_from_begin - dist_from_begin

                        profile_links = [link for link in profile_links
                            if link['start_channel_distance'] +
                                link['real_length'] >= dist_from_begin and
                            link['start_channel_distance'] <= end_dist_from_begin]
                        profile_links = sorted(
                            profile_links,
                            key=lambda x: x['start_channel_distance'])
                    else:
                        # get start distance from (selected) calc node layer
                        dist_from_begin = (feature['start_channel_distance'] +
                                     feature['real_length'])
                        end_dist_from_begin =  max(dist_from_begin - max_length_on_channel, 0.0)
                        length_on_channel = dist_from_begin - end_dist_from_begin

                        profile_links = [link for link in profile_links
                            if link['start_channel_distance'] <= (dist_from_begin + 0.01) and
                            (link['start_channel_distance'] +
                                link['real_length']) >= (end_dist_from_begin - 0.01)]
                        profile_links = sorted(profile_links,
                            key=lambda x: x['start_channel_distance'],
                            reverse=True)

                    # get info at end point of needed
                    sub_distance = begin_dist
                    for i, link in enumerate(profile_links):
                        # begin of pipe
                        sub_begin_dist = sub_distance
                        if direction == 1:
                            link_left = max(link['start_channel_distance'],
                                             dist_from_begin)
                            link_right = min(link['start_channel_distance'] + link['real_length'],
                                             end_dist_from_begin)
                            link_length = link_right - link_left
                        else:
                            link_left = max(link['start_channel_distance'],
                                            end_dist_from_begin)
                            link_right = min(link['start_channel_distance'] + link['real_length'],
                                       dist_from_begin)
                            link_length = link_right - link_left

                        length_on_channel -= link_length
                        sub_distance += link_length
                        sub_end_dist = sub_distance

                        if direction == 1:
                            sub_begin_node_id = link['start_node']
                            sub_end_node_id = link['end_node']
                        else:
                            sub_begin_node_id = link['end_node']
                            sub_end_node_id = link['start_node']

                        sub_begin_node = self.node_dict[sub_begin_node_id]
                        sub_end_node = self.node_dict[sub_end_node_id]

                        if sub_begin_node['type'] in [SideViewDockWidget.CONNECTION_NODE, SideViewDockWidget.BOUNDARY]:
                            # take same levels as at the end of line
                            begin_level = sub_end_node['bottom_level']
                            begin_height = sub_end_node['height']
                            begin_surface = sub_end_node['surface_level']
                            begin_drain = sub_end_node['drain_level']
                        elif sub_first and sub_end_node['type'] not in [SideViewDockWidget.CONNECTION_NODE, SideViewDockWidget.BOUNDARY]:
                            # interpolate based on starting point
                            begin_weight = (link_length / link['real_length'])
                            end_weight = 1 - begin_weight
                            begin_level = (
                                begin_weight * sub_begin_node['bottom_level'] +
                                end_weight * sub_end_node['bottom_level'])
                            begin_height = (
                                begin_weight * sub_begin_node['height'] +
                                end_weight * sub_end_node['height'])
                            if (sub_begin_node['surface_level'] is not None and
                                sub_end_node['surface_level'] is not None):
                                begin_surface = (
                                    begin_weight * sub_begin_node['surface_level'] +
                                    end_weight * sub_end_node['surface_level'])
                            if (sub_begin_node['drain_level'] is not None and
                                sub_end_node['drain_level'] is not None):
                                begin_drain = (
                                    begin_weight * sub_begin_node['drain_level'] +
                                    end_weight * sub_end_node['drain_level'])
                        else:
                            begin_level = sub_begin_node['bottom_level']
                            begin_height = sub_begin_node['height']
                            begin_surface = sub_begin_node['surface_level']
                            begin_drain = sub_begin_node['drain_level']

                        if sub_end_node['type'] in [SideViewDockWidget.CONNECTION_NODE, SideViewDockWidget.BOUNDARY]:
                            end_level = sub_begin_node['bottom_level']
                            end_height = sub_begin_node['height']
                            end_surface = sub_begin_node['surface_level']
                            end_drain = sub_begin_node['drain_level']
                        elif i == len(profile_links) - 1 and sub_begin_node['type'] not in [SideViewDockWidget.CONNECTION_NODE, SideViewDockWidget.BOUNDARY]:
                            # interpolate based on starting point

                            end_weight = (link_length / link['real_length'])
                            begin_weight = 1 - end_weight
                            end_level = (
                                begin_weight * sub_begin_node['bottom_level'] +
                                end_weight * sub_end_node['bottom_level'])
                            end_height = (
                                begin_weight * sub_begin_node['height'] +
                                end_weight * sub_end_node['height'])

                            if (sub_begin_node['surface_level'] is not None and
                                sub_end_node['surface_level'] is not None):
                                end_surface = (
                                    begin_weight * sub_begin_node['surface_level'] +
                                    end_weight * sub_end_node['surface_level'])
                            else:
                                end_surface = np.nan

                            if (sub_begin_node['drain_level'] is not None and
                                sub_end_node['drain_level'] is not None):
                                end_drain = (
                                    begin_weight * sub_begin_node['drain_level'] +
                                    end_weight * sub_end_node['drain_level'])
                            else:
                                end_drain = np.nan

                        else:
                            end_level = sub_end_node['bottom_level']
                            end_height = sub_end_node['height']
                            end_surface = sub_end_node['surface_level']
                            end_drain = sub_end_node['drain_level']

                        bottom_line.append(
                            (sub_begin_dist + 0.5 * float(sub_begin_node['length']),
                             begin_level,
                             ltype))
                        bottom_line.append(
                            (sub_end_dist - 0.5 * float(sub_end_node['length']),
                             end_level,
                             ltype))
                        upper_line.append(
                            (sub_begin_dist + 0.5 * float(sub_begin_node['length']),
                             begin_level + begin_height,
                             ltype))
                        upper_line.append(
                            (sub_end_dist - 0.5 * float(sub_end_node['length']),
                             end_level + end_height,
                             ltype))

                        if (sub_first or sub_begin_node['type'] in [SideViewDockWidget.CONNECTION_NODE, SideViewDockWidget.BOUNDARY]):
                            drain_level.append((sub_begin_dist, begin_drain))
                            surface_level.append((sub_begin_dist, begin_surface))

                        drain_level.append((sub_end_dist, end_drain))
                        surface_level.append((sub_end_dist, end_surface))

                        sub_first = False
                else:
                    # structure or pipe
                    if direction == 1:
                        begin_level = float(feature['start_level'])
                        end_level = float(feature['end_level'])
                        begin_height = float(feature['start_height'])
                        end_height = float(feature['end_height'])
                    else:
                        begin_level = float(feature['end_level'])
                        end_level = float(feature['start_level'])
                        begin_height = float(feature['end_height'])
                        end_height = float(feature['start_height'])

                    bottom_line.append(
                        (begin_dist + 0.5 * float(begin_node['length']),
                         begin_level,
                         ltype))
                    bottom_line.append(
                        (end_dist-0.5*float(end_node['length']),
                         end_level,
                         ltype))

                    # upper line
                    upper_line.append(
                        (begin_dist + 0.5 * float(begin_node['length']),
                        begin_level + begin_height,
                        ltype))
                    upper_line.append(
                        (end_dist - 0.5 * float(end_node['length']),
                        end_level + end_height,
                        ltype))

                    if first:
                        drain_level.append((begin_dist,
                                            begin_node['drain_level']))
                        surface_level.append((begin_dist,
                                              begin_node['surface_level']))

                    drain_level.append((end_dist, end_node['drain_level']))
                    surface_level.append((end_dist, end_node['surface_level']))

                last_channel_id = feature['channel_id']

                if end_node['type'] == SideViewDockWidget.MANHOLE:
                    bottom_line.append((end_dist-0.5*float(end_node['length']), float(end_node['bottom_level']), SideViewDockWidget.PIPE))
                    bottom_line.append((end_dist+0.5*float(end_node['length']), float(end_node['bottom_level']), SideViewDockWidget.PIPE))
                    # todo last: bottom_line.append((float(begin_dist)+0,5*float(end_node['length']), float(begin_node['surface_level'])))

                if end_node['type'] == SideViewDockWidget.MANHOLE:
                    upper_line.append((end_dist-0.5*float(end_node['length']), float(end_node['surface_level']), SideViewDockWidget.PIPE))
                    upper_line.append((end_dist+0.5*float(end_node['length']), float(end_node['surface_level']), SideViewDockWidget.PIPE))


                # store node information for water level line
                if first:
                    self.sideview_nodes.append({'distance': begin_dist,
                                               'id': begin_node_id,
                                                'idx': begin_node_idx})
                    first = False

                self.sideview_nodes.append({'distance': end_dist,
                                           'id': end_node_id,
                                            'idx': end_node_idx})

        if len(profile) > 0:

            # split upper and lower line into different line types (with
            # different styling

            tables  = {
                SideViewDockWidget.PIPE: [],
                SideViewDockWidget.CHANNEL: [],
                SideViewDockWidget.CULVERT: [],
                SideViewDockWidget.PUMP: [],
                SideViewDockWidget.WEIR: [],
                SideViewDockWidget.ORIFICE: []
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

            ts_table = np.array([(b[0], b[1]) for b in bottom_line],
                                dtype=float)
            self.bottom_plot.setData(ts_table, connect='finite')

            ts_table = np.array(tables[SideViewDockWidget.PIPE], dtype=float)
            self.sewer_bottom_plot.setData(ts_table, connect='finite')

            ts_table = np.array(tables[SideViewDockWidget.CHANNEL], dtype=float)
            self.channel_bottom_plot.setData(ts_table, connect='finite')

            ts_table = np.array(tables[SideViewDockWidget.CULVERT], dtype=float)
            self.culvert_bottom_plot.setData(ts_table, connect='finite')

            ts_table = np.array(tables[SideViewDockWidget.WEIR], dtype=float)
            self.weir_bottom_plot.setData(ts_table, connect='finite')

            ts_table = np.array(tables[SideViewDockWidget.ORIFICE], dtype=float)
            self.orifice_bottom_plot.setData(ts_table, connect='finite')

            ts_table = np.array(tables[SideViewDockWidget.PUMP], dtype=float)
            self.pump_bottom_plot.setData(ts_table, connect='finite')

            tables = {
                SideViewDockWidget.PIPE: [],
                SideViewDockWidget.CHANNEL: [],
                SideViewDockWidget.CULVERT: [],
                SideViewDockWidget.PUMP: [],
                SideViewDockWidget.WEIR: [],
                SideViewDockWidget.ORIFICE: []
            }
            last_type = None
            for point in upper_line:
                ptype = point[2]

                if ptype != last_type:
                    if last_type is not None:
                        tables[ptype].append((point[0], np.nan))
                    last_type = ptype

                tables[ptype].append((point[0], point[1]))

            ts_table = np.array([(b[0], b[1]) for b in upper_line],
                                    dtype=float)
            self.upper_plot.setData(ts_table, connect='finite')

            ts_table = np.array(tables[SideViewDockWidget.PIPE], dtype=float)
            self.sewer_upper_plot.setData(ts_table, connect='finite')

            ts_table = np.array(tables[SideViewDockWidget.CHANNEL], dtype=float)
            self.channel_upper_plot.setData(ts_table, connect='finite')

            ts_table = np.array(tables[SideViewDockWidget.CULVERT], dtype=float)
            self.culvert_upper_plot.setData(ts_table, connect='finite')

            ts_table = np.array(tables[SideViewDockWidget.WEIR], dtype=float)
            self.weir_upper_plot.setData(ts_table, connect='finite')

            ts_table = np.array(tables[SideViewDockWidget.ORIFICE], dtype=float)
            self.orifice_upper_plot.setData(ts_table, connect='finite')

            ts_table = np.array(tables[SideViewDockWidget.PUMP], dtype=float)
            self.pump_upper_plot.setData(ts_table, connect='finite')

            ts_table = np.array(drain_level, dtype=float)
            self.drain_level_plot.setData(ts_table, connect='finite')

            ts_table = np.array(surface_level, dtype=float)
            self.surface_level_plot.setData(ts_table, connect='finite')

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

        ds_item = self.time_slider.get_current_ts_datasource_item()
        if ds_item:
            ds = ds_item.datasource()
            for node in self.sideview_nodes:
                try:
                    if python_value(node['idx']) is not None:
                        ts = ds.get_timeseries('nodes',
                                               int(node['idx']+1),
                                               ['s1'])
                    else:
                        ts = ds.get_timeseries('v2_connection_nodes',
                                               node['id'],
                                               ['s1'])
                    node['timeseries'] = ts
                except KeyError:
                    node['timeseries'] = None

            self.draw_waterlevel_line()

        else:
             # reset water level line
            ts_table = np.array(np.array([(0.0, np.nan)]), dtype=float)
            self.water_level_plot.setData(ts_table)

    def draw_waterlevel_line(self):

        timestamp_nr = self.time_slider.value()

        water_level_line = []
        for node in self.sideview_nodes:
            if node['timeseries'] is not None:
                water_level = node['timeseries'][timestamp_nr][1]
                water_level_line.append((node['distance'], water_level))
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
        log('close sideview graph')
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
        point_ll = self.canvas.getCoordinateTransform().toMapCoordinates(x-5,
                                                                         y-5)
        point_ru = self.canvas.getCoordinateTransform().toMapCoordinates(x+5,
                                                                         y+5)
        rect = QgsRectangle(min(point_ll.x(), point_ru.x()),
                            min(point_ll.y(), point_ru.y()),
                            max(point_ll.x(), point_ru.x()),
                            max(point_ll.y(), point_ru.y()))

        transform = QgsCoordinateTransform(
            self.canvas.mapSettings().destinationCrs(), self.line_layer.crs())

        rect = transform.transform(rect)
        filter = QgsFeatureRequest().setFilterRect(rect)
        selected = self.line_layer.getFeatures(filter)

        clicked_point = self.canvas.getCoordinateTransform(
            ).toMapCoordinates(x, y)
        # transform to wgs84 (lon, lat) if not already:
        transformed_point = transform.transform(clicked_point)

        selected_points = [s for s in selected]
        if len(selected_points) > 0:
            self.callback_on_select(selected_points, transformed_point)

    def activate(self):
        self.canvas.setCursor(QCursor(Qt.CrossCursor))
        print("Route tool activated")

    def deactivate(self):
        self.deactivated.emit()
        self.canvas.setCursor(QCursor(Qt.ArrowCursor))
        print("Route tool deactivated")

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return False

class CustomDistancePropeter(QgsArcProperter):
    """custom properter for graph layer"""

    def __init__(self):
        QgsArcProperter.__init__(self)

    def property(self, distance, feature):
        value = feature['real_length']
        if python_value(value) is None:
            value = distance # feature.geometry().length()
        return value

    def requiredAttributes(self):
        # Must be a list of the attribute indexes (int), not strings:
        attributes = []
        return attributes


class SideViewDockWidget(QDockWidget):
    """Main Dock Widget for showing 3di results in Graphs"""

    # todo:
    # toon vlaggetje bij geselecteerde punten
    # meer punten achter elkaar selecteerbaar
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


    def __init__(self, iface, parent_widget=None,
                 parent_class=None, nr=0, tdi_root_tool=None):
        """Constructor"""
        super(SideViewDockWidget, self).__init__(parent_widget)

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
        self.line_layer, self.point_dict, self.channel_profiles = \
            self.create_combined_layers(
                self.tdi_root_tool.ts_datasource.model_spatialite_filepath,
                tdi_root_tool.line_layer)

        self.sideviews = []
        widget = SideViewPlotWidget(self, 0,
                                    self.line_layer,
                                    self.point_dict,
                                    self.channel_profiles,
                                    self.tdi_root_tool,
                                    "name")
        self.active_sideview = widget
        self.sideviews.append((0, widget))
        self.side_view_tab_widget.addTab(widget, widget.name)

        # init route graph
        director = QgsLineVectorLayerDirector(self.line_layer, -1, '', '', '', 3)

        self.route = Route(self.line_layer, director, id_field='nr',
                           weight_properter=CustomDistancePropeter(),
                           distance_properter=CustomDistancePropeter())

        # link route map tool
        self.route_tool = RouteTool(self.iface.mapCanvas(),
                                    self.line_layer,
                                    self.on_route_point_select)

        self.route_tool.deactivated.connect(self.unset_route_tool)

        # temp layer for side profile trac
        self.rb = QgsRubberBand(self.iface.mapCanvas())
        self.rb.setColor(Qt.red)
        self.rb.setWidth(2)

        # temp layer for last selected point
        self.point_markers = QgsVertexMarker(self.iface.mapCanvas())

        # add tree layer to map (for fun and testing purposes)
        self.vl_tree_layer = self.route.get_virtual_tree_layer()

        self.vl_tree_layer.loadNamedStyle(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), os.pardir,
                'layer_styles', 'tools', 'tree.qml'))

        QgsMapLayerRegistry.instance().addMapLayer(self.vl_tree_layer)

    def create_combined_layers(self, spatialite_path, model_line_layer):

        # if model_line_layer is None:
        #     canvas = self.tdi_root_tool.iface.mapCanvas()
        #     model_line_layer = canvas.currentLayer()

        def get_layer(spatialite_path, table_name, geom_column=''):
            uri2 = QgsDataSourceURI()
            uri2.setDatabase(spatialite_path)
            uri2.setDataSource('', table_name, geom_column)

            return QgsVectorLayer(uri2.uri(),
                                   table_name,
                                   'spatialite')
        # connection node layer
        profile_layer = get_layer(spatialite_path,
                                  'v2_cross_section_definition')

        cross_section_location_layer = get_layer(spatialite_path,
                                  'v2_cross_section_location', 'the_geom')

        connection_node_layer = get_layer(spatialite_path,
                                          'v2_connection_nodes',
                                          'the_geom')
        manhole_layer = get_layer(spatialite_path, 'v2_manhole')
        boundary_layer = get_layer(spatialite_path,
                                   'v2_1d_boundary_conditions')
        pipe_layer = get_layer(spatialite_path, 'v2_pipe')
        channel_layer = get_layer(spatialite_path, 'v2_channel', 'the_geom')
        weir_layer = get_layer(spatialite_path, 'v2_weir')
        orifice_layer = get_layer(spatialite_path, 'v2_orifice')
        pump_layer = get_layer(spatialite_path, 'v2_pumpstation')
        culvert_layer = get_layer(spatialite_path, 'v2_culvert')

        lines = []
        points = {}
        profiles = {}
        for profile in profile_layer.getFeatures():
            # todo: add support for other definitions
            rel_bottom_level = 0
            open = False
            if profile['shape'] == 1:
                # rectangle
                if profile['height'] is not None:
                    height = float(profile['height'])
                else:
                    # square
                    height = float(profile['width'])

            elif profile['shape'] == 2:
                # round
                height = float(profile['width'])
            elif profile['shape'] in [5, 6]:
                # tabulated and tabulated interpolated
                height_list = profile['height'].split(' ')
                rel_bottom_level = float(height_list[0])
                height = float(height_list[-1]) - rel_bottom_level
                if float(profile['width'].split(' ')[-1]) > 0.01:
                    open = True

            profiles[profile['id']] = {
                'height': height,
                'rel_bottom_level': rel_bottom_level,
                'open': open
            }


        for cn in connection_node_layer.getFeatures():
            points[cn['id']] = {
                'point': cn.geometry().asPoint(),
                'type': self.CONNECTION_NODE,
                'surface_level': None,
                'drain_level': None,
                'bottom_level': None,
                'length': 0.0
            }
        for manhole in manhole_layer.getFeatures():
            p = points[manhole['connection_node_id']]
            p['type'] = self.MANHOLE
            p['surface_level'] = python_value(manhole['surface_level'])
            p['drain_level'] = python_value(manhole['drain_level'],
                                            p['surface_level'])
            p['bottom_level'] = python_value(manhole['bottom_level'])
            p['length'] = python_value(manhole['width'], 0.0)

        # todo: add calculation nodes

        for bound in boundary_layer.getFeatures():
            p = points[bound['connection_node_id']]
            p['type'] = self.BOUNDARY
            p['surface_level'] = None
            p['drain_level'] = None
            p['bottom_level'] = None
            p['length'] = 0.0

        for pipe in pipe_layer.getFeatures():
            # note: no support of calculation nodes on pipes
            profile = profiles[pipe['cross_section_definition_id']]
            pipe_def ={
                'id': 'pipe_' + str(pipe['id']),
                'type': self.PIPE,
                'start_node': pipe['connection_node_start_id'],
                'end_node': pipe['connection_node_end_id'],
                'start_level': pipe['invert_level_start_point'] +
                        profile['rel_bottom_level'],
                'end_level': pipe['invert_level_end_point']  +
                        profile['rel_bottom_level'],
                'start_height': profile['height'],
                'end_height': profile['height']
            }

            lines.append(pipe_def)

        for orifice in orifice_layer.getFeatures():
            profile = profiles[orifice['cross_section_definition_id']]
            orifice_def = {
                'id': 'orifice_' + str(orifice['id']),
                'type': self.ORIFICE,
                'start_node': orifice['connection_node_start_id'],
                'end_node': orifice['connection_node_end_id'],
                'start_level': orifice['crest_level'],
                'end_level': orifice['crest_level'],
                'start_height': profile['height'],
                'end_height': profile['height']
            }
            lines.append(orifice_def)

        for weir in weir_layer.getFeatures():
            profile = profiles[weir['cross_section_definition_id']]

            weir_def = {
                'id': 'weir_' + str(weir['id']),
                'type': self.WEIR,
                'start_node': weir['connection_node_start_id'],
                'end_node': weir['connection_node_end_id'],
                'start_level': weir['crest_level'],
                'end_level': weir['crest_level'],
                'start_height': profile['height'],
                'end_height': profile['height']
            }
            lines.append(weir_def)

        for culvert in culvert_layer.getFeatures():
            profile = profiles[culvert['cross_section_definition_id']]

            culvert_def = {
                'id': 'culvert_' + str(culvert['id']),
                'type': self.CULVERT,
                'start_node': culvert['connection_node_start_id'],
                'end_node': culvert['connection_node_end_id'],
                'start_level': culvert['invert_level_start_point'] +
                                profile['rel_bottom_level'],
                'end_level': culvert['invert_level_end_point'] +
                                profile['rel_bottom_level'],
                'start_height': profile['height'],
                'end_height': profile['height']
            }
            lines.append(culvert_def)

        for pump in pump_layer.getFeatures():

            start_upper_level = pump['start_level_suction_side']
            end_upper_level = pump['start_level_delivery_side']
            start_lower_level = pump['stop_level_suction_side']
            end_lower_level = pump['stop_level_delivery_side']
            start_height = None
            end_height = None

            # default values from each other
            # QpyNullVariant is behaving strange,
            if hasattr(start_lower_level, 'isNull') and start_lower_level.isNull():
                if not hasattr(end_lower_level, 'isNull'):
                    start_lower_level = end_lower_level
            else:
                if hasattr(end_lower_level, 'isNull') and end_lower_level.isNull():
                    end_lower_level = start_lower_level

            if hasattr(start_upper_level, 'isNull') and start_upper_level.isNull():
                if not hasattr(end_upper_level, 'isNull'):
                    start_upper_level = end_upper_level
            else:
                if hasattr(end_upper_level,
                           'isNull') and end_upper_level.isNull():
                    end_upper_level = start_upper_level

            if start_upper_level is not None and start_lower_level is not None:
                start_height = float(start_upper_level) - float(start_lower_level)
                end_height = float(end_upper_level) - float(end_lower_level)

            pump_def = {
                'id': 'pump_' + str(pump['id']),
                'type': self.PUMP,
                'start_node': pump['connection_node_start_id'],
                'end_node': pump['connection_node_end_id'],
                'start_level': start_lower_level,
                'end_level': end_lower_level,
                'start_height': start_height,
                'end_height': end_height
            }
            lines.append(pump_def)

        channel_profiles = {}
        channel_calc_points = {}
        channel_cs_locations = {}

        for cs in cross_section_location_layer.getFeatures():

            ids = cs['channel_id']
            if ids not in channel_cs_locations:
                channel_cs_locations[ids] = []

            channel_cs_locations[ids].append(cs)

        if model_line_layer is not None:
            # create indexed sets of calculation points
            request = QgsFeatureRequest().setFilterExpression(
                    u"type='v2_channel'")
            for line in model_line_layer.getFeatures(request):
                ids = line['spatialite_id']
                if ids not in channel_calc_points:
                    channel_calc_points[ids] = []
                channel_calc_points[ids].append(line)

        for channel in channel_layer.getFeatures():
            channel_profiles[channel['id']] = []
            # prepare profile information of channel
            if channel['id'] in channel_cs_locations:
                crs_points = channel_cs_locations[channel['id']]
            else:
                crs_points = []

            profile_channel_parts = split_line_at_points(
                                        channel.geometry(),
                                        crs_points,
                                        point_feature_id_field='id',
                                        start_node_id=None,
                                        end_node_id=None)

            # split on cross section locations
            for i, part in enumerate(profile_channel_parts):

                if part['start_point_id'] is not None:
                    start_id = "crs_" + str(part['start_point_id'])
                else:
                    start_id = channel['connection_node_start_id']

                if part['end_point_id'] is not None:
                    end_id = "crs_" + str(part['end_point_id'])
                else:
                    end_id = channel['connection_node_end_id']

                channel_part = {
                    'id': 'subch_' + str(channel['id']) + '_' + str(i),
                    'type': self.CHANNEL,
                    'start_node': start_id,
                    'end_node': end_id,
                    'real_length': part['length'],
                    'sub_channel_nr': i,
                    'channel_id': channel['id'],
                    'start_channel_distance': part['distance_at_line']
                }
                if model_line_layer is None:
                    # no calc points available, use cross sections to devide
                    # graph layer in parts
                    lines.append(channel_part)
                # use cross sections part for only as info for drawing
                # sideview
                channel_profiles[channel['id']].append(channel_part)

            for p in crs_points:
                crs_def = profiles[p['definition_id']]
                level = p['reference_level'] + crs_def['rel_bottom_level']
                height = crs_def['height']
                bank_level = p['bank_level']

                points['crs_'+ str(p['id'])] = {
                    'point': p.geometry().asPoint(),
                    'type': self.CROSS_SECTION,
                    'surface_level': bank_level,
                    'drain_level': bank_level,
                    'bottom_level': level,
                    'height': height,
                    'length': 0.0
                }

            if model_line_layer is not None:
                # create channel part for each sub link (taking calculation
                # nodes into account)

                cpoints_idx = []
                cpoints = {}
                # get calculation points on line
                for line in channel_calc_points[str(channel['id'])]:
                    cpoints_idx.append(line['start_node_idx'])
                    cpoints[line['start_node_idx']] = \
                                line.geometry().asPolyline()[0]
                    cpoints_idx.append(line['end_node_idx'])
                    cpoints[line['end_node_idx']] = \
                                line.geometry().asPolyline()[-1]

                # all calculation nodes (points in between, must be a
                # startpoint as well as an endpoint, so 2 occurances)
                cpoint_count = dict(Counter(cpoints_idx))
                calc_points = [key for key, value in
                               cpoint_count.items() if value == 2]

                calculation_points = [{'id': key, 'geom': value} for key, value
                               in cpoints.items() if key in calc_points]

                channel_parts = split_line_at_points(
                                            channel.geometry(),
                                            calculation_points,
                                            point_feature_id_field='id',
                                            start_node_id=None,
                                            end_node_id=None)

                for i, part in enumerate(channel_parts):
                    if i == 0:
                        start_node_id = channel['connection_node_start_id']
                    else:
                        start_node_id = 'calc_' + str(part['start_point_id'])

                    if i == len(channel_parts)-1:
                        end_node_id = channel['connection_node_end_id']
                    else:
                        end_node_id = 'calc_' + str(part['end_point_id'])

                    channel_part = {
                        'id': 'subch_' + str(channel['id']) + '_' + str(i),
                        'type': self.CHANNEL,
                        'start_node': start_node_id,
                        'end_node': end_node_id,
                        'start_node_idx': part['start_point_id'],
                        'end_node_idx': part['end_point_id'],
                        'real_length': part['length'],
                        'sub_channel_nr': i,
                        'channel_id': channel['id'],
                        'start_channel_distance': part['distance_at_line'],
                        'geom': part['geom']
                    }
                    lines.append(channel_part)

                for p in calculation_points:
                    points['calc_'+ str(p['id'])] = {
                        'point': p['geom'],
                        'type': self.CALCULATION_NODE,
                        'surface_level': None,
                        'drain_level': None,
                        'bottom_level': None,
                        'height': None,
                        'length': 0.0
                    }

        #  make point dict permanent
        self.point_dict = points

        # create line layer
        uri = "LineString?crs=epsg:4326&index=yes"
        vl = QgsVectorLayer(uri, "graph_layer", "memory")
        pr = vl.dataProvider()

        pr.addAttributes([
            # This is the flowline index in Python (0-based indexing)
            # Important: this differs from the feature id which is flowline idx+1!!
            QgsField("nr", QVariant.Int),
            QgsField("id", QVariant.String, len=25),
            QgsField("type", QVariant.Int),
            QgsField("start_node", QVariant.Int),
            QgsField("end_node", QVariant.Int),
            QgsField("start_node_idx", QVariant.Int),
            QgsField("end_node_idx", QVariant.Int),
            QgsField("start_level", QVariant.Double),
            QgsField("end_level", QVariant.Double),
            QgsField("start_height", QVariant.Double),
            QgsField("end_height", QVariant.Double),
            QgsField("channel_id", QVariant.String, len=25),
            QgsField("sub_channel_nr", QVariant.Int),
            QgsField("start_channel_distance", QVariant.Double),
            QgsField("real_length", QVariant.Double)
        ])
        vl.updateFields()  # tell the vector layer to fetch changes from the provider

        features = []
        i = 0
        for line in lines:
            feat = QgsFeature()

            p1 = points[line['start_node']]['point']
            if python_value(line['end_node']) is not None:
                p2 = points[line['end_node']]['point']
            else:
                p2 = QgsPoint(p1.x(), p1.y()+0.0001)

            geom = QgsGeometry.fromPolyline([p1, p2])
            # geom = line.get('geom', QgsGeometry.fromPolyline([p1, p2]))

            feat.setGeometry(geom)

            feat.setAttributes([
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
            ])
            features.append(feat)
            i += 1

        pr.addFeatures(features)
        vl.updateExtents()

        QgsMapLayerRegistry.instance().addMapLayer(vl)

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
            lon2, lat2 = coordinate
            return haversine(lon1, lat1, lon2, lat2)

        selected_coordinates = reduce(
            lambda accum, f: accum + [f.geometry().vertexAt(0),
                                      f.geometry().vertexAt(1)],
            selected_features, [])

        if len(selected_coordinates) == 0:
            return

        closest_point = min(selected_coordinates, key=haversine_clicked)
        next_point = QgsPoint(closest_point)

        success, msg = self.route.add_point(next_point)

        if not success:
            statusbar_message(msg)

        self.active_sideview.set_sideprofile(self.route.path,
                                             self.route.path_points)

        transform = QgsCoordinateTransform(self.line_layer.crs(),
                                           self.iface.mapCanvas().mapRenderer().destinationCrs())

        self.rb.reset()
        for pnt in self.route.path_vertexes:
            t_pnt = transform.transform(pnt)
            self.rb.addPoint(t_pnt)

    def reset_sideview(self):
        self.route.reset()
        self.rb.reset()
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

        self.rb.reset()

        for sideview_plot in self.sideviews:
            sideview_plot[1].on_close()

        # todo: find out how to unload layer from memory (done automic if
        # there are no references?)
        QgsMapLayerRegistry.instance().removeMapLayer(self.vl_tree_layer.id())
        QgsMapLayerRegistry.instance().removeMapLayer(self.line_layer.id())

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
        self.select_sideview_button = QPushButton(self)
        self.select_sideview_button.setObjectName("SelectedSideview")
        self.button_bar_hlayout.addWidget(self.select_sideview_button)

        self.reset_sideview_button = QPushButton(self)
        self.reset_sideview_button.setObjectName("ResetSideview")
        self.button_bar_hlayout.addWidget(self.reset_sideview_button)

        spacer_item = QSpacerItem(40,
                                  20,
                                  QSizePolicy.Expanding,
                                  QSizePolicy.Minimum)
        self.button_bar_hlayout.addItem(spacer_item)
        self.main_vlayout.addItem(self.button_bar_hlayout)

        # add tabWidget for graphWidgets
        self.side_view_tab_widget = QTabWidget(self)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(6)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
                self.side_view_tab_widget.sizePolicy().hasHeightForWidth())
        self.side_view_tab_widget.setSizePolicy(size_policy)
        self.side_view_tab_widget.setObjectName("sideViewTabWidget")
        self.main_vlayout.addWidget(self.side_view_tab_widget)

        # add dockwidget
        dock_widget.setWidget(self.dock_widget_content)
        self.retranslate_ui(dock_widget)
        QMetaObject.connectSlotsByName(dock_widget)

    def retranslate_ui(self, dock_widget):
        dock_widget.setWindowTitle(_translate(
            "DockWidget", "3di sideview %i" % self.nr, None))
        self.select_sideview_button.setText(_translate(
            "DockWidget", "Kies sideview traject", None))


        self.reset_sideview_button.setText(_translate(
            "DockWidget", "Reset sideview traject", None))
