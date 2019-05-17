# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

from ThreeDiToolbox.tool_result_selection.result_downloader import DownloadResultModel
from ThreeDiToolbox.utils.user_messages import messagebar_message
from ThreeDiToolbox.utils.user_messages import pop_up_info
from ThreeDiToolbox.tool_result_selection.result_selection_view import (
    ThreeDiResultSelectionWidget,
)
from qgis.core import QgsNetworkAccessManager
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.PyQt.QtWidgets import QFileDialog

import json
import logging
import os
import re


logger = logging.getLogger(__name__)

USER_DOWNLOAD_DIRECTORY = 1111

assert (
    QNetworkRequest.User < USER_DOWNLOAD_DIRECTORY < QNetworkRequest.UserMax
), "User defined attribute codes must be between User and UserMax."


# From Django:
# https://github.com/django/django/blob/master/django/utils/text.py
def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)


class ThreeDiResultSelection(QObject):
    """QGIS Plugin Implementation."""

    # TODO: Reinout suggests to use requests library and get rid e.g. QNetworkRequest,
    # QgsNetworkAccessManager

    state_changed = pyqtSignal([str, str, list])

    tool_name = "result_selection"

    def __init__(self, iface, ts_datasource):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        QObject.__init__(self)
        self.iface = iface

        self.ts_datasource = ts_datasource
        # TODO: unsure if this is the right place for initializing this model
        self.download_result_model = DownloadResultModel()

        # TODO: fix this fugly shizzle
        self.download_directory = None
        self.username = None
        self.password = None

        # download administration
        self.network_manager = QgsNetworkAccessManager(self)

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.icon_path = ":/plugins/ThreeDiToolbox/icons/icon_add_datasource.png"
        self.menu_text = u"Select 3Di results"

        self.is_active = False
        self.dialog = None
        self.ts_datasource.model_schematisation_change.connect(self.on_state_changed)
        self.ts_datasource.results_change.connect(self.on_state_changed)

    def on_unload(self):
        """Cleanup necessary items here when dialog is closed"""

        # disconnects
        if self.dialog:
            self.dialog.close()

    def on_close_dialog(self):
        """Cleanup necessary items here when dialog is closed"""

        self.dialog.closingDialog.disconnect(self.on_close_dialog)

        self.dialog = None
        self.is_active = False

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.is_active:

            self.is_active = True

            if self.dialog is None:
                # Create the dialog (after translation) and keep reference
                self.dialog = ThreeDiResultSelectionWidget(
                    parent=None,
                    iface=self.iface,
                    ts_datasource=self.ts_datasource,
                    download_result_model=self.download_result_model,
                    parent_class=self,
                )

                # download signals; signal connections should persist after
                # closing the dialog.
                self.dialog.downloadResultButton.clicked.connect(self.handle_download)

            # connect to provide cleanup on closing of dockwidget
            self.dialog.closingDialog.connect(self.on_close_dialog)

            # show the widget
            self.dialog.show()
        else:
            self.dialog.setWindowState(
                self.dialog.windowState() & ~Qt.WindowMinimized | Qt.WindowActive
            )
            self.dialog.raise_()

    def on_state_changed(self, setting_key, value):

        if setting_key == "result_directories":
            output = []
            for result in value:
                output.append(
                    json.JSONEncoder().encode(
                        {
                            "active": result.active.value,
                            "name": result.name.value,
                            "file_path": result.file_path.value,
                            "type": result.type.value,
                        }
                    )
                )
        else:
            output = value

        self.state_changed.emit(self.tool_name, setting_key, [output])

    def set_state(self, setting_dict):
        self.ts_datasource.reset()

        self.ts_datasource.model_spatialite_filepath = setting_dict.get(
            "model_schematisation", None
        )

        result_list = setting_dict.get("result_directories", None)
        if result_list is not None:
            for result_json in result_list:
                result = json.JSONDecoder().decode(result_json)
                self.ts_datasource.insertRows([result])

    def get_state_description(self):
        from io import IOBase

        return (
            self.tool_name,
            {"model_schematisation": IOBase, "result_directories": list},  # file,
        )

    @property
    def logged_in(self):
        return self.username is not None and self.password is not None

    def handle_download(self):
        result_type_codes_download = [
            "logfiles",
            # non-groundwater codes
            "subgrid_map",
            "flow-aggregate",
            "id-mapping",
            # groundwater codes
            "results-3di",
            "aggregate-results-3di",
            "grid-admin",
        ]
        selection_model = self.dialog.downloadResultTableView.selectionModel()
        proxy_indexes = selection_model.selectedIndexes()
        if len(proxy_indexes) != 1:
            pop_up_info("Please select one result.")
            return
        proxy_selection_index = proxy_indexes[0]
        selection_index = self.dialog.download_proxy_model.mapToSource(
            proxy_selection_index
        )
        item = self.download_result_model.rows[selection_index.row()]
        to_download = [
            r
            for r in item.results.value
            if r["result_type"]["code"] in result_type_codes_download
        ]
        to_download_urls = [dl["attachment_url"] for dl in to_download]
        logger.debug(item.name.value)

        # ask user where to store download
        directory = QFileDialog.getExistingDirectory(
            None, "Choose a directory", os.path.expanduser("~")
        )
        if not directory:
            return
        dir_name = get_valid_filename(item.name.value)
        self.download_directory = os.path.join(directory, dir_name)

        # For now, only work with empty directories that we create ourselves.
        # Because the files are downloaded and processed in chunks, we cannot
        # guarantee data integrity with existing files.
        if os.path.exists(self.download_directory):
            pop_up_info("The directory %s already exists." % self.download_directory)
            return
        logger.info("Creating download directory.")
        os.mkdir(self.download_directory)

        logger.debug(self.download_directory)

        CHUNK_SIZE = 16 * 1024
        # Important note: QNetworkAccessManager is asynchronous, which means
        # the downloads are processed asynchronous using callbacks.
        for url in to_download_urls:
            request = QNetworkRequest(QUrl(url))
            request.setRawHeader(b"username", bytes(self.username, "utf-8"))
            request.setRawHeader(b"password", bytes(self.password, "utf-8"))
            request.setAttribute(USER_DOWNLOAD_DIRECTORY, self.download_directory)

            reply = self.network_manager.get(request)
            # Get replies in chunks, and process them
            reply.setReadBufferSize(CHUNK_SIZE)
            reply.readyRead.connect(self.on_single_download_ready_to_read_chunk)
            reply.finished.connect(self.on_single_download_finished)
        pop_up_info("Download started.")

    def on_single_download_ready_to_read_chunk(self):
        """Process a chunk of the downloaded data."""
        # TODO: do some exception handling if the download did not succeed
        reply = self.sender()
        raw_chunk = reply.readAll()  # QByteArray
        filename = reply.url().toString().split("/")[-1]
        download_directory = reply.request().attribute(USER_DOWNLOAD_DIRECTORY)
        if not download_directory:
            raise RuntimeError(
                "Request is not set up properly, USER_DOWNLOAD_DIRECTORY is "
                "required to locate the download directory."
            )
        with open(os.path.join(download_directory, filename), "ab") as f:
            f.write(raw_chunk)

    def on_single_download_finished(self):
        """Usage: mostly for notifying the user the download has finished."""
        reply = self.sender()
        filename = reply.url().toString().split("/")[-1]
        reply.close()
        messagebar_message("Done", "Finished downloading %s" % filename)
