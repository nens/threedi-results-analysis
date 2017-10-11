# -*- coding: utf-8 -*-
import os
import logging


from PyQt4 import QtCore
from PyQt4 import uic
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

log = logging.getLogger(__name__)


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), os.pardir, 'ui',
    'controlled_structures_create_table_control_dialog.ui'))


class CreateTableControlDialogWidget(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor

        Args:
            parent: Qt parent Widget
        """
        super(CreateTableControlDialogWidget, self).__init__(parent)
        # Show gui
        self.setupUi(self)
