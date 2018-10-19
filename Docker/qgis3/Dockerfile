FROM qgis-desktop:base
MAINTAINER Richard Boon <richard.boon@nelen-schuurmans.nl>
# Inspired by https://hub.docker.com/r/timcera/qgis-desktop-ubuntu/~/dockerfile/

# QGIS 3 (TODO: specify the version somewhere)
RUN echo "deb     https://qgis.org/ubuntugis xenial main" >> /etc/apt/sources.list
RUN echo "deb-src https://qgis.org/ubuntugis xenial main" >> /etc/apt/sources.list

# Key for qgis ubuntugis
# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key CAEB3DC3BDF7FB45
RUN wget -O - https://qgis.org/downloads/qgis-2017.gpg.key | gpg --import
RUN gpg --export --armor CAEB3DC3BDF7FB45 | apt-key add -

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

ADD requirements-dev.txt .
RUN pip3 install -r requirements-dev.txt -U

# Called when the Docker image is started in the container
ADD start.sh /start.sh
RUN chmod 0755 /start.sh
CMD /start.sh
