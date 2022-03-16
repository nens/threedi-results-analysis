from qgis/qgis:release-3_22
RUN apt-get update && apt-get install -y python3-pyqt5.qtwebsockets wget python3-netcdf4 && apt-get clean
# RUN mkdir -p /tests_directory
COPY requirements-dev.txt /root
# coverage is already installed globally, so we need to force-install it explicitly
RUN pip3 install 'coverage>5' --force
RUN pip3 install -r /root/requirements-dev.txt
RUN qgis_setup.sh
WORKDIR /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/ThreeDiToolbox
# Note: we'll mount the current dir into this WORKDIR
