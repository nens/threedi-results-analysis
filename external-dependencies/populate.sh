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
pip3 wheel --constraint ../constraints.txt --no-deps GeoAlchemy2 lizard-connector pyqtgraph threedigrid cached-property threedi-modelchecker click threedidepth alembic importlib-resources mako packaging colorama networkx condenser

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

wget https://files.pythonhosted.org/packages/a1/f1/cbded664cf2b68224ff1915e6fdc722dcd3c86143d72c31036a519653d6d/cftime-1.5.0.tar.gz

# Download windows wheels (cp39, win, amd64)
wget https://files.pythonhosted.org/packages/43/10/ead321694ef6adf0717ca4b3a7d4cf5b52e8456cc35c2b82abbd3777fd06/cftime-1.5.0-cp39-none-win_amd64.whl
wget https://files.pythonhosted.org/packages/92/2e/8a85d66cd4646a81027f3efbc17278beaa86fd351b5f1339a7a5b0d79c14/netCDF4-1.5.4-cp39-cp39-win_amd64.whl#sha256=223b84f8d2a148e889b1933944109bdecbefc097200ab42e8a66c967b1398e1b
wget https://files.pythonhosted.org/packages/6f/4c/1cdac6e8036f68d0a546118c78b35855b6e7ed8a7010d23ac48f1984051d/pygeos-0.12.0-cp39-cp39-win_amd64.whl
wget https://files.pythonhosted.org/packages/83/83/664c4e0c286d2dbf8294147493263e0991b37538e594b591504ddedf6881/threedigrid_builder-1.3.6-cp39-cp39-win_amd64.whl

# Download linux wheels (both cp38 and cp310)
wget https://files.pythonhosted.org/packages/d8/4b/ba9f72ae150d0a887e53b476ee29609c0ae1d28cd914bb66685a03ddfad2/cftime-1.5.0-cp39-cp39-manylinux_2_5_x86_64.manylinux1_x86_64.whl
wget https://files.pythonhosted.org/packages/90/0b/6f149c71dc7e035bb872c7f819127749d0a3c4388473f28be59ddb0b61fc/pygeos-0.12.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha256=962df97f937d6656ce9293e7072318e99860b0d41f61df9017551855a8bc188e
wget https://files.pythonhosted.org/packages/b4/64/01e6c648e6d0b305e0d1cdbe4fd96bc8d0fbae7cb14a929e5645cbe71524/pygeos-0.12.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha256=26fae3eabb83a15348c2c3f78892114aca9bc4efaa342ab2fa3fa39a85e05dc5

wget https://files.pythonhosted.org/packages/fa/fc/c012ec111ec8753369cbef9cc1e749bf3c9323106703909d36a9864e47e7/threedigrid_builder-1.3.6-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha256=f4b4feb237e7dead3adf4c6993d2411689c444d25783f26c7526a95a117f5472
wget https://files.pythonhosted.org/packages/1e/a4/cbb2e7c4565cfd63de2da6332a2ba2f7674637cf33b2643581afc5e11f82/threedigrid_builder-1.3.6-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha256=e33938002b5db6b1d2dba729d1673a932fc37f6d11e14dd607f7a77523ea2190
touch .generated.marker
