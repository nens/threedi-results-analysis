#!/bin/bash
# Create checksums for the files the docker image depends on.
# A change in any one of them should result in a re-build of the image.

set -e  # Fail immediately upon an error.
md5sum \
    docker-compose.yml \
    Docker/qgis3.4.5/Dockerfile \
    requirements.txt \
    requirements-dev.txt \
    > $HOME/docker-cache/docker-checksum
