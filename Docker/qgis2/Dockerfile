FROM qgis-desktop:base
MAINTAINER Richard Boon <richard.boon@nelen-schuurmans.nl>
# Inspired by https://hub.docker.com/r/timcera/qgis-desktop-ubuntu/~/dockerfile/

ARG USER_ID
ARG GROUP_ID
ARG USERNAME

# QGIS 2.18 (TODO: specify the version somewhere)
RUN echo "deb     https://qgis.org/ubuntu xenial main" >> /etc/apt/sources.list
RUN echo "deb-src https://qgis.org/ubuntu xenial main" >> /etc/apt/sources.list
RUN wget -O - https://qgis.org/downloads/qgis-2017.gpg.key | gpg --import
RUN gpg --export --armor CAEB3DC3BDF7FB45 | apt-key add -

RUN apt-get -y update \
    && apt-get -y install --no-install-recommends \
       gdal-bin \
       qgis \
       python-qgis \
       python-h5py \
       qgis-provider-grass \
       grass \
    && apt-get clean \
    && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --upgrade pip
RUN pip install setuptools

ADD requirements-dev.txt .
RUN pip install -r requirements-dev.txt -U

RUN groupadd -g $GROUP_ID $GROUP_ID
RUN useradd -m -d /home/$USERNAME --shell /bin/bash --uid $USER_ID --gid $GROUP_ID $USERNAME

WORKDIR /home/$USERNAME

COPY docker-entrypoint.sh /
RUN chmod u+x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/usr/bin/qgis"]
