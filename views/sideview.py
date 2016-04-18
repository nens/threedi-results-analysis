# -*- coding: utf-8 -*-
from PyQt4.QtCore import Qt, QSize, QEvent, pyqtSignal, QMetaObject, QVariant
from PyQt4.QtGui import QTableView, QWidget, QVBoxLayout, QHBoxLayout, \
    QSizePolicy, QPushButton, QSpacerItem, QApplication, QTabWidget, \
    QDockWidget, QComboBox, QMessageBox, QColor, QCursor

import numpy as np
import os

from qgis.networkanalysis import QgsLineVectorLayerDirector, QgsGraphBuilder,\
        QgsDistanceArcProperter, QgsGraphAnalyzer

from qgis.core import QgsPoint, QgsRectangle, QgsCoordinateTransform, QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsMapLayerRegistry, QgsFeatureRequest
from qgis.networkanalysis import QgsArcProperter
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


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class SideViewPlotWidget(pg.PlotWidget):
    """Side view plot element"""

    def __init__(self, parent=None, nr=0, datasource_model=None, name=""):
        """

        :param parent: Qt parent widget
        """
        super(SideViewPlotWidget, self).__init__(parent)

        self.name = name
        self.nr = nr

        self.showGrid(True, True, 0.5)
        self.setLabel("bottom", "Afstand", "m")
        self.setLabel("left", "Hoogte", "mNAP")

        pen = pg.mkPen(color=QColor(256,0,0),
                           width=2)

        self.bottom_plot = pg.PlotDataItem(np.array([(0.0, 0.0)]), pen=pen)
        self.upper_plot = pg.PlotDataItem(np.array([(0.0, 0.0)]), pen=pen)

        self.addItem(self.bottom_plot)
        self.addItem(self.upper_plot)

    def set_sideprofile(self, profile, route_points):

        bottom_line = []
        upper_line = []

        for route_part in profile:
            for begin_dist, end_dist, distance, direction, feature in route_part:

                if direction == 1:
                    begin_level = feature['invert_level_start_point']
                    end_level = feature['invert_level_end_point']
                else:
                    begin_level = feature['invert_level_end_point']
                    end_level = feature['invert_level_start_point']

                bottom_line.append((float(begin_dist), float(begin_level)))
                bottom_line.append((float(end_dist), float(end_level)))

                shape = feature['sewerage_cross_section_definition_shape']
                if shape == 1:
                    height = feature['sewerage_cross_section_definition_height']
                elif shape == 2:
                    height = feature['sewerage_cross_section_definition_width']
                else:
                    # todo: get height of other shapes
                    height = 1

                upper_line.append((float(begin_dist), float(begin_level)+float(height)))
                upper_line.append((float(end_dist), float(end_level)+float(height)))

        ts_table = np.array(bottom_line, dtype=float)
        self.bottom_plot.setData(ts_table)

        ts_table = np.array(upper_line, dtype=float)
        self.upper_plot.setData(ts_table)
        self.autoRange()

    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """

        if self.ds_model:
            self.ds_model.dataChanged.disconnect(self.ds_data_changed)
            self.ds_model.rowsInserted.disconnect(self.on_insert_ds)
            self.ds_model.rowsAboutToBeRemoved.disconnect(self.on_remove_ds)
            self.ds_model = None

    def closeEvent(self, event):
        """
        overwrite of QDockWidget class to emit signal
        :param event: QEvent
        """
        self.on_close()
        event.accept()


class RouteTool(QgsMapTool):
    def __init__(self, canvas, point_layer, line_layer, callback_on_select):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.layer = point_layer
        self.line_layer = line_layer
        self.point_layer = point_layer
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
                                           self.layer.crs())

        rect = transform.transform(rect)

        self.layer.removeSelection()
        self.layer.select(rect, False)

        selected = self.layer.selectedFeatures()

        if len(selected) > 0:
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

    # todo:s
    # toon vlaggetje bij geselecteerde punten
    # meer punten achter elkaar selecteerbaar
    # punten verplaatsen
    # als op lijn wordt gedrukt en vastgehouden
    # op leidingen kunnen drukken in plaats van alleen op putten
    # detecteer dichtsbijzijnde punt in plaats van willekeurige binnen gebied
    # toon op basis van eerst geselecteerde punt de mogelijke andere punten

    # let op CRS van vreschillende lagen en CRS changes


    closingWidget = pyqtSignal(int)

    def __init__(self, iface, parent_widget=None,
                 parent_class=None, nr=0, ts_datasource=None):
        """Constructor"""
        super(SideViewDockWidget, self).__init__(parent_widget)

        self.iface = iface
        self.parent_class = parent_class
        self.nr = nr
        self.ts_datasource = ts_datasource

        # setup ui
        self.setup_ui(self)

        self.sideviews = []
        widget = SideViewPlotWidget(self, 0, self.ts_datasource, "name")
        self.active_sideview = widget
        self.sideviews.append((0, widget))
        self.side_view_tab_widget.addTab(widget, widget.name)

        # add listeners
        self.select_sideview_button.clicked.connect(
                self.toggle_route_tool)

        # init class attributes
        self.sideviews = []
        self.route_tool_active = False

        # find layers
        self.line_layer = None
        self.point_layer = None

        for layer in self.iface.legendInterface().layers():
            if layer.name() == 'sewerage_pipe_view':
                self.line_layer = layer
            elif layer.name() == 'sewerage_manhole':
                self.point_layer = layer

        if self.line_layer is None or self.point_layer is None:
            print("no layer found for graph")
            return

        # init route graph
        director = QgsLineVectorLayerDirector(self.line_layer, -1, '', '', '', 3)
        self.route = Route(self.line_layer, director)

        # link route map tool
        self.route_tool = RouteTool(self.iface.mapCanvas(),
                                    self.point_layer,
                                    self.line_layer,
                                    self.on_route_point_select)

        # temp layer for sideprofile trac
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

        # else
        next_point = QgsPoint(selected_features[0].geometry().asPoint())

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
