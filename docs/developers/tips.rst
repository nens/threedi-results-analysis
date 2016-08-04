


First load the qgis library and then the pyqt4 dependancies. Otherwise the error:
 'ValueError: API 'QDate' has already been set to version 1' could appear.


Debugging with PyCharm
----------------------

For debugging under pycharm (under Windows):
- Start pycharm with the following .bat file (or comparable with the right links)::

    @echo off
    SET OSGEO4W_ROOT=C:\OSGeo4W64
    call "%OSGEO4W_ROOT%"\bin\o4w_env.bat
    call "%OSGEO4W_ROOT%"\apps\grass\grass-6.4.3\etc\env.bat
    @echo off
    path %PATH%;%OSGEO4W_ROOT%\apps\qgis\bin;

    set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis\python;
    set PYTHONPATH=%PYTHONPATH%;C:\Users\bastiaan.roos\.qgis2\python\plugins
    set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\Python27\Lib\site-packages
    set QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis
    cd %HOMEPATH%\development
    start "PyCharm aware of Quantum GIS" /B "C:\Program Files (x86)\JetBrains\PyCharm 2016.1.2\bin\pycharm.exe" %*



- Add to the project root the file 'remote_debugger_settings.py with the following code::

    import sys
    sys.path.append('C:\\Program Files (x86)\\JetBrains\\PyCharm 2016.1.2\\debug-eggs\\pycharm-debug.egg')

    import pydevd

    pydevd.settrace('localhost',
                    port=3105,
                    stdoutToServer=True,
                    stderrToServer=True,
                    suspend=False)
