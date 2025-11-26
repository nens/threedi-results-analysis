from pathlib import Path
from typing import Optional

from qgis.core import QgsSettings
from qgis.PyQt import uic
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import pyqtSignal, QItemSelectionModel
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtCore import QModelIndex
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtSvg import QSvgWidget
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QDockWidget
from qgis.PyQt.QtWidgets import QMenu, QPushButton, QHBoxLayout
from threedi_results_analysis import PLUGIN_DIR
from threedi_results_analysis.gui.threedi_plugin_grid_result_dialog import (
    ThreeDiPluginGridResultDialog,
)
from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem
from threedi_results_analysis.utils.constants import TOOLBOX_QGIS_SETTINGS_GROUP

import logging


logger = logging.getLogger(__name__)


FORM_CLASS, _ = uic.loadUiType(
    Path(__file__).parent / 'threedi_plugin_dockwidget_base.ui',
)


class ThreeDiPluginDockWidget(QDockWidget, FORM_CLASS):
    grid_file_selected = pyqtSignal(str)
    result_grid_file_selected = pyqtSignal([str, str])
    align_starts_checked = pyqtSignal(bool)

    grid_removal_selected = pyqtSignal(ThreeDiGridItem)
    result_removal_selected = pyqtSignal(ThreeDiResultItem)

    item_selected = pyqtSignal(QModelIndex)
    item_deselected = pyqtSignal(QModelIndex)

    def __init__(self, parent, iface):
        super(ThreeDiPluginDockWidget, self).__init__(parent)
        self.iface = iface

        self.first_show = True

        self.setupUi(self)
        self.toolButton_Add.clicked.connect(self._add_clicked)
        self.toolButton_RemoveItem.clicked.connect(self._remove_current_index_clicked)
        self.alignStartsCheckBox.stateChanged.connect(self._align_starts_clicked)

        # Set logo
        path_rana_logo = PLUGIN_DIR / "icons" / "banner.svg"
        self.replace_logo(svg_path=path_rana_logo, width=150)

        # Set button SVGs
        svg_path_icon_add = PLUGIN_DIR / "icons" / "icon_add.svg"
        self.toolButton_Add.setIcon(QIcon(str(svg_path_icon_add)))

        svg_path_icon_remove = PLUGIN_DIR / "icons" / "icon_remove.svg"
        self.toolButton_RemoveItem.setIcon(QIcon(str(svg_path_icon_remove)))

        # Replace any backslashes with slash to make QGIS happy when accessing a Windows network location.
        open_eye_logo = str(PLUGIN_DIR / "icons" / "open.png").replace("\\", "/")
        closed_eye_logo = str(PLUGIN_DIR / "icons" / "closed.png").replace("\\", "/")
        self.treeView.setStyleSheet(f"""QTreeView::indicator:unchecked {{image: url({closed_eye_logo});}}
                                    QTreeView::indicator:checked {{image: url({open_eye_logo});}}""")

        self.treeView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.customMenuRequested)

        # We'll make the dialog persistent so we can set some signals
        self.dialog = ThreeDiPluginGridResultDialog(self)
        # Map signal to signal
        self.dialog.grid_file_selected.connect(self.grid_file_selected)
        self.dialog.result_grid_file_selected.connect(self.result_grid_file_selected)

        self.custom_actions = {}

    def replace_logo(self, svg_path: Path | str, width: Optional[int] = None, height: Optional[int] = None):
        """
        QSvgWidgets are not supported in Qt designer, so we use a QLabel (self.logo) as a placeholder
        This function replaces self.logo with a QSvgWidget at the same position in the layout.
        """

        old_label = self.logo
        parent = old_label.parentWidget()
        layout = parent.layout()

        if layout is None:
            raise RuntimeError("self.logo is not inside a layout.")

        # Find index of the QLabel inside its layout
        index = None
        for i in range(layout.count()):
            if layout.itemAt(i).widget() is old_label:
                index = i
                break

        if index is None:
            raise RuntimeError("Could not find self.logo inside layout.")

        # Remove QLabel
        layout.removeWidget(old_label)
        old_label.deleteLater()

        # Create SVG widget
        svg_widget = QSvgWidget(str(svg_path))
        renderer = svg_widget.renderer()
        original_size = renderer.defaultSize()  # QSize
        if width is None:
            if height is None:
                raise ValueError("Either width or height must be specified.")
            width = int(original_size.width() / original_size.height() * height)
        elif height is None:
            height = int(original_size.height() / original_size.width() * width)
        svg_widget.setFixedWidth(width)
        svg_widget.setFixedHeight(height)

        # Insert SVG widget in the same layout slot
        layout.insertWidget(index, svg_widget)

        # Store reference if needed later
        self.logo = svg_widget

    def add_custom_actions(self, actions):
        self.custom_actions |= actions

    def customMenuRequested(self, pos):
        index = self.treeView.indexAt(pos)
        menu = QMenu(self)
        action_remove = QAction("Remove", self)
        action_remove.triggered.connect(lambda _, sel_index=index: self._remove_current_index_clicked(sel_index))
        menu.addAction(action_remove)

        for custom_action in self.custom_actions:
            if custom_action.isSeparator():
                menu.addSeparator()
                continue
            else:
                menu.addAction(custom_action)
            custom_action.triggered.disconnect()
            custom_action.triggered.connect(lambda _, sel_index=index: self._current_index_clicked(sel_index))

        menu.popup(self.treeView.viewport().mapToGlobal(pos))

    @pyqtSlot(QModelIndex)
    def _current_index_clicked(self, index=None):
        # note that index is the "current", not the "selected"
        if not index:
            index = self.treeView.selectionModel().currentIndex()
        if index is not None and index.isValid():
            item = self.treeView.model().itemFromIndex(index)
            action = self.sender()
            if isinstance(item, ThreeDiGridItem):
                self.custom_actions[action][0](item)
            elif isinstance(item, ThreeDiResultItem):
                self.custom_actions[action][1](item)
            else:
                raise RuntimeError("Unknown model item type")

    def _remove_current_index_clicked(self, index=None):
        # note that index is the "current", not the "selected"
        if not index:
            index = self.treeView.selectionModel().currentIndex()
        if index is not None and index.isValid():
            item = self.treeView.model().itemFromIndex(index)
            if isinstance(item, ThreeDiGridItem):
                self.grid_removal_selected.emit(item)
            elif isinstance(item, ThreeDiResultItem):
                self.result_removal_selected.emit(item)
            else:
                raise RuntimeError("Unknown model item type")

    def set_model(self, model):

        tree_view = self.treeView
        tree_view.setModel(model)

        tree_view.selectionModel().selectionChanged.connect(self._selection_changed)
        tree_view.setColumnWidth(1, 65)

        header = tree_view.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)
        header.setSectionResizeMode(1, header.ResizeMode.Fixed)

    def get_tools_widget(self):
        return self.toolWidget

    def _add_clicked(self):
        self.dialog.refresh()
        self.dialog.exec()

    def _align_starts_clicked(self):
        self.align_starts_checked.emit(self.alignStartsCheckBox.isChecked())

    def _selection_changed(self, selected, deselected):
        deselected_indexes = deselected.indexes()
        if deselected_indexes:
            self.item_deselected.emit(deselected_indexes[0])
        selected_indexes = selected.indexes()
        if selected_indexes:
            self.item_selected.emit(selected_indexes[0])

    def _get_dir(self) -> str:
        value = QgsSettings().value(TOOLBOX_QGIS_SETTINGS_GROUP + "/lastOpenDir")
        if value is None:
            return ""
        dir_path = Path(value)
        if not dir_path.is_dir():
            return ""
        return str(dir_path)

    def _set_dir(self, path: str):
        dir_path = Path(path).parent
        if dir_path.is_dir():
            QgsSettings().setValue(TOOLBOX_QGIS_SETTINGS_GROUP + "/lastOpenDir", str(dir_path))
        else:
            QgsSettings().remove(TOOLBOX_QGIS_SETTINGS_GROUP + "/lastOpenDir")

    @pyqtSlot()
    def toggle_visible(self, *args, **kwargs):
        # Add the dockwidget, tabified with any other right area dock widgets
        if self.first_show:
            main_window = self.iface.mainWindow()
            right_area_dock_widgets = [
                d for d in main_window.findChildren(QDockWidget)
                if main_window.dockWidgetArea(d) == Qt.DockWidgetArea.RightDockWidgetArea
                if d.isVisible()
            ] + [self]
            tabify_with = [right_area_dock_widgets[0].objectName()]
            for dock_widget in right_area_dock_widgets:
                self.iface.removeDockWidget(dock_widget)
                self.iface.addTabifiedDockWidget(
                    Qt.DockWidgetArea.RightDockWidgetArea, dock_widget, tabify_with, True
                )
            self.first_show = False
        else:
            self.setVisible(not self.isVisible())

    @pyqtSlot(ThreeDiGridItem)
    def expand_grid(self, item: ThreeDiGridItem):
        index = self.treeView.model().indexFromItem(item)
        self.treeView.expand(index)
        selection_model = self.treeView.selectionModel()
        # Deselect other grids
        selection_model.clearSelection()

        selection_model.setCurrentIndex(index, QItemSelectionModel.SelectionFlag.SelectCurrent)
