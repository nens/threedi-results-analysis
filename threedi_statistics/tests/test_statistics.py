import unittest
import os.path

from zThreeDiStatistics.tools.statistics import StatisticsTool
from ThreeDiToolbox.datasource.netcdf import NetcdfDataSource

from pyspatialite import dbapi2 as dbapi

test_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


class DummyTimeseriesDatasourceModel(object):

    def __init__(self, modeldb_path, resultnc_path):
        self.model_spatialite_filepath = modeldb_path
        self.resultnc_path = resultnc_path
        self.ds = NetcdfDataSource(resultnc_path)
        self.rows = [
            self
        ]

    def datasource(self):
        return self.ds

    def spatialite_cache_filepath(self):
        return self.resultnc_path.replace('subgrid_map.nc', 'subgrid_map.sqlite1')


class TestStatistics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.stat = StatisticsTool(
            None,
            DummyTimeseriesDatasourceModel(
                os.path.join(test_data_dir, 'ds_jonas.sqlite'),
                os.path.join(test_data_dir, 'subgrid_map.nc')
            )
        )

        cls.stat.get_modeldb_session()
        cls.stat.run(test=True)

    def test_flowlines(self):
        resultdb_path = self.stat.ts_datasource.spatialite_cache_filepath()
        con_res = dbapi.connect(resultdb_path)
        con_res.row_factory = dbapi.Row

        flowline_cursor = con_res.execute(
            'SELECT '
            '* '
            'FROM pipe_stats_view '
            'WHERE id=4473 '
        )
        flowline = flowline_cursor.fetchone()

        # self.assertAlmostEqual(flowline['cum_discharge'],  47.152777, places=1)
        # self.assertAlmostEqual(flowline['cum_discharge_positive'], 47.152777, places=1)
        # uit aggregatie netcdf
        self.assertAlmostEqual(flowline['cum_discharge'], 47.1212, places=3)
        self.assertAlmostEqual(flowline['cum_discharge_positive'], 47.1212, places=3)
        self.assertAlmostEqual(flowline['cum_discharge_negative'], 0, places=3)
        self.assertAlmostEqual(flowline['end_discharge'], 0.007, places=3)
        self.assertAlmostEqual(flowline['max_discharge'], 0.007, places=3)
        self.assertAlmostEqual(flowline['end_velocity'], 0.4, places=3)
        self.assertAlmostEqual(flowline['max_velocity'], 0.4, places=3)
        self.assertAlmostEqual(flowline['max_waterlevel_start'], 1.6222, places=3)
        self.assertAlmostEqual(flowline['max_waterlevel_end'], 1.49941, places=3)

        self.assertAlmostEqual(flowline['max_head_difference'], 0.67466742, places=3)

        self.assertAlmostEqual(flowline['max_filling'], 7.2279, places=1)
        self.assertAlmostEqual(flowline['end_filling'], 7.2279, places=1)
        self.assertAlmostEqual(flowline['max_hydro_gradient'], 1.349335, places=3)  # 0.67466742 /50 * 100

    def test_flowlines_negative(self):
        resultdb_path = self.stat.ts_datasource.spatialite_cache_filepath()
        con_res = dbapi.connect(resultdb_path)
        con_res.row_factory = dbapi.Row

        flowline_cursor = con_res.execute(
            'SELECT '
            '* '
            'FROM pipe_stats_view '
            'WHERE id=4475 '
        )
        flowline = flowline_cursor.fetchone()

        # self.assertAlmostEqual(flowline['cum_discharge'],  47.152777, places=1)
        # self.assertAlmostEqual(flowline['cum_discharge_positive'], 47.152777, places=1)
        # uit aggregatie netcdf
        self.assertAlmostEqual(flowline['cum_discharge'], -0.166, places=3)
        self.assertAlmostEqual(flowline['cum_discharge_positive'], 0, places=3)
        self.assertAlmostEqual(flowline['cum_discharge_negative'], 0.166, places=3)
        self.assertAlmostEqual(flowline['end_discharge'], 0, places=3)
        self.assertAlmostEqual(flowline['max_discharge'], -0.00017881, places=6)
        self.assertAlmostEqual(flowline['end_velocity'], 0, places=3)
        self.assertAlmostEqual(flowline['max_velocity'], -0.06418, places=3)

    def test_weir(self):
        resultdb_path = self.stat.ts_datasource.spatialite_cache_filepath()
        con_res = dbapi.connect(resultdb_path)
        con_res.row_factory = dbapi.Row

        cursor = con_res.execute(
            'SELECT '
            '* '
            'FROM weir_stats_view '
            'WHERE spatialite_id=6003 '
        )
        weir = cursor.fetchone()

        self.assertAlmostEqual(weir['max_waterlevel_start'], 1.09199, places=3)
        self.assertIsNone(weir['max_waterlevel_end'])
        self.assertAlmostEqual(weir['max_overfall_height'], -1.408, places=3)
        self.assertIsNone(weir['perc_volume'])

    def test_pump(self):
        resultdb_path = self.stat.ts_datasource.spatialite_cache_filepath()
        con_res = dbapi.connect(resultdb_path)
        con_res.row_factory = dbapi.Row

        cursor = con_res.execute(
            'SELECT '
            '* '
            'FROM pumpline_stats '
            'WHERE spatialite_id=61 '
        )
        pump = cursor.fetchone()

        # self.assertAlmostEqual(pump['cum_discharge'], 5.822114, places=3)
        self.assertAlmostEqual(pump['end_discharge'], 0.001, places=8)
        self.assertAlmostEqual(pump['max_discharge'], 0.003993951, places=3)
        self.assertAlmostEqual(pump['perc_max_discharge'], 99.85, places=2)
        self.assertAlmostEqual(pump['perc_end_discharge'], 25.0, places=1)
        self.assertAlmostEqual(pump['perc_cum_discharge'], 12.6584, places=2)
        self.assertAlmostEqual(pump['duration_pump_on_max'], 0.404313, places=3)

    def test_manholes(self):
        resultdb_path = self.stat.ts_datasource.spatialite_cache_filepath()
        con_res = dbapi.connect(resultdb_path)
        con_res.row_factory = dbapi.Row

        cursor = con_res.execute(
            'SELECT '
            '* '
            'FROM manhole_stats_view '
            'WHERE spatialite_id=1005 '
        )
        manhole = cursor.fetchone()

        self.assertAlmostEqual(manhole['max_waterlevel'], 0.046200, places=3)
        self.assertAlmostEqual(manhole['end_waterlevel'], 0.046172, places=3)
        self.assertAlmostEqual(manhole['max_waterdepth_surface'], -3.454, places=3)
        self.assertAlmostEqual(manhole['end_filling'], 1.3192, places=1)
        self.assertAlmostEqual(manhole['max_filling'], 1.32, places=1)
