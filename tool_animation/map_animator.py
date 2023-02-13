from qgis.core import NULL
from qgis.core import QgsDateTimeRange
from qgis.core import QgsInterval
from qgis.core import QgsProject
from qgis.core import QgsTemporalNavigationObject
from qgis.core import QgsVectorLayer
from qgis.core import QgsWkbTypes
from qgis.utils import iface
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QCheckBox
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtWidgets import QHBoxLayout, QGridLayout
from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.QtWidgets import QGroupBox
from threedigrid.admin.constants import NO_DATA_VALUE
from threedi_results_analysis.datasource.result_constants import DISCHARGE
from threedi_results_analysis.datasource.result_constants import H_TYPES
from threedi_results_analysis.datasource.result_constants import NEGATIVE_POSSIBLE
from threedi_results_analysis.datasource.result_constants import Q_TYPES
from threedi_results_analysis.datasource.result_constants import WATERLEVEL
from threedi_results_analysis.datasource.result_constants import AGGREGATION_OPTIONS
from threedi_results_analysis.datasource.threedi_results import ThreediResult
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem, ThreeDiGridItem
from threedi_results_analysis.utils.user_messages import StatusProgressBar
from threedi_results_analysis.utils.utils import generate_parameter_config
from threedi_results_analysis.utils.timing import timing
from typing import List

import threedi_results_analysis.tool_animation.animation_styler as styler
import copy
import logging
import math
import numpy as np
from bisect import bisect
from functools import lru_cache
from datetime import datetime as Datetime
from datetime import timedelta as Timedelta


logger = logging.getLogger(__name__)


def get_layer_by_id(layer_id):
    return QgsProject.instance().mapLayer(layer_id)


def copy_layer_into_memory_layer(source_layer, layer_name):
    source_provider = source_layer.dataProvider()

    uri = "{0}?crs=EPSG:{1}".format(
        QgsWkbTypes.displayString(source_provider.wkbType()).lstrip("WKB"),
        str(source_provider.crs().postgisSrid()),
    )

    dest_layer = QgsVectorLayer(uri, layer_name, "memory")
    dest_provider = dest_layer.dataProvider()

    dest_provider.addAttributes(source_provider.fields())
    dest_layer.updateFields()

    dest_provider.addFeatures([f for f in source_provider.getFeatures()])
    dest_layer.updateExtents()

    return dest_layer


def strip_agg_options(param: str) -> str:
    for opt in AGGREGATION_OPTIONS:
        if param.endswith("_" + opt):
            return param.rstrip("_" + opt)

    return param


