"""Module for setting up both python and qgis logging.

In our plugin code, we just want to use ``logger.info()`` and so. This ought
to end up in a logfile we can look at for debug purposes. Ideally, customers
can mail it to us.

Log messages also ought to end up in qgis's ``QgsMessageLog`` at the bottom of
the screen (if you've enabled it). We should set this up only for our own
messages, btw.

TODO: there probably needs to be some tweaking of log levels. Perhaps the
verbosity ought to be made configurable.

"""
import logging
import os

from qgis.core import Qgis
from qgis.core import QgsApplication
from qgis.core import QgsMessageLog

LOGFILE_NAME = "threedi-qgis-log.txt"


logger = logging.getLogger()


class QgisLogHandler(logging.Handler):
    """logging handler to get python log messages into the qgis interface."""

    def __init__(self, iface, *args, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)
        self.iface = iface

    def emit(self, record):
        """Show info/warn/error in message area; critical in the messagebar.
        """
        msg = self.format(record)
        if record.levelno >= logging.CRITICAL:
            level = Qgis.Critical
            self.iface.messageBar().pushMessage(record.funcName, msg, level, 0)
        elif record.levelno >= logging.WARNING:
            level = Qgis.Warning
        else:
            level = Qgis.Info

        QgsMessageLog.logMessage(msg, level=level)


def logfile_path():
    return os.path.join(QgsApplication.qgisSettingsDirPath(), LOGFILE_NAME)


def setup_logging(iface=None):
    """Set up python and qgis logging.

    All python logging should go to a log file. Every time we start, we start
    the file anew.

    It should also go to the console.

    The qgis logging inside the interface should only be what we ourselves
    want to log, to prevent us from adding messages from other plugins
    multiple times.

    """
    root_logger = logging.getLogger("")
    our_plugin_logger = logging.getLogger("ThreeDiToolbox")

    # Python's default log level is WARN, but we also want to see DEBUG
    # messages.
    root_logger.setLevel(logging.DEBUG)

    log_format = logging.Formatter("%(name)s %(levelname)s %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(log_format)
    root_logger.addHandler(stream_handler)

    qgis_log_handler = QgisLogHandler(iface)
    qgis_log_handler.setLevel(logging.INFO)
    qgis_log_handler.setFormatter(log_format)
    our_plugin_logger.addHandler(qgis_log_handler)

    file_handler = logging.FileHandler(logfile_path(), mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    logger.info("Started logfile: %s", logfile_path())
