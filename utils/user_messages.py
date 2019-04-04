from __future__ import print_function

# If you don't include this import the test 'test_set_and_load_list'
# test_project will fail! WTF?
from builtins import object
from contextlib import contextmanager

try:
    from qgis.gui import QgsMessageBar
except ImportError:
    pass

from qgis.PyQt.QtWidgets import QMessageBox, QProgressBar
from qgis.PyQt.QtCore import Qt

from qgis.core import Qgis

try:
    from qgis.utils import iface
except Exception:
    iface = None


def log(msg, level="INFO"):
    """Shortcut for QgsMessageLog.logMessage function."""
    if level not in ["INFO", "CRITICAL", "WARNING"]:
        level = "INFO"
    level = level[0] + level[1:].lower()

    try:
        from qgis.core import QgsMessageLog
    except ImportError:
        print(msg)
        return

    loglevel = getattr(Qgis, level)
    QgsMessageLog.logMessage(msg, level=loglevel)
    if iface is None:
        print(msg)


def pop_up_info(msg="", title="Information", parent=None):
    """Display an info message via Qt box"""
    QMessageBox.information(parent, title, "%s" % msg)


def statusbar_message(msg=""):
    """Display message in status bar """
    if iface is not None:
        iface.mainWindow().statusBar().showMessage(msg)


def messagebar_message(title, msg, level=None, duration=0):
    """ Show message in the message bar (just above the map)
    args:
        title: (str) title of messages, showed bold in the start of the message
        msg: (str) message
        level: (int) INFO = 0, WARNING = 1, CRITICAL = 2, SUCCESS = 3. It is
            possible to use QgsMessage.INFO, etc
        duration: (int) how long this the message displays in seconds
    """
    try:
        from qgis.gui import QgsMessageBar

        if not level:
            level = Qgis.Info
    except ImportError:
        print("%s: %s" % (title, msg))

    if iface is not None:
        iface.messageBar().pushMessage(title, msg, level, duration)


def pop_up_question(msg="", title="", parent=None):
    """Message box question (Yes or No).

    Returns:
        True if 'Yes' was clicked, or False if 'No' was clicked.
    """
    reply = QMessageBox.question(
        parent, title, msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )

    return reply == QMessageBox.Yes


class StatusProgressBar(object):
    def __init__(self, maximum=100, message_title=""):

        self.maximum = maximum
        self.message_bar = iface.messageBar().createMessage(message_title, "")

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.message_bar.layout().addWidget(self.progress_bar)
        if iface is not None:
            iface.messageBar().pushWidget(self.message_bar, Qgis.MessageLevel())

        self.step_size = 1
        self.progress = 0

    def set_step_size(self, step_size):

        self.step_size = step_size

    def increase_progress(self, steps=1, message=None):

        self.progress += steps * self.step_size
        self.progress_bar.setValue(self.progress)
        if message:
            self.message_bar.setText(message)

    def __del__(self):
        if iface is not None:
            iface.messageBar().clearWidgets()


@contextmanager
def progress_bar(iface, min_value=1, max_value=100):
    """
    If you want more control over the layout of your progress bar and want
    to be able to add messages to it etc, use the StatusProgressBar object

    usage:
    with progress_bar(iface) as pb:
        pb.setValue(value)
    """
    # clear the message bar
    iface.messageBar().clearWidgets()
    # set a new message bar
    progressMessageBar = iface.messageBar()

    _progress_bar = QProgressBar()
    # Maximum is set to 100, making it easy to work with
    # percentage of completion
    _progress_bar.setMinimum(min_value)
    _progress_bar.setMaximum(max_value)
    # pass the progress bar to the message Bar
    progressMessageBar.pushWidget(_progress_bar)
    yield _progress_bar
    iface.messageBar().clearWidgets()
