from qgis.PyQt.QtCore import QObject, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtXml import QDomDocument
from qgis.utils import iface
from qgis.core import QgsApplication, QgsDateTimeRange, QgsInterval, QgsProject, QgsPathResolver, QgsSettings
from ThreeDiToolbox.misc_tools import About
from ThreeDiToolbox.misc_tools import CacheClearer
from ThreeDiToolbox.misc_tools import ShowLogfile
from ThreeDiToolbox.misc_tools import ToggleResultsManager
from ThreeDiToolbox.processing.providers import ThreediProvider
from ThreeDiToolbox.threedi_plugin_dockwidget import ThreeDiPluginDockWidget
from ThreeDiToolbox.threedi_plugin_layer_manager import ThreeDiPluginLayerManager
from ThreeDiToolbox.threedi_plugin_model import ThreeDiPluginModel
from ThreeDiToolbox.threedi_plugin_model_validation import ThreeDiPluginModelValidator
from ThreeDiToolbox.threedi_plugin_model_serialization import ThreeDiPluginModelSerializer
from ThreeDiToolbox.tool_animation.map_animator import MapAnimator
from ThreeDiToolbox.tool_graph.graph import ThreeDiGraph
from ThreeDiToolbox.tool_result_selection.models import TimeseriesDatasourceModel
from ThreeDiToolbox.tool_result_selection.result_selection import ThreeDiResultSelection
from ThreeDiToolbox.tool_sideview.sideview import ThreeDiSideView
from ThreeDiToolbox.tool_statistics import StatisticsTool
from ThreeDiToolbox.tool_water_balance import WaterBalanceTool
from ThreeDiToolbox.tool_watershed.watershed_analysis import ThreeDiWatershedAnalyst
from ThreeDiToolbox.utils import color
from ThreeDiToolbox.utils.layer_tree_manager import LayerTreeManager
from ThreeDiToolbox.utils.qprojects import ProjectStateMixin
from datetime import datetime as Datetime
import numpy as np
import logging

logger = logging.getLogger(__name__)


