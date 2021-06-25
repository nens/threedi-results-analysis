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

# Download windows wheel (cp37, win, amd64) from https://pypi.org/simple/netcdf4/
wget https://files.pythonhosted.org/packages/85/6d/eafbe5378c6307a322f29a1afe2c1a19fca6822fb6bb5f8c5a84492d689d/netCDF4-1.5.7-cp37-cp37m-win_amd64.whl#sha256=1ee78d5c129fcfeafd6d4a6339984d6108dbabfb8a2cec651f9dc2132c792c78

touch .generated.marker
