"""Qt/QGIS debugging tools"""

def pyqt_set_trace():
    """Set a breakpoint in the Python debugger that works with Qt/QGIS.

    You need to start QGIS from the terminal for this.
    """
    import pdb
    from PyQt4.QtCore import pyqtRemoveInputHook
    pyqtRemoveInputHook()
    pdb.set_trace()
