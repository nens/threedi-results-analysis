FROM ubuntu:bionic
MAINTAINER Richard Boon <richard.boon@nelen-schuurmans.nl>
# Inspired by https://hub.docker.com/r/timcera/qgis-desktop-ubuntu/~/dockerfile/

# Debian docker config settings.
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

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
        curl \
    && rm -rf /var/lib/apt/lists/*
RUN echo "deb https://qgis.org/ubuntu-ltr bionic main" >> /etc/apt/sources.list
RUN curl -sSL 'http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x39877635093f2656019711faf7e06f06199ef2f2' | apt-key add -
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key F7E06F06199EF2F2

# Now install the ubuntu packages we need.
RUN apt-get update \
    && apt-get -y install --no-install-recommends \
        build-essential \
        dbus \
        gdal-bin \
        git \
        grass \
        less \
        pyqt5-dev-tools \
        python-dev \
        python3-dev \
        libhdf5-dev \
        python3-pip \
        python3-qgis \
        # Needed for the threedi-api-qgis-client:
        python3-pyqt5.qtwebsockets \
        # Needed for threedidepth:
        python3-netcdf4 \
        qgis \
        qgis-provider-grass \
        # strace is for debugging segfaults
        strace \
        unzip \
        wget \
        zip \
    && rm -rf /var/lib/apt/lists/*

# Seems to be a message bus used by Qt?
RUN dbus-uuidgen > /var/lib/dbus/machine-id

# Install some python libraries (partially already installed through apt)
ADD requirements-dev.txt .
RUN pip3 install -U pip setuptools
RUN pip3 install -r requirements-dev.txt
# Required for threedidepth
RUN pip3 install scipy==1.5.2

# Add the qgis-core plugins (like 'db_manager') and our own plugin dir and the
# python dirto the PYTHONPATH. This is needed for pytest and so to find the
# code. (Qgis finds it just fine without this PYTHONPATH, of course, it is set
# in Qgis's "python/user.py").
ENV PYTHONPATH /home/nens/.local/share/QGIS/QGIS3/profiles/default/python:/home/nens/.local/share/QGIS/QGIS3/profiles/default/python/plugins:/usr/share/qgis/python/plugins

# Default command if nothing is specified.
CMD ["/usr/bin/qgis"]

USER nens
RUN mkdir -p /home/nens/.local/share/QGIS/QGIS3/profiles/default/python/plugins/ThreeDiToolbox
RUN HDF5_DIR=/usr/lib/x86_64-linux-gnu/hdf5/serial/ pip3 install --target /home/nens/.local/share/QGIS/QGIS3/profiles/default/python --no-binary=h5py h5py==2.10.0
WORKDIR /home/nens/.local/share/QGIS/QGIS3/profiles/default/python/plugins/ThreeDiToolbox
