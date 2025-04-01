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
GeoAlchemy2 \
alembic \
cached-property \
click \
colorama \
condenser \
h5netcdf \
importlib-resources \
mako \
networkx \
packaging \
pyqtgraph \
python-editor \
threedi-mi-utils \
threedi-modelchecker \
threedi-schema \
threedidepth \
threedigrid \
typing-extensions \
zipp \
hydxlib \

# Start a build/ directory for easier later cleanup.
mkdir build
cd build

# Due to a very slow server the following dependencies are not downloaded if already present
# Download the custom compiled qgis version tar of h5py, create a tar from the distro subfolder
# Download h5py 3.8.0 for QGis versions before 3.40
if ! test -f ../h5py-3.8.0.tar; then
    wget http://download.osgeo.org/osgeo4w/v2/x86_64/release/python3/python3-h5py/python3-h5py-3.8.0-1.tar.bz2
    tar -xvf python3-h5py-3.8.0-1.tar.bz2
    tar -cf h5py-3.8.0.tar -C ./apps/Python39/Lib/site-packages/ .
    cp h5py-3.8.0.tar ..
else
    echo "h5py-3.8.0.tar already present, skipping download"
fi

# Download h5py 3.10.0 for QGis versions after 3.40
if ! test -f ../h5py-3.10.0.tar; then
    wget http://download.osgeo.org/osgeo4w/v2/x86_64/release/python3/python3-h5py/python3-h5py-3.10.0-1.tar.bz2
    tar -xvf python3-h5py-3.10.0-1.tar.bz2
    tar -cf h5py-3.10.0.tar -C ./apps/Python312/Lib/site-packages/ .
    cp h5py-3.10.0.tar ..
else
    echo "h5py-3.10.0.tar already present, skipping download"
fi

# as well as scipy
# Download scipy 1.10.1 for QGis versions before 3.40
if ! test -f ../scipy-1.10.1.tar; then
    wget http://download.osgeo.org/osgeo4w/v2/x86_64/release/python3/python3-scipy/python3-scipy-1.10.1-1.tar.bz2
    tar -xvf python3-scipy-1.10.1-1.tar.bz2
    tar -cf scipy-1.10.1.tar -C ./apps/Python39/Lib/site-packages/ .
    cp scipy-1.10.1.tar ..
else
    echo "scipy-1.10.1.tar already present, skipping download"
fi

# Download scipy 1.13.0 for QGis versions after 3.40
if ! test -f ../scipy-1.13.0.tar; then
    wget http://download.osgeo.org/osgeo4w/v2/x86_64/release/python3/python3-scipy/python3-scipy-1.13.0-1.tar.bz2
    tar -xvf python3-scipy-1.13.0-1.tar.bz2
    tar -cf scipy-1.13.0.tar -C ./apps/Python312/Lib/site-packages/ .
    cp scipy-1.13.0.tar ..
else
    echo "scipy-1.13.0.tar already present, skipping download"
fi

# Back up a level and clean up the build/ directory.
cd ..
rm -rf build

# Copy the compiled windows scipy to external dependencies
cp scipy/scipy-1.6.2-cp39-cp39-win_amd64.whl .

# Also copy the custom compiled windows h5py to external dependencies for QGis versions before 3.28.6
cp h5py/h5py-2.10.0-cp39-cp39-win_amd64.whl .

# Copy pure wheels to prevent pip in docker (or Windows) to select platform dependent version
wget https://files.pythonhosted.org/packages/cd/84/66072ee12c3e79061f183c09a24be24f45bb1286600589640363d9d416b0/SQLAlchemy-2.0.6-py3-none-any.whl#sha256=c5d754665edea1ecdc79e3023659cb5594372e10776f3b3734d75c2c3ce95013

# Download windows wheels (cp39, cp312, win, amd64)

