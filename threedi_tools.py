"""
/***************************************************************************
 ThreeDiToolbox
                                 A QGIS plugin for working with 3Di
                                 hydraulic models
                              -------------------
        begin                : 2016-03-04
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Nelen&Schuurmans
        email                : servicedesk@nelen-schuurmans.nl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from . import resources  # NoQa, initialize the Qt resources.
from .misc_tools import About
from .misc_tools import CacheClearer
from .misc_tools import ShowLogfile
from .models.datasources import TimeseriesDatasourceModel
from .tool_animation.map_animator import MapAnimator
from .tool_commands.command_box import CommandBox
from .tool_graph.graph import ThreeDiGraph
from .tool_result_selection.result_selection import ThreeDiResultSelection
from .tool_sideview.sideview import ThreeDiSideView
from .tool_statistics import StatisticsTool
from .tool_water_balance import WaterBalanceTool
from .utils.layer_tree_manager import LayerTreeManager
from .utils.qprojects import ProjectStateMixin
from .views.timeslider import TimesliderWidget
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtCore import QTranslator
from qgis.PyQt.QtCore import qVersion
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QLCDNumber

import logging
import os
import os.path


logger = logging.getLogger(__name__)

# Pycharm's refactor option "move" automatically deletes unused import statements,
# If "from . import resources" is deleted then tool-icons wont show up. Lets call it.
resources  # noqa


class ThreeDiTools(QObject, ProjectStateMixin):
    """Main Plugin Class which register toolbar ad menu and add tools """

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

        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir, "i18n", "ThreeDiTools_{}.qm".format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > "4.3.3":
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u"&3Di toolbox")

        self.ts_datasource = TimeseriesDatasourceModel()

        # Set toolbar and init a few toolbar widgets
        self.toolbar = self.iface.addToolBar("ThreeDiTools")
        self.toolbar.setObjectName("ThreeDiTools")
        self.toolbar_animation = self.iface.addToolBar("ThreeDiAnimation")
        self.toolbar_animation.setObjectName("ThreeDiAnimation")

        self.timeslider_widget = TimesliderWidget(
            self.toolbar_animation, self.iface, self.ts_datasource
        )
        self.lcd = QLCDNumber()
        self.timeslider_widget.valueChanged.connect(self.on_slider_change)

        self.map_animator_widget = MapAnimator(self.toolbar_animation, self.iface, self)

        # Init the rest of the tools
        self.about_tool = About(iface)
        self.cache_clearer = CacheClearer(iface, self.ts_datasource)
        self.result_selection_tool = ThreeDiResultSelection(iface, self.ts_datasource)
        self.toolbox_tool = CommandBox(iface, self.ts_datasource)
        self.graph_tool = ThreeDiGraph(iface, self.ts_datasource, self)
        self.sideview_tool = ThreeDiSideView(iface, self)
        self.stats_tool = StatisticsTool(iface, self.ts_datasource)
        self.water_balance_tool = WaterBalanceTool(iface, self.ts_datasource)
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
            self.logfile_tool,
        ]

        self.active_datasource = None
        self.group_layer_name = "3Di toolbox layers"
        self.group_layer = None

        self.line_layer = None
        self.point_layer = None

        self.layer_manager = LayerTreeManager(self.iface, self.ts_datasource)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("ThreeDiTools", message)

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

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        for tool in self.tools:
            self.add_action(
                tool,
                tool.icon_path,
                text=self.tr(tool.menu_text),
                callback=tool.run,
                parent=self.iface.mainWindow(),
            )

        self.toolbar_animation.addWidget(self.map_animator_widget)
        self.toolbar_animation.addWidget(self.timeslider_widget)
        self.toolbar_animation.addWidget(self.lcd)

        self.ts_datasource.rowsRemoved.connect(self.check_status_model_and_results)
        self.ts_datasource.rowsInserted.connect(self.check_status_model_and_results)
        self.ts_datasource.dataChanged.connect(self.check_status_model_and_results)

        self.init_state_sync()

        self.check_status_model_and_results()

    def on_slider_change(self, value):
        """Callback for slider valueChanged signal."""
        self.lcd.display(value)

    def check_status_model_and_results(self, *args):
        """ Check if a (new and valid) model or result is selected and react on
            this by pre-processing of things and activation/ deactivation of
            tools. function is triggered by changes in the ts_datasource
            args:
                *args: (list) the arguments provided by the different signals
        """
        # Enable/disable tools that depend on netCDF results.
        # For side views also the spatialite needs to be imported or else it
        # crashes with a segmentation fault
        if self.ts_datasource.rowCount() > 0:
            self.graph_tool.action_icon.setEnabled(True)
            self.cache_clearer.action_icon.setEnabled(True)
        else:
            self.graph_tool.action_icon.setEnabled(False)
            self.cache_clearer.action_icon.setEnabled(False)

        if (
            self.ts_datasource.rowCount() > 0
            and self.ts_datasource.model_spatialite_filepath is not None
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

        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u"&3Di toolbox"), action)
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
