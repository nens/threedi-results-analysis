# -*- coding: utf-8 -*-
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

    model = item_field.item.model
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
            show=True, default_value=True, column_width=20, column_name=""
        )
        color = ColorField(
            show=True,
            column_width=30,
            column_name="",
            default_value=select_default_color,
        )
        object_id = ValueField(show=True, column_width=50, column_name="id")
        object_name = ValueField(show=True, column_width=140, column_name="name")
        object_type = ValueField(show=False)
        hover = ValueField(show=False, default_value=False)
        file_path = ValueField(show=False)

        _plots = {}

        def plots(self, parameters=None, result_ds_nr=0, absolute=False):
            """
            get pyqtgraph plot of selected object and timeseries
            :param parameters: string, parameter identification
            :param result_ds_nr: nr of result datasource in model
            :return: pyqtgraph PlotDataItem
            """
            result_key = str(self.model.datasource.rows[result_ds_nr])
            if not str(parameters) in self._plots:
                self._plots[str(parameters)] = {}
            if result_key not in self._plots[str(parameters)]:
                ts_table = self.timeseries_table(
                    parameters=parameters, result_ds_nr=result_ds_nr, absolute=absolute
                )
                pattern = self.model.datasource.rows[result_ds_nr].pattern.value
                pen = pg.mkPen(color=self.color.qvalue, width=2, style=pattern)
                self._plots[str(parameters)][result_key] = pg.PlotDataItem(
                    ts_table, pen=pen
                )

            return self._plots[str(parameters)][result_key]

        def timeseries_table(self, parameters=None, result_ds_nr=0, absolute=False):
            """
            get list of timestamp values for object and parameters
            from result datasource
            :param parameters:
            :param result_ds_nr:
            :return: numpy array with timestamp, values
            """
            ds = self.model.datasource.rows[result_ds_nr].datasource()
            timeseries = ds.get_timeseries(
                parameters, self.object_id.value, fill_value=np.NaN
            )
            if timeseries.shape[1] == 1:
                return EMPTY_TIMESERIES
            if absolute:
                timeseries = np.abs(timeseries)
            return timeseries
