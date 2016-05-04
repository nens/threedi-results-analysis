# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ThreeDiToolbox
                                 A QGIS plugin for working with 3di
                                 hydraulic models
                              -------------------
        begin                : 2016-04-27
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
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QSlider
import qgis


class TimesliderWidget(QSlider):
    """QGIS Plugin Implementation."""

    datasource_changed = pyqtSignal()

    def __init__(self, parent, iface, ts_datasource):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        super(TimesliderWidget, self).__init__(Qt.Horizontal)

        self.iface = iface
        self.ts_datasource = ts_datasource
        self.active_datasource = None

        self.setEnabled(False)
        self.ts_datasource.dataChanged.connect(self.ds_data_changed)
        self.ts_datasource.rowsInserted.connect(self.on_insert_ds)
        self.ts_datasource.rowsRemoved.connect(self.on_remove_ds)


    def get_current_ts_datasource_item(self):

        return self.active_datasource


    def on_insert_ds(self, parent, start, end):
        """
        Set slider settings based on loaded netCDF. based on Qt addRows
        model trigger.

        Note:   for now only take first netCDF from list, todo: support more

        :param parent: parent of event (Qt parameter)
        :param start: first row nr
        :param end: last row nr
        """
        if self.ts_datasource.rowCount() > 0:
            self.setEnabled(True)
            ds = self.ts_datasource.rows[0]
            if ds != self.active_datasource:

                self.timestamps = ds.datasource().get_timestamps()
                self.min_value = self.timestamps[0]
                self.max_value = self.timestamps[-1]
                self.interval = self.timestamps[1] - self.timestamps[0]
                self.nr_values = len(self.timestamps)

                self.setMaximum(self.nr_values - 1)
                self.setMinimum(0)
                self.setTickPosition(QSlider.TicksBelow)
                self.setTickInterval(1)
                self.setSingleStep(1)
                self.active_datasource = ds
                self.setValue(0)
                self.datasource_changed.emit()
        else:
            self.setMaximum(1)
            self.setValue(0)
            self.setEnabled(False)
            self.active_datasource = None

    def on_remove_ds(self, index, start, end):
        """
        Set slider settings based on loaded netCDF. based on Qt model
        removeRows trigger
        :param index: Qt Index (not used)
        :param start: first row nr
        :param end: last row nr
        """
        # for now: try to init first netCDF
        self.on_insert_ds(None, None, None)

    def ds_data_changed(self, index):
        """
        Set slider settings based on loaded netCDF. based on Qt
        data change trigger
        :param index: index of changed field
        """
        # for now: try to init first netCDF
        self.on_insert_ds(None, None, None)
