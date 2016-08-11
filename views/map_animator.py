import os
from PyQt4.QtGui import (QWidget, QHBoxLayout, QPushButton, QApplication, QComboBox)
from PyQt4.QtCore import (QVariant, )
from qgis.core import (QgsField, QgsMapLayerRegistry)
import numpy as np

from graph import generate_parameter_config
from ..utils.geo_processing import copy_layer_into_memory_layer
from ..utils.user_messages import messagebar_message

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


set_parameter_config = {
    'q': [{'name': 'Debiet', 'unit': 'm3/s', 'parameters': ['q']},
          {'name': 'Snelheid', 'unit': 'm/s', 'parameters': ['u1']},
          {'name': 'Debiet interflow', 'unit': 'm3/s', 'parameters': ['qp']},
          {'name': 'Snelheid interflow', 'unit': 'm/s', 'parameters': ['up1']}],
    'h': [{'name': 'Waterstand', 'unit': 'mNAP', 'parameters': ['s1']},
          {'name': 'Volume', 'unit': 'm3', 'parameters': ['vol']}]
}


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

        self.state = False

        self.setup_ui()

        # set initial state
        self.line_parameter_combo_box.setEnabled(False)
        self.node_parameter_combo_box.setEnabled(False)

        # connect to signals
        self.activateButton.clicked.connect(self.set_activation_state)

        self.state_connectiong_set = False

        self.line_parameter_combo_box.currentIndexChanged.connect(
                self.on_line_parameter_change)
        self.node_parameter_combo_box.currentIndexChanged.connect(
                self.on_node_parameter_change)

        self.root_tool.timeslider_widget.datasource_changed.connect(
                self.on_active_datasource_change)

        self.on_active_datasource_change()

    def on_line_parameter_change(self):
        old_parameter = self.current_line_parameter

        self.current_line_parameter = \
            self.line_parameters[self.line_parameter_combo_box.currentText()]

        if old_parameter != self.current_line_parameter:
            self.update_results()

    def on_node_parameter_change(self):
        old_parameter = self.current_node_parameter
        self.current_node_parameter = \
            self.node_parameters[self.node_parameter_combo_box.currentText()]

        if old_parameter != self.current_node_parameter:
            self.update_results()

    def on_active_datasource_change(self):
        # reset
        parameter_config = self._get_active_parameter_config()

        for combo_box, parameters, pc in (
                (self.line_parameter_combo_box, self.line_parameters, parameter_config['q']),
                (self.node_parameter_combo_box, self.node_parameters, parameter_config['h'])):

            nr_old_parameters = combo_box.count()

            parameters.update(dict([(p['name'], p) for p in pc]))

            combo_box.insertItems(0, [p['name'] for p in pc])

            # todo: find best matching parameter based on previous selection
            if nr_old_parameters > 0:
                combo_box.setCurrentIndex(0)

            nr_parameters_tot = combo_box.count()
            for i in reversed(range(nr_parameters_tot - nr_old_parameters, nr_parameters_tot)):
                combo_box.removeItem(i)

    def _get_active_parameter_config(self):

        active_ds = self.root_tool.timeslider_widget.active_datasource

        if active_ds is not None:
            # TODO: just taking the first datasource, not sure if correct:
            ds = active_ds.datasource()
            available_subgrid_vars = ds.available_subgrid_map_vars
            available_agg_vars = ds.available_aggregation_vars
            if not available_agg_vars:
                messagebar_message(
                    "Warning", "No aggregation netCDF was found.", level=0,
                    duration=5)
            parameter_config = generate_parameter_config(
                available_subgrid_vars, available_agg_vars)
        else:
            parameter_config = {'q': {}, 'h': {}}

        return parameter_config

    def set_activation_state(self, state):
        self.state = self.activateButton.isChecked()

        if state:
            if self.root_tool.ts_datasource.rowCount() > 0:
                self.line_parameter_combo_box.setEnabled(True)
                self.node_parameter_combo_box.setEnabled(True)
                self.prepare_animation_layers()
                self.root_tool.timeslider_widget.sliderReleased.connect(self.update_results)

            # add listeners
            self.state_connection_set = True
        else:
            self.line_parameter_combo_box.setEnabled(False)
            self.node_parameter_combo_box.setEnabled(False)

            if self.state_connection_set:
                # remove listeners
                self.state_connection_set = False

    def prepare_animation_layers(self):

        result = self.root_tool.timeslider_widget.active_datasource

        if result is None:
            # todo: log warning
            return

        if self.node_layer is not None:
            #todo: react on datasource change
            return

        line, node, pump = result.get_memory_layers()

        self.line_layer = copy_layer_into_memory_layer(line, 'line_results')
        self.line_layer.dataProvider().addAttributes([
            QgsField("result", QVariant.Double)
        ])
        self.line_layer.updateFields()

        self.node_layer = copy_layer_into_memory_layer(node, 'node_results')
        self.node_layer.dataProvider().addAttributes([
            QgsField("result", QVariant.Double)
        ])
        self.node_layer.updateFields()

        # todo: add this layers to the correct location
        self.line_layer.loadNamedStyle(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), os.path.pardir,
            'layer_styles', 'tools', 'line_discharge.qml'))

        self.node_layer.loadNamedStyle(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), os.path.pardir,
            'layer_styles', 'tools', 'node_waterlevel_diff.qml'))

        QgsMapLayerRegistry.instance().addMapLayer(self.node_layer, True)
        QgsMapLayerRegistry.instance().addMapLayer(self.line_layer, True)

    def update_results(self):
        if not self.state:
            return

        result = self.root_tool.timeslider_widget.active_datasource

        timestamp_nr = self.root_tool.timeslider_widget.value()

        ds = result.datasource()

        for layer, parameter, stat in (
                (self.node_layer, self.current_node_parameter['parameters'], 'diff'),
                (self.line_layer, self.current_line_parameter['parameters'], 'abs')):

            provider = layer.dataProvider()

            values = ds.get_values_by_timestamp(parameter[0], timestamp_nr)
            if stat == 'diff':
                values = values - ds.get_values_by_timestamp(parameter[0], 0)
            elif stat == 'abs':
                values = np.fabs(values)

            update_dict = {}
            field_index = layer.fieldNameIndex('result')

            for feature in layer.getFeatures():
                ids = int(feature.id())
                value = values[ids - 1]
                update_dict[ids] = {
                    field_index: float(value)}

            provider.changeAttributeValues(update_dict)
            layer.setCacheImage(None)
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
        widget.activateButton.setText(_translate(
            "MapAnimator", "Animatie aan", None))
