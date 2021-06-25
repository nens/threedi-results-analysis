#!/bin/bash
export LANG=C.UTF-8
# Cleanup, we don't want old stuff to linger around.
rm *.whl
rm -rf *.egg
rm -rf SQLAlchemy*
rm -rf build

# Download pure python dependencies and convert them to wheels.
pip3 wheel --constraint ../constraints.txt --no-deps GeoAlchemy2 lizard-connector pyqtgraph threedigrid cached-property threedi-modelchecker click threedidepth alembic mako

# Start a build/ directory for easier later cleanup.
mkdir build
cd build

# Grab sqlalchemy. Use a small trick to get a universal egg.
pip3 download --no-binary :all: --constraint ../../constraints.txt SQLAlchemy
tar -xzf SQLAlchemy*gz
rm SQLAlchemy*gz
sed -i 's/distclass/\#distclass/g' SQLAlchemy*/setup.py
DISABLE_SQLALCHEMY_CEXT=1 pip wheel --no-deps --wheel-dir .. SQLAlchemy-*/

# Back up a level and clean up the build/ directory.
cd ..
rm -rf build

# Copy the custom compiled windows h5py to external dependencies
cp h5py/h5py-2.10.0-cp37-cp37m-win_amd64.whl .

# Copy the compiled windows scipy to external dependencies
cp scipy/scipy-1.5.2-cp37-cp37m-win_amd64.whl .

touch .generated.marker
