from qgis.core import QgsProcessingProvider
from .algorithms import CrossSectionalDischargeAlgorithm
from .leak_detector_algorithms import (
    DetectLeakingObstaclesAlgorithm,
    DetectLeakingObstaclesWithDischargeThresholdAlgorithm
)


class ThreeDiCustomStatisticsProvider(QgsProcessingProvider):
    """Loads the Processing Toolbox algorithms"""

    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)

    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(CrossSectionalDischargeAlgorithm())
        self.addAlgorithm(DetectLeakingObstaclesAlgorithm())
        self.addAlgorithm(DetectLeakingObstaclesWithDischargeThresholdAlgorithm())

    def id(self, *args, **kwargs):
        """The ID of your plugin, used for identifying the provider.

        This string should be a unique, short, character only string,
        eg "qgis" or "gdal". This string should not be localised.
        """
        return "threedi_custom_statistics"

    def name(self, *args, **kwargs):
        """The human friendly name of your plugin in Processing.

          This string should be as short as possible (e.g. "Lastools", not
        "Lastools version 1.0.1 64-bit") and localised.
        """
        return self.tr("3Di Custom Statistics")

    def icon(self):
        """Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        return QgsProcessingProvider.icon(self)
