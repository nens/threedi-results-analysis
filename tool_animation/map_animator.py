# TODO: calculate seperate class_bounds for groundwater
# TODO: add listeners to result selection switch (ask if ok)

from math import isnan
from qgis.core import NULL
from qgis.core import QgsField
from qgis.core import QgsLayerTreeGroup
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.core import QgsWkbTypes
from qgis.utils import iface
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QCheckBox
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtWidgets import QFrame
from qgis.PyQt.QtWidgets import QLCDNumber
from qgis.PyQt.QtWidgets import QHBoxLayout
from qgis.PyQt.QtWidgets import QLabel
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtWidgets import QWidget
from threedigrid.admin.constants import NO_DATA_VALUE
from threedigrid.admin.gridresultadmin import GridH5ResultAdmin
from ThreeDiToolbox.datasource.result_constants import DISCHARGE
from ThreeDiToolbox.datasource.result_constants import H_TYPES
from ThreeDiToolbox.datasource.result_constants import NEGATIVE_POSSIBLE
from ThreeDiToolbox.datasource.result_constants import Q_TYPES
from ThreeDiToolbox.datasource.result_constants import WATERLEVEL
from ThreeDiToolbox.threedi_plugin_model import ThreeDiResultItem
from ThreeDiToolbox.utils.user_messages import StatusProgressBar
from ThreeDiToolbox.utils.utils import generate_parameter_config
from typing import Iterable
from typing import List
from typing import Union

import ThreeDiToolbox.tool_animation.animation_styler as styler
import copy
import logging
import numpy as np


logger = logging.getLogger(__name__)


class PercentileError(ValueError):
    """Raised when calculation of percentiles resulted in NaN"""

    pass


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
    if variable in Q_TYPES:
        if groundwater:
            nodes_or_lines = gr.lines.filter(kcu__in=[-150, 150])
        else:
            nodes_or_lines = gr.lines.filter(kcu__ne=-150).filter(kcu__ne=150)
    elif variable in H_TYPES:
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
        raise ValueError("unknown variable")

    last_timestamp = nodes_or_lines.timestamps[-1]
    ts = nodes_or_lines.timeseries(0, last_timestamp)
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
        raise PercentileError
    np_percentiles = np.nanpercentile(values_above_threshold, percentile)
    if isinstance(np_percentiles, np.ndarray):
        result = list(map(float, np_percentiles))
    else:
        result = float(np_percentiles)
    return result


