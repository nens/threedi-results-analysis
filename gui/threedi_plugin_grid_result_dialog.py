from logging import getLogger
from pathlib import Path

from threedi_results_analysis.utils.constants import TOOLBOX_QGIS_SETTINGS_GROUP
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtWidgets import QAbstractItemView
from qgis.core import QgsSettings
from qgis.PyQt.QtGui import QStandardItemModel, QStandardItem
from threedi_results_analysis.utils.workingdir import list_local_schematisations
from threedi_results_analysis.utils.user_messages import pop_up_critical

logger = getLogger(__name__)

FORM_CLASS, _ = uic.loadUiType(
    Path(__file__).parent / 'threedi_plugin_grid_result_dialog.ui',
)


class ThreeDiPluginGridResultDialog(QtWidgets.QDialog, FORM_CLASS):
    grid_file_selected = pyqtSignal(str)
    result_file_selected = pyqtSignal(str)

    def __init__(self, parent):
        super(ThreeDiPluginGridResultDialog, self).__init__(parent)
        self.setupUi(self)

        self.gridQgsFileWidget.fileChanged.connect(self._select_grid)
        self.gridQgsFileWidget.setDefaultRoot(ThreeDiPluginGridResultDialog._get_dir())
        self.gridQgsFileWidget.lineEdit().setEnabled(False)
        self.addGridPushButton.clicked.connect(self._add_grid)

        self.resultQgsFileWidget.fileChanged.connect(self._select_result)
        self.resultQgsFileWidget.setDefaultRoot(ThreeDiPluginGridResultDialog._get_dir())
        self.resultQgsFileWidget.lineEdit().setEnabled(False)
        self.addResultPushButton.clicked.connect(self._add_result)

        self.tabWidget.currentChanged.connect(self._tabChanged)
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.header_labels = ["Schematisation", "Revision", "Simulation"]
        self.tableView.horizontalHeader().setStretchLastSection(True)

    @pyqtSlot(str)
    def _select_grid(self, input_gridadmin_h5_or_gpkg: str) -> None:

        if not input_gridadmin_h5_or_gpkg:
            self.gridQgsFileWidget.setFilePath("")
            self.addGridPushButton.setEnabled(False)
            return

        ThreeDiPluginGridResultDialog._set_dir(input_gridadmin_h5_or_gpkg)
        self.gridQgsFileWidget.setDefaultRoot(ThreeDiPluginGridResultDialog._get_dir())

        self.addGridPushButton.setEnabled(True)

    @pyqtSlot(str)
    def _select_result(self, input_result_nc: str) -> None:
        if not input_result_nc:
            self.resultQgsFileWidget.setFilePath("")
            self.addResultPushButton.setEnabled(False)
            return

        ThreeDiPluginGridResultDialog._set_dir(input_result_nc)
        self.resultQgsFileWidget.setDefaultRoot(ThreeDiPluginGridResultDialog._get_dir())

        self.addResultPushButton.setEnabled(True)

    @pyqtSlot()
    def _add_grid(self) -> None:
        self.addGridPushButton.setEnabled(False)
        self.grid_file_selected.emit(self.gridQgsFileWidget.filePath())

    @pyqtSlot()
    def _add_result(self) -> None:
        self.addResultPushButton.setEnabled(False)
        self.result_file_selected.emit(self.resultQgsFileWidget.filePath())

    @staticmethod
    def _get_dir() -> str:
        value = QgsSettings().value(TOOLBOX_QGIS_SETTINGS_GROUP + "/lastOpenDir")
        if value is None:
            return ""
        dir_path = Path(value)
        if not dir_path.is_dir():
            return ""
        return str(dir_path)

    @staticmethod
    def _set_dir(path: str) -> None:
        dir_path = Path(path).parent
        if dir_path.is_dir():
            QgsSettings().setValue(TOOLBOX_QGIS_SETTINGS_GROUP + "/lastOpenDir", str(dir_path))
        else:
            QgsSettings().remove(TOOLBOX_QGIS_SETTINGS_GROUP + "/lastOpenDir")

    @pyqtSlot(int)
    def _tabChanged(self, idx: int) -> None:
        if self.tabWidget.currentWidget() is self.threedi:

            # Repopulate the table
            self.model.clear()
            self.model.setHorizontalHeaderLabels(self.header_labels)
            threedi_working_dir = QgsSettings().value("threedi/working_dir", "")
            if not threedi_working_dir:
                pop_up_critical("3Di Models & Simulations working directory not yet set.")

            local_schematisations = list_local_schematisations(threedi_working_dir)
            for schematisation_id, local_schematisation in local_schematisations.items():
                # Iterate over revisions
                for revision_number, local_revision in local_schematisation.revisions.items():
                    # Iterate over results
                    for results in local_revision.results_dirs:
                        name_item = QStandardItem(local_schematisation.name)
                        name_item.setEditable(False)
                        revision_item = QStandardItem(str(revision_number))
                        revision_item.setEditable(False)
                        result_item = QStandardItem(results)
                        result_item.setEditable(False)
                        self.model.appendRow([name_item, revision_item, result_item])

        for i in range(len(self.header_labels)):
            self.tableView.resizeColumnToContents(i)
