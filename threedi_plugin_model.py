from pathlib import Path
from cached_property import cached_property
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from ThreeDiToolbox.datasource.threedi_results import ThreediResult

import logging
import re

logger = logging.getLogger(__name__)


class ThreeDiGridItem(QStandardItem):
    """
    A model item for computation grids
    """
    def __init__(self, path, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = Path(path)
        self.setSelectable(True)
        self.setEditable(True)
        self.setText(text)
        self.layer_group = None
        # map from table name to layer id, required to check
        # whether a layer is already loaded
        self.layer_ids = {}


class ThreeDiResultItem(QStandardItem):
    """
    A model item for 3Di results.
    """
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = Path(path)
        self.setCheckable(True)
        self.setCheckState(0)

    @cached_property
    def threedi_result(self):
        # ThreediResult is a wrapper around a theedigrid's
        # netcdf support
        return ThreediResult(self.path)


class ThreeDiPluginModel(QStandardItemModel):
    """
    The datamodel of the Toolbox.

    All grids and results are stored in this
    hierarchical model as items. The model itself does not contain much
    functionality, it merely keeps track of the grids and results and emits
    signals when the model is modified.

    Serialization of the model to XML can be done via read() and write()
    """
    grid_added = pyqtSignal(ThreeDiGridItem)
    result_added = pyqtSignal(ThreeDiResultItem)
    result_checked = pyqtSignal(ThreeDiResultItem)
    result_unchecked = pyqtSignal(ThreeDiResultItem)
    result_selected = pyqtSignal(ThreeDiResultItem)
    result_deselected = pyqtSignal(ThreeDiResultItem)
    result_changed = pyqtSignal(ThreeDiResultItem)
    grid_selected = pyqtSignal(ThreeDiGridItem)
    grid_deselected = pyqtSignal(ThreeDiGridItem)
    grid_changed = pyqtSignal(ThreeDiGridItem)
    grid_removed = pyqtSignal(ThreeDiGridItem)
    result_removed = pyqtSignal(ThreeDiResultItem)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemChanged.connect(self._item_changed)

    @pyqtSlot(str)
    def add_grid(self, input_gridadmin_h5_or_gpkg: str, text: str = "", layer_ids=None) -> ThreeDiGridItem:
        """Adds a grid item to the model, emits grid_added"""
        parent_item = self.invisibleRootItem()
        path_h5_or_gpkg = Path(input_gridadmin_h5_or_gpkg)
        if self.contains(path_h5_or_gpkg, ignore_suffix=True):
            return

        grid_item = ThreeDiGridItem(path_h5_or_gpkg, text if text else self._resolve_grid_item_text(path_h5_or_gpkg))

        if layer_ids:
            grid_item.layer_ids = dict(layer_ids)  # Make an explicit copy

        parent_item.appendRow(grid_item)
        self.grid_added.emit(grid_item)

        logger.info(f"Number of grids: {self.number_of_grids()}")
        return grid_item

    @pyqtSlot(str, ThreeDiGridItem)
    def add_result(self, input_result_nc: str, parent_item: ThreeDiGridItem, text: str = "") -> ThreeDiResultItem:
        """Adds a result item to the parent grid item, emits result_added"""
        path_nc = Path(input_result_nc)
        if self.contains(path_nc):
            return

        result_item = ThreeDiResultItem(path_nc, text if text else self._resolve_result_item_text(path_nc))
        parent_item.appendRow(result_item)
        self.result_added.emit(result_item)

        logger.info(f"Number of results: {self.number_of_results()}")
        return result_item

    @pyqtSlot(ThreeDiGridItem)
    def remove_grid(self, item: ThreeDiGridItem) -> bool:
        """Removes a grid from the model, emits grid_removed"""
        result = self.removeRows(self.indexFromItem(item).row(), 1)
        self.grid_removed.emit(item)
        return result

    @pyqtSlot(ThreeDiResultItem)
    def remove_result(self, item: ThreeDiResultItem) -> bool:
        """Removes a result from the model, emits result_removed"""
        grid_item = item.parent()
        assert isinstance(grid_item, ThreeDiGridItem)
        grid_item.removeRow(item.row())

        self.result_removed.emit(item)
        logger.info(f"Number of results: {self.number_of_results()}")
        return True

    def number_of_grids(self) -> int:
        """Return the number of grid items by doing a full traversal."""
        return self._number_of_type(self.invisibleRootItem(), ThreeDiGridItem)

    def number_of_results(self) -> int:
        """Return the number of result items by doing a full traversal."""
        return self._number_of_type(self.invisibleRootItem(), ThreeDiResultItem)

    def _number_of_type(self, item, type) -> int:
        count = 0
        if isinstance(item, type):
            count += 1

        for i in range(item.rowCount()):
            count += self._number_of_type(item.child(i), type)
        return count

    @pyqtSlot()
    def clear(self, emit: bool = True) -> None:
        """Removes all items from the model.

        Traverses through the three top-down, emits grid_removed and result_removed
        for each subsequent item (if emit is True), then clears the tree.
        """
        # Traverse and emit if desired
        if emit:
            self._clear_recursive(self.invisibleRootItem())
        # Clear the actual model
        super().clear()

    def _clear_recursive(self, item: QStandardItemModel):
        if isinstance(item, ThreeDiGridItem):
            self.grid_removed.emit(item)
        elif isinstance(item, ThreeDiResultItem):
            self.result_removed.emit(item)

        # Traverse into the children
        if item.hasChildren():
            for i in range(item.rowCount()):
                self._clear_recursive(item.child(i))

    def contains(self, path: Path, ignore_suffix: bool = False) -> bool:
        """Return if any item has a path attribute equal to path."""
        def _contains(item, path: Path, ignore_suffix: bool):
            if hasattr(item, "path"):
                p1, p2 = item.path, path
                if ignore_suffix:
                    p1, p2 = p1.with_suffix(""), p2.with_suffix("")
                if p1 == p2:
                    logger.warning(f"Item {path} was already added.")
                    return True
            return any(_contains(
                item=item.child(i),
                path=path,
                ignore_suffix=ignore_suffix
            ) for i in range(item.rowCount()))

        return _contains(
            item=self.invisibleRootItem(),
            path=path,
            ignore_suffix=ignore_suffix,
        )

    # @pyqtSlot(QStandardItem)
    def _item_changed(self, item: QStandardItem):
        if isinstance(item, ThreeDiResultItem):
            {
                2: self.result_checked, 0: self.result_unchecked,
            }[item.checkState()].emit(item)
            self.result_changed.emit(item)

            # Note that we not allow multiple results to be selected, deselect
            # the others in case an item is selected.
            assert item.parent()
            if item.checkState() == 2:
                for i in range(item.parent().rowCount()):
                    if item.parent().child(i) is not item:
                        item.parent().child(i).setCheckState(0)

        elif isinstance(item, ThreeDiGridItem):
            logger.info("Item data changed")
            self.grid_changed.emit(item)

    def select_item(self, index):
        logger.info("selected")
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

    def _resolve_result_item_text(self, file: Path) -> str:
        """The text of the result item depends on its containing file structure
        """
        if file.parent is not None:
            return file.parent.stem

        # Fallback
        return file.stem

    def _resolve_grid_item_text(self, file: Path) -> str:
        """The text of the grid item depends on its containing file structure

        In case the grid file is in the 3Di Models & Simulations local directory
        structure, the text should be schematisation name + revision nr. Otherwise just a number.
        """
        if file.parent.parent is not None and file.parent.parent.parent is not None:
            folder = file.parent
            if folder.stem == "grid":
                rev_folder = folder.parent
                return rev_folder.parent.stem + " " + ThreeDiPluginModel._retrieve_revision_str(rev_folder)

            folder = file.parent.parent
            if folder.stem == "results":
                rev_folder = folder.parent
                return rev_folder.parent.stem + " " + ThreeDiPluginModel._retrieve_revision_str(rev_folder)

        # Fallback
        return file.parent.stem

    @staticmethod
    def _retrieve_revision_str(path: Path) -> str:
        """Retrieves the revision number from the path."""
        rev_folder = str(path.stem)
        if rev_folder.endswith("work in progress") :
            return "(WIP)"

        version = re.match("^revision (\d+)$", rev_folder)
        if version is not None:
            return "#" + version.group(1)

        # Fallback
        return "(None)"
