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
from ThreeDiToolbox.models.toolbox import CommandModel
from ThreeDiToolbox.views.threedi_toolbox_dockwidget import CommandBoxDockWidget
from importlib.machinery import SourceFileLoader
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAbstractItemView

import logging
import os.path
import types


logger = logging.getLogger(__name__)


class CommandBox(object):
    """QGIS Plugin Implementation."""

    def __init__(self, iface, ts_datasource):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        self.ts_datasource = ts_datasource

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.icon_path = ":/plugins/ThreeDiToolbox/icons/icon_commands.png"
        self.menu_text = u"Commands for working with 3Di models"

        self.pluginIsActive = False
        self.dockwidget = None

        self.commandbox = None

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
            return CommandBox.leaf_path(q_model_index.parent()) + [
                q_model_index.data()
            ]

    def run_script(self, qm_idx):
        """Dynamically import and run the selected script from the tree view.

        Args:
            qm_idx: the clicked QModelIndex
        """
        # We're only interested in leaves of the tree:
        # TODO: need to make sure the leaf is not an empty directory
        if self.is_leaf(qm_idx):
            filename = qm_idx.data()
            item = self.commandboxmodel.item(qm_idx.row(), qm_idx.column())
            path = self.leaf_path(qm_idx)

            logger.debug(filename)
            logger.debug(item)
            logger.debug(path)

            curr_dir = os.path.dirname(__file__)
            module_path = os.path.join(curr_dir, "tool_commands", *path)
            name, ext = os.path.splitext(path[-1])
            if ext != ".py":
                logger.error("Not a Python script")
                return

            logger.debug(module_path)
            logger.debug(name)

            loader = SourceFileLoader(name, module_path)
            mod = types.ModuleType(loader.name)
            loader.exec_module(mod)
            logger.debug(str(mod))

            self.command = mod.CustomCommand(
                iface=self.iface, ts_datasource=self.ts_datasource
            )
            self.command.run()

    def add_commands(self):
        self.commandboxmodel = CommandModel()
        self.dockwidget.treeView.setModel(self.commandboxmodel)
        self.dockwidget.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dockwidget.treeView.doubleClicked.connect(self.run_script)
