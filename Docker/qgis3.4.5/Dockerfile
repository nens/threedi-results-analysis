FROM ubuntu:xenial
MAINTAINER Richard Boon <richard.boon@nelen-schuurmans.nl>
# Inspired by https://hub.docker.com/r/timcera/qgis-desktop-ubuntu/~/dockerfile/

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

ENV TZ Europe/Amsterdam

ARG uid=1000
ARG gid=1000
RUN groupadd -g $gid nens && useradd -lm -u $uid -g $gid nens

RUN echo $TZ > /etc/timezone \
    && apt-get -y update \
    && apt-get -y install --no-install-recommends \
        tzdata \
        dirmngr \
        apt-transport-https \
        python-software-properties \
        software-properties-common \
        wget \
        dbus \
        libhdf5-serial-dev \
        python-dev \
        build-essential \
        git \
        gosu \
    && add-apt-repository ppa:ubuntugis/ubuntugis-unstable \
    && rm /etc/localtime \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && apt-get clean \
    && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN dbus-uuidgen > /var/lib/dbus/machine-id

RUN echo "deb     https://qgis.org/ubuntugis-ltr xenial main" >> /etc/apt/sources.list
RUN echo "deb-src https://qgis.org/ubuntugis-ltr xenial main" >> /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key CAEB3DC3BDF7FB45

RUN apt-get -y update \
    && apt-get -y install --no-install-recommends \
        python3-dev \
        python3-pip \
        gdal-bin \
        qgis \
        # python3-qgis-common \
        python3-qgis \
        qgis-provider-grass \
        grass \
        pyqt5-dev-tools \
    && apt-get clean \
    && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip3 install --upgrade pip
RUN pip3 install setuptools

# Warning: modifications of requirements.txt do not automatically result in a
# newly build docker image! You have to fire off the re-build by hand.
ADD requirements.txt .
ADD requirements-dev.txt .
RUN pip3 install -r requirements.txt -U
RUN pip3 install -r requirements-dev.txt -U

# Remove once netcdf4 is completely removed.
ENV USE_SETUPCFG=0
ENV HDF5_INCDIR=/usr/include/hdf5/serial
ENV HDF5_LIBDIR=/usr/lib/x86_64-linux-gnu/hdf5/serial
RUN pip install netCDF4

# Make sure the h5py is compiled with the same HDF5 version of QGIS.
RUN pip3 uninstall h5py -y
ENV HDF5_DIR /usr/lib/x86_64-linux-gnu/hdf5/serial/
RUN pip3 install --no-binary=h5py h5py

# Add the qgis-core plugins (like 'db_manager') to the PYTHONPATH
ENV PYTHONPATH /usr/share/qgis/python/plugins

WORKDIR /home/nens/.local/share/QGIS/QGIS3/profiles/default/python/plugins/ThreeDiToolbox
CMD ["/usr/bin/qgis"]
USER nens
