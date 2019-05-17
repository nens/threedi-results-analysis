from ThreeDiToolbox.tool_result_selection.result_selection import ThreeDiResultSelection
from ThreeDiToolbox.models.datasources import TimeseriesDatasourceModel


from ThreeDiToolbox.tool_result_selection.result_selection_view import (
    FORM_CLASS,
    ThreeDiResultSelectionWidget,
)
from ThreeDiToolbox.tool_result_selection.result_downloader import DownloadResultModel


from qgis.PyQt.QtWidgets import QWidget
import mock
import unittest
import os


spatialite_datasource_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "data", "test_spatialite.sqlite"
)

THREEDI_RESULTS_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "data",
    "testmodel",
    "v2_bergermeer",
    "results_3di.nc",
)


class TestThreeDiResultSelection(unittest.TestCase):
    def setUp(self):
        """test whether ThreeDiResultSelection can be instantiated """
        iface = mock.Mock()
        self.ts_datasource = TimeseriesDatasourceModel()
        self.result_selection_tool = ThreeDiResultSelection(iface, self.ts_datasource)
        self.download_result_model = DownloadResultModel()
        parent_class = mock.Mock()

        # TODO: mock self.dialog ??
        #
        # try:
        #     self.dialog = ThreeDiResultSelectionWidget(
        #         parent=None,
        #         iface=iface,
        #         ts_datasource=self.ts_datasource,
        #         download_result_model=self.download_result_model,
        #         parent_class=parent_class,
        #     )
        # except Exception as e:
        #     print(e)
        #
        # self.result_selection_view = ThreeDiResultSelectionWidget(QWidget, FORM_CLASS)

    def test_icon_path_is_set(self):
        self.assertEqual(
            self.result_selection_tool.icon_path,
            ":/plugins/ThreeDiToolbox/icons/icon_add_datasource.png",
        )
