from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt.QtXml import QDomElement
from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem
from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem
from typing import Callable
from typing import Dict
from typing import Tuple


class ThreeDiPluginTool(QObject):
    """
    The base class of each tool
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def write(self, doc: QDomDocument, elem: QDomElement) -> bool:
        """Called when a QGS project is written, allowing each tool to presist
        additional info int the dedicated xml tools node."""

        return True

    def read(self, _: QDomElement) -> bool:
        """Called when a QGS project is read, allowing each tool to read
        additional info from the dedicated xml tools node."""

        return True

    def on_unload(self):
        """Called when the plugin is unloaded. Tool can cleanup necessary items"""
        pass

    def get_custom_actions(self) -> Dict[QAction, Tuple[Callable[[ThreeDiGridItem], None], Callable[[ThreeDiResultItem], None]]]:
        """Called to retrieve the tool specific actions for the context-menu (right-button click) in Result Manager tree, including
         optional separators. Tool needs to provide an implementation for both a grid item and for a result item, e.g:

            @pyqtSlot(ThreeDiGridItem)
            def add_summary_grid(self, item:ThreeDiGridItem) -> None:
                logger.info(f"grid {item.id}")

            @pyqtSlot(ThreeDiResultItem)
            def add_summary_result(self, item:ThreeDiGridItem) -> None:
                logger.info(f"result {item.id}")

            def get_custom_actions(self) -> Dict[QAction, Tuple[Callable[[ThreeDiGridItem], None], Callable[[ThreeDiResultItem], None]]]:
                separator = QAction()
                separator.setSeparator(True)
                return {separator: (None, None),
                        QAction("Show flow summary"): (self.add_summary_grid, self.add_summary_result)
                }
        """
        return {}
