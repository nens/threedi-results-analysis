from PyQt4.QtCore import Qt, QAbstractTableModel, QModelIndex, QSize
from ..utils.user_messages import log
import inspect
from base_fields import COLOR_FIELD, CHECKBOX_FIELD, VALUE_FIELD


class BaseModelItem(object):

    def __init__(self, model=None, **kwargs):

        self.model = model
        self._plots = {}

        for field_name, field_class in self._fields:
            value = None
            if field_name in kwargs.keys():
                value = kwargs[field_name]

            setattr(self, field_name,
                    field_class.create_row_field(item=self, value=value))

        #for function_name, function in self._functions:
        #    setattr(self, function_name, function)

    def get_row_nr(self):
        """
        get rownr of this item in the model
        :return: int: row number
        """

        return self.model.rows.index(self)

    def __getitem__(self, item):

        name = self.model.columns[item].name
        return getattr(self, name)

    def get_fields(self, show_only=False):

        if show_only:
            return [(name, cl) for name, cl in self._fields if cl.show]
        else:
            return self._fields


class BaseModel(QAbstractTableModel):
    """Customized QAbstractTableModel with more pythonic way of field declaration and storage of settings and values in
    ModelItems, ItemFields and Fields"""

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
        self._fields = sorted(
                [(name, cl) for name, cl in inspect.getmembers(self.Fields,
                                            lambda a:not(inspect.isroutine(a)))
                    if not name.startswith('__') and not name.startswith('_') ],
                    key=lambda cl: cl[1]._nr)

        self.columns = [cl for name, cl in self._fields]

        item_functions = [(name, value) for name, value
                    in inspect.getmembers(self.Fields, lambda a:(inspect.isroutine(a)))
                    if not name.startswith('__')]

        self.item_class = type(self.class_name + 'Item', (self._base_model_item_class, self.Fields), {
            '_fields': self._fields
        })

        #for function_name, function in item_functions:
        #    setattr(self.item_class, function_name, function)

        # initiate fields with fieldname, link to model and column_nr
        for i in range(0, len(self._fields)):
            name, field = self._fields[i]
            if hasattr(field, 'contribute_to_class'):
                field.contribute_to_class(name, self, i)

        # process initial data
        self.insertRows(initial_data, signal=False)

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
        return len(self.columns)

    def index(self, row_nr, col_nr, parent=None):
        """
        Creates index for this model. Required function for QAbstractTableModel
        :param row_nr: int row number
        :param col_nr: int column number
        :param parent: parent of index
        :return: QModelIndex instance
        """
        return self.createIndex(row_nr, col_nr)

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
        # elif role == Qt.ToolTipRole:
        #     return 'tooltip'

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
                return self.columns[col_nr].column_name
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
        :return: was setting value successful
        """

        # dataChanged.emit is done within the ItemField, triggered by setting the value
        self._rows[index.row()][index.column()].value = value
        return True

    def flags(self, index):

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if self.columns[index.column()].field_type == CHECKBOX_FIELD:
            flags |= Qt.ItemIsUserCheckable | Qt.ItemIsEditable

        return flags

    def insertRows(self, data_items, signal=True):
        """
        required Qt function for adding rows, including sending signals
        :param data_items: list with values as dictionaries
        :param signal: send signal, False will prevent function from sending signal
        """
        if signal:
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount()+len(data_items)-1)

        for data_item in data_items:
            item = self._create_item(**data_item)
            self._rows.append(item)

        if signal:
            self.endInsertRows()

    def removeRows(self, row, count, parent=QModelIndex()):
        """
        required Qt function to remove rows from model
        :param row: first number to remove (count starts with row 1)
        :param count: number of rows to remove
        :param parent: some Qt parameter
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
