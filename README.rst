ThreeDiToolbox
==============

.. image:: https://travis-ci.org/nens/ThreeDiToolbox.svg?branch=master
    :target: https://travis-ci.org/nens/ThreeDiToolbox

.. image:: https://coveralls.io/repos/github/nens/ThreeDiToolbox/badge.svg?branch=HEAD
    :target: https://coveralls.io/github/nens/ThreeDiToolbox?branch=HEAD


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


Installation on windows
-----------------------

You need to install Qgis 3.4 (the "long term release"). Either the stand-alone
installer or the osgeo4w install is fine. For osgeo4w, pick the "qgis LTR
full" version.

Add the Lizard QGIS repository: via the QGIS menu bar go to "Plugins > Manage
And Install Plugins... > Settings". Add
``https://plugins.lizard.net/plugins.xml`` and reload. Install the plugin by
selecting ThreeDiToolbox.

The extra dependencies that we need are bundled with the plugins and
automatically installed into the ``python\`` directory of your qgis profile.


Installation on linux
---------------------

You need to install Qgis 3.4 (the "long term release"). On ubuntu 18.04
(bionic), the following works::

  $ echo "deb https://qgis.org/ubuntu-ltr bionic main" >> /etc/apt/sources.list
  $ apt-key adv --keyserver keyserver.ubuntu.com --recv-key CAEB3DC3BDF7FB45
  $ apt-get update
  $ apt-get install qgis python3-h5py

This installs qgis and the necessary ``h5py`` dependency.

Inside qgis, add https://plugins.lizard.net/plugins.xml as a package
index. Now you can install ThreeDiToolbox.

The extra dependencies that we need (apart from ``h5py``) are bundled with the
plugins and automatically installed into the ``python\`` directory of your
qgis profile.


Local development
-----------------

Local development happens with docker to make sure we're working in a nicely
isolated environment. So first build the docker::

  $ docker-compose build

If your user ID isn't ``1000``, you can run it like this::

  $ docker-compose build --build-arg uid=`id -u` --build-arg gid=`id -g`

The docker-qgis's settings are persisted in a "named docker volume",
``qgis-docker``. To wipe it clean, run ``docker-compose down -v``.

The tests that run on travis-ci.org cache the docker image that is being build
in order to shave 5 minutes off the test duration. The image is automatically
rebuild when the ``Dockerfile``, ``docker-compose.yml`` or one of the two
`requirements` files changes. It is also possible to empty travis' cache in
case something seems to be wrong.

To run the full tests including coverage report and flake8::

  $ docker-compose run qgis-desktop make test

You can also just run pytest. You won't get the coverage report. You *can*
however then use one of the pytest options, like ``-x``, which aborts the test
at the first failure::

  $ docker-compose run qgis-desktop pytest -x

To get a "coverage" report for the docstrings or to run flake8::

  $ docker-compose run qgis-desktop make docstrings

To run black (standard pep8-compatible code formatting), isort (import
sorting) and flake8 (reporting missing imports and so), run::

  $ docker-compose run qgis-desktop make beautiful


Release
-------

Make sure you have ``zest.releaser`` with ``qgispluginreleaser`` installed. To make a release (also
see: [1]_)::

    $ cd /path/to/the/plugin
    $ fullrelease  # NOTE: if it asks you if you want to check out the tag press 'y'.

Manually copy to server::

    $ scp ThreeDiToolbox.0.2.zip <user.name>@packages-server.example.local:/srv/packages.lizardsystem.nl/var/plugins


Notes
-----

.. [1] Under the hood it calls ``make zip`` which is modified a bit (see ``Makefile``, old zip directive
       is still avaiable) so that it doesn't copy everything to your QGIS plugin directory.
