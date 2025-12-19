# See https://docs.qgis.org/3.10/en/docs/pyqgis_developer_cookbook/processing.html
from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon
from threedi_results_analysis.processing.cross_sectional_discharge_algorithm import (
    CrossSectionalDischargeAlgorithm,
)
from threedi_results_analysis.processing.gpkg_conversion_algorithm import (
    ThreeDiConvertToGpkgAlgorithm,
)
from threedi_results_analysis.processing.grid_creation_algorithm import (
    ThreeDiGenerateCompGridAlgorithm,
)
from threedi_results_analysis.processing.leak_detector_algorithms import (
    DetectLeakingObstaclesAlgorithm,
)
from threedi_results_analysis.processing.leak_detector_algorithms import (
    DetectLeakingObstaclesWithDischargeThresholdAlgorithm,
)
from threedi_results_analysis.processing.rasters_to_netcdf_algorithm import (
    RastersToNetCDFAlgorithm,
)
from threedi_results_analysis.processing.schematisation_algorithms import (
    CheckSchematisationAlgorithm,
)
from threedi_results_analysis.processing.schematisation_algorithms import (
    ImportHydXAlgorithm,
)
from threedi_results_analysis.processing.schematisation_algorithms import (
    MigrateAlgorithm,
)
from threedi_results_analysis.processing.structure_control_action_algorithms import (
    StructureControlActionAlgorithm,
)
from threedi_results_analysis.processing.threedidepth_algorithms import (
    WaterDepthOrLevelSingleTimeStepAlgorithm,
)
from threedi_results_analysis.processing.threedidepth_algorithms import (
    WaterDepthOrLevelMultipleTimeStepAlgorithm,
)
from threedi_results_analysis.processing.threedidepth_algorithms import (
    WaterDepthOrLevelMaximumAlgorithm,
)
from threedi_results_analysis.processing.threedidepth_algorithms import (
    ConcentrationSingleTimeStepAlgorithm,
)
from threedi_results_analysis.processing.threedidepth_algorithms import (
    ConcentrationMultipleTimeStepAlgorithm,
)
from threedi_results_analysis.processing.threedidepth_algorithms import (
    ConcentrationMaximumAlgorithm,
)
from threedi_results_analysis.processing.water_depth_difference_algorithm import (
    WaterDepthDiffAlgorithm,
)


import os


class ThreediProvider(QgsProcessingProvider):
    """Loads the Processing Toolbox algorithms for Rana results analysis"""

    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(WaterDepthOrLevelSingleTimeStepAlgorithm())
        self.addAlgorithm(WaterDepthOrLevelMultipleTimeStepAlgorithm())
        self.addAlgorithm(WaterDepthOrLevelMaximumAlgorithm())
        self.addAlgorithm(ConcentrationSingleTimeStepAlgorithm())
        self.addAlgorithm(ConcentrationMultipleTimeStepAlgorithm())
        self.addAlgorithm(ConcentrationMaximumAlgorithm())
        self.addAlgorithm(CheckSchematisationAlgorithm())
        self.addAlgorithm(MigrateAlgorithm())
        self.addAlgorithm(ThreeDiConvertToGpkgAlgorithm())
        self.addAlgorithm(ThreeDiGenerateCompGridAlgorithm())
        self.addAlgorithm(CrossSectionalDischargeAlgorithm())
        self.addAlgorithm(DetectLeakingObstaclesAlgorithm())
        self.addAlgorithm(DetectLeakingObstaclesWithDischargeThresholdAlgorithm())
        self.addAlgorithm(RastersToNetCDFAlgorithm())
        self.addAlgorithm(StructureControlActionAlgorithm())
        self.addAlgorithm(ImportHydXAlgorithm())
        self.addAlgorithm(WaterDepthDiffAlgorithm())

    def id(self, *args, **kwargs):
        """The ID of your plugin, used for identifying the provider.

        This string should be a unique, short, character only string,
        eg "qgis" or "gdal". This string should not be localised.
        """
        return "threedi"

    def name(self, *args, **kwargs):
        """The human friendly name of your plugin in Processing.

        This string should be as short as possible (e.g. "Lastools", not
        "Lastools version 1.0.1 64-bit") and localised.
        """
        return self.tr("Rana Results Analysis")

    def icon(self):
        """Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons", "rana_blue_on_transparent.svg")
        return QIcon(icon_path)
