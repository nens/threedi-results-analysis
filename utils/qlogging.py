import logging

from qgis.core import Qgis
from qgis.core import QgsMessageLog


LOGGING_TO_QGIS = {
    logging.INFO: Qgis.Info,
    logging.WARNING: Qgis.Warning,
    logging.CRITICAL: Qgis.Critical,
}


class QgisHandler(logging.Handler):
    def __init__(self, iface, *args, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)
        self.iface = iface

        # add references, because this somehow does not work directly,
        # something with the scope of the emit function (does this exists
        # in Python?)
        self.qgsMessageLog_ref = QgsMessageLog
        self.logging_ref = logging

    def emit(self, record):
        msg = self.format(record)
        if record.levelno >= logging.CRITICAL:
            level = Qgis.Critical
            self.iface.messageBar().pushMessage(record.funcName, msg, level, 0)
        elif record.levelno >= logging.WARNING:
            level = Qgis.Warning
        else:
            level = Qgis.Info

        QgsMessageLog.logMessage(msg, level=level)


def setup_logging(iface=None):

    logger = logging.getLogger("")  # set up a root logger

    ql = QgisHandler(iface)
    ql.setLevel(logging.INFO)

    # fh = logging.FileHandler('plugin_log.logger')
    # fh.setLevel(logging.WARNING)

    st = logging.StreamHandler()
    st.setLevel(logging.INFO)

    format = logging.Formatter("%(name)-12s - %(levelname)-8s - %(message)s")
    # fh.setFormatter(format)
    st.setFormatter(format)

    logger.addHandler(ql)
    # logger.addHandler(fh)
    logger.addHandler(st)

    logger.setLevel(logging.INFO)  # set level of root logger
