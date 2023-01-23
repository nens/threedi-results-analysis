from qgis.core import NULL
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.core import QgsWkbTypes
from qgis.utils import iface
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QCheckBox
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtWidgets import QLCDNumber
from qgis.PyQt.QtWidgets import QHBoxLayout, QGridLayout
from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.QtWidgets import QGroupBox
from threedigrid.admin.constants import NO_DATA_VALUE
from threedigrid.admin.gridresultadmin import GridH5ResultAdmin
from ThreeDiToolbox.datasource.result_constants import DISCHARGE
from ThreeDiToolbox.datasource.result_constants import H_TYPES
from ThreeDiToolbox.datasource.result_constants import NEGATIVE_POSSIBLE
from ThreeDiToolbox.datasource.result_constants import Q_TYPES
from ThreeDiToolbox.datasource.result_constants import WATERLEVEL
from ThreeDiToolbox.datasource.result_constants import AGGREGATION_OPTIONS
from ThreeDiToolbox.threedi_plugin_model import ThreeDiResultItem, ThreeDiGridItem
from ThreeDiToolbox.utils.utils import generate_parameter_config
from typing import Iterable
from typing import List
from typing import Union

import ThreeDiToolbox.tool_animation.animation_styler as styler
import copy
import logging
import math
import numpy as np


logger = logging.getLogger(__name__)


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


def threedi_result_percentiles(
    gr: GridH5ResultAdmin,
    groundwater: bool,
    variable: str,
    percentile: Union[float, Iterable],
    absolute: bool,
    lower_threshold: float,
    relative_to_t0: bool,
    nodatavalue=NO_DATA_VALUE,
) -> Union[float, List[float]]:
    """
    Calculate given percentile given variable in a 3Di results netcdf

    If variable is water level and relative_to_t0 = True,
    nodatavalues in the water level timeseries (i.e., dry nodes)
    will be replaced by the node's bottom level (z-coordinate)


    :param gr: GridH5ResultAdmin
    :param groundwater: calculate percentiles for groundwater (True) or anything but groundwater (False)
    :param variable: one of ThreeDiToolbox.datasource.result_constants.SUBGRID_MAP_VARIABLES,
    with the exception of q_pump
    :param percentile: Percentile or sequence of class_bounds to compute, which must be between 0 and 100 inclusive.
    :param absolute: calculate percentiles on absolute values
    :param lower_threshold: ignore values below this threshold
    :param relative_to_t0: calculate percentiles on difference w/ initial values (applied before absolute)
    :param nodatavalue: ignore these values
    """
    stripped_variable = strip_agg_options(variable)

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

    ts = nodes_or_lines.timeseries(indexes=slice(None))
    values = getattr(ts, variable)
    values_t0 = values[0]
    if absolute:
        values = np.absolute(values)
        values_t0 = np.absolute(values_t0)
    values[values == nodatavalue] = np.nan
    values_t0[values_t0 == nodatavalue] = np.nan

    if relative_to_t0:
        if variable == WATERLEVEL.name:
            values_t0[np.isnan(values_t0)] = z_coordinates[np.isnan(values_t0)]
            z_coordinates_tiled = np.tile(z_coordinates, (values.shape[0], 1))
            values[np.isnan(values)] = z_coordinates_tiled[np.isnan(values)]
        values -= values_t0
    values_above_threshold = values[values > lower_threshold]
    if np.isnan(values_above_threshold).all():
        return MapAnimator.EMPTY_CLASS_BOUNDS
    np_percentiles = np.nanpercentile(values_above_threshold, percentile)
    if isinstance(np_percentiles, np.ndarray):
        result = list(map(float, np_percentiles))
    else:
        result = float(np_percentiles)
    return result


