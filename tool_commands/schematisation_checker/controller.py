from PyQt5.QtWidgets import QFileDialog
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog
from qgis._core import QgsApplication
from threedi_modelchecker.threedi_database import ThreediDatabase
from ThreeDiToolbox.utils.threedi_database import get_databases

import os


FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), "view.ui"))


class SchemaCheckerDialogWidget(QDialog, FORM_CLASS):
    STANDARD_OUTPUT_FILE_PATH = os.path.join(
        QgsApplication.qgisSettingsDirPath(), 'model-errors.csv'
    )

    def __init__(self, iface, command):
        super(SchemaCheckerDialogWidget, self).__init__()
        self.setupUi(self)
        self.iface = iface
        self.command = command
        self.available_databases = get_databases()
        self.outputfile_path_display.setText(self.STANDARD_OUTPUT_FILE_PATH)
        self.open_file_button.clicked.connect(self.on_open_file)
        self.database_combobox.addItems(list(self.available_databases.keys()))
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_cancel)

    def on_accept(self):
        selected_database_key = self.database_combobox.currentText()
        selected_db = self.available_databases.get(selected_database_key)
        db_type = selected_db.get("db_type")
        connection_settings = selected_db.get("db_settings")
        output_file_path = self.outputfile_path_display.text()

        threedi_db = ThreediDatabase(connection_settings, db_type=db_type)
        self.command.run_it(threedi_db, output_file_path)

    def on_cancel(self):
        self.close()

    def on_open_file(self):
        output_filename_path, _ = QFileDialog.getSaveFileName(
            self, "Save Result File", self.STANDARD_OUTPUT_FILE_PATH, "CSV (*.csv)"
        )
        if output_filename_path == '':
            output_filename_path = self.STANDARD_OUTPUT_FILE_PATH
        self.outputfile_path_display.setText(output_filename_path)

