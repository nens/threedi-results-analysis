from PyQt4.QtCore import Qt, QAbstractTableModel, QModelIndex, QSize, QVariant, QAbstractItemModel
from PyQt4.QtGui import QStyle, QColor
from collections import OrderedDict
from ThreeDiToolbox.utils.user_messages import log
import inspect
from base_fields import COLOR_FIELD, CHECKBOX_FIELD, VALUE_FIELD
import numpy as np
import pyqtgraph as pg
from ThreeDiToolbox.datasource.spatialite import TdiSpatialite


class BaseModelItem(object):

    _model_collection = None

    def __init__(self, model=None, **kwargs):

        self._model = model

        for field_name, field_class in self._fields:
            value = None
            if field_name in kwargs.keys():
                value = kwargs[field_name]

            setattr(self, field_name,
                    field_class.create_row_field(item=self, value=value))

        #for function_name, function in self._functions:
        #    setattr(self, function_name, function)


    def __getitem__(self, item):

        name = self._model._columns[item].name
        return getattr(self, name)


    def get_fields(self, show_only=False):

        if show_only:
            return [(name, cl) for name, cl in self._fields if cl.show]
        else:
            return self._fields

    def pen(self):
        return pg.mkPen(color=self.color.qvalue, width=2)

    def timeseries_table(self, parameters=None, netcdf_nr=0):

        float_data = []
        ts = self._model.datasource.rows[netcdf_nr]
        b = ts.datasource().get_timeseries(self.object_type.value, self.object_id.value, parameters)
        for t, v in self._model.datasource.rows[netcdf_nr].datasource().get_timeseries(self.object_type.value, self.object_id.value, parameters):
            # some value data may come back as 'NULL' string; convert it to None
            # or else convert it to float
            v = None if v == 'NULL' else float(v)
            float_data.append((float(t), v))
        return np.array(float_data, dtype=float)

    def datasource(self):
        if hasattr(self, '_datasource'):
            return self._datasource
        else: # self.type.value == 'spatialite':
            self._datasource = TdiSpatialite(self.file_path.value)
            return self._datasource



class BaseModel(QAbstractTableModel):

    _base_model_item_class = BaseModelItem
    datasource = None
    class_name = "BaseModel"

    def __init__(self, datasource=None, initial_data=[], parent=None):
        """
        initialisation.
        :param data: initial data. Array of item data.
            item format is dictionary with {
                '<field_id>': <field_value>,
                ...
            }
        :param: parent: some parent object used by Qt
        :return: -
        """
        self._rows = []

        super(BaseModel, self).__init__(parent)

        self.datasource = datasource

        # create item class
        self._fields = [(name, value) for name, value
                    in inspect.getmembers(self.Fields, lambda a:not(inspect.isroutine(a)))
                    if not name.startswith('__')]

        self._columns = sorted([cl for name, cl in self._fields if cl.show], key=lambda cl: cl._nr)

        item_functions = [(name, value) for name, value
                    in inspect.getmembers(self.Fields, lambda a:(inspect.isroutine(a)))
                    if not name.startswith('__')]

        self.item_class = type(self.class_name + 'Item', (self._base_model_item_class, ), {
            '_fields': self._fields, '_functions': item_functions
        })

#        for function_name, function in item_functions:
#            setattr(self.item_class, function_name, function)

        # initiate fields with fieldname and link to model
        for name, field in self._fields:
            if hasattr(field, 'contribute_to_class'):
                field.contribute_to_class(name, self)

        # process initial data
        self.insertRows(initial_data, signal=False)

        return

    def _create_item(self, *args, **kwargs):
        """

        :param args: all (initial) values of the fields. See Fields class for available fields
        :param kwargs: all (initial) values of the fields. See Fields class for available fields
        :return: created item
        """
        return self.item_class(self, *args, **kwargs)

    def rowCount(self, index=QModelIndex):
        """
        get number of rows (nr of items). Required function for QAbstractTableModel
        :param index: QModelIndex
        :return:
        """
        return len(self._rows)

    def columnCount(self, index=QModelIndex):
        """
        get visible columns for display in table. Required function for QAbstractTableModel
        :param index: QModelIndex
        :return:
        """
        return len(self._columns)

    def data(self, index, role=Qt.DisplayRole):
        """Qt function to get data from items for the visible columns"""

        if not index.isValid():
            return None

        item = self.rows[index.row()]

        if role == Qt.DisplayRole:
            if item[index.column()].field_type == VALUE_FIELD:
                return item[index.column()].value
        elif role == Qt.BackgroundRole:
            if item[index.column()].field_type == COLOR_FIELD:
                return item[index.column()].qvalue
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter
        elif role == Qt.CheckStateRole:
            if item[index.column()].field_type == CHECKBOX_FIELD:
                return item[index.column()].qvalue
            else:
                return None
        elif role == Qt.ToolTipRole:
            return 'tooltip'
        else:
            log(str(role))
            pass

    def headerData(self, col_nr, orientation=Qt.Horizontal, role=Qt.DisplayRole):
        """
        required Qt function for getting column information
        :param col_nr: column number
        :param orientation: Qt orientation of header Qt.Horizontal or Qt.Vertical
        :param role: Qt Role (DisplayRole, SizeHintRole, etc)
        :return: value of column, given the role
        """
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self._columns[col_nr].column_name
        else:
            # give grey balk at start of row a small dimension to select row
            if Qt.SizeHintRole:
                return QSize(10, 0)

    def setData(self, index, value, role):
        """
        required Qt function for setting data, including sending of signals
        :param index: QtModelIndex instance
        :param value: new value for ItemField
        :param role: Qt role (DisplayRole, CheckStateRole)
        :return: self
        """

        if self._columns[index.column()].field_type == CHECKBOX_FIELD:
            self._rows[index.row()][index.column()].qvalue = value
            self.dataChanged.emit(index, index)
        else:
            self._rows[index.row()][index.column()].qvalue = value
            self.dataChanged.emit(index, index)
        return self

    def flags(self, index):

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if self._columns[index.column()].field_type == CHECKBOX_FIELD:
            flags |= Qt.ItemIsUserCheckable | Qt.ItemIsEditable

        return flags

    def insertRows(self, data_items, signal=True):
        """
        required Qt function for adding rows, including sending signals
        :param data_items: list with values as dictionaries
        :param signal: send signal, False will prevent function from sending signal
        :return: self
        """
        if signal:
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount()+len(data_items)-1)

        for data_item in data_items:
            item = self._create_item(**data_item)
            self._rows.append(item)

        if signal:
            self.endInsertRows()

        return self

    def removeRows(self, row, count, parent=QModelIndex()):
        """
        required Qt function to remove rows from model
        :param row: first number to remove (count starts with row 1)
        :param count: number of rows to remove
        :param parent: some Qt parameter
        :return:
        """
        #signal
        self.beginRemoveRows(parent, row, row+count-1)

        for i in range(row+count-1, row-1, -1):
            del self._rows[i]

        #signal
        self.endRemoveRows()

    @property
    def rows(self):
        """
        :return: list of model items of model
        """
        return self._rows

