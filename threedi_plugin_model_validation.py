from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from .threedi_plugin_model import ThreeDiGridItem, ThreeDiResultItem
import h5py
from osgeo import ogr
import logging
logger = logging.getLogger(__name__)


class ThreeDiPluginModelValidator(QObject):
    grid_validated = pyqtSignal(ThreeDiGridItem, bool)
    result_validated = pyqtSignal(ThreeDiResultItem, bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @pyqtSlot(ThreeDiGridItem)
    def validate_grid(self, item: ThreeDiGridItem):
        item.setIcon(QIcon(":images/themes/default/mIconSuccess.svg"))
        self.grid_validated.emit(item, True)

    @pyqtSlot(ThreeDiResultItem)
    def validate_result(self, item: ThreeDiResultItem):
        item.setIcon(QIcon(":images/themes/default/mIndicatorBadLayer.svg"))

        # Check right file name
        if not item.path.name == "results_3di.nc":
            logger.error("Unexpected file name for results file")
            self.result_validated.emit(item, False)
            return

        # For validation, just load the file
        try:
            result = h5py.File(item.path, "r")

            # Check whether corresponding grid item belongs to same model
            result_model_slug = result.attrs['model_slug'].decode()
            grid_item = item.parent()
            assert isinstance(grid_item, ThreeDiGridItem)
            driver = ogr.GetDriverByName('GPKG')
            package = driver.Open(str(grid_item.path), True)
            grid_model_slug = package.GetMetadataItem('model_slug')

            if grid_model_slug is None:
                logger.warning("No model information in grid")

            if result_model_slug != grid_model_slug:
                logger.error("Result corresponds to different model than grid")
                self.result_validated.emit(item, False)
                return
        except Exception:
            logger.error("Unable to load file")
            self.result_validated.emit(item, False)
            return

        # It is assumed that the aggregate_results_3di file is located in the same directory
        try:
            h5py.File(item.path.with_name("aggregate_results_3di.nc"), "r")
        except Exception:
            logger.error("Unable to load aggregate results file")
            self.result_validated.emit(item, False)
            return

        item.setIcon(QIcon(":images/themes/default/mIconSuccess.svg"))
        self.result_validated.emit(item, True)
