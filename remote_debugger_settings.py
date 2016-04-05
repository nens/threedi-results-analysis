import sys
sys.path.append('C:\\OSGeo4W64\\apps\\Python27\\Lib\\site-packages\\pycharm-debug.egg')

import pydevd

pydevd.settrace('localhost',
                port=3105,
                stdoutToServer=True,
                stderrToServer=True,
                suspend=False)
