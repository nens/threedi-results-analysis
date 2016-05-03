# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ThreeDiToolbox
                                 A QGIS plugin for working with 3di
                                 hydraulic models
                              -------------------
        begin                : 2016-03-04
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Nelen&Schuurmans
        email                : bastiaan.roos@nelen-schuurmans.nl
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
import os.path

from PyQt4.QtCore import Qt
from PyQt4 import QtGui

# Import the code for the DockWidget
from .views.threedi_toolbox_dockwidget import ThreeDiToolboxDockWidget
from .models.toolbox import ToolboxModel
from .utils.user_messages import pop_up_question


class ThreeDiToolbox:
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

        self.icon_path = ':/plugins/ThreeDiToolbox/icon_toolbox.png'
        self.menu_text = u'Toolbox for working with 3di models'

        self.pluginIsActive = False
        self.dockwidget = None

        self.toolbox = None

    def on_unload(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING ThreeDiToolbox"

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

            #print "** STARTING ThreeDiToolbox"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget is None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = ThreeDiToolboxDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingWidget.connect(self.on_close_child_widget)

            # show the dockwidget
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
            self.add_tools()

    @staticmethod
    def is_leaf(q_model_index):
        """Check if QModelIndex is a leaf, i.e., has no children."""
        return (q_model_index.isValid() and
                not q_model_index.child(0, 0).isValid())

    @staticmethod
    def leaf_path(q_model_index):
        if not q_model_index.parent().isValid():
            return [q_model_index.data()]
        else:
            return ThreeDiToolbox.leaf_path(q_model_index.parent()) + \
                [q_model_index.data()]

    def run_script(self, qm_idx):
        """Dynamically import and run the selected script from the tree view.

        Args:
            qm_idx: the clicked QModelIndex
        """
        # We're only interested in leaves of the tree:
        # TODO: need to make sure the leaf is not an empty directory
        if self.is_leaf(qm_idx):
            if not pop_up_question(
                    msg="Are you sure you want to run this script?",
                    title="Warning"):
                return
            filename = qm_idx.data()
            item = self.toolboxmodel.item(qm_idx.row(), qm_idx.column())
            path = self.leaf_path(qm_idx)
            print(filename)
            print(item)
            print(path)
            # from .qdebug import pyqt_set_trace; pyqt_set_trace()

            curr_dir = os.path.dirname(__file__)
            module_path = os.path.join(curr_dir, 'commands', *path)
            name, ext = os.path.splitext(path[-1])
            if ext != '.py':
                print("Not a Python script")
                return
            print(module_path)
            print(name)
            import imp
            mod = imp.load_source(name, module_path)
            print(mod)

            self.command = mod.CustomCommand(
                iface=self.iface, ts_datasource=self.ts_datasource)
            self.command.run()

    def add_tools(self):
        self.toolboxmodel = ToolboxModel()
        self.dockwidget.treeView.setModel(self.toolboxmodel)
        self.dockwidget.treeView.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers)
        self.dockwidget.treeView.doubleClicked.connect(self.run_script)
