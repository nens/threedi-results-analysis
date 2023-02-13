from pathlib import Path
from typing import List
from functools import cached_property
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtCore import QModelIndex, Qt
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from threedi_results_analysis.datasource.threedi_results import ThreediResult
from threedi_results_analysis.utils.layer_from_netCDF import get_or_create_cell_layer
from threedi_results_analysis.utils.layer_from_netCDF import get_or_create_flowline_layer
from threedi_results_analysis.utils.layer_from_netCDF import get_or_create_node_layer
from threedi_results_analysis.utils.layer_from_netCDF import get_or_create_pumpline_layer
from threedi_results_analysis.utils.user_messages import StatusProgressBar

import logging
import uuid

logger = logging.getLogger(__name__)

already_used_ids = []


def _generate_identifier() -> str:
    global already_used_ids
    while True:
        id = str(uuid.uuid4())
        if id not in already_used_ids:
            already_used_ids.append(id)
            return id


class ThreeDiModelItem(QStandardItem):
    """
    Base class for all model items
    """
    id: str  # uuid

    def __init__(self, *args, **kwargs):
        self.id = _generate_identifier()
        super().__init__(*args, **kwargs)


class ThreeDiGridItem(ThreeDiModelItem):
    """
    A model item for computation grids
    """
    def __init__(self, path: Path, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.setSelectable(True)
        self.setEditable(True)
        self.setText(text)

        # map from table name to layer id, required to check
        # whether a layer is already loaded
        self.layer_ids = {}

        # We only want signals when the text has been changed
        self._old_text = ""

        # layer info
        self.layer_group = None


class ThreeDiResultItem(ThreeDiModelItem):
    """
    A model item for 3Di results.
    """
    def __init__(self, path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.setCheckable(True)
        self.setCheckState(Qt.CheckState.Unchecked)

        # layer info
        # map of grid layers id to added result field names (tuple of ids)
        # (Two fields, initial_value and result, are required)
        # Used for cleaning up result fields when result is removed
        self._result_field_names = {}

        # Used to distinguish item changed and item checked
        self._old_text = ""

        # Used by Graph tool
        self._pattern = None # NOQA

        # TODO: temporary until anim tool has been refactored
        # The following four are caches for self.get_result_layers()
        self._line_layer = None
        self._node_layer = None
        self._cell_layer = None
        self._pumpline_layer = None

    @cached_property
    def threedi_result(self):
        # ThreediResult is a wrapper around a theedigrid's
        # netcdf support
        return ThreediResult(self.path)

    # TODO: temporary until anim tool has been refactored
    def get_result_layers(self, progress_bar=None):
        """Return QgsVectorLayers for line, node, and pumpline layers.

        Use cached versions (``self._line_layer`` and so) if present.

        """
        sqlite_gridadmin_filepath = str(self.path.parent / "gridadmin.sqlite")
        if progress_bar is None:
            progress_bar = StatusProgressBar(100, "3Di Toolbox")
        progress_bar.increase_progress(0, "Create flowline layer")
        self._line_layer = self._line_layer or get_or_create_flowline_layer(
            self.threedi_result, sqlite_gridadmin_filepath
        )
        progress_bar.increase_progress(25, "Create node layer")
        self._node_layer = self._node_layer or get_or_create_node_layer(
            self.threedi_result, sqlite_gridadmin_filepath
        )
        progress_bar.increase_progress(25, "Create cell layer")
        self._cell_layer = self._cell_layer or get_or_create_cell_layer(
            self.threedi_result, sqlite_gridadmin_filepath
        )
        progress_bar.increase_progress(25, "Create pumpline layer")
        self._pumpline_layer = self._pumpline_layer or get_or_create_pumpline_layer(
            self.threedi_result, sqlite_gridadmin_filepath
        )
        progress_bar.increase_progress(25, "Processing...")
        return [
            self._line_layer,
            self._node_layer,
            self._cell_layer,
            self._pumpline_layer,
        ]


class ThreeDiPluginModel(QStandardItemModel):
    """
    The datamodel of the Toolbox.

    All grids and results are stored in this
    hierarchical model as items. The model itself does not contain much
    functionality, it merely keeps track of the grids and results and emits
    signals when the model is modified.
    """
    grid_added = pyqtSignal(ThreeDiGridItem)
    result_added = pyqtSignal(ThreeDiResultItem)
    result_checked = pyqtSignal(ThreeDiResultItem)
    result_unchecked = pyqtSignal(ThreeDiResultItem)
    result_changed = pyqtSignal(ThreeDiResultItem)
    grid_changed = pyqtSignal(ThreeDiGridItem)
    grid_removed = pyqtSignal(ThreeDiGridItem)
    result_removed = pyqtSignal(ThreeDiResultItem)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(2)
        self.itemChanged.connect(self._item_changed)

    @pyqtSlot(ThreeDiGridItem)
    def add_grid(self, grid_item: ThreeDiGridItem) -> ThreeDiGridItem:
        """Adds a grid item to the model, emits grid_added"""
        if self.contains(grid_item.path, ignore_suffix=True):
            return None

        grid_item._old_text = grid_item.text()
        # if layer_ids:
        #    grid_item.layer_ids = dict(layer_ids)  # Make an explicit copy

        self.invisibleRootItem().appendRow(grid_item)
        self.grid_added.emit(grid_item)

        return grid_item

    @pyqtSlot(ThreeDiResultItem, ThreeDiGridItem)
    def add_result(self, result_item: ThreeDiResultItem, parent_item: ThreeDiGridItem) -> ThreeDiResultItem:
        """Adds a result item to the parent grid item, emits result_added"""
        if self.contains(result_item.path):
            return

        result_item._old_text = result_item.text()
        parent_item.appendRow([result_item, QStandardItem()])  # for result time
        self.result_added.emit(result_item)

        return result_item

    def _remove_grid(self, item: ThreeDiGridItem) -> bool:
        """Removes a grid from the model, emits grid_removed"""
        # Emit the removed signals for the node and its children
        self._clear_recursive(item)

        # Remove the actual grid
        return self.removeRows(self.indexFromItem(item).row(), 1)

    def _remove_result(self, item: ThreeDiResultItem) -> bool:
        """Removes a result from the model, emits result_removed"""
        grid_item = item.parent()
        assert isinstance(grid_item, ThreeDiGridItem)

        item.setCheckState(Qt.CheckState.Unchecked)
        self.result_removed.emit(item)
        grid_item.removeRow(item.row())

        return True

    @pyqtSlot(QModelIndex)
    def remove_index(self, index: QModelIndex) -> bool:
        """Removes a result from the model, emits result_removed"""
        item = self.itemFromIndex(index)
        if isinstance(item, ThreeDiGridItem):
            return self._remove_grid(item)
        if isinstance(item, ThreeDiResultItem):
            return self._remove_result(item)

    def get_results(self, checked_only: bool) -> List[ThreeDiResultItem]:
        """Returns the list of selected results (traversal)"""
        def _get_results(
            results: List[ThreeDiResultItem],
            item: QStandardItemModel,
            checked_only: bool
        ):
            if isinstance(item, ThreeDiResultItem):
                if checked_only:
                    if item.checkState() == Qt.CheckState.Checked:
                        results.append(item)
                else:
                    results.append(item)

            if item.hasChildren():
                for i in range(item.rowCount()):
                    _get_results(results, item.child(i), checked_only)

            return results

        results = []
        _get_results(results, self.invisibleRootItem(), checked_only)
        return results

    def get_result_field_names(self, layer_id):
        names = {
            f_name
            for result_item in self.get_results(checked_only=False)
            for l_id, f_names in result_item._result_field_names.items()
            for f_name in f_names
            if l_id == layer_id
        }
        return names

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
        self.setColumnCount(2)

    def _clear_recursive(self, item: QStandardItemModel):
        """Traverses through the subthree top-down, emits grid_removed and
        result_removed for each subsequent item"""
        if isinstance(item, ThreeDiGridItem):
            self.grid_removed.emit(item)
        elif isinstance(item, ThreeDiResultItem):
            item.setCheckState(Qt.CheckState.Unchecked)
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
        # Only signal changes in grid and result items
        if not isinstance(item, (ThreeDiGridItem, ThreeDiResultItem)):
            return

        # Distinguish changed and checked
        if item._old_text != item.text():
            item._old_text = item.text()
            if isinstance(item, ThreeDiResultItem):
                self.result_changed.emit(item)
                return
            self.grid_changed.emit(item)
            return

        if isinstance(item, ThreeDiGridItem):
            return

        # Item is a result item with a (possibly?) modified checkstate
        if item.checkState() == Qt.CheckState.Checked:
            # Note that we not allow multiple results to be checked,
            # first deselect the others in case an item is checked.
            for i in range(item.parent().rowCount()):
                other_item = item.parent().child(i)
                if other_item is item:
                    continue
                other_item.setCheckState(Qt.CheckState.Unchecked)
            self.result_checked.emit(item)
            return

        self.set_time_item(item)
        self.result_unchecked.emit(item)

    def set_time_item(self, result_item, text=''):
        result_index = self.indexFromItem(result_item)
        time_item = self.itemFromIndex(result_index.siblingAtColumn(1))
        time_item.setText(text)
