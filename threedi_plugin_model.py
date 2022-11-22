from pathlib import Path
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from qgis.PyQt.QtXml import QDomDocument, QDomElement

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


class ThreeDiResultItem(QStandardItem):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = Path(path)
        self.setCheckable(True)
        self.setCheckState(2)


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
    def add_grid(self, input_gridadmin_h5_or_gpkg: str) -> ThreeDiGridItem:
        """Adds a grid item to the model, emits grid_added"""
        parent_item = self.invisibleRootItem()
        path_h5_or_gpkg = Path(input_gridadmin_h5_or_gpkg)
        grid_item = ThreeDiGridItem(path_h5_or_gpkg, self._resolve_grid_item_text(path_h5_or_gpkg))
        parent_item.appendRow(grid_item)
        self.grid_added.emit(grid_item)
        return grid_item

    @pyqtSlot(str)
    def add_result(self, input_result_nc: str) -> ThreeDiResultItem:
        """Adds a result item to the model, emits result_added"""
        # TODO add it under the right grid - inspect the paths?
        # BVB: Better to let user select parent node and do validation, I think
        parent_item = self.invisibleRootItem().child(0)
        path_nc = Path(input_result_nc)
        result_item = ThreeDiResultItem(path_nc, path_nc.stem)
        parent_item.appendRow(result_item)
        self.result_added.emit(result_item)
        return result_item

    @pyqtSlot(ThreeDiGridItem)
    def remove_grid(self, item: ThreeDiGridItem) -> bool:
        """Removes a grid from the model, emits grid_removed"""
        result = self.removeRows(self.indexFromItem(item).row(), 1)
        self.grid_removed.emit(item)
        return result

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

    def read(self, doc: QDomDocument) -> bool:
        self.clear()

        # Find existing element corresponding to the result model
        results_nodes = doc.elementsByTagName("threedi_result")

        if results_nodes.length() > 1:
            logger.error("XML file contains multiple threedi_result elements, aborting load.")
            return False
        elif results_nodes.length() == 0:
            return True  # Nothing to load

        results_node = results_nodes.at(0)
        assert results_node.parentNode() is not None

        # Now traverse through the XML tree and add model items
        return self._read_recursive(results_node, self.invisibleRootItem())

    def _read_recursive(self,  xml_parent: QDomElement, model_parent: QStandardItem) -> bool:
        child_xml_nodes = xml_parent.childNodes()

        for i in range(child_xml_nodes.count()):
            xml_node = child_xml_nodes.at(i)

            if xml_node.isElement():
                tag_name = xml_node.toElement().tagName()
                if tag_name == "grid":
                    # Create model item
                    model_node = self.add_grid(xml_node.toElement().attribute("path"))
                    self._read_recursive(xml_node, model_node)
            else:
                logger.error("Unexpected XML item, aborting read")
                self.clear()
                return False

        return True

    # @pyqtSlot(QDomDocument)
    def write(self, doc: QDomDocument) -> bool:
        # Find and remove the existing element corresponding to the result model
        results_nodes = doc.elementsByTagName("threedi_result")
        if results_nodes.length() == 1:
            results_node = results_nodes.at(0)
            assert results_node.parentNode() is not None
            results_node.parentNode().removeChild(results_node)

        # Create new results node under main (qgis) node
        qgis_nodes = doc.elementsByTagName("qgis")
        assert qgis_nodes.length() == 1 and qgis_nodes.at(0) is not None
        qgis_node = qgis_nodes.at(0)
        results_node = doc.createElement("threedi_result")
        results_node = qgis_node.appendChild(results_node)
        assert results_node is not None

        # Traverse through the model and save the nodes
        return self._write_recursive(doc, results_node, self.invisibleRootItem())

    def _write_recursive(self, doc: QDomDocument, xml_parent: QDomElement, model_parent: QStandardItem) -> bool:
        # Something is wrong when exactly one of them is None
        assert not (bool(xml_parent is not None) ^ bool(model_parent is not None))

        # Iterate over model child nodes and continue recursive traversion
        if model_parent.hasChildren():
            for i in range(model_parent.rowCount()):
                model_node = model_parent.child(i)
                xml_node = doc.createElement("temp")  # tag required

                # Populate the new xml_node with the info from model_node
                if isinstance(model_node, ThreeDiGridItem):
                    xml_node.setTagName("grid")
                    xml_node.setAttribute("path", str(model_node.path))
                elif isinstance(model_node, ThreeDiResultItem):
                    xml_node.setTagName("result")
                else:
                    logger.error("Unknown node type for serialization")
                    return False

                xml_node = xml_parent.appendChild(xml_node)
                assert xml_node is not None

                self._write_recursive(doc, xml_node, model_node)

        return True

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
