from ThreeDiToolbox.tool_result_selection.result_selection import ThreeDiResultSelection
from ThreeDiToolbox.models.datasources import TimeseriesDatasourceModel
from ThreeDiToolbox.tool_result_selection.result_downloader import DownloadResultModel

import mock
import unittest


class TestThreeDiResultSelection(unittest.TestCase):
    def setUp(self):
        """test whether ThreeDiResultSelection can be instantiated """
        iface = mock.Mock()
        self.ts_datasource = TimeseriesDatasourceModel()
        self.result_selection_tool = ThreeDiResultSelection(iface, self.ts_datasource)
        self.download_result_model = DownloadResultModel()
        # parent_class = mock.Mock()

        # TODO: ThreeDiResultSelection contains a self.dialog that must be mocked ??
        # since below does not work:
        # self.dialog = ThreeDiResultSelectionWidget(
        #     parent=None,
        #     iface=iface,
        #     ts_datasource=self.ts_datasource,
        #     download_result_model=self.download_result_model,
        #     parent_class=parent_class)

    def test_icon_path_is_set(self):
        self.assertEqual(
            self.result_selection_tool.icon_path,
            ":/plugins/ThreeDiToolbox/icons/icon_add_datasource.png",
        )
