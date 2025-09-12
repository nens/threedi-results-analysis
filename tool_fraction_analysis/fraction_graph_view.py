from qgis.core import Qgis
from qgis.core import QgsFeature
from qgis.core import QgsFeatureRequest
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.gui import QgsRubberBand
from qgis.PyQt.QtCore import QSize
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtWidgets import QHBoxLayout
from qgis.PyQt.QtWidgets import QSizePolicy
from qgis.PyQt.QtWidgets import QSplitter
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.PyQt.QtWidgets import QWidget
from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem
from threedi_results_analysis.tool_fraction_analysis.fraction_model import FractionModel
from threedi_results_analysis.tool_fraction_analysis.fraction_plot import FractionPlot
from threedi_results_analysis.tool_fraction_analysis.fraction_table import FractionTable
from threedi_results_analysis.utils.constants import TOOLBOX_MESSAGE_TITLE
from threedi_results_analysis.utils.user_messages import messagebar_message

import logging


logger = logging.getLogger(__name__)


class FractionWidget(QWidget):
    def __init__(
        self,
        parent,
        model: ThreeDiPluginModel,
        iface
    ):
        super().__init__(parent)

        self.result_model = model
        self.parent = parent
        self.iface = iface
        self.fraction_model = FractionModel(self, self.result_model)
        self.fraction_model.itemChanged.connect(self.model_item_changed)
        self.setup_ui()
        self.clear()

    def model_item_changed(self, item):
        # a plot is toggled or color is changed
        if item.index().column() == 0:
            self.fraction_plot.item_checked(item)
        elif item.index().column() == 1:
            self.fraction_plot.item_color_changed(item)

    def clear(self):
        self.fraction_model.clear()
        self.fraction_plot.clear_plot()

        self.current_result_id = None
        self.current_layer = None
        self.current_substance_unit = None
        self.current_feature_id = None
        self.current_stacked = False
        self.current_volume = False

    def result_selected(self, result_item: ThreeDiResultItem, substance_units):
        self.current_result_id = result_item.id
        self.current_feature_id = None
        self.fraction_plot.clear_plot()
        self.fraction_model.set_fraction(result_item, substance_units)

    def highlight_feature(self):
        if self.current_feature_id and self.current_result_id and self.current_layer:
            result_item = self.result_model.get_result(self.current_result_id)
            for table_name, layer_id in result_item.parent().layer_ids.items():
                if self.current_layer == table_name:
                    # query layer for object
                    filt = u'"id" = {0}'.format(self.current_feature_id)
                    request = QgsFeatureRequest().setFilterExpression(filt)
                    lyr = QgsProject.instance().mapLayer(layer_id)
                    features = lyr.getFeatures(request)
                    for feature in features:
                        self.marker.setToGeometry(feature.geometry(), lyr)

    def unhighlight_all_features(self):
        self.marker.reset()

    def setup_ui(self):
        mainLayout = QHBoxLayout(self)
        self.setLayout(mainLayout)
        splitterWidget = QSplitter(self)

        self.fraction_plot = FractionPlot(self, self.result_model, self.fraction_model)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.fraction_plot.sizePolicy().hasHeightForWidth())
        self.fraction_plot.setSizePolicy(sizePolicy)
        self.fraction_plot.setMinimumSize(QSize(250, 250))
        splitterWidget.addWidget(self.fraction_plot)

        legendWidget = QWidget(self)
        vLayoutTable = QVBoxLayout(self)
        vLayoutTable.setMargin(0)
        legendWidget.setLayout(vLayoutTable)

        self.ts_units_combo_box = QComboBox(self)
        self.ts_units_combo_box.insertItems(0, ["hrs", "mins", "s"])
        self.ts_units_combo_box.currentIndexChanged.connect(self.time_units_change)
        vLayoutTable.addWidget(self.ts_units_combo_box)
        self.fraction_table = FractionTable(self)
        self.fraction_table.hoverEnterRow.connect(self.highlight_feature)
        self.fraction_table.hoverExitAllRows.connect(self.unhighlight_all_features)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraction_table.sizePolicy().hasHeightForWidth())
        self.fraction_table.setSizePolicy(sizePolicy)
        self.fraction_table.setMinimumSize(QSize(250, 0))
        self.fraction_table.setModel(self.fraction_model)
        vLayoutTable.addWidget(self.fraction_table)
        splitterWidget.addWidget(legendWidget)
        mainLayout.addWidget(splitterWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        self.marker = QgsRubberBand(self.iface.mapCanvas())
        self.marker.setColor(Qt.red)
        self.marker.setWidth(2)

    def time_units_change(self):
        self.fraction_plot.setLabel("bottom", "Time", self.ts_units_combo_box.currentText())
        if self.current_feature_id and self.current_substance_unit:
            self.fraction_plot.fraction_selected(self.current_feature_id, self.current_substance_unit, self.ts_units_combo_box.currentText(), self.current_stacked, self.current_volume)

    def substance_units_change(self, substance_unit):
        self.current_substance_unit = substance_unit
        if self.current_result_id:
            self.fraction_model.set_fraction(self.result_model.get_result(self.current_result_id), self.current_substance_unit)
        if self.current_feature_id:
            self.fraction_plot.fraction_selected(self.current_feature_id, self.current_substance_unit, self.ts_units_combo_box.currentText(), self.current_stacked, self.current_volume)

    def stacked_changed(self, check_state):
        self.current_stacked = (check_state == Qt.Checked)
        if self.current_feature_id:
            self.fraction_plot.fraction_selected(self.current_feature_id, self.current_substance_unit, self.ts_units_combo_box.currentText(), self.current_stacked, self.current_volume)

    def volume_changed(self, check_state):
        self.current_volume = (check_state == Qt.Checked)
        if self.current_feature_id:
            self.fraction_plot.fraction_selected(self.current_feature_id, self.current_substance_unit, self.ts_units_combo_box.currentText(), self.current_stacked, self.current_volume)

    def feature_selected(self, layer: QgsVectorLayer, feature: QgsFeature) -> bool:
        if not layer.objectName() in ("node", "cell"):
            msg = """Please select results from either the 'nodes' or 'cells' layer."""
            messagebar_message(TOOLBOX_MESSAGE_TITLE, msg, Qgis.Warning, 5.0)
            return False

        if len(self.result_model.get_results(checked_only=False)) == 0:
            logger.warning("No results loaded")
            return False

        assert layer.dataProvider().name() in ["memory", "ogr"]
        new_idx = feature["id"]
        self.current_feature_id = new_idx
        result_items = self.result_model.get_results(checked_only=False)
        for result_item in result_items:
            # Check whether this layer belongs to the selected grid
            if layer.id() in result_item.parent().layer_ids.values():
                self.fraction_plot.fraction_selected(new_idx, self.current_substance_unit, self.ts_units_combo_box.currentText(), self.current_stacked, self.current_volume)
                self.current_result_id = result_item.id
                self.current_layer = layer.objectName()
                break

        return True
