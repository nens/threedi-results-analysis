Dependency handling README
==========================

Qgis comes bundled with several python libraries, but we need a few more. The
extra dependencies (as wheels and eggs) are placed in this
``external-dependencies/`` directory and bundled with the plugin.

The main ``ThreeDiToolbox/__init__.py`` (see :py:mod:`ThreeDiToolbox`) calls
``dependencies.py`` and installs the dependencies into the user profile's
``python/`` directory, so right next to ``python/plugins/``.

Qgis always places the python directory (and the plugins directory) on the
python path, see ``userpythonhome`` in
https://github.com/qgis/QGIS/blob/master/python/user.py


Python packages included on linux
---------------------------------

Assuming the ``ubuntu-ltr`` "qgis long term release" repository, the following
python packages are included when you apt-install qgis::

  python3-dateutil
  python3-future
  python3-gdal
  python3-httplib2
  python3-jinja2
  python3-markupsafe
  python3-matplotlib
  python3-numpy (via python3-gdal)
  python3-numpy-abi9 (via python3-gdal)
  python3-owslib
  python3-plotly
  python3-psycopg2
  python3-pygments
  python3-pyproj
  python3-requests
  python3-sip
  python3-six
  python3-tz
  python3-yaml

The ones we explicitly need are gdal and numpy.


Python packages included on windows
-----------------------------------

On windows, you can install qgis with osgeo4w, but you can also download a
standalone installer. This installer also uses osgeo4w. In qgis's script that
creates a windows installer with nsis
(https://github.com/qgis/QGIS/blob/master/ms-windows/osgeo4w/creatensis.pl),
you can see that it defaults to the ``qgis-full`` osgeo4w package and its
dependenies.

According to the description on
https://trac.osgeo.org/osgeo4w/wiki/PackagingInstructions, osgeo4w uses the
information in http://download.osgeo.org/osgeo4w/x86_64/setup.ini to build the
packages.

In the ``setup.ini``, we also see the ``qgis-ltr-full`` target, which is what
we need. In may 2019, the combination of ``qgis-ltr`` and ``qgis-ltr-full``
includes the following python packages::

  python3-core
  python3-exifread
  python3-future
  python3-gdal
  python3-httplib2
  python3-jinja2
  python3-markupsafe
  python3-matplotlib
  python3-mock
  python3-networkx
  python3-nose2
  python3-owslib
  python3-pillow
  python3-pip
  python3-plotly
  python3-psycopg2
  python3-pygments
  python3-pyodbc
  python3-pyparsing
  python3-pypiwin32
  python3-pyproj
  python3-python-dateutil
  python3-pytz
  python3-pyyaml
  python3-qscintilla
  python3-requests
  python3-scipy  # Note: depends on python3-numpy
  python3-shapely
  python3-simplejson
  python3-xlrd
  python3-xlwt


Extra dependencies we need
--------------------------

There is no ``setup.py`` in qgis plugins, so there's no default place to list
dependencies (and their versions). ``dependencies.py`` has the master list of
extra dependencies:

- pyqtgraph
- sqlalchemy
- geoalchemy2
- h5py
- lizard-connector
- threedigrid

Most are pip-installable just fine as they're pure python packages. There are
two exceptions:

- sqlalchemy has three small C modules for improved speed. There are python
  fallbacks, however. Our build scripts switch off the C modules, so we can
  treat sqlalchemy as a pure python package, simplifying the install.

- h5py. This is a package that really needs to match various other libraries
  in the system. For windows, it means a custom built package (which we
  include in the plugin). The windows package is built using the following 
  steps:
    - Add environment variable to your QGIS installation of choice: 
        ``HDF5_DIR=C:\Program Files\QGIS 3.4``
    - Then build wheel with local binaries to folder of interest:
        ``pip3 wheel -w . --no-binary=h5py --no-deps h5py==2.10.0``
  On linux, it means ``apt install python3-h5py``.

- Our ``threedidepth`` package needs netcdf4, this has the same
  problems as h5py. So on linux we need ``apt install
  python3-netcdf4``.
  TODO: windows build. Put it in a subdir like h5py and copy it to the
  directory of this readme in ``populate.sh``.
  

Our dependency handling
-----------------------

``dependencies.py`` (see :py:mod:`ThreeDiToolbox.dependencies`) can be called
directly, which generates a ``constraints.txt`` file for use with pip. The
``Makefile`` handles this for us: it updates the constraints file when the
python file changes.

The ``external-dependencies/`` directory (containing this README) has a
``populate.sh`` script. The ``Makefile`` runs it when needed. It populates the
directory with our dependencies so that we can bundle it with the plugin:

- ``populate.sh`` uses ``pip3 wheel`` to create universal wheel files for the
  four pure python libaries.

- It also downloads and extracts sqlalchemy. It makes a small change to its
  ``setup.py`` and builds a universal wheel by disabling C extension building.

- Lastly, it copies the custom built h5py package from the folder 'h5py'.

The :py:func:`ThreeDiToolbox.dependencies.ensure_everything_installed`
function is called by our main ``ThreeDiToolbox/__init__.py``:

- It first checks if the correct versions of our dependencies are
  installed. It doesn't matter where they're installed: system packages,
  qgis-bundled or in the profile directory.

- If something is missing, it calls python3's build-in "pip" to install it
  from the ``external-dependencies/`` directory into the user profile's
  ``python/`` directory.

As a last step, ``ThreeDiToolbox/__init__.py`` calls
:py:func:`ThreeDiToolbox.dependencies.check_importability` to make doubly sure
all dependencies are present. Not only the ones from
``external-dependencies/``, but also ``gdal`` and ``numpy`` to make sure
they're properly included with qgis.
