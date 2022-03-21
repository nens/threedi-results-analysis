from qgis.PyQt.QtWidgets import QMessageBox, QProgressBar
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsMessageLog, Qgis
import cProfile
import time
import os
import sys


DOT_EXE = "dot"
if sys.platform == "win32" or os.name == "os2":
    DOT_EXE += ".exe"


def is_installed(executable):
    from distutils.spawn import find_executable
    return find_executable(executable) is not None


def render_profile(profile_output, profile_format):
    """ render diagram's source .dot file using the "dot" tool from graphviz """
    cmd = "gprof2dot -f pstats {} | ".format(profile_output)
    cmd += DOT_EXE + " -T{} -o {}.{}".format(profile_format, profile_output, profile_format)
    if os.system(cmd) != 0:
        raise Exception("Profiling rendering failed!")


class UserCommunication(object):
    """
    Class for communication with user.
    """

    def __init__(self, iface, context):
        self.iface = iface
        self.context = context
        self.profiles = dict()
        self.timers = dict()

    def show_info(self, msg, parent=None, context=None):
        if self.iface is not None:
            parent = parent if parent is not None else self.iface.mainWindow()
            context = self.context if context is None else context
            QMessageBox.information(parent, context, msg)
        else:
            print(msg)

    def show_warn(self, msg, parent=None, context=None):
        if self.iface is not None:
            parent = parent if parent is not None else self.iface.mainWindow()
            context = self.context if context is None else context
            QMessageBox.warning(parent, context, msg)
        else:
            print(msg)

    def log(self, msg, level):
        if self.iface is not None:
            QgsMessageLog.logMessage(msg, self.context, level)
        else:
            print(msg)

    def log_info(self, msg):
        if self.iface is not None:
            try:
                QgsMessageLog.logMessage(msg, self.context, Qgis.Info)
            except TypeError:
                QgsMessageLog.logMessage(repr(msg), self.context, Qgis.Info)
        else:
            print(msg)

    def bar_error(self, msg, dur=5):
        if self.iface is not None:
            self.iface.messageBar().pushMessage(self.context, msg, level=Qgis.Critical, duration=dur)
        else:
            print(msg)

    def bar_warn(self, msg, dur=5):
        if self.iface is not None:
            self.iface.messageBar().pushMessage(self.context, msg, level=Qgis.Warning, duration=dur)
        else:
            print(msg)

    def bar_info(self, msg, dur=5):
        if self.iface is not None:
            self.iface.messageBar().pushMessage(self.context, msg, level=Qgis.Info, duration=dur)
        else:
            print(msg)

    def question(self, msg, parent=None):
        if self.iface is not None:
            m = QMessageBox(parent) if parent is not None else QMessageBox()
            m.setWindowTitle(self.context)
            m.setTextFormat(Qt.RichText)
            m.setText(msg)
            m.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            m.setDefaultButton(QMessageBox.No)
            return True if m.exec_() == QMessageBox.Yes else False
        else:
            print(msg)

    def progress_bar(self, msg, minimum=0, maximum=0, init_value=0, clear_msgbar=False):
        if clear_msgbar:
            self.iface.messageBar().clearWidgets()
        pmb = self.iface.messageBar().createMessage(msg)
        pb = QProgressBar()
        pb.setMinimum(minimum)
        pb.setMaximum(maximum)
        pb.setValue(init_value)
        pb.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        pmb.layout().addWidget(pb)
        self.iface.messageBar().pushWidget(pmb, Qgis.Info)
        return pb

    def clear_bar_messages(self):
        self.iface.messageBar().clearWidgets()

    def start_profiler(self, name):
        self.profiles[name] = cProfile.Profile()
        self.profiles[name].enable()

    def stop_profiler(self, name, dumpfile, call_graph=True):
        self.profiles[name].disable()
        self.profiles[name].dump_stats(dumpfile)

        if is_installed("gprof2dot") and is_installed(DOT_EXE) and call_graph:
            # pip install gprof2dot, https://github.com/jrfonseca/gprof2dot
            render_profile(dumpfile, "pdf")

    def start_timer(self, name):
        self.timers[name] = time.time()

    def read_timer(self, name, reset=True):
        timer_time = time.time() - self.timers[name]
        if reset:
            self.start_timer(name)
        return timer_time