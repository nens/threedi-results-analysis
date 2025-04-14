import pyqtgraph as pg


pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")
from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel


class FractionPlot(pg.PlotWidget):
    """Graph element"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.showGrid(True, True, 0.5)
        self.current_parameter = None
        self.fraction_model = None
        self.result_model = None
        self.parent = parent
        self.current_time_units = "hrs"
        self.setLabel("bottom", "Time", self.current_time_units)
        # Auto SI prefix scaling doesn't work properly with m3, m2 etc.
        self.getAxis("left").enableAutoSIPrefix(False)

    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """
        if self.fraction_model:
            self.fraction_model.dataChanged.disconnect(self.fraction_data_changed)
            self.fraction_model.rowsInserted.disconnect(self.on_insert_fractions)
            self.fraction_model.rowsAboutToBeRemoved.disconnect(
                self.on_remove_fractions
            )
            self.fraction_model = None

    def closeEvent(self, event):
        """
        overwrite of QDockWidget class to emit signal
        :param event: QEvent
        """
        self.on_close()
        event.accept()

    def set_fraction_model(self, model):
        self.fraction_model = model
        self.fraction_model.dataChanged.connect(self.fraction_data_changed)
        self.fraction_model.rowsInserted.connect(self.on_insert_fractions)
        self.fraction_model.rowsAboutToBeRemoved.connect(self.on_remove_fractions)

    def set_result_model(self, model: ThreeDiPluginModel):
        self.result_model = model

    def on_insert_fractions(self, parent, start, end):
        """
        add list of items to graph. based on Qt addRows model trigger
        :param parent: parent of event (Qt parameter)
        :param start: first row nr
        :param end: last row nr
        """
        for i in range(start, end + 1):
            item = self.fraction_model.rows[i]
            self.addItem(
                item.plots(
                    self.current_parameter["parameters"],
                    time_units=self.current_time_units,
                )
            )

    def on_remove_fractions(self, index, start, end):
        """
        remove items from graph. based on Qt model removeRows
        trigger
        :param index: Qt Index (not used)
        :param start: first row nr
        :param end: last row nr
        """
        for i in range(start, end + 1):
            item = self.fraction_model.rows[i]
            self.removeItem(
                        item.plots(self.current_parameter["parameters"], time_units=self.current_time_units)
                    )

        self.plotItem.vb.menu.viewAll.triggered.emit()

    def fraction_data_changed(self, index):
        """
        change graphs
        :param index: index of changed field
        """
        item = self.fraction_model.rows[index.row()]

        if self.fraction_model.columns[index.column()].name == "active":
            if item.active.value:
                self.show_timeseries(index.row())
            else:
                self.hide_timeseries(index.row())

        elif self.fraction_model.columns[index.column()].name == "hover":
            width = 2
            if item.hover.value:
                width = 5
            item.plots(self.current_parameter["parameters"], time_units=self.current_time_units).setPen(
                color=item.color.qvalue, width=width, style=item.result.value._pattern)

        elif self.fraction_model.columns[index.column()].name == "color":
            item.plots(self.current_parameter["parameters"], time_units=self.current_time_units).setPen(
                color=item.color.qvalue, width=2, style=item.result.value._pattern)

    def hide_timeseries(self, location_nr):
        """
        hide timeseries of location in graph
        :param row_nr: integer, row number of location
        """

        plot = self.fraction_model.rows[location_nr].plots(
            self.current_parameter["parameters"], time_units=self.current_time_units)
        self.removeItem(plot)

    def show_timeseries(self, location_nr):
        """
        show timeseries of location in graph
        :param row_nr: integer, row number of location
        """

        plot = self.fraction_model.rows[location_nr].plots(
            self.current_parameter["parameters"], time_units=self.current_time_units)
        self.addItem(plot)

    def set_parameter(self, parameter, time_units):
        """
        on selection of parameter (in combobox), change timeseries in graphs
        :param parameter: parameter identification string
        :param time_units: current time units string
        """

        if self.current_parameter == parameter and self.current_time_units == time_units:
            return

        old_parameter = self.current_parameter
        old_time_units = self.current_time_units
        self.current_parameter = parameter
        self.current_time_units = time_units

        for item in self.fraction_model.rows:
            if not item.active.value:
                continue

            self.removeItem(
                item.plots(old_parameter["parameters"], time_units=old_time_units)
            )
            self.addItem(
                item.plots(self.current_parameter["parameters"], time_units=self.current_time_units)
            )

        self.setLabel(
            "left", self.current_parameter["name"], self.current_parameter["unit"]
        )