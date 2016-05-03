# -*- coding: utf-8 -*-
from PyQt4.QtCore import Qt, QSize, QEvent, pyqtSignal, QMetaObject, QVariant
from PyQt4.QtGui import QTableView, QWidget, QVBoxLayout, QHBoxLayout, \
    QSizePolicy, QPushButton, QSpacerItem, QApplication, QTabWidget, \
    QDockWidget, QComboBox, QMessageBox, QColor, QCursor

import numpy as np
import os


from qgis.networkanalysis import QgsLineVectorLayerDirector, QgsGraphBuilder,\
        QgsDistanceArcProperter, QgsGraphAnalyzer
import qgis
from qgis.core import QgsPoint, QgsRectangle, QgsCoordinateTransform, \
    QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsMapLayerRegistry, \
    QGis
from qgis.gui import QgsRubberBand, QgsVertexMarker, QgsMapTool

from ..datasource.spatialite import get_object_type, layer_qh_type_mapping
from ..models.graph import LocationTimeseriesModel
from ..utils.user_messages import log, statusbar_message

from ..utils.route import Route


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


class SideViewPlotWidget(pg.PlotWidget):
    """Side view plot element"""

    profile_route_updated = pyqtSignal()

    def __init__(self, parent=None, nr=0, line_layer=None, point_dict=None, tdi_root_tool=None, name=""):
        """

        :param parent: Qt parent widget
        """
        super(SideViewPlotWidget, self).__init__(parent)

        self.name = name
        self.nr = nr
        self.node_dict = point_dict
        self.line_layer = line_layer
        self.time_slider = tdi_root_tool.timeslider_widget

        self.profile = []
        self.profile_nodes = []

        self.showGrid(True, True, 0.5)
        self.setLabel("bottom", "Afstand", "m")
        self.setLabel("left", "Hoogte", "mNAP")

        pen = pg.mkPen(color=QColor(30, 30 , 30), width=2)

        self.bottom_plot = pg.PlotDataItem(np.array([(0.0, 0.0)]), pen=pen)
        self.upper_plot = pg.PlotDataItem(np.array([(0.0, 0.0)]), pen=pen)

        pen = pg.mkPen(color=QColor(0, 255, 0), width=2,  style=Qt.DashLine)
        self.drain_level_plot = pg.PlotDataItem(np.array([(0.0, 0.0)]), pen=pen)
        pen = pg.mkPen(color=QColor(0, 255, 0), width=2)
        self.surface_level_plot = pg.PlotDataItem(np.array([(0.0, 0.0)]), pen=pen)

        self.fill = pg.FillBetweenItem(self.bottom_plot,
                                       self.upper_plot,
                                       pg.mkBrush(200, 200, 200))

        pen = pg.mkPen(color=QColor(0, 255, 255), width=2)
        self.water_level_plot = pg.PlotDataItem(np.array([(0.0, 0.0)]), pen=pen)

        self.addItem(self.drain_level_plot)
        self.addItem(self.surface_level_plot)
        self.addItem(self.fill)
        self.addItem(self.bottom_plot)
        self.addItem(self.upper_plot)
        self.addItem(self.water_level_plot)

        # set listeners to signals
        self.profile_route_updated.connect(self.update_water_level_cache)
        self.time_slider.valueChanged.connect(self.draw_waterlevel_line)
        self.time_slider.datasource_changed.connect(self.update_water_level_cache)

    def set_sideprofile(self, profile, route_points):

        self.profile = profile
        self.profile_nodes = []

        bottom_line = []
        upper_line = []
        drain_level = []
        surface_level = []

        first = True

        for route_part in profile:
            for begin_dist, end_dist, distance, direction, feature in route_part:

                if direction == 1:
                    begin_level = feature['start_level']
                    end_level = feature['end_level']
                    begin_node_id = feature['start_node']
                    end_node_id = feature['end_node']
                    begin_height = feature['start_height']
                    end_height = feature['end_height']
                else:
                    begin_level = feature['end_level']
                    end_level = feature['start_level']
                    begin_node_id = feature['end_node']
                    end_node_id = feature['start_node']
                    begin_height = feature['end_height']
                    end_height = feature['start_height']


                # request = QgsFeatureRequest().setFilterExpression(u'"id" = %s' % str(begin_node_id))
                # begin_node = self.node_layer.getFeatures(request).next()
                # request = QgsFeatureRequest().setFilterExpression(u'"id" = %s' % str(end_node_id))
                # end_node = self.node_layer.getFeatures(request).next()

                begin_node = self.node_dict[begin_node_id]
                end_node = self.node_dict[end_node_id]

                # bottom line
                if first and begin_node['type'] == SideViewDockWidget.MANHOLE:
                    bottom_line.append((float(begin_dist)-0.5*float(begin_node['length']), float(begin_node['surface_level'])))
                    bottom_line.append((float(begin_dist)-0.5*float(begin_node['length']), float(begin_node['bottom_level'])))
                    bottom_line.append((float(begin_dist)+0.5*float(begin_node['length']), float(begin_node['bottom_level'])))

                bottom_line.append((float(begin_dist)+0.5*float(begin_node['length']), float(begin_level)))
                bottom_line.append((float(end_dist)-0.5*float(end_node['length']), float(end_level)))

                if end_node['type'] == SideViewDockWidget.MANHOLE:
                    bottom_line.append((float(end_dist)-0.5*float(end_node['length']), float(end_node['bottom_level'])))
                    bottom_line.append((float(end_dist)+0.5*float(end_node['length']), float(end_node['bottom_level'])))
                    # todo last: bottom_line.append((float(begin_dist)+0,5*float(end_node['length']), float(begin_node['surface_level'])))

                # upper line

                if first and begin_node['type'] == SideViewDockWidget.MANHOLE:
                    upper_line.append((float(begin_dist)-0.5*float(begin_node['length']), float(begin_node['surface_level'])))
                    upper_line.append((float(begin_dist)+0.5*float(begin_node['length']), float(begin_node['surface_level'])))

                upper_line.append((float(begin_dist)+0.5*float(begin_node['length']), float(begin_level)+float(begin_height)))
                upper_line.append((float(end_dist)-0.5*float(end_node['length']), float(end_level)+float(end_height)))

                if end_node['type'] == SideViewDockWidget.MANHOLE:
                    upper_line.append((float(end_dist)-0.5*float(end_node['length']), float(end_node['surface_level'])))
                    upper_line.append((float(end_dist)+0.5*float(end_node['length']), float(end_node['surface_level'])))

                if first:
                    drain_level.append((float(begin_dist), begin_node['drain_level']))
                    surface_level.append((float(begin_dist), begin_node['surface_level']))

                drain_level.append((float(end_dist), end_node['drain_level']))
                surface_level.append((float(end_dist), end_node['surface_level']))


                # store node information for water level line
                if first:
                    self.profile_nodes.append({'distance': begin_dist,
                                               'id': begin_node_id})
                    first = False

                self.profile_nodes.append({'distance': end_dist,
                                           'id': end_node_id})

        if len(profile) > 0:
            ts_table = np.array(bottom_line, dtype=float)
            self.bottom_plot.setData(ts_table)

            ts_table = np.array(upper_line, dtype=float)
            self.upper_plot.setData(ts_table)

            ts_table = np.array(drain_level, dtype=float)
            self.drain_level_plot.setData(ts_table)

            ts_table = np.array(surface_level, dtype=float)
            self.surface_level_plot.setData(ts_table)

            # reset water level line
            ts_table = np.array(np.array([(0.0, 0.0)]), dtype=float)
            self.water_level_plot.setData(ts_table)

            self.autoRange()

            self.profile_route_updated.emit()
        else:
            # reset sideview
            ts_table = np.array(np.array([(0.0, 0.0)]), dtype=float)
            self.bottom_plot.setData(ts_table)
            self.upper_plot.setData(ts_table)
            self.drain_level_plot.setData(ts_table)
            self.surface_level_plot.setData(ts_table)
            self.water_level_plot.setData(ts_table)

            self.profile = []
            self.profile_nodes = []

    def update_water_level_cache(self):

        ds_item = self.time_slider.get_current_ts_datasource_item()
        if ds_item:
            ds = ds_item.datasource()
            for node in self.profile_nodes:
                ts = ds.get_timeseries('v2_connection_nodes', node['id'], ['s1'])
                node['timeseries'] = ts

            self.draw_waterlevel_line()

        else:
             # reset water level line
            ts_table = np.array(np.array([(0.0, 0.0)]), dtype=float)
            self.water_level_plot.setData(ts_table)

    def draw_waterlevel_line(self):

        timestamp_nr = self.time_slider.value()

        water_level_line = []
        for node in self.profile_nodes:
            water_level_line.append((node['distance'], node['timeseries'][timestamp_nr][1]))

        ts_table = np.array(water_level_line, dtype=float)
        self.water_level_plot.setData(ts_table)


    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """

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
        #Get the click
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

        transform = QgsCoordinateTransform(self.canvas.mapSettings().destinationCrs(),
                                           self.line_layer.crs())

        rect = transform.transform(rect)
        self.line_layer.removeSelection()

        # todo: select is not fastest way to get line
        self.line_layer.select(rect, False)
        selected = self.line_layer.selectedFeatures()

        if len(selected) > 0:
            # todo get point closest to selection point
            self.callback_on_select(selected)

    def activate(self):
        self.canvas.setCursor(QCursor(Qt.CrossCursor))

    def deactivate(self):
        self.canvas.setCursor(QCursor(Qt.ArrowCursor))

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return False


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
        self.select_sideview_button.clicked.connect(
                self.toggle_route_tool)

        # init class attributes
        self.route_tool_active = False

        # create point and line layer out of spatialite layers
        self.line_layer, self.point_dict = self.create_combined_layers(
                self.tdi_root_tool.ts_datasource.model_spatialite_filepath)

        self.sideviews = []
        widget = SideViewPlotWidget(self, 0, self.line_layer, self.point_dict, self.tdi_root_tool, "name")
        self.active_sideview = widget
        self.sideviews.append((0, widget))
        self.side_view_tab_widget.addTab(widget, widget.name)

        # init route graph
        director = QgsLineVectorLayerDirector(self.line_layer, -1, '', '', '', 3)

        self.route = Route(self.line_layer, director, id_field='nr')

        # link route map tool
        self.route_tool = RouteTool(self.iface.mapCanvas(),
                                    self.line_layer,
                                    self.on_route_point_select)

        # temp layer for side profile trac
        self.rb = QgsRubberBand(self.iface.mapCanvas())
        self.rb.setColor(Qt.red)
        self.rb.setWidth(4)

        # temp layer for last selected point
        self.point_markers = QgsVertexMarker(self.iface.mapCanvas())

        # add tree layer to map (for fun and testing purposes)
        self.vl_tree_layer = self.route.get_virtual_tree_layer()

        self.vl_tree_layer.loadNamedStyle(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), os.pardir,
                'layer_styles', 'tools', 'tree.qml'))

        QgsMapLayerRegistry.instance().addMapLayer(self.vl_tree_layer)

    def create_combined_layers(self, spatialite_path):

        def get_layer(spatialite_path, table_name, geom_column=''):
            uri2 = QgsDataSourceURI()
            uri2.setDatabase(spatialite_path)
            uri2.setDataSource('', table_name, geom_column)

            return QgsVectorLayer(uri2.uri(),
                                   table_name,
                                   'spatialite')
        # connection node layer
        profile_layer = get_layer(spatialite_path, 'v2_cross_section_definition')
        connection_node_layer = get_layer(spatialite_path, 'v2_connection_nodes', 'the_geom')
        manhole_layer = get_layer(spatialite_path, 'v2_manhole')
        boundary_layer = get_layer(spatialite_path, 'v2_1d_boundary_conditions')
        pipe_layer = get_layer(spatialite_path, 'v2_pipe')
        # channel_layer = get_layer(spatialite_path, 'v2_channel', 'the_geom')
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
            if profile['shape'] == 1:
                height = profile['height']
            elif profile['shape'] == 2:
                height = profile['width']
            else:
                height = 0.1

            profiles[profile['id']] = {
                'height': height,
                'rel_bottom_level': rel_bottom_level
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
            p['length'] = python_value(manhole['width'], 0)

        for bound in boundary_layer.getFeatures():
            p = points[bound['connection_node_id']]
            p['type'] = self.BOUNDARY

        for pipe in pipe_layer.getFeatures():
            # note: no support of calculation nodes on pipes
            profile = profiles[pipe['cross_section_definition_id']]
            pipe_def ={
                'id': 'pipe_' + str(pipe['id']),
                'type': 'pipe',
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

        # todo: channels - add cross sections and calc points to line, etc.

        # make point dict permanent
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
            QgsField("start_level", QVariant.Double),
            QgsField("end_level", QVariant.Double),
            QgsField("start_height", QVariant.Double),
            QgsField("end_height", QVariant.Double)
            ])
        vl.updateFields()  # tell the vector layer to fetch changes from the provider

        features = []
        i = 0
        for line in lines:
            feat = QgsFeature()

            # .asPoint make Qgis crash, try another way
            p1 = points[line['start_node']]['point']
            if python_value(line['end_node']) is not None:
                p2 = points[line['end_node']]['point']
            else:
                p2 = QgsPoint(p1.x(), p1.y()+0.0001)

            feat.setGeometry(QgsGeometry.fromPolyline([p1, p2]))

            feat.setAttributes([
                i,
                line["id"],
                line["type"],
                line["start_node"],
                line["end_node"],
                line["start_level"],
                line["end_level"],
                line["start_height"],
                line["end_height"]
            ])
            features.append(feat)
            i += 1

        pr.addFeatures(features)
        vl.updateExtents()

        QgsMapLayerRegistry.instance().addMapLayer(vl)

        return vl, points

    def toggle_route_tool(self):

        if self.route_tool_active:
            self.route_tool_active = False
            self.iface.mapCanvas().unsetMapTool(self.route_tool)
        else:
            self.route_tool_active = True
            self.iface.mapCanvas().setMapTool(self.route_tool)

    def on_route_point_select(self, selected_features):

        if self.route.has_path:
            self.route.reset()

        # Todo: improve this for better user experience. this is quiet random
        # better to take closest point
        next_point = QgsPoint(selected_features[0].geometry().vertexAt(0))

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


    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """
        self.select_sideview_button.clicked.disconnect(
                self.toggle_route_tool)

        if self.route_tool_active:
            self.iface.mapCanvas().unsetMapTool(self.route_tool)

        self.rb.reset()
        # todo: find out how to unload layer from memory
        QgsMapLayerRegistry.instance().removeMapLayer(self.vl_tree_layer)

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
