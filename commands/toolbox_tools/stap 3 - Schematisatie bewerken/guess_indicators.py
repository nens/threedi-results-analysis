# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import logging
import inspect

from ThreeDiToolbox.views.guess_indicator_dialog import (
    GuessIndicatorDialogWidget)
from ThreeDiToolbox.commands.base.custom_command import (
    CustomCommandBase)
from ThreeDiToolbox.utils.threedi_database import (
    ThreediDatabase)
from ThreeDiToolbox.utils.guess_indicators import (
    Guesser)

logger = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):
    """
    Things to note:

    If you select a memory layer the behaviour will be different from clicking
    on a normal spatialite view. For example, NcStatsAgg will be used instead
    of NcStats.
    """

    class Fields(object):
        name = "Test script"
        value = 1

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._fields = sorted(
            [(name, cl) for name, cl in
             inspect.getmembers(self.Fields,
                                lambda a: not(inspect.isroutine(a)))
             if not name.startswith('__') and not name.startswith('_')])
        self.iface = kwargs.get('iface')
        self.ts_datasource = kwargs.get('ts_datasource')


    def run(self):
        self.show_gui()

    def show_gui(self):

        checks = []
        self.tool_dialog_widget = GuessIndicatorDialogWidget(
            checks=checks, command=self)
        self.tool_dialog_widget.exec_()  # block execution

    def run_it(self, action_list, only_empty_fields, db_set, db_type):

        # todo: check if database is empty, otherwise popup

        db = ThreediDatabase(db_set, db_type)
        guesser = Guesser(db)
        guesser.run(action_list, only_empty_fields)

        # todo: show logging

