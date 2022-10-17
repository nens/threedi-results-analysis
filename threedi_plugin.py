from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QObject, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QLCDNumber
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
from ThreeDiToolbox.views.timeslider import TimesliderWidget
from qgis.core import Qgis, QgsVectorLayer, QgsProject, QgsCoordinateReferenceSystem
from qgis.utils import iface
from threedigrid.admin.exporters.geopackage import GeopackageExporter
from ThreeDiToolbox.utils.user_messages import StatusProgressBar, pop_up_critical
import os
from osgeo import ogr


# Import the code for the DockWidget
from .threedi_plugin_dockwidget import ThreeDiPluginDockWidget

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
        # Save reference to the QGIS interface
        QObject.__init__(self)

        self.iface = iface
        self.dockwidget = None

        # Declare instance attributes
        self.actions = []
        self.menu = "&3Di toolbox"

        self.ts_datasources = TimeseriesDatasourceModel()

        # Set toolbar and init a few toolbar widgets
        self.toolbar = self.iface.addToolBar("ThreeDiToolbox")
        self.toolbar.setObjectName("ThreeDiToolbox")
        self.toolbar_animation = self.iface.addToolBar("ThreeDiAnimation")
        self.toolbar_animation.setObjectName("ThreeDiAnimation")

        self.timeslider_widget = TimesliderWidget(self.iface, self.ts_datasources)
        self.timeslider_widget.valueChanged.connect(self.on_slider_change)

        self.lcd = QLCDNumber()
        self.lcd.setToolTip('Time format: "days hours:minutes"')
        self.lcd.setSegmentStyle(QLCDNumber.Flat)

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
        # ^^^ TODO: this doesn't seem to be set in here!
        self.group_layer_name = "3Di toolbox layers"
        self.group_layer = None

        self.line_layer = None
        self.point_layer = None

        self.layer_manager = LayerTreeManager(self.iface, self.ts_datasources)

        # Processing Toolbox scripts
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
        # Disabled until threedidepth is fixed
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

        if self.dockwidget == None:
            self.dockwidget = ThreeDiPluginDockWidget(None)
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.grid_file_selected.connect(self.add_grid_file)
            self.dockwidget.show()

        # Processing Toolbox of Qgis will eventually replace our custom-toolbox
        self.initProcessing()

        self.toolbar_animation.addWidget(self.map_animator_widget)
        self.toolbar_animation.addWidget(self.timeslider_widget)
        # Let lcd display a maximum of 9 digits, this way it can display a maximum
        # simulation duration of 999 days, 23 hours and 59 minutes.
        self.lcd.setDigitCount(9)
        self.toolbar_animation.addWidget(self.lcd)

        self.ts_datasources.rowsRemoved.connect(self.check_status_model_and_results)
        self.ts_datasources.rowsInserted.connect(self.check_status_model_and_results)
        self.ts_datasources.dataChanged.connect(self.check_status_model_and_results)

        self.init_state_sync()

        self.check_status_model_and_results()

    def update_slider_enabled_state(self):
        timeslider_needed = self.map_animator_widget.active or self.sideview_tool.active
        self.timeslider_widget.setEnabled(timeslider_needed)
        self.lcd.setEnabled(timeslider_needed)

    def on_slider_change(self, time_index):
        """Callback for slider valueChanged signal.

        Displays the time after the start of the simulation in <DDD HH:MM> (days, hours,
        minutes).

        :param time_index: (int) value the timeslider widget is set to. This is the time
            index of active netcdf result
        """
        days, hours, minutes = self.timeslider_widget.index_to_duration(time_index)
        formatted_display = "{:d} {:02d}:{:02d}".format(days, hours, minutes)
        self.lcd.display(formatted_display)

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

        self.timeslider_widget.valueChanged.disconnect(self.on_slider_change)

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

    def add_grid_file(self, input_gridadmin_h5: str) -> bool:
        """Converts h5 grid file to gpkg and add the layers to the project"""

        input_gridadmin_base, _ = os.path.splitext(input_gridadmin_h5)
        input_gridadmin_gpkg = input_gridadmin_base + '.gpkg'
        
        progress_bar = StatusProgressBar(100, "Generating geopackage")
        exporter = GeopackageExporter(input_gridadmin_h5, input_gridadmin_gpkg)
        exporter.export(lambda count, total, pb=progress_bar: pb.set_value((count * 100) // total))
        del progress_bar

        iface.messageBar().pushMessage("GeoPackage", "Generated geopackage", Qgis.Info)

        if not ThreeDiPlugin.add_layers_from_gpkg(input_gridadmin_gpkg):
            pop_up_critical("Failed adding the layers to the project.")
            return False

        iface.messageBar().pushMessage("GeoPackage", "Added layers to the project", Qgis.Info)
       
        return True

    # TODO: I think these methods need to be moved to some util module
    @staticmethod
    def add_layers_from_gpkg(gpkg_file) -> bool:
        """Retrieves layers from gpk and add to project.

           Checks whether all layers contain the same CRS, if
           so, sets this CRS on the project
        """

        gpkg_layers = [l.GetName() for l in ogr.Open(gpkg_file )]
        srs_ids = set()
        for layer in gpkg_layers:
            
            # Using the QgsInterface function addVectorLayer shows (annoying) confirmation dialogs
            # iface.addVectorLayer(gpkg_file + "|layername=" + layer, layer, 'ogr')
            vector_layer = QgsVectorLayer(gpkg_file + "|layername=" + layer, layer, "ogr")
            if not vector_layer.isValid():
                return False

            # TODO: styling?

            layer_srs_id = vector_layer.crs().srsid()
            srs_ids.add(layer_srs_id)
                    
            QgsProject.instance().addMapLayer(vector_layer)
        
        if len(srs_ids) == 1:
            srs_id = srs_ids.pop()
            crs = QgsCoordinateReferenceSystem.fromSrsId(srs_id)
            if crs.isValid():
                QgsProject.instance().setCrs(crs)
                iface.messageBar().pushMessage("GeoPackage", "Setting project CRS according to the source geopackage", Qgis.Info)
            else:
                iface.messageBar().pushMessage("GeoPackage", "Skipping setting project CRS - does gridadmin file contains a valid SRS?", Qgis.Warning)
                return False
        else:
            iface.messageBar().pushMessage("GeoPackage", f"Skipping setting project CRS - the source file {gpkg_file} SRS codes are inconsistent.", Qgis.Warning)
            return False

        return True