@lru_cache(maxsize=None)
def threedi_result_percentiles(
    threedi_result: ThreediResult,
    groundwater: bool,
    variable: str,
    absolute: bool,
    lower_threshold: float,
    relative_to_t0: bool,
    simple=False,
) -> List[float]:
    """
    Calculate percentile values given variable in a 3Di results netcdf

    If variable is water level and relative_to_t0 = True,
    nodatavalues in the water level timeseries (i.e., dry nodes)
    will be replaced by the node's bottom level (z-coordinate)


    :param gr: GridH5ResultAdmin
    :param groundwater: calculate percentiles for groundwater (True) or anything but groundwater (False)
    :param variable: one of threedi_results_analysis.datasource.result_constants.SUBGRID_MAP_VARIABLES,
    with the exception of q_pump
    :param percentile: Percentile or sequence of class_bounds to compute, which must be between 0 and 100 inclusive.
    :param absolute: calculate percentiles on absolute values
    :param lower_threshold: ignore values below this threshold
    :param relative_to_t0: calculate percentiles on difference w/ initial values (applied before absolute)
    :param nodatavalue: ignore these values
    """
    if groundwater and not threedi_result.result_admin.has_groundwater:
        return MapAnimator.CLASS_BOUNDS_EMPTY

    stripped_variable = strip_agg_options(variable)
    gr = threedi_result.get_gridadmin(variable)
    if stripped_variable in Q_TYPES:
        if groundwater:
            nodes_or_lines = gr.lines.filter(kcu__in=[-150, 150])
        else:
            nodes_or_lines = gr.lines.filter(kcu__ne=-150).filter(kcu__ne=150)
    elif stripped_variable in H_TYPES:
        if groundwater:
            nodes_or_lines = gr.nodes.filter(node_type__in=[2, 6])
            if variable == WATERLEVEL.name and relative_to_t0:
                z_coordinates = gr.cells.filter(node_type__in=[2, 6]).z_coordinate
        else:
            nodes_or_lines = gr.nodes.filter(node_type__ne=2).filter(node_type__ne=6)
            if variable == WATERLEVEL.name and relative_to_t0:
                z_coordinates = (
                    gr.cells.filter(node_type__ne=2)
                    .filter(node_type__ne=6)
                    .z_coordinate
                )
    else:
        raise ValueError(f"unknown variable: {variable}")

    if simple:
        # only read the first and the last steps
        timestamps = threedi_result.get_timestamps(variable)
        indexes = slice(None, None, timestamps.size - 1)
        ts = nodes_or_lines.timeseries(indexes=indexes)
    else:
        ts = nodes_or_lines.timeseries(indexes=slice(None))

    values = getattr(ts, variable)
    values_t0 = values[0]
    if absolute:
        values = np.absolute(values)
        values_t0 = np.absolute(values_t0)
    values[values == NO_DATA_VALUE] = np.nan
    values_t0[values_t0 == NO_DATA_VALUE] = np.nan

    if relative_to_t0:
        if variable == WATERLEVEL.name:
            mask_t0 = np.isnan(values_t0)
            values_t0[mask_t0] = z_coordinates[mask_t0]
            z_coordinates_tiled = np.tile(z_coordinates, (values.shape[0], 1))
            mask = np.isnan(values)
            values[mask] = z_coordinates_tiled[mask]
        values -= values_t0
    values_above_threshold = values[values > lower_threshold]
    if np.isnan(values_above_threshold).all():
        return MapAnimator.CLASS_BOUNDS_EMPTY
    result = np.nanpercentile(
        values_above_threshold, MapAnimator.CLASS_BOUNDS_PERCENTILES
    ).tolist()
    return result


