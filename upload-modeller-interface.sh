#!/bin/bash
# Unlike upload-artifact.sh, which is run automatically by travis,
# this script is intended for manual use.
#
# Pass it the filename of the modeller interface executable as the first (and
# only) argument.
#
# MODELLER_INTERFACE_ARTIFACTS_KEY should be set as env variable in your shell.
# Reinout can give you the value to use.

set -e
set -u

ARTIFACT=$1

PROJECT=modeller-interface

curl -X POST \
     --retry 3 \
     -H "Content-Type: multipart/form-data" \
     -F key=${MODELLER_INTERFACE_ARTIFACTS_KEY} \
     -F artifact=@${ARTIFACT} \
     https://artifacts.lizard.net/upload/${PROJECT}/
