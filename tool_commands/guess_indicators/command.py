# (c) Nelen & Schuurmans, see LICENSE.rst.

from ThreeDiToolbox.tool_commands.custom_command_base import CustomCommandBase
from ThreeDiToolbox.tool_commands.guess_indicators import guess_indicator_dialog
from ThreeDiToolbox.tool_commands.guess_indicators import guess_indicators_utils
from ThreeDiToolbox.utils.threedi_database import ThreediDatabase
from ThreeDiToolbox.utils.user_messages import messagebar_message

import inspect
import logging


logger = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):
    """ """

    class Fields(object):
        name = "Guess indicator script"
        value = 1

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._fields = sorted(
            [
                (name, cl)
                for name, cl in inspect.getmembers(
                    self.Fields, lambda a: not (inspect.isroutine(a))
                )
                if not name.startswith("__") and not name.startswith("_")
            ]
        )
        self.iface = kwargs.get("iface")
        self.ts_datasources = kwargs.get("ts_datasources")
        self.tool_dialog_widget = None

    def run(self):
        self.show_gui()

    def show_gui(self):

        checks = []
        self.tool_dialog_widget = guess_indicator_dialog.GuessIndicatorDialogWidget(
            checks=checks, command=self
        )
        self.tool_dialog_widget.exec_()  # block execution

    def run_it(self, action_list, only_empty_fields, db_set, db_type):

        db = ThreediDatabase(db_set, db_type)
        guesser = guess_indicators_utils.Guesser(db)
        msg = guesser.run(action_list, only_empty_fields)

        messagebar_message("Guess indicators ready", msg, duration=20)
        logger.info("Guess indicators ready.\n" + msg)
