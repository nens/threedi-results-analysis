#!/bin/bash
# Check if the checksum for the docker image is OK.
# This means that the cached image is still valid.

set -e  # Fail immediately upon an error.
md5sum --check $HOME/docker-cache/docker-checksum
