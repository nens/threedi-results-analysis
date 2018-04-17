# -*- coding: utf-8 -*-
from __future__ import division

import logging
import os
import urllib2

from lizard_connector.connector import Endpoint
from PyQt4.QtCore import pyqtSignal, QSettings, QModelIndex, QThread
from PyQt4.QtGui import QWidget, QFileDialog
from PyQt4 import uic

from ..datasource.netcdf import (find_id_mapping_file,
                                 find_h5_file,
                                 layer_qh_type_mapping,
                                 detect_netcdf_version)
from ..utils.user_messages import pop_up_info
from .log_in_dialog import LoginDialog


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), os.pardir, 'ui',
    'threedi_result_selection_dialog.ui'))

log = logging.getLogger(__name__)


def _reshape_scenario_results(results):
    MEBIBYTE = 1048576
    return [
        {
            'name': r['name'],
            'url': r['url'],
            'size_mebibytes': round(r['total_size'] / MEBIBYTE, 1),
            'results': r['result_set'],
        }
        for r in results
    ]


class ResultsWorker(QThread):
    """Thread for getting scenario results API data from Lizard."""

    output = pyqtSignal(object)

    def __init__(
            self, parent=None, endpoint=None, username=None, password=None):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.exiting = False
        super(ResultsWorker, self).__init__(parent)

    def __del__(self):
        print("Deleting worker.")
        log.info("Deleting worker.")
        self.stop()

    def run(self):
        for results in self.endpoint:
            if self.exiting:
                print("Exiting...")
                break
            items = _reshape_scenario_results(results)
            print("ResultsWorker - got new data")
            self.output.emit(items)

    def stop(self):
        """Stop the thread gracefully."""
        print("Stopping worker.")
        self.exiting = True
        self.wait()


