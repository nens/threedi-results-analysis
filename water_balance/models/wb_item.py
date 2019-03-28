# -*- coding: utf-8 -*-
from builtins import str
from builtins import object
from collections import OrderedDict
from random import randint

import numpy as np
from ThreeDiToolbox.models.base import BaseModel
from ThreeDiToolbox.models.base_fields import ValueField, \
    ColorField, CheckboxField

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
    (43, 61, 38)
]

EMPTY_TIMESERIES = np.array([], dtype=float)


class ValueWithChangeSignal(object):

    def __init__(self, signal_name, signal_setting_name, init_value=None):
        self.signal_name = signal_name
        self.signal_setting_name = signal_setting_name
        self.value = init_value

    def __get__(self, instance, type):
        return self.value

    def __set__(self, instance, value):
        self.value = value
        getattr(instance, self.signal_name).emit(
            self.signal_setting_name, value)


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
    return (randint(0, 256), randint(0, 256), randint(0, 256), int(180))


class WaterbalanceItemModel(BaseModel):
    """Model implementation for waterbalance graph items"""

    ts = np.array([0])

    aggregation = ValueWithChangeSignal(
        'agg_change', 'aggregation', 'm3/s')
    split_meth0d = ValueWithChangeSignal(
        'split_change', 'split_method', 'defined')

    class Fields(object):
        """Fields and functions of ModelItem"""

        active = CheckboxField(show=True,
                               default_value=True,
                               column_width=20,
                               column_name='')
        fill_color = ColorField(show=False,
                                column_width=30,
                                column_name='',
                                default_value=select_default_color)
        pen_color = ColorField(show=True,
                               column_width=30,
                               column_name='',
                               default_value=select_default_color)
        name = ValueField(show=True,
                          column_width=210,
                          column_name='name')
        hover = ValueField(show=False, default_value=False)
        layer_in_table = ValueField(show=False, default_value=False)
        order = ValueField(show=False)
        default_method = ValueField(show=False)
        series = ValueField(show=False)
        ts_series = ValueField(show=False)
        _plots = {}
