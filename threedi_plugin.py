from qgis.PyQt.QtCore import QObject, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QDockWidget
from qgis.PyQt.QtXml import QDomDocument, QDomElement
from qgis.utils import iface
from qgis.core import QgsApplication, QgsProject, QgsPathResolver, QgsSettings, QgsMapLayer
from threedi_results_analysis.misc_tools import About
from threedi_results_analysis.misc_tools import CacheClearer
from threedi_results_analysis.misc_tools import ShowLogfile
from threedi_results_analysis.misc_tools import ToggleResultsManager
from threedi_results_analysis.processing.providers import ThreediProvider
from threedi_results_analysis.gui.threedi_plugin_dockwidget import ThreeDiPluginDockWidget
from threedi_results_analysis.threedi_plugin_layer_manager import ThreeDiPluginLayerManager
from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel
from threedi_results_analysis.threedi_plugin_model_validation import ThreeDiPluginModelValidator
from threedi_results_analysis.threedi_plugin_model_serialization import ThreeDiPluginModelSerializer
from threedi_results_analysis.tool_animation.map_animator import MapAnimator
from threedi_results_analysis.tool_graph.graph import ThreeDiGraph
from threedi_results_analysis.tool_result_selection.models import TimeseriesDatasourceModel
from threedi_results_analysis.tool_result_selection.result_selection import ThreeDiResultSelection
from threedi_results_analysis.tool_sideview.sideview import ThreeDiSideView
from threedi_results_analysis.tool_statistics import StatisticsTool
from threedi_results_analysis.tool_water_balance import WaterBalanceTool
from threedi_results_analysis.tool_watershed.watershed_analysis import ThreeDiWatershedAnalyst
from threedi_results_analysis.utils import color
from threedi_results_analysis.utils.layer_tree_manager import LayerTreeManager
from threedi_results_analysis.utils.qprojects import ProjectStateMixin

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
        self.validator = ThreeDiPluginModelValidator(self.model)

        QgsProject.instance().writeProject.connect(self.write)
        QgsProject.instance().writeMapLayer.connect(self.write_map_layer)
        QgsProject.instance().readProject.connect(self.read)
        QgsProject.instance().removeAll.connect(self.model.clear)

        # Declare instance attributes
        self.actions = []
        self.menu = "&3Di toolbox"

        self.ts_datasources = TimeseriesDatasourceModel()

        # Set toolbar and init a few toolbar widgets
        self.toolbar = self.iface.addToolBar("ThreeDiResultAnalysis")
        self.toolbar.setObjectName("ThreeDiResultAnalysisToolBar")

        # Init the rest of the tools
        self.about_tool = About(iface)
        self.toggle_results_manager = ToggleResultsManager(iface, self)
        self.cache_clearer = CacheClearer(iface, self.ts_datasources)
        self.result_selection_tool = ThreeDiResultSelection(iface, self.ts_datasources)
        self.graph_tool = ThreeDiGraph(iface, self.model)
        self.sideview_tool = ThreeDiSideView(iface, self.model)
        self.stats_tool = StatisticsTool(iface, self.ts_datasources)
        self.water_balance_tool = WaterBalanceTool(iface, self.model)
        self.watershed_tool = ThreeDiWatershedAnalyst(iface, self.ts_datasources)
        self.logfile_tool = ShowLogfile(iface)

        self.tools = [  # second item indicates enabled on startup
            (self.about_tool, True),
            (self.toggle_results_manager, True),
            (self.cache_clearer, True),
            (self.result_selection_tool, True),
            (self.graph_tool, False),
            (self.sideview_tool, False),
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

        # Add the dockwidget, tabified with any other right area dock widgets
        main_window = iface.mainWindow()
        right_area_dock_widgets = [
            d for d in main_window.findChildren(QDockWidget)
            if main_window.dockWidgetArea(d) == Qt.RightDockWidgetArea
            if d.isVisible()
        ] + [self.dockwidget]
        tabify_with = [right_area_dock_widgets[0].objectName()]
        for dock_widget in right_area_dock_widgets:
            self.iface.removeDockWidget(dock_widget)
            self.iface.addTabifiedDockWidget(
                Qt.RightDockWidgetArea, dock_widget, tabify_with, True
            )

        # Connect the signals

        self.dockwidget.grid_file_selected.connect(self.validator.validate_grid)
        self.dockwidget.result_file_selected.connect(self.validator.validate_result_grid)
        self.validator.result_valid.connect(self.loader.load_result)
        self.validator.grid_valid.connect(self.loader.load_grid)
        self.loader.grid_loaded.connect(self.model.add_grid)
        self.loader.result_loaded.connect(self.model.add_result)

        self.model.grid_added.connect(self.dockwidget.expand_grid)

        # Removal signals
        self.dockwidget.result_removal_selected.connect(self.loader.unload_result)
        self.dockwidget.grid_removal_selected.connect(self.loader.unload_grid)
        self.loader.grid_unloaded.connect(self.model.remove_grid)
        self.loader.result_unloaded.connect(self.model.remove_result)

        self.model.grid_changed.connect(self.loader.update_grid)
        self.model.result_changed.connect(self.loader.update_result)
        self.model.result_unchecked.connect(self.loader.result_unchecked)

        self.toggle_results_manager.triggered.connect(self.dockwidget.toggle_visible)

        self.ts_datasources.rowsRemoved.connect(self.check_status_model_and_results)
        self.ts_datasources.rowsInserted.connect(self.check_status_model_and_results)
        self.ts_datasources.dataChanged.connect(self.check_status_model_and_results)

        self.dockwidget.show()
        self.dockwidget.set_model(self.model)

        self.initProcessing()

        # animation signals
        self.map_animator = MapAnimator(self.dockwidget.get_tools_widget(), self.model)
        self.model.result_checked.connect(self.map_animator.results_changed)
        self.model.result_unchecked.connect(self.map_animator.results_changed)
        self.model.result_added.connect(self.map_animator.results_changed)
        tc = iface.mapCanvas().temporalController()
        tc.updateTemporalRange.connect(self.map_animator.update_results)

        # graph signals
        self.model.result_added.connect(self.graph_tool.result_added)
        self.model.result_removed.connect(self.graph_tool.result_removed)
        self.model.result_changed.connect(self.graph_tool.result_changed)
        self.model.grid_changed.connect(self.graph_tool.grid_changed)

        # sideview signals
        self.model.grid_added.connect(self.sideview_tool.grid_added)
        self.model.grid_removed.connect(self.sideview_tool.grid_removed)
        self.model.grid_changed.connect(self.sideview_tool.grid_changed)
        self.model.result_added.connect(self.sideview_tool.result_added)
        self.model.result_removed.connect(self.sideview_tool.result_removed)
        self.model.result_changed.connect(self.sideview_tool.result_changed)
        tc.updateTemporalRange.connect(self.sideview_tool.update_waterlevels)

        self.init_state_sync()

        # Disable warning that scratch layer data will be lost
        QgsSettings().setValue("askToSaveMemoryLayers", False, QgsSettings.App)

        self.check_status_model_and_results()

    def write(self, doc: QDomDocument) -> bool:
        # Resolver convert relative to absolute paths and vice versa
        resolver = QgsPathResolver(QgsProject.instance().fileName() if (QgsProject.instance().filePathStorage() == 1) else "")
        return ThreeDiPluginModelSerializer.write(self.model, doc, resolver)

    def write_map_layer(self, layer: QgsMapLayer, elem: QDomElement, _: QDomDocument):
        # Ensure all our dynamically added attributes are not serialized
        result_field_names = self.model.get_result_field_names(layer.id())
        ThreeDiPluginModelSerializer.remove_result_field_references(
            elem, result_field_names,
        )

    def read(self, doc: QDomDocument) -> bool:
        self.model.clear()
        self.dockwidget.set_model(self.model)

        # Resolver convert relative to absolute paths and vice versa
        resolver = QgsPathResolver(QgsProject.instance().fileName() if (QgsProject.instance().filePathStorage() == 1) else "")
        if not ThreeDiPluginModelSerializer.read(self.loader, doc, resolver):
            self.model.clear()
            return False

        return True

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
            self.stats_tool.action_icon.setEnabled(True)
        else:
            self.stats_tool.action_icon.setEnabled(False)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI.

        Called then the plugin is unloaded.
        """

        # Stop animating
        tc = iface.mapCanvas().temporalController()
        tc.updateTemporalRange.disconnect(self.map_animator.update_results)

        # Clears model and emits subsequent signals
        self.model.clear()

        self.ts_datasources.rowsRemoved.disconnect(self.check_status_model_and_results)
        self.ts_datasources.rowsInserted.disconnect(self.check_status_model_and_results)
        self.ts_datasources.dataChanged.disconnect(self.check_status_model_and_results)

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
