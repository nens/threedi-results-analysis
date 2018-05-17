ThreeDiToolbox
==============

.. image:: https://travis-ci.org/nens/ThreeDiToolbox.svg?branch=master
    :target: https://travis-ci.org/nens/ThreeDiToolbox

A QGIS plugin for working with 3Di models and netCDF results. Features include:

- Importing spatialite and netCDF datasources
- Visualization of 3Di network structure based on the netCDF
- Visualization of datasource time series
- Sideviews
- An extensible toolbox with custom Python scripts (for e.g. statistical analysis)
- import of sufhyd files

`Take a look at the Wiki for information`_.

.. _`Take a look at the Wiki for information`: https://github.com/nens/threedi-qgis-plugin/wiki


Installing requirements
-----------------------

- QGIS 2.14 or 2.16 (64 bit is recommended)
- pyqtgraph
- sqlalchemy version 1.1.0 or higher
- geoalchemy2 with custom modifications, source available here: https://github.com/nens/geoalchemy2
- netCDF4 (included only for Windows using 64 bit QGIS)
- h5py (included for Windows)

Most Python dependencies are included in the **distribution** of the plugin,
but if you clone this repository you need to manually install them in the
``external`` directory::

    $ pip install -r requirements.txt --target=external --no-deps -U

Windows
  The package includes the dependency 'netCDF4' for 64 bit installations of QGIS under
  Windows (tested on Windows 7 SP1 and Windows 10). If you are using the 32 bit version of QGIS,
  it is best to upgrade to the 64 bit version or build the Python netCDF4 including C bindings yourself.

Linux
  If you're on Linux, NetCDF and HDF5 dependencies are **not** included, so you have to install them::

    $ sudo apt-get install libhdf5-serial-dev libnetcdf-dev

  Install Python packages globally because we don't include them for Linux::

    $ sudo pip install -r requirements-dev.txt -U

  You might need to install the Qt4 PostgreSQL driver for loading sufhyd::

    $ sudo apt-get install libqt4-sql-psql


Installation
------------

The plugin can be added using one of the following ways:

- Using the Lizard QGIS repository: via the QGIS menu bar go to
  Plugins > Manage And Install Plugins... > Settings; add ``https://plugins.lizard.net/plugins.xml`` and reload.
  Install the plugin by selecting ThreeDiToolbox.
- Copy or symlink the repo directory to your plugin directory (on Linux:
  ``~/.qgis2/python/plugins``, on Windows: ``C:\\Users\<username>\.qgis2\python\plugins\``); make sure to install
  external dependencies (see Requirements section).


Release
-------

Make sure you have ``zest.releaser`` with ``qgispluginreleaser`` installed. To make a release (also
see: [1]_)::

    $ cd /path/to/the/plugin
    $ fullrelease  # NOTE: if it asks you if you want to check out the tag press 'y'.

Manually copy to server::

    $ scp ThreeDiToolbox.0.2.zip <user.name>@packages-server.example.local:/srv/packages.lizardsystem.nl/var/plugins


Tests
-----

Install test dependencies::

    $ pip install nose nose-exclude coverage==4.0

Run tests with ``nosetests`` inside the plugin directory. Running ``make test`` also works.


Notes
-----

.. [1] Under the hood it calls ``make zip`` which is modified a bit (see ``Makefile``, old zip directive
       is still avaiable) so that it doesn't copy everything to your QGIS plugin directory.
