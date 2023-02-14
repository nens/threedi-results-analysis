from logging import getLogger
from pathlib import Path

from threedi_results_analysis.utils.constants import TOOLBOX_QGIS_SETTINGS_GROUP
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.core import QgsSettings

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
        self.browseGridPushButton.clicked.connect(self._select_grid)
        self.browseResultPushButton.clicked.connect(self._select_result)
        self.addGridPushButton.clicked.connect(self._add_grid)
        self.addResultPushButton.clicked.connect(self._add_result)

    @pyqtSlot()
    def _select_grid(self):
        dir_path = ThreeDiPluginGridResultDialog._get_dir()
        input_gridadmin_h5_or_gpkg, _ = QFileDialog.getOpenFileName(
            self,
            "Load HDF5 or GeoPackage",
            dir_path,
            "HDF5 or GeoPackage (*.h5 *.gpkg)",
        )
        if not input_gridadmin_h5_or_gpkg:
            self.gridFileLineEdit.clear()
            self.addGridPushButton.setEnabled(False)
            return

        ThreeDiPluginGridResultDialog._set_dir(input_gridadmin_h5_or_gpkg)
        self.gridFileLineEdit.setText(input_gridadmin_h5_or_gpkg)
        self.addGridPushButton.setEnabled(True)

    @pyqtSlot()
    def _select_result(self):
        dir_path = self._get_dir()
        input_result_nc, _ = QFileDialog.getOpenFileName(
            self,
            "Load NetCDF",
            dir_path,
            "NetCDF (*.nc)"
        )
        if not input_result_nc:
            self.addResultPushButton.setEnabled(False)
            self.resultFileLineEdit.clear()
            return
        ThreeDiPluginGridResultDialog._set_dir(input_result_nc)
        self.resultFileLineEdit.setText(input_result_nc)
        self.addResultPushButton.setEnabled(True)

    @pyqtSlot()
    def _add_grid(self):
        self.addGridPushButton.setEnabled(False)
        self.grid_file_selected.emit(self.gridFileLineEdit.text())

    @pyqtSlot()
    def _add_result(self):
        self.addResultPushButton.setEnabled(False)
        self.result_file_selected.emit(self.resultFileLineEdit.text())

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
    def _set_dir(path: str):
        dir_path = Path(path).parent
        if dir_path.is_dir():
            QgsSettings().setValue(TOOLBOX_QGIS_SETTINGS_GROUP + "/lastOpenDir", str(dir_path))
        else:
            QgsSettings().remove(TOOLBOX_QGIS_SETTINGS_GROUP + "/lastOpenDir")
