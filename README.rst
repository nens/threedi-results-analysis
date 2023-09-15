3Di Results Analysis Tool
==============

Analyse `3Di`_ results and visualize computational grids in the 3Di Modeller Interface.
A QGIS plugin for analying 3Di results and visualize computational grids in the 3Di Modeller Interface.

.. _`3Di`: https://3diwatermanagement.com/

  The tools that this plugin provides allow you to:

    - Make (maximum) water depth or water level rasters from raw 3Di simulation results.
    - Visualize results on the map canvas for a specific timestep
    - Plot timeseries of discharge, water level or any other variable in a graph
    - Make side view plots of water levels and water level gradients at any time during the simulation
    - Calculate the water balance for any given area in the model domain
    - Calculate aggregated results such as maximum water level per node or total discharge per flowline
    - Calculate the total discharge crossing a user-defined line
    - Find the upstream or downstream area for any node or group of nodes

Installation on windows
-----------------------

You need to install Qgis 3.28.5+ (the "long term release") at qgis.org. 

Add the Lizard QGIS repository: via the QGIS menu bar go to "Plugins > Manage
And Install Plugins... > Settings". Add
``https://plugins.lizard.net/plugins.xml`` and reload. Install the plugin by
selecting 3Di Results Analysis.

The extra dependencies that we need are bundled with the plugins and
automatically installed into the ``deps`` directory of the plugin in your qgis profile.

Installation on linux
---------------------

You need to install Qgis 3.4 (the "long term release"). On ubuntu 18.04
(bionic), the following works::

  $ echo "deb https://qgis.org/ubuntu-ltr bionic main" >> /etc/apt/sources.list
  $ apt-key adv --keyserver keyserver.ubuntu.com --recv-key 51F523511C7028C
  $ apt-get update
  $ apt-get install qgis python3-h5py

This installs qgis and the necessary ``h5py`` dependency.

Inside qgis, add https://plugins.lizard.net/plugins.xml as a package
index. Now you can install ThreeDiToolbox.

The extra dependencies that we need (apart from ``h5py``) are bundled with the
plugins and automatically installed into the ``python\\`` directory of your
qgis profile.


Local development
-----------------

On Linux, local development happens with docker to make sure we're working in a nicely
isolated environment. So first build the docker::

  $ docker-compose build

The docker-qgis's settings are persisted in a "named docker volume",
``qgis-docker``. To wipe it clean, run ``docker-compose down -v``.

To run the full tests including coverage report and flake8::

  $ docker-compose run -e QT_QPA_PLATFORM=offscreen qgis-desktop make test

You can also just run pytest. You won't get the coverage report. You *can*
however then use one of the pytest options, like ``-x``, which aborts the test
at the first failure::

  $ docker-compose run --rm qgis-desktop pytest -x

To get a "coverage" report for the docstrings or to run flake8::

  $ docker-compose run --rm qgis-desktop make docstrings

To run black (standard pep8-compatible code formatting), isort (import
sorting) and flake8 (reporting missing imports and so), run::

  $ docker-compose run --rm qgis-desktop make beautiful

To run the QGIS application itself in the docker::

  $ xhost +local:docker  # you may need this to run the gui
  $ docker-compose run --rm qgis-desktop qgis


Release
-------

Make sure you have ``zest.releaser`` with ``qgispluginreleaser`` installed. The
``qgispluginreleaser`` ensures the metadata.txt, which is used by the qgis plugin
manager is also updated to the new version. To make a new release enter the following
commands and follow their steps::

    $ cd /path/to/the/plugin
    $ fullrelease

This creates a new release and tag on github. Additionally, a zip file
``threedi_results_analysis.<version>.zip`` is created. Github actions is configured to also
create this zip and upload it to https://plugins.lizard.net/ when a new tag is
created, using the ``upload-artifact.sh`` script.

You can also manually create a zip file of the current checked out code with the
following command::

    $ docker-compose run --rm qgis-desktop make zip

