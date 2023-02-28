from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot
from pathlib import Path
from qgis.core import Qgis, QgsVectorLayer
from threedi_results_analysis.threedi_plugin_model import ThreeDiGridItem, ThreeDiResultItem
from threedi_results_analysis.utils.user_messages import messagebar_message, pop_up_critical
from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel
from threedi_results_analysis.utils.constants import TOOLBOX_MESSAGE_TITLE
from threedi_results_analysis.utils.utils import listdirs
import h5py
import logging
logger = logging.getLogger(__name__)

MSG_TITLE = "3Di Results Manager"


class ThreeDiPluginModelValidator(QObject):
    """
    This class validates 3Di computation grid and result files. When
    a grid or result is valid, a signal is emited
    so listeners can handle accordingly.
    """
    grid_valid = pyqtSignal(ThreeDiGridItem)
    result_valid = pyqtSignal(ThreeDiResultItem, ThreeDiGridItem)
    grid_invalid = pyqtSignal(ThreeDiGridItem)
    result_invalid = pyqtSignal(ThreeDiResultItem, ThreeDiGridItem)

    def __init__(self, model: ThreeDiPluginModel, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    @pyqtSlot(str)
    def validate_grid(self, grid_file: str) -> ThreeDiGridItem:
        """
        Validates the grid and returns the new (or already existing) ThreeDiGridItem
        """
        new_item = ThreeDiGridItem(Path(grid_file), "")

        # Check whether model already contains this grid file.
        for i in range(self.model.invisibleRootItem().rowCount()):
            grid_item = self.model.invisibleRootItem().child(i)
            if grid_item.path.with_suffix("") == Path(grid_file).with_suffix(""):
                logger.warning("Model already contains this file")
                self.grid_invalid.emit(new_item)
                return grid_item

        # Note that in the 3Di M&S working directory setup, each results
        # folder in the revision can contain the same gridadmin file. Check
        # whether there is a grid loaded from one of these result folders.
        folder = Path(grid_file).parent
        if folder.parent.name == 'results':
            if str(folder.parent.parent.name).startswith('revision'):
                result_folders = [Path(d) for d in listdirs(folder.parent)]

                # Iterate over the grids
                for i in range(self.model.invisibleRootItem().rowCount()):
                    grid_item = self.model.invisibleRootItem().child(i)
                    assert isinstance(grid_item, ThreeDiGridItem)
                    grid_folder = Path(grid_item.path).parent
                    if grid_folder in result_folders:
                        logger.warning("Model already contains grid file from this revision.")
                        # Todo: should we do a simple shallow file-compare?
                        self.grid_invalid.emit(grid_item)
                        return grid_item

        self.grid_valid.emit(new_item)
        return new_item

    @pyqtSlot(str, str)
    def validate_result_grid(self, results_path: str, grid_path: str):
        """
        Validate the result, but first validate (and add) the grid.
        """
        grid_item = self.validate_grid(grid_path)
        if not grid_item:
            return

        # The grid should now be added, retrieve the corresponding grid from model and validate result
        self.validate_result(results_path, grid_item)

    @pyqtSlot(str, ThreeDiGridItem)
    def validate_result(self, results_path: str, grid_item: ThreeDiGridItem):
        logger.info(f"Validating result with grid item {grid_item.text()}")
        """
        Validate the result when added to the selected grid item.
        """
        def fail(msg):
            messagebar_message(TOOLBOX_MESSAGE_TITLE, msg, Qgis.Warning, 5.0)
            self.result_invalid.emit(result_item, grid_item)

        result_item = ThreeDiResultItem(Path(results_path))

        if self.model.contains(Path(results_path), True):
            return fail("Model already contains this file")

        # Check correct file name
        if not result_item.path.name == "results_3di.nc":
            return fail("Unexpected file name for results file")

        # Check opening with h5py, detects a.o. incomplete downloads
        try:
            results_h5 = h5py.File(result_item.path.open("rb"), "r")
        except OSError as error:
            if "truncated file" in str(error):
                return fail(
                    f"Results file {result_item.path} is incomplete. "
                    "If possible, copy or download it again."
                )
            return fail(f"Results file cannot be opened: {str(error.errno)} {str(error.strerror)} {str(error.args)}")

        # Try to open accompanying aggregate results file
        aggregate_results_path = result_item.path.with_name("aggregate_results_3di.nc")
        if aggregate_results_path.exists():
            try:
                h5py.File(aggregate_results_path.open("rb"), "r")
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

        grid_model_slug = ThreeDiPluginModelValidator.get_grid_slug(grid_item.path)

        logger.info(f"Comparing grid slug {grid_model_slug} to {result_model_slug}")

        if grid_model_slug is None or result_model_slug is None:
            msg = "No model meta information in result or grid, skipping slug validation."
            messagebar_message(TOOLBOX_MESSAGE_TITLE, msg, Qgis.Warning, 5)
        elif result_model_slug != grid_model_slug:
            # Really wrong grid, find a grid with the right slug, if not available, abort with pop-up
            root_node = grid_item.model().invisibleRootItem()
            for i in range(root_node.rowCount()):
                other_grid_item = root_node.child(i)
                other_grid_model_slug = ThreeDiPluginModelValidator.get_grid_slug(other_grid_item.path)

                if result_model_slug == other_grid_model_slug:
                    logger.info(f"Found other corresponding grid with slug {other_grid_model_slug}, setting that grid as parent.")

                    # Propagate the result with the new parent grid
                    return self.result_valid.emit(result_item, other_grid_item)

            msg = "Result corresponds to different model than loaded grids, removed from Results Manager"
            pop_up_critical(msg)
            return fail(msg)

        self.result_valid.emit(result_item, grid_item)

    @staticmethod
    def get_grid_slug(geopackage_path: Path) -> str:
        meta_layer = QgsVectorLayer(str(geopackage_path) + "|layername=meta", "meta", "ogr")

        if not meta_layer.isValid() or not (meta_layer.featureCount() == 1):
            logger.warning("Invalid, zero or more than 1 meta data table. Unable to derive slug")
            return None

        # Take first
        meta = next(meta_layer.getFeatures())
        return meta["model_slug"]
