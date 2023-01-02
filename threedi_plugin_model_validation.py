from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from qgis.core import Qgis
from .threedi_plugin_model import ThreeDiGridItem, ThreeDiResultItem
from .utils.user_messages import messagebar_message
import h5py
from osgeo import ogr
import logging
logger = logging.getLogger(__name__)

MSG_TITLE = "3Di Results Manager"


class ThreeDiPluginModelValidator(QObject):
    """
    This class validates 3Di computation grid and result files. When
    validation is completed, a signal with the validation result is emited
    so listeners can handle accordingly.
    """
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

        def fail(msg):
            # logger.error(msg)
            messagebar_message(MSG_TITLE, msg, Qgis.Warning)
            self.result_validated.emit(item, False)

        # Check correct file name
        results_path = item.path

        if not results_path.name == "results_3di.nc":
            return fail("Unexpected file name for results file")

        # Check opening with h5py, detects a.o. incomplete downloads
        try:
            results_h5 = h5py.File(results_path, "r")
        except OSError as error:
            if "truncated file" in str(error):
                return fail(
                    f"Results file {results_path} is incomplete. "
                    "If possible, copy or download it again."
                )
            return fail("Results file cannot be opened.")

        # Any modern enough calc core adds a 'threedicore_version' atribute
        if "threedicore_version" not in results_h5.attrs:
            return fail("Result file is too old, please recalculate.")

        # Check whether corresponding grid item belongs to same model
        result_model_slug = results_h5.attrs['model_slug'].decode()
        grid_item = item.parent()
        assert isinstance(grid_item, ThreeDiGridItem)
        driver = ogr.GetDriverByName('GPKG')
        package = driver.Open(str(grid_item.path), True)
        grid_model_slug = package.GetMetadataItem('model_slug')

        if grid_model_slug is None:
            logger.warning("No model meta information in grid layer, skipping model validation.")
        elif result_model_slug != grid_model_slug:
            return fail("Result corresponds to different model than grid")

        # Try to open accompanying aggregate results file
        aggregate_results_path = item.path.with_name("aggregate_results_3di.nc")
        if aggregate_results_path.exists():
            try:
                h5py.File(aggregate_results_path, "r")
            except OSError as error:
                if "truncated file" in str(error):
                    return fail(
                        f"Aggregate results file {aggregate_results_path} "
                        "is incomplete. If possible, copy or download it "
                        "again."
                    )
                return fail("Aggregate results file cannot be opened.")

        item.setIcon(QIcon(":images/themes/default/mIconSuccess.svg"))
        self.result_validated.emit(item, True)
