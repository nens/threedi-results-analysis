from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtXml import QDomElement, QDomDocument
import logging

logger = logging.getLogger(__name__)


class ThreeDiPluginTool(QObject):
    """
    The base class of each tool
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def write(self, doc: QDomDocument, elem: QDomElement) -> bool:
        return True

    def on_unload(self):
        pass
