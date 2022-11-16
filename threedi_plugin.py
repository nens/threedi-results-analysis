from qgis.core import QgsApplication, QgsDateTimeRange
from qgis.PyQt.QtCore import QObject, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from ThreeDiToolbox.misc_tools import About
from ThreeDiToolbox.misc_tools import CacheClearer
from ThreeDiToolbox.misc_tools import ShowLogfile
from ThreeDiToolbox.processing.providers import ThreediProvider
from ThreeDiToolbox.tool_animation.map_animator import MapAnimator
from ThreeDiToolbox.tool_commands.command_box import CommandBox
from ThreeDiToolbox.tool_graph.graph import ThreeDiGraph
from ThreeDiToolbox.tool_result_selection.models import TimeseriesDatasourceModel
from ThreeDiToolbox.tool_result_selection.result_selection import ThreeDiResultSelection
from ThreeDiToolbox.tool_sideview.sideview import ThreeDiSideView
from ThreeDiToolbox.tool_statistics import StatisticsTool
from ThreeDiToolbox.tool_water_balance import WaterBalanceTool
from ThreeDiToolbox.tool_watershed.watershed_analysis import ThreeDiWatershedAnalyst
from ThreeDiToolbox.utils import color
from ThreeDiToolbox.utils import styler
from ThreeDiToolbox.utils.layer_tree_manager import LayerTreeManager
from ThreeDiToolbox.utils.qprojects import ProjectStateMixin
from qgis.core import Qgis
from qgis.utils import iface
from ThreeDiToolbox.threedi_plugin_import import ThreeDiPluginModelLoader
import datetime
from datetime import timedelta

# Import the code for the DockWidget
from .threedi_plugin_dockwidget import ThreeDiPluginDockWidget
from .threedi_plugin_model import ThreeDiPluginModel
from .threedi_plugin_model_validation import ThreeDiPluginModelValidator

import logging

logger = logging.getLogger(__name__)


