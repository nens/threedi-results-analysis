#!/bin/bash
# Cleanup, we don't want old stuff to linger around.
rm *.whl
rm -rf *.egg
rm -rf SQLAlchemy*
rm -rf build

# Download pure python dependencies and convert them to wheels.
pip3 wheel --constraint ../constraints.txt --no-deps GeoAlchemy2 lizard-connector pyqtgraph threedigrid cached-property threedi-modelchecker

# Start a build/ directory for easier later cleanup.
mkdir build
cd build

# Grab sqlalchemy. Use a small trick to get a universal egg.
pip3 download --constraint ../../constraints.txt SQLAlchemy
tar -xzf SQLAlchemy*gz
rm SQLAlchemy*gz
sed -i 's/distclass/\#distclass/g' SQLAlchemy*/setup.py
DISABLE_SQLALCHEMY_CEXT=1 pip wheel --no-deps --wheel-dir .. SQLAlchemy-*/

# Download windows 64 bit osgeo4w h5py egg.
wget http://download.osgeo.org/osgeo4w/x86_64/release/python3/python3-h5py/python3-h5py-2.7.0-1.tar.bz2
tar -xjf python3-h5py*.tar.bz2
mv apps/Python36/Lib/site-packages/h5py*egg ..
rm -rf apps
rm *.bz2
# Same with 32 bit egg
wget http://download.osgeo.org/osgeo4w/x86/release/python3/python3-h5py/python3-h5py-2.7.0-1.tar.bz2
tar -xjf python3-h5py*.tar.bz2
mv apps/Python36/Lib/site-packages/h5py*egg ..

# Back up a level and clean up the build/ directory.
cd ..
rm -rf build

touch .generated.marker
