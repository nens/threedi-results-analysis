import inspect
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor

VALUE_FIELD =  0
CHECKBOX_FIELD = 10
COLOR_FIELD = 20


field_nr = 0

def get_field_nr():
    global field_nr
    field_nr += 1
    return field_nr


class BaseItemField(object):
    """base class for each value in a row"""

    def __init__(self, item, field, value=None):
        self._item = item
        self._field = field
        self._value = None

        if value is not None:
            self._value = value
        else:
            if hasattr(self._field.default_value, '__call__'):
                self._value = self._field.default_value(self)
            else:
                self._value = self._field.default_value


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

        #todo signal
        self._value = value
        return self._value

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

        return self._value

    @qvalue.setter
    def qvalue(self, value):
        """
        set value using Qt objects. function will translate back to
        model storage format
        :return: current value
        """
        if self.field_type == CHECKBOX_FIELD:
            if value == Qt.Checked:
                self._value = True
            else:
                self._value = False
        else:
            self._value = value

    def __getattr__(self, prop_name):
        """
        get properties of related field, directly on item field
        :param prop_name: property name
        :return: value of related Field property
        """

        if hasattr(self._field, prop_name):
            return getattr(self._field, prop_name)
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

        self._nr = get_field_nr()
        self._model = None

    def contribute_to_class(self, name, model):

        self.name = name
        if self.column_name is None:
            self.column_name = name
        self._model = model

    def create_row_field(self, item, value=None):

        return BaseItemField(item, field=self, value=value)



class ValueField(BaseField):

    def __init__(self, *args, **kwargs):
        super(ValueField, self).__init__(*args, **kwargs)
        self.field_type = VALUE_FIELD


class ColorField(BaseField):

    def __init__(self, *args, **kwargs):
        super(ColorField, self).__init__(*args, **kwargs)
        self.field_type = COLOR_FIELD


class CheckboxField(BaseField):

    def __init__(self, **kwargs):
        super(CheckboxField, self).__init__(**kwargs)
        self.field_type = CHECKBOX_FIELD


