from qgis/qgis:release-3_22
RUN apt-get update && apt-get install -y python3-pyqt5.qtwebsockets && apt-get clean
RUN mkdir /tests_directory
COPY . /tests_directory
RUN qgis_setup.sh ThreeDiToolbox
RUN pip3 install pytest
WORKDIR /tests_directory
