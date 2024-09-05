from threedi_results_analysis.tool_flow_summary.flow_summary import FlowSummaryTool

import mock
import unittest


class TestFlowSummaryTool(unittest.TestCase):
    def setUp(self):
        """test whether FlowSummaryTool can be instantiated"""
        iface = mock.Mock()
        self.flow_summary = FlowSummaryTool(None, iface, None)

    def test_icon_path_is_set(self):
        self.assertEqual(
            self.flow_summary.icon_path, "/root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/threedi_results_analysis/icons/icon_summary.png"
        )

    def test_result_addition(self):
        pass
