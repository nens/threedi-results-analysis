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
alembic \
cached-property \
click \
colorama \
condenser \
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
typing-extensions \
zipp \

# Start a build/ directory for easier later cleanup.
mkdir build
cd build

# Back up a level and clean up the build/ directory.
cd ..
rm -rf build

# Copy the custom compiled windows h5py to external dependencies
cp h5py/h5py-2.10.0-cp39-cp39-win_amd64.whl .

# Copy the compiled windows scipy to external dependencies
cp scipy/scipy-1.6.2-cp39-cp39-win_amd64.whl .

wget https://files.pythonhosted.org/packages/a1/f1/cbded664cf2b68224ff1915e6fdc722dcd3c86143d72c31036a519653d6d/cftime-1.5.0.tar.gz

# Copy pure wheels to prevent pip in docker (or Windows) to select platform dependent version
wget https://files.pythonhosted.org/packages/cd/84/66072ee12c3e79061f183c09a24be24f45bb1286600589640363d9d416b0/SQLAlchemy-2.0.6-py3-none-any.whl#sha256=c5d754665edea1ecdc79e3023659cb5594372e10776f3b3734d75c2c3ce95013

# Download windows wheels (cp39, win, amd64)
wget https://files.pythonhosted.org/packages/43/10/ead321694ef6adf0717ca4b3a7d4cf5b52e8456cc35c2b82abbd3777fd06/cftime-1.5.0-cp39-none-win_amd64.whl
wget https://files.pythonhosted.org/packages/72/e4/05217659d428f2772a6f78018587da68d5f23b73515075f57b29f87fa8f8/threedigrid_builder-1.8.0-cp39-cp39-win_amd64.whl
wget https://files.pythonhosted.org/packages/92/2e/8a85d66cd4646a81027f3efbc17278beaa86fd351b5f1339a7a5b0d79c14/netCDF4-1.5.4-cp39-cp39-win_amd64.whl#sha256=223b84f8d2a148e889b1933944109bdecbefc097200ab42e8a66c967b1398e1b
wget https://files.pythonhosted.org/packages/b2/8e/83d9e3bff5c0ff7a0ec7e850c785916e616ab20d8793943f9e1d2a987fab/shapely-2.0.0-cp39-cp39-win_amd64.whl
wget https://files.pythonhosted.org/packages/b3/89/1d3b78577a6b2762cb254f6ce5faec9b7c7b23052d1cdb7237273ff37d10/greenlet-2.0.2-cp39-cp39-win_amd64.whl#sha256=db1a39669102a1d8d12b57de2bb7e2ec9066a6f2b3da35ae511ff93b01b5d564

# Download linux wheels (cp310)
wget https://files.pythonhosted.org/packages/6e/11/a1f1af20b6a1a8069bc75012569d030acb89fd7ef70f888b6af2f85accc6/greenlet-2.0.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha256=d75209eed723105f9596807495d58d10b3470fa6732dd6756595e89925ce2470
wget https://files.pythonhosted.org/packages/06/07/0700e5e33c44bc87e19953244c29f73669cfb6f19868899170f9c7e34554/shapely-2.0.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
wget https://files.pythonhosted.org/packages/f1/52/c82afa01f9e8a62c68824ca18c4c2360fbcfb78d775c3705149dea4b3665/threedigrid_builder-1.8.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha256=8dee081e3a5f8f7df18538c7ab33678bc0291c752e482a868eef819cadcfe5b0

touch .generated.marker
