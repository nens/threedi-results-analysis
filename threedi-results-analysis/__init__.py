
from .plugin import ThreediResultsAnalysisPlugin


def classFactory(iface):
    return ThreediResultsAnalysisPlugin(iface)


