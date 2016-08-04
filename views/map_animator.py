import os
from PyQt4.QtGui import (QWidget, QHBoxLayout, QPushButton, QApplication, QComboBox)
from PyQt4.QtCore import (QVariant, )
from qgis.core import (QgsField, QgsMapLayerRegistry)
import numpy as np

from ..utils.geo_processing import copy_layer_into_memory_layer

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
        self.node_parameters = []
        self.line_parameters = []
        self.current_node_parameter = None
        self.current_line_parameter = None
        self.node_layer = None
        self.line_layer = None

        self.setup_ui()

        # set initial state
        self.line_parameter_combo_box.setEnabled(False)
        self.node_parameter_combo_box.setEnabled(False)

        self.set_line_parameter_config(set_parameter_config['q'])
        self.set_node_parameter_config(set_parameter_config['h'])

        # connect to signals
        self.activateButton.clicked.connect(self.set_activation_state)

        self.state_connectiong_set = False

    def set_activation_state(self, state):
        state = self.activateButton.isChecked()

        if state:
            if self.root_tool.ts_datasource.rowCount() > 0:
                self.line_parameter_combo_box.setEnabled(True)
                self.node_parameter_combo_box.setEnabled(True)
                self.prepare_annimation_layers()
                self.root_tool.timeslider_widget.sliderReleased.connect(self.update_results)


            # add listeners
            self.state_connection_set = True
        else:
            self.line_parameter_combo_box.setEnabled(False)
            self.node_parameter_combo_box.setEnabled(False)

            if self.state_connection_set:
                # remove listeners
                self.state_connection_set = False

    def prepare_annimation_layers(self):

        if self.root_tool.ts_datasource.rowCount() == 0:
            # todo: log warning
            return

        if self.node_layer is not None:
            return

        result = self.root_tool.ts_datasource.rows[0]
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
        result = self.root_tool.ts_datasource.rows[0]

        timestamp_nr = self.root_tool.timeslider_widget.value()

        ds = result.datasource()

        for layer, parameter, stat in ((self.node_layer, 's1', 'diff'), (self.line_layer, 'q', 'abs')):

            provider = layer.dataProvider()

            values = ds.get_values_timestamp(parameter, timestamp_nr)
            if stat == 'diff':
                values = values - ds.get_values_timestamp(parameter, 0)
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

    def set_line_parameter_config(self, parameter_config):

        self.line_parameters = dict([(p['name'], p) for p in parameter_config])
        self.line_parameter_combo_box.addItems(self.line_parameters.keys())
        # for pc in self.line_parameters.keys():
        #     self.line_parameter_combo_box.addItem(pc)
        self.line_parameter_combo_box.setCurrentIndex(1)
        self.current_line_parameter = \
            self.line_parameters[self.line_parameter_combo_box.currentText()]

    def set_node_parameter_config(self, parameter_config):
        self.node_parameters = dict([(p['name'], p) for p in parameter_config])
        self.node_parameter_combo_box.addItems(self.node_parameters.keys())
        # for pc in self.line_parameters.keys():
        #     self.line_parameter_combo_box.addItem(pc)
        self.node_parameter_combo_box.setCurrentIndex(1)
        self.current_node_parameter = \
            self.node_parameters[self.node_parameter_combo_box.currentText()]

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
