# -*- coding: utf-8 -*-
from builtins import range
from builtins import str
from qgis.PyQt import QtCore
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QAbstractItemView
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QLabel
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtWidgets import QTableWidget
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.PyQt.QtWidgets import QWidget
from ThreeDiToolbox.threedi_schema_edits.controlled_structures import (
    ControlledStructures
)
from ThreeDiToolbox.utils.threedi_database import get_database_properties

import logging
import os


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


logger = logging.getLogger(__name__)


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)


except AttributeError:

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "ui",
        "controlled_structures_create_control_group_dialog.ui",
    )
)


class CreateControlGroupDialogWidget(QDialog, FORM_CLASS):
    def __init__(
        self,
        parent=None,
        db_key=None,
        control_group_id=None,
        dockwidget_controlled_structures=None,
    ):
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
        self.dockwidget_controlled_structures = dockwidget_controlled_structures
        self.db_key = db_key
        self.control_group_id = control_group_id
        # Show gui
        self.setupUi(self)
        self.tablewidget_input_control.setCellWidget(
            0, 0, self.combobox_input_control_measuring_group
        )
        self.tablewidget_input_control.setCellWidget(
            0, 1, self.combobox_input_rule_type
        )
        self.tablewidget_input_control.setCellWidget(0, 2, self.combobox_input_rule_id)
        self.tablewidget_input_control.setCellWidget(
            0, 6, self.pushbutton_input_control_new
        )
        self.update_ids()
        # Connect signals
        self.pushbutton_input_control_new.clicked.connect(self.create_new_control)
        self.combobox_input_rule_id.activated.connect(self.update_structure_ids)
        self.buttonbox.accepted.connect(self.on_accept)
        self.buttonbox.rejected.connect(self.on_reject)

    def on_accept(self):
        """Accept and run the Command.run_it method."""
        self.save_control_group()
        self.accept()

    def on_reject(self):
        """Cancel"""
        self.reject()
        logger.debug("Reject")

    def closeEvent(self, event):
        """
        Close widget, called by Qt on close
        :param event: QEvent, close event
        """

        self.buttonbox.accepted.disconnect(self.on_accept)
        self.buttonbox.rejected.disconnect(self.on_reject)

        event.accept()

    def update_ids(self):
        db = get_database_properties(self.db_key)
        control_structure = ControlledStructures(flavor=db["db_entry"]["db_type"])
        control_structure.start_sqalchemy_engine(db["db_settings"])
        # Measuring group id's
        self.combobox_input_control_measuring_group.clear()
        try:
            list_of_measure_group_ids = control_structure.get_attributes(
                table_name="v2_control_measure_group", attribute_name="id"
            )
            self.combobox_input_control_measuring_group.addItems(
                list_of_measure_group_ids
            )
        except Exception:
            pass
        # Rule id's
        try:
            self.combobox_input_rule_id.clear()
            list_of_rule_ids = control_structure.get_attributes(
                table_name="v2_control_table", attribute_name="id"
            )
            self.combobox_input_rule_id.addItems(list_of_rule_ids)
            self.update_structure_ids()
        except Exception:
            pass

    def update_structure_ids(self):
        db = get_database_properties(self.db_key)
        control_structure = ControlledStructures(flavor=db["db_entry"]["db_type"])
        control_structure.start_sqalchemy_engine(db["db_settings"])
        start_row = 0
        rule_id = self.combobox_input_rule_id.currentText()
        table_name = "v2_control_table"
        id_name = "id"
        where = "{id_name} = {value}".format(id_name=id_name, value=rule_id)
        try:
            # Structure type
            attribute_name = "target_type"
            structure_type = str(
                control_structure.get_features_with_where_clause(
                    table_name, attribute_name, where
                )[0][0]
            )
            structure = ""
            if structure_type == "v2_culvert":
                structure = "culvert"
            elif structure_type == "v2_pumpstation":
                structure = "pumpstation"
            elif structure_type == "v2_orifice":
                structure = "orifice"
            elif structure_type == "v2_weir":
                structure = "weir"
            self.tablewidget_input_control.setItem(
                start_row, 3, QTableWidgetItem(structure)
            )
            # Structure id
            attribute_name = "target_id"
            structure_id = str(
                control_structure.get_features_with_where_clause(
                    table_name, attribute_name, where
                )[0][0]
            )
            self.tablewidget_input_control.setItem(
                start_row, 4, QTableWidgetItem(structure_id)
            )
            # Action type
            attribute_name = "action_type"
            action_type = str(
                control_structure.get_features_with_where_clause(
                    table_name, attribute_name, where
                )[0][0]
            )
            self.tablewidget_input_control.setItem(
                start_row, 5, QTableWidgetItem(action_type)
            )
        # Empty v2_control
        except Exception:
            pass

    def create_new_control(self):
        """Create a new control."""
        # Always add a new control on top of the table.
        row_position = 1
        self.tablewidget_input_control.insertRow(row_position)
        self.tablewidget_input_control.setItem(
            row_position,
            0,
            QTableWidgetItem(self.combobox_input_control_measuring_group.currentText()),
        )
        self.tablewidget_input_control.setItem(
            row_position,
            1,
            QTableWidgetItem(self.combobox_input_rule_type.currentText()),
        )
        self.tablewidget_input_control.setItem(
            row_position, 2, QTableWidgetItem(self.combobox_input_rule_id.currentText())
        )
        self.tablewidget_input_control.setItem(
            row_position,
            3,
            QTableWidgetItem(self.tablewidget_input_control.item(0, 3).text()),
        )
        self.tablewidget_input_control.setItem(
            row_position,
            4,
            QTableWidgetItem(self.tablewidget_input_control.item(0, 4).text()),
        )
        self.tablewidget_input_control.setItem(
            row_position,
            5,
            QTableWidgetItem(self.tablewidget_input_control.item(0, 5).text()),
        )
        pushbutton_control_remove = QPushButton("Remove")
        pushbutton_control_remove.clicked.connect(self.remove_control_row)
        self.tablewidget_input_control.setCellWidget(
            row_position, 6, pushbutton_control_remove
        )

    def remove_control_row(self):
        """Remove a control row."""
        row_number = self.tablewidget_input_control.currentRow()
        if row_number != 0:
            self.tablewidget_input_control.removeRow(row_number)

    def save_control_group(self):
        """Save the control group."""
        # Get model
        db = get_database_properties(self.db_key)
        control_structure = ControlledStructures(flavor=db["db_entry"]["db_type"])
        control_structure.start_sqalchemy_engine(db["db_settings"])
        # Create a new tab for the Control tab in the dockwidget
        self.add_control_group_tab_dockwidget()
        # Save control group
        table_name = "v2_control_group"
        attributes = {
            "description": self.textedit_input_control_description.toPlainText(),
            "id": self.control_group_id,
            "name": self.lineedit_input_control_name.text(),
        }
        control_structure.insert_into_table(table_name, attributes)
        # Save controls
        table_name = "v2_control"
        amount_of_rows = self.tablewidget_input_control.rowCount()
        for row in range(amount_of_rows):
            # Get the new control id
            if row != 0:
                with control_structure.engine.connect() as con:
                    rs = con.execute("""SELECT MAX(id) FROM v2_control;""")
                    control_id = rs.fetchone()[0]
                    if not control_id:
                        control_id = 0
                    new_control_id = control_id + 1
                attributes = {
                    "control_type": "table",
                    "control_id": self.tablewidget_input_control.item(row, 2).text(),
                    "control_group_id": self.control_group_id,
                    "measure_group_id": self.tablewidget_input_control.item(
                        row, 0
                    ).text(),
                    "id": new_control_id,
                }
                control_structure.insert_into_table(table_name, attributes)
        # Setup the value of the table in the tab in the dockwidget
        self.setup_control_group_table_dockwidget()

    def add_control_group_tab_dockwidget(self):
        """
        Create a tab for the measure group within the Measure group tab
        in the dockwidget.
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        tab.setLayout(layout)

        label_field = QLabel(tab)
        label_field.setGeometry(10, 10, 741, 21)
        label_field.setText("Name: {}".format(self.lineedit_input_control_name.text()))

        label_field = QLabel(tab)
        label_field.setGeometry(10, 40, 741, 51)
        label_field.setText(
            "Description: {}".format(
                self.textedit_input_control_description.toPlainText()
            )
        )

        control_group_table = QTableWidget(tab)
        control_group_table.setGeometry(10, 100, 741, 181)
        control_group_table.insertColumn(0)
        control_group_table.setHorizontalHeaderItem(
            0, QTableWidgetItem("measuring_group_id")
        )
        control_group_table.insertColumn(1)
        control_group_table.setHorizontalHeaderItem(1, QTableWidgetItem("rule_type"))
        control_group_table.insertColumn(2)
        control_group_table.setHorizontalHeaderItem(2, QTableWidgetItem("rule_id"))
        control_group_table.insertColumn(3)
        control_group_table.setHorizontalHeaderItem(3, QTableWidgetItem("structure"))
        control_group_table.insertColumn(4)
        control_group_table.setHorizontalHeaderItem(4, QTableWidgetItem("structure_id"))
        control_group_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Add the tab to the tabwidget in the dockwidget
        self.dockwidget_controlled_structures.control_group_table = control_group_table

        self.dockwidget_controlled_structures.tab_control_view.insertTab(
            0, tab, "Control group: {}".format(str(self.control_group_id))
        )

    def setup_control_group_table_dockwidget(self):
        """
        Setup a tab for the measure group in the Measure group tab
        in the dockwidget.
        """
        amount_of_rows = self.tablewidget_input_control.rowCount()
        tablewidget_dockwidget = (
            self.dockwidget_controlled_structures.control_group_table
        )
        tablewidget_dialog = self.tablewidget_input_control
        for row in range(amount_of_rows):
            # Skip first row with comboboxes
            if row != 0:
                row_position = row - 1
                tablewidget_dockwidget.insertRow(row_position)
                measuring_group_id = str(tablewidget_dialog.item(row, 0).text())
                tablewidget_dockwidget.setItem(
                    row_position, 0, QTableWidgetItem(measuring_group_id)
                )
                rule_type = str(tablewidget_dialog.item(row, 1).text())
                tablewidget_dockwidget.setItem(
                    row_position, 1, QTableWidgetItem(rule_type)
                )
                rule_id = str(tablewidget_dialog.item(row, 2).text())
                tablewidget_dockwidget.setItem(
                    row_position, 2, QTableWidgetItem(rule_id)
                )
                structure = str(tablewidget_dialog.item(row, 3).text())
                tablewidget_dockwidget.setItem(
                    row_position, 3, QTableWidgetItem(structure)
                )
                structure_id = str(tablewidget_dialog.item(row, 4).text())
                tablewidget_dockwidget.setItem(
                    row_position, 4, QTableWidgetItem(structure_id)
                )
