FROM qgis-desktop:base
MAINTAINER Richard Boon <richard.boon@nelen-schuurmans.nl>
# Inspired by https://hub.docker.com/r/timcera/qgis-desktop-ubuntu/~/dockerfile/

ARG USER_ID
ARG GROUP_ID
ARG USERNAME

# QGIS 3 (TODO: specify the version somewhere)
RUN echo "deb     https://qgis.org/ubuntugis xenial main" >> /etc/apt/sources.list
RUN echo "deb-src https://qgis.org/ubuntugis xenial main" >> /etc/apt/sources.list
RUN wget -O - https://qgis.org/downloads/qgis-2017.gpg.key | gpg --import
RUN gpg --export --armor CAEB3DC3BDF7FB45 | apt-key add -

RUN add-apt-repository ppa:ubuntugis/ubuntugis-unstable
RUN apt-get -y update \
    && apt-get -y install --no-install-recommends \
        python3-dev \
        python3-pip \
        gdal-bin \
        qgis \
        python-qgis \
        qgis-provider-grass \
        grass \
        pyqt5-dev-tools \
    && apt-get clean \
    && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip3 install --upgrade pip
RUN pip3 install setuptools

ADD requirements.txt .
ADD requirements-dev.txt .
RUN pip3 install -r requirements.txt -U
RUN pip3 install -r requirements-dev.txt -U

ENV USE_SETUPCFG=0
ENV HDF5_INCDIR=/usr/include/hdf5/serial
ENV HDF5_LIBDIR=/usr/lib/x86_64-linux-gnu/hdf5/serial
RUN pip install netCDF4

# Make sure the h5py is compiled with the same HDF5 version of QGIS.
RUN pip3 uninstall h5py -y
ENV HDF5_DIR /usr/lib/x86_64-linux-gnu/hdf5/serial/
RUN pip3 install --no-binary=h5py h5py

RUN groupadd -g $GROUP_ID $GROUP_ID
RUN useradd -m -d /home/$USERNAME --shell /bin/bash --uid $USER_ID --gid $GROUP_ID $USERNAME

WORKDIR /home/$USERNAME

# Add the qgis-core plugins (like 'db_manager') to the PYTHONPATH
ENV PYTHONPATH /usr/share/qgis/python/plugins

COPY Docker/qgis3/docker-entrypoint.sh /
RUN chmod u+x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/usr/bin/qgis"]
