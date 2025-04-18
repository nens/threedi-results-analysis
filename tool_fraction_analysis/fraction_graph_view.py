from qgis.core import Qgis
from qgis.core import QgsFeature
from qgis.core import QgsFeatureRequest
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.gui import QgsRubberBand
from qgis.PyQt.QtCore import pyqtSlot
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

        self.model = model
        self.parent = parent
        self.iface = iface

        self.setup_ui()

        self.fraction_model = FractionModel(self, self.model)
        self.fraction_plot.set_fraction_model(self.fraction_model)
        self.fraction_plot.set_result_model(self.model)
        self.fraction_table.setModel(self.fraction_model)
        
        # set listeners
        self.ts_units_combo_box.currentIndexChanged.connect(self.time_units_change)
        self.fraction_table.deleteRequested.connect(self._removeRows)

        self.marker = QgsRubberBand(self.iface.mapCanvas())
        self.marker.setColor(Qt.red)
        self.marker.setWidth(2)

    def _removeRows(self, index_list):
        # Also here, remove in decreasing order to keep table idx valid
        row_list = [index.row() for index in index_list]
        row_list.sort(reverse=True)
        for row in row_list:
            self.fraction_model.removeRows(row, 1)

    def refresh_table(self):
        # trigger all listeners by emiting dataChanged signal
        self.fraction_model.beginResetModel()
        self.fraction_model.endResetModel()
        self.fraction_table._update_table_widgets()

    @pyqtSlot(ThreeDiResultItem)
    def result_removed(self, result_item: ThreeDiResultItem):
        # Remove corresponding plots that refer to this item
        item_idx_to_remove = []
        for count, item in enumerate(self.fraction_model.rows):
            if item.result.value is result_item:
                item_idx_to_remove.append(count)

        # We delete them descending to keep the row idx consistent
        for item_idx in reversed(item_idx_to_remove):
            self.fraction_model.removeRows(item_idx, 1)

    def closeEvent(self, event):
        """
        overwrite of QDockWidget class to emit signal
        :param event: QEvent
        """
        self.on_close()
        event.accept()

    def highlight_feature(self, obj_id, obj_type, result_item: ThreeDiResultItem):

        for table_name, layer_id in result_item.parent().layer_ids.items():

            if obj_type == table_name:
                # query layer for object
                filt = u'"id" = {0}'.format(obj_id)
                request = QgsFeatureRequest().setFilterExpression(filt)
                lyr = QgsProject.instance().mapLayer(layer_id)
                features = lyr.getFeatures(request)
                for feature in features:
                    self.marker.setToGeometry(feature.geometry(), lyr)

    def unhighlight_all_features(self):
        """Remove the highlights from all layers"""
        self.marker.reset()

    def setup_ui(self):

        mainLayout = QHBoxLayout(self)
        self.setLayout(mainLayout)

        splitterWidget = QSplitter(self)

        # add plot
        self.fraction_plot = FractionPlot(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.fraction_plot.sizePolicy().hasHeightForWidth())
        self.fraction_plot.setSizePolicy(sizePolicy)
        self.fraction_plot.setMinimumSize(QSize(250, 250))
        splitterWidget.addWidget(self.fraction_plot)

        # add widget for timeseries table and other controls
        legendWidget = QWidget(self)
        vLayoutTable = QVBoxLayout(self)
        legendWidget.setLayout(vLayoutTable)

        # add comboboxes
        self.ts_units_combo_box = QComboBox(self)
        self.ts_units_combo_box.insertItems(0, ["hrs", "mins", "s"])
        vLayoutTable.addWidget(self.ts_units_combo_box)
        vLayoutTable.setMargin(0)

        # add timeseries table
        self.fraction_table = FractionTable(self)
        self.fraction_table.hoverEnterRow.connect(self.highlight_feature)
        self.fraction_table.hoverExitAllRows.connect(self.unhighlight_all_features)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraction_table.sizePolicy().hasHeightForWidth())
        self.fraction_table.setSizePolicy(sizePolicy)
        self.fraction_table.setMinimumSize(QSize(250, 0))
        vLayoutTable.addWidget(self.fraction_table)
        splitterWidget.addWidget(legendWidget)
        mainLayout.addWidget(splitterWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)

    def time_units_change(self):
        time_units = self.ts_units_combo_box.currentText()
        self.fraction_plot.setLabel("bottom", "Time", time_units)
        self.fraction_plot.set_parameter(self.current_parameter, time_units)
        self.fraction_plot.plotItem.vb.menu.viewAll.triggered.emit()

    def get_feature_index(self, layer, feature):
        """
        get the id of the selected id feature
        :param layer: selected Qgis layer to be added
        :param feature: selected Qgis feature to be added
        :return: idx (integer)
        We can't do ``feature.id()``, so we have to pick something that we
        have agreed on. For now we have hardcoded the 'id' field as the
        default, but that doesn't mean it's always the case in the future
        when more layers are added!
        """
        idx = feature.id()
        if layer.dataProvider().name() in ["memory", "ogr"]:
            idx = feature["id"]
        return idx

    def set_fraction(self, layer: QgsVectorLayer, feature: QgsFeature) -> bool:
        """
        :param layer: layer of features
        :param feature: Qgis layer feature to be added
        :return: boolean: new objects are added
        """

        if not layer.objectName() in ("node", "cell"):
            msg = """Please select results from either the 'nodes' or 'cells' layer."""
            messagebar_message(TOOLBOX_MESSAGE_TITLE, msg, Qgis.Warning, 5.0)
            return False

        if len(self.model.get_results(checked_only=False)) == 0:
            logger.warning("No results loaded")
            return False

        # Retrieve summary of existing items in model (!= graph plots)
        new_idx = self.get_feature_index(layer, feature)
        result_items = self.model.get_results(checked_only=False)
        for result_item in result_items:
            # Check whether this result belongs to the selected grid
            if layer.id() in result_item.parent().layer_ids.values():
                self.fraction_model.set_fraction(new_idx, result_item)
                break
        
        return True
