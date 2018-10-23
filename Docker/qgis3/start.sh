#!/bin/bash

# Put any tasks you would like to have carried
# out when the container is first created here

groupadd -g $GROUP_ID qgis
useradd -m -d /home/$USER_NAME --shell /bin/bash --uid $USER_ID --gid $GROUP_ID $USER_NAME
chown $USER_ID:$GROUP_ID /home/$USER_NAME
su $USER_NAME -c "/usr/bin/qgis"
