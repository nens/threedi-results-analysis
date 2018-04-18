# -*- coding: utf-8 -*-

import os
from PyQt4.QtCore import Qt, pyqtSignal
from ..datasource.netcdf_groundwater import NetcdfDataSourceGroundwater
from ..datasource.netcdf import NetcdfDataSource
from .base import BaseModel
from .base_fields import CheckboxField, ValueField
from ..utils.layer_from_netCDF import (
    get_or_create_flowline_layer,
    get_or_create_node_layer,
    get_or_create_pumpline_layer,
    make_flowline_layer,
    make_node_layer,
    make_pumpline_layer,
    FLOWLINES_LAYER_NAME,
    NODES_LAYER_NAME,
    PUMPLINES_LAYER_NAME,
)
from ..utils.user_messages import log
from ..datasource.spatialite import Spatialite
from ..utils.user_messages import StatusProgressBar

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


class DataSourceLayerManager(object):
    """
    Abstracts away datasource-layer specifics.
    """
    type_ds_mapping = {
        'netcdf': NetcdfDataSource,
        'netcdf-groundwater': NetcdfDataSourceGroundwater,
    }

    def __init__(self, ds_type, file_path):
        self.ds_type = ds_type
        self.file_path = file_path

        self._datasource = None

        self._line_layer = None
        self._node_layer = None
        self._pumpline_layer = None

        self.type_ds_layer_func_mapping = {
            'netcdf': self._get_result_layers_regular,
            'netcdf-groundwater': self._get_result_layers_groundwater,
        }

    @property
    def datasource(self):
        """Returns an instance of a subclass of ``BaseDataSource``."""
        if self._datasource is None:
            ds_class = self.type_ds_mapping[self.ds_type]
            self._datasource = ds_class(self.file_path)
        return self._datasource

    @property
    def datasource_dir(self):
        return os.path.dirname(self.file_path)

    def get_result_layers(self):
        """Get QgsVectorLayers for line, node, and pumpline layers."""
        f = self.type_ds_layer_func_mapping[self.ds_type]
        return f()

    @property
    def spatialite_cache_filepath(self):
        """Only valid for type 'netcdf'"""
        if self.ds_type == 'netcdf':
            return self.file_path[:-3] + '.sqlite1'
        elif self.ds_type == 'netcdf-groundwater':
            return os.path.join(self.datasource_dir, 'gridadmin.sqlite')
        else:
            raise ValueError("Invalid datasource type %s" % self.ds_type)

    def _get_result_layers_regular(self):
        """Note: lines and nodes are always in the netCDF, pumps are not
        always in the netCDF.
        """

        spl = Spatialite(self.spatialite_cache_filepath)

        if self._line_layer is None:
            if FLOWLINES_LAYER_NAME in [t[1] for t in spl.getTables()]:
                # todo check nr of attributes
                self._line_layer = spl.get_layer(
                    FLOWLINES_LAYER_NAME, None, 'the_geom')
            else:
                self._line_layer = make_flowline_layer(
                    self.datasource, spl)

        if self._node_layer is None:
            if NODES_LAYER_NAME in [t[1] for t in spl.getTables()]:
                self._node_layer = spl.get_layer(
                    NODES_LAYER_NAME, None, 'the_geom')
            else:
                self._node_layer = make_node_layer(self.datasource, spl)

        if self._pumpline_layer is None:

            if PUMPLINES_LAYER_NAME in [t[1] for t in spl.getTables()]:
                self._pumpline_layer = spl.get_layer(
                    PUMPLINES_LAYER_NAME, None, 'the_geom')
            else:
                try:
                    self._pumpline_layer = make_pumpline_layer(
                        self.datasource, spl)
                except KeyError:
                    log("No pumps in netCDF", level='WARNING')

        return [self._line_layer, self._node_layer, self._pumpline_layer]

    def _get_result_layers_groundwater(self, progress_bar=None):

        if progress_bar is None:
            progress_bar = StatusProgressBar(100, 'create gridadmin.sqlite')

        sqlite_path = os.path.join(self.datasource_dir, 'gridadmin.sqlite')
        progress_bar.increase_progress(33, "create flowline layer")
        # this will also create a new sqlite if it doesn't exist
        # spl = Spatialite(sqlite_path)
        self._line_layer = self._line_layer or get_or_create_flowline_layer(
            self.datasource, sqlite_path)
        progress_bar.increase_progress(33, "create node layer")
        self._node_layer = self._node_layer or get_or_create_node_layer(
            self.datasource, sqlite_path)
        progress_bar.increase_progress(34, "create pumplayer")
        self._pumpline_layer = self._pumpline_layer or \
            get_or_create_pumpline_layer(self.datasource, sqlite_path)
        return [self._line_layer, self._node_layer, self._pumpline_layer]


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
    model_spatialite_filepath = ValueWithChangeSignal(
        'model_schematisation_change', 'model_schematisation')

    class Fields:
        active = CheckboxField(show=True, default_value=True, column_width=20,
                               column_name='')
        name = ValueField(show=True, column_width=130, column_name='Name')
        file_path = ValueField(show=True, column_width=260, column_name='File')
        type = ValueField(show=False)
        pattern = ValueField(show=False, default_value=get_line_pattern)

        def datasource_layer_manager(self):
            if not hasattr(self, '_datasource_layer_manager'):
                self._datasource_layer_manager = DataSourceLayerManager(
                    self.type.value, self.file_path.value)
            return self._datasource_layer_manager

        def datasource(self):
            return self.datasource_layer_manager().datasource

        def spatialite_cache_filepath(self):
            return self.datasource_layer_manager().spatialite_cache_filepath

        def get_result_layers(self):
            return self.datasource_layer_manager().get_result_layers()

    def reset(self):

        self.removeRows(0, self.rowCount())

    def on_change(self, start=None, stop=None, etc=None):

        self.results_change.emit('result_directories', self.rows)