class ThreeDiResultSelectionWidget(QWidget, FORM_CLASS):
    """Dialog for selecting model (spatialite and result files netCDFs)"""
    closingDialog = pyqtSignal()

    def __init__(
            self, parent=None, iface=None, ts_datasource=None,
            download_result_model=None, parent_class=None):
        """Constructor

        :parent: Qt parent Widget
        :iface: QGiS interface
        :ts_datasource: TimeseriesDatasourceModel instance
        :download_result_model: DownloadResultModel instance
        :parent_class: the tool class which instantiated this widget. Is used
             here for storing volatile information
        """
        super(ThreeDiResultSelectionWidget, self).__init__(parent)

        self.parent_class = parent_class
        self.iface = iface
        self.setupUi(self)

        # login administration
        self.login_dialog = LoginDialog()
        # NOTE: autoDefault was set on ``log_in_button`` (via Qt Designer),
        # which makes pressing Enter work for logging in.
        self.login_dialog.log_in_button.clicked.connect(self.handle_log_in)

        # set models on table views and update view columns
        self.ts_datasource = ts_datasource
        self.resultTableView.setModel(self.ts_datasource)
        self.ts_datasource.set_column_sizes_on_view(self.resultTableView)
        self.download_result_model = download_result_model
        self.downloadResultTableView.setModel(self.download_result_model)
        self.download_result_model.set_column_sizes_on_view(
            self.downloadResultTableView)

        self.toggle_login_interface()

        # connect signals
        self.selectTsDatasourceButton.clicked.connect(
            self.select_ts_datasource)
        self.closeButton.clicked.connect(self.close)
        self.removeTsDatasourceButton.clicked.connect(
            self.remove_selected_ts_ds)
        self.selectModelSpatialiteButton.clicked.connect(
            self.select_model_spatialite_file)
        self.loginButton.clicked.connect(self.on_login_button_clicked)

        # set combobox list
        combo_list = [ds for ds in self.get_3di_spatialites_legendlist()]

        if self.ts_datasource.model_spatialite_filepath and \
                self.ts_datasource.model_spatialite_filepath not in combo_list:
            combo_list.append(self.ts_datasource.model_spatialite_filepath)

        if not self.ts_datasource.model_spatialite_filepath:
            combo_list.append('')

        self.modelSpatialiteComboBox.addItems(combo_list)

        if self.ts_datasource.model_spatialite_filepath:
            current_index = self.modelSpatialiteComboBox.findText(
                self.ts_datasource.model_spatialite_filepath)

            self.modelSpatialiteComboBox.setCurrentIndex(
                current_index)
        else:
            current_index = self.modelSpatialiteComboBox.findText('')
            self.modelSpatialiteComboBox.setCurrentIndex(current_index)

        self.modelSpatialiteComboBox.currentIndexChanged.connect(
            self.model_spatialite_change)

        self.thread = None

    def on_close(self):
        """
        Clean object on close
        """
        self.selectTsDatasourceButton.clicked.disconnect(
            self.select_ts_datasource)
        self.closeButton.clicked.disconnect(self.close)
        self.removeTsDatasourceButton.clicked.disconnect(
            self.remove_selected_ts_ds)
        self.selectModelSpatialiteButton.clicked.disconnect(
            self.select_model_spatialite_file)
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

    def select_ts_datasource(self):
        """
        Open File dialog for selecting netCDF result files, triggered by button
        :return: boolean, if file is selected
        """

        settings = QSettings('3di', 'qgisplugin')

        try:
            init_path = settings.value('last_used_datasource_path', type=str)
        except TypeError:
            init_path = os.path.expanduser("~")

        filename = QFileDialog.getOpenFileName(self,
                                               'Open resultaten file',
                                               init_path,
                                               'NetCDF (*.nc)')

        if filename:
            # Little test for checking if there is an id mapping file available
            # If not we check if an .h5 file is available
            # If not we're not going to proceed

            if detect_netcdf_version(filename) == 'netcdf-groundwater':
                try:
                    find_h5_file(filename)
                    ds_type = 'netcdf-groundwater'
                except IndexError:
                    pop_up_info("You selected a netcdf that was created "
                                "before June 2018. It needs a .h5 file, we "
                                "could however not find this .h5 file. "
                                "We searched in folder [../preprocessed]. "
                                "Please add this file to the correct location"
                                " and try again",
                                title='Error')
                    return False
            elif detect_netcdf_version(filename) == 'netcdf':
                try:
                    find_id_mapping_file(filename)
                    ds_type = 'netcdf'
                except IndexError:
                    pop_up_info("You selected a netcdf that was created "
                                "after May 2018. It needs a id_mapping file, "
                                "we could however not find this "
                                "id_mapping file. We searched in folder "
                                "[../preprocessed]. Please add his file to the"
                                " correct location and try again",
                                title='Error')
                    return False

            items = [{
                'type': ds_type,
                'name': os.path.basename(filename).lower().rstrip('.nc'),
                'file_path': filename
            }]
            self.ts_datasource.insertRows(items)
            settings.setValue('last_used_datasource_path',
                              os.path.dirname(filename))
            return True
        return False

    def remove_selected_ts_ds(self):
        """
        Remove selected result files from model, called by 'remove' button
        """

        selection_model = self.resultTableView.selectionModel()
        # get unique rows in selected fields
        rows = set([index.row()
                    for index in selection_model.selectedIndexes()])
        for row in reversed(sorted(rows)):
            self.ts_datasource.removeRows(row, 1)

    def get_3di_spatialites_legendlist(self):
        """
        Get list of spatialite data sources currently active in canvas
        :return: list of strings, unique spatialite paths
        """

        tdi_spatialites = []

        for layer in self.iface.legendInterface().layers():
            if layer.name() in layer_qh_type_mapping.keys() and \
                    layer.dataProvider().name() == 'spatialite':
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

        self.ts_datasource.model_spatialite_filepath = \
            self.modelSpatialiteComboBox.currentText()
        # Just emitting some dummy model indices cuz what else can we do, there
        # is no corresponding rows/columns that's been changed
        self.ts_datasource.dataChanged.emit(QModelIndex(), QModelIndex())

    def select_model_spatialite_file(self):
        """
        Open file dialog on click on button 'load model'
        :return: Boolean, if file is selected
        """

        settings = QSettings('3di', 'qgisplugin')

        try:
            init_path = settings.value('last_used_spatialite_path', type=str)
        except TypeError:
            init_path = os.path.expanduser("~")

        filename = QFileDialog.getOpenFileName(
            self,
            'Open 3Di model spatialite file',
            init_path,
            'Spatialite (*.sqlite)')

        if filename == "":
            return False

        self.ts_datasource.spatialite_filepath = filename
        index_nr = self.modelSpatialiteComboBox.findText(filename)

        if index_nr < 0:
            self.modelSpatialiteComboBox.addItem(filename)
            index_nr = self.modelSpatialiteComboBox.findText(filename)

        self.modelSpatialiteComboBox.setCurrentIndex(index_nr)

        settings.setValue('last_used_spatialite_path',
                          os.path.dirname(filename))
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
        num_rows = len(self.download_result_model.rows)
        self.download_result_model.removeRows(0, num_rows)
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
        """Handle logging in and populating DownloadResultModel."""
        # Get the username and password
        username = self.login_dialog.user_name_input.text()
        password = self.login_dialog.user_password_input.text()

        if username == '' or password == '':
            pop_up_info("Username or password cannot be empty.")
            return

        try:
            scenarios_endpoint = Endpoint(
                username=username,
                password=password,
                endpoint='scenarios',
            )
            endpoint = scenarios_endpoint.download_paginated(page_size=10)
        except urllib2.HTTPError as e:
            if e.code == 401:
                pop_up_info("Incorrect username and/or password.")
            else:
                pop_up_info(str(e))
        else:
            self.set_logged_in_status(username, password)
            self.toggle_login_interface()
            # don't persist info in the dialog: useful when logged out
            self.login_dialog.user_name_input.clear()
            self.login_dialog.user_password_input.clear()

            # start thread
            self.thread = ResultsWorker(
                endpoint=endpoint, username=username, password=password)
            self.thread.output.connect(self.update_download_result_model)
            self.thread.start()

            # return to widget
            self.login_dialog.close()

    def update_download_result_model(self, items):
        self.download_result_model.insertRows(items)

    @property
    def username(self):
        return self.parent_class.username

    @username.setter
    def username(self, username):
        self.parent_class.username = username

    @property
    def password(self):
        return self.parent_class.password

    @password.setter
    def password(self, password):
        self.parent_class.password = password

    @property
    def logged_in(self):
        """Return the logged in status."""
        return self.parent_class.logged_in

    def set_logged_in_status(self, username, password):
        """Set logged in status to True."""
        self.username = username
        self.password = password

    def set_logged_out_status(self):
        """Set logged in status to False."""
        self.username = None
        self.password = None
