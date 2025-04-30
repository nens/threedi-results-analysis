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

    hoverExitAllRows = pyqtSignal()
    hoverEnterRow = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("QTreeView::item:hover{background-color:#FFFF00;}")
        self.setMouseTracking(True)
        self.verticalHeader().hide()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
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
                index = self.indexAt(event.pos())
                row = index.row()
                if row != -1:
                    self.hoverEnterRow.emit()
                else:
                    self.hoverExitAllRows.emit()
            elif event.type() == QEvent.Leave:
                self.hoverExitAllRows.emit()
        return QTableView.eventFilter(self, widget, event)

    def setModel(self, model):
        super().setModel(model)
        self.model().dataChanged.connect(self._update_table_widgets)
        self.model().rowsInserted.connect(self._update_table_widgets)
        self.model().rowsAboutToBeRemoved.connect(self._update_table_widgets)
        self.horizontalHeader().setStretchLastSection(True)
        self.resizeColumnsToContents()
        self.setVisible(True)

    def _update_table_widgets(self):
        """The PenStyle widget is not part of the model, but explicitely added/overlayed to the table"""
        for row in range(self.model().rowCount()):
            style, color = self.model().item(row, 1).data()
            # If index widget A is replaced with index widget B, index widget A will be deleted.
            patternWidget = PenStyleWidget(style, QColor(*color), self)
            patternWidget.setPalette(self.palette())
            self.setIndexWidget(self.model().index(row, 1), patternWidget)
