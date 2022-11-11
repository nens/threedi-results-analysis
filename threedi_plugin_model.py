from pathlib import Path


from qgis.PyQt.QtCore import pyqtSignal

# from PyQt5.QtGui import QStandardItem, QStandardItemModel
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel


class ThreeDiGridItem(QStandardItem):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = Path(path)
        self.setSelectable(False)


class ThreeDiResultItem(QStandardItem):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = Path(path)
        self.setCheckable(True)
        self.setCheckState(2)


class ThreeDiPluginModel(QStandardItemModel):
    grid_item_added = pyqtSignal(ThreeDiGridItem)
    result_item_added = pyqtSignal(ThreeDiResultItem)
    result_item_checked = pyqtSignal(ThreeDiResultItem)
    result_item_unchecked = pyqtSignal(ThreeDiResultItem)
    result_item_selected = pyqtSignal(ThreeDiResultItem)
    result_item_deselected = pyqtSignal(ThreeDiResultItem)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemChanged.connect(self.item_changed)

    def item_changed(self, item):
        if not isinstance(item, ThreeDiResultItem):
            return
        {
            2: self.result_item_checked, 0: self.result_item_unchecked,
        }[item.checkState()].emit(item)

    def add_grid_file(self, input_gridadmin_h5_or_gpkg: str) -> bool:
        """Converts h5 grid file to gpkg and add the layers to the project"""
        parent_item = self.invisibleRootItem()
        path_h5_or_gpkg = Path(input_gridadmin_h5_or_gpkg)
        grid_item = ThreeDiGridItem(path_h5_or_gpkg, path_h5_or_gpkg.stem)
        parent_item.appendRow(grid_item)
        self.grid_item_added.emit(grid_item)

    def add_result_file(self, input_result_nc: str) -> bool:
        """Converts h5 grid file to gpkg and add the layers to the project"""
        # TODO add it under the right grid - inspect the paths?
        parent_item = self.invisibleRootItem().child(0)
        path_nc = Path(input_result_nc)
        result_item = ThreeDiResultItem(path_nc, path_nc.stem)
        parent_item.appendRow(result_item)
        self.result_item_added.emit(result_item)

    def select_result(self, index):
        self.result_item_selected.emit(self.itemFromIndex(index))

    def deselect_result(self, index):
        self.result_item_deselected.emit(self.itemFromIndex(index))