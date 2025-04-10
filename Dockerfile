FROM qgis/qgis:final-3_34_4
RUN apt-get update && apt-get install -y python3-pyqt5.qtwebsockets wget python3-scipy python3-h5py zip && apt-get clean
# RUN mkdir -p /tests_directory
COPY requirements-dev.txt /root
COPY requirements-test.txt /root
# coverage is already installed globally, so we need to force-install it explicitly
RUN pip3 install 'coverage>6.1.1,<7.0' --force
RUN pip3 install -r /root/requirements-dev.txt
RUN qgis_setup.sh

# Copied the original PYTHONPATH and added the profile's python dir to
# imitate qgis' behaviour.
ENV PYTHONPATH=/usr/share/qgis/python/:/usr/share/qgis/python/plugins:/usr/lib/python3/dist-packages/qgis:/usr/share/qgis/python/qgis:/root/.local/share/QGIS/QGIS3/profiles/default/python
 
# Install the test dependencies in a folder in python path
# Retrieve constraints from dependency loader
ADD https://raw.githubusercontent.com/nens/nens-dependency-loader/refs/heads/main/dependencies.py /root/dependencies.py
RUN python3 /root/dependencies.py

RUN pip3 install -r /root/requirements-test.txt -c /root/constraints.txt --no-deps --upgrade --target /usr/share/qgis/python/plugins

# Note: we'll mount the current dir into this WORKDIR
WORKDIR /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/threedi_results_analysis
