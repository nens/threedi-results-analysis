#!/bin/bash
rm *.whl
rm -rf SQLAlchemy*
rm -rf build
pip3 wheel --constraint ../constraints.txt --no-deps GeoAlchemy2 lizard-connector pyqtgraph threedigrid

mkdir build
cd build

pip3 download --constraint ../../constraints.txt SQLAlchemy
tar -xvf SQLAlchemy*gz
rm SQLAlchemy*gz
sed -i 's/distclass/\#distclass/g' SQLAlchemy*/setup.py
DISABLE_SQLALCHEMY_CEXT=1 pip wheel --no-deps --wheel-dir .. SQLAlchemy-*/

cd ..
rm -rf build
