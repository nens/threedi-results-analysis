from PyQt4.QtCore import Qt, QSize, QEvent, QModelIndex, QPersistentModelIndex,\
    pyqtSignal, QMetaObject
from PyQt4.QtGui import QTableView, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QColor, QPushButton, QSpacerItem,\
    QApplication, QWidget, QGridLayout, QVBoxLayout, QTabWidget, QDockWidget, QComboBox

from ..datasource.spatialite import get_object_type, get_available_parameters, layer_qh_type_mapping, \
    parameter_config
from ..models.graph import LocationTimeseriesModel
from ..utils.user_messages import log

import pyqtgraph as pg
from qgis.core import QgsDataSourceURI


pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class GraphPlot(pg.PlotWidget):

    def __init__(self, parent=None):

        super(GraphPlot, self).__init__(parent)

        self.showGrid(True, True, 0.5)
        self.setLabel("bottom", "Tijd", "s")

        self.current_parameter = None

    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """
        if self.model:
            self.model.dataChanged.disconnect(self.data_changed)
            self.model.rowsInserted.disconnect(self.insert_plot)
            self.model.rowsAboutToBeRemoved.disconnect(self.remove_plot)
            self.model = None


    def closeEvent(self, event):
        """
        overwrite of QDockWidget class to emit signal
        :param event: QEvent
        """
        self.on_close()
        event.accept()

    def setModel(self, model):

        self.model = model
        self.model.dataChanged.connect(self.data_changed)
        self.model.rowsInserted.connect(self.insert_plot)
        self.model.rowsAboutToBeRemoved.connect(self.remove_plot)

    def insert_plot(self, parent, start, end):
        """
        add list of items of model from plot. based on Qt addRows model trigger
        :param parent: parent of event (Qt parameter)
        :param start: first row nr
        :param end: last row nr
        """
        for i in range(start, end+1):
            item = self.model.rows[i]
            self.addItem(item.plots(self.current_parameter['parameters']))

    def remove_plot(self, index, start, end):
        """
        remove list of items of model from plot. based on Qt model removeRows trigger
        :param index: Qt Index (not used)
        :param start: first row nr
        :param end: last row nr
        """
        for i in range(start, end+1):
            item = self.model.rows[i]
            if item.active.value:
                self.removeItem(item.plots(self.current_parameter['parameters']))

    def data_changed(self, index):

        if self.model.columns[index.column()].name == 'active':
            active = self.model.rows[index.row()].active.value

            if active:
                self.show_timeseries(index.row())
            else:
                self.hide_timeseries(index.row())
        elif self.model.columns[index.column()].name == 'hover':
            item = self.model.rows[index.row()]
            if item.hover.value:
                item.plots(self.current_parameter['parameters']).setPen(color=item.color.qvalue, width=4)
            else:
                item.plots(self.current_parameter['parameters']).setPen(color=item.color.qvalue, width=2)

    def hide_timeseries(self, row_nr):

        plot = self.model.rows[row_nr].plots(self.current_parameter['parameters'])
        self.removeItem(plot)

    def show_timeseries(self, row_nr):

        plot = self.model.rows[row_nr].plots(self.current_parameter['parameters'])
        self.addItem(plot)

    def set_parameter(self, parameter):

        if self.current_parameter == parameter:
            return

        old_parameter = self.current_parameter
        self.current_parameter = parameter

        for item in self.model.rows:
            if item.active.value:
                self.removeItem(item.plots(old_parameter['parameters']))
                self.addItem(item.plots(self.current_parameter['parameters']))

        self.setLabel("left", self.current_parameter['name'], self.current_parameter['unit'])


class LocationTimeseriesTable(QTableView):

    hoverExitRow = pyqtSignal(int)
    hoverEnterRow = pyqtSignal(int)

    def __init__(self, parent=None):
        super(LocationTimeseriesTable, self).__init__(parent)
        self.setStyleSheet("QTreeView::item:hover{background-color:#FFFF00;}")
        self.setMouseTracking(True)
        self.model = None
        # self.entered.connect(self.hover_row)

        self._last_hovered_row = None
        self.viewport().installEventFilter(self)

    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """
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
            else:
                row = self._last_hovered_row

            if row != self._last_hovered_row:
                if self._last_hovered_row is not None:
                    try:
                        self.hover_exit(self._last_hovered_row)
                    except IndexError:
                        log("Hover row index %s out of range" %
                            self._last_hovered_row, level='WARNING')
                    #self.hoverExitRow.emit(self._last_hovered_row)
                #self.hoverEnteredRow.emit(index.row())
                if row is not None:
                    try:
                        self.hover_enter(row)
                    except:
                        log("Hover row index %s out of range" % row,
                            level='WARNING')
                self._last_hovered_row = row
                pass
        return QTableView.eventFilter(self, widget, event)

    def hover_exit(self, row_nr):

        if row_nr >= 0:
            item = self.model.rows[row_nr]
            item.hover.value = False

    def hover_enter(self, row_nr):

        if row_nr >= 0:
            item = self.model.rows[row_nr]
            item.hover.value = True

    def setModel(self, model):
        super(LocationTimeseriesTable, self).setModel(model)

        self.model = model

        self.resizeColumnsToContents()
        for col_nr in range(0, model.columnCount()):
            width = model.columns[col_nr].column_width
            if width:
                self.setColumnWidth(col_nr, width)
            if not model.columns[col_nr].show:
                self.setColumnHidden(col_nr, True);

    def hover_row(self, index):
        pass
        #log("row %i, col %i"%(index.row(), index.column()))
        # if index.row() != self.row_hovered:
        #     if self.row_hovered is not None:
        #         self.model.setData()
        #     self.row_hovered = index.row()
        #     self.model.setData()

