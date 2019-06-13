from cached_property import cached_property
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import Qt
from ThreeDiToolbox.datasource.spatialite import Spatialite
from ThreeDiToolbox.datasource.threedi_results import ThreediResult
from ThreeDiToolbox.models.base import BaseModel
from ThreeDiToolbox.models.base_fields import CheckboxField
from ThreeDiToolbox.models.base_fields import ValueField
from ThreeDiToolbox.utils.layer_from_netCDF import FLOWLINES_LAYER_NAME
from ThreeDiToolbox.utils.layer_from_netCDF import get_or_create_flowline_layer
from ThreeDiToolbox.utils.layer_from_netCDF import get_or_create_node_layer
from ThreeDiToolbox.utils.layer_from_netCDF import get_or_create_pumpline_layer
from ThreeDiToolbox.utils.layer_from_netCDF import make_flowline_layer
from ThreeDiToolbox.utils.layer_from_netCDF import make_pumpline_layer
from ThreeDiToolbox.utils.layer_from_netCDF import NODES_LAYER_NAME
from ThreeDiToolbox.utils.layer_from_netCDF import PUMPLINES_LAYER_NAME
from ThreeDiToolbox.utils.user_messages import pop_up_info
from ThreeDiToolbox.utils.user_messages import StatusProgressBar

import logging
import os


logger = logging.getLogger(__name__)


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
        Qt.DashDotDotLine,
    ]

    used_patterns = [item.pattern.value for item in item_field.item.model.rows]

    for style in available_styles:
        if style not in used_patterns:
            return style

    return Qt.SolidLine


def pop_up_unkown_datasource_type():
    msg = (
        "QGIS3 works with ThreeDiToolbox >v1.6 and can only handle \n"
        "results created after March 2018 (groundwater release). \n\n"
        "You can do two things: \n"
        "1. simulate this model again and load the result in QGIS3 \n"
        "2. load this result into QGIS2.18 ThreeDiToolbox v1.6 "
    )
    # we only continue if self.datasource_type == 'netcdf-groundwater'
    logger.error(msg)
    pop_up_info(msg, title="Error")
    raise AssertionError("unknown datasource type")


class ValueWithChangeSignal(object):
    def __init__(self, signal_name, signal_setting_name, init_value=None):
        self.signal_name = signal_name
        self.signal_setting_name = signal_setting_name
        self.value = init_value

    def __get__(self, instance, type):
        return self.value

    def __set__(self, instance, value):
        self.value = value
        getattr(instance, self.signal_name).emit(self.signal_setting_name, value)


