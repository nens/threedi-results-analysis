threedi-qgis-plugin
===================

3Di QGIS Plugin (3Di Toolbox)


Installation
------------

There are multiple ways to install:

- Copy/symlink everything to your QGIS plugin directory (on Linux: ``~/.qgis2/python/plugins``)
- Add https://plugins.lizard.net/plugins.xml as a plugin repository to QGIS.

      - Via menu bar go to: Plugins > Manage And Install Plugins... > Settings; add the repo and reload.
      
Release
-------

You can make releases with ``zest.releaser`` if you also have ``qgispluginreleaser`` installed. The
``fullrelease`` command should be sufficient. Under the hood it calls ``make zip`` which is modified
a bit (see ``Makefile``, old zip directive is still avaiable) so that it doesn't copy everything to your
QGIS plugin directory.

Manually copy to server::

    $ scp ThreeDiToolbox.0.2.zip 119-packages-d1.external-nens.local:/srv/packages.lizardsystem.nl/var/plugins
