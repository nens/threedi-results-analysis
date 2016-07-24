import sys
sys.path.append('C:\\Program Files (x86)\\JetBrains\\PyCharm 2016.1.2\\debug-eggs\\pycharm-debug.egg')

import pydevd

pydevd.settrace('localhost',
                port=3105,
                stdoutToServer=True,
                stderrToServer=True,
                suspend=False)
