import unittest

from ThreeDiToolbox.stats.ncstats import NcStats, NcStatsAgg


class TestNcStats(unittest.TestCase):
    """Test the NcStats class"""

    def test_smoke(self):
        ncstats = NcStats(datasource='mock')
        self.assertEqual(ncstats.datasource, 'mock')

    def test_available_parameters1(self):
        """Test that we can get all the methods defined in
        AVAILABLE_STRUCTURE_PARAMETERS"""
        ncstats = NcStats(datasource='mock')
        for parameter_name in ncstats.AVAILABLE_STRUCTURE_PARAMETERS:
            # if this crashes a method isn't implemented
            getattr(ncstats, parameter_name)

    def test_available_parameters2(self):
        """Test that we can get all the methods defined in
        AVAILABLE_MANHOLE_PARAMETERS"""
        ncstats = NcStats(datasource='mock')
        for parameter_name in ncstats.AVAILABLE_MANHOLE_PARAMETERS:
            # if this crashes a method isn't implemented
            getattr(ncstats, parameter_name)


class TestNcStatsAgg(unittest.TestCase):
    """Test the NcStatsAgg class"""

    def test_smoke(self):
        ncstats = NcStatsAgg(datasource='mock')
        self.assertEqual(ncstats.datasource, 'mock')

    def test_available_parameters1(self):
        """Test that we can get all the methods defined in
        AVAILABLE_STRUCTURE_PARAMETERS"""
        ncstats = NcStatsAgg(datasource='mock')
        for parameter_name in ncstats.AVAILABLE_STRUCTURE_PARAMETERS:
            # if this crashes a method isn't implemented
            getattr(ncstats, parameter_name)

    def test_available_parameters2(self):
        """Test that we can get all the methods defined in
        AVAILABLE_MANHOLE_PARAMETERS"""
        ncstats = NcStatsAgg(datasource='mock')
        for parameter_name in ncstats.AVAILABLE_MANHOLE_PARAMETERS:
            # if this crashes a method isn't implemented
            getattr(ncstats, parameter_name)
