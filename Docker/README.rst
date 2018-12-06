Introduction
============
This folder contains the docker containers for running QGIS desktop with
the ThreeDiToolbox requirements.


Developing
----------
The two folders qgis2 and qgis3 define image for QGIS 2 and for QGIS 3
respectively. Both depend on the base image `qgis-desktop:base`. Make sure you
are on the `QGIS2` branch when developing for QGIS 2. Development for
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

The building of the docker image takes the following arguments: USER_ID,
GROUP_ID and USER_NAME. A user in the docker is created with these arguments and
should correspond to your host UID, GID and USERNAME respectively if you want
the GUI to work within Docker.

Running tests::

    $ docker-compose run qgis-desktop make test
    $ docker-compose run qgis-desktop make pep8

You might want to persist qgis settings when restarting docker images. Qgis
saves these settings in the following locations:

    - /home/${USER}/.local/share/QGIS  # Qgis3
    - /home/${USER}/.qgis2/  # Qgis2

Create a `docker-compose.override.yml` and mount these volumes to persist the
settings.