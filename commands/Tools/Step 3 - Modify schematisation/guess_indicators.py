# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

from ThreeDiToolbox.commands.base.custom_command import CustomCommandBase
from ThreeDiToolbox.utils.guess_indicators import Guesser
from ThreeDiToolbox.utils.threedi_database import ThreediDatabase
from ThreeDiToolbox.utils.user_messages import messagebar_message
from ThreeDiToolbox.views.guess_indicator_dialog import GuessIndicatorDialogWidget

import inspect
import logging


logger = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):
    """
    """

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
        self.ts_datasource = kwargs.get("ts_datasource")
        self.tool_dialog_widget = None

    def run(self):
        self.show_gui()

    def show_gui(self):

        checks = []
        self.tool_dialog_widget = GuessIndicatorDialogWidget(
            checks=checks, command=self
        )
        self.tool_dialog_widget.exec_()  # block execution

    def run_it(self, action_list, only_empty_fields, db_set, db_type):

        db = ThreediDatabase(db_set, db_type)
        guesser = Guesser(db)
        msg = guesser.run(action_list, only_empty_fields)

        messagebar_message("Guess indicators ready", msg, duration=20)
        logger.info("Guess indicators ready.\n" + msg)
