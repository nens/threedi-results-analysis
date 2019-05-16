#!/bin/bash
# Cleanup, we don't want old stuff to linger around.
rm *.whl
rm -rf *.egg
rm -rf SQLAlchemy*
rm -rf build

# Download pure python dependencies and convert them to wheels.
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

touch .generated.marker
