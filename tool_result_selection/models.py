from cached_property import cached_property
from pathlib import Path
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import Qt
from ThreeDiToolbox.datasource.threedi_results import ThreediResult
from ThreeDiToolbox.models.base import BaseModel
from ThreeDiToolbox.models.base_fields import CheckboxField
from ThreeDiToolbox.models.base_fields import ValueField
from ThreeDiToolbox.utils.layer_from_netCDF import get_or_create_flowline_layer
from ThreeDiToolbox.utils.layer_from_netCDF import get_or_create_node_layer
from ThreeDiToolbox.utils.layer_from_netCDF import get_or_create_pumpline_layer
from ThreeDiToolbox.utils.user_messages import pop_up_info
from ThreeDiToolbox.utils.user_messages import StatusProgressBar

import logging


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

    already_used_patterns = [item.pattern.value for item in item_field.row.model.rows]

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
    logger.error(msg)
    pop_up_info(msg, title="Error")


class ValueWithChangeSignal(object):
    """Value for use inside a BaseModel. A change emits a signal.

    It works like a python property. The whole ``__get__``, ``instance``,
    ``owner`` stuff is explained here:
    https://stackoverflow.com/a/18038707/27401

    The ``signal_setting_name`` has to do with the way project state is saved,
    see ``utils/qprojects.py``.

    """

    def __init__(self, signal_name, signal_setting_name, initial_value=None):
        """Initialize ourselves as a kind-of-python-property.

        ``signal_name`` is the name of a class attribute that should be a qtsignal.

        ``signal_setting_name`` is the string that gets emitted as the first
        argument of the signal. It functions as a key for the key/value state
        storage mechanism from ``utils.qprojects.py``.

        """
        self.signal_name = signal_name
        self.signal_setting_name = signal_setting_name
        self.value = initial_value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value
        getattr(instance, self.signal_name).emit(self.signal_setting_name, value)


class DatasourceLayerHelper(object):
    """Helper class for TimeseriesDatasourceModel

    Our methods are transparently called from
    :py:class:`TimeseriesDatasourceModel`, so effectively we could also be
    methods on *that* class.

    """
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.datasource_dir = self.file_path.parent
        # Note: this is the older sqlite gridadmin, not the newer gridadmin.h5!
        self.sqlite_gridadmin_filepath = str(self.datasource_dir / "gridadmin.sqlite")

        # The following three are caches for self.get_result_layers()
        self._line_layer = None
        self._node_layer = None
        self._pumpline_layer = None

    @cached_property
    def threedi_result(self):
        """Return an instance of a subclass of ``BaseDataSource``."""
        return ThreediResult(self.file_path)

    def get_result_layers(self, progress_bar=None):
        """Return QgsVectorLayers for line, node, and pumpline layers.

        Use cached versions (``self._line_layer`` and so) if present.

        """
        if progress_bar is None:
            progress_bar = StatusProgressBar(100, "create gridadmin.sqlite")
        progress_bar.increase_progress(0, "create flowline layer")
        progress_bar.increase_progress(33, "create node layer")
        self._line_layer = self._line_layer or get_or_create_flowline_layer(
            self.threedi_result, self.sqlite_gridadmin_filepath
        )
        progress_bar.increase_progress(33, "create pumplayer layer")
        self._node_layer = self._node_layer or get_or_create_node_layer(
            self.threedi_result, self.sqlite_gridadmin_filepath
        )
        progress_bar.increase_progress(34, "done")
        self._pumpline_layer = self._pumpline_layer or get_or_create_pumpline_layer(
            self.threedi_result, self.sqlite_gridadmin_filepath
        )
        return [self._line_layer, self._node_layer, self._pumpline_layer]


class TimeseriesDatasourceModel(BaseModel):
    """Model for selecting threedi netcdf results.

    Used as ``self.ts_datasources`` throughout the entire plugin.

    Often, ``self.ts_datasources.rows[0]`` is used, as the first one is
    effectively treated as the selected datasource

    We're also used for storing the selected model schematisation as
    :py:attr:`model_spatialite_filepath`.

    """

    model_schematisation_change = pyqtSignal(str, str)
    results_change = pyqtSignal(str, list)

    def __init__(self):
        BaseModel.__init__(self)
        self.dataChanged.connect(self.on_change)
        self.rowsRemoved.connect(self.on_change)
        self.rowsInserted.connect(self.on_change)

    tool_name = "result_selection"
    #: model_spatialite_filepath is the currently selected 3di model db.
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
        def datasource_layer_helper(self):
            """Return DatasourceLayerHelper."""
            datasource_type = self.type.value
            if datasource_type != "netcdf-groundwater":
                pop_up_unkown_datasource_type()
                raise AssertionError("unknown datasource type: %s" % datasource_type)
            # Previously, the manager could handle more kinds of datasource
            # types. If in the future, more kinds again are needed,
            # instantiate a different kind of manager here.
            return DatasourceLayerHelper(self.file_path.value)

        def threedi_result(self):
            """Return ThreediResult instance."""
            return self.datasource_layer_helper.threedi_result

        def sqlite_gridadmin_filepath(self):
            # Note: this is the older sqlite gridadmin, not the newer gridadmin.h5!
            return self.datasource_layer_helper.sqlite_gridadmin_filepath

        def get_result_layers(self):
            return self.datasource_layer_helper.get_result_layers()

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
