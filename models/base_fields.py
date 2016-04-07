from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor

VALUE_FIELD = 0
CHECKBOX_FIELD = 10
COLOR_FIELD = 20


field_nr = 0


def get_field_nr():
    global field_nr
    field_nr += 1
    return field_nr


class BaseItemField(object):
    """base class for each field in a row containing the value"""

    def __init__(self, item, field, value=None):
        """
        initialization
        :param item: ModelItem to which this ItemField belongs
        :param field: ModelField
        :param value: Initial value
        """
        self.item = item
        self.field = field
        self._value = None

        if value is not None:
            self._value = value
        else:
            if hasattr(self.field.default_value, '__call__'):
                self._value = self.field.default_value(self)
            else:
                self._value = self.field.default_value

    @property
    def value(self):
        """
        get current value
        :return: current value
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        set new value
        :param value: value to be set for field item
        :return: new value of field item
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
        """
        private function for setting value, including sending a signal if value changed
        :param value: new value
        :param signal: bool, send dataChanged event through model on value change
        :return: value changed
        """
        if value == self._value:
            return False
        else:
            self._value = value
            if signal:
                if self.item.model:
                    index = self.item.model.index(
                        self.item.get_row_nr(), self.field.column_nr)
                    self.item.model.dataChanged.emit(index, index)
            return True

    @property
    def qvalue(self):
        """
        get current value in a Qt object
        :return: current value
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
        """
        get properties of related field, directly on item field
        :param prop_name: property name
        :return: value of related Field property
        """
        if hasattr(self.field, prop_name):
            return getattr(self.field, prop_name)
        else:
            raise AttributeError


class BaseField(object):

    def __init__(self, name=None, column_name=None, default_value=None, show=False, column_width=0):

        self.type = None
        self.name = name
        self.column_name = column_name
        self.default_value = default_value
        self.show = show
        self.column_width = column_width

        #get nr on creation to determine order in code, which will be equal to the order of the columns
        self.column_nr = None
        self._nr = get_field_nr()
        self.model = None

    def contribute_to_class(self, name, model, column_nr):

        self.name = name
        if self.column_name is None:
            self.column_name = name
        self.model = model
        self.column_nr = column_nr

    def create_row_field(self, item, value=None):

        return BaseItemField(item, field=self, value=value)


class ValueField(BaseField):
    """Field implementation for Values, which (for now) can be everything which can be showed in plain text
     (string, int, float)"""
    def __init__(self, *args, **kwargs):
        super(ValueField, self).__init__(*args, **kwargs)
        self.field_type = VALUE_FIELD


class ColorField(BaseField):
    """Field implementation for Colors."""

    def __init__(self, *args, **kwargs):
        """same as BaseField. Color values are a list of three color values in the range of 0-256.
        For example (68, 55, 204)"""
        super(ColorField, self).__init__(*args, **kwargs)
        self.field_type = COLOR_FIELD


class CheckboxField(BaseField):
    """Field implementation for booleans with checkboxes"""

    def __init__(self, **kwargs):
        super(CheckboxField, self).__init__(**kwargs)
        self.field_type = CHECKBOX_FIELD


