# TODO: calculate seperate class_bounds for groundwater
# TODO: add listeners to result selection switch (ask if ok)

import copy

from typing import (
    Iterable,
    List,
    Union
)
from math import isnan
from qgis.core import (
    NULL,
    Qgis,
    QgsMessageLog,
    QgsExpressionContextUtils,
    QgsField,
    QgsLayerTreeGroup,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes
)
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QWidget
)
from ThreeDiToolbox.utils import styler
from ThreeDiToolbox.utils.utils import generate_parameter_config
from ThreeDiToolbox.utils.user_messages import StatusProgressBar
from ThreeDiToolbox.utils.styler import ANIMATION_LAYERS_NR_LEGEND_CLASSES
from ThreeDiToolbox.datasource.result_constants import (
    Q_TYPES,
    H_TYPES,
    NEG_POSSIBLE,
    WATERLEVEL,
    DISCHARGE
)
from threedigrid.admin.gridresultadmin import GridH5ResultAdmin
from threedigrid.admin.constants import NO_DATA_VALUE

import logging
import numpy as np
import os

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


def threedi_result_percentiles(
        gr: GridH5ResultAdmin,
        variable: str,
        percentile: Union[float, Iterable],
        absolute: bool,
        lower_threshold: float,
        relative_to_t0: bool,
        nodatavalue=NO_DATA_VALUE
) -> Union[float, List[float]]:
    """
    Calculate given percentile given variable in a 3Di results netcdf

    If variable is water level and relative_to_t0 = True,
    nodatavalues in the water level timeseries (i.e., dry nodes)
    will be replaced by the node's bottom level (z-coordinate)

    :param gr: GridH5ResultAdmin
    :param variable: one of ThreeDiToolbox.datasource.result_constants.SUBGRID_MAP_VARIABLES,
    with the exception of q_pump
    :param percentile: Percentile or sequence of class_bounds to compute, which must be between 0 and 100 inclusive.
    :param absolute: calculate percentiles on absolute values
    :param lower_threshold: ignore values below this threshold
    :param relative_to_t0: calculate percentiles on difference w/ initial values (applied before absolute)
    :param nodatavalue: ignore these values
    """
    if variable in Q_TYPES:
        nodes_or_lines = gr.lines
    elif variable in H_TYPES:
        nodes_or_lines = gr.nodes
        if variable == WATERLEVEL.name and relative_to_t0:
            z_coordinates = gr.cells.z_coordinate
    else:
        raise ValueError('unknown variable')

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
    np_percentiles = np.nanpercentile(values_above_threshold, percentile)
    if isinstance(np_percentiles, np.ndarray):
        result = list(map(float, np_percentiles))
    else:
        result = float(np_percentiles)
    return result

