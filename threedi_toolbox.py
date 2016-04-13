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

# Import the code for the DockWidget
from threedi_toolbox_dockwidget import ThreeDiToolboxDockWidget
from .models.toolbox import ToolboxModel


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

    def add_tools(self):
        self.toolboxmodel = ToolboxModel()
        self.dockwidget.treeView.setModel(self.toolboxmodel)
