### TODO: Martijn add instructions for compiling h5py for the Windows qgis

HDF5_DIR = C:\Program Files\QGIS 3.4

pip3 wheel -w . --no-binary=h5py --no-deps --global-option=build_ext --global-option="-IC:\Program Files\QGIS 3.4\include" --global-option="-LC:\Program Files\QGIS 3.4\lib" h5py==2.10.0


