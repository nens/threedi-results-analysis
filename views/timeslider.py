"""
/***************************************************************************
 ThreeDiToolbox
                                 A QGIS plugin for working with 3Di
                                 hydraulic models
                              -------------------
        begin                : 2016-04-27
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
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QSlider


class TimesliderWidget(QSlider):
    """QGIS Plugin Implementation."""

    datasource_changed = pyqtSignal()

    def __init__(self, parent, iface, ts_datasources):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        super().__init__(Qt.Horizontal)

        self.iface = iface
        self.ts_datasources = ts_datasources
        self.active_datasource = None
        # ^^^ Note: the plugin itself also already manages this one.

        self.setEnabled(False)
        self.ts_datasources.dataChanged.connect(self.ds_data_changed)
        self.ts_datasources.rowsInserted.connect(self.on_insert_datasource)
        self.ts_datasources.rowsRemoved.connect(self.on_remove_datasource)

    def on_insert_datasource(self, parent, start, end):
        """
        Set slider settings based on loaded netCDF. based on Qt addRows
        model trigger.

        Note:   for now only take first netCDF from list, todo: support more

        :param parent: parent of event (Qt parameter)
        :param start: first row nr
        :param end: last row nr
        """
        if self.ts_datasources.rowCount() > 0:
            self.setEnabled(True)
            datasource = self.ts_datasources.rows[0]
            if datasource != self.active_datasource:

                self.timestamps = datasource.datasource().get_timestamps()
                self.min_value = self.timestamps[0]
                self.max_value = self.timestamps[-1]
                self.interval = self.timestamps[1] - self.timestamps[0]
                self.nr_values = len(self.timestamps)

                self.setMaximum(self.nr_values - 1)
                self.setMinimum(0)
                self.setTickPosition(QSlider.TicksBelow)
                self.setTickInterval(1)
                self.setSingleStep(1)
                self.active_datasource = datasource
                self.setValue(0)
                self.datasource_changed.emit()
        else:
            self.setMaximum(1)
            self.setValue(0)
            self.setEnabled(False)
            self.active_datasource = None

    def on_remove_datasource(self, index, start, end):
        """
        Set slider settings based on loaded netCDF. based on Qt model
        removeRows trigger
        :param index: Qt Index (not used)
        :param start: first row nr
        :param end: last row nr
        """
        # for now: try to init first netCDF
        self.on_insert_datasource(None, None, None)

    def ds_data_changed(self, index):
        """
        Set slider settings based on loaded netCDF. based on Qt
        data change trigger
        :param index: index of changed field
        """
        # for now: try to init first netCDF
        self.on_insert_datasource(None, None, None)
