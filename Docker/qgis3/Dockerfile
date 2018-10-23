FROM qgis-desktop:base
MAINTAINER Richard Boon <richard.boon@nelen-schuurmans.nl>
# Inspired by https://hub.docker.com/r/timcera/qgis-desktop-ubuntu/~/dockerfile/

ARG USER_ID
ARG GROUP_ID
ARG USER_NAME

# QGIS 3 (TODO: specify the version somewhere)
RUN echo "deb     https://qgis.org/ubuntugis xenial main" >> /etc/apt/sources.list
RUN echo "deb-src https://qgis.org/ubuntugis xenial main" >> /etc/apt/sources.list

# Key for qgis ubuntugis
# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key CAEB3DC3BDF7FB45
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
    && apt-get clean \
    && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip3 install --upgrade pip
RUN pip3 install setuptools

ADD requirements.txt .
ADD requirements-dev.txt .
RUN pip3 install -r requirements.txt -U
RUN pip3 install -r requirements-dev.txt -U

# Make sure the h5py is compiled with the same HDF5 version of QGIS.
RUN pip3 uninstall h5py -y
ENV HDF5_DIR /usr/lib/x86_64-linux-gnu/hdf5/serial/
RUN pip3 install --no-binary=h5py h5py

RUN groupadd -g $GROUP_ID qgis
RUN useradd -m -d /home/$USER_NAME --shell /bin/bash --uid $USER_ID --gid $GROUP_ID $USER_NAME
RUN chown $USER_ID:$GROUP_ID /home/$USER_NAME

USER $USER_NAME

CMD "/usr/bin/qgis"