class MapAnimator(QWidget):
    """ """

    EMPTY_CLASS_BOUNDS = [0] * (styler.ANIMATION_LAYERS_NR_LEGEND_CLASSES + 1)

    def __init__(self, parent, model):

        super().__init__(parent)
        self.model = model
        self.node_parameters = {}
        self.line_parameters = {}
        self.current_node_parameter = None
        self.current_line_parameter = None
        self.line_parameter_class_bounds = self.EMPTY_CLASS_BOUNDS
        self.node_parameter_class_bounds = self.EMPTY_CLASS_BOUNDS
        self.groundwater_line_parameter_class_bounds = self.EMPTY_CLASS_BOUNDS
        self.groundwater_node_parameter_class_bounds = self.EMPTY_CLASS_BOUNDS
        self.subgroup_1d = None
        self.subgroup_2d = None
        self.subgroup_groundwater = None
        self._animation_group = None

        # layers: store only layer id str to avoid keeping reference to deleted C++ object
        self._node_layer = None
        self._cell_layer = None
        self._line_layer_1d = None
        self._line_layer_2d = None
        self._line_layer_groundwater = None
        self._node_layer_groundwater = None
        self._cell_layer_groundwater = None
        self.setup_ui()
        self.active = False
        self.setEnabled(False)

    @pyqtSlot(ThreeDiResultItem)
    def results_changed(self, item: ThreeDiResultItem):
        if self.model.number_of_results() > 0:
            self.setEnabled(True)
        else:
            self.active = False
            self.setEnabled(False)

    # TODO: Move to util module
    @staticmethod
    def id_from_layer(layer: QgsVectorLayer):
        if layer is None:
            return None
        elif isinstance(layer, QgsVectorLayer):
            return layer.id()
        else:
            raise TypeError

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, activate: bool):
        """Enables/disables UI (except activateButtion) and adds/removes animation layers to QGIS project"""
        if activate:
            if not self._active:
                progress_bar = StatusProgressBar(300, "3Di Animation")
                self.prepare_animation_layers(progress_bar=progress_bar)
                progress_bar.increase_progress(1, "Create flowline animation layer")
                self.fill_parameter_combobox_items()
                self.on_line_parameter_change()  # to fill 'result' field of animation layers w/ data for cur. timestep
                progress_bar.increase_progress(99, "Create node animation layer")
                self.on_node_parameter_change()  # to fill 'result' field of animation layers w/ data for cur. timestep

                progress_bar.increase_progress(100, "Ready")
                self._active = True

        else:
            self.line_parameter_combo_box.clear()
            self.node_parameter_combo_box.clear()
            self.remove_animation_layers()
            self.activateButton.setChecked(False)
            self._active = False

        self.line_parameter_combo_box.setEnabled(activate)
        self.node_parameter_combo_box.setEnabled(activate)
        self.difference_checkbox.setEnabled(activate)
        self.difference_label.setEnabled(activate)
        self.lcd.setEnabled(activate)

        iface.mapCanvas().refresh()

    @property
    def node_layer(self):
        return QgsProject.instance().mapLayer(self._node_layer)

    @node_layer.setter
    def node_layer(self, layer: QgsVectorLayer):
        self._node_layer = self.id_from_layer(layer)

    @property
    def cell_layer(self):
        return QgsProject.instance().mapLayer(self._cell_layer)

    @cell_layer.setter
    def cell_layer(self, layer: QgsVectorLayer):
        self._cell_layer = self.id_from_layer(layer)

    @property
    def line_layer_2d(self):
        return QgsProject.instance().mapLayer(self._line_layer_2d)

    @line_layer_2d.setter
    def line_layer_2d(self, layer: QgsVectorLayer):
        self._line_layer_2d = self.id_from_layer(layer)

    @property
    def line_layer_1d(self):
        return QgsProject.instance().mapLayer(self._line_layer_1d)

    @line_layer_1d.setter
    def line_layer_1d(self, layer: QgsVectorLayer):
        self._line_layer_1d = self.id_from_layer(layer)

    @property
    def node_layer_groundwater(self):
        return QgsProject.instance().mapLayer(self._node_layer_groundwater)

    @node_layer_groundwater.setter
    def node_layer_groundwater(self, layer: QgsVectorLayer):
        self._node_layer_groundwater = self.id_from_layer(layer)

    @property
    def cell_layer_groundwater(self):
        return QgsProject.instance().mapLayer(self._cell_layer_groundwater)

    @cell_layer_groundwater.setter
    def cell_layer_groundwater(self, layer: QgsVectorLayer):
        self._cell_layer_groundwater = self.id_from_layer(layer)

    @property
    def line_layer_groundwater(self):
        return QgsProject.instance().mapLayer(self._line_layer_groundwater)

    @line_layer_groundwater.setter
    def line_layer_groundwater(self, layer: QgsVectorLayer):
        self._line_layer_groundwater = self.id_from_layer(layer)

    @property
    def animation_group(self):
        return QgsProject.instance().layerTreeRoot().findGroup(self._animation_group)

    @animation_group.setter
    def animation_group(self, group: QgsLayerTreeGroup):
        if group is None:
            self._animation_group = None
        else:
            self._animation_group = group.name()

    def setEnabled(self, enable: bool):
        """Toggles activateButton enabled and sets tool to active if animation layers already exist"""
        self.activateButton.setEnabled(enable)
        if enable:
            if self.node_layer is None:
                self.active = False
            else:
                self.active = True
        else:
            self.active = False

    def style_layers(self, style_lines: bool, style_nodes: bool):
        """
        Apply styling to surface water and groundwater flowline layers,
        based value distribution in the results and difference vs. current choice
        """
        has_groundwater = (
            self.root_tool.ts_datasources.rows[0].threedi_result().result_admin.has_groundwater  # TODO: ACTIVE
        )

        if self.current_line_parameter is None:
            style_lines = False

        if self.current_node_parameter is None:
            style_nodes = False

        if style_lines:
            # 1d
            styler.style_animation_flowline_current(
                self.line_layer_1d,
                self.line_parameter_class_bounds,
                self.current_line_parameter["parameters"],
            )
            # 2d
            styler.style_animation_flowline_current(
                self.line_layer_2d,
                self.line_parameter_class_bounds,
                self.current_line_parameter["parameters"],
            )
            if has_groundwater:
                styler.style_animation_flowline_current(
                    self.line_layer_groundwater,
                    self.groundwater_line_parameter_class_bounds,
                    self.current_line_parameter["parameters"],
                )

        if style_nodes:
            if self.difference_checkbox.isChecked():
                # nodes
                styler.style_animation_node_difference(
                    self.node_layer,
                    self.node_parameter_class_bounds,
                    self.current_node_parameter["parameters"],
                )
                # cells
                styler.style_animation_node_difference(
                    self.cell_layer,
                    self.node_parameter_class_bounds,
                    self.current_node_parameter["parameters"],
                    cells=True,
                )
                if has_groundwater:
                    # cells
                    styler.style_animation_node_difference(
                        self.cell_layer_groundwater,
                        self.groundwater_node_parameter_class_bounds,
                        self.current_node_parameter["parameters"],
                        cells=True,
                    )
            else:
                # nodes
                styler.style_animation_node_current(
                    self.node_layer,
                    self.node_parameter_class_bounds,
                    self.current_node_parameter["parameters"],
                )
                # cells
                styler.style_animation_node_current(
                    self.cell_layer,
                    self.node_parameter_class_bounds,
                    self.current_node_parameter["parameters"],
                    cells=True,
                )
                if has_groundwater:
                    # cells
                    styler.style_animation_node_current(
                        self.cell_layer_groundwater,
                        self.groundwater_node_parameter_class_bounds,
                        self.current_node_parameter["parameters"],
                        cells=True,
                    )

    def on_datasource_change(self):
        self.setEnabled(self.root_tool.ts_datasources.rowCount() > 0)

    def on_line_parameter_change(self):
        old_parameter = self.current_line_parameter
        combobox_current_text = self.line_parameter_combo_box.currentText()
        if combobox_current_text in self.line_parameters.keys():
            self.current_line_parameter = self.line_parameters[combobox_current_text]
        else:
            self.current_line_parameter = None
            return

        if old_parameter != self.current_line_parameter:
            self.update_class_bounds(update_nodes=False, update_lines=True)
            self._update_results(update_nodes=False, update_lines=True)
            self.style_layers(style_nodes=False, style_lines=True)

    def on_node_parameter_change(self):
        old_parameter = self.current_node_parameter
        combobox_current_text = self.node_parameter_combo_box.currentText()
        if combobox_current_text in self.node_parameters.keys():
            self.current_node_parameter = self.node_parameters[combobox_current_text]
        else:
            self.current_node_parameter = None
            return

        if old_parameter != self.current_node_parameter:
            self.update_class_bounds(update_nodes=True, update_lines=False)
            self._update_results(update_nodes=True, update_lines=False)
            self.style_layers(style_nodes=True, style_lines=False)

    def on_difference_checkbox_state_change(self):
        self.update_class_bounds(update_nodes=True, update_lines=False)
        self._update_results(update_nodes=True, update_lines=False)
        self.style_layers(style_nodes=True, style_lines=False)

    def update_class_bounds(self, update_nodes: bool, update_lines: bool):
        gr = (
            self.root_tool.ts_datasources.rows[0].threedi_result().result_admin  # TODO: ACTIVE
        )

        if update_nodes:
            if (
                NEGATIVE_POSSIBLE[self.current_node_parameter["parameters"]]
                or self.difference_checkbox.isChecked()
            ):
                lower_threshold = float("-Inf")
            else:
                lower_threshold = 0

            try:
                self.node_parameter_class_bounds = threedi_result_percentiles(
                    gr=gr,
                    groundwater=False,
                    variable=self.current_node_parameter["parameters"],
                    percentile=list(
                        range(0, 100, int(100 / styler.ANIMATION_LAYERS_NR_LEGEND_CLASSES))
                    )
                    + [100],
                    absolute=False,
                    lower_threshold=lower_threshold,
                    relative_to_t0=self.difference_checkbox.isChecked(),
                )
            except PercentileError:
                self.node_parameter_class_bounds = self.EMPTY_CLASS_BOUNDS

            if gr.has_groundwater:
                try:
                    self.groundwater_node_parameter_class_bounds = (
                        threedi_result_percentiles(
                            gr=gr,
                            groundwater=True,
                            variable=self.current_node_parameter["parameters"],
                            percentile=list(
                                range(
                                    0,
                                    100,
                                    int(100 / styler.ANIMATION_LAYERS_NR_LEGEND_CLASSES),
                                )
                            )
                            + [100],
                            absolute=False,
                            lower_threshold=lower_threshold,
                            relative_to_t0=self.difference_checkbox.isChecked(),
                        )
                    )
                except PercentileError:
                    self.groundwater_node_parameter_class_bounds = (
                        self.EMPTY_CLASS_BOUNDS
                    )

        if update_lines:
            try:
                self.line_parameter_class_bounds = threedi_result_percentiles(
                    gr=gr,
                    groundwater=False,
                    variable=self.current_line_parameter["parameters"],
                    percentile=list(
                        range(0, 100, int(100 / styler.ANIMATION_LAYERS_NR_LEGEND_CLASSES))
                    )
                    + [100],
                    absolute=True,
                    lower_threshold=float(0),
                    relative_to_t0=self.difference_checkbox.isChecked(),
                )
            except PercentileError:
                self.line_parameter_class_bounds = self.EMPTY_CLASS_BOUNDS

            if gr.has_groundwater:
                try:
                    self.groundwater_line_parameter_class_bounds = (
                        threedi_result_percentiles(
                            gr=gr,
                            groundwater=True,
                            variable=self.current_line_parameter["parameters"],
                            percentile=list(
                                range(
                                    0,
                                    100,
                                    int(100 / styler.ANIMATION_LAYERS_NR_LEGEND_CLASSES),
                                )
                            )
                            + [100],
                            absolute=True,
                            lower_threshold=float(0),
                            relative_to_t0=self.difference_checkbox.isChecked(),
                        )
                    )
                except PercentileError:
                    self.groundwater_line_parameter_class_bounds = (
                        self.EMPTY_CLASS_BOUNDS
                    )

    def fill_parameter_combobox_items(self):
        """
        Callback for datasource_changed signal

        Also sets self.line_parameters and self.node_parameters
        """

        # reset
        parameter_config = self._get_active_parameter_config()

        for combo_box, parameters, pc in (
            (
                self.line_parameter_combo_box,
                self.line_parameters,
                parameter_config["q"],
            ),
            (
                self.node_parameter_combo_box,
                self.node_parameters,
                parameter_config["h"],
            ),
        ):

            combo_box.clear()

            parameters.update(dict([(p["name"], p) for p in pc]))
            for param_name, param in parameters.items():
                if param["parameters"] in (DISCHARGE.name, WATERLEVEL.name):
                    idx = 0
                else:
                    idx = 99999
                combo_box.insertItem(idx, param_name)
            combo_box.setCurrentIndex(0)

    def _get_active_parameter_config(self):

        active_ts_datasource = self.root_tool.ts_datasources.rows[0]  # TODO: ACTIVE

        if active_ts_datasource is not None:
            # TODO: just taking the first datasource, not sure if correct:
            threedi_result = active_ts_datasource.threedi_result()
            available_subgrid_vars = threedi_result.available_subgrid_map_vars
            # Make a deepcopy because we don't want to change the cached variables
            # in threedi_result.available_subgrid_map_vars
            available_subgrid_vars = copy.deepcopy(available_subgrid_vars)
            # 'q_pump' is a special case, which is currently not supported in the
            # animation tool.
            if "q_pump" in available_subgrid_vars:
                available_subgrid_vars.remove("q_pump")

            parameter_config = generate_parameter_config(
                available_subgrid_vars, agg_vars=[]
            )
        else:
            parameter_config = {"q": {}, "h": {}}

        return parameter_config

    def on_activate_button_clicked(self, checked: bool):
        activate = checked and self.root_tool.ts_datasources.rowCount() > 0
        self.active = activate

    @staticmethod
    def prepare_animation_layer(
        source_layer: QgsVectorLayer,
        result_admin: GridH5ResultAdmin,
        output_layer_name: str,
        attributes: List[QgsField],
        groundwater: bool,
        only_1d: bool,
        only_2d: bool,
    ):
        output_layer = copy_layer_into_memory_layer(source_layer, output_layer_name)
        output_layer.dataProvider().addAttributes(attributes)
        features = output_layer.getFeatures()

        exclude_types = set()
        reverse_exclude_type_str = "this string will never occur in any type"
        if groundwater:
            exclude_types.update({"2d", "1d", "2d_bound", "1d_bound", "1d_2d"})
            reverse_exclude_type_str = "v2"
        else:
            exclude_types.update(
                {
                    "2d_groundwater",
                    "2d_groundwater_bound",
                    "2d_vertical_infiltration",
                    "1d_2d_groundwater",
                }
            )
        if only_1d:
            exclude_types.update(
                {
                    "2d",
                    "2d_bound",
                    "2d_groundwater",
                    "2d_groundwater_bound",
                    "2d_vertical_infiltration",
                    "1d_2d",
                }
            )
        if only_2d:
            exclude_types.update({"1d", "1d_bound"})
            reverse_exclude_type_str = "v2"
        delete_ids = [
            f.id()
            for f in features
            if f.attribute("type") in exclude_types
            or reverse_exclude_type_str in f.attribute("type")
        ]
        provider = output_layer.dataProvider()
        provider.deleteFeatures(delete_ids)
        output_layer.updateFields()

        field_index = output_layer.fields().lookupField("z_coordinate")
        if field_index != -1:
            data = result_admin.cells.only("id", "z_coordinate").data
            id_z_coordinate_map = dict(zip(data["id"], data["z_coordinate"]))
            update_dict = {}
            for feature in output_layer.getFeatures():
                node_id = feature["id"]
                feature_id = feature.id()
                z_coordinate = float(id_z_coordinate_map[node_id])
                if node_id in id_z_coordinate_map.keys():
                    update_dict[feature_id] = {field_index: z_coordinate}
            provider.changeAttributeValues(update_dict)

        return output_layer

    def prepare_animation_layers(self, progress_bar=None):
        result = self.root_tool.ts_datasources.rows[0]  # TODO: ACTIVE

        if result is None:
            # todo: logger warning
            return

        if self.node_layer is not None:
            # todo: react on datasource change
            return

        result_admin = result.threedi_result().result_admin

        line, node, cell, pump = result.get_result_layers(progress_bar=progress_bar)
        node_attributes = [
            QgsField("z_coordinate", QVariant.Double),
            QgsField("initial_value", QVariant.Double),
            QgsField("result", QVariant.Double),
        ]
        line_attributes = [
            QgsField("initial_value", QVariant.Double),
            QgsField("result", QVariant.Double),
        ]

        # update lines without groundwater results
        # 1d
        line_layer_1d = self.prepare_animation_layer(
            source_layer=line,
            result_admin=result_admin,
            output_layer_name="Flowlines",
            attributes=line_attributes,
            groundwater=False,
            only_1d=True,
            only_2d=False,
        )

        line_layer_2d = self.prepare_animation_layer(
            source_layer=line,
            result_admin=result_admin,
            output_layer_name="Flowlines",
            attributes=line_attributes,
            groundwater=False,
            only_1d=False,
            only_2d=True,
        )

        # update lines with groundwater results
        if result_admin.has_groundwater:
            line_layer_groundwater = self.prepare_animation_layer(
                source_layer=line,
                result_admin=result_admin,
                output_layer_name="Flowlines",
                attributes=line_attributes,
                groundwater=True,
                only_1d=False,
                only_2d=False,
            )

        # update nodes without groundwater results
        # NB: there is no 1D groundwater, so no groundwater nodes layer
        node_layer = self.prepare_animation_layer(
            source_layer=node,
            result_admin=result_admin,
            output_layer_name="Nodes",
            attributes=node_attributes,
            groundwater=False,
            only_1d=True,
            only_2d=False,
        )

        # update cells without groundwater results
        cell_layer = self.prepare_animation_layer(
            source_layer=cell,
            result_admin=result_admin,
            output_layer_name="Cells",
            attributes=node_attributes,
            groundwater=False,
            only_1d=False,
            only_2d=True,  # doesn't matter in fact, source layer already containts only 2d
        )

        # update cells with groundwater results
        if result_admin.has_groundwater:
            cell_layer_groundwater = self.prepare_animation_layer(
                source_layer=cell,
                result_admin=result_admin,
                output_layer_name="Cells",
                attributes=node_attributes,
                groundwater=True,
                only_1d=False,
                only_2d=True,  # doesn't matter in fact, source layer already containts only 2d
            )

        self.style_layers(style_lines=True, style_nodes=True)

        root = QgsProject.instance().layerTreeRoot()

        animation_group_name = "3Di Animation Layers"
        if self.animation_group is None:
            animation_group = root.findGroup(animation_group_name)
            if animation_group is None:
                animation_group = root.insertGroup(0, animation_group_name)
        else:
            animation_group = self.animation_group
        animation_group.removeAllChildren()  # TODO: do not remove child layers put there by the user
        if result_admin.has_groundwater:
            subgroup_groundwater = animation_group.insertGroup(0, "Groundwater")
        subgroup_2d = animation_group.insertGroup(0, "2D and domain exchange")
        subgroup_1d = animation_group.insertGroup(0, "1D")

        QgsProject.instance().addMapLayer(line_layer_1d, False)
        QgsProject.instance().addMapLayer(line_layer_2d, False)
        QgsProject.instance().addMapLayer(node_layer, False)
        QgsProject.instance().addMapLayer(cell_layer, False)
        if result_admin.has_groundwater:
            QgsProject.instance().addMapLayer(line_layer_groundwater, False)
            QgsProject.instance().addMapLayer(cell_layer_groundwater, False)

        # 1D group
        subgroup_1d.insertLayer(0, line_layer_1d)
        self.line_layer_1d = line_layer_1d
        subgroup_1d.insertLayer(0, node_layer)
        self.node_layer = node_layer
        self.subgroup_1d = subgroup_1d

        # 2D group
        subgroup_2d.insertLayer(0, cell_layer)
        self.cell_layer = cell_layer
        subgroup_2d.insertLayer(0, line_layer_2d)
        self.line_layer_2d = line_layer_2d
        self.subgroup_2d = subgroup_2d

        # Groundwater group
        if result_admin.has_groundwater:
            subgroup_groundwater.insertLayer(0, cell_layer_groundwater)
            self.cell_layer_groundwater = cell_layer_groundwater
            subgroup_groundwater.insertLayer(0, line_layer_groundwater)
            self.line_layer_groundwater = line_layer_groundwater
            self.subgroup_groundwater = subgroup_groundwater

        self.animation_group = animation_group

    def remove_animation_layers(self):
        """Remove animation layers and remove group if it is empty"""
        if self.animation_group is not None:
            project = QgsProject.instance()
            for lyr in (
                self.line_layer_1d,
                self.line_layer_2d,
                self.node_layer,
                self.cell_layer,
                self.line_layer_groundwater,
                self.node_layer_groundwater,
                self.cell_layer_groundwater,
            ):
                if lyr is not None:
                    project.removeMapLayer(lyr)
            self.line_layer_1d = None
            self.line_layer_2d = None
            self.node_layer = None
            self.cell_layer = None
            self.node_layer_groundwater = None
            self.line_layer_groundwater = None
            self.cell_layer_groundwater = None

            if len(self.subgroup_1d.children()) == 0:
                # ^^^ to prevent deleting the group when a user has added other layers into it
                self.animation_group.removeChildNode(self.subgroup_1d)
                self.subgroup_1d = None

            if len(self.subgroup_2d.children()) == 0:
                # ^^^ to prevent deleting the group when a user has added other layers into it
                self.animation_group.removeChildNode(self.subgroup_2d)
                self.subgroup_2d = None

            if self.subgroup_groundwater is not None:
                if len(self.subgroup_groundwater.children()) == 0:
                    # ^^^ to prevent deleting the group when a user has added other layers into it
                    self.animation_group.removeChildNode(self.subgroup_groundwater)
                    self.subgroup_groundwater = None

            if len(self.animation_group.children()) == 0:
                # ^^^ to prevent deleting the group when a user has added other layers into it
                QgsProject.instance().layerTreeRoot().removeChildNode(
                    self.animation_group
                )
                self.animation_group = None

    def _update_results(self, update_nodes: bool, update_lines: bool):
        self.update_results(0, update_nodes, update_lines)  # TODO: last timestep_nr should be stored

    def update_results(self, timestep_nr, update_nodes: bool, update_lines: bool):
        """Fill the initial_value and result fields of the animation layers, depending on active result parameter"""

        # messagebar_message("Timestep in MapAnimator", f"{timestep_nr}")

        if not self.active:
            return

        result = self.root_tool.ts_datasources.rows[0]  # TODO: ACTIVE
        threedi_result = result.threedi_result()

        # Update UI (LCD)
        days, hours, minutes = MapAnimator.index_to_duration(timestep_nr, threedi_result.get_timestamps())
        formatted_display = "{:d} {:02d}:{:02d}".format(days, hours, minutes)
        self.lcd.display(formatted_display)

        layers_to_update = []
        if update_nodes:
            layers_to_update.append((self.node_layer, self.current_node_parameter))
            layers_to_update.append((self.cell_layer, self.current_node_parameter))
            if threedi_result.result_admin.has_groundwater:
                layers_to_update.append(
                    (self.node_layer_groundwater, self.current_node_parameter)
                )
                layers_to_update.append(
                    (self.cell_layer_groundwater, self.current_node_parameter)
                )
        if update_lines:
            layers_to_update.append((self.line_layer_1d, self.current_line_parameter))
            layers_to_update.append((self.line_layer_2d, self.current_line_parameter))
            if threedi_result.result_admin.has_groundwater:
                layers_to_update.append(
                    (self.line_layer_groundwater, self.current_line_parameter)
                )

        for layer, parameter_config in layers_to_update:
            if layer is not None:
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

                update_dict = {}
                t0_field_index = layer.fields().lookupField("initial_value")
                ti_field_index = layer.fields().lookupField("result")

                for feature in layer.getFeatures():
                    ids = int(feature.id())
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
                    value_t0 = float(values_t0[ids - 1])
                    if isnan(value_t0):
                        value_t0 = NULL
                    value_ti = float(values_ti[ids - 1])
                    if isnan(value_ti):
                        value_ti = NULL
                    update_dict[ids] = {
                        t0_field_index: value_t0,
                        ti_field_index: value_ti,
                    }

                provider.changeAttributeValues(update_dict)

                if self.difference_checkbox.isChecked() and layer in (
                    self.node_layer,
                    self.node_layer_groundwater,
                    self.cell_layer,
                    self.cell_layer_groundwater,
                ):
                    layer_name_postfix = "relative to t0"
                else:
                    layer_name_postfix = "current timestep"
                layer_name = (
                    f"{parameter_long_name} [{parameter_units}] ({layer_name_postfix})"
                )

                layer.setName(layer_name)
                layer.triggerRepaint()

    def setup_ui(self):
        self.HLayout = QHBoxLayout(self)
        self.setLayout(self.HLayout)
        self.activateButton = QPushButton(self)
        self.activateButton.setCheckable(True)
        self.activateButton.setText("Animation on")
        self.HLayout.addWidget(self.activateButton)

        self.line_parameter_combo_box = QComboBox(self)
        self.line_parameter_combo_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.line_parameter_combo_box.setToolTip("Choose flowline variable to display")
        self.HLayout.addWidget(self.line_parameter_combo_box)

        hline1 = QFrame()
        hline1.setFrameShape(QFrame.VLine)
        hline1.setFrameShadow(QFrame.Sunken)
        self.HLayout.addWidget(hline1)

        self.node_parameter_combo_box = QComboBox(self)
        self.node_parameter_combo_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.node_parameter_combo_box.setToolTip("Choose node variable to display")
        self.HLayout.addWidget(self.node_parameter_combo_box)

        self.difference_checkbox = QCheckBox(self)
        self.difference_checkbox.setToolTip(
            "Display difference relative to simulation start (nodes only)"
        )
        self.difference_label = QLabel(self)
        self.difference_label.setText("Relative")
        self.difference_label.setToolTip(
            "Display difference relative to simulation start (nodes only)"
        )
        self.HLayout.addWidget(self.difference_checkbox)
        self.HLayout.addWidget(self.difference_label)

        hline2 = QFrame()
        hline2.setFrameShape(QFrame.VLine)
        hline2.setFrameShadow(QFrame.Sunken)
        self.HLayout.addWidget(hline2)

        self.lcd = QLCDNumber()
        self.lcd.setToolTip('Time format: "days hours:minutes"')
        self.lcd.setSegmentStyle(QLCDNumber.Flat)

        # Let lcd display a maximum of 9 digits, this way it can display a maximum
        # simulation duration of 999 days, 23 hours and 59 minutes.
        self.lcd.setDigitCount(9)
        self.HLayout.addWidget(self.lcd)

        # connect to signals
        self.activateButton.clicked.connect(self.on_activate_button_clicked)
        self.line_parameter_combo_box.currentIndexChanged.connect(
            self.on_line_parameter_change
        )
        self.node_parameter_combo_box.currentIndexChanged.connect(
            self.on_node_parameter_change
        )
        self.difference_checkbox.stateChanged.connect(
            self.on_difference_checkbox_state_change
        )

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
