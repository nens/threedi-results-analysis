

from PyQt4.QtGui  import QMessageBox, QProgressBar
from PyQt4.QtCore import Qt
from qgis.core import QgsMessageLog
from qgis.utils import iface


def log(msg, level='INFO'):
    """Shortcut for QgsMessageLog.logMessage function."""
    if level not in ['INFO', 'CRITICAL', 'WARNING']:
        level = 'INFO'
    loglevel = getattr(QgsMessageLog, level)
    QgsMessageLog.logMessage(msg, level=loglevel)

def pop_up_info(msg='', title='Information', parent=None):
    """Display an info message via Qt box"""
    QMessageBox.information(parent, title, '%s' % msg)

def statusbar_message(msg=''):
    """Display message in status bar """
    iface.mainWindow().statusBar().showMessage(msg)


class StatusProgressBar(object):

    def __init__(self, maximum=100, message_title=''):

        self.maximum = maximum
        self.message_bar = iface.messageBar().createMessage(message_title, '')

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.message_bar.layout().addWidget(self.progress_bar)
        iface.messageBar().pushWidget(self.message_bar, iface.messageBar().INFO)

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
        iface.messageBar().clearWidgets()
