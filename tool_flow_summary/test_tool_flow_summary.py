from threedi_results_analysis.tool_flow_summary.flow_summary import FlowSummaryTool
from threedi_results_analysis.tool_flow_summary.flow_summary import VariableTable

import mock
import unittest


TEST_DATA = {
        "calculation_node_with_max_volume_error": 13973,
        "default_timestep": {
            "units": "s",
            "value": 5.0146
        },
        "maximum_timestep": {
            "units": "s",
            "value": 5.0379
        },
        "minimum_timestep": {
            "units": "s",
            "value": 5.0
        },
        "model_id": 65899,
        "model_name": "ilan2023-16",
        "model_type": "1D/2D",
        "revision_id": 58400,
        "schematisation_id": 6745,
        "simulation_id": 217430,
        "simulation_start": "2024-09-03 12:00:00",
        "simulation_time": {
            "units": "s",
            "value": 14400.1904
        }
    }

TEST_DATA2 = {
        "calculation_node_with_max_volume_error": 13973,
        "additional": 13973,
        "default_timestep": {
            "units": "s",
            "value": 10000
        },
        "additional2": {
            "units": "s",
            "value": 5.0146
        },
    }

TEST_DATA3 = {
        "additional": 2,
        "additional2": {
            "units": "s",
            "value": 3
        },
        "simulation_time": {
            "units": "s",
            "value": 3.14
        }
    }

# same param, but different unit
TEST_DATA4 = {
        "additional2": {
            "units": "h",
            "value": 44444
        },
    }


class TestFlowSummaryTool(unittest.TestCase):
    def setUp(self):
        """test whether FlowSummaryTool can be instantiated"""
        iface = mock.Mock()
        self.flow_summary = FlowSummaryTool(None, iface, None)

    def test_icon_path_is_set(self):
        self.assertEqual(
            self.flow_summary.icon_path, "/root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/threedi_results_analysis/icons/icon_summary.png"
        )

    def test_result_addition_removal(self):
        table = VariableTable(None)
        assert table.columnCount() == 1
        assert table.rowCount() == 0

        table.add_summary_results("test", TEST_DATA)
        assert table.columnCount() == 2
        assert table.rowCount() == 12

        table.add_summary_results("test", TEST_DATA2)
        assert table.columnCount() == 3
        assert table.rowCount() == 14

        table.add_summary_results("test", TEST_DATA3)
        assert table.columnCount() == 4
        assert table.rowCount() == 14

        assert table.item(1, 2).text() == "10000"

        # same data, but different unit
        table.add_summary_results("test", TEST_DATA4)
        assert table.columnCount() == 5
        assert table.rowCount() == 15

        assert table.item(14, 4).text() == "44444"

        # remove TEST_DATA
        table.remove_result(1)
        assert table.columnCount() == 4
        assert table.rowCount() == 15

        assert table.item(14, 3).text() == "44444"

        table.clean_results()
        assert table.columnCount() == 1
        assert table.rowCount() == 0
