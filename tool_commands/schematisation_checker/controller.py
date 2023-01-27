from qgis.core import QgsApplication
from qgis.PyQt import QtWidgets
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtGui import QDesktopServices
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QFileDialog
from threedi_schema import ThreediDatabase
from ThreeDiToolbox.utils.threedi_database import get_databases

import os


FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), "view.ui"))


class SchemaCheckerDialogWidget(QDialog, FORM_CLASS):
    STANDARD_OUTPUT_FILE_PATH = os.path.join(
        QgsApplication.qgisSettingsDirPath(), "model-errors.csv"
    )

    def __init__(self, iface, command):
        super(SchemaCheckerDialogWidget, self).__init__()
        self.setupUi(self)
        self.iface = iface
        self.command = command
        self.available_databases = get_databases()
        self.save_file_location_display.setText(self.STANDARD_OUTPUT_FILE_PATH)
        self.save_file_location_button.clicked.connect(self.on_save)
        self.database_combobox.addItems(list(self.available_databases.keys()))
        self.run_button.clicked.connect(self.on_run)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.open_result_button.clicked.connect(self.on_open)

    def on_run(self):
        """Handler when user presses the 'run' button.

        Starts the threedi-modelchecker script on the selected database and writes the
        results to the selected outputfile."""
        selected_database_key = self.database_combobox.currentText()
        selected_db = self.available_databases.get(selected_database_key)
        connection_settings = selected_db.get("db_settings")
        selected_db_filepath = connection_settings["db_path"]
        output_file_path = self.save_file_location_display.text()

        threedi_db = ThreediDatabase(selected_db_filepath)
        success = self.command.run_it(threedi_db, output_file_path)
        if success:
            self.open_result_button.setEnabled(True)

    def on_cancel(self):
        self.close()

    def on_save(self):
        """Handler when user presses the 'Save'button.

        Opens a QFileDialog to allow the user to select a file where the results are
        saved to."""
        output_filename_path, _ = QFileDialog.getSaveFileName(
            self, "Save Result File", self.STANDARD_OUTPUT_FILE_PATH, "CSV (*.csv)"
        )
        if output_filename_path == "":
            output_filename_path = self.STANDARD_OUTPUT_FILE_PATH
        self.save_file_location_display.setText(output_filename_path)

    def on_open(self):
        """Handler when user presses the 'Open' button.

        Opens the result file with the user's application preferences"""
        file_path = self.save_file_location_display.text()
        file_url = QUrl("file:///%s" % file_path)
        QDesktopServices.openUrl(file_url)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    SchemaCheckerDialog = SchemaCheckerDialogWidget(iface=None, command=None)
    SchemaCheckerDialog.show()
    sys.exit(app.exec_())
