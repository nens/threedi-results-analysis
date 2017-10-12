# -*- coding: utf-8 -*-
import os
import logging


from PyQt4 import QtCore
from PyQt4 import uic
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QPushButton

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

from ThreeDiToolbox.threedi_schema_edits.controlled_structures import \
    ControlledStructures
from ThreeDiToolbox.utils.constants import DICT_TABLE_ID
from ThreeDiToolbox.utils.constants import DICT_TABLE_NAMES
from ThreeDiToolbox.utils.threedi_database import get_databases
from ThreeDiToolbox.utils.threedi_database import get_database_properties

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
    def __init__(self, parent=None, db_key=None, table_control_id=None,
                 dockwidget_controlled_structures=None):
        """Constructor

        Args:
            parent: Qt parent Widget
            (str) db_key: The key of the database. It's a combination of
                          database type (postgres/ spatialite) and
                          name of the database.
            (int) table_control_id: The new id of the control table.
            (QDockWidget) dockwidget_controlled_structures:
                The main dockwidget of the control structures feature.
                This dockwidget is populated with the new table control
                upon pressing OK.
        """
        super(CreateTableControlDialogWidget, self).__init__(parent)
        # Show gui
        self.setupUi(self)

        self.table_control_id = table_control_id
        self.dockwidget_controlled_structures = \
            dockwidget_controlled_structures

        self.db_key = db_key
        self.databases = get_databases()
        self.db = get_database_properties(self.db_key)
        self.control_structure = ControlledStructures(
            flavor=self.db["db_entry"]['db_type'])
        self.setup_ids()
        self.connect_signals()

    def on_accept(self):
        """Accept and run the Command.run_it method."""
        self.save_table_control()
        self.accept()

    def on_reject(self):
        """Cancel"""
        self.reject()
        log.debug("Reject")

    def closeEvent(self, event):
        """
        Close widget, called by Qt on close
        :param event: QEvent, close event
        """

        self.buttonbox.accepted.disconnect(self.on_accept)
        self.buttonbox.rejected.disconnect(self.on_reject)

        event.accept()

    def setup_ids(self):
        """Setup the table control id, structure type and structure id."""
        # Set the id of the table control
        self.label_input_rule_id_number.setText(str(self.table_control_id))
        self.control_structure.start_sqalchemy_engine(self.db["db_settings"])
        # Set the structure type
        self.combobox_input_structure_table.clear()
        for key in DICT_TABLE_ID:
            self.combobox_input_structure_table.addItem(key)
        # Set the structure id's
        self.setup_structure_ids()

    def setup_structure_ids(self):
        """Setup the structure id's."""
        structure_type = self.combobox_input_structure_table.currentText()
        self.combobox_input_structure_id.clear()
        list_of_structure_ids = self.control_structure.get_attributes(
            table_name=DICT_TABLE_NAMES[structure_type],
            attribute_name=DICT_TABLE_ID[structure_type])
        self.combobox_input_structure_id.addItems(
            list_of_structure_ids)

    def connect_signals(self):
        """Connect the signals."""
        self.pushbutton_input_rule_add_row.clicked.connect(
            self.add_row)
        self.combobox_input_structure_table.activated.connect(
            self.setup_structure_ids)
        self.buttonbox.accepted.connect(self.on_accept)
        self.buttonbox.rejected.connect(self.on_reject)

    def add_row(self):
        """Add a row to the tablewidget."""
        # The row should be added on the top of the table
        row_position = 0
        self.tablewidget_input_rule_table_control.insertRow(row_position)
        pushbutton_remove_row = QPushButton("Remove")
        pushbutton_remove_row.clicked.connect(self.remove_row)
        self.tablewidget_input_rule_table_control.setCellWidget(
            row_position, 2, pushbutton_remove_row)

    def remove_row(self):
        """Remove a row from the tablewidget."""
        tablewidget = self.tablewidget_input_rule_table_control
        row_number = tablewidget.currentRow()
        tablewidget.removeRow(row_number)
