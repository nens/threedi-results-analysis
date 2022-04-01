
from qgis.core import QgsApplication
from .processing_provider.threedi_processing_provider import ThreeDiResultsAnalysisProcessingProvider


class ThreediResultsAnalysisPlugin(object):
    def __init__(self, iface):
        self.iface = iface

    def initProcessing(self):
        self.provider = ThreeDiResultsAnalysisProcessingProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
