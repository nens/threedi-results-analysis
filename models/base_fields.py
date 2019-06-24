from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor


VALUE_FIELD = 0
CHECKBOX_FIELD = 10
COLOR_FIELD = 20


field_nr = 0


def get_field_nr():
    global field_nr
    field_nr += 1
    return field_nr


class RowFieldValue(object):
    """Class holding the value for a column/field for a certain row.

    The field is the BaseField instance (so: really a column).

    The value is mapped to something QT-friendly.

    The "row" is a BaseModelRow instance.

    """

    def __init__(self, row, field, value=None):
        """Initialization.

        :param row: BaseModelRow to which this ItemField belongs
        :param field: ModelField
        :param value: Initial value

        """
        self.row = row
        self.field = field
        self._value = None

        if value is not None:
            self._value = value
        else:
            # TODO: use iscallable()?
            if hasattr(self.field.default_value, "__call__"):
                self._value = self.field.default_value(self)
            else:
                self._value = self.field.default_value

    @property
    def value(self):
        """Return current value."""
        return self._value

    @value.setter
    def value(self, value):
        """Set new value, possibly after some adjustments, and return it.

        :param value: value to be set for field row
        :return: new value of field row
        """
        if self.field_type == CHECKBOX_FIELD:
            if type(value) == bool:
                self._set_value(value)
            elif value == Qt.Checked:
                self._set_value(True)
            elif value == Qt.Unchecked:
                self._set_value(False)
        else:
            self._set_value(value)

        return self._value

    def _set_value(self, value, signal=True):
        """Set value (if changed) and fire a signal.

        Private function for setting value, including sending a signal if
        value changed

        :param value: new value
        :param signal: bool, send dataChanged event through model on value
                       change

        """
        if value == self._value:
            # No need to set it and fire a signal and so.
            return
        self._value = value
        if signal:
            if self.row.model:
                index = self.row.model.index(
                    self.row.get_row_nr(), self.field.column_nr
                )
                self.row.model.dataChanged.emit(index, index)

    @property
    def qvalue(self):
        """Return current value as a Qt object

        :return: current value, adjusted for qt.

        """
        if self.field_type == CHECKBOX_FIELD:
            if self.value:
                return Qt.Checked
            else:
                return Qt.Unchecked
        elif self.field_type == COLOR_FIELD:
            if self.value is not None:
                return QColor(*self.value)
        else:
            return self._value

    def __getattr__(self, prop_name):
        """Return property of related field, directly from this row field.

        :param prop_name: property name
        :return: value of related Field property

        # TODO: check if it is used. I see item_field.row.model.rows() and
        so.... Everyone seems to dive into its internals anyway...

        """
        if hasattr(self.field, prop_name):
            return getattr(self.field, prop_name)
        else:
            raise AttributeError


class BaseField(object):
    """Configuration for a column: what kind of field are we?

    Important is the ``.create_row_field()`` method that creates a
    RowFieldValue, which is basically a row's value for this column.

    """

    field_type = None

    def __init__(
        self,
        name=None,
        column_name=None,
        default_value=None,
        show=False,
        column_width=0,
    ):

        self.type = None
        self.name = name
        self.column_name = column_name
        self.default_value = default_value
        self.show = show
        self.column_width = column_width

        # get nr on creation to determine order in code, which will be equal
        # to the order of the columns
        self.column_nr = None
        self._nr = get_field_nr()
        self.model = None

    def contribute_to_class(self, name, model, column_nr):
        self.name = name
        if self.column_name is None:
            self.column_name = name
        self.model = model
        self.column_nr = column_nr

    def create_row_field(self, row, value=None):
        return RowFieldValue(row, field=self, value=value)


class ValueField(BaseField):
    """Field implementation for Values, which (for now) can be everything
    which can be showed in plain text (string, int, float)"""

    field_type = VALUE_FIELD


class ColorField(BaseField):
    """Field implementation for Colors."""

    field_type = COLOR_FIELD


class CheckboxField(BaseField):
    """Field implementation for booleans with checkboxes"""

    field_type = CHECKBOX_FIELD