class GraphWidget(QWidget):

    def __init__(self, parent=None, ts_datasource=None, parameter_config=[], name=""):
        super(GraphWidget, self).__init__(None)

        self.name = name
        self.parameters = dict([(p['name'], p) for p in parameter_config])
        self.ts_datasource = ts_datasource
        self.parent = parent

        self.setup_ui()

        self.model = LocationTimeseriesModel(datasource=self.ts_datasource)
        self.graph_plot.setModel(self.model)
        self.location_timeseries_table.setModel(self.model)

        # init parameter selection
        for pc in self.parameters.keys():
            self.parameter_combo_box.addItem(pc)
        self.parameter_combo_box.setCurrentIndex(1)
        self.current_parameter = self.parameters[self.parameter_combo_box.currentText()]
        self.graph_plot.set_parameter(self.current_parameter)

        # set listeners
        self.parameter_combo_box.currentIndexChanged.connect(self.parameter_change)
        self.remove_timeseries_button.clicked.connect(self.remove_objects_table)

    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """
        self.parameter_combo_box.currentIndexChanged.disconnect(self.parameter_change)
        self.remove_timeseries_button.clicked.disconnect(self.remove_objects_table)

    def closeEvent(self, event):
        """
        overwrite of QDockWidget class to emit signal
        :param event: QEvent
        """
        self.on_close()
        event.accept()

    def setup_ui(self):
        """
        Create Qt widgets and elements
        """

        self.setObjectName(self.name)

        self.hLayout = QHBoxLayout(self)
        self.hLayout.setObjectName("hLayout")

        # add graphplot
        self.graph_plot = GraphPlot(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.graph_plot.sizePolicy().hasHeightForWidth())
        self.graph_plot.setSizePolicy(sizePolicy)
        self.graph_plot.setMinimumSize(QSize(250, 250))
        self.hLayout.addWidget(self.graph_plot)

        # add layout for timeseries table and other controls
        self.vLayoutTable = QVBoxLayout(self)
        self.hLayout.addLayout(self.vLayoutTable)

        # add combobox for parameter selection
        self.parameter_combo_box = QComboBox(self)
        self.vLayoutTable.addWidget(self.parameter_combo_box)

        # add timeseries table
        self.location_timeseries_table = LocationTimeseriesTable(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.location_timeseries_table.sizePolicy().hasHeightForWidth())
        self.location_timeseries_table.setSizePolicy(sizePolicy)
        self.location_timeseries_table.setMinimumSize(QSize(250, 0))
        self.vLayoutTable.addWidget(self.location_timeseries_table)

        # add buttons below table
        self.hLayoutButtons = QHBoxLayout(self)
        self.vLayoutTable.addLayout(self.hLayoutButtons)

        self.remove_timeseries_button = QPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_timeseries_button.sizePolicy().hasHeightForWidth())
        self.remove_timeseries_button.setSizePolicy(sizePolicy)
        self.remove_timeseries_button.setObjectName("remove_timeseries_button")
        self.hLayoutButtons.addWidget(self.remove_timeseries_button)
        self.hLayoutButtons.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.retranslateUi()

    def retranslateUi(self):
        """
        set translated widget text
        """
        self.remove_timeseries_button.setText(_translate("DockWidget", "Verwijder", None))

    def parameter_change(self, nr):
        """
        set current selected parameter and trigger refresh of graphs
        :param nr: nr of selected option of combobox
        :return:
        """
        self.current_parameter = self.parameters[self.parameter_combo_box.currentText()]
        self.graph_plot.set_parameter(self.current_parameter)

        #todo: trigger refresh of graphs

    def add_objects(self, layer, features):
        """

        :param layer: layer of features
        :param features: Qgis layer features to be added
        """

        # Get the active database as URI, connInfo is something like:
        # u"dbname='/home/jackieleng/git/threedi-turtle/var/models/
        # DS_152_1D_totaal_bergingsbak/results/
        # DS_152_1D_totaal_bergingsbak_result.sqlite'"
        connInfo = QgsDataSourceURI(
            layer.dataProvider().dataSourceUri()).connectionInfo()
        filename = connInfo.split("'")[1]

        # get attribute information from selected layers
        items = []
        for feature in features:
            item = {
                'object_type': layer.name(),
                'object_id': feature['id'],
                'object_name': feature['display_name'],
                'file_path': filename
            }
            items.append(item)

        self.model.insertRows(items)

    def remove_objects_table(self):
        """
        removes selected objects from table
        :return:
        """
        selection_model = self.location_timeseries_table.selectionModel()
        #get unique rows in selected fields
        rows = set([index.row() for index in selection_model.selectedIndexes()])
        for row in reversed(sorted(rows)):
            self.model.removeRows(row,1)


class GraphDockWidget(QDockWidget):
    """Main Dock Widget for showing 3di results in Graphs"""

    closingWidget = pyqtSignal(int)

    def __init__(self, iface, parent_widget=None, parent_class=None, nr=0, ts_datasource=None):
        """Constructor"""
        super(GraphDockWidget, self).__init__(parent_widget)

        self.iface = iface
        self.parent_class = parent_class
        self.nr = nr
        self.ts_datasource = ts_datasource

        self.setup_ui(self)

        # add listeners
        self.addSelectedObjectButton.clicked.connect(self.add_objects)
        # init current layer state and add listener
        self.selected_layer_changed(self.iface.mapCanvas().currentLayer)
        self.iface.currentLayerChanged.connect(self.selected_layer_changed)

        # add graph widgets
        self.q_graph_widget = GraphWidget(self, self.ts_datasource, parameter_config['q'], "Q graph")
        self.h_graph_widget = GraphWidget(self, self.ts_datasource, parameter_config['h'], "H graph")
        self.graphTabWidget.addTab(self.q_graph_widget, self.q_graph_widget.name)
        self.graphTabWidget.addTab(self.h_graph_widget, self.h_graph_widget.name)

    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """
        self.addSelectedObjectButton.clicked.disconnect(self.add_objects)
        self.iface.currentLayerChanged.disconnect(self.selected_layer_changed)

        #self.q_graph_widget.close()
        #self.h_graph_widget.close()

    def closeEvent(self, event):
        """
        overwrite of QDockWidget class to emit signal
        :param event: QEvent
        """
        self.on_close()
        self.closingWidget.emit(self.nr)
        event.accept()

    def selected_layer_changed(self, active_layer):

        tdi_layer = False

        #get active layer from canvas, otherwise .dataProvider doesn't work
        canvas = self.iface.mapCanvas()
        current_layer = canvas.currentLayer()

        if current_layer:
            provider = current_layer.dataProvider()
            valid_object_type = get_object_type(current_layer.name())

            if provider.name() == 'spatialite' and valid_object_type:
                tdi_layer = True

        #activate button if 3di layers found
        self.addSelectedObjectButton.setEnabled(tdi_layer)

    def add_objects(self):

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

        if layer_qh_type_mapping[current_layer.name()] == 'q':
            self.q_graph_widget.add_objects(current_layer, selected_features)
            self.graphTabWidget.setCurrentIndex(self.graphTabWidget.indexOf(self.q_graph_widget))
        else:
            self.h_graph_widget.add_objects(current_layer, selected_features)
            self.graphTabWidget.setCurrentIndex(self.graphTabWidget.indexOf(self.h_graph_widget))

    def setup_ui(self, dock_widget):
        """
        initiate main Qt building blocks of interface
        :param dock_widget: QDockWidget instance
        """

        dock_widget.setObjectName("dock_widget")

        self.dockWidgetContent = QWidget()
        self.dockWidgetContent.setObjectName("dockWidgetContent")

        self.mainVLayout = QVBoxLayout(self.dockWidgetContent)
        self.dockWidgetContent.setLayout(self.mainVLayout)

        # add button to add objects to graphs
        self.buttonBarHLayout = QHBoxLayout()
        self.addSelectedObjectButton = QPushButton(self.dockWidgetContent)
        self.addSelectedObjectButton.setObjectName("addSelectedObjectButton")
        self.buttonBarHLayout.addWidget(self.addSelectedObjectButton)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.buttonBarHLayout.addItem(spacerItem)
        self.mainVLayout.addItem(self.buttonBarHLayout)

        # add tabWidget for graphWidgets
        self.graphTabWidget = QTabWidget(self.dockWidgetContent)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(6)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphTabWidget.sizePolicy().hasHeightForWidth())
        self.graphTabWidget.setSizePolicy(sizePolicy)
        self.graphTabWidget.setObjectName("graphTabWidget")
        self.mainVLayout.addWidget(self.graphTabWidget)

        # add dockwidget
        dock_widget.setWidget(self.dockWidgetContent)
        self.retranslate_ui(dock_widget)
        QMetaObject.connectSlotsByName(dock_widget)

    def retranslate_ui(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "3di resultaat grafieken %i" % self.nr, None))
        self.addSelectedObjectButton.setText(_translate("DockWidget", "Voeg toe", None))



