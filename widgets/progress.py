from contextlib import contextmanager

from PyQt4 import QtGui

@contextmanager
def progress_bar(iface, min_value=1, max_value=100):
    # clear the message bar
    iface.messageBar().clearWidgets()
    # set a new message bar
    progressMessageBar = iface.messageBar()

    _progress_bar = QtGui.QProgressBar()
    # Maximum is set to 100, making it easy to work with
    # percentage of completion
    _progress_bar.setMinimum(min_value)
    _progress_bar.setMaximum(max_value)
    # pass the progress bar to the message Bar
    progressMessageBar.pushWidget(_progress_bar)
    yield _progress_bar
    iface.messageBar().clearWidgets()
