

from PyQt4.QtGui  import QMessageBox
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