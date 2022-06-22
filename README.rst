ThreeDiToolbox
==============

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

You need to install Qgis 3.16.5+ (the "long term release"). Either the
stand-alone installer or the osgeo4w install is fine. For osgeo4w, pick the
"qgis LTR full" version.

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
  $ apt-key adv --keyserver keyserver.ubuntu.com --recv-key 51F523511C7028C
  $ apt-get update
  $ apt-get install qgis python3-h5py

This installs qgis and the necessary ``h5py`` dependency.

Inside qgis, add https://plugins.lizard.net/plugins.xml as a package
index. Now you can install ThreeDiToolbox.

The extra dependencies that we need (apart from ``h5py``) are bundled with the
plugins and automatically installed into the ``python\`` directory of your
qgis profile.


Installation on OSX
-------------------

Running the plugin on OSX *should* be possible, but you need to make sure to
install qgis LTR with gdal, numpy and h5py.


Local development
-----------------

Local development happens with docker to make sure we're working in a nicely
isolated environment. So first build the docker::

  $ docker-compose build

If your user ID isn't ``1000``, you can run it like this::

  $ docker-compose build --build-arg uid=`id -u` --build-arg gid=`id -g`

The docker-qgis's settings are persisted in a "named docker volume",
``qgis-docker``. To wipe it clean, run ``docker-compose down -v``.

The tests that run on github cache the docker image that is being build
in order to shave 5 minutes off the test duration. The image is automatically
rebuild when the ``Dockerfile``, ``docker-compose.yml`` or one of the two
`requirements` files changes.

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


Release
-------

Make sure you have ``zest.releaser`` with ``qgispluginreleaser`` installed. The
``qgispluginreleaser`` ensures the metadata.txt, which is used by the qgis plugin
manager is also updated to the new version. To make a new release enter the following
commands and follow their steps::

    $ cd /path/to/the/plugin
    $ fullrelease

This creates a new release and tag on github. Additionally, a zip file
``ThreeDiToolbox.<version>.zip`` is created. Github actions is configured to also
create this zip and upload it to https://plugins.lizard.net/ when a new tag is
created, using the ``upload-artifact.sh`` script.

You can also manually create a zip file of the current checked out code with the
following command::

    $ docker-compose run --rm qgis-desktop make zip


Modeller interface release
--------------------------

We also provide the 3Di-modeller-interface for our users. This is standalone Qgis
installation for windows including the plugins ThreeDiToolbox and ThreeDiCustomizations
(https://github.com/nens/ThreeDiCustomizations). In the ``Makefile`` file you can specify
the version of Qgis you want to build with the ``QGIS_VERSION``. To build the installer
make sure you checked out the specific ThreediToolbox tag you want to build the
installer for. Also, a really clean checkout is important, so do something like this::

    $ mkdir /tmp/reallyclean
    $ cd /tmp/reallyclean
    $ git clone git@github.com:nens/ThreeDiToolbox.git
    $ cd ThreeDiToolbox
    $ git checkout 1.17    <== the tag that you want to release
    $ make installer

This process can take a while as it will download over 2GB of data. Eventually it
creates a ``3DiModellerInterface-OSGeo4W-<QGIS_VERSION>-Setup-x86_64.exe`` file.

Uploading the ``.exe`` is done locally with the shell script
``upload-modeller-interface.sh``. Look inside that file: you'll need to set one
environment variable ``MODELLER_INTERFACE_ARTIFACTS_KEY``. Afterwards, run it like
this::

  $ ./upload-modeller-interface.sh 3DiModellerInterface-OSGeo4W-<QGIS_VERSION>-Setup-x86_64.exe

It is uploaded to https://artifacts.lizard.net and there is some configuration
there that shows the upload directory as
https://docs.3di.live/modeller-interface-downloads/ (and similarly for
docs.staging.3di.live and the old docs.3di.lizard.net: it is all the same
upload directory).

You can clean up the files created for the 3Di-modeller-interface and the ``.exe`` file
with the following command::

    $ make clean-installer

The Makefile starts a ``makensis`` docker container from harbor.lizard.net that runs a perl script  
``create_qgis_3di_nsis.pl`` that is a modification of the original QGIS installer script. The code
for this docker image can be found at https://github.com/nens/3Di-modeller-interface-installer/.

