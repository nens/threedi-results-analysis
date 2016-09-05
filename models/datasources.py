# -*- coding: utf-8 -*-

from PyQt4.QtCore import Qt, pyqtSignal
from ..datasource.netcdf import NetcdfDataSource
from base import BaseModel
from base_fields import CheckboxField, ValueField
from ..utils.layer_from_netCDF import (
    make_flowline_layer, make_node_layer, make_pumpline_layer)
from ..utils.user_messages import log
import os
from ..datasource.spatialite import Spatialite


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

class ValueWithChangeSignal(object):

    def __init__(self, signal_name, signal_setting_name, init_value = None):
        self.signal_name = signal_name
        self.signal_setting_name = signal_setting_name
        self.value = init_value

    def __get__(self, instance, type):
        return self.value

    def __set__(self, instance, value):
        self.value = value
        getattr(instance, self.signal_name).emit(self.signal_setting_name, value)

class TimeseriesDatasourceModel(BaseModel):

    model_schematisation_change = pyqtSignal(str, str)
    results_change = pyqtSignal(str, list)

    def __init__(self):
        BaseModel.__init__(self)
        self.dataChanged.connect(self.on_change)
        self.rowsRemoved.connect(self.on_change)
        self.rowsInserted.connect(self.on_change)

    # fields:
    tool_name = 'result_selection'
    model_spatialite_filepath = ValueWithChangeSignal('model_schematisation_change',
                                                      'model_schematisation')

    class Fields:
        active = CheckboxField(show=True, default_value=True, column_width=20,
                               column_name='')
        name = ValueField(show=True, column_width=130, column_name='Name')
        file_path = ValueField(show=True, column_width=260, column_name='File')
        type = ValueField(show=False)
        pattern = ValueField(show=False, default_value=get_line_pattern)

        _line_layer = None
        _node_layer = None
        _pumpline_layer = None

        def datasource(self):
            if hasattr(self, '_datasource'):
                return self._datasource
            elif self.type.value == 'netcdf':
                self._datasource = NetcdfDataSource(self.file_path.value)
                return self._datasource

        def get_result_layers(self):
            """Note: lines and nodes are always in the netCDF, pumps are not
            always in the netCDF."""

            file_name = self.datasource().file_path[:-3] + '.sqlite1'
            spl = Spatialite(file_name)

            if self._line_layer is None:
                if 'flowlines' in [t[1] for t in spl.getTables()]:
                    # todo check nr of attributes
                    self._line_layer = spl.get_layer('flowlines', None, 'the_geom')
                else:
                    self._line_layer = make_flowline_layer(self.datasource(), spl)

            if self._node_layer is None:
                if 'nodes' in [t[1] for t in spl.getTables()]:
                    self._node_layer = spl.get_layer('nodes', None, 'the_geom')
                else:
                    self._node_layer = make_node_layer(self.datasource(), spl)

            if self._pumpline_layer is None:

                if 'pumplines' in [t[1] for t in spl.getTables()]:
                    self._pumpline_layer = spl.get_layer('pumplines', None, 'the_geom')
                else:
                    try:
                        self._pumpline_layer = make_pumpline_layer(self.datasource(), spl)
                    except KeyError:
                        log("No pumps in netCDF", level='WARNING')

            return self._line_layer, self._node_layer, self._pumpline_layer

    def reset(self):

        self.removeRows(0, self.rowCount())

    def on_change(self, start=None, stop=None, etc=None):

        self.results_change.emit('result_directories', self.rows)






