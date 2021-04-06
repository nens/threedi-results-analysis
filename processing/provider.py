# See https://docs.qgis.org/3.10/en/docs/pyqgis_developer_cookbook/processing.html
from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from ThreeDiToolbox.processing.threedidepth_algorithm import ThreediDepth
from ThreeDiToolbox.processing.dwf_calculation_algorithm import DWFCalculatorAlgorithm


class ThreediProvider(QgsProcessingProvider):
    """Loads the Processing Toolbox algorithms for 3Di"""

    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(ThreediDepth())
        self.addAlgorithm(DWFCalculatorAlgorithm())
        # add additional algorithms here
        # self.addAlgorithm(MyOtherAlgorithm())

    def id(self, *args, **kwargs):
        """The ID of your plugin, used for identifying the provider.

        This string should be a unique, short, character only string,
        eg "qgis" or "gdal". This string should not be localised.
        """
        return 'threedi'

    def name(self, *args, **kwargs):
        """The human friendly name of your plugin in Processing.

        This string should be as short as possible (e.g. "Lastools", not
        "Lastools version 1.0.1 64-bit") and localised.
        """
        return self.tr('3Di')

    def icon(self):
        """Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        return QIcon(":/plugins/ThreeDiToolbox/icons/icon.png")
