import logging
import os

from threedi_modelchecker import exporters
from threedi_modelchecker.exporters import format_check_results
from threedi_modelchecker.model_checks import ThreediModelChecker
from threedi_modelchecker.threedi_model.constants import LATEST_MIGRATION_ID

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
        """Show SchemaChecker dialog"""
        self.modelchecker_widget = SchemaCheckerDialogWidget(
            self.iface, command=self,
        )
        self.modelchecker_widget.exec_()

    def run(self):
        self.show_gui()

    def run_it(self, threedi_db):
        """Applies the threedi-modelchecker to `threedi_db`

        The connection to the `threedi_db` and its south_migration_history are first
        validated. Next, any model errors are written to a text file.
        """
        logger.info("Starting threedi-modelchecker")

        try:
            threedi_db.check_connection()
        except Exception as e:
            pop_up_info(
                "Unable to start a connection with the database, please check"
                " the connection settings.")
            logger.exception("Unable to start a connection with the database")
            return

        model_checker = ThreediModelChecker(threedi_db)

        if not model_checker.schema.is_latest_migration():
            user_message = provide_migration_details(model_checker)
            pop_up_info(user_message)
            return

        model_errors = []
        for check, error in model_checker.get_model_error_iterator():
            formatted_model_error = format_check_results(check, error)
            model_errors.append(formatted_model_error)
        output_filename = 'Model_errors.txt'
        output_file_path = os.path.join(self.plugin_dir, output_filename)
        exporters.export_to_file(model_errors, output_file_path)

        logger.info("Successfully finished running threedi-modelchecker")
        pop_up_info("Finished, see result in <a href='file:/%s'>%s</a>" %
                    (output_file_path, output_filename))


def provide_migration_details(model_checker):
    """Return a user-message about the `model_checker` migration.

    The migration is checked in the south_migration_history table and is checked
    against the threed-modelchecker expected migration.

    :param model_checker: (ThreediModelChecker)
    :return: (str) containing a user-message
    """
    if model_checker.schema.is_latest_migration():
        return "The selected 3Di model is up to date."
    migration_id, migration_name = model_checker.schema.get_latest_migration()
    logger.info("The selected 3Di model does not have the latest migration")
    logger.info(
        "Migration id: %s Migration name: %s Expected migration id: %s",
        migration_id,
        migration_name,
        LATEST_MIGRATION_ID,
    )
    if migration_id < LATEST_MIGRATION_ID:
        message = (
            "The selected 3Di model does not have the latest migration, please "
            "migrate your model to the latest version."
        )
    elif migration_id > LATEST_MIGRATION_ID:
        message = (
            "The 3Di model has a higher migration than expected, do you have"
            "the latest version of ThreediToolbox?"
        )
    else:
        raise AssertionError(
            "This should not be possible, get_latest_migration contains a bug"
        )
    return message
