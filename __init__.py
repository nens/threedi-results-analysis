# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ThreeDiToolbox
                                 A QGIS plugin
 Toolbox for working with 3di hydraulic models
                             -------------------
        begin                : 2016-03-04
        copyright            : (C) 2016 by Nelen&Schuurmans
        email                : bastiaan.roos@nelen-schuurmans.nl
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

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ThreeDiToolbox class from file ThreeDiToolbox.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    try:
        #load optional settings for remote debugging for development purposes
        #add file remote_debugger_settings.py in main directory to use debugger
        import remote_debugger_settings
    except:
        print 'could not load remote debugger'

    from .threedi_tools import ThreeDiTools
    return ThreeDiTools(iface)
