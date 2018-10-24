# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

from builtins import object
import logging
import inspect

from ThreeDiToolbox.views.import_sufhyd_dialog import (
    ImportSufhydDialogWidget)
from ThreeDiToolbox.commands.base.custom_command import (
    CustomCommandBase)
from ThreeDiToolbox.utils.threedi_database import (
    ThreediDatabase)
from ThreeDiToolbox.utils.import_sufhyd import (
    Importer)

logger = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):
    """
    Things to note:

    If you select a memory layer the behaviour will be different from clicking
    on a normal spatialite view. For example, NcStatsAgg will be used instead
    of NcStats.
    """

    class Fields(object):
        name = "Import sufhyd"
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
        self.tool_dialog_widget = None

    def run(self):
        self.show_gui()

    def show_gui(self):

        self.tool_dialog_widget = ImportSufhydDialogWidget(
            iface=self.iface, ts_datasource=self.ts_datasource, command=self)
        self.tool_dialog_widget.exec_()  # block execution

    def run_it(self, sufhyd_file, db_set, db_type):

        # todo: check if database is empty, otherwise popup

        db = ThreediDatabase(db_set, db_type)
        importer = Importer(sufhyd_file, db)
        importer.run_import()

        # todo: show logging
