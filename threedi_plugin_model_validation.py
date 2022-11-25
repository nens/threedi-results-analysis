from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from .threedi_plugin_model import ThreeDiGridItem, ThreeDiResultItem


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
        self.result_validated.emit(item, True)
