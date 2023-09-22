from pathlib import Path
from qgis.core import QgsSettings
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import QModelIndex
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtCore import QSortFilterProxyModel
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtWidgets import QWidget
from threedi_schema import ThreediDatabase
from threedi_schema import errors
from ThreeDiToolbox.datasource.result_constants import LAYER_QH_TYPE_MAPPING
from ThreeDiToolbox.utils.user_messages import pop_up_info
from ThreeDiToolbox.utils.user_messages import pop_up_question
from ThreeDiToolbox.utils.utils import backup_sqlite

import logging
import os
import shutil

ui_file = Path(__file__).parent / "result_selection_view.ui"
FORM_CLASS, _ = uic.loadUiType(ui_file)

logger = logging.getLogger(__name__)

class ThreeDiResultSelectionWidget(QWidget, FORM_CLASS):
    """Dialog for selecting model (spatialite and result files netCDFs)

    TODO: actually, it is two dialogs in one: a selector of results and a
    separate downloader of results. They are not really connected. So
    splitting them makes the code simpler. And, more importantly, it makes the
    UI clearer.

    """

    closingDialog = pyqtSignal()

    def __init__(
        self,
        parent=None,
        iface=None,
        ts_datasources=None,
        tool=None,
    ):
        """Constructor

        :parent: Qt parent Widget
        :iface: QGiS interface
        :ts_datasources: TimeseriesDatasourceModel instance
        :downloadable_results: DownloadableResultModel instance
        :tool: the tool class which instantiated this widget. Is used
             here for storing volatile information
        """
        super().__init__(parent)

        self.tool = tool
        self.iface = iface
        self.setupUi(self)

        # set models on table views and update view columns
        self.ts_datasources = ts_datasources

        # connect signals
        self.closeButton.clicked.connect(self.close)
        self.selectModelSpatialiteButton.clicked.connect(
            self.select_model_spatialite_file
        )

        # set combobox list
        combo_list = [
            datasource for datasource in self.get_3di_spatialites_legendlist()
        ]

        if (
            self.ts_datasources.model_spatialite_filepath
            and self.ts_datasources.model_spatialite_filepath not in combo_list
        ):
            combo_list.append(self.ts_datasources.model_spatialite_filepath)

        if not self.ts_datasources.model_spatialite_filepath:
            combo_list.append("")

        self.modelSpatialiteComboBox.addItems(combo_list)

        if self.ts_datasources.model_spatialite_filepath:
            current_index = self.modelSpatialiteComboBox.findText(
                self.ts_datasources.model_spatialite_filepath
            )

            self.modelSpatialiteComboBox.setCurrentIndex(current_index)
        else:
            current_index = self.modelSpatialiteComboBox.findText("")
            self.modelSpatialiteComboBox.setCurrentIndex(current_index)

        self.modelSpatialiteComboBox.currentIndexChanged.connect(
            self.model_spatialite_change
        )

    def on_close(self):
        """
        Clean object on close
        """
        self.closeButton.clicked.disconnect(self.close)
        self.selectModelSpatialiteButton.clicked.disconnect(
            self.select_model_spatialite_file
        )
    def closeEvent(self, event):
        """
        Close widget, called by Qt on close
        :param event: QEvent, close event
        """
        self.closingDialog.emit()
        self.on_close()
        event.accept()

    def keyPressEvent(self, event):
        """Handle key press events on the widget."""
        # Close window if the Escape key is pressed
        if event.key() == Qt.Key_Escape:
            self.close()

    def get_3di_spatialites_legendlist(self):
        """
        Get list of spatialite data sources currently active in canvas
        :return: list of strings, unique spatialite paths
        """

        tdi_spatialites = []
        for layer in self.iface.layerTreeView().selectedLayers():
            if (
                layer.name() in list(LAYER_QH_TYPE_MAPPING.keys())
                and layer.dataProvider().name() == "spatialite"
            ):
                source = layer.dataProvider().dataSourceUri().split("'")[1]
                if source not in tdi_spatialites:
                    tdi_spatialites.append(source)

        return tdi_spatialites

    def model_spatialite_change(self, nr):
        """
        Change active modelsource. Called by combobox when selected
        spatialite changed
        :param nr: integer, nr of item selected in combobox
        """
        filepath = self.modelSpatialiteComboBox.currentText()
        logger.info("Different spatialite 3di model selected: %s", filepath)
        self.ts_datasources.model_spatialite_filepath = filepath
        # Just emitting some dummy model indices cuz what else can we do, there
        # is no corresponding rows/columns that's been changed
        self.ts_datasources.dataChanged.emit(QModelIndex(), QModelIndex())

    def select_model_spatialite_file(self):
        """
        Open file dialog on click on button 'load model'
        :return: Boolean, if file is selected
        """

        settings = QSettings("3di", "qgisplugin")

        try:
            init_path = settings.value("last_used_spatialite_path", type=str)
        except TypeError:
            logger.debug(
                "Last used datasource path is no string, setting it to our home dir."
            )
            init_path = os.path.expanduser("~")

        filepath, __ = QFileDialog.getOpenFileName(
            self, "Open 3Di model spatialite file", init_path, "Spatialite (*.sqlite)"
        )

        if filepath == "":
            return False

        model_checker_db = ThreediDatabase(filepath)
        schema = model_checker_db.schema
        try:
            schema.validate_schema()
            schema.set_spatial_indexes()
        except errors.MigrationMissingError:
            warn_and_ask_msg = (
                "The selected spatialite cannot be used because its database schema version is out of date. "
                "Would you like to migrate your spatialite to the current schema version?"
            )
            do_migration = pop_up_question(warn_and_ask_msg, "Warning")
            if not do_migration:
                return False
            backup_filepath = backup_sqlite(filepath)
            schema.upgrade(backup=False, upgrade_spatialite_version=True)
            schema.set_spatial_indexes()
            shutil.rmtree(os.path.dirname(backup_filepath))
        except errors.UpgradeFailedError:
            msg = (
                "There are errors in the spatialite. Please re-open this file in QGIS 3.16, run the model checker and "
                "fix error messages. Then attempt to upgrade again. For questions please contact the servicedesk."
            )
            pop_up_info(msg, "Warning")
            return False

        self.ts_datasources.spatialite_filepath = filepath
        index_nr = self.modelSpatialiteComboBox.findText(filepath)
        if index_nr < 0:
            self.modelSpatialiteComboBox.addItem(filepath)
            index_nr = self.modelSpatialiteComboBox.findText(filepath)

        self.modelSpatialiteComboBox.setCurrentIndex(index_nr)

        add_spatialite_connection(filepath, self.iface)
        settings.setValue("last_used_spatialite_path", os.path.dirname(filepath))
        return True

def add_spatialite_connection(spatialite_path, iface):
    """Add spatialite_path as a spatialite connection in the qgis-browser"""
    filename = os.path.basename(spatialite_path)
    QgsSettings().setValue(
        f"SpatiaLite/connections/{filename}/sqlitepath", spatialite_path
    )
    iface.reloadConnections()
