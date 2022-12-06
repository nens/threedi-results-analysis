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
        # for validation, just load the file
        try:
            h5py.File(item.path, "r")
        except Exception:
            # TODO: a non-existing file raises an OSError, not an IOError!
            item.setIcon(QIcon(":images/themes/default/mIndicatorBadLayer.svg"))
            self.result_validated.emit(item, True)
            return

        item.setIcon(QIcon(":images/themes/default/mIconSuccess.svg"))
        self.result_validated.emit(item, False)
