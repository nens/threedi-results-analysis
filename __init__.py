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
import sys
import os
try:
    from .utils.user_messages import pop_up_info, log
except ImportError:
    pop_up_info = log = lambda x: x

msg = ''

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'external'))

try:
    import sqlalchemy
    import spatialalchemy
except ImportError, e:
    pop_up_info("Error loading sqlalchemy or spatialalchemy from "
                "'external' subdirectory. error %s" % e.message)

try:
    import netCDF4
    msg += 'Use local installation of python netCDF4 library'
except ImportError:
    if os.name == 'nt':
        if sys.maxsize > 2**32:
            # Windows 64 bit
            # use netCDF in external map
            sys.path.append(os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'external', 'netCDF4-win64'))
            import netCDF4

            msg += 'Used netCDF4 library, provided with plugin. '
        else:
            pop_up_info('Error: could not find netCDF4 installation. Change '
                        'to the 64-bit version of QGIS or try to install the '
                        'netCDF4 python libary yourself.')
            netCDF4 = None
    else:
        pop_up_info('Error: could not find netCDF4 installation. Please '
                    'install python-netCDF4 package.')
        netCDF4 = None

if netCDF4 is not None:
    msg += 'Python-netcdf version {python_netcdf}, netCDF4 version ' \
           '{netcdf} and HDF5 version {netcdf}.'.format(
                    python_netcdf = netCDF4.__version__,
                    netcdf = netCDF4.__netcdf4libversion__,
                    hdf5 = netCDF4.__hdf5libversion__)
    log(msg)


try:
    import pyqtgraph
    log('Use local installation of pyqtgraph ')
except ImportError:
    log('Use provided version of pyqtgraph')
    sys.path.append(os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'external', 'pyqtgraph-0.9.10'))
    try:
        import pyqtgraph
    except:
        # TODO: fix this error (which is the reason of this exception):
        # Exception: PyQtGraph requires either PyQt4 or PySide; neither package
        # could be imported.
        pass
except Exception:
    # TODO: fix this error (which is the reason of this exception):
    # Exception: PyQtGraph requires either PyQt4 or PySide; neither package
    # could be imported.
    msg = "Error: Exception while loading pyqtgraph. Probably couldn't import PyQt"
    log(msg)
    pop_up_info(msg)


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ThreeDiToolbox class from file ThreeDiToolbox.

    :param iface: QgsInterface. A QGIS interface instance.
    """

    from .threedi_tools import ThreeDiTools
    from .utils.qlogging import setup_logging

    setup_logging(iface)

    return ThreeDiTools(iface)
