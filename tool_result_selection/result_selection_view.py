from lizard_connector.connector import Endpoint
from pathlib import Path
from qgis.core import QgsSettings
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import QModelIndex
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtCore import QSortFilterProxyModel
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtCore import QThread
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtWidgets import QWidget
from ThreeDiToolbox.datasource.result_constants import LAYER_QH_TYPE_MAPPING
from ThreeDiToolbox.datasource.threedi_results import find_h5_file
from ThreeDiToolbox.tool_result_selection.login_dialog import LoginDialog
from ThreeDiToolbox.utils.user_messages import pop_up_info
from urllib.error import HTTPError

import h5py
import logging
import os


ui_file = Path(__file__).parent / "result_selection_view.ui"
assert ui_file.is_file()
FORM_CLASS, _ = uic.loadUiType(ui_file)
MEBIBYTE = 1048576

logger = logging.getLogger(__name__)


def _reshape_scenario_results(results):
    return [
        {
            "name": result["name"],
            "url": result["url"],
            "size_mebibytes": round(result["total_size"] / MEBIBYTE, 1),
            "results": result["result_set"],
        }
        for result in results
    ]


class DownloadWorker(QThread):
    """Thread for getting scenario results API data from Lizard."""

    output = pyqtSignal(object)
    connection_failure = pyqtSignal(int, str)

    def __init__(self, parent=None, endpoint=None, username=None, password=None):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.exiting = False
        super().__init__(parent)

    def __del__(self):
        logger.info("Deleting download-worker.")
        self.stop()

    def run(self):
        try:
            for results in self.endpoint:
                if self.exiting:
                    logger.info("Exiting...")
                    break
                items = _reshape_scenario_results(results)
                logger.debug("DownloadWorker - got new data")
                self.output.emit(items)
        except HTTPError as e:
            message = (
                "Something went wrong trying to connect to {0}. {1}: "
                "{2}".format(e.url, e.code, e.reason)
            )
            logger.exception(message)
            self.connection_failure.emit(e.code, e.reason)

    def stop(self):
        """Stop the thread gracefully."""
        logger.info("Stopping download-worker...")
        self.exiting = True
        self.wait()


