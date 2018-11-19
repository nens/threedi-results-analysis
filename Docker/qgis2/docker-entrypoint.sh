#!/bin/sh

USERNAME=$(cut -d: -f1 /etc/passwd | tail -1)
USER_ID=$(id -u ${USERNAME})

if [ "$1" = '/usr/bin/qgis' ]; then
    chown $USERNAME:$USER_ID . -R
    sh gosu $USERNAME:$USER_ID /usr/bin/qgis
fi

gosu $USERNAME:$USER_ID "${@}"