class MapAnimator(QGroupBox):
    """ """

    EMPTY_CLASS_BOUNDS = [0] * (styler.ANIMATION_LAYERS_NR_LEGEND_CLASSES)

    def __init__(self, parent, model):

        super().__init__("Animation", parent)
        self.model = model
        self.node_parameters = {}
        self.line_parameters = {}
        self.current_node_parameter = None
        self.current_line_parameter = None
        self.setup_ui(parent)

    @pyqtSlot(ThreeDiResultItem)
    def results_changed(self, item: ThreeDiResultItem):
        self.setEnabled(self.model.number_of_results() > 0)
        # Fill comboboxes based on result files
        self.fill_parameter_combobox_items()

    @pyqtSlot(ThreeDiResultItem)
    def result_activated(self, item: ThreeDiResultItem):

        # Fill comboboxes based on result files
        self.fill_parameter_combobox_items()

        self.restyle()

        self.line_parameter_combo_box.setEnabled(True)
        self.node_parameter_combo_box.setEnabled(True)
        self.difference_checkbox.setEnabled(True)
        self.lcd.setEnabled(True)

        iface.mapCanvas().refresh()

    @pyqtSlot(ThreeDiResultItem)
    def result_deactivated(self, item: ThreeDiResultItem):
        # Fill comboboxes based on result files
        self.fill_parameter_combobox_items()

        active = (len(self.model.get_results(selected=True)) > 0)
        self.line_parameter_combo_box.setEnabled(active)
        self.node_parameter_combo_box.setEnabled(active)
        self.difference_checkbox.setEnabled(active)
        self.lcd.setEnabled(active)

        iface.mapCanvas().refresh()

    def style_layers(self, result_item: ThreeDiResultItem, line_parameter_class_bounds, node_parameter_class_bounds):
        """
        Apply styling to surface water and groundwater flowline layers,
        based value distribution in the results and difference vs. current choice
        """

        # has_groundwater = (
        #    self.model.get_results(selected=True)[result_idx].threedi_result.result_admin.has_groundwater
        # )

        # Adjust the styling of the grid layer based on the bounds and result field name
        grid_item = result_item.parent()
        assert isinstance(grid_item, ThreeDiGridItem)

        layer_id = grid_item.layer_ids["flowline"]
        virtual_field_name = result_item._result_field_names[layer_id][0]
        postfix = virtual_field_name[6:]  # remove "result" prefix

        layer = QgsProject.instance().mapLayer(layer_id)

        logger.info("Styling flowline layer")
        styler.style_animation_flowline_current(
            layer,
            line_parameter_class_bounds,
            self.current_line_parameter["parameters"],
            postfix,
        )

        layer_id = grid_item.layer_ids["node"]
        layer = QgsProject.instance().mapLayer(layer_id)
        virtual_field_name = result_item._result_field_names[layer_id][0]
        postfix = virtual_field_name[6:]  # remove "result" prefix

        logger.info("Styling node layer")
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

        layer_id = grid_item.layer_ids["cell"]
        layer = QgsProject.instance().mapLayer(layer_id)
        virtual_field_name = result_item._result_field_names[layer_id][0]
        postfix = virtual_field_name[6:]  # remove "result" prefix

        logger.info("Styling cell layer")
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

    def restyle(self):
        self.current_line_parameter = self.line_parameters[self.line_parameter_combo_box.currentText()]
        self.current_node_parameter = self.node_parameters[self.node_parameter_combo_box.currentText()]

        for result_idx in range(len(self.model.get_results(selected=True))):
            result_item = self.model.get_results(selected=True)[result_idx]

            line_parameter_class_bounds, node_parameter_class_bounds, _, _ = self.update_class_bounds(result_item)
            self.update_results(result_item, 0)
            self.style_layers(result_item, line_parameter_class_bounds, node_parameter_class_bounds)

    def update_class_bounds(self, result_item: ThreeDiResultItem):

        line_parameter_class_bounds = self.EMPTY_CLASS_BOUNDS
        node_parameter_class_bounds = self.EMPTY_CLASS_BOUNDS
        groundwater_line_parameter_class_bounds = self.EMPTY_CLASS_BOUNDS
        groundwater_node_parameter_class_bounds = self.EMPTY_CLASS_BOUNDS

        threedi_result = result_item.threedi_result
        percentile = np.linspace(
            0, 100, styler.ANIMATION_LAYERS_NR_LEGEND_CLASSES, dtype=int
        ).tolist()

        # nodes
        node_variable = self.current_node_parameter["parameters"]
        if self.current_node_parameter["aggregated"]:
            gr = threedi_result.aggregate_result_admin
        else:
            gr = threedi_result.result_admin

        # deftermine lower threshold
        base_nc_name = strip_agg_options(node_variable)
        logger.info(base_nc_name)
        if (
            NEGATIVE_POSSIBLE[base_nc_name] or self.difference_checkbox.isChecked()
        ):
            lower_threshold = float("-Inf")
        else:
            lower_threshold = 0

        node_parameter_class_bounds = threedi_result_percentiles(
            gr=gr,
            groundwater=False,
            variable=node_variable,
            percentile=percentile,
            absolute=False,
            lower_threshold=lower_threshold,
            relative_to_t0=self.difference_checkbox.isChecked(),
        )
        if gr.has_groundwater:
            groundwater_node_parameter_class_bounds = (
                threedi_result_percentiles(
                    gr=gr,
                    groundwater=True,
                    variable=node_variable,
                    percentile=percentile,
                    absolute=False,
                    lower_threshold=lower_threshold,
                    relative_to_t0=self.difference_checkbox.isChecked(),
                )
            )

        # update lines
        line_variable = self.current_line_parameter["parameters"]
        if self.current_line_parameter["aggregated"]:
            gr = threedi_result.aggregate_result_admin
        else:
            gr = threedi_result.result_admin
        line_parameter_class_bounds = threedi_result_percentiles(
            gr=gr,
            groundwater=False,
            variable=line_variable,
            percentile=percentile,
            absolute=True,
            lower_threshold=float(0),
            relative_to_t0=self.difference_checkbox.isChecked(),
        )

        if gr.has_groundwater:
            groundwater_line_parameter_class_bounds = (
                threedi_result_percentiles(
                    gr=gr,
                    groundwater=True,
                    variable=line_variable,
                    percentile=percentile,
                    absolute=True,
                    lower_threshold=float(0),
                    relative_to_t0=self.difference_checkbox.isChecked(),
                )
            )

        return (line_parameter_class_bounds, node_parameter_class_bounds, groundwater_line_parameter_class_bounds, groundwater_node_parameter_class_bounds)

    def fill_parameter_attributes(self):
        config = self._get_active_parameter_config()
        self.line_parameters = {r["name"]: r for r in config["q"]}
        self.node_parameters = {r["name"]: r for r in config["h"]}

    def fill_parameter_combobox_items(self):
        """
        Fills parameter and comboboxes based on selected result
        """
        self.fill_parameter_attributes()

        Q_CUM = 'q_cum'
        active = {WATERLEVEL.name, Q_CUM}
        if Q_CUM not in (v['parameters'] for v in self.line_parameters.values()):
            active.add(DISCHARGE.name)

        for combo_box, parameters in (
            (self.line_parameter_combo_box, self.line_parameters),
            (self.node_parameter_combo_box, self.node_parameters),
        ):
            combo_box.clear()
            for param_name, param in parameters.items():
                if param["parameters"] in active:
                    idx = 0
                else:
                    idx = 99999
                combo_box.insertItem(idx, param_name)
            combo_box.setCurrentIndex(0)

    def _get_active_parameter_config(self):
        """
        Generates a parameter dict based on selected results.
        """
        q_vars = []
        h_vars = []

        for result_idx in range(len(self.model.get_results(selected=True))):
            threedi_result = self.model.get_results(selected=True)[result_idx].threedi_result
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

        result = {"q": q_vars, "h": h_vars}
        logger.info(result)
        return result

    def update_results(self, result_item: ThreeDiResultItem, timestep_nr):
        """Fill the initial_value and result fields of the animation layers, depending on active result parameter"""

        if self.isEnabled():

            if not self.current_line_parameter or not self.current_node_parameter:
                return

            threedi_result = result_item.threedi_result

            # Update UI (LCD)
            days, hours, minutes = MapAnimator.index_to_duration(timestep_nr, threedi_result.get_timestamps())
            formatted_display = "{:d} {:02d}:{:02d}".format(days, hours, minutes)
            self.lcd.display(formatted_display)

            layers_to_update = []

            qgs_instance = QgsProject.instance()
            grid = result_item.parent()
            line, node, cell = (
                qgs_instance.mapLayer(grid.layer_ids[k])
                for k in ("flowline", "node", "cell")
            )
            layers_to_update.append((line, self.current_line_parameter))
            layers_to_update.append((node, self.current_node_parameter))
            layers_to_update.append((cell, self.current_node_parameter))

            # TODO relocate this
            ids_by_layer_attr = "_ids_by_layer"
            if not hasattr(self, ids_by_layer_attr):
                ids_by_layer = {}
                setattr(self, ids_by_layer_attr, ids_by_layer)
            else:
                ids_by_layer = getattr(self, ids_by_layer_attr)

            for layer, parameter_config in layers_to_update:

                if layer is None:
                    continue

                layer_id = layer.id()
                provider = layer.dataProvider()
                parameter = parameter_config["parameters"]
                parameter_long_name = parameter_config["name"]
                parameter_units = parameter_config["unit"]
                values_t0 = threedi_result.get_values_by_timestep_nr(parameter, 0)
                values_ti = threedi_result.get_values_by_timestep_nr(
                    parameter, timestep_nr
                )

                if isinstance(values_t0, np.ma.MaskedArray):
                    values_t0 = values_t0.filled(np.NaN)
                if isinstance(values_ti, np.ma.MaskedArray):
                    values_ti = values_ti.filled(np.NaN)

                # I suspect the two lines above intend to do the same as the two (new) lines below, but the lines above
                # don't work. Perhaps issue should be solved in threedigrid? [LvW]
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

                try:
                    ids = ids_by_layer[layer_id]
                except KeyError:
                    ids = np.array([
                        f.id()
                        for f in layer.getFeatures()
                    ], dtype="i8")
                    ids_by_layer[layer_id] = ids

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

                if self.difference_checkbox.isChecked() and layer in (node, cell):
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

        self.lcd = QLCDNumber()
        self.lcd.setToolTip('Time format: "days hours:minutes"')
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        # Let lcd display a maximum of 9 digits, this way it can display a maximum
        # simulation duration of 999 days, 23 hours and 59 minutes.
        self.lcd.setDigitCount(9)
        self.HLayout.addWidget(self.lcd)

        self.line_parameter_combo_box.activated.connect(self.restyle)
        self.node_parameter_combo_box.activated.connect(self.restyle)
        self.difference_checkbox.stateChanged.connect(self.restyle)

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
