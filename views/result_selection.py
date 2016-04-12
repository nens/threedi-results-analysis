# -*- coding: utf-8 -*-
import os
from PyQt4.QtCore import pyqtSignal, QSettings
from PyQt4.QtGui import QWidget, QFileDialog, QMessageBox
from PyQt4.QtSql import QSqlDatabase
from PyQt4 import uic
from qgis.core import QgsDataSourceURI, QgsVectorLayer, QgsMapLayerRegistry

from ..datasource.spatialite import layer_qh_type_mapping, \
    layer_object_type_mapping


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), os.pardir, 'ui',
            'threedi_result_selection_dialog.ui'))


class ThreeDiResultSelectionWidget(QWidget, FORM_CLASS):
    """Dialog for selecting model (spatialite and result files netCDFs"""
    closingDialog = pyqtSignal()

    def __init__(self, parent=None, iface=None, ts_datasource=None):
        """constructor"""
        super(ThreeDiResultSelectionWidget, self).__init__(parent)

        self.iface = iface
        self.setupUi(self)

        self.ts_datasource = ts_datasource
        self.resultTableView.setModel(self.ts_datasource)

        for col_nr in range(0, self.ts_datasource.columnCount()):
            width = self.ts_datasource.columns[col_nr].column_width
            if width:
                self.resultTableView.setColumnWidth(col_nr, width)
            if not self.ts_datasource.columns[col_nr].show:
                self.resultTableView.setColumnHidden(col_nr, True)

        # set events
        self.selectTsDatasourceButton.clicked.connect(
                self.select_ts_datasource)
        self.closeButton.clicked.connect(self.close)
        self.removeTsDatasourceButton.clicked.connect(
                self.remove_selected_ts_ds)
        self.selectModelSpatialiteButton.clicked.connect(
                self.select_model_spatialite_file)

        # set combobox list
        combo_list = [ds for ds in self.get_3di_spatialites_legendlist()]

        if self.ts_datasource.model_spatialite_filepath and \
                self.ts_datasource.model_spatialite_filepath not in combo_list:
            combo_list.append(self.ts_datasource.spatialite_filepath)

        self.modelSpatialiteComboBox.addItems(combo_list)

        if self.ts_datasource.model_spatialite_filepath:
            self.modelSpatialiteComboBox.setCurrentIndex(
                    self.modelSpatialiteComboBox.findData(
                            self.ts_datasource.spatialite_filepath))

        self.modelSpatialiteComboBox.currentIndexChanged.connect(
            self.model_spatialite_change)

    def on_close(self):
        """
        clean object on close
        """

        self.selectTsDatasourceButton.clicked.disconnect(
                self.select_ts_datasource)
        self.closeButton.clicked.disconnect(self.close)
        self.removeTsDatasourceButton.clicked.disconnect(
                self.remove_selected_ts_ds)
        self.selectModelSpatialiteButton.clicked.connect(
                self.select_model_spatialite_file)

    def closeEvent(self, event):
        """
        function called by qt on close
        :param event: QEvent, close event
        """
        self.closingDialog.emit()
        self.on_close()
        event.accept()

    def select_ts_datasource(self):
        """
        file dialog for selecting netCDF result files
        :return: boolean, if file is selected
        """

        settings = QSettings('3di', 'qgisplugin')

        try:
            init_path = settings.value('last_used_path', type=str)
        except TypeError:
            init_path = os.path.expanduser("~")

        fname = QFileDialog.getOpenFileName(self, 'Open resultaten file',
                                            init_path , 'NetCDF (*.nc)')

        if fname:
            items = [{
                'type': 'netcdf',
                'name': os.path.basename(fname).lower().rstrip('.nc'),
                'file_path': fname
            }]
            self.ts_datasource.insertRows(items)
            settings.setValue('last_used_path', os.path.dirname(fname))

            return True

        return False

    def remove_selected_ts_ds(self):
        """
        remove selected result files from model (called by 'remove' button)
        """

        selection_model = self.resultTableView.selectionModel()
        #get unique rows in selected fields
        rows = set([index.row() for index in selection_model.selectedIndexes()])
        for row in reversed(sorted(rows)):
            self.ts_datasource.removeRows(row,1)

    def get_3di_spatialites_legendlist(self):
        """
        get list of spatialite data sources currently active in canvas
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
        called by combobox when selected spatialite changed
        :param nr: integer, nr of item selected in combobox
        """

        self.ts_datasource.model_spatialite_filepath = \
                self.modelSpatialiteComboBox.currentText()

    def _add_spl_layer_to_canvas(self, fname, table_name):
        """
        add spatialite layer to canvas (map)
        :param fname: string, spatialite path
        :param table_name: string, table or view name
        """

        schema = ''

        uri2 = QgsDataSourceURI()
        uri2.setDatabase(fname)
        uri2.setDataSource(schema, table_name, 'the_geom')
        vlayer = QgsVectorLayer(uri2.uri(),
                                table_name,
                                'spatialite')
        if vlayer.isValid():
            QgsMapLayerRegistry.instance().addMapLayer(vlayer)

    def select_model_spatialite_file(self):
        """
        file dialog when selection 'load model'
        :return: Boolean, if file is selected
        """

        settings = QSettings('3di', 'qgisplugin')

        try:
            init_path = settings.value('last_used_path', type=str)
        except TypeError:
            init_path = os.path.expanduser("~")

        fname = QFileDialog.getOpenFileName(self,
                                            'Open 3di model spatialite file',
                                            init_path ,
                                            'Spatialite (*.sqlite)')

        if fname is None:
            return False

        self.ts_datasource.spatialite_filepath = fname
        index_nr = self.modelSpatialiteComboBox.findText(fname)

        if index_nr < 0:
            self.modelSpatialiteComboBox.addItem(fname)
            index_nr = self.modelSpatialiteComboBox.findText(fname)

        self.modelSpatialiteComboBox.setCurrentIndex(index_nr)

        if fname not in self.get_3di_spatialites_legendlist():
            # add spatialite to layer menu
            msg = "Voeg de kaartlagen uit de spatialite toe?"
            reply = QMessageBox.question(self, 'Kaartlagen toevoegen',
                     msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.No:
                return True

            uri = QgsDataSourceURI()
            uri.setDatabase(fname)
            db = QSqlDatabase.addDatabase("QSQLITE")

            # Reuse the path to DB to set database name
            db.setDatabaseName(uri.database())
            # Open the connection
            db.open()
            # query the table
            query = db.exec_("""SELECT f_table_name FROM geometry_columns
                WHERE f_geometry_column = 'the_geom';""")

            while query.next():
                table_name = query.record().value(0)
                if table_name in layer_object_type_mapping.keys():
                    self._add_spl_layer_to_canvas(fname, table_name)

            query = db.exec_("""SELECT view_name FROM views_geometry_columns
                WHERE view_geometry = 'the_geom';""")

            while query.next():
                view_name = query.record().value(0)
                if view_name in layer_object_type_mapping.keys():
                    self._add_spl_layer_to_canvas(fname, view_name)

        return True
