from pathlib import Path
from cached_property import cached_property
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from qgis.PyQt.QtXml import QDomDocument, QDomElement
from ThreeDiToolbox.utils.constants import TOOLBOX_XML_ELEMENT_ROOT
from ThreeDiToolbox.datasource.threedi_results import ThreediResult

import logging
import re

logger = logging.getLogger(__name__)


class ThreeDiGridItem(QStandardItem):
    def __init__(self, path, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = Path(path)
        self.setSelectable(True)
        self.setEditable(True)
        self.setText(text)

        self._layer_group = None

    @property
    def layer_group(self):
        return self._layer_group

    @layer_group.setter
    def layer_group(self, value):
        if self._layer_group is None and value is not None:
            value.nameChanged.connect(self.update_text_from_layer_group)
        self._layer_group = value

    # @pyqtSlot(QgsLayerTreeGroup, str)
    def update_text_from_layer_group(self, layer_group, text):
        self.setText(text)


class ThreeDiResultItem(QStandardItem):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = Path(path)
        self.setCheckable(True)
        self.setCheckState(2)

    @cached_property
    def threedi_result(self):
        # ThreediResult is a wrapper around a theedigrid's
        # netcdf support
        return ThreediResult(self.path)


class ThreeDiPluginModel(QStandardItemModel):
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
            self.result_changed.emit(item)
        elif isinstance(item, ThreeDiGridItem):
            logger.info("Item data changed")
            self.grid_changed.emit(item)

    @pyqtSlot(str)
    def add_grid(self, input_gridadmin_h5_or_gpkg: str, text: str = "") -> ThreeDiGridItem:
        """Adds a grid item to the model, emits grid_added"""
        parent_item = self.invisibleRootItem()
        path_h5_or_gpkg = Path(input_gridadmin_h5_or_gpkg)
        if self.contains(path_h5_or_gpkg, ignore_suffix=True):
            return
        grid_item = ThreeDiGridItem(path_h5_or_gpkg, text if text else self._resolve_grid_item_text(path_h5_or_gpkg))
        parent_item.appendRow(grid_item)
        self.grid_added.emit(grid_item)
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
        return True

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

        self._grid_counter = 0

    def _clear_recursive(self, item: QStandardItemModel):
        if isinstance(item, ThreeDiGridItem):
            self.grid_removed.emit(item)
        elif isinstance(item, ThreeDiResultItem):
            self.result_removed.emit(item)

        # Traverse into the children
        if item.hasChildren():
            for i in range(item.rowCount()):
                self._clear_recursive(item.child(i))

    def read(self, doc: QDomDocument, resolver) -> bool:
        """Reads the model from the provided XML DomDocument

        Recursively traverses down the XML tree. Returns True
        on success. Resolver is used to convert between relative
        and absolute paths.
        """
        self.clear()

        # Find existing element corresponding to the result model
        results_nodes = doc.elementsByTagName(TOOLBOX_XML_ELEMENT_ROOT)

        if results_nodes.length() > 1:
            logger.error("XML file contains multiple toolbox root elements, aborting load.")
            return False
        elif results_nodes.length() == 0:
            return True  # Nothing to load

        results_node = results_nodes.at(0)
        assert results_node.parentNode() is not None

        # Now traverse through the XML tree and add model items
        if not self._read_recursive(results_node, self.invisibleRootItem(), resolver):
            logger.error("Unexpected XML item, aborting read")
            self.clear()
            return False

        return True

    def _read_recursive(self,  xml_parent: QDomElement, model_parent: QStandardItem, resolver) -> bool:
        child_xml_nodes = xml_parent.childNodes()

        for i in range(child_xml_nodes.count()):
            xml_node = child_xml_nodes.at(i)

            if xml_node.isElement():
                xml_element_node = xml_node.toElement()
                tag_name = xml_element_node.tagName()
                model_node = None
                if tag_name == "grid":
                    model_node = self.add_grid(
                        resolver.readPath(xml_element_node.attribute("path")),
                        xml_element_node.attribute("text"),
                    )
                elif tag_name == "result":
                    model_node = self.add_result(
                        resolver.readPath(xml_element_node.attribute("path")),
                        model_parent,
                        xml_element_node.attribute("text"),
                    )
                else:
                    logger.error("Unexpected XML item type, aborting read")
                    return False

                assert model_node is not None
                if not self._read_recursive(xml_node, model_node, resolver):
                    return False
            else:
                return False

        return True

    def write(self, doc: QDomDocument, resolver) -> bool:
        """Add the model to the provided XML DomDocument

        Recursively traverses down the model tree. Returns True
        on success. Resolver is used to convert between relative
        and absolute paths.
        """
        # Find and remove the existing element corresponding to the result model
        results_nodes = doc.elementsByTagName(TOOLBOX_XML_ELEMENT_ROOT)
        if results_nodes.length() == 1:
            results_node = results_nodes.at(0)
            assert results_node.parentNode() is not None
            results_node.parentNode().removeChild(results_node)

        # Create new results node under main (qgis) node
        qgis_nodes = doc.elementsByTagName("qgis")
        assert qgis_nodes.length() == 1 and qgis_nodes.at(0) is not None
        qgis_node = qgis_nodes.at(0)
        results_node = doc.createElement(TOOLBOX_XML_ELEMENT_ROOT)
        results_node = qgis_node.appendChild(results_node)
        assert results_node is not None

        # Traverse through the model and save the nodes
        if not self._write_recursive(doc, results_node, self.invisibleRootItem(), resolver):
            logger.error("Unable to write model")
            return False

        return True

    def _write_recursive(self, doc: QDomDocument, xml_parent: QDomElement, model_parent: QStandardItem, resolver) -> bool:
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
                    xml_node.setAttribute("path", resolver.writePath(str(model_node.path)))
                    xml_node.setAttribute("text", model_node.text())
                elif isinstance(model_node, ThreeDiResultItem):
                    xml_node.setTagName("result")
                    xml_node.setAttribute("path", resolver.writePath(str(model_node.path)))
                    xml_node.setAttribute("text", model_node.text())
                else:
                    logger.error("Unknown node type for serialization")
                    return False

                xml_node = xml_parent.appendChild(xml_node)
                assert xml_node is not None

                if not self._write_recursive(doc, xml_node, model_node, resolver):
                    return False

        return True

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
        if file.parent.parent is not None and file.parent.parent.parent is not None:
            if ThreeDiPluginModel._is_in_revision_folder(file):
                return file.parent.parent.parent.stem + ": " + ThreeDiPluginModel._retrieve_revision(file)

        text = str(self._grid_counter)
        self._grid_counter += 1
        return text

    @staticmethod
    def _resolve_result_item_text(file: Path) -> str:
        """The text of the result item is its parent folder
        """
        if file.parent is not None:
            return str(file.parent.stem)

        # Fallback
        return file.stem

    @staticmethod
    def _is_in_revision_folder(file: Path) -> bool:
        """Check if the file is in a 3Di revision folder."""
        logger.info(str(file))
        folder = file.parent.stem
        if folder not in ["results", "grid"]:
            return False

        rev_folder = file.parent.parent.stem
        logger.info(rev_folder)
        if rev_folder.endswith("work in progress") or rev_folder.startswith("revision "):
            return True

        return True

    @staticmethod
    def _retrieve_revision(file: Path) -> str:
        """Retrieves the revision number from the path."""
        rev_folder = str(file.parent.parent.stem)
        if rev_folder.endswith("work in progress") :
            return "work in progress"

        return re.match("^revision (\d+)$", rev_folder).group(1)
