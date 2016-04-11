from ..datasource.spatialite import TdiSpatialite
from ..datasource.netcdf import NetcdfDataSource
from base import BaseModel
from base_fields import CheckboxField, ValueField


class TimeseriesDatasourceModel(BaseModel):

    model_spatialite_filepath = None

    class Fields:

        active = CheckboxField(show=True, default_value=True, column_width=20, column_name='')
        name = ValueField(show=True, column_width=130, column_name='Name')
        file_path = ValueField(show=True, column_width=260, column_name='File')
        type = ValueField(show=False)

        def datasource(self):
            if hasattr(self, '_datasource'):
                return self._datasource
            elif self.type.value == 'spatialite':
                self._datasource = TdiSpatialite(self.file_path.value)
                return self._datasource
            elif self.type.value == 'netcdf':
                self._datasource = NetcdfDataSource(self.file_path.value)
                return self._datasource

