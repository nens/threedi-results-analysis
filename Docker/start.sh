#!/bin/bash

# Put any tasks you would like to have carried
# out when the container is first created here

groupadd -g $GROUP_ID qgis
useradd --shell /bin/bash --uid $USER_ID --gid $GROUP_ID $USER_NAME
su $USER_NAME -c "/usr/bin/qgis"
