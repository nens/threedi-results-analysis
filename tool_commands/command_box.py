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
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAbstractItemView
from ThreeDiToolbox.tool_commands.command_dialog_base import CommandBoxDockWidget
from ThreeDiToolbox.tool_commands.command_model import CommandModel
from ThreeDiToolbox.tool_commands.constants import COMMANDS_DIR

import importlib
import logging


logger = logging.getLogger(__name__)

DEFAULT_COMMAND_NAME = "command.py"


class CommandBox(object):
    """QGIS Plugin Implementation."""

    def __init__(self, iface, ts_datasources):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        self.ts_datasources = ts_datasources

        self.icon_path = ":/plugins/ThreeDiToolbox/icons/icon_command.png"
        self.menu_text = "Commands for working with 3Di models"

        self.pluginIsActive = False
        self.dockwidget = None

        self.commandboxmodel = None
        self.commandbox = None
        self.default_command_name = "command.py"

    def on_unload(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""
        # disconnects
        if self.dockwidget:
            self.dockwidget.close()

    def on_close_child_widget(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""
        self.dockwidget.treeView.doubleClicked.disconnect(self.run_script)
        self.dockwidget.closingWidget.disconnect(self.on_close_child_widget)

        self.dock_widget = None
        self.pluginIsActive = False

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget is None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = CommandBoxDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingWidget.connect(self.on_close_child_widget)

            # show the dockwidget
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
            self.add_commands()

    @staticmethod
    def is_leaf(q_model_index):
        """Check if QModelIndex is a leaf, i.e., has no children."""
        return q_model_index.isValid() and not q_model_index.child(0, 0).isValid()

    def get_module_path(self, display_name):
        package_name = display_name.replace(" ", "_")
        module_path = COMMANDS_DIR / package_name / DEFAULT_COMMAND_NAME
        return module_path

    def get_import_string(self, display_name):
        """ return: string (e.g. 'ThreeDiToolbox.tool_commands.raster_checker.') """
        package_name = display_name.replace(" ", "_")
        command_without_extension = DEFAULT_COMMAND_NAME.split(".py")[0]
        import_string = (
            __package__ + "." + package_name + "." + command_without_extension
        )
        return import_string

    def import_command(self, import_string):
        try:
            imported_command = importlib.import_module(import_string)
            return imported_command
        except ImportError:
            logging.error(f"could not import {import_string}")

    def run_script(self, qm_idx):
        """Dynamically import and run the selected script from the tree view.
        Args: qm_idx: the clicked QModelIndex
        """
        # We're only interested in leaves of the tree:
        if self.is_leaf(qm_idx):
            display_name = qm_idx.data()

            module_path = self.get_module_path(display_name)
            if not module_path.is_file():
                logger.error(f"{module_path} is not a file")
                return
            logger.debug(f"command display name: {display_name}")
            logger.debug(f"command module_path: {module_path}")

            import_string = self.get_import_string(display_name)
            imported_command = self.import_command(import_string)
            if not imported_command:
                return
            # TODO: keep reference to `command_instance` so it doesn't get cleaned up
            # during garbage collection. See https://wiki.qt.io/PySide_Pitfalls.
            command_instance = imported_command.CustomCommand(
                iface=self.iface, ts_datasources=self.ts_datasources
            )
            command_instance.run()

    def add_commands(self):
        self.commandboxmodel = CommandModel()
        self.dockwidget.treeView.setModel(self.commandboxmodel)
        self.dockwidget.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dockwidget.treeView.doubleClicked.connect(self.run_script)
