from collections import OrderedDict

from .base import BaseModel
from .base_fields import ValueField, ColorField, CheckboxField
from ..datasource.spatialite import TdiSpatialite

import numpy as np
import pyqtgraph as pg


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


def select_default_color(item_field):

    model = item_field.item.model
    colors = OrderedDict([(str(color), color) for color in COLOR_LIST])

    for item in model.rows:
        if str(item.color.value) in colors:
            del colors[str(item.color.value)]

    if len(colors) >= 1:
        return colors.values()[0]

    return COLOR_LIST[0]


class LocationTimeseriesModel(BaseModel):

    class Fields:

        active = CheckboxField(show=True, default_value=True, column_width=20, column_name='')
        color = ColorField(show=True, column_width=30, column_name='', default_value=select_default_color)
        object_id = ValueField(show=True, column_width=50, column_name='id')
        object_name = ValueField(show=True, column_width=140, column_name='name')
        object_type = ValueField(show=False)
        hover = ValueField(show=False, default_value=False)
        file_path = ValueField(show=True)

        def datasource(self):
            if hasattr(self, '_datasource'):
                return self._datasource
            else: # self.type.value == 'spatialite':
                self._datasource = TdiSpatialite(self.file_path.value)
                return self._datasource

        def plots(self, parameters=None, netcdf_nr=0):
            if not str(parameters) in self._plots:
                self._plots[str(parameters)] = {}
            if not str(netcdf_nr) in self._plots[str(parameters)]:
                ts_table = self.timeseries_table(parameters=parameters, netcdf_nr=netcdf_nr)
                pen = pg.mkPen(color=self.color.qvalue, width=2)
                self._plots[str(parameters)][str(netcdf_nr)] = pg.PlotDataItem(ts_table, pen=pen)

            return self._plots[str(parameters)][str(netcdf_nr)]

        def timeseries_table(self, parameters=None, netcdf_nr=0):
            float_data = []
            # for t, v in self.model.datasource.rows[netcdf_nr].datasource().get_timeseries(
            #         self.object_type.value, self.object_id.value, parameters):
            for t, v in self.model.datasource.rows[netcdf_nr]\
                    .datasource().get_timeseries(self.object_type.value, self.object_id.value, parameters):
                # some value data may come back as 'NULL' string; convert it to None
                # or else convert it to float
                v = None if v == 'NULL' else float(v)
                float_data.append((float(t), v))


            return np.array(float_data, dtype=float)
