#!/bin/bash
set -e
set -u

VERSION=$(grep "^version" ./threedi-results-analysis/metadata.txt | cut -d= -f2)

# ARTIFACTS_KEY should be set as env variable in the travis UI.
ARTIFACT=threedi-results-analysis.${VERSION}.zip
PROJECT=threedi-results-analysis

curl -X POST \
     --retry 3 \
     -H "Content-Type: multipart/form-data" \
     -F key=${ARTIFACTS_KEY} \
     -F artifact=@${ARTIFACT} \
     https://artifacts.lizard.net/upload/${PROJECT}/