# -*- coding: utf-8 -*-
import os
import logging


from PyQt4 import QtCore
from PyQt4 import uic
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

from ThreeDiToolbox.threedi_schema_edits.controlled_structures import \
    ControlledStructures
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
    'controlled_structures_create_control_group_dialog.ui'))


class CreateControlGroupDialogWidget(QDialog, FORM_CLASS):

    def __init__(self, parent=None, db_key=None, control_group_id=None,
                 dockwidget_controlled_structures=None):
        """Constructor

        Args:
            parent: Qt parent Widget
            (str) db_key: The key of the database. It's a combination of
                          database type (postgres/ spatialite) and
                          name of the database.
            (int) control_group_id: The new id of the control group.
            (QDockWidget) dockwidget_controlled_structures:
                The main dockwidget of the control structures feature.
                This dockwidget is populated with the new control group
                upon pressing OK.
        """
        super(CreateControlGroupDialogWidget, self).__init__(parent)
        self.dockwidget_controlled_structures = \
            dockwidget_controlled_structures
        self.db_key = db_key
        self.control_group_id = control_group_id
        # Show gui
        self.setupUi(self)
        self.tablewidget_input_control.setCellWidget(
            0, 0, self.combobox_input_control_measuring_group)
        self.tablewidget_input_control.setCellWidget(
            0, 1, self.combobox_input_rule_type)
        self.tablewidget_input_control.setCellWidget(
            0, 2, self.combobox_input_rule_id)
        self.tablewidget_input_control.setCellWidget(
            0, 3, self.combobox_input_structure_table)
        self.tablewidget_input_control.setCellWidget(
            0, 4, self.combobox_input_structure_id)
        self.tablewidget_input_control.setCellWidget(
            0, 5, self.combobox_input_field)
        self.tablewidget_input_control.setCellWidget(
            0, 6, self.pushbutton_input_control_new)
        self.update_ids()
        # Connect signals
        self.pushbutton_input_control_new.clicked.connect(
            self.create_new_control)
        self.combobox_input_rule_id.activated.connect(
            self.update_structure_options)
        self.buttonbox.accepted.connect(self.on_accept)
        self.buttonbox.rejected.connect(self.on_reject)

    def on_accept(self):
        """Accept and run the Command.run_it method."""
        self.save_control_group()
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

    def update_ids(self):
        """Update the id's."""
        db = get_database_properties(self.db_key)
        control_structure = ControlledStructures(
            flavor=db["db_entry"]['db_type'])
        control_structure.start_sqalchemy_engine(db["db_settings"])
        # Measuring group id's
        self.combobox_input_control_measuring_group.clear()
        list_of_measure_group_ids = control_structure.get_attributes(
            table_name="v2_control_measure_group", attribute_name="id")  # read table name dynamically
        self.combobox_input_control_measuring_group.addItems(
            list_of_measure_group_ids)
        # Rule id's
        self.combobox_input_rule_id.clear()
        list_of_rule_ids = control_structure.get_attributes(
            table_name="v2_control_table", attribute_name="id")  # read table name dynamically
        self.combobox_input_rule_id.addItems(
            list_of_rule_ids)
        # Structure type
        self.combobox_input_structure_table.clear()
        rule_id = self.combobox_input_rule_id.currentText()
        with control_structure.engine.connect() as con:
            rs = con.execute(
                '''SELECT {attribute} FROM {table_name} WHERE {id_name}={value};'''
                .format(attribute="target_type",
                        table_name="v2_control_table",
                        id_name="id",
                        value=rule_id)
            )
            structure_type = rs.fetchone()[0]
        self.combobox_input_structure_table.addItem(structure_type)
        # Structure id
        self.combobox_input_structure_id.clear()
        with control_structure.engine.connect() as con:
            rs = con.execute(
                '''SELECT {attribute} FROM {table_name} WHERE {id_name}={value};'''
                .format(attribute="target_id",
                        table_name="v2_control_table",
                        id_name="id",
                        value=rule_id)
            )
            structure_id = rs.fetchone()[0]
        self.combobox_input_structure_id.addItem(str(structure_id))
        # Action type
        self.combobox_input_field.clear()
        with control_structure.engine.connect() as con:
            rs = con.execute(
                '''SELECT {attribute} FROM {table_name} WHERE {id_name}={value};'''
                .format(attribute="action_type",
                        table_name="v2_control_table",
                        id_name="id",
                        value=rule_id)
            )
            action_type = rs.fetchone()[0]
        self.combobox_input_field.addItem(str(action_type))

    def update_structure_options(self):
        """Update the structure options."""
        db = get_database_properties(self.db_key)
        control_structure = ControlledStructures(
            flavor=db["db_entry"]['db_type'])
        control_structure.start_sqalchemy_engine(db["db_settings"])
        # Structure type
        self.combobox_input_structure_table.clear()
        rule_id = self.combobox_input_rule_id.currentText()
        with control_structure.engine.connect() as con:
            rs = con.execute(
                '''SELECT {attribute} FROM {table_name} WHERE {id_name}={value};'''
                .format(attribute="target_type",
                        table_name="v2_control_table",
                        id_name="id",
                        value=rule_id)
            )
            structure_type = rs.fetchone()[0]
        self.combobox_input_structure_table.addItem(structure_type)
        # Structure id
        self.combobox_input_structure_id.clear()
        with control_structure.engine.connect() as con:
            rs = con.execute(
                '''SELECT {attribute} FROM {table_name} WHERE {id_name}={value};'''
                .format(attribute="target_id",
                        table_name="v2_control_table",
                        id_name="id",
                        value=rule_id)
            )
            structure_id = rs.fetchone()[0]
        self.combobox_input_structure_id.addItem(str(structure_id))
        # Action type
        self.combobox_input_field.clear()
        with control_structure.engine.connect() as con:
            rs = con.execute(
                '''SELECT {attribute} FROM {table_name} WHERE {id_name}={value};'''
                .format(attribute="action_type",
                        table_name="v2_control_table",
                        id_name="id",
                        value=rule_id)
            )
            action_type = rs.fetchone()[0]
        self.combobox_input_field.addItem(str(action_type))

    def create_new_control(self):
        """Create a new control."""
        # Always add a new control on top of the table.
        row_position = 1
        self.tablewidget_input_control.insertRow(row_position)
        self.tablewidget_input_control.setItem(
            row_position, 0, QTableWidgetItem(
                self.combobox_input_control_measuring_group.currentText()))
        self.tablewidget_input_control.setItem(
            row_position, 1,
            QTableWidgetItem(self.combobox_input_rule_type.currentText()))
        self.tablewidget_input_control.setItem(
            row_position, 2,
            QTableWidgetItem(self.combobox_input_rule_id.currentText()))
        self.tablewidget_input_control.setItem(
            row_position, 3, QTableWidgetItem(
                self.combobox_input_structure_table.currentText()))
        self.tablewidget_input_control.setItem(
            row_position, 4,
            QTableWidgetItem(self.combobox_input_structure_id.currentText()))
        self.tablewidget_input_control.setItem(
            row_position, 5,
            QTableWidgetItem(self.combobox_input_field.currentText()))
        pushbutton_control_remove = QPushButton("Remove")
        pushbutton_control_remove.clicked.connect(
            self.remove_control_row)
        self.tablewidget_input_control.setCellWidget(
            row_position, 6, pushbutton_control_remove)

    def remove_control_row(self):
        """Remove a control row."""
        row_number = self.tablewidget_input_control.currentRow()
        if row_number != 0:
            self.tablewidget_input_control.removeRow(row_number)

    def save_control_group(self):
        """Save the control group."""
        # Get model
        db = get_database_properties(self.db_key)
        control_structure = ControlledStructures(
            flavor=db["db_entry"]['db_type'])
        control_structure.start_sqalchemy_engine(db["db_settings"])
        # Get the new control_group_id
        with control_structure.engine.connect() as con:
            rs = con.execute(
                '''SELECT MAX(id) FROM v2_control_group;'''
            )
            control_group_id = rs.fetchone()[0]
            if not control_group_id:
                control_group_id = 0
            new_control_group_id = control_group_id + 1
        # Create a new tab for the Control tab in the dockwidget
        tab = QWidget()
        layout = QVBoxLayout(tab)
        tab.setLayout(layout)

        label_field = QLabel(tab)
        label_field.setGeometry(10, 10, 741, 21)
        label_field.setText("Name: {}".format(
            self.lineedit_input_control_name.text()))

        label_field = QLabel(tab)
        label_field.setGeometry(10, 40, 741, 51)
        label_field.setText("Description: {}".format(
            self.textedit_input_control_description.toPlainText()))

        control_group_table = QTableWidget(tab)
        control_group_table.setGeometry(10, 100, 741, 251)
        control_group_table.insertColumn(0)
        control_group_table.setHorizontalHeaderItem(
            0, QTableWidgetItem("measuring_group_id"))
        control_group_table.insertColumn(1)
        control_group_table.setHorizontalHeaderItem(
            1, QTableWidgetItem("rule_type"))
        control_group_table.insertColumn(2)
        control_group_table.setHorizontalHeaderItem(
            2, QTableWidgetItem("rule_id"))
        control_group_table.insertColumn(3)
        control_group_table.setHorizontalHeaderItem(
            3, QTableWidgetItem("structure"))
        control_group_table.insertColumn(4)
        control_group_table.setHorizontalHeaderItem(
            4, QTableWidgetItem("structure_id"))
        # Add the tab to the tabwidget in the dockwidget
        self.dockwidget_controlled_structures.control_group_table = \
            control_group_table

        self.dockwidget_controlled_structures\
            .tab_control_view.insertTab(
                0, tab, "Control group: {}".format(
                    str(new_control_group_id)))
        # Save control group
        table_name = "v2_control_group"
        attributes = {
            "description": self.textedit_input_control_description
            .toPlainText(),
            "id": new_control_group_id,
            "name": self.lineedit_input_control_name.text()
        }
        control_structure.insert_into_table(table_name, attributes)
        # Save controls
        table_name = "v2_control"
        amount_of_rows = self.tablewidget_input_control.rowCount()
        for row in range(amount_of_rows):
            # Get the new control id
            if row != 0:
                with control_structure.engine.connect() as con:
                    rs = con.execute(
                        '''SELECT MAX(id) FROM v2_control;'''
                    )
                    control_id = rs.fetchone()[0]
                    if not control_id:
                        control_id = 0
                    new_control_id = control_id + 1
                attributes = {
                    "control_type": "table",  # staat nu automatisch op table_control  # = rule_type
                    "control_id": self.tablewidget_input_control
                    .item(row, 2).text(),  # rule_id
                    "control_group_id": new_control_group_id,
                    "measure_group_id": self.tablewidget_input_control
                    .item(row, 0).text(),
                    "id": new_control_id
                }
                control_structure.insert_into_table(table_name, attributes)
        # Create new tab in Control tab in dockwidget
        amount_of_rows = self.tablewidget_input_control.rowCount()
        for row in range(amount_of_rows):
            # Skip first row with comboboxes
            if row != 0:
                row_position = row - 1
                self.dockwidget_controlled_structures.control_group_table.insertRow(row_position)
                measuring_group_id = str(self.tablewidget_input_control.item(row, 0).text())
                self.dockwidget_controlled_structures.control_group_table.setItem(row_position, 0, QTableWidgetItem(measuring_group_id))
                rule_type = str(self.tablewidget_input_control.item(row, 1).text())
                self.dockwidget_controlled_structures.control_group_table.setItem(row_position, 1, QTableWidgetItem(rule_type))
                rule_id = str(self.tablewidget_input_control.item(row, 2).text())
                self.dockwidget_controlled_structures.control_group_table.setItem(row_position, 2, QTableWidgetItem(rule_id))
                structure = str(self.tablewidget_input_control.item(row, 3).text())
                self.dockwidget_controlled_structures.control_group_table.setItem(row_position, 3, QTableWidgetItem(structure))
                structure_id = str(self.tablewidget_input_control.item(row, 4).text())
                self.dockwidget_controlled_structures.control_group_table.setItem(row_position, 4, QTableWidgetItem(structure_id))
        # Zie save in dockwidget
