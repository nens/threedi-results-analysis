from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from qgis.core import Qgis
from ThreeDiToolbox.threedi_plugin_model import ThreeDiGridItem, ThreeDiResultItem
from ThreeDiToolbox.utils.user_messages import messagebar_message, pop_up_critical
from ThreeDiToolbox.utils.constants import TOOLBOX_MESSAGE_TITLE
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
    grid_validated = pyqtSignal(ThreeDiGridItem)
    result_validated = pyqtSignal(ThreeDiResultItem)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @pyqtSlot(ThreeDiGridItem)
    def validate_grid(self, item: ThreeDiGridItem):
        item.setIcon(QIcon(":images/themes/default/mIconSuccess.svg"))
        self.grid_validated.emit(item)

    @pyqtSlot(ThreeDiResultItem)
    def validate_result(self, result_item: ThreeDiResultItem):
        result_item.setIcon(QIcon(":images/themes/default/mIndicatorBadLayer.svg"))

        def fail(msg):
            messagebar_message(TOOLBOX_MESSAGE_TITLE, msg, Qgis.Warning, 5.0)

        # Check correct file name
        results_path = result_item.path

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

        # Try to open accompanying aggregate results file
        aggregate_results_path = result_item.path.with_name("aggregate_results_3di.nc")
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

        # Any modern enough calc core adds a 'threedicore_version' atribute
        if "threedicore_version" not in results_h5.attrs:
            return fail("Result file is too old, please recalculate.")

        # Check whether corresponding grid item belongs to same model
        result_model_slug = results_h5.attrs['model_slug'].decode()
        grid_item = result_item.parent()
        assert isinstance(grid_item, ThreeDiGridItem)
        driver = ogr.GetDriverByName('GPKG')
        package = driver.Open(str(grid_item.path), True)
        grid_model_slug = package.GetMetadataItem('model_slug')

        logger.info(f"Comparing grid slug {grid_model_slug} to result slug {result_model_slug}")

        if result_model_slug is None or grid_model_slug is None:
            msg = "No model meta information in result or grid, skipping slug validation."
            messagebar_message(TOOLBOX_MESSAGE_TITLE, msg, Qgis.Warning, 5)
        elif result_model_slug != grid_model_slug:

            # Really wrong grid, find a grid with the right slug, if not available, abort with pop-up
            root_node = result_item.model().invisibleRootItem()
            for i in range(root_node.rowCount()):
                other_grid_item = root_node.child(i)

                package = ogr.GetDriverByName('GPKG').Open(str(other_grid_item.path), True)
                other_grid_model_slug = package.GetMetadataItem('model_slug')

                if result_model_slug == other_grid_model_slug:
                    logger.info("Found other corresponding grid with slug {other_grid_model_slug}, moving result to that grid.")

                    # Remove the result from the model and start the processing sequence all over
                    new_results_args = {"input_result_nc": result_item.path, "parent_item": other_grid_item, "text": result_item.text()}
                    result_item.model().remove_result(result_item)
                    return other_grid_item.model().add_result(**new_results_args)

            msg = "Result corresponds to different model than loaded grids, removed from Results Manager"
            result_item.model().remove_result(result_item)
            pop_up_critical(msg)
            return fail(msg)

        result_item.setIcon(QIcon(":images/themes/default/mIconSuccess.svg"))
        self.result_validated.emit(result_item)
