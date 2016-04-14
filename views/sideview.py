# -*- coding: utf-8 -*-
from PyQt4.QtCore import Qt, QSize, QEvent, pyqtSignal, QMetaObject
from PyQt4.QtGui import QTableView, QWidget, QVBoxLayout, QHBoxLayout, \
    QSizePolicy, QPushButton, QSpacerItem, QApplication, QTabWidget, \
    QDockWidget, QComboBox, QMessageBox

from qgis.networkanalysis import QgsLineVectorLayerDirector, QgsGraphBuilder,\
        QgsDistanceArcProperter, QgsGraphAnalyzer

from qgis.core import QgsPoint, QgsRectangle
from qgis.gui import QgsRubberBand, QgsVertexMarker, QgsMapTool

from ..datasource.spatialite import get_object_type, layer_qh_type_mapping
from ..models.graph import LocationTimeseriesModel
from ..utils.user_messages import log, statusbar_message



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


class SideViewWidget(pg.PlotWidget):
    """Side view plot element"""

    def __init__(self, parent=None, nr=0, datasource_model=None, name=""):
        """

        :param parent: Qt parent widget
        """
        super(SideViewWidget, self).__init__(parent)

        self.name = name
        self.nr = nr

        self.showGrid(True, True, 0.5)
        self.setLabel("bottom", "Afstand", "m")
        self.setLabel("left", "Hoogte", "mNAP")

        self.ds_model = datasource_model

        self.ds_model.dataChanged.connect(self.ds_data_changed)
        self.ds_model.rowsInserted.connect(self.on_insert_ds)
        self.ds_model.rowsAboutToBeRemoved.connect(self.on_remove_ds)

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

    def on_insert_ds(self, parent, start, end):
        """
        add list of items to graph. based on Qt addRows model trigger
        :param parent: parent of event (Qt parameter)
        :param start: first row nr
        :param end: last row nr
        """
        for i in range(start, end+1):
            ds = self.ds_model.rows[i]
            if ds.active.value:
                # todo: do something
                pass

    def on_remove_ds(self, index, start, end):
        """
        remove items from graph. based on Qt model removeRows
        trigger
        :param index: Qt Index (not used)
        :param start: first row nr
        :param end: last row nr
        """
        for i in range(start, end+1):
            ds = self.ds_model.rows[i]
            if ds.active.value:
                # todo: do something
                pass

    def ds_data_changed(self, index):
        """
        change graphs based on changes in locations. based on Qt
        data change trigger
        :param index: index of changed field
        """
        if self.ds_model.columns[index.column()].name == 'active':
            # todo: do something
            pass

class RouteTool(QgsMapTool):
    def __init__(self, canvas, layer, callback_on_select):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.layer = layer
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
        self.layer.removeSelection()
        self.layer.select(rect, False)

        selected = self.layer.selectedFeatures()

        if len(selected) > 0:
            self.callback_on_select(selected)

    def activate(self):
        pass

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return False