class ThreeDiPlugin(QObject, ProjectStateMixin):
    """Main Plugin Class which register toolbar ad menu and add tools"""

    def __init__(self, iface):
        QObject.__init__(self)

        # Save reference to the QGIS interface
        self.iface = iface

        self.provider = None

    def initProcessing(self):
        """Create the Qgis Processing Toolbox provider and its algorithms

        Called by QGIS to check for processing algorithms.
        """
        self.provider = ThreediProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI.

        Called when the plugin is loaded.
        """
        self.model = ThreeDiPluginModel()
        self.loader = ThreeDiPluginLayerManager()
        self.validator = ThreeDiPluginModelValidator()

        QgsProject.instance().writeProject.connect(self.write)
        QgsProject.instance().readProject.connect(self.read)
        QgsProject.instance().removeAll.connect(self.model.clear)

        # Declare instance attributes
        self.actions = []
        self.menu = "&3Di toolbox"

        self.ts_datasources = TimeseriesDatasourceModel()

        # Set toolbar and init a few toolbar widgets
        self.toolbar = self.iface.addToolBar("ThreeDiToolbox")

        # Init the rest of the tools
        self.about_tool = About(iface)
        self.toggle_results_manager = ToggleResultsManager(iface, self)
        self.cache_clearer = CacheClearer(iface, self.ts_datasources)
        self.result_selection_tool = ThreeDiResultSelection(iface, self.ts_datasources)
        self.graph_tool = ThreeDiGraph(iface, self.model)
        self.sideview_tool = ThreeDiSideView(iface, self)
        self.stats_tool = StatisticsTool(iface, self.ts_datasources)
        self.water_balance_tool = WaterBalanceTool(iface, self.ts_datasources)
        self.watershed_tool = ThreeDiWatershedAnalyst(iface, self.ts_datasources)
        self.logfile_tool = ShowLogfile(iface)

        self.tools = [  # second item indicates enabled on startup
            (self.about_tool, True),
            (self.toggle_results_manager, True),
            (self.cache_clearer, True),
            (self.result_selection_tool, True),
            (self.graph_tool, False),
            (self.sideview_tool, True),
            (self.stats_tool, True),
            (self.water_balance_tool, True),
            (self.watershed_tool, True),
            (self.logfile_tool, True),
        ]

        self.layer_manager = LayerTreeManager(self.iface, self.ts_datasources)

        # Styling (TODO: can this be moved to where it is used?)
        for color_ramp in color.COLOR_RAMPS:
            color.add_color_ramp(color_ramp)

        for tool, enabled in self.tools:
            self._add_action(
                tool,
                tool.icon_path,
                text=tool.menu_text,
                callback=tool.run,
                parent=self.iface.mainWindow(),
                enabled_flag=enabled
            )

        assert not hasattr(self, "dockwidget")  # Should be destroyed on unload
        self.dockwidget = ThreeDiPluginDockWidget(None)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)

        # Connect the signals
        self.dockwidget.grid_file_selected.connect(self.model.add_grid)
        self.dockwidget.result_file_selected.connect(self.model.add_result)
        self.dockwidget.item_selected.connect(self.model.select_item)
        self.dockwidget.item_deselected.connect(self.model.deselect_item)
        self.dockwidget.remove_current_index_clicked.connect(self.model.remove_index)

        self.model.grid_added.connect(self.loader.load_grid)
        self.model.grid_added.connect(self.dockwidget.expand_grid)
        self.model.result_added.connect(self.loader.load_result)
        self.model.grid_removed.connect(self.loader.unload_grid)
        self.model.result_removed.connect(self.loader.unload_result)
        self.model.grid_changed.connect(self.loader.update_grid)
        self.model.result_changed.connect(self.loader.update_result)
        self.model.result_unchecked.connect(self.loader.result_unchecked)

        self.loader.grid_loaded.connect(self.validator.validate_grid)
        self.loader.result_loaded.connect(self.validator.validate_result)

        self.model.result_checked.connect(self._update_temporal_controller)
        self.model.result_unchecked.connect(self._update_temporal_controller)

        self.toggle_results_manager.triggered.connect(self.dockwidget.toggle_visible)

        self.ts_datasources.rowsRemoved.connect(self.check_status_model_and_results)
        self.ts_datasources.rowsInserted.connect(self.check_status_model_and_results)
        self.ts_datasources.dataChanged.connect(self.check_status_model_and_results)
        tc = iface.mapCanvas().temporalController()
        tc.updateTemporalRange.connect(self._temporal_update)

        self.dockwidget.show()
        self.dockwidget.set_model(self.model)

        self.initProcessing()

        self.map_animator = MapAnimator(self.dockwidget.get_tools_widget(), self.model)

        self.model.result_added.connect(self.map_animator.results_changed)
        self.model.result_removed.connect(self.map_animator.results_changed)
        self.model.result_checked.connect(self.map_animator.result_activated)
        self.model.result_unchecked.connect(self.map_animator.result_deactivated)

        self.model.result_added.connect(self.graph_tool.result_added)
        self.model.result_removed.connect(self.graph_tool.result_removed)
        self.model.result_checked.connect(self.graph_tool.result_activated)
        self.model.result_unchecked.connect(self.graph_tool.result_deactivated)

        self.init_state_sync()
        tc.setTemporalExtents(QgsDateTimeRange(Datetime(2020, 5, 17), Datetime.now()))

        # Disable warning that scratch layer data will be lost
        QgsSettings().setValue("askToSaveMemoryLayers", False, QgsSettings.App)

        self.check_status_model_and_results()

    def write(self, doc: QDomDocument) -> bool:
        # Resolver convert relative to absolute paths and vice versa
        resolver = QgsPathResolver(QgsProject.instance().fileName() if (QgsProject.instance().filePathStorage() == 1) else "")
        return ThreeDiPluginModelSerializer.write(self.model, doc, resolver)

    def read(self, doc: QDomDocument) -> bool:
        # Resolver convert relative to absolute paths and vice versa
        resolver = QgsPathResolver(QgsProject.instance().fileName() if (QgsProject.instance().filePathStorage() == 1) else "")
        return ThreeDiPluginModelSerializer.read(self.model, doc, resolver)

    def check_status_model_and_results(self, *args):
        """Check if a (new and valid) model or result is selected and react on
        this by pre-processing of things and activation/ deactivation of
        tools. function is triggered by changes in the ts_datasources
        args:
            *args: (list) the arguments provided by the different signals
        """

        # Enable/disable tools that depend on netCDF results.
        # For side views also the spatialite needs to be imported or else it
        # crashes with a segmentation fault
        if self.ts_datasources.rowCount() > 0:
            self.cache_clearer.action_icon.setEnabled(True)

        else:
            self.cache_clearer.action_icon.setEnabled(False)

        if (
            self.ts_datasources.rowCount() > 0
            and self.ts_datasources.model_spatialite_filepath is not None
        ):
            self.sideview_tool.action_icon.setEnabled(True)
            self.stats_tool.action_icon.setEnabled(True)
            self.water_balance_tool.action_icon.setEnabled(True)
        else:
            self.sideview_tool.action_icon.setEnabled(False)
            self.stats_tool.action_icon.setEnabled(False)
            self.water_balance_tool.action_icon.setEnabled(False)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI.

        Called then the plugin is unloaded.
        """

        # Stop animating
        tc = iface.mapCanvas().temporalController()
        tc.updateTemporalRange.disconnect(self._temporal_update)

        # Clears model and emits subsequent signals
        self.model.clear()

        # Disconnect all signals
        self.dockwidget.grid_file_selected.disconnect(self.model.add_grid)
        self.dockwidget.result_file_selected.disconnect(self.model.add_result)
        self.dockwidget.item_selected.disconnect(self.model.select_item)
        self.dockwidget.item_deselected.disconnect(self.model.deselect_item)
        self.dockwidget.remove_current_index_clicked.disconnect(self.model.remove_index)

        self.model.grid_added.disconnect(self.loader.load_grid)
        self.model.grid_added.disconnect(self.dockwidget.expand_grid)
        self.model.result_added.disconnect(self.loader.load_result)
        self.model.grid_removed.disconnect(self.loader.unload_grid)
        self.model.result_removed.disconnect(self.loader.unload_result)
        self.model.grid_changed.disconnect(self.loader.update_grid)
        self.model.result_changed.disconnect(self.loader.update_result)

        self.loader.grid_loaded.disconnect(self.validator.validate_grid)
        self.loader.result_loaded.disconnect(self.validator.validate_result)

        self.ts_datasources.rowsRemoved.disconnect(self.check_status_model_and_results)
        self.ts_datasources.rowsInserted.disconnect(self.check_status_model_and_results)
        self.ts_datasources.dataChanged.disconnect(self.check_status_model_and_results)

        # Clean up resources

        self.unload_state_sync()
        QgsApplication.processingRegistry().removeProvider(self.provider)

        for action in self.actions:
            self.iface.removePluginMenu("&3Di toolbox", action)
            self.iface.removeToolBarIcon(action)

        for tool, _ in self.tools:
            tool.on_unload()

        self.layer_manager.on_unload()

        self.iface.removeDockWidget(self.dockwidget)
        del self.dockwidget
        del self.toolbar

    def _update_temporal_controller(self, *args):
        results = self.model.get_selected_results()
        tc = iface.mapCanvas().temporalController()
        if not results:
            return

        logger.info("Updating temporal controller")
        # gather info
        threedi_results = [r.threedi_result for r in results]
        datetimes = [
            np.array(tr.dt_timestamps, dtype='datetime64[s]')
            for tr in threedi_results
        ]

        # frame duration
        intervals = [
            round((d[1:] - d[:-1]).min().item().total_seconds())
            for d in datetimes
            if d.size >= 2
        ]
        frame_duration = max(1, min(intervals)) if intervals else 1
        tc.setFrameDuration(QgsInterval(frame_duration))
        logger.info(f"frame_duration {frame_duration}")

        # extent
        start_time = min(d[0].item() for d in datetimes)
        end_time = max(d[-1].item() for d in datetimes)
        tc.setTemporalExtents(QgsDateTimeRange(start_time, end_time, True, True))
        logger.info(f"start_time {start_time}")
        logger.info(f"end_time {end_time}")

        tc.setCurrentFrameNumber(tc.findBestFrameNumberForFrameStart(end_time))

    def _temporal_update(self, _):

        tc = iface.mapCanvas().temporalController()
        tct = tc.dateTimeRangeForFrameNumber(tc.currentFrameNumber()).begin().toPyDateTime()
        # Convert the timekey to result index
        timekey = (tct-tc.temporalExtents().begin().toPyDateTime()).total_seconds()

        for result_idx in range(len(self.model.get_selected_results())):
            result_item = self.model.get_selected_results()[result_idx]
            timestamps = result_item.threedi_result.timestamps
            # TODO: are the timekeys always sorted? Are they cached?
            index = int(timestamps.searchsorted(timekey+0.01, "right")-1)

            # messagebar_message("timekey", f"time: {timekey} current: {tc.currentFrameNumber()} current: {index}")
            # messagebar_message("Time2", f"{tct}: {current}", Qgis.Warning)
            # messagebar_message("count", f"{tc.totalFrameCount()}")
            logger.info(f"result_idx = {result_idx}, index = {index}, current frame: {tc.currentFrameNumber()}, #timesteps: {len(timestamps)}")
            self.map_animator.update_results(result_item, index)

    def _add_action(
        self,
        tool_instance,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        setattr(tool_instance, "action_icon", action)
        self.actions.append(action)
        return action
