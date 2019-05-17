# -*- coding: utf-8 -*-

from ThreeDiToolbox.models.base import BaseModel
from ThreeDiToolbox.models.base_fields import ValueField


class DownloadResultModel(BaseModel):
    def __init__(self):
        super(DownloadResultModel, self).__init__(self)
        print('hoi')

    class Fields(object):
        name = ValueField(show=True, column_width=250, column_name="Name")
        size_mebibytes = ValueField(
            show=True, column_width=120, column_name="Size (MiB)"
        )
        url = ValueField(show=True, column_width=300, column_name="URL")
        results = ValueField(show=False)  # the scenario results
