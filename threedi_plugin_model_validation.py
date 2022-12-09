from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from .threedi_plugin_model import ThreeDiGridItem, ThreeDiResultItem
import h5py

import logging
logger = logging.getLogger(__name__)


class ThreeDiPluginModelValidator(QObject):
    grid_validated = pyqtSignal(ThreeDiGridItem, bool)
    result_validated = pyqtSignal(ThreeDiResultItem, bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @pyqtSlot(ThreeDiGridItem)
    def validate_grid(self, item: ThreeDiGridItem):
        item.setIcon(QIcon(":images/themes/default/mIconSuccess.svg"))
        self.grid_validated.emit(item, True)

    @pyqtSlot(ThreeDiResultItem)
    def validate_result(self, item: ThreeDiResultItem):
        item.setIcon(QIcon(":images/themes/default/mIndicatorBadLayer.svg"))

        if not item.path.name == "results_3di.nc":
            logger.error("Unexpected file name for results file")
            self.result_validated.emit(item, False)
            return

        # For validation, just load the file
        try:
            h5py.File(item.path, "r")
        except Exception:
            logger.error("Unable to load file")
            self.result_validated.emit(item, False)
            return

        # It is assumed that the aggregate_results_3di file is located in the same directory
        try:
            h5py.File(item.path.with_name("aggregate_results_3di.nc"), "r")
        except Exception:
            logger.error("Unable to load aggregate results file")
            self.result_validated.emit(item, False)
            return

        item.setIcon(QIcon(":images/themes/default/mIconSuccess.svg"))
        self.result_validated.emit(item, True)