class ThreeDiResultSelectionWidget(QWidget, FORM_CLASS):
    """Dialog for selecting model (spatialite and result files netCDFs)

    TODO: actually, it is two dialogs in one: a selector of results and a
    separate downloader of results. They are not really connected. So
    splitting them makes the code simpler. And, more importantly, it makes the
    UI clearer.

    """

    closingDialog = pyqtSignal()

    def __init__(
        self,
        parent=None,
        iface=None,
        ts_datasources=None,
        downloadable_results=None,
        tool=None,
    ):
        """Constructor

        :parent: Qt parent Widget
        :iface: QGiS interface
        :ts_datasources: TimeseriesDatasourceModel instance
        :downloadable_results: DownloadableResultModel instance
        :tool: the tool class which instantiated this widget. Is used
             here for storing volatile information
        """
        super().__init__(parent)

        self.tool = tool
        self.iface = iface
        self.setupUi(self)

        # login administration
        self.login_dialog = LoginDialog()
        # NOTE: autoDefault was set on ``log_in_button`` (via Qt Designer),
        # which makes pressing Enter work for logging in.
        self.login_dialog.log_in_button.clicked.connect(self.handle_log_in)

        # set models on table views and update view columns
        self.ts_datasources = ts_datasources
        self.resultTableView.setModel(self.ts_datasources)
        self.ts_datasources.set_column_sizes_on_view(self.resultTableView)

        self.downloadable_results = downloadable_results
        self.download_proxy_model = QSortFilterProxyModel()
        self.download_proxy_model.setSourceModel(self.downloadable_results)
        self.download_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filterLineEdit.textChanged.connect(
            self.download_proxy_model.setFilterFixedString
        )
        self.downloadResultTableView.setModel(self.download_proxy_model)

        self.toggle_login_interface()

        # connect signals
        self.selectTsDatasourceButton.clicked.connect(self.select_ts_datasource)
        self.closeButton.clicked.connect(self.close)
        self.removeTsDatasourceButton.clicked.connect(
            self.remove_selected_ts_datasource
        )
        self.selectModelSpatialiteButton.clicked.connect(
            self.select_model_spatialite_file
        )
        self.loginButton.clicked.connect(self.on_login_button_clicked)

        # set combobox list
        combo_list = [
            datasource for datasource in self.get_3di_spatialites_legendlist()
        ]

        if (
            self.ts_datasources.model_spatialite_filepath
            and self.ts_datasources.model_spatialite_filepath not in combo_list
        ):
            combo_list.append(self.ts_datasources.model_spatialite_filepath)

        if not self.ts_datasources.model_spatialite_filepath:
            combo_list.append("")

        self.modelSpatialiteComboBox.addItems(combo_list)

        if self.ts_datasources.model_spatialite_filepath:
            current_index = self.modelSpatialiteComboBox.findText(
                self.ts_datasources.model_spatialite_filepath
            )

            self.modelSpatialiteComboBox.setCurrentIndex(current_index)
        else:
            current_index = self.modelSpatialiteComboBox.findText("")
            self.modelSpatialiteComboBox.setCurrentIndex(current_index)

        self.modelSpatialiteComboBox.currentIndexChanged.connect(
            self.model_spatialite_change
        )

        self.thread = None

    def on_close(self):
        """
        Clean object on close
        """
        self.selectTsDatasourceButton.clicked.disconnect(self.select_ts_datasource)
        self.closeButton.clicked.disconnect(self.close)
        self.removeTsDatasourceButton.clicked.disconnect(
            self.remove_selected_ts_datasource
        )
        self.selectModelSpatialiteButton.clicked.disconnect(
            self.select_model_spatialite_file
        )
        self.loginButton.clicked.disconnect(self.on_login_button_clicked)

        # stop the thread when we close the widget
        if self.thread:
            self.thread.output.disconnect(self.update_download_result_model)
            self.thread.stop()

    def closeEvent(self, event):
        """
        Close widget, called by Qt on close
        :param event: QEvent, close event
        """
        self.closingDialog.emit()
        self.on_close()
        event.accept()

    def keyPressEvent(self, event):
        """Handle key press events on the widget."""
        # Close window if the Escape key is pressed
        if event.key() == Qt.Key_Escape:
            self.close()

    def select_ts_datasource(self):
        """
        Open File dialog for selecting netCDF result files, triggered by button
        :return: boolean, if file is selected
        """

        settings = QSettings("3di", "qgisplugin")

        try:
            init_path = settings.value("last_used_datasource_path", type=str)
        except TypeError:
            logger.debug(
                "Last used datasource path is no string, setting it to our home dir."
            )
            init_path = os.path.expanduser("~")

        filename, __ = QFileDialog.getOpenFileName(
            self,
            "Open resultaten file",
            init_path,
            "NetCDF (subgrid_map.nc results_3di.nc)",
        )

        if filename:
            # Little test for checking if there is an id mapping file available
            # If not we check if an .h5 file is available
            # If not we're not going to proceed

            datasource_type = detect_netcdf_version(filename)
            logger.info(
                "Netcdf result file selected: %s, type is %s", filename, datasource_type
            )
            if datasource_type == "netcdf-groundwater":
                try:
                    find_h5_file(filename)
                except FileNotFoundError:
                    logger.warning(
                        "Groundwater h5 not found (%s), warning the user.", filename
                    )
                    pop_up_info(
                        "You selected a netcdf that was created "
                        "(after May 2018) with a 3Di calculation"
                        "core that is able to include groundwater"
                        " calculations. The ThreeDiToolbox reads "
                        "this netcdf together with an .h5 file, we "
                        "could however not find this .h5 file. Please "
                        "add this file next to the netcdf and try "
                        "again",
                        title="Error",
                    )
                    return False
            elif datasource_type == "netcdf":
                logger.warning(
                    "Result file (%s) version is too old. Warning the user.", filename
                )
                pop_up_info(
                    "The selected result data is too old and no longer "
                    "supported in this version of ThreediToolbox. Please "
                    "recalculate the results with a newer version of the "
                    "threedicore or use the ThreediToolbox plugin for QGIS 2",
                    title="Error",
                )
                # TODO: the below "return False" was previously missing. Check
                # if Reinout was right in adding it :-)
                return False

            items = [
                {
                    "type": datasource_type,
                    "name": os.path.basename(filename).lower().rstrip(".nc"),
                    "file_path": filename,
                }
            ]
            self.ts_datasources.insertRows(items)
            settings.setValue("last_used_datasource_path", os.path.dirname(filename))
            return True
        return False

    def remove_selected_ts_datasource(self):
        """
        Remove selected result files from model, called by 'remove' button
        """

        selection_model = self.resultTableView.selectionModel()
        # get unique rows in selected fields
        rows = set([index.row() for index in selection_model.selectedIndexes()])
        for row in reversed(sorted(rows)):
            self.ts_datasources.removeRows(row, 1)

    def get_3di_spatialites_legendlist(self):
        """
        Get list of spatialite data sources currently active in canvas
        :return: list of strings, unique spatialite paths
        """

        tdi_spatialites = []
        for layer in self.iface.layerTreeView().selectedLayers():
            if (
                layer.name() in list(LAYER_QH_TYPE_MAPPING.keys())
                and layer.dataProvider().name() == "spatialite"
            ):
                source = layer.dataProvider().dataSourceUri().split("'")[1]
                if source not in tdi_spatialites:
                    tdi_spatialites.append(source)

        return tdi_spatialites

    def model_spatialite_change(self, nr):
        """
        Change active modelsource. Called by combobox when selected
        spatialite changed
        :param nr: integer, nr of item selected in combobox
        """
        filepath = self.modelSpatialiteComboBox.currentText()
        logger.info("Different spatialite 3di model selected: %s", filepath)
        self.ts_datasources.model_spatialite_filepath = filepath
        # Just emitting some dummy model indices cuz what else can we do, there
        # is no corresponding rows/columns that's been changed
        self.ts_datasources.dataChanged.emit(QModelIndex(), QModelIndex())

    def select_model_spatialite_file(self):
        """
        Open file dialog on click on button 'load model'
        :return: Boolean, if file is selected
        """

        settings = QSettings("3di", "qgisplugin")

        try:
            init_path = settings.value("last_used_spatialite_path", type=str)
        except TypeError:
            logger.debug(
                "Last used datasource path is no string, setting it to our home dir."
            )
            init_path = os.path.expanduser("~")

        filepath, __ = QFileDialog.getOpenFileName(
            self, "Open 3Di model spatialite file", init_path, "Spatialite (*.sqlite)"
        )

        if filepath == "":
            return False

        self.ts_datasources.spatialite_filepath = filepath
        index_nr = self.modelSpatialiteComboBox.findText(filepath)
        if index_nr < 0:
            self.modelSpatialiteComboBox.addItem(filepath)
            index_nr = self.modelSpatialiteComboBox.findText(filepath)

        self.modelSpatialiteComboBox.setCurrentIndex(index_nr)

        add_spatialite_connection(filepath, self.iface)
        settings.setValue("last_used_spatialite_path", os.path.dirname(filepath))
        return True

    def on_login_button_clicked(self):
        """Handle log in and out."""
        if self.logged_in:
            self.handle_log_out()
        else:
            self.login_dialog.user_name_input.setFocus()
            self.login_dialog.show()

    def handle_log_out(self):
        self.set_logged_out_status()
        if self.thread:
            self.thread.stop()
        num_rows = len(self.downloadable_results.rows)
        self.downloadable_results.removeRows(0, num_rows)
        self.toggle_login_interface()

    def toggle_login_interface(self):
        """Enable/disable aspects of the interface based on login status."""
        # TODO: better to use signals maybe?
        if self.logged_in:
            self.loginButton.setText("Log out")
            self.downloadResultTableView.setEnabled(True)
            self.downloadResultButton.setEnabled(True)
        else:
            self.loginButton.setText("Log in")
            self.downloadResultTableView.setEnabled(False)
            self.downloadResultButton.setEnabled(False)

    def handle_log_in(self):
        """Handle logging in and populating DownloadableResultModel."""
        # Get the username and password
        username = self.login_dialog.user_name_input.text()
        password = self.login_dialog.user_password_input.text()

        if username == "" or password == "":
            pop_up_info("Username or password cannot be empty.")
            return

        try:
            scenarios_endpoint = Endpoint(
                username=username, password=password, endpoint="scenarios"
            )
            endpoint = scenarios_endpoint.download_paginated(page_size=10)
        except HTTPError as e:
            logger.exception("Error trying to log in")
            if e.code == 401:
                pop_up_info("Incorrect username and/or password.")
            else:
                pop_up_info(str(e))
            return

        self.set_logged_in_status(username, password)
        self.toggle_login_interface()
        # don't persist info in the dialog: useful when logged out
        self.login_dialog.user_name_input.clear()
        self.login_dialog.user_password_input.clear()

        # start thread
        self.thread = DownloadWorker(
            endpoint=endpoint, username=username, password=password
        )
        self.thread.connection_failure.connect(self.handle_connection_failure)
        self.thread.output.connect(self.update_download_result_model)
        self.thread.start()

        # return to widget
        self.login_dialog.close()

    def update_download_result_model(self, items):
        self.downloadable_results.insertRows(items)

    def handle_connection_failure(self, status, reason):
        pop_up_info(
            "Something went wrong trying to connect to "
            "lizard: {0} {1}".format(status, reason)
        )
        self.handle_log_out()

    @property
    def username(self):
        return self.tool.username

    @username.setter
    def username(self, username):
        self.tool.username = username

    @property
    def password(self):
        return self.tool.password

    @password.setter
    def password(self, password):
        self.tool.password = password

    @property
    def logged_in(self):
        """Return the logged in status."""
        return self.tool.logged_in

    def set_logged_in_status(self, username, password):
        """Set logged in status to True."""
        # TODO: it doesn't really do that. I *suspect* that the parent class
        # has a logged_in() method that checks if username and password are
        # set there. It's all quite indirect.
        self.username = username
        self.password = password

    def set_logged_out_status(self):
        """Set logged in status to False."""
        self.username = None
        self.password = None


