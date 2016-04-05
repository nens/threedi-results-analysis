from PyQt4.QtCore import Qt, QAbstractTableModel, QModelIndex, QSize, QVariant, QAbstractItemModel

from ThreeDiToolbox.datasource.spatialite import TdiSpatialite
from base import BaseModel
from base_fields import CheckboxField, ValueField


class TimeseriesDatasourceModel(BaseModel):

    class Fields:

        active = CheckboxField(show=True, default_value=True, column_width=20, column_name='')
        object_name = ValueField(show=True, column_width=50, column_name='Name')
        file_path = ValueField(show=False)
        type = ValueField(show=False)

        def datasource(self):
            if self._datasource:
                pass
            elif self.type.value == 'spatialite':
                self._datasource = TdiSpatialite(self.file_path.value)

            return self._datasource