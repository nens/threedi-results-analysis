# -*- coding: utf-8 -*-
from PyQt4.QtCore import Qt
from ..datasource.spatialite import TdiSpatialite
from ..datasource.netcdf import NetcdfDataSource
from base import BaseModel
from base_fields import CheckboxField, ValueField
from ..utils.layer_from_netCDF import make_flowline_layer, make_node_layer


def get_line_pattern(item_field):
    """
    get (default) line pattern for plots from this datasource
    :param item_field:
    :return:
    """
    available_styles = [
        Qt.SolidLine,
        Qt.DashLine,
        Qt.DotLine,
        Qt.DashDotLine,
        Qt.DashDotDotLine
    ]

    used_patterns = [item.pattern.value for item in item_field.item.model.rows]

    for style in available_styles:
        if style not in used_patterns:
            return style

    return Qt.SolidLine

class TimeseriesDatasourceModel(BaseModel):

    model_spatialite_filepath = None

    class Fields:

        active = CheckboxField(show=True, default_value=True, column_width=20, column_name='')
        name = ValueField(show=True, column_width=130, column_name='Name')
        file_path = ValueField(show=True, column_width=260, column_name='File')
        type = ValueField(show=False)
        pattern = ValueField(show=False, default_value=get_line_pattern)

        _line_layer = None
        _node_layer = None

        def datasource(self):
            if hasattr(self, '_datasource'):
                return self._datasource
            elif self.type.value == 'spatialite':
                self._datasource = TdiSpatialite(self.file_path.value)
                return self._datasource
            elif self.type.value == 'netcdf':
                self._datasource = NetcdfDataSource(self.file_path.value)
                return self._datasource

        def get_memory_layers(self):

            if self._line_layer is None:
                self._line_layer = make_flowline_layer(self.datasource())

            if self._node_layer is None:
                self._node_layer = make_node_layer(self.datasource())

            return self._line_layer, self._node_layer
