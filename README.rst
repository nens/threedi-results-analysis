threedi-qgis-plugin
===================

3Di QGIS Plugin (3Di Toolbox)


Requirements
------------

This plugin has the following dependencies/requirements:

- QGIS 2.8 or 2.14 (64bit is recommended)
- pyqtgraph (included)
- netCDF4 (included for Windows using 64bit QGIS)

Windows
  The package includes the dependencies 'pyqtgraph' and 'netCDF4' for 64bit installations of QGIS under
  Windows (tested on Windows 7 SP1 and Windows 10). If you are using other the 32 bit installation of QGIS,
  it's best to upgrade to the 64 bit version or build the Python netCDF4 including C bindings yourself.

Linux
  Install the python netCDF4 package using ``pip install netCDF4``. The included pyqtgraph should be good.


Installing the plugin
---------------------

The plugin can be added using one of the following ways:

- Through the Lizard QGIS repository. Via menu bar go to:
  Plugins > Manage And Install Plugins... > Settings; add the repo and reload.
  Install the plugin by selecting ThreeDiToolbox.
- Copy or symlink the repo directory to your plugin directory (on Linux:
  ``~/.qgis2/python/plugins``, on Windows: ``C:\\Users\<username>\.qgis2\python\plugins\``);
  make sure the dir is called ``ThreeDiToolbox`` ([1]_)


Release
-------

You can make releases using ``zest.releaser`` with ``qgispluginreleaser`` installed. The
``fullrelease`` command should be sufficient. Under the hood it calls ``make zip`` which is modified
a bit (see ``Makefile``, old zip directive is still avaiable) so that it doesn't copy everything to your
QGIS plugin directory::

    $ cd /path/to/the/plugin
    $ fullrelease  # NOTE: if it asks you if you want to check out the tag press 'y'.

Manually copy to server::

    $ scp ThreeDiToolbox.0.2.zip 119-packages-d1.external-nens.local:/srv/packages.lizardsystem.nl/var/plugins


Tests
-----

For now running tests is a bit cumbersome because of the relative imports in the code. You have to be
outside of the repository directory and then run test modules independently like this::

    $ python -m unittest threedi-qgis-plugin.test.test_datasources
    etc.

**New method** with ``nose`` test runner. Make sure you have ``nose`` installed (``pip install nose``).
First you have to rename the plugin dir to the right package name, which is ``ThreeDiToolbox`` or
else the relative imports won't work correctly (see [1]_). Then run ``nosetests`` inside the plugin directory::

    $ nosetests


Notes
-----

.. [1] The repo dir itself is a package (has an ``__init__.py``). To make everything work correctly
       the repo dir must be named ``ThreeDiToolbox``. Easiest way is to clone like this::

           $ git clone git@github.com:nens/threedi-qgis-plugin.git ThreeDiToolbox
