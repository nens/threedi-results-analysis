from qgis.PyQt.QtGui import QIcon

from qgis.core import QgsProcessingProvider

from .convert_to_gpkg import ThreeDiConvertToGpkgAlgorithm
from ..utils import icon_path


class ThreeDiResultsAnalysisProcessingProvider(QgsProcessingProvider):

    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(ThreeDiConvertToGpkgAlgorithm())

    def id(self, *args, **kwargs):
        return 'threedi-results-analysis'

    def name(self, *args, **kwargs):
        return self.tr('3Di Results Analysis')

    def icon(self):
        return QIcon(icon_path("threedi.svg"))
