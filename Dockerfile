from qgis/qgis:release-3_22
RUN apt-get update && apt-get install -y python3-pyqt5.qtwebsockets wget && apt-get clean
# RUN mkdir -p /tests_directory
COPY requirements-dev.txt /root
RUN pip3 install -r /root/requirements-dev.txt
RUN qgis_setup.sh
WORKDIR /root/.local/share/QGIS/QGIS3/profiles/default
# Note: we'll mount the current dir into /root/.local/share/QGIS/QGIS3/profiles/default/ThreeDiToolbox
