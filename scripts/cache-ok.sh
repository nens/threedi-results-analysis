#!/bin/bash
# Check if the checksum for the docker image is OK.
# This means that the cached image is still valid.

set -e  # Fail immediately upon an error.
echo "Checking if all the files the image depends on are still the same..."
md5sum --check ~/docker-cache/docker-checksum
