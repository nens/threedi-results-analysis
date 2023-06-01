from collections import OrderedDict
from random import randint
from threedi_results_analysis.models.base import BaseModel
from threedi_results_analysis.models.base_fields import CheckboxField, CHECKBOX_FIELD
from threedi_results_analysis.models.base_fields import ColorField
from threedi_results_analysis.models.base_fields import ValueField
from typing import Dict

import logging
import numpy as np
import pyqtgraph as pg
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor


logger = logging.getLogger(__name__)


COLOR_LIST = [
    (34, 34, 34),
    (243, 195, 0),
    (135, 86, 146),
    (243, 132, 0),
    (161, 202, 241),
    (190, 0, 50),
    (194, 178, 128),
    (132, 132, 130),
    (0, 136, 86),
    (230, 143, 172),
    (0, 103, 165),
    (249, 147, 121),
    (96, 78, 151),
    (246, 166, 0),
    (179, 68, 108),
    (220, 211, 0),
    (136, 45, 23),
    (141, 182, 0),
    (101, 69, 34),
    (226, 88, 34),
    (43, 61, 38),
]

EMPTY_TIMESERIES = np.array([], dtype=float)


def select_default_color(item_field):
    """
    return color for lines
    :param item_field: ItemField object
    :return: tuple with the 3 color bands (values between 0-256)
    """

    model = item_field.row.model
    colors = OrderedDict([(str(color), color) for color in COLOR_LIST])

    for item in model.rows:
        if str(item.color.value) in colors:
            del colors[str(item.color.value)]

    if len(colors) >= 1:
        return list(colors.values())[0]

    # predefined colors are all used, return random color
    return (randint(0, 256), randint(0, 256), randint(0, 256))


class LocationTimeseriesModel(BaseModel):
    """Model implementation for (selected objects) for display in graph"""

    feature_color_map: Dict[int, int] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataChanged.connect(self.update_labels)

    def update_labels(self, index):
        if self.columns[index.column()].name == "object_label":
            # Update user-editable label of other plots for same feature
            updated_item = self.rows[index.row()]
            updated_feature_id = updated_item.object_id.value
            updated_grid = updated_item.result.value.parent()
            updated_object_type = updated_item.object_type.value
            assert updated_grid
            new_label = updated_item.object_label.value
            for item in self.rows:
                if (item.object_id.value == updated_feature_id and
                        item.result.value.parent() is updated_grid and
                        item.object_type.value == updated_object_type):  # e.g. flowline
                    self.blockSignals(True)
                    item.object_label.value = new_label
                    self.blockSignals(False)

    def get_color(self, idx: int) -> QColor:
        if not self.feature_color_map:
            self.feature_color_map[idx] = 0
        elif idx not in self.feature_color_map:
            # pick next color from COLOR_LIST
            self.feature_color_map[idx] = ((max(self.feature_color_map.values())+1) % len(COLOR_LIST))

        return COLOR_LIST[self.feature_color_map[idx]]

    def flags(self, index):

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if self.columns[index.column()].field_type == CHECKBOX_FIELD:
            flags |= Qt.ItemIsUserCheckable | Qt.ItemIsEditable
        elif index.column() == 5:  # user-defined label
            flags |= Qt.ItemIsEditable

        return flags

    def data(self, index, role=Qt.DisplayRole):
        """Qt function to get data from items for the visible columns"""

        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            if index.column() == 2:  # grid: take name from result parent
                return self.rows[index.row()][index.column()+1].value.parent().text()
            elif index.column() == 3:  # result
                return self.rows[index.row()][index.column()].value.text()

        return super().data(index, role)

    class Fields(object):
        """Fields and functions of ModelItem"""

        active = CheckboxField(
            show=True, default_value=True, column_width=20, column_name="active"
        )
        color = ColorField(
            show=True,
            column_width=30,
            column_name="color"
        )

        grid_name = ValueField(show=True, column_width=100, column_name="grid", default_value="grid")
        result = ValueField(show=True, column_width=100, column_name="result")
        object_id = ValueField(show=True, column_width=50, column_name="id")
        object_label = ValueField(show=True, column_width=100, column_name="label")  # user-defined label per feature
        object_name = ValueField(show=True, column_width=50, column_name="type")  # e.g. 2D-1D
        object_type = ValueField(show=False)  # e.g. flowline
        hover = ValueField(show=False, default_value=False)

        _plots = {}

        def plots(self, parameters, absolute, time_units):
            """
            Get pyqtgraph plot of selected object and timeseries.

            Performs some caching on key: "result_uuid, feature_id, layer_name (pump, flowlines), time-unit, absolute"
            :param parameters: string, parameter identification
            :param result_ds_nr: nr of result ts_datasources in model
            :return: pyqtgraph PlotDataItem
            """
            # Key is result uuid, feature id, layer name (pump, flowlines), time-unit, absolute
            result_key = (self.result.value.id, str(self.object_id.value), self.object_type.value, time_units, absolute)
            if not str(parameters) in self._plots:
                self._plots[str(parameters)] = {}
            if result_key not in self._plots[str(parameters)]:
                ts_table = self.timeseries_table(
                    parameters=parameters, absolute=absolute, time_units=time_units,
                )

                pen = pg.mkPen(color=self.color.value, width=2, style=self.result.value._pattern)

                logger.info(f"Creating plot item for {result_key}: {parameters}")
                self._plots[str(parameters)][result_key] = pg.PlotDataItem(ts_table, pen=pen)

            # logger.info(f"Retrieving plot for {result_key}: {parameters}")
            return self._plots[str(parameters)][result_key]

        def timeseries_table(self, parameters, absolute, time_units):
            """
            get list of timestamp values for object and parameters
            from result ts_datasources
            :param parameters:
            :param result_ds_nr:
            :return: numpy array with timestamp, values
            """
            threedi_result = self.result.value.threedi_result

            if (parameters not in threedi_result.available_subgrid_map_vars and
                    parameters not in threedi_result.available_aggregation_vars):
                logger.warning(f"Parameter {parameters} not available in result {self.result.value.text()}")
                return EMPTY_TIMESERIES

            ga = threedi_result.get_gridadmin(parameters)
            if ga.has_pumpstations:
                pump_fields = set(list(ga.pumps.Meta.composite_fields.keys()))
            else:
                pump_fields = {}
            if self.object_type.value == "pump_linestring" and parameters not in pump_fields:
                return EMPTY_TIMESERIES
            if self.object_type.value == "flowline" and parameters in pump_fields:
                return EMPTY_TIMESERIES

            timeseries = threedi_result.get_timeseries(
                parameters, node_id=self.object_id.value, fill_value=np.NaN
            )
            if timeseries.shape[1] == 1:
                logger.info("1-element timeserie, plotting empty serie")
                return EMPTY_TIMESERIES
            if absolute:
                timeseries = np.abs(timeseries)
            if time_units == "hrs":
                vector = np.array([3600, 1])
            elif time_units == "mins":
                vector = np.array([60, 1])
            else:
                vector = np.array([1, 1])
            return timeseries / vector
