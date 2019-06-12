from pathlib import Path
from PyQt5.QtWidgets import QDialog
from qgis.core import QgsProject
from qgis.PyQt import uic
from ThreeDiToolbox.tool_commands.create_breach_locations import breach_location

import logging


logger = logging.getLogger(__name__)

ui_file = Path(__file__).parent / "breach_location_dialog.ui"
assert ui_file.is_file()
FORM_CLASS, _ = uic.loadUiType(ui_file)


class CreateBreachLocationsDialogWidget(QDialog, FORM_CLASS):
    def __init__(self, parent=None, command=None):
        """Constructor
        Args:
            parent: Qt parent Widget
            iface: QGiS interface
            ts_datasource: TimeseriesDatasourceModel instance
            command: Command instance with a run_it method which will be called
                     on acceptance of the dialog
        """
        super().__init__(parent)
        self.setupUi(self)
        # default maximum for QSpinBox is 99, so setValue is limited to 99.
        # That's why we set the Maximum to 5000
        self.spinbox_search_distance.setMaximum(5000)
        self.spinbox_search_distance.setMinimum(2)
        self.spinbox_levee_distace.setMaximum(5000)
        self.spinbox_levee_distace.setMinimum(1)
        self.setWindowTitle("Create breach locations")
        tool_help = """Move connected points across the nearest levee. You can limit 
        your point set to your current selection. Using the dry-run option will not 
        save the new geometries to the database table yet but will store them to a 
        memory layer called 'temp_connected_pnt'. Like this you can test your settings 
        first before actually applying them to your model. Using the 'dry-run' option 
        thus is highly recommended."""
        self.help_text_browser.setText(
            tool_help.replace("        ", "").replace("\n", " ").replace("\r", "")
        )
        connected_pnt_lyr = QgsProject.instance().mapLayersByName("v2_connected_pnt")
        # automatically pre-select the right layer if present
        if connected_pnt_lyr:
            lyr = connected_pnt_lyr[0]
            self.connected_pny_lyr_box.setLayer(lyr)

        self.command = command
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)

    def on_accept(self):
        """Accept and run the Command.run_it method."""

        breach_loc = breach_location.BreachLocation(
            search_distance=self.spinbox_search_distance.value(),
            distance_to_levee=self.spinbox_levee_distace.value(),
            use_selection=self.checkBox_feat.isChecked(),
            is_dry_run=self.checkBox_dry_run.isChecked(),
            connected_pnt_lyr=self.connected_pny_lyr_box.currentLayer(),
        )
        self.command.run_it(breach_loc, self.checkBox_auto_commit.isChecked())
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
        event.accept()
