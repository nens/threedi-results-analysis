import logging
import os

from threedi_modelchecker import exporters
from threedi_modelchecker.exporters import format_check_results
from threedi_modelchecker.model_checks import ThreediModelChecker

from ThreeDiToolbox.tool_commands.base.custom_command import CustomCommandBase
from ThreeDiToolbox.tool_commands.schematisation_checker.controller import \
    SchemaCheckerDialogWidget
from ThreeDiToolbox.utils.user_messages import pop_up_info

logger = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):

    def __init__(self, **kwargs):
        self.iface = kwargs.get('iface')
        self.modelchecker_widget = None
        self.plugin_dir = kwargs.get('plugin_dir')

    def show_gui(self):
        """Show a GUI as a frontend for this script."""
        # Gui should allow the user to select a sqlite or postgis database
        # gui takes this command as an argument
        # If user presses 'accept/ok', it runs `run_it`

        self.modelchecker_widget = SchemaCheckerDialogWidget(
            self.iface, command=self,
        )
        self.modelchecker_widget.exec_()  # block execution

    def run(self):
        """Entry point of CustomCommand. Either call show_gui or run_it here.
        """
        self.show_gui()

    def run_it(self, threedi_db):
        """Runs the script; this should contain the actual implementation of
        the script logic.
        """
        logger.info("Starting schematisation checker")

        try:
            threedi_db.check_connection()
        except Exception as e:
            pop_up_info(
                "Unable to start a connection with the database, please check"
                " the connection settings.")
            logger.exception("Unable to start a connection with the database")
            return

        output_filename = 'Model_errors.txt'
        output_file_path = os.path.join(self.plugin_dir, output_filename)

        model_errors = []
        model_checker = ThreediModelChecker(threedi_db)
        for check, error in model_checker.get_model_error_iterator():
            formatted_model_error = format_check_results(check, error)
            model_errors.append(formatted_model_error)
        exporters.export_to_file(model_errors, output_file_path)

        pop_up_info("Finished, see result in <a href='file:/%s'>%s</a>" %
                    (output_file_path, output_filename))