def add_spatialite_connection(spatialite_path, iface):
    """Add spatialite_path as a spatialite connection in the qgis-browser"""
    filename = os.path.basename(spatialite_path)
    QgsSettings().setValue(
        f"SpatiaLite/connections/{filename}/sqlitepath",
        spatialite_path
    )
    iface.reloadConnections()


def detect_netcdf_version(netcdf_file_path):
    """An ad-hoc way to detect whether we work with
    1. or an regular netcdf: one that has been made with on "old" calculation
    core (without groundater). This netcdf does not include an attribute
    'threedicore_version'
    2. or an groundwater netcdf: one that has been made with on "new"
    calculation core (with optional groundater calculations). This netcdf
    does include an attribute 'threedicore_version'

    Args:
        netcdf_file_path: path to the result netcdf

    Returns:
        the version (a string) of the netcdf
            - 'netcdf'
            - 'netcdf-groundwater'

    """
    try:
        dataset = h5py.File(netcdf_file_path, mode="r")
        if "threedicore_version" in dataset.attrs:
            return "netcdf-groundwater"
        else:
            return "netcdf"
    except IOError:
        # old 3Di results cannot be opened with h5py. The can be opened with
        # NetCDF4 Dataset (dataset.file_format = NETCDF3_CLASSIC). If you open
        # a new 3Di result with NetCDF4 you get dataset.file_format = NETCDF4
        return "netcdf"
