#!/bin/bash
export LANG=C.UTF-8

# Fail immediately upon error exit code.
set -e

# Cleanup, we don't want old stuff to linger around.
rm -f *.whl
rm -rf *.egg
rm -f *.gz
rm -rf SQLAlchemy*
rm -rf build

# Download pure python dependencies and convert them to wheels.
pip3 wheel --constraint ../constraints.txt --no-deps GeoAlchemy2 lizard-connector pyqtgraph threedigrid cached-property threedi-modelchecker click threedidepth alembic mako packaging python-editor colorama networkx condenser

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
cp h5py/h5py-2.10.0-cp39-cp39-win_amd64.whl .

# Copy the compiled windows scipy to external dependencies
cp scipy/scipy-1.6.2-cp39-cp39-win_amd64.whl .

# Download windows wheel (cp39, win, amd64) from https://pypi.org/simple/netcdf4/
wget https://files.pythonhosted.org/packages/92/2e/8a85d66cd4646a81027f3efbc17278beaa86fd351b5f1339a7a5b0d79c14/netCDF4-1.5.4-cp39-cp39-win_amd64.whl#sha256=223b84f8d2a148e889b1933944109bdecbefc097200ab42e8a66c967b1398e1b
# Same with cftime, but now also for linux
wget https://files.pythonhosted.org/packages/43/10/ead321694ef6adf0717ca4b3a7d4cf5b52e8456cc35c2b82abbd3777fd06/cftime-1.5.0-cp39-none-win_amd64.whl
wget https://files.pythonhosted.org/packages/d8/4b/ba9f72ae150d0a887e53b476ee29609c0ae1d28cd914bb66685a03ddfad2/cftime-1.5.0-cp39-cp39-manylinux_2_5_x86_64.manylinux1_x86_64.whl
wget https://files.pythonhosted.org/packages/a1/f1/cbded664cf2b68224ff1915e6fdc722dcd3c86143d72c31036a519653d6d/cftime-1.5.0.tar.gz
wget https://files.pythonhosted.org/packages/6f/4c/1cdac6e8036f68d0a546118c78b35855b6e7ed8a7010d23ac48f1984051d/pygeos-0.12.0-cp39-cp39-win_amd64.whl
wget https://files.pythonhosted.org/packages/83/83/664c4e0c286d2dbf8294147493263e0991b37538e594b591504ddedf6881/threedigrid_builder-1.3.6-cp39-cp39-win_amd64.whl

touch .generated.marker
