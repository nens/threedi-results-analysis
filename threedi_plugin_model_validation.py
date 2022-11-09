from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot
from .threedi_plugin_model import ThreeDiGridItem, ThreeDiResultItem

class ThreeDiPluginModelValidator(QObject):
    grid_item_validated = pyqtSignal(ThreeDiGridItem, bool)
    result_item_validated = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @pyqtSlot(ThreeDiGridItem)
    def grid_item_added(self, item: ThreeDiGridItem):
        import winsound
        winsound.Beep(2500, 1000)
        self.grid_item_validated.emit(item, True)

    @pyqtSlot(ThreeDiResultItem)
    def result_item_added(self, item: ThreeDiResultItem):
        self.result_item_validated.emit(item, True)