class SideViewDockWidget(QDockWidget):
    """Main Dock Widget for showing 3di results in Graphs"""

    closingWidget = pyqtSignal(int)

    def __init__(self, iface, parent_widget=None,
                 parent_class=None, nr=0, ts_datasource=None):
        """Constructor"""
        super(SideViewDockWidget, self).__init__(parent_widget)

        self.iface = iface
        self.parent_class = parent_class
        self.nr = nr
        self.ts_datasource = ts_datasource

        self.setup_ui(self)

        # add listeners
        self.select_sideview_button.clicked.connect(
                self.toggle_route_tool)

        self.sideviews = []

        # add graph widgets
        widget = SideViewWidget(self, 0, self.ts_datasource, "name")

        self.active_sideview = widget
        self.sideviews.append((0, widget))

        self.side_view_tab_widget.addTab(widget, widget.name)

        # init graph
        line_layer = None
        point_layer = None

        for layer in self.iface.legendInterface().layers():
            if layer.name() == 'sewerage_pipe_view':
                line_layer = layer
            elif layer.name() == 'sewerage_manhole':
                point_layer = layer

        if line_layer is None or point_layer is None:
            print("no layer found for graph")
            return

        self.director = QgsLineVectorLayerDirector(line_layer,
                                                   -1, '', '', '', 3)

        properter = QgsDistanceArcProperter()
        self.director.addProperter(properter)
        crs = layer.self.iface.mapCanvas().mapRenderer().destinationCrs()
        self.builder = QgsGraphBuilder(crs)

        points = []
        for feature in point_layer.getFeatures():
            points.append(QgsPoint(feature.geometry().asPoint()))

        self.tied_points = self.director.makeGraph(self.builder, points)
        self.graph = self.builder.graph()

        # temp layer for lines
        self.rb = QgsRubberBand(self.iface.mapCanvas())
        self.rb.setColor(Qt.red)

        # temp layer for points
        #self.point_markers = QgsVertexMarker(self.iface.mapCanvas())

        self.id_start = None
        self.id_end = None
        self.start_point = None

        self.point_layer = point_layer
        self.route_tool = RouteTool(self.iface.mapCanvas(),
                                    self.point_layer,
                                    self.on_route_point_select)

        self.route_tool_active = False
        self.path_found = False

    def toggle_route_tool(self):

        if self.route_tool_active:
            self.route_tool_active = False
            self.iface.mapCanvas().unsetMapTool(self.route_tool)
        else:
            self.route_tool_active = True
            self.iface.mapCanvas().setMapTool(self.route_tool)

    def on_route_point_select(self, selected_features):
        # selecteer 1 punt --> toon vlaggetje
        # selecteer 2e punt --> toon vlaggetje
        # als control ingedrukt, verleng lijn
        # als op lijn wordt gedrukt en vastgehouden --> voeg tussenpunt toe
        # toon op basis van eerst geselecteerde punt de mogelijke andere punten

        # let op CRS van vreschillende lagen en CRS changes

        # detect nearby point on map click

        if self.path_found:
            # reset for now
            self.path_found = False
            self.id_start = None
            self.start_point = None
            self.id_end = None

        if self.start_point is None or self.id_start < 0:

            self.on_select_first_route_point(selected_features[0])
            return

        end_point = QgsPoint(selected_features[0].geometry().asPoint())

        self.id_end = self.graph.findVertex(end_point)

        if self.tree[self.id_end] == -1:
             print("Path not found")
        else:
            self.path_found = True
            p = []
            curPos = self.id_end
            while curPos != self.id_start:
                p.append(self.graph.vertex(
                        self.graph.arc(self.tree[curPos]).inVertex()).point())
                curPos = self.graph.arc(self.tree[curPos]).outVertex()

            p.append(self.start_point)

            for pnt in p:
                self.rb.addPoint(pnt)

    def on_select_first_route_point(self, feature):

        self.rb.reset()

        self.start_point = QgsPoint(feature.geometry().asPoint())

        self.id_start = self.graph.findVertex(self.start_point)

        if self.id_start == -1:
             print("Path not found")
             return

        (self.tree, self.cost) = QgsGraphAnalyzer.dijkstra(self.graph,
                                                           self.id_start,
                                                           0)

        # for i in range(0, len(self.tree)):
        #     tp = self.tree[i]
        #     cp = self.cost[i]
        #     v = int(tp)
        #     if int(tp) > 0:
        #         self.point_markers.setCenter(self.tied_points[i])


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

    def closeEvent(self, event):
        """
        overwrite of QDockWidget class to emit signal
        :param event: QEvent
        """
        self.on_close()
        self.closingWidget.emit(self.nr)
        event.accept()

    def select_sideview_traject(self):
        """
        Activate tool for selecting of traject on map for sideview
        """

        canvas = self.iface.mapCanvas()
        current_layer = canvas.currentLayer()
        if not current_layer:
            #todo: feedback select layer first
            return

        provider = current_layer.dataProvider()
        if not provider.name() == 'spatialite':
            return

        if current_layer.name() not in layer_qh_type_mapping.keys():
            #todo: feedback layer not supported
            return

        selected_features = current_layer.selectedFeatures()


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