wget https://files.pythonhosted.org/packages/31/bf/17962857bb5ccaab55837cba85dfa3d26bf94be1674582781dc4460fb0ca/threedigrid_builder-1.24.0-cp39-cp39-win_amd64.whl#sha256=5fa00e96623760fb3aebe25df51b3b878b317da750a40b97852f55ec546dff23
wget https://files.pythonhosted.org/packages/9d/eb/4f373b92089dbb7e8772b1a80f3e850b9e98dc15805c82449d46424d73de/threedigrid_builder-1.24.0-cp312-cp312-win_amd64.whl#sha=dbf0a4909d7d77d34e1db51c5e5c3baa2408b9e92ef8539a5f8f7f669ed08e10
wget https://files.pythonhosted.org/packages/b2/8e/83d9e3bff5c0ff7a0ec7e850c785916e616ab20d8793943f9e1d2a987fab/shapely-2.0.0-cp39-cp39-win_amd64.whl
wget https://files.pythonhosted.org/packages/7b/b3/857afd9dfbfc554f10d683ac412eac6fa260d1f4cd2967ecb655c57e831a/shapely-2.0.6-cp312-cp312-win_amd64.whl
wget https://files.pythonhosted.org/packages/43/21/a5d9df1d21514883333fc86584c07c2b49ba7c602e670b174bd73cfc9c7f/greenlet-3.1.1-cp312-cp312-win_amd64.whl#sha256=7124e16b4c55d417577c2077be379514321916d5790fa287c9ed6f23bd2ffd01
wget https://files.pythonhosted.org/packages/b3/89/1d3b78577a6b2762cb254f6ce5faec9b7c7b23052d1cdb7237273ff37d10/greenlet-2.0.2-cp39-cp39-win_amd64.whl#sha256=db1a39669102a1d8d12b57de2bb7e2ec9066a6f2b3da35ae511ff93b01b5d564
wget https://files.pythonhosted.org/packages/5f/d6/5f59a5e5570c4414d94c6da4c97731deab832cbd14eaf23189d54a92d1e1/cftime-1.6.2-cp39-cp39-win_amd64.whl#sha256=86fe550b94525c327578a90b2e13418ca5ba6c636d5efe3edec310e631757eea
wget https://files.pythonhosted.org/packages/17/98/ba5b4a2f37c6c88454b696dd5c7a4e76fc8bfd014364b47ddd7e2cec0fcd/cftime-1.6.4-cp312-cp312-win_amd64.whl#sha256=5b5ad7559a16bedadb66af8e417b6805f758acb57aa38d2730844dfc63a1e667

# Download linux wheels (cp38, cp310, cp312)
wget https://files.pythonhosted.org/packages/10/07/8cac304df78f158930282df9efacd17c13c53def91e674bac0346135419c/threedigrid_builder-1.24.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha=c9d2cf33e5791b910fb05a946fe4bf44ca5c731b5b504ef67e9a6e7c5988fb3d
wget https://files.pythonhosted.org/packages/f7/54/d6beb88bf21298c36a1fc86f622026b568c9d39d6380cfdb0f419f745194/threedigrid_builder-1.24.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha=e4fad6ddb127dc4b6557fd7fa88d15f1562b52a6de95ce047604191956b367a7
wget https://files.pythonhosted.org/packages/d5/7d/9a57e187cbf2fbbbdfd4044a4f9ce141c8d221f9963750d3b001f0ec080d/shapely-2.0.6-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
wget https://files.pythonhosted.org/packages/06/07/0700e5e33c44bc87e19953244c29f73669cfb6f19868899170f9c7e34554/shapely-2.0.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
wget https://files.pythonhosted.org/packages/4e/03/f3bcb7d96aef6d56b62e2f25996f161c05f92a45d452165be2007b756e0f/shapely-2.0.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
wget https://files.pythonhosted.org/packages/57/5c/7c6f50cb12be092e1dccb2599be5a942c3416dbcfb76efcf54b3f8be4d8d/greenlet-3.1.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha256=99cfaa2110534e2cf3ba31a7abcac9d328d1d9f1b95beede58294a60348fba36
wget https://files.pythonhosted.org/packages/6e/11/a1f1af20b6a1a8069bc75012569d030acb89fd7ef70f888b6af2f85accc6/greenlet-2.0.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha256=d75209eed723105f9596807495d58d10b3470fa6732dd6756595e89925ce2470
wget https://files.pythonhosted.org/packages/e1/17/d8042d82f44c08549b535bf2e7d1e87aa1863df5ed6cf1cf773eb2dfdf67/cftime-1.6.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha256=acb294fdb80e33545ae54b4421df35c4e578708a5ffce1c00408b2294e70ecef
wget https://files.pythonhosted.org/packages/44/51/bc9d47beee47afda1d335f05efa848dc403bd183344f03d431281518e8ab/cftime-1.5.0-cp38-cp38-manylinux_2_5_x86_64.manylinux1_x86_64.whl#sha256=7a820e16357dbdc9723b2059f7178451de626a8b2e5f80b9d91a77e3dac42133
wget https://files.pythonhosted.org/packages/04/56/233d817ef571d778281f3d639049b342f6ff0bb4de4c5ee630befbd55319/cftime-1.6.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl#sha256=f92f2e405eeda47b30ab6231d8b7d136a55f21034d394f93ade322d356948654

touch .generated.marker
