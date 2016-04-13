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
import qgis

from views.graph import GraphDockWidget


class ThreeDiGraph:
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

        self.icon_path = ':/plugins/ThreeDiToolbox/icon_graph.png'
        self.menu_text = u'Show 3di results in Graph'

        self.dock_widgets = []
        self.widget_nr = 0

    def on_unload(self):
        """
        on close of graph plugin
        """
        for widget in self.dock_widgets:
            widget.close()

        #self.ts_datasource.close()
        #self.ts_datasource = None

    def on_close_child_widget(self, widget_nr):
        """Cleanup necessary items here when plugin dockwidget is closed"""
        nr = None

        # find widget based on nr
        for i in range(0, len(self.dock_widgets)):
            widget = self.dock_widgets[i]
            if widget.nr == widget_nr:
                nr = i

        # close widget
        if nr is not None:
            widget = self.dock_widgets[nr]
            widget.closingWidget.disconnect(self.on_close_child_widget)

            del self.dock_widgets[nr]

    def run(self):
        """
        Run method that loads and starts the plugin (docked graph widget)
        """
        # create the dockwidget
        self.widget_nr += 1
        new_widget = GraphDockWidget(self.iface, parent_class=self, nr=self.widget_nr, ts_datasource=self.ts_datasource)
        self.dock_widgets.append(new_widget)

        # connect cleanup on closing of dockwidget
        new_widget.closingWidget.connect(self.on_close_child_widget)

        # show the dockwidget
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, new_widget)

        #make stack of graph widgets (instead of next to each other)
        if len(self.dock_widgets) > 1:
            window = qgis.core.QgsApplication.activeWindow()
            window.tabifyDockWidget(self.dock_widgets[0], new_widget)

        new_widget.show()
