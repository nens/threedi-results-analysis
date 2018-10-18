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
       libhdf5-serial-dev \
       libnetcdf-dev \
       python-dev \
       build-essential \
       git \
    && apt-get clean \
    && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
