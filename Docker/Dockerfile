FROM ubuntu:xenial
MAINTAINER Richard Boon <richard.boon@nelen-schuurmans.nl>
# Inspired by https://hub.docker.com/r/timcera/qgis-desktop-ubuntu/~/dockerfile/

## for apt to be noninteractive
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

ENV TZ Europe/Amsterdam

# Need to have apt-transport-https in-place before drawing from
# https://qgis.org
RUN echo $TZ > /etc/timezone \
    && apt-get -y update \
    && apt-get -y install --no-install-recommends \
       tzdata \
       dirmngr \
       apt-transport-https \
       python-software-properties \
       software-properties-common \
       wget \
    && add-apt-repository ppa:ubuntugis/ubuntugis-unstable \
    && rm /etc/localtime  \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && apt-get clean \
    && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# https://qgis.org/ubuntugis
RUN echo "deb     https://qgis.org/ubuntu xenial main" >> /etc/apt/sources.list
RUN echo "deb-src https://qgis.org/ubuntu xenial main" >> /etc/apt/sources.list

# Key for qgis ubuntugis
# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key CAEB3DC3BDF7FB45
RUN wget -O - https://qgis.org/downloads/qgis-2017.gpg.key | gpg --import
RUN gpg --export --armor CAEB3DC3BDF7FB45 | apt-key add -

RUN apt-get -y update \
    && apt-get -y install --no-install-recommends \
       python-pip \
       python-requests \
       python-numpy \
       python-pandas \
       python-scipy \
       python-matplotlib \
       python-h5py \
       python-pyside.qtwebkit \
       gdal-bin \
       qgis \
       python-qgis \
       qgis-provider-grass \
       grass \
       libhdf5-serial-dev \
       libnetcdf-dev \
       python-dev \
       build-essential \
       git \
    && apt-get clean \
    && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install netCDF4

ADD requirements-dev.txt .
RUN pip install -r requirements-dev.txt -U

# Called when the Docker image is started in the container
ADD start.sh /start.sh
RUN chmod 0755 /start.sh
CMD /start.sh
