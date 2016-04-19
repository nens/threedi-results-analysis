# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ThreeDiToolboxDockWidget
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
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), '..', 'ui',
    'threedi_toolbox_dockwidget_base.ui'))


class ThreeDiToolboxDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingWidget = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(ThreeDiToolboxDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        self.setupUi(self)

    def closeEvent(self, event):
        self.closingWidget.emit()
        event.accept()