class MapAnimator(QGroupBox):
    """ """

    CLASS_BOUNDS_EMPTY = [0] * (styler.ANIMATION_LAYERS_NR_LEGEND_CLASSES)
    CLASS_BOUNDS_PERCENTILES = np.linspace(
        0, 100, styler.ANIMATION_LAYERS_NR_LEGEND_CLASSES, dtype=int
    ).tolist()

    def __init__(self, parent, model):

        super().__init__("Visualization settings", parent)
        self.model = model
        self.node_parameters = None
        self.line_parameters = None
        self.last_line_parameter = None
        self.last_node_parameter = None

        self.current_datetime = None
        self.setup_ui(parent)
        self._updating_temporal_controller = False

    def _update_temporal_controller(self, results):
        logger.info("Updating temporal controller")

        # gather info
        threedi_results = [r.threedi_result for r in results]
        datetimes = [
            np.array(tr.dt_timestamps, dtype='datetime64[s]')
            for tr in threedi_results
        ]

        # frame duration
        intervals = [
            round((d[1:] - d[:-1]).min().item().total_seconds())
            for d in datetimes
            if d.size >= 2
        ]
        frame_duration = max(1, min(intervals)) if intervals else 1
        logger.info(f"frame_duration {frame_duration}")

        # extent
        start_time = min(d[0].item() for d in datetimes)
        end_time = max(d[-1].item() for d in datetimes)
        end_time += Timedelta(seconds=frame_duration)  # to access last step
        temporal_extents = QgsDateTimeRange(start_time, end_time, True, True)
        logger.info(f"start_time {start_time}")
        logger.info(f"end_time {end_time}")

        temporal_controller = iface.mapCanvas().temporalController()
        self._updating_temporal_controller = True
        temporal_controller.setNavigationMode(QgsTemporalNavigationObject.NavigationMode.Animated)
        temporal_controller.setFrameDuration(QgsInterval(frame_duration))
        temporal_controller.setTemporalExtents(temporal_extents)
        temporal_controller.rewindToStart()
        self._updating_temporal_controller = False
        temporal_controller.skipToEnd()

    @pyqtSlot(ThreeDiResultItem)
    def results_changed(self, item: ThreeDiResultItem):
        results = self.model.get_results(checked_only=True)
        active = bool(results)

        self.line_parameter_combo_box.setEnabled(active)
        self.node_parameter_combo_box.setEnabled(active)
        self.difference_checkbox.setEnabled(active)
        self.setEnabled(active)

        self._update_parameter_attributes()
        self._update_parameter_combo_boxes()

        if not active:
            return

        self._restyle(lines=True, nodes=True)
        self._update_temporal_controller(results)
        # iface.mapCanvas().refresh()

    def _update_parameter_attributes(self):
        config = self._get_active_parameter_config()
        self.line_parameters = {r["name"]: r for r in config["q"]}
        self.node_parameters = {r["name"]: r for r in config["h"]}

    def _style_line_layers(self, result_item: ThreeDiResultItem, progress_bar):
        threedi_result = result_item.threedi_result
        self.last_line_parameter = self.current_line_parameter["parameters"]
        line_parameter_class_bounds, _ = self._get_class_bounds_line(threedi_result, self.last_line_parameter)
        grid_item = result_item.parent()
        assert isinstance(grid_item, ThreeDiGridItem)
        logger.info("Styling flowline layer")
        layer_id = grid_item.layer_ids["flowline"]
        virtual_field_name = result_item._result_field_names[layer_id][0]
        postfix = virtual_field_name[6:]  # remove "result" prefix
        layer = get_layer_by_id(layer_id)
        styler.style_animation_flowline_current(
            layer,
            line_parameter_class_bounds,
            self.current_line_parameter["parameters"],
            postfix,
        )
        progress_bar.increase_progress()

    def _style_node_layers(self, result_item: ThreeDiResultItem, progress_bar):
        """ Compute class bounds and apply style to node and cell layers. """
        threedi_result = result_item.threedi_result
        self.last_node_parameter = self.current_node_parameter["parameters"]
        node_parameter_class_bounds, _ = self._get_class_bounds_node(threedi_result, self.last_node_parameter)

        # Adjust the styling of the grid layer based on the bounds and result field name
        grid_item = result_item.parent()
        assert isinstance(grid_item, ThreeDiGridItem)

        logger.info("Styling node layer")
        layer_id = grid_item.layer_ids["node"]
        layer = get_layer_by_id(layer_id)
        virtual_field_name = result_item._result_field_names[layer_id][0]
        postfix = virtual_field_name[6:]  # remove "result" prefix
        if self.difference_checkbox.isChecked():
            styler.style_animation_node_difference(
                layer,
                node_parameter_class_bounds,
                self.current_node_parameter["parameters"],
                False,
                postfix,
            )
        else:
            styler.style_animation_node_current(
                layer,
                node_parameter_class_bounds,
                self.current_node_parameter["parameters"],
                False,
                postfix,
            )
        progress_bar.increase_progress()

        logger.info("Styling cell layer")
        layer_id = grid_item.layer_ids["cell"]
        layer = get_layer_by_id(layer_id)
        virtual_field_name = result_item._result_field_names[layer_id][0]
        postfix = virtual_field_name[6:]  # remove "result" prefix
        if self.difference_checkbox.isChecked():
            styler.style_animation_node_difference(
                layer,
                node_parameter_class_bounds,
                self.current_node_parameter["parameters"],
                True,
                postfix,
            )
        else:
            styler.style_animation_node_current(
                layer,
                node_parameter_class_bounds,
                self.current_node_parameter["parameters"],
                True,
                postfix,
            )
        progress_bar.increase_progress()

    @property
    def current_line_parameter(self):
        return self.line_parameters[self.line_parameter_combo_box.currentText()]

    @property
    def current_node_parameter(self):
        return self.node_parameters[self.node_parameter_combo_box.currentText()]

    def _restyle(self, lines, nodes):
        result_items = self.model.get_results(checked_only=True)
        total = (int(lines) + 2 * int(nodes)) * len(result_items)
        progress_bar = StatusProgressBar(total - 1, "Styling layers")

        for result_item in result_items:
            if lines:
                self._style_line_layers(result_item, progress_bar)
            if nodes:
                self._style_node_layers(result_item, progress_bar)
        del progress_bar

    def _restyle_and_update_lines(self):
        """To be used when line parameter changes."""
        self._restyle(lines=True, nodes=False)
        self._update_results()

    def _restyle_and_update_nodes(self):
        """To be used when node parameter or relative checkbox changes."""
        self._restyle(lines=False, nodes=True)
        self._update_results()

    def _get_class_bounds_node(self, threedi_result, node_variable):
        base_nc_name = strip_agg_options(node_variable)
        if (
            NEGATIVE_POSSIBLE[base_nc_name] or self.difference_checkbox.isChecked()
        ):
            lower_threshold = float("-Inf")
        else:
            lower_threshold = 0

        kwargs = dict(
            threedi_result=threedi_result,
            variable=node_variable,
            absolute=False,
            lower_threshold=lower_threshold,
            relative_to_t0=self.difference_checkbox.isChecked(),
        )
        with timing('percentiles1'):
            surfacewater_bounds = threedi_result_percentiles(
                groundwater=False, **kwargs,
            )
        with timing('percentiles2'):
            groundwater_bounds = threedi_result_percentiles(
                groundwater=True, **kwargs,
            )
        return surfacewater_bounds, groundwater_bounds

    def _get_class_bounds_line(self, threedi_result, line_variable):
        kwargs = dict(
            threedi_result=threedi_result,
            variable=line_variable,
            absolute=True,
            lower_threshold=float(0),
            relative_to_t0=self.difference_checkbox.isChecked(),
        )
        with timing('percentiles3'):
            surfacewater_bounds = threedi_result_percentiles(
                groundwater=False, **kwargs,
            )
        with timing('percentiles4'):
            groundwater_bounds = threedi_result_percentiles(
                groundwater=True, **kwargs,
            )
        return surfacewater_bounds, groundwater_bounds

    def _update_parameter_combo_boxes(self):
        """
        Fills parameter and combo boxes based on selected result
        """
        self._update_parameter_attributes()

        Q_CUM = 'q_cum'
        active = {WATERLEVEL.name, Q_CUM}
        if Q_CUM not in (v['parameters'] for v in self.line_parameters.values()):
            active.add(DISCHARGE.name)

        for combo_box, parameters, last_param in (
            (self.line_parameter_combo_box, self.line_parameters, self.last_line_parameter),
            (self.node_parameter_combo_box, self.node_parameters, self.last_node_parameter),
        ):
            combo_box.clear()
            if parameters:
                active_idx = None
                for idx, param_name in enumerate(sorted(parameters)):  # Sort on key
                    combo_box.addItem(param_name)
                    if last_param:
                        if parameters[param_name]["parameters"] == last_param:
                            active_idx = idx
                    elif parameters[param_name]["parameters"] in active:
                        active_idx = active_idx or idx  # Only assign if not yet set

                combo_box.setCurrentIndex(active_idx)
            else:
                last_param = None

    def _get_active_parameter_config(self):
        """
        Generates a parameter dict based on selected results.
        """
        q_vars = []
        h_vars = []

        for result in self.model.get_results(checked_only=True):
            threedi_result = result.threedi_result
            available_subgrid_vars = threedi_result.available_subgrid_map_vars

            # Make a deepcopy because we don't want to change the cached variables
            # in threedi_result.available_subgrid_map_vars
            available_subgrid_vars = copy.deepcopy(available_subgrid_vars)
            # 'q_pump' is a special case, which is currently not supported in the
            # animation tool.
            if "q_pump" in available_subgrid_vars:
                available_subgrid_vars.remove("q_pump")
            agg_vars = threedi_result.available_aggregation_vars[:]  # a copy

            parameter_config = generate_parameter_config(
                available_subgrid_vars, agg_vars=agg_vars
            )

            def _intersection(a: List, b: List):
                if not a:
                    return b

                return [x for x in a if x in b]

            q_vars = _intersection(q_vars, parameter_config["q"])
            h_vars = _intersection(h_vars, parameter_config["h"])

        config = {"q": q_vars, "h": h_vars}
        return config

    def update_results(self, qgs_dt_range):
        """ Slot for the updateTemporalRange signal. """
        if not self.isEnabled():
            return

        if self._updating_temporal_controller:
            return  # it emits a number of signals during the process

        try:
            self.current_datetime = qgs_dt_range.begin().toPyDateTime()
        except ValueError:
            logger.info('Could not convert animation datetime to python.')
            return

        self._update_results()

    def _update_results(self):
        logger.info('updating results to %s', self.current_datetime)
        for result_item in self.model.get_results(checked_only=True):
            self._update_result_item_results(result_item)

    @lru_cache(maxsize=None)
    def _get_feature_ids(self, layer):
        return np.array([f.id() for f in layer.getFeatures()], dtype="i8")

    def _update_result_item_results(self, result_item):
        """Fill initial value and result fields of the animation layers, based
        on currently set animation datetime and parameters."""
        grid_item = result_item.parent()

        layers_to_update = [
            (
                get_layer_by_id(grid_item.layer_ids["flowline"]),
                self.current_line_parameter,
            ),
            (
                get_layer_by_id(grid_item.layer_ids["node"]),
                self.current_node_parameter,
            ),
            (
                get_layer_by_id(grid_item.layer_ids["cell"]),
                self.current_node_parameter,
            ),
        ]

        # add item with relative time to model
        threedi_result = result_item.threedi_result

        begin_datetime = Datetime.fromisoformat(threedi_result.dt_timestamps[0])
        end_datetime = Datetime.fromisoformat(threedi_result.dt_timestamps[-1])
        current_datetime = max(
            begin_datetime, min(self.current_datetime, end_datetime),
        )

        current_delta = (current_datetime - begin_datetime)
        current_delta_str = '{}d {:02}:{:02}'.format(
            current_delta.days,
            current_delta.seconds // 3600,
            current_delta.seconds % 3600 // 60,
        )
        self.model.set_time_item(result_item, current_delta_str)

        for layer, parameter_config in layers_to_update:

            layer_id = layer.id()
            provider = layer.dataProvider()
            parameter = parameter_config["parameters"]
            parameter_long_name = parameter_config["name"]
            parameter_units = parameter_config["unit"]

            # determine timestep number for current parameter
            current_seconds = current_delta.total_seconds()
            parameter_timestamps = threedi_result.get_timestamps(parameter)
            timestep_nr = bisect(parameter_timestamps, current_seconds)
            timestep_nr = min(timestep_nr, parameter_timestamps.size - 1)

            values_t0 = threedi_result.get_values_by_timestep_nr(parameter, 0)
            values_ti = threedi_result.get_values_by_timestep_nr(
                parameter, timestep_nr
            )

            # theedigrid may have returned masked arrays in the past
            if isinstance(values_t0, np.ma.MaskedArray):
                values_t0 = values_t0.filled(np.NaN)
            if isinstance(values_ti, np.ma.MaskedArray):
                values_ti = values_ti.filled(np.NaN)

            if parameter == WATERLEVEL.name:
                # dry cells have a NO_DATA_VALUE water level
                values_t0[values_t0 == NO_DATA_VALUE] = np.NaN
                values_ti[values_ti == NO_DATA_VALUE] = np.NaN

            ti_field_index, t0_field_index = (
                layer.fields().indexOf(n)
                for n in result_item._result_field_names[layer_id]
            )
            assert ti_field_index != -1
            assert t0_field_index != -1

            ids = self._get_feature_ids(layer)

            # NOTE OF CAUTION: subtracting 1 from id  is mandatory for
            # groundwater because those indexes start from 1 (something to
            # do with a trash element), but for the non-groundwater version
            # it is not. HOWEVER, due to some magic hackery in how the
            # *_result layers are created/copied from the regular result
            # layers, the resulting feature ids also start from 1, which
            # why we need to subtract it in both cases, which btw is
            # purely coincidental.
            # TODO: to avoid all this BS this part should be refactored
            # by passing the index to get_values_by_timestep_nr, which
            # should take this into account
            print(min(ids), max(ids), values_t0.size, values_ti.size)
            dvalues_t0 = values_t0[ids - 1]
            dvalues_ti = values_ti[ids - 1]
            update_dict = {
                k: {
                    t0_field_index: NULL if math.isnan(v0) else v0,
                    ti_field_index: NULL if math.isnan(vi) else vi,
                } for k, v0, vi in zip(
                    ids.tolist(),
                    dvalues_t0.tolist(),
                    dvalues_ti.tolist(),
                )
            }
            provider.changeAttributeValues(update_dict)

            if (
                self.difference_checkbox.isChecked()
                and parameter_config == self.current_node_parameter
            ):
                layer_name_postfix = "relative to t0"
            else:
                layer_name_postfix = "current timestep"
            layer_name = (
                f"{parameter_long_name} [{parameter_units}] ({layer_name_postfix})"
            )

            layer.setName(layer_name)

            # Don't update invisible layers
            layer_tree_root = QgsProject.instance().layerTreeRoot()
            layer_tree_layer = layer_tree_root.findLayer(layer)
            if layer_tree_layer.isVisible():
                layer.triggerRepaint()

    def setup_ui(self, parent_widget: QWidget):
        parent_widget.layout().addWidget(self)

        self.HLayout = QHBoxLayout(self)
        self.setLayout(self.HLayout)

        line_group = QGroupBox("Flowline variable", self)
        line_group.setLayout(QGridLayout(self))

        self.line_parameter_combo_box = QComboBox(line_group)
        self.line_parameter_combo_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.line_parameter_combo_box.setToolTip("Choose flowline variable to display")
        line_group.layout().addWidget(self.line_parameter_combo_box)

        self.HLayout.addWidget(line_group)

        node_group = QGroupBox("Node variable", self)
        node_group.setLayout(QGridLayout(self))
        self.node_parameter_combo_box = QComboBox(node_group)
        self.node_parameter_combo_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.node_parameter_combo_box.setToolTip("Choose node variable to display")
        node_group.layout().addWidget(self.node_parameter_combo_box)

        self.difference_checkbox = QCheckBox("Relative", self)
        self.difference_checkbox.setToolTip(
            "Display difference relative to simulation start (nodes only)"
        )

        node_group.layout().addWidget(self.difference_checkbox, 0, 1)

        self.HLayout.addWidget(node_group)

        self.HLayout.addStretch()

        self.line_parameter_combo_box.activated.connect(self._restyle_and_update_lines)
        self.node_parameter_combo_box.activated.connect(self._restyle_and_update_nodes)
        self.difference_checkbox.stateChanged.connect(self._restyle_and_update_nodes)

        self.setEnabled(False)

    @staticmethod
    def index_to_duration(index, timestamps):
        """Return the duration between start of simulation and the selected time index

        Duration is returned as a tuple (days, hours, minutes) of the current active
        datasource, rounded down.

        Args:
            index (int): time index of the current selected datasource

        Returns:
            tuple days, hours, minutes

        """
        selected_timestamp = int(timestamps[index])
        days = selected_timestamp // 86400
        hours = (selected_timestamp // 3600) % 24
        minutes = (selected_timestamp // 60) % 60
        return days, hours, minutes
