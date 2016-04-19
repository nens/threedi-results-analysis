threedi-qgis-plugin
===================

3Di QGIS Plugin (3Di Toolbox)


Installation
----
The plugin could be added using one of the following ways:
- Through the Lizard QGIS repository. Via menu bar go to: Plugins > Manage And Install Plugins... > Settings; add the repo and reload.
Install the plugin by selecting ThreeDiToolbox.
- Copy/ symlink everything in this map to your plugin directory (on Linux: ``~/.qgis2/python/plugins``, on
Windows: ``c:\\Users\<username>\.qgis2\python\plugins\``)

Installation on Windows
------------
Using the 64 bit installation of QGIS is recommended for this plugin.

The package includes the dependencies 'pyqtgraph' and 'netCDF4' for 64bit installations of QGIS under Windows.

If you are using other the 32 bit installation of QGIS, best to upgrade to the 64 bit version or build
the python netCDF4 including c bindings yourself.

Installation on Linux
------------

Install the python netCDF4 package using ``pip install netCDF4``


Release
-------

You can make releases with ``zest.releaser`` if you also have ``qgispluginreleaser`` installed. The
``fullrelease`` command should be sufficient. Under the hood it calls ``make zip`` which is modified
a bit (see ``Makefile``, old zip directive is still avaiable) so that it doesn't copy everything to your
QGIS plugin directory::

    $ cd /path/to/the/plugin
    $ fullrelease  # *** NOTE: if it asks you if you want to check out the tag press 'y'. ***

Manually copy to server::

    $ scp ThreeDiToolbox.0.2.zip 119-packages-d1.external-nens.local:/srv/packages.lizardsystem.nl/var/plugins
