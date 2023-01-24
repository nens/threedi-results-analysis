from collections import OrderedDict
from random import randint
from ThreeDiToolbox.models.base import BaseModel
from ThreeDiToolbox.models.base_fields import CheckboxField
from ThreeDiToolbox.models.base_fields import ColorField
from ThreeDiToolbox.models.base_fields import ValueField

import logging
import numpy as np
import pyqtgraph as pg


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

    class Fields(object):
        """Fields and functions of ModelItem"""

        active = CheckboxField(
            show=True, default_value=True, column_width=20, column_name="active"
        )
        color = ColorField(
            show=True,
            column_width=30,
            column_name="color",
            default_value=select_default_color,
        )

        grid_name = ValueField(show=True, column_width=100, column_name="grid", default_value="grid")
        result_name = ValueField(show=True, column_width=100, column_name="result", default_value="result")
        object_id = ValueField(show=True, column_width=50, column_name="id")
        object_name = ValueField(show=True, column_width=140, column_name="name")
        object_type = ValueField(show=False)
        hover = ValueField(show=False, default_value=False)

        _plots = {}

        def plots(self, parameters, result_item, absolute, time_units):
            """
            Get pyqtgraph plot of selected object and timeseries. Performs some caching.
            :param parameters: string, parameter identification
            :param result_ds_nr: nr of result ts_datasources in model
            :return: pyqtgraph PlotDataItem
            """
            # TODO: the result_item.text() can change
            result_key = (result_item.text(), time_units)
            if not str(parameters) in self._plots:
                self._plots[str(parameters)] = {}
            if result_key not in self._plots[str(parameters)]:
                ts_table = self.timeseries_table(
                    parameters=parameters, result_item=result_item, absolute=absolute, time_units=time_units,
                )

                pen = pg.mkPen(color=self.color.qvalue, width=2, style=result_item._pattern)
                self._plots[str(parameters)][result_key] = pg.PlotDataItem(
                    ts_table, pen=pen
                )

            return self._plots[str(parameters)][result_key]

        def timeseries_table(self, parameters, result_item, absolute, time_units):
            """
            get list of timestamp values for object and parameters
            from result ts_datasources
            :param parameters:
            :param result_ds_nr:
            :return: numpy array with timestamp, values
            """
            threedi_result = result_item.threedi_result

            ga = threedi_result.get_gridadmin(parameters)
            if ga.has_pumpstations:
                pump_fields = set(list(ga.pumps.Meta.composite_fields.keys()))
            else:
                pump_fields = {}
            if self.object_type.value == "pumplines" and parameters not in pump_fields:
                return EMPTY_TIMESERIES
            if self.object_type.value == "flowlines" and parameters in pump_fields:
                return EMPTY_TIMESERIES

            timeseries = threedi_result.get_timeseries(
                parameters, node_id=self.object_id.value, fill_value=np.NaN
            )
            if timeseries.shape[1] == 1:
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
