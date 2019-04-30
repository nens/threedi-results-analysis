FROM ubuntu:bionic
MAINTAINER Richard Boon <richard.boon@nelen-schuurmans.nl>
# Inspired by https://hub.docker.com/r/timcera/qgis-desktop-ubuntu/~/dockerfile/

# Debian docker config settings.
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
# Don't let qgis grab python's import mechanism (which breaks pytest).
ENV QGIS_NO_OVERRIDE_IMPORT 1

# User handling to get proper non-root-owned files on linux.
ARG uid=1000
ARG gid=1000
RUN groupadd -g $gid nens && useradd -lm -u $uid -g $gid nens

# Set up ubuntu for the qgis repository
RUN apt-get update \
    && apt-get -y install --no-install-recommends \
        dirmngr \
        gpg-agent \
        software-properties-common \
    && rm -rf /var/lib/apt/lists/*
RUN echo "deb https://qgis.org/ubuntu-ltr bionic main" >> /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key CAEB3DC3BDF7FB45

# Now install the ubuntu packages we need.
RUN apt-get update \
    && apt-get -y install --no-install-recommends \
        python3-dev \
        python3-pip \
        gdal-bin \
        wget \
        qgis \
        python3-qgis \
        qgis-provider-grass \
        grass \
        pyqt5-dev-tools \
        dbus \
        libhdf5-serial-dev \
        python-dev \
        build-essential \
        git \
	strace \
	valgrind \
    && rm -rf /var/lib/apt/lists/*

# Seems to be a message bus used by Qt?
RUN dbus-uuidgen > /var/lib/dbus/machine-id

RUN pip3 install --upgrade pip
RUN pip3 install setuptools

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

# Add the qgis-core plugins (like 'db_manager') and our own plugin dir to the PYTHONPATH.
ENV PYTHONPATH /home/nens/.local/share/QGIS/QGIS3/profiles/default/python/plugins:/usr/share/qgis/python/plugins

# Default command if nothing is specified.
CMD ["/usr/bin/qgis"]

USER nens
RUN mkdir -p /home/nens/.local/share/QGIS/QGIS3/profiles/default/python/plugins/ThreeDiToolbox
WORKDIR /home/nens/.local/share/QGIS/QGIS3/profiles/default/python/plugins/ThreeDiToolbox
