#!/bin/sh

cd /home/$1

chown $1:$2 . -R

gosu $1:$2 /usr/bin/qgis