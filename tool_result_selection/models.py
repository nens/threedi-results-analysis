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
from ThreeDiToolbox.utils.signal_helper import ValueWithChangeSignal
from ThreeDiToolbox.utils.user_messages import pop_up_info
from ThreeDiToolbox.utils.user_messages import StatusProgressBar

import logging
import os


logger = logging.getLogger(__name__)


def get_line_pattern(item_field):
    """Return (default) line pattern for plots from this datasource.

    Look at the already-used styles and try to pick an unused one.

    :param item_field:
    :return: QT line pattern
    """
    available_styles = [
        Qt.SolidLine,
        Qt.DashLine,
        Qt.DotLine,
        Qt.DashDotLine,
        Qt.DashDotDotLine,
    ]

    already_used_patterns = [item.pattern.value for item in item_field.item.model.rows]

    for style in available_styles:
        if style not in already_used_patterns:
            # Hurray, an unused style.
            return style
    # No unused styles. Use the solid line style as a default.
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


class DataSourceLayerManager(object):
    """
    Abstracts away datasource-layer specifics.
    """

    DATASOURCE_TYPE_MAPPING = {"netcdf-groundwater": ThreediResult}
    DATASOURCE_TYPE_LAYER_FUNC_MAPPING = {
        "netcdf-groundwater": "_get_result_layers_groundwater"
    }
    DATASOURCE_TYPE_CACHE_FILE_MAPPING = {"netcdf-groundwater": "gridadmin.sqlite"}

    def __init__(self, datasource_type, file_path):
        if datasource_type not in self.DATASOURCE_TYPE_MAPPING:
            pop_up_unkown_datasource_type()
            raise AssertionError("unknown datasource type: %s" % datasource_type)

        self.datasource_type = datasource_type
        self.file_path = file_path

        # The following three are filled by self._get_result_layers_*()
        self._line_layer = None
        self._node_layer = None
        self._pumpline_layer = None

    @cached_property
    def datasource(self):
        """Returns an instance of a subclass of ``BaseDataSource``."""
        datasource_class = self.DATASOURCE_TYPE_MAPPING[self.datasource_type]
        return datasource_class(self.file_path)

    @property
    def datasource_dir(self):
        return os.path.dirname(self.file_path)

    def get_result_layers(self):
        """Get QgsVectorLayers for line, node, and pumpline layers."""
        method_name = self.DATASOURCE_TYPE_LAYER_FUNC_MAPPING[self.datasource_type]
        method = getattr(self, method_name)
        return method()

    @property
    def spatialite_cache_filepath(self):
        """Only valid for type 'netcdf-groundwater'"""
        filename = self.DATASOURCE_TYPE_CACHE_FILE_MAPPING[self.datasource_type]
        return os.path.join(self.datasource_dir, filename)

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


class DownloadableResultModel(BaseModel):
    """Model with 3di results that can be downloaded from lizard."""

    class Fields(object):
        name = ValueField(show=True, column_width=250, column_name="Name")
        size_mebibytes = ValueField(
            show=True, column_width=120, column_name="Size (MiB)"
        )
        url = ValueField(show=True, column_width=300, column_name="URL")
        results = ValueField(show=False)  # the scenario results
