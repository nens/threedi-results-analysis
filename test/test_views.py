import unittest

from ThreeDiToolbox.views.graph import (
    parse_aggvarname,
    generate_parameter_config,
)

from ThreeDiToolbox.views.guess_indicator_dialog import *
from ThreeDiToolbox.views.import_sufhyd_dialog import *
from ThreeDiToolbox.views.map_animator import *
from ThreeDiToolbox.views.sideview import *
from ThreeDiToolbox.views.timeslider import *
from ThreeDiToolbox.views.tool_dialog import *
from ThreeDiToolbox.views.result_selection import *


class TestGraph(unittest.TestCase):
    def test_parse_aggvarname(self):
        param, method = parse_aggvarname('s1_max')
        self.assertEqual(param, 's1')
        self.assertEqual(method, 'max')

        param, method = parse_aggvarname('s1_cum_negative')
        self.assertEqual(param, 's1')
        self.assertEqual(method, 'cum_negative')

        param, method = parse_aggvarname('infiltration_rate_cum_negative')
        self.assertEqual(param, 'infiltration_rate')
        self.assertEqual(method, 'cum_negative')

    def test_generate_parameter_config(self):
        param_config = generate_parameter_config(['q'], ['q_max'])
        self.assertEqual(len(param_config['h']), 0)
        self.assertEqual(len(param_config['q']), 2)

        param_config = generate_parameter_config(['q', 'u1'], ['s1_max'])
        self.assertEqual(len(param_config['h']), 1)
        self.assertEqual(len(param_config['q']), 2)

        param_config = generate_parameter_config(['s1'], [])
        self.assertEqual(len(param_config['h']), 1)
        self.assertEqual(len(param_config['q']), 0)

    def test_generate_parameter_config_unknown_param(self):
        with self.assertRaises(KeyError):
            generate_parameter_config(['dunno'], [])