class ThreeDiPlugin(QObject, ProjectStateMixin):
    """Main Plugin Class which register toolbar ad menu and add tools"""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        QObject.__init__(self)

        # Save reference to the QGIS interface
        self.iface = iface
        self.dockwidget = None
        self.model = ThreeDiPluginModel()
        self.model.grid_item_added.connect(ThreeDiPluginModelLoader.import_grid_item)
        self.model.result_item_added.connect(ThreeDiPluginModelLoader.import_result_item)
        self.model.result_item_checked.connect(lambda item: print(item))
        self.model.result_item_unchecked.connect(lambda item: print(item))
        self.model.result_item_selected.connect(lambda item: print(item))
        self.model.result_item_deselected.connect(lambda item: print(item))

        self.validator = ThreeDiPluginModelValidator()
        self.model.result_item_added.connect(self.validator.result_item_added)

        # Declare instance attributes
        self.actions = []
        self.menu = "&3Di toolbox"

        self.ts_datasources = TimeseriesDatasourceModel()

        # Set toolbar and init a few toolbar widgets
        self.toolbar = self.iface.addToolBar("ThreeDiToolbox")
        self.toolbar.setObjectName("ThreeDiToolbox")
        self.toolbar_animation = self.iface.addToolBar("ThreeDiAnimation")
        self.toolbar_animation.setObjectName("ThreeDiAnimation")

        self.map_animator_widget = MapAnimator(self.toolbar_animation, self.iface, self)

        # Init the rest of the tools
        self.about_tool = About(iface)
        self.cache_clearer = CacheClearer(iface, self.ts_datasources)
        self.result_selection_tool = ThreeDiResultSelection(iface, self.ts_datasources)
        self.toolbox_tool = CommandBox(iface, self.ts_datasources)
        self.graph_tool = ThreeDiGraph(iface, self.ts_datasources, self)
        self.sideview_tool = ThreeDiSideView(iface, self)
        self.stats_tool = StatisticsTool(iface, self.ts_datasources)
        self.water_balance_tool = WaterBalanceTool(iface, self.ts_datasources)
        self.watershed_tool = ThreeDiWatershedAnalyst(iface, self.ts_datasources)
        self.logfile_tool = ShowLogfile(iface)

        self.tools = [
            self.about_tool,
            self.cache_clearer,
            self.result_selection_tool,
            self.toolbox_tool,
            self.graph_tool,
            self.sideview_tool,
            self.stats_tool,
            self.water_balance_tool,
            self.watershed_tool,
            self.logfile_tool,
        ]

        self.active_ts_datasource = None
        self.layer_manager = LayerTreeManager(self.iface, self.ts_datasources)

        self.provider = None

        # Styling
        for color_ramp in color.COLOR_RAMPS:
            styler.add_color_ramp(color_ramp)

    def add_action(
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

    def initProcessing(self):
        """Create the Qgis Processing Toolbox provider and its algorithms"""
        self.provider = ThreediProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        for tool in self.tools:
            self.add_action(
                tool,
                tool.icon_path,
                text=tool.menu_text,
                callback=tool.run,
                parent=self.iface.mainWindow(),
            )

        if self.dockwidget is None:
            self.dockwidget = ThreeDiPluginDockWidget(None)
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)

            self.dockwidget.grid_file_selected.connect(self.model.add_grid_file)
            self.dockwidget.result_file_selected.connect(self.model.add_result_file)
            self.dockwidget.item_selected.connect(self.model.select_item)
            self.dockwidget.item_deselected.connect(self.model.deselect_item)

            self.dockwidget.show()

        self.dockwidget.treeView.setModel(self.model)
        # TODO: should this logic be moved inside the treeWidget?
        self.dockwidget.treeView.selectionModel().selectionChanged.connect(self.dockwidget._selection_changed)

        self.initProcessing()

        self.toolbar_animation.addWidget(self.map_animator_widget)

        self.ts_datasources.rowsRemoved.connect(self.check_status_model_and_results)
        self.ts_datasources.rowsInserted.connect(self.check_status_model_and_results)
        self.ts_datasources.dataChanged.connect(self.check_status_model_and_results)

        self.init_state_sync()

        tc = iface.mapCanvas().temporalController()
        tc.updateTemporalRange.connect(self.update_animation)
        tc.setTemporalExtents(QgsDateTimeRange(datetime.datetime(2020, 5, 17), datetime.datetime.now()))

        self.check_status_model_and_results()

    def update_slider_enabled_state(self):
        pass
        # timeslider_needed = self.map_animator_widget.active or self.sideview_tool.active
        # self.lcd.setEnabled(timeslider_needed)

    def check_status_model_and_results(self, *args):
        """Check if a (new and valid) model or result is selected and react on
        this by pre-processing of things and activation/ deactivation of
        tools. function is triggered by changes in the ts_datasources
        args:
            *args: (list) the arguments provided by the different signals
        """
        # First some logging.
        logger.info(
            "Timeseries datasource change. %s ts_datasources:",
            self.ts_datasources.rowCount(),
        )
        for ts_datasource in self.ts_datasources.rows:
            logger.info(
                "    - %s (%s)", ts_datasource.name.value, ts_datasource.file_path.value
            )
        logger.info(
            "The selected 3di model spatialite: %s",
            self.ts_datasources.model_spatialite_filepath,
        )

        # Enable/disable tools that depend on netCDF results.
        # For side views also the spatialite needs to be imported or else it
        # crashes with a segmentation fault
        if self.ts_datasources.rowCount() > 0:
            self.graph_tool.action_icon.setEnabled(True)
            self.cache_clearer.action_icon.setEnabled(True)
            self.map_animator_widget.setEnabled(True)

            # TEST: connect TemporalController
            datasource = self.ts_datasources.rows[0]
            timestamps = datasource.threedi_result().get_timestamps()
            tc = iface.mapCanvas().temporalController()
            start_time = datetime.datetime(2000, 1, 1)
            end_time = start_time + timedelta(seconds=round(timestamps[-1]))
            tc.setTemporalExtents(QgsDateTimeRange(start_time, end_time, True, True))
            iface.messageBar().pushMessage("stamps", f"{timestamps}", Qgis.Info)
            iface.messageBar().pushMessage("end", f"{end_time}", Qgis.Info)

        else:
            self.graph_tool.action_icon.setEnabled(False)
            self.cache_clearer.action_icon.setEnabled(False)
            self.map_animator_widget.active = False
            self.map_animator_widget.setEnabled(False)
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
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.unload_state_sync()
        QgsApplication.processingRegistry().removeProvider(self.provider)

        for action in self.actions:
            self.iface.removePluginMenu("&3Di toolbox", action)
            self.iface.removeToolBarIcon(action)

            for tool in self.tools:
                tool.on_unload()

        self.layer_manager.on_unload()

        self.iface.removeDockWidget(self.dockwidget)
        del self.dockwidget

        try:
            del self.toolbar
        except AttributeError:
            logger.exception("Error, toolbar already removed? Continuing anyway.")

        try:
            del self.toolbar_animation
        except AttributeError:
            logger.exception(
                "Error, toolbar animation already removed? Continuing anyway."
            )

    def update_animation(self, x):

        if self.ts_datasources.rowCount() > 0:
            tc = iface.mapCanvas().temporalController()
            tct = tc.dateTimeRangeForFrameNumber(tc.currentFrameNumber()).begin().toPyDateTime()

            # Convert the timekey to result index
            timekey = (tct-datetime.datetime(2000, 1, 1)).total_seconds()

            datasource = self.ts_datasources.rows[0]
            timestamps = datasource.threedi_result().timestamps
            # TODO: are the timekeys always sorted?
            index = int(timestamps.searchsorted(timekey+0.1, "right")-1)

            # iface.messageBar().pushMessage("timekey", f"time: {timekey} current: {tc.currentFrameNumber()} current: {index}", Qgis.Info)
            # iface.messageBar().pushMessage("Time2", f"{tct}: {current}", Qgis.Warning)
            # iface.messageBar().pushMessage("count", f"{tc.totalFrameCount()}", Qgis.Info)
            self.map_animator_widget.update_results(index, True, True)
