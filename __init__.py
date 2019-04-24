# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ThreeDiToolbox
                                 A QGIS plugin for working with 3Di
                                 hydraulic models
                             -------------------
        begin                : 2016-03-04
        copyright            : (C) 2016 by Nelen&Schuurmans
        email                : servicedesk@nelen-schuurmans.nl
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
import imp
import sys
import os

import faulthandler

faulthandler.enable()


sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "external")
)


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ThreeDiToolbox class from file ThreeDiToolbox.

    :param iface: QgsInterface. A QGIS interface instance.
    """
    from .threedi_tools import ThreeDiTools
    from .utils.qlogging import setup_logging
    from .dependencies import try_to_import_dependencies

    setup_logging(iface)
    try_to_import_dependencies()
    return ThreeDiTools(iface)
