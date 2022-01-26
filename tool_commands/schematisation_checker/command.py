from qgis.core import Qgis
from sqlalchemy.exc import OperationalError
from threedi_modelchecker import errors
from threedi_modelchecker.model_checks import ThreediModelChecker
from ThreeDiToolbox.tool_commands.custom_command_base import CustomCommandBase
from ThreeDiToolbox.tool_commands.schematisation_checker import controller
from ThreeDiToolbox.utils.user_messages import messagebar_message
from ThreeDiToolbox.utils.user_messages import pop_up_info
from ThreeDiToolbox.utils.user_messages import progress_bar

import csv
import logging
import os


logger = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):
    def __init__(self, iface, ts_datasources):
        # ts_datasources is not used in this command. However due to the dynamic
        # importing and running of CustomCommands (see
        # ThreeDiToolbox/tool_commands/command_box.py) it is still required in the
        # constructor of a CustomCommand.
        self.iface = iface

    def show_gui(self):
        """Show SchemaChecker dialog"""
        self.modelchecker_widget = controller.SchemaCheckerDialogWidget(
            self.iface, command=self
        )
        self.modelchecker_widget.show()  # non-blocking

    def run(self):
        self.show_gui()

    def run_it(self, threedi_db, output_file_path):
        """Apply the threedi-modelchecker to `threedi_db`

        The connection to the `threedi_db` and its south_migration_history are first
        validated. Next, any model errors are written to `output_file_path` as csv file.
        """
        logger.info("Starting threedi-modelchecker")
        try:
            model_checker = ThreediModelChecker(threedi_db)
            model_checker.db.check_connection()
        except OperationalError as exc:
            logger.exception("Failed to start a connection with the database.")
            pop_up_info(
                "Something went wrong trying to connect to the database, please check"
                " the connection settings: %s" % exc.args[0]
            )
            return
        except errors.MigrationMissingError:
            logger.exception(
                "The selected 3Di model does not have the latest migration"
            )
            pop_up_info(
                "The selected 3Di model does not have the latest migration, please "
                "migrate your model to the latest version."
            )
            return

        _, output_filename = os.path.split(output_file_path)
        session = model_checker.db.get_session()
        total_checks = len(model_checker.config.checks)
        try:
            with progress_bar(self.iface, max_value=total_checks) as pb, open(
                output_file_path, "w", newline=""
            ) as output_file:
                writer = csv.writer(output_file)
                writer.writerow(
                    ["id", "table", "column", "value", "error_code", "level", "description"]
                )
                for i, check in enumerate(model_checker.checks(level="info")):
                    model_errors = check.get_invalid(session)
                    for error_row in model_errors:
                        writer.writerow(
                            [
                                error_row.id,
                                check.table.name,
                                check.column.name,
                                getattr(error_row, check.column.name),
                                check.error_code,
                                check.level.value,
                                check.description(),
                            ]
                        )
                    pb.setValue(i)
        except PermissionError:
            # PermissionError happens for example when a user has the file already open
            # with Excel on Windows, which locks the file.
            logger.error("Unable to write to file %s", output_file_path)
            pop_up_info(
                "Not enough permissions to write the file '%s'.\n\n"
                "The file might be used by another program. Please close all "
                "other programs using the file or select another output "
                "file." % output_file_path,
                title="Warning",
            )
            return

        logger.info("Successfully finished running threedi-modelchecker")
        messagebar_message(
            "Info",
            "Finished running schematisation-checker",
            level=Qgis.Success,
            duration=5,
        )
        return True
