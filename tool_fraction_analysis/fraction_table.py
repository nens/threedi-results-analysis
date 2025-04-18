from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import QEvent
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QAbstractItemView
from qgis.PyQt.QtWidgets import QColorDialog
from qgis.PyQt.QtWidgets import QTableView
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem
from threedi_results_analysis.utils.widgets import PenStyleWidget

import logging


logger = logging.getLogger(__name__)


class FractionTable(QTableView):

    hoverExitRow = pyqtSignal(int)
    hoverExitAllRows = pyqtSignal()
    hoverEnterRow = pyqtSignal(int, str, ThreeDiResultItem)
    deleteRequested = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("QTreeView::item:hover{background-color:#FFFF00;}")
        self.setMouseTracking(True)
        self.verticalHeader().hide()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.model = None
        self._last_hovered_row = None
        self.viewport().installEventFilter(self)

    def on_close(self):
        """
        unloading widget and remove all required stuff
        :return:
        """
        self.setMouseTracking(False)
        self.viewport().removeEventFilter(self)

    def closeEvent(self, event):
        self.on_close()
        event.accept()

    def eventFilter(self, widget, event):
        if widget is self.viewport():
            if event.type() == QEvent.MouseMove:
                row = self.indexAt(event.pos()).row()
                if row == 0 and self.model and row > self.model.rowCount():
                    row = None

            elif event.type() == QEvent.Leave:
                row = None
                self.hoverExitAllRows.emit()
            else:
                row = self._last_hovered_row

            if row != self._last_hovered_row:
                if self._last_hovered_row is not None:
                    try:
                        self.hover_exit(self._last_hovered_row)
                    except IndexError:
                        logger.warning(
                            "Hover row index %s out of range" % self._last_hovered_row
                        )
                    # self.hoverExitRow.emit(self._last_hovered_row)
                # self.hoverEnterRow.emit(row)
                if row is not None:
                    try:
                        self.hover_enter(row)
                    except IndexError:
                        logger.warning("Hover row index %s out of range" % row)
                self._last_hovered_row = row
                pass
        return QTableView.eventFilter(self, widget, event)

    def hover_exit(self, row_nr):
        if row_nr >= 0:
            item = self.model.rows[row_nr]
            item.hover.value = False

    def hover_enter(self, row_nr):
        if row_nr >= 0:
            item = self.model.rows[row_nr]
            self.hoverEnterRow.emit(item.object_id.value, item.object_type.value, item.result.value)
            item.hover.value = True

    def setModel(self, model):
        super().setModel(model)
        self.model = model
        self.model.dataChanged.connect(self._update_table_widgets)
        self.model.rowsInserted.connect(self._update_table_widgets)
        self.model.rowsAboutToBeRemoved.connect(self._update_table_widgets)
        self.setVisible(False)
        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)
        self.setVisible(True)
        self.setColumnWidth(0, 20)  # checkbox

    def _update_table_widgets(self):
        return
        """The PenStyle widget is not part of the model, but explicitely added/overlayed to the table"""
        for i in range(self.model.rowCount()):
            item = self.model.rows[i]
            index = self.model.index(i, 1)
            pen_color = QColor(item.color.value[0], item.color.value[1], item.color.value[2])
            # If index widget A is replaced with index widget B, index widget A will be deleted.
            patternWidget = PenStyleWidget(item.result.value._pattern, pen_color, self)
            # patternWidget.setAutoFillBackground(True)
            patternWidget.setPalette(self.palette())
            self.setIndexWidget(index, patternWidget)
