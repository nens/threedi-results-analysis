import logging
from qgis.core import QgsMessageLog


class QGisHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)

        QgsMessageLog.logMessage(msg, level=record.levelname)

        if (record.levelno >= logging.ERROR and
                self.iface is not None):
            if record.levelno == logging.CRITICAL:
                level = 2  # error
            else:
                level = 1  # warning

            self.iface.messageBar().pushMessage(
                    record.funcName, msg, level, 0)


def setup_logging(iface=None):

    log = logging.getLogger('')

    ql = QGisHandler(iface)
    ql.setLevel(logging.INFO)

    fh = logging.FileHandler('plugin_log.log')
    fh.setLevel(logging.WARNING)

    st = logging.StreamHandler()
    st.setLevel(logging.INFO)

    format = logging.Formatter('%(name)-12s - %(levelname)-8s - %(message)s')
    fh.setFormatter(format)
    st.setFormatter(format)

    log.addHandler(ql)
    # log.addHandler(fh)
    log.addHandler(st)
