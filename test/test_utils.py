"""
Test utils.
"""
import unittest
from ThreeDiToolbox.utils.layer_from_netCDF import make_flowline_layer


class TestLayerFuncs(unittest.TestCase):
    def test_smoke(self):
        make_flowline_layer
