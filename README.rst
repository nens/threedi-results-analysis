threedi-qgis-plugin
===================

.. image:: https://travis-ci.org/nens/threedi-qgis-plugin.svg?branch=master
    :target: https://travis-ci.org/nens/threedi-qgis-plugin

A QGIS plugin for working with 3Di models and netCDF results. Features include:

- Importing spatialite and netCDF datasources
- Visualization of 3Di network structure based on the netCDF
- Visualization of datasource time series
- Sideviews
- An extensible toolbox with custom Python scripts (for e.g. statistical analysis)
- import of sufhyd files

`Take a look at the Wiki for information`_.

.. _`Take a look at the Wiki for information`: https://github.com/nens/threedi-qgis-plugin/wiki


Requirements
------------

- QGIS 2.14 or 2.16 (64 bit is recommended)
- pyqtgraph (included)
- netCDF4 (included only for Windows using 64 bit QGIS)
- sqlalchemy version 1.1.0 or higher (included)
- spatialalchemy with custom modifications, source available here: https://github.com/nens/geoalchemy2 (included)

Windows
  The package includes the dependencies 'pyqtgraph' and 'netCDF4' for 64 bit installations of QGIS under
  Windows (tested on Windows 7 SP1 and Windows 10). If you are using the 32 bit version of QGIS,
  it is best to upgrade to the 64 bit version or build the Python netCDF4 including C bindings yourself.

Linux
  Install the netCDF4 libs:``sudo apt-get install libhdf5-serial-dev libnetcdf-dev``.
  Install the python netCDF4 package using ``pip install netCDF4``
  You might need to install the Qt4 PostgreSQL driver for loading sufhyd: ``sudo apt-get install libqt4-sql-psql``.


Installation
------------

The plugin can be added using one of the following ways:

- Using the Lizard QGIS repository: via the QGIS menu bar go to
  Plugins > Manage And Install Plugins... > Settings; add ``https://plugins.lizard.net/plugins.xml`` and reload.
  Install the plugin by selecting ThreeDiToolbox.
- Copy or symlink the repo directory to your plugin directory (on Linux:
  ``~/.qgis2/python/plugins``, on Windows: ``C:\\Users\<username>\.qgis2\python\plugins\``);
  make sure the dir is called ``ThreeDiToolbox`` ([1]_)


Release
-------

Make sure you have ``zest.releaser`` with ``qgispluginreleaser`` installed. To make a release (also
see: [2]_)::

    $ cd /path/to/the/plugin
    $ fullrelease  # NOTE: if it asks you if you want to check out the tag press 'y'.

Manually copy to server::

    $ scp ThreeDiToolbox.0.2.zip <user.name>@packages-server.example.local:/srv/packages.lizardsystem.nl/var/plugins


Tests
-----

Install test dependencies::

    $ pip install nose nose-exclude coverage==4.0

The plugin directory must be called ``ThreeDiToolbox`` or else the
relative imports won't work correctly (see [1]_). Run tests with ``nosetests``
inside the plugin directory. Running ``make test`` also works.


Notes
-----

.. [1] The repo dir itself is a package (has an ``__init__.py``). To make everything work correctly
       the repo dir must be named ``ThreeDiToolbox``. Easiest way is to clone like this::

           $ git clone git@github.com:nens/threedi-qgis-plugin.git ThreeDiToolbox
           $ git submodule update --init --recursive

.. [2] Under the hood it calls ``make zip`` which is modified a bit (see ``Makefile``, old zip directive
       is still avaiable) so that it doesn't copy everything to your QGIS plugin directory.
