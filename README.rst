ThreeDiToolbox
==============

.. image:: https://travis-ci.org/nens/ThreeDiToolbox.svg?branch=master
    :target: https://travis-ci.org/nens/ThreeDiToolbox

A QGIS plugin with tools for working with models and netCDF results from
`3Di`_ hydraulic/hydrologic modelling software.

.. _`3Di`: http://www.3di.nu/

The main features are:

- Visualization of model network structure and discretization
- Time series visualization
- Sideviews
- Visualize results spatially
- An extensible toolbox with custom Python scripts (for e.g. statistical analysis)
- Import of sufhyd files

Take a look at the `Wiki`_ for more information.

.. _`Wiki`: https://github.com/nens/ThreeDiToolbox/wiki


Installing requirements
-----------------------

- QGIS 3 (64 bit)
- pyqtgraph
- sqlalchemy version 1.1.0 or higher
- geoalchemy2 with custom modifications, source available here: https://github.com/nens/geoalchemy2
- h5py (included for Windows)

These Python dependencies are included in the **distribution** of the plugin,
but if you clone this repository you need to manually install them in the
``external`` directory::

    $ pip install -r requirements.txt --target=external --no-deps -U

Windows
^^^^^^^

The package includes the dependencies 'netCDF4' and 'h5py' for 64 bit
installations of QGIS under Windows (tested on Windows 7 SP1 and Windows 10).
If you are using the 32 bit version of QGIS, it is best to upgrade to the 64
bit version or build the python packages netCDF4 and h5py including C bindings
yourself. When building these packages, make sure to use the HDF5 version used
in Qgis (1.8.11)::

    $ python -m pip install --no-binary=h5py --no-deps --global-option=build_ext --global-option="-IC:\Program Files\QGIS 3.4\include" --global-option="-LC:\Program Files\QGIS 3.4\lib" h5py

Linux
^^^^^

For Linux, NetCDF and h5py dependencies are **not** included, so you have to
install them::

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

Make sure test deps from ``requirements-dev.txt`` are installed. Run tests with::

    $ source scripts/run-env-linux.sh /usr  # this should be automated (e.g. using Makefile)
    $ make test


Notes
-----

.. [1] Under the hood it calls ``make zip`` which is modified a bit (see ``Makefile``, old zip directive
       is still avaiable) so that it doesn't copy everything to your QGIS plugin directory.
