from qgis.core import QgsField
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.core import QgsWkbTypes
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtWidgets import QHBoxLayout
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtWidgets import QWidget
from ThreeDiToolbox.utils.user_messages import messagebar_message
from ThreeDiToolbox.utils.utils import generate_parameter_config

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


class MapAnimator(QWidget):
    """
    todo:
    - make active button toggle between states
    - enable/ disable pulldowns on activate
    - on enable, copy current model layers to memory and add column
    - add listener to slider - set current values in layer
    - add listeners to pulldown -
    - add listeners to result selection switch (ask if ok)
    - styling for layers

    """

    def __init__(self, parent, iface, root_tool):

        QWidget.__init__(self, parent)
        self.iface = iface
        self.root_tool = root_tool
        self.node_parameters = {}
        self.line_parameters = {}
        self.current_node_parameter = None
        self.current_line_parameter = None
        self.node_layer = None
        self.line_layer = None
        self.line_layer_groundwater = None
        self.node_layer_groundwater = None
        self.state = False
        self.setup_ui()

        # set initial state
        self.line_parameter_combo_box.setEnabled(False)
        self.node_parameter_combo_box.setEnabled(False)

        # connect to signals
        self.activateButton.clicked.connect(self.set_activation_state)

        self.state_connectiong_set = False

        self.line_parameter_combo_box.currentIndexChanged.connect(
            self.on_line_parameter_change
        )
        self.node_parameter_combo_box.currentIndexChanged.connect(
            self.on_node_parameter_change
        )

        self.root_tool.timeslider_widget.datasource_changed.connect(
            self.on_active_ts_datasource_change
        )

        self.on_active_ts_datasource_change()

    def on_line_parameter_change(self):
        old_parameter = self.current_line_parameter

        self.current_line_parameter = self.line_parameters[
            self.line_parameter_combo_box.currentText()
        ]

        if old_parameter != self.current_line_parameter:
            self.update_results()

    def on_node_parameter_change(self):
        old_parameter = self.current_node_parameter
        self.current_node_parameter = self.node_parameters[
            self.node_parameter_combo_box.currentText()
        ]

        if old_parameter != self.current_node_parameter:
            self.update_results()

    def on_active_ts_datasource_change(self):
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

            nr_old_parameters = combo_box.count()

            parameters.update(dict([(p["name"], p) for p in pc]))

            combo_box.insertItems(0, [p["name"] for p in pc])

            # todo: find best matching parameter based on previous selection
            if nr_old_parameters > 0:
                combo_box.setCurrentIndex(0)

            nr_parameters_tot = combo_box.count()
            for i in reversed(
                list(range(nr_parameters_tot - nr_old_parameters, nr_parameters_tot))
            ):
                combo_box.removeItem(i)

    def _get_active_parameter_config(self):

        active_ts_datasource = self.root_tool.timeslider_widget.active_ts_datasource

        if active_ts_datasource is not None:
            # TODO: just taking the first datasource, not sure if correct:
            threedi_result = active_ts_datasource.threedi_result()
            available_subgrid_vars = threedi_result.available_subgrid_map_vars
            available_agg_vars = threedi_result.available_aggregation_vars
            if not available_agg_vars:
                messagebar_message(
                    "Warning", "No aggregation netCDF was found.", level=0, duration=5
                )
            parameter_config = generate_parameter_config(
                available_subgrid_vars, available_agg_vars
            )
        else:
            parameter_config = {"q": {}, "h": {}}

        return parameter_config

    def set_activation_state(self, state):
        self.state = self.activateButton.isChecked()

        if state:
            if self.root_tool.ts_datasources.rowCount() > 0:
                self.line_parameter_combo_box.setEnabled(True)
                self.node_parameter_combo_box.setEnabled(True)
                self.prepare_animation_layers()
                self.root_tool.timeslider_widget.sliderReleased.connect(
                    self.update_results
                )

            # add listeners
            self.state_connection_set = True
        else:
            self.line_parameter_combo_box.setEnabled(False)
            self.node_parameter_combo_box.setEnabled(False)

            if self.state_connection_set:
                # remove listeners
                self.state_connection_set = False

    def prepare_animation_layers(self):

        result = self.root_tool.timeslider_widget.active_ts_datasource

        if result is None:
            # todo: logger warning
            return

        if self.node_layer is not None:
            # todo: react on datasource change
            return

        line, node, pump = result.get_result_layers()

        # lines without groundwater results
        self.line_layer = copy_layer_into_memory_layer(line, "line_results")
        self.line_layer.dataProvider().addAttributes(
            [QgsField("result", QVariant.Double)]
        )
        features = self.line_layer.getFeatures()
        ids = [
            f.id()
            for f in features
            if f.attribute("type") == "2d_groundwater"
            or f.attribute("type") == "1d_2d_groundwater"
        ]
        self.line_layer.dataProvider().deleteFeatures(ids)
        self.line_layer.updateFields()

        # lines with groundwater results
        self.line_layer_groundwater = copy_layer_into_memory_layer(
            line, "line_results_groundwater"
        )
        self.line_layer_groundwater.dataProvider().addAttributes(
            [QgsField("result", QVariant.Double)]
        )
        features = self.line_layer_groundwater.getFeatures()
        ids = [
            f.id()
            for f in features
            if f.attribute("type") != "2d_groundwater"
            and f.attribute("type") != "1d_2d_groundwater"
        ]
        self.line_layer_groundwater.dataProvider().deleteFeatures(ids)
        self.line_layer_groundwater.updateFields()

        # nodes without groundwater results
        self.node_layer = copy_layer_into_memory_layer(node, "node_results")
        self.node_layer.dataProvider().addAttributes(
            [QgsField("result", QVariant.Double)]
        )
        features = self.node_layer.getFeatures()
        ids = [
            f.id()
            for f in features
            if f.attribute("type") == "2d_groundwater"
            or f.attribute("type") == "2d_groundwater_bound"
        ]
        self.node_layer.dataProvider().deleteFeatures(ids)
        self.node_layer.updateFields()

        # nodes with groundwater results
        self.node_layer_groundwater = copy_layer_into_memory_layer(
            node, "node_results_groundwater"
        )
        self.node_layer_groundwater.dataProvider().addAttributes(
            [QgsField("result", QVariant.Double)]
        )
        features = self.node_layer_groundwater.getFeatures()
        ids = [
            f.id()
            for f in features
            if f.attribute("type") != "2d_groundwater"
            and f.attribute("type") != "2d_groundwater_bound"
        ]
        self.node_layer_groundwater.dataProvider().deleteFeatures(ids)
        self.node_layer_groundwater.updateFields()

        # todo: add this layers to the correct location
        self.line_layer.loadNamedStyle(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                os.path.pardir,
                "layer_styles",
                "tools",
                "line_discharge.qml",
            )
        )

        self.line_layer_groundwater.loadNamedStyle(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                os.path.pardir,
                "layer_styles",
                "tools",
                "line_groundwater_velocity.qml",
            )
        )

        self.node_layer.loadNamedStyle(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                os.path.pardir,
                "layer_styles",
                "tools",
                "node_waterlevel_diff.qml",
            )
        )

        self.node_layer_groundwater.loadNamedStyle(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                os.path.pardir,
                "layer_styles",
                "tools",
                "node_groundwaterlevel_diff.qml",
            )
        )

        root = QgsProject.instance().layerTreeRoot()

        animation_group_name = "animation_layers"
        animation_group = root.findGroup(animation_group_name)
        if animation_group is None:
            animation_group = root.insertGroup(0, animation_group_name)
        animation_group.removeAllChildren()

        QgsProject.instance().addMapLayer(self.line_layer, False)
        QgsProject.instance().addMapLayer(self.line_layer_groundwater, False)
        QgsProject.instance().addMapLayer(self.node_layer, False)
        QgsProject.instance().addMapLayer(self.node_layer_groundwater, False)

        animation_group.insertLayer(0, self.line_layer)
        animation_group.insertLayer(1, self.line_layer_groundwater)
        animation_group.insertLayer(2, self.node_layer)
        animation_group.insertLayer(3, self.node_layer_groundwater)

    def update_results(self):
        if not self.state:
            return

        result = self.root_tool.timeslider_widget.active_ts_datasource

        timestep_nr = self.root_tool.timeslider_widget.value()

        threedi_result = result.threedi_result()

        for layer, parameter, stat in (
            (self.node_layer, self.current_node_parameter["parameters"], "diff"),
            (self.line_layer, self.current_line_parameter["parameters"], "act"),
            (
                self.node_layer_groundwater,
                self.current_node_parameter["parameters"],
                "diff",
            ),
            (
                self.line_layer_groundwater,
                self.current_line_parameter["parameters"],
                "act",
            ),
        ):  # updated to act for actual, display actual value

            provider = layer.dataProvider()

            values = threedi_result.get_values_by_timestep_nr(parameter, timestep_nr)
            if isinstance(values, np.ma.MaskedArray):
                values = values.filled(np.NaN)
            if stat == "diff":
                values = values - threedi_result.get_values_by_timestep_nr(parameter, 0)
            # updated to act for actual, display actual value
            elif stat == "act":
                values = values  # removed np.fabs(values) to get actual value

            update_dict = {}
            field_index = layer.fields().lookupField("result")

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
                value = values[ids - 1]
                update_dict[ids] = {field_index: float(value)}

            provider.changeAttributeValues(update_dict)
            # layer.setCacheImage(None)
            layer.triggerRepaint()

    def activate_animator(self):
        pass

    def deactivate_animator(self):
        pass

    def setup_ui(self):
        self.HLayout = QHBoxLayout(self)
        self.setLayout(self.HLayout)
        self.activateButton = QPushButton(self)
        self.activateButton.setCheckable(True)
        self.HLayout.addWidget(self.activateButton)

        self.line_parameter_combo_box = QComboBox(self)
        self.node_parameter_combo_box = QComboBox(self)

        self.HLayout.addWidget(self.line_parameter_combo_box)
        self.HLayout.addWidget(self.node_parameter_combo_box)

        self.retranslate_ui(self)

    def retranslate_ui(self, widget):
        widget.activateButton.setText("Animation on")
