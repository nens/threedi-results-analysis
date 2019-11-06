#!/bin/bash
set -e
set -u

VERSION=$(grep "^version" metadata.txt| cut -d= -f2)

# ARTIFACTS_KEY should be set as env variable in the travis UI.
# TRAVIS_BRANCH is set automatically by travis
ARTIFACT=ThreeDiToolbox.${VERSION}.zip
PROJECT=ThreeDiToolbox

# Rename generated ThreeDiToolbox.zip to include version number.
cp ThreeDiToolbox.zip ${ARTIFACT}

curl -X POST \
     --retry 3 \
     -H "Content-Type: multipart/form-data" \
     -F key=${ARTIFACTS_KEY} \
     -F artifact=@${ARTIFACT} \
     -F branch=${TRAVIS_BRANCH} \
     https://artifacts.lizard.net/upload/${PROJECT}/
