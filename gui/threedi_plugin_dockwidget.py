from logging import getLogger
from pathlib import Path

from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem
from threedi_results_analysis.utils.constants import TOOLBOX_QGIS_SETTINGS_GROUP
from threedi_results_analysis.gui.threedi_plugin_grid_result_dialog import ThreeDiPluginGridResultDialog
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import QModelIndex
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.core import QgsSettings
from qgis.PyQt.QtGui import QPixmap
from threedi_results_analysis import PLUGIN_DIR

logger = getLogger(__name__)

FORM_CLASS, _ = uic.loadUiType(
    Path(__file__).parent / 'gui' / 'threedi_plugin_dockwidget_base.ui',
)


class ThreeDiPluginDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    grid_file_selected = pyqtSignal(str)
    result_file_selected = pyqtSignal(str, ThreeDiGridItem)
    remove_current_index_clicked = pyqtSignal(QModelIndex)

    item_selected = pyqtSignal(QModelIndex)
    item_deselected = pyqtSignal(QModelIndex)

    def __init__(self, parent):
        super(ThreeDiPluginDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_Add.clicked.connect(self._add_clicked)
        self.pushButton_AddResult.clicked.connect(self._add_result_clicked)
        self.pushButton_RemoveItem.clicked.connect(self._remove_current_index_clicked)

        # Set logo
        path_3di_logo = str(PLUGIN_DIR / "icons" / "icon.png")
        logo_3di = QPixmap(path_3di_logo)
        logo_3di = logo_3di.scaledToHeight(30)
        self.logo.setPixmap(logo_3di)

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
        dialog = ThreeDiPluginGridResultDialog(self)
        # Connect signal to signal
        dialog.grid_file_selected.connect(self.grid_file_selected)

        def _get_current_grid() -> ThreeDiGridItem:
            logger.error("Retrieving current grid")
            index = self.treeView.selectionModel().currentIndex()
            if index is None:
                logger.warning("No current index in model")
                return None

            item = self.treeView.model().itemFromIndex(index)
            if not isinstance(item, ThreeDiGridItem):
                logger.warning(f"No grid item at index {index}")
                return None

            return item

        dialog.result_file_selected.connect(lambda path: self.result_file_selected.emit(path, _get_current_grid()))
        dialog.exec()

    def _add_result_clicked(self):
        index = self.treeView.selectionModel().currentIndex()
        if index is None:
            logger.warning("No current index in model")
            return

        item = self.treeView.model().itemFromIndex(index)
        if not isinstance(item, ThreeDiGridItem):
            logger.warning(f"No grid item at index {index}")
            return

        dialog = ThreeDiPluginGridResultDialog(self)
        dialog.result_file_selected.connect(lambda path, grid_item=item: self.result_file_selected.emit(path, grid_item))
        dialog.exec()

    def _remove_current_index_clicked(self):
        # not that index is the "current", not the "selected"
        index = self.treeView.selectionModel().currentIndex()
        if index is not None:
            self.remove_current_index_clicked.emit(index)

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
        self.setVisible(not self.isVisible())

    @pyqtSlot(ThreeDiGridItem)
    def expand_grid(self, item: ThreeDiGridItem):
        index = self.treeView.model().indexFromItem(item)
        self.treeView.expand(index)
        selection_model = self.treeView.selectionModel()
        # Deselect other grids
        selection_model.clearSelection()

        selection_model.setCurrentIndex(index, selection_model.SelectCurrent)
