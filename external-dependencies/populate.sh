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
pip3 wheel --constraint ../constraints.txt --no-deps \
packaging \
GeoAlchemy2 \
SQLAlchemy \
alembic \
cached-property \
click \
colorama \
condenser \
greenlet \
hydxlib \
importlib-resources \
lizard-connector \
mako \
networkx \
packaging \
pyqtgraph \
python-editor \
threedi-modelchecker \
threedi-schema \
threedidepth \
threedigrid \
zipp \

# Start a build/ directory for easier later cleanup.
mkdir build
cd build

# Grab sqlalchemy. Use a small trick to get a universal egg.
#pip3 download --no-binary :all: --constraint ../../constraints.txt SQLAlchemy
#tar -xzf SQLAlchemy*gz
#rm SQLAlchemy*gz
#sed -i 's/distclass/\#distclass/g' SQLAlchemy*/setup.py
#DISABLE_SQLALCHEMY_CEXT=1 pip wheel --no-deps --wheel-dir .. SQLAlchemy-*/

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
wget https://files.pythonhosted.org/packages/b2/8e/83d9e3bff5c0ff7a0ec7e850c785916e616ab20d8793943f9e1d2a987fab/shapely-2.0.0-cp39-cp39-win_amd64.whl
wget https://files.pythonhosted.org/packages/72/e4/05217659d428f2772a6f78018587da68d5f23b73515075f57b29f87fa8f8/threedigrid_builder-1.8.0-cp39-cp39-win_amd64.whl

# Download linux wheels (both cp38 and cp310)
wget https://files.pythonhosted.org/packages/d8/4b/ba9f72ae150d0a887e53b476ee29609c0ae1d28cd914bb66685a03ddfad2/cftime-1.5.0-cp39-cp39-manylinux_2_5_x86_64.manylinux1_x86_64.whl
wget https://files.pythonhosted.org/packages/44/51/bc9d47beee47afda1d335f05efa848dc403bd183344f03d431281518e8ab/cftime-1.5.0-cp38-cp38-manylinux_2_5_x86_64.manylinux1_x86_64.whl#sha256=7a820e16357dbdc9723b2059f7178451de626a8b2e5f80b9d91a77e3dac42133

wget https://files.pythonhosted.org/packages/06/07/0700e5e33c44bc87e19953244c29f73669cfb6f19868899170f9c7e34554/shapely-2.0.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
wget https://files.pythonhosted.org/packages/4e/03/f3bcb7d96aef6d56b62e2f25996f161c05f92a45d452165be2007b756e0f/shapely-2.0.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
wget https://files.pythonhosted.org/packages/f1/52/c82afa01f9e8a62c68824ca18c4c2360fbcfb78d775c3705149dea4b3665/threedigrid_builder-1.8.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha256=8dee081e3a5f8f7df18538c7ab33678bc0291c752e482a868eef819cadcfe5b0
wget https://files.pythonhosted.org/packages/f5/ac/ff78d3ffaa2ef5bfaadaa0dab1798487a22ade0551f435b109b2a808b98a/threedigrid_builder-1.8.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha256=0c22a64709f01c10d38a2164c37791d2939f790c1d1a2bc8dbe9e8b639f756e2

touch .generated.marker