class DataSourceLayerManager(object):
    """
    Abstracts away datasource-layer specifics.
    """

    type_datasource_mapping = {"netcdf-groundwater": ThreediResult}

    def __init__(self, datasource_type, file_path):
        self.datasource_type = datasource_type
        self.file_path = file_path

        # The following three are filled by self._get_result_layers_*()
        self._line_layer = None
        self._node_layer = None
        self._pumpline_layer = None

        self.type_datasource_layer_func_mapping = {
            "netcdf-groundwater": self._get_result_layers_groundwater
        }

    @cached_property
    def datasource(self):
        """Returns an instance of a subclass of ``BaseDataSource``."""
        if self.datasource_type != "netcdf-groundwater":
            pop_up_unkown_datasource_type()
        datasource_class = self.type_datasource_mapping[self.datasource_type]
        return datasource_class(self.file_path)

    @property
    def datasource_dir(self):
        return os.path.dirname(self.file_path)

    def get_result_layers(self):
        """Get QgsVectorLayers for line, node, and pumpline layers."""
        f = self.type_datasource_layer_func_mapping[self.datasource_type]
        return f()

    @property
    def spatialite_cache_filepath(self):
        """Only valid for type 'netcdf-groundwater'"""
        if self.datasource_type == "netcdf-groundwater":
            return os.path.join(self.datasource_dir, "gridadmin.sqlite")
        else:
            raise ValueError("Invalid datasource type %s" % self.datasource_type)

    def _get_result_layers_regular(self):
        """Note: lines and nodes are always in the netCDF, pumps are not
        always in the netCDF.
        """

        spl = Spatialite(self.spatialite_cache_filepath)

        if self._line_layer is None:
            if FLOWLINES_LAYER_NAME in [t[1] for t in spl.getTables()]:
                # todo check nr of attributes
                self._line_layer = spl.get_layer(FLOWLINES_LAYER_NAME, None, "the_geom")
            else:
                self._line_layer = make_flowline_layer(self.datasource, spl)

        if self._node_layer is None:
            if NODES_LAYER_NAME in [t[1] for t in spl.getTables()]:
                self._node_layer = spl.get_layer(NODES_LAYER_NAME, None, "the_geom")
            else:
                # self._node_layer = make_node_layer(self.datasource, spl)
                # TODO: ^^^^ above make_node_layer() is defective.
                pass

        if self._pumpline_layer is None:

            if PUMPLINES_LAYER_NAME in [t[1] for t in spl.getTables()]:
                self._pumpline_layer = spl.get_layer(
                    PUMPLINES_LAYER_NAME, None, "the_geom"
                )
            else:
                try:
                    self._pumpline_layer = make_pumpline_layer(self.datasource, spl)
                except KeyError:
                    # TODO: we assume there are no pumps, but a keyerror can
                    # occur in many places inside that huge function.
                    logger.exception("No pumps in netCDF")

        return [self._line_layer, self._node_layer, self._pumpline_layer]

    def _get_result_layers_groundwater(self, progress_bar=None):

        if progress_bar is None:
            progress_bar = StatusProgressBar(100, "create gridadmin.sqlite")
        progress_bar.increase_progress(0, "create flowline layer")
        sqlite_path = os.path.join(self.datasource_dir, "gridadmin.sqlite")
        progress_bar.increase_progress(33, "create node layer")
        self._line_layer = self._line_layer or get_or_create_flowline_layer(
            self.datasource, sqlite_path
        )
        progress_bar.increase_progress(33, "create pumplayer layer")
        self._node_layer = self._node_layer or get_or_create_node_layer(
            self.datasource, sqlite_path
        )
        progress_bar.increase_progress(34, "done")
        self._pumpline_layer = self._pumpline_layer or get_or_create_pumpline_layer(
            self.datasource, sqlite_path
        )
        return [self._line_layer, self._node_layer, self._pumpline_layer]


class TimeseriesDatasourceModel(BaseModel):

    model_schematisation_change = pyqtSignal(str, str)
    results_change = pyqtSignal(str, list)

    def __init__(self):
        BaseModel.__init__(self)
        self.dataChanged.connect(self.on_change)
        self.rowsRemoved.connect(self.on_change)
        self.rowsInserted.connect(self.on_change)

    tool_name = "result_selection"
    # model_spatialite_filepath is the currently selected 3di model db.
    model_spatialite_filepath = ValueWithChangeSignal(
        "model_schematisation_change", "model_schematisation"
    )
    # TODO: don't we want a similar one for the selected netcdf? Instead of doing [0]?

    class Fields(object):
        active = CheckboxField(
            show=True, default_value=True, column_width=20, column_name=""
        )
        name = ValueField(show=True, column_width=130, column_name="Name")
        file_path = ValueField(show=True, column_width=615, column_name="File")
        type = ValueField(show=False)
        pattern = ValueField(show=False, default_value=get_line_pattern)

        @cached_property
        def datasource_layer_manager(self):
            return DataSourceLayerManager(self.type.value, self.file_path.value)

        def datasource(self):
            # TODO: which kind of datasource is this? The netcdf of a
            # ts_datasources object?
            return self.datasource_layer_manager.datasource

        def spatialite_cache_filepath(self):
            return self.datasource_layer_manager.spatialite_cache_filepath

        def get_result_layers(self):
            return self.datasource_layer_manager.get_result_layers()

    def reset(self):

        self.removeRows(0, self.rowCount())

    def on_change(self, start=None, stop=None, etc=None):
        # TODO: what are emitted aren't directories but datasource models?
        self.results_change.emit("result_directories", self.rows)


class DownloadResultModel(BaseModel):
    """Model with 3di results that can be downloaded from lizard."""

    class Fields(object):
        name = ValueField(show=True, column_width=250, column_name="Name")
        size_mebibytes = ValueField(
            show=True, column_width=120, column_name="Size (MiB)"
        )
        url = ValueField(show=True, column_width=300, column_name="URL")
        results = ValueField(show=False)  # the scenario results
