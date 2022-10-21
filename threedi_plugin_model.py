from pathlib import Path


from qgis.PyQt.QtCore import pyqtSignal

# from PyQt5.QtGui import QStandardItem, QStandardItemModel
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel


class ThreeDiGridItem(QStandardItem):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = Path(path)


class ThreeDiResultItem(QStandardItem):
    pass


class ThreeDiPluginModel(QStandardItemModel):
    grid_item_added = pyqtSignal(ThreeDiGridItem)
    result_item_added = pyqtSignal(ThreeDiResultItem)

    def add_grid_file(self, input_gridadmin_h5: str) -> bool:
        """Converts h5 grid file to gpkg and add the layers to the project"""
        parent_item = self.invisibleRootItem()
        path_h5 = Path(input_gridadmin_h5)
        grid_item = ThreeDiGridItem(path_h5, path_h5.stem)
        parent_item.appendRow(grid_item)
        self.grid_item_added.emit(grid_item)
