from pathlib import Path
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from qgis.PyQt.QtXml import QDomDocument

import logging
import os

logger = logging.getLogger(__name__)


class ThreeDiGridItem(QStandardItem):
    def __init__(self, path, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = Path(path)
        self.layer_group = None

        self.setSelectable(True)
        self.setEditable(True)
        self.setText(text)
        self.setRowCount(1)


class ThreeDiResultItem(QStandardItem):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = Path(path)
        self.setCheckable(True)
        self.setCheckState(2)
        self.setRowCount(1)


class ThreeDiPluginModel(QStandardItemModel):
    grid_added = pyqtSignal(ThreeDiGridItem)
    result_added = pyqtSignal(ThreeDiResultItem)
    result_checked = pyqtSignal(ThreeDiResultItem)
    result_unchecked = pyqtSignal(ThreeDiResultItem)
    result_selected = pyqtSignal(ThreeDiResultItem)
    result_deselected = pyqtSignal(ThreeDiResultItem)
    grid_selected = pyqtSignal(ThreeDiGridItem)
    grid_deselected = pyqtSignal(ThreeDiGridItem)
    grid_removed = pyqtSignal(ThreeDiGridItem)
    result_removed = pyqtSignal(ThreeDiResultItem)

    # Counter for label (needs to be set when model is loaded)
    _grid_counter = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemChanged.connect(self.item_changed)

    # @pyqtSlot(QStandardItem)
    def item_changed(self, item: QStandardItem):
        if isinstance(item, ThreeDiResultItem):
            {
                2: self.result_checked, 0: self.result_unchecked,
            }[item.checkState()].emit(item)
        elif isinstance(item, ThreeDiGridItem):
            logger.info("Item data changed")

    @pyqtSlot(str)
    def add_grid(self, input_gridadmin_h5_or_gpkg: str) -> bool:
        """Adds a grid item to the model, emits grid_added"""
        parent_item = self.invisibleRootItem()
        path_h5_or_gpkg = Path(input_gridadmin_h5_or_gpkg)
        grid_item = ThreeDiGridItem(path_h5_or_gpkg, self._resolve_grid_item_text(path_h5_or_gpkg))
        parent_item.appendRow(grid_item)
        self.grid_added.emit(grid_item)
        return True

    @pyqtSlot(str)
    def add_result(self, input_result_nc: str) -> bool:
        """Adds a result item to the model, emits result_added"""
        # TODO add it under the right grid - inspect the paths?
        # BVB: Better to let user select parent node and do validation, I think
        parent_item = self.invisibleRootItem().child(0)
        path_nc = Path(input_result_nc)
        result_item = ThreeDiResultItem(path_nc, path_nc.stem)
        parent_item.appendRow(result_item)
        self.result_added.emit(result_item)
        return True

    @pyqtSlot(ThreeDiGridItem)
    def remove_grid(self, item: ThreeDiGridItem) -> bool:
        """Removes a grid from the model, emits grid_removed"""
        result = self.removeRows(self.indexFromItem(item).row(), 1)
        self.grid_removed.emit(item)
        return result

    @pyqtSlot()
    def clear(self) -> None:
        """Removes all items from the model.

        Traverses through the three top-down, emits grid_removed and result_removed
        for each subsequent item, the clears the tree.
        """
        # Traverse and emit
        self._clear_recursive(self.invisibleRootItem())
        # Clear the actual model
        super().clear()

    # @pyqtSlot(QDomDocument)
    def write(self, doc: QDomDocument) -> bool:
        # todo: clear existing model from the doc
        # todo: write current model to the doc
        return True

    def _clear_recursive(self, item: QStandardItemModel):
        if isinstance(item, ThreeDiGridItem):
            self.grid_removed.emit(item)
        elif isinstance(item, ThreeDiResultItem):
            self.result_removed.emit(item)

        # Traverse into the children
        if item.hasChildren():
            for i in range(item.rowCount()):
                self._clear_recursive(item.child(i))

    def select_item(self, index):
        item = self.itemFromIndex(index)
        if isinstance(item, ThreeDiGridItem):
            self.grid_selected.emit(item)
        elif isinstance(item, ThreeDiResultItem):
            self.result_selected.emit(item)

    def deselect_item(self, index):
        item = self.itemFromIndex(index)
        if isinstance(item, ThreeDiGridItem):
            self.grid_deselected.emit(item)
        elif isinstance(item, ThreeDiResultItem):
            self.result_selected.emit(item)

    def _resolve_grid_item_text(self, file: Path) -> str:
        """The text of the grid item depends on its containing file structure

        In case the grid file is in the 3Di Models & Simulations local directory
        structure, the text should be schematisation name + revision nr. Otherwise just a number.
        """
        logger.info(str(file.parent.parent.parent))
        if file.parent.parent is not None and file.parent.parent.parent is not None:
            if ThreeDiPluginModel._is_revision_folder(str(file.parent.parent)):
                return file.parent.parent.parent.stem + ": " + file.parent.parent.stem

        text = str(self._grid_counter)
        self._grid_counter += 1
        return text

    @staticmethod
    def _is_revision_folder(revision_dir: str) -> bool:
        """Check if all revision subpaths are present."""
        logger.info(str(revision_dir))
        paths = [
            os.path.join(revision_dir, "admin"),
            os.path.join(revision_dir, "grid"),
            os.path.join(revision_dir, "results"),
            os.path.join(revision_dir, "schematisation"),
            os.path.join(revision_dir, "schematisation", "rasters"),
        ]

        return all(os.path.exists(p) if p else False for p in paths)
