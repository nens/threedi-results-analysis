Introduction
============
This folder contains the docker container for running QGIS desktop with
the ThreeDiToolbox installed.

To build the image and run the image enter the following commands::

    $ docker-compose build
    $ docker-compose up

A QGIS application should start in a docker container. The docker container will
automatically mount the project in the QGIS plugin folder and mount your QGIS
localsettings so custom settings are persistent. You might need to reload the
ThreeDiToolbox plugin if you have never installed it before. Do this via the
`plugins` --> `Manage and Install Plugins`.

To run the test enter the following command::

    $ docker-compose run -e QT_QPA_PLATFORM=offscreen qgis-desktop make test

Check PEP8::

    $ docker-compose run qgis-desktop make pep8

