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
from importlib.machinery import SourceFileLoader
from pathlib import Path
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAbstractItemView
from ThreeDiToolbox.tool_commands.command_dialog_base import CommandBoxDockWidget
from ThreeDiToolbox.tool_commands.command_model import CommandModel
from ThreeDiToolbox.tool_commands.constants import COMMAND_STRUCTURE

import logging
import types


logger = logging.getLogger(__name__)


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
        self.menu_text = u"Commands for working with 3Di models"

        self.pluginIsActive = False
        self.dockwidget = None

        self.commandboxmodel = None
        self.commandbox = None
        self._command_package_mapping = {}

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

    @staticmethod
    def leaf_path(q_model_index):
        if not q_model_index.parent().isValid():
            return [q_model_index.data()]
        else:
            return CommandBox.leaf_path(q_model_index.parent()) + [q_model_index.data()]

    def get_package(self, module_name):
        for step, commands in COMMAND_STRUCTURE.items():
            package_name = commands.get(module_name)
            if package_name:
                return package_name

    def run_script(self, qm_idx):
        """Dynamically import and run the selected script from the tree view.

        Args:
            qm_idx: the clicked QModelIndex
        """
        # We're only interested in leaves of the tree:
        # TODO: need to make sure the leaf is not an empty directory
        if self.is_leaf(qm_idx):
            module_name = qm_idx.data()
            package_name = self.get_package(module_name)
            if not package_name:
                logging.warning("package of clicked command not found")
                return
            tool_commands_dir = Path(__file__).parent
            module_path = tool_commands_dir / package_name / module_name
            logger.debug(module_name)
            logger.debug(module_path)
            name = module_path.stem
            ext = module_path.suffix
            if ext != ".py":
                logger.error("Not a Python script")
                return

            loader = SourceFileLoader(name, str(module_path))
            mod = types.ModuleType(loader.name)
            loader.exec_module(mod)
            logger.debug(str(mod))

            command = mod.CustomCommand(
                iface=self.iface, ts_datasources=self.ts_datasources
            )
            command.run()

    def add_commands(self):
        self.commandboxmodel = CommandModel()
        self.dockwidget.treeView.setModel(self.commandboxmodel)
        self.dockwidget.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dockwidget.treeView.doubleClicked.connect(self.run_script)
