Introduction
============
This folder contains the docker containers for running QGIS desktop with
the ThreeDiToolbox requirements.


Developing
----------
The two folders qgis2 and qgis3 define image for QGIS 2 and for QGIS 3
respectively. Both depend on the base image `qgis-desktop:base`. Make sure you
are on the `QGIS2` branch when developing for QGIS 2 (TODO). Development for
QGIS 3 should continue on master.

To build the image, first make sure you have the base image `qgis-desktop:base`.
You can build it with the following command::

    $ cd Docker/base
    $ docker build -t qgis-desktop:base .


Next go to the project root and enter the following command::

    $ docker-compose build

To start the QGIS application::

    $ docker-compose up

A QGIS application should start in a docker container. The docker container will
automatically mount the project in the QGIS plugin folder and mount your QGIS
localsettings. You might need to reload the ThreeDiToolbox plugin if you have
never installed it before. Do this via the `plugins` --> `Manage and Install
Plugins`.

Running tests
TODO

How to upload images
TODO