class MapAnimator(QWidget):
    """
    """

    def __init__(self, parent, iface, root_tool):

        super().__init__(parent)
        self.iface = iface
        self.root_tool = root_tool
        self.node_parameters = {}
        self.line_parameters = {}
        self.current_node_parameter = None
        self.current_line_parameter = None
        self.line_parameter_class_bounds = [0] * (ANIMATION_LAYERS_NR_LEGEND_CLASSES + 1)
        self.node_parameter_class_bounds = [0] * (ANIMATION_LAYERS_NR_LEGEND_CLASSES + 1)
        self.animation_group = None
        self._node_layer = None  # store only layer id str to avoid keeping reference to deleted C++ object
        self._line_layer = None  # store only layer id str to avoid keeping reference to deleted C++ object
        self._line_layer_groundwater = None   # store only layer id str to avoid keeping reference to deleted C++ object
        self._node_layer_groundwater = None   # store only layer id str to avoid keeping reference to deleted C++ object
        self.setup_ui()
        self.active = False
        self.setEnabled(False)

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
                self.root_tool.timeslider_widget.sliderReleased.connect(self.on_slider_released) # TODO: check if this doesn't result in multiple connections to same signal
                self.root_tool.timeslider_widget.setValue(0)

                # Fake setting the slider to start to fill layers
                self.root_tool.timeslider_widget.sliderReleased.emit()
                self.root_tool.timeslider_widget.valueChanged.emit(0)
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
        self.root_tool.lcd.setEnabled(activate)
        self.root_tool.timeslider_widget.setEnabled(activate)

        self.iface.mapCanvas().refresh()

    @property
    def node_layer(self):
        return QgsProject.instance().mapLayer(self._node_layer)

    @node_layer.setter
    def node_layer(self, layer: QgsVectorLayer):
        self._node_layer = self.id_from_layer(layer)

    @property
    def line_layer(self):
        return QgsProject.instance().mapLayer(self._line_layer)

    @line_layer.setter
    def line_layer(self, layer: QgsVectorLayer):
        self._line_layer = self.id_from_layer(layer)

    @property
    def node_layer_groundwater(self):
        return QgsProject.instance().mapLayer(self._node_layer_groundwater)

    @node_layer_groundwater.setter
    def node_layer_groundwater(self, layer: QgsVectorLayer):
        self._node_layer_groundwater = self.id_from_layer(layer)

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
        has_groundwater = self. \
            root_tool. \
            timeslider_widget. \
            active_ts_datasource. \
            threedi_result(). \
            result_admin. \
            has_groundwater

        if self.current_line_parameter is None:
            style_lines = False

        if self.current_node_parameter is None:
            style_nodes = False

        if style_lines:
            styler.style_animation_flowline_current(
                self.line_layer,
                self.line_parameter_class_bounds,
                self.current_line_parameter['parameters']
            )
            if has_groundwater:
                styler.style_animation_flowline_current(
                    self.line_layer_groundwater,
                    self.line_parameter_class_bounds,
                    self.current_line_parameter['parameters']
                )

        if style_nodes:
            if self.difference_checkbox.isChecked():
                styler.style_animation_node_difference(
                    self.node_layer,
                    self.node_parameter_class_bounds,
                    self.current_node_parameter['parameters']
                )
                if has_groundwater:
                    styler.style_animation_node_difference(
                        self.node_layer_groundwater,
                        self.node_parameter_class_bounds,
                        self.current_node_parameter['parameters']
                    )
            else:
                styler.style_animation_node_current(self.node_layer, self.node_parameter_class_bounds)
                if has_groundwater:
                    styler.style_animation_node_current(self.node_layer_groundwater, self.node_parameter_class_bounds)

    def on_datasource_change(self):
        self.setEnabled(self.root_tool.ts_datasources.rowCount() > 0)

    def on_slider_released(self):
        self.update_results(update_nodes=True, update_lines=True)

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
            self.update_results(update_nodes=False, update_lines=True)
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
            self.update_results(update_nodes=True, update_lines=False)
            self.style_layers(style_nodes=True, style_lines=False)

    def on_difference_checkbox_state_change(self):
        self.update_class_bounds(update_nodes=True, update_lines=False)
        self.update_results(update_nodes=True, update_lines=False)
        self.style_layers(style_nodes=True, style_lines=False)

    def update_class_bounds(self, update_nodes: bool, update_lines: bool):
        gr = self. \
            root_tool. \
            timeslider_widget. \
            active_ts_datasource. \
            threedi_result(). \
            result_admin

        if update_nodes:
            if NEG_POSSIBLE[self.current_node_parameter['parameters']] or self.difference_checkbox.isChecked():
                lower_threshold = float('-Inf')
            else:
                lower_threshold = 0

            self.node_parameter_class_bounds = threedi_result_percentiles(
                gr=gr,
                variable=self.current_node_parameter["parameters"],
                percentile=list(range(0, 100, int(100 / ANIMATION_LAYERS_NR_LEGEND_CLASSES))) + [100],
                absolute=False,
                lower_threshold=lower_threshold,
                relative_to_t0=self.difference_checkbox.isChecked()
            )

        if update_lines:
            self.line_parameter_class_bounds = threedi_result_percentiles(
                gr=gr,
                variable=self.current_line_parameter["parameters"],
                percentile=list(range(0, 100, int(100 / ANIMATION_LAYERS_NR_LEGEND_CLASSES))) + [100],
                absolute=True,
                lower_threshold=float(0),
                relative_to_t0=self.difference_checkbox.isChecked()
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

        active_ts_datasource = self.root_tool.timeslider_widget.active_ts_datasource

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
            # TimesliderWidget of the map_animator does not yet support variables of
            # the aggregate netcdf, thus we do not display those variables.
            parameter_config = generate_parameter_config(
                available_subgrid_vars, agg_vars=[]
            )
        else:
            parameter_config = {"q": {}, "h": {}}

        return parameter_config

    def on_activate_button_clicked(self, checked: bool):
        activate = checked and self.root_tool.ts_datasources.rowCount() > 0
        self.active = activate

    def prepare_animation_layers(self, progress_bar=None):
        result = self.root_tool.timeslider_widget.active_ts_datasource

        if result is None:
            # todo: logger warning
            return

        if self.node_layer is not None:
            # todo: react on datasource change
            return

        result_admin = result.threedi_result().result_admin

        line, node, pump = result.get_result_layers(progress_bar=progress_bar)

        # update lines without groundwater results
        line_layer = copy_layer_into_memory_layer(line, "Flowlines")
        line_layer.dataProvider().addAttributes(
            [
                QgsField("initial_value", QVariant.Double),
                QgsField("result", QVariant.Double)
            ]
        )
        features = line_layer.getFeatures()
        ids = [
            f.id()
            for f in features
            if f.attribute("type") == "2d_groundwater"
               or f.attribute("type") == "1d_2d_groundwater"
        ]
        line_layer.dataProvider().deleteFeatures(ids)
        line_layer.updateFields()

        # update lines with groundwater results
        if result_admin.has_groundwater:
            line_layer_groundwater = copy_layer_into_memory_layer(
                line, "Groundwater: Flowlines"
            )
            line_layer_groundwater.dataProvider().addAttributes(
                [
                    QgsField("initial_value", QVariant.Double),
                    QgsField("result", QVariant.Double)
                ]
            )
            features = line_layer_groundwater.getFeatures()
            ids = [
                f.id()
                for f in features
                if f.attribute("type") != "2d_groundwater"
                   and f.attribute("type") != "1d_2d_groundwater"
            ]
            line_layer_groundwater.dataProvider().deleteFeatures(ids)
            line_layer_groundwater.updateFields()

        # update nodes without groundwater results
        node_layer = copy_layer_into_memory_layer(node, "Nodes")
        node_layer.dataProvider().addAttributes(
            [
                QgsField("z_coordinate", QVariant.Double),
                QgsField("initial_value", QVariant.Double),
                QgsField("result", QVariant.Double)
            ]
        )
        features = node_layer.getFeatures()
        ids = [
            f.id()
            for f in features
            if f.attribute("type") == "2d_groundwater"
               or f.attribute("type") == "2d_groundwater_bound"
        ]
        provider = node_layer.dataProvider()
        provider.deleteFeatures(ids)
        node_layer.updateFields()

        # fill z_coordinate for 2d nodes
        data = result_admin.cells.only('id', 'z_coordinate').data
        id_z_coordinate_map = dict(zip(data['id'], data['z_coordinate']))
        update_dict = {}
        field_index = node_layer.fields().lookupField('z_coordinate')
        for feature in node_layer.getFeatures():
            node_id = feature['id']  # instead of feature.id() to avoid the problem described in self.prepare_animation_layers
            feature_id = feature.id()
            z_coordinate = float(id_z_coordinate_map[node_id])
            if node_id in id_z_coordinate_map.keys():
                update_dict[feature_id] = {field_index: z_coordinate}
        provider.changeAttributeValues(update_dict)

        # update nodes with groundwater results
        if result_admin.has_groundwater:
            node_layer_groundwater = copy_layer_into_memory_layer(
                node, "Groundwater: Nodes"
            )
            node_layer_groundwater.dataProvider().addAttributes(
                [
                    QgsField("z_coordinate", QVariant.Double),
                    QgsField("initial_value", QVariant.Double),
                    QgsField("result", QVariant.Double)
                ]
            )
            features = node_layer_groundwater.getFeatures()
            ids = [
                f.id()
                for f in features
                if f.attribute("type") != "2d_groundwater"
                   and f.attribute("type") != "2d_groundwater_bound"
            ]
            provider = node_layer_groundwater.dataProvider()
            provider.deleteFeatures(ids)
            node_layer_groundwater.updateFields()

            # fill z_coordinate for 2d nodes
            data = result_admin.cells.only('id', 'z_coordinate').data
            id_z_coordinate_map = dict(zip(data['id'], data['z_coordinate']))
            update_dict = {}
            field_index = node_layer.fields().lookupField('z_coordinate')
            for feature in node_layer.getFeatures():
                node_id = feature['id']  # instead of feature.id() to avoid the problem described in self.prepare_animation_layers
                feature_id = feature.id()
                z_coordinate = float(id_z_coordinate_map[node_id])
                if node_id in id_z_coordinate_map.keys():
                    update_dict[feature_id] = {field_index: z_coordinate}
            provider.changeAttributeValues(update_dict)

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

        QgsProject.instance().addMapLayer(line_layer, False)
        QgsProject.instance().addMapLayer(node_layer, False)
        if result_admin.has_groundwater:
            QgsProject.instance().addMapLayer(line_layer_groundwater, False)
            QgsProject.instance().addMapLayer(node_layer_groundwater, False)

        if result_admin.has_groundwater:
            animation_group.insertLayer(0, line_layer_groundwater)
            self.line_layer_groundwater = line_layer_groundwater
            animation_group.insertLayer(0, node_layer_groundwater)
            self.node_layer_groundwater = node_layer_groundwater
        animation_group.insertLayer(0, line_layer)
        self.line_layer = line_layer
        animation_group.insertLayer(0, node_layer)
        self.node_layer = node_layer
        self.animation_group = animation_group

    def remove_animation_layers(self):
        """Remove animation layers and remove group if it is empty"""
        if self.animation_group is not None:
            project = QgsProject.instance()
            for lyr in (self.line_layer, self.node_layer, self.line_layer_groundwater, self.node_layer_groundwater):
                if lyr is not None:
                    project.removeMapLayer(lyr)
            self.line_layer = None
            self.node_layer = None
            self.node_layer_groundwater = None
            self.line_layer_groundwater = None
            if len(self.animation_group.children()) == 0:
                # ^^^ to prevent deleting the group when a user has added other layers into it
                QgsProject.instance().layerTreeRoot().removeChildNode(self.animation_group)
                self.animation_group = None

    def update_results(self, update_nodes: bool, update_lines: bool):
        """Fill the initial_value and result fields of the animation layers, depending on active result parameter"""

        if not self.active:
            return

        result = self.root_tool.timeslider_widget.active_ts_datasource
        timestep_nr = self.root_tool.timeslider_widget.value()
        threedi_result = result.threedi_result()

        layers_to_update = []
        if update_nodes:
            layers_to_update.append(
                (self.node_layer,
                 self.current_node_parameter,
                 )
            )
            if threedi_result.result_admin.has_groundwater:
                layers_to_update.append(
                    (self.node_layer_groundwater,
                     self.current_node_parameter,
                    )
                )

        if update_lines:
            layers_to_update.append(
                (self.line_layer,
                 self.current_line_parameter,
                 )
            )
            if threedi_result.result_admin.has_groundwater:
                layers_to_update.append(
                    (self.line_layer_groundwater,
                     self.current_line_parameter,
                     )
                )

        for layer, parameter_config in layers_to_update:
            if layer is not None:
                provider = layer.dataProvider()
                parameter = parameter_config['parameters']
                parameter_long_name = parameter_config['name']
                parameter_units = parameter_config['unit']
                values_t0 = threedi_result.get_values_by_timestep_nr(parameter, 0)
                values_ti = threedi_result.get_values_by_timestep_nr(parameter, timestep_nr)

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
                    fields_values_map = {}
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
                    update_dict[ids] = {t0_field_index: value_t0, ti_field_index: value_ti}

                provider.changeAttributeValues(update_dict)

                if self.difference_checkbox.isChecked() and layer in (self.node_layer, self.node_layer_groundwater):
                    layer_name_postfix = 'relative to t0'
                else:
                    layer_name_postfix = 'current timestep'
                layer_name = f'{parameter_long_name} [{parameter_units}] ({layer_name_postfix})'

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
        self.line_parameter_combo_box.setToolTip('Choose flowline variable to display')
        self.HLayout.addWidget(self.line_parameter_combo_box)

        hline1 = QFrame()
        hline1.setFrameShape(QFrame.VLine)
        hline1.setFrameShadow(QFrame.Sunken)
        self.HLayout.addWidget(hline1)

        self.node_parameter_combo_box = QComboBox(self)
        self.node_parameter_combo_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.node_parameter_combo_box.setToolTip('Choose node variable to display')
        self.HLayout.addWidget(self.node_parameter_combo_box)

        self.difference_checkbox = QCheckBox(self)
        self.difference_checkbox.setToolTip('Display difference relative to simulation start (nodes only)')
        self.difference_label = QLabel(self)
        self.difference_label.setText('Relative')
        self.difference_label.setToolTip('Display difference relative to simulation start (nodes only)')
        self.HLayout.addWidget(self.difference_checkbox)
        self.HLayout.addWidget(self.difference_label)

        hline2 = QFrame()
        hline2.setFrameShape(QFrame.VLine)
        hline2.setFrameShadow(QFrame.Sunken)
        self.HLayout.addWidget(hline2)

        # connect to signals
        self.activateButton.clicked.connect(self.on_activate_button_clicked)
        self.line_parameter_combo_box.currentIndexChanged.connect(self.on_line_parameter_change)
        self.node_parameter_combo_box.currentIndexChanged.connect(self.on_node_parameter_change)
        self.difference_checkbox.stateChanged.connect(self.on_difference_checkbox_state_change)
        self.root_tool.timeslider_widget.datasource_changed.connect(self.on_datasource_change)
