from qgis.core import QgsApplication
from sqlalchemy.exc import OperationalError
from threedi_modelchecker import errors
from threedi_modelchecker.model_checks import ThreediModelChecker
from ThreeDiToolbox.tool_commands.custom_command_base import CustomCommandBase
from ThreeDiToolbox.tool_commands.schematisation_checker import controller
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
        self.modelchecker_widget.exec_()

    def run(self):
        self.show_gui()

    def run_it(self, threedi_db):
        """Apply the threedi-modelchecker to `threedi_db`

        The connection to the `threedi_db` and its south_migration_history are first
        validated. Next, any model errors are written to a csv file.
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
                "migrate your model to the latest version. Download the latest "
                "version of the model here: <a href='https://3di.lizard.net/models/'>https://3di.lizard.net/models/</a>"  # noqa
            )
            return
        except errors.MigrationTooHighError:
            logger.exception(
                "The selected 3Di model has a higher migration than expected."
            )
            pop_up_info(
                "The 3Di model has a higher migration than expected, do you have "
                "the latest version of ThreediToolbox?"
            )
            return
        except errors.MigrationNameError:
            logger.exception(
                "Unexpected migration name, but migration id is matching. "
                "We are gonna continue for now and hope for the best."
            )

        output_filename = "model-errors.csv"
        output_file_path = os.path.join(
            QgsApplication.qgisSettingsDirPath(), output_filename
        )

        session = model_checker.db.get_session()

        total_checks = len(model_checker.config.checks)
        with progress_bar(self.iface, max_value=total_checks) as pb, open(
            output_file_path, "w", newline=""
        ) as output_file:
            writer = csv.writer(output_file)
            writer.writerow(
                ["id", "table", "column", "value", "description", "type of check"]
            )
            for i, check in enumerate(model_checker.checks()):
                model_errors = check.get_invalid(session)
                for error_row in model_errors:
                    writer.writerow(
                        [
                            error_row.id,
                            check.table.name,
                            check.column.name,
                            getattr(error_row, check.column.name),
                            check.description(),
                            check,
                        ]
                    )
                pb.setValue(i)

        logger.info("Successfully finished running threedi-modelchecker")
        pop_up_info(
            "Finished, see result in <a href='file:///%s'>%s</a>"
            % (output_file_path, output_filename)
        )
