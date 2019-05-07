from builtins import object
import unittest
import mock
import os.path
from sqlite3 import dbapi2 as dbapi
import shutil
import tempfile

from ThreeDiToolbox.threedi_statistics.tools.statistics import StatisticsTool
from ThreeDiToolbox.datasource.threedi_results import ResultData

from ThreeDiToolbox.test.test_datasources import netcdf_groundwater_datasource_nc_path

test_data_dir = os.path.dirname(netcdf_groundwater_datasource_nc_path)


class DummyTimeseriesDatasourceModel(object):
    def __init__(self, modeldb_path, resultnc_path):
        self.model_spatialite_filepath = modeldb_path
        self.resultnc_path = resultnc_path
        self.ds = ResultData(resultnc_path)
        self.rows = [self]

    def datasource(self):
        return self.ds

    def spatialite_cache_filepath(self):
        return self.resultnc_path.replace("results_3di.nc", "gridadmin.sqlite")


class TestStatistics(unittest.TestCase):
    """ In TestStatistics the gridadmin.sqlite is updated: tables are added if
    they not exist (or removed first if they exist). ThreeDiToolbox assumes:
    - gridadmin.sqlite is in same folder as model.sqlite and two netcdf files
    - filename must be "gridadmin.sqlite"
    We do not want to copy (large!) netcdfs to tempdir, therefore we
    - create copy of gridadmin.sqlite into tempdir
    - mock path to gridadmin.sqlite (becomes '/tmpdir/gridadmin.sqlite')
    - remove tempdir (e.g. in a tearDownClass() is not needed apparently """

    @classmethod
    @mock.patch("ThreeDiToolbox.threedi_statistics.tools.statistics.progress_bar")
    @mock.patch("ThreeDiToolbox.threedi_statistics.tools.statistics.pop_up_question")
    def setUpClass(cls, mock_pop_up_question, mock_progress_bar):
        mock_pop_up_question.return_value = True

        orig_gridadmin_sqlite_path = os.path.join(test_data_dir, "gridadmin.sqlite")
        assert os.path.exists(orig_gridadmin_sqlite_path)

        cls.tempdir = tempfile.gettempdir()
        tmp_filename = "tmp_gridadmin.sqlite"
        tmp_filename_path = os.path.join(cls.tempdir, tmp_filename)
        shutil.copy2(orig_gridadmin_sqlite_path, tmp_filename_path)

        def monkey_patch_return_tmp_path():
            return tmp_filename_path

        dummy = DummyTimeseriesDatasourceModel(
            os.path.join(test_data_dir, "v2_bergermeer.sqlite"),
            os.path.join(test_data_dir, "results_3di.nc"),
        )
        dummy.spatialite_cache_filepath = monkey_patch_return_tmp_path

        cls.stat = StatisticsTool(None, dummy)
        # check that path of gridadmin.sqlite is correctly update to the tmp path
        assert cls.stat.ts_datasource.spatialite_cache_filepath() == tmp_filename_path
        cls.stat.get_modeldb_session()
        # calculate statistics
        cls.stat.run()

    def test_files_exist(self):
        model_sqlite_path = os.path.join(test_data_dir, "v2_bergermeer.sqlite")
        gridadmin_sqlite_path = os.path.join(test_data_dir, "gridadmin.sqlite")
        self.assertTrue(os.path.exists(model_sqlite_path))
        self.assertTrue(os.path.exists(gridadmin_sqlite_path))

    def test_flowline_stats_view(self):
        resultdb_path = self.stat.ts_datasource.spatialite_cache_filepath()
        con_res = dbapi.connect(resultdb_path)
        con_res.row_factory = dbapi.Row
        flowline_cursor = con_res.execute(
            "SELECT * FROM flowline_stats_view WHERE id=31878"
        )
        flowline = flowline_cursor.fetchone()
        self.assertAlmostEqual(flowline["cum_discharge"], 20.003, places=3)
        self.assertAlmostEqual(flowline["cum_discharge_positive"], 20.064, places=3)
        self.assertAlmostEqual(flowline["cum_discharge_negative"], 0.0609, places=3)
        self.assertAlmostEqual(flowline["end_discharge"], 0.03558, places=3)
        self.assertAlmostEqual(flowline["max_discharge"], 0.0442, places=3)
        self.assertAlmostEqual(flowline["end_velocity"], 0.00391, places=3)
        self.assertAlmostEqual(flowline["max_velocity"], 0.0060, places=3)
        self.assertAlmostEqual(flowline["max_waterlevel_start"], -1.581, places=3)
        self.assertAlmostEqual(flowline["max_waterlevel_end"], -1.59, places=2)
        self.assertAlmostEqual(flowline["max_head_difference"], 9997.40, places=1)

    def test_manhole_stats_rwa_view(self):
        resultdb_path = self.stat.ts_datasource.spatialite_cache_filepath()
        con_res = dbapi.connect(resultdb_path)
        con_res.row_factory = dbapi.Row
        cursor = con_res.execute("SELECT * FROM manhole_stats_rwa_view WHERE id=10751")
        manhole = cursor.fetchone()
        self.assertAlmostEqual(manhole["duration_water_on_surface"], 0.29599, places=3)
        self.assertAlmostEqual(manhole["max_waterlevel"], -0.47999, places=3)
        self.assertAlmostEqual(manhole["end_waterlevel"], -0.47999, places=3)
        self.assertAlmostEqual(manhole["max_waterdepth_surface"], 0.0700, places=2)
        self.assertAlmostEqual(manhole["end_filling"], 103, places=1)
        self.assertAlmostEqual(manhole["max_filling"], 103, places=1)

    def test_manhole_stats_view(self):
        resultdb_path = self.stat.ts_datasource.spatialite_cache_filepath()
        con_res = dbapi.connect(resultdb_path)
        con_res.row_factory = dbapi.Row
        cursor = con_res.execute("SELECT * FROM manhole_stats_view WHERE id=10780")
        manhole = cursor.fetchone()
        self.assertAlmostEqual(manhole["duration_water_on_surface"], 0.3320, places=3)
        self.assertAlmostEqual(manhole["max_waterlevel"], -0.4699, places=3)
        self.assertAlmostEqual(manhole["end_waterlevel"], -0.5170, places=3)
        self.assertAlmostEqual(manhole["max_waterdepth_surface"], 0.170, places=2)
        self.assertAlmostEqual(manhole["end_filling"], 106.2, places=1)
        self.assertAlmostEqual(manhole["max_filling"], 108.5, places=1)

    def test_pipe_stats_dwa_mixed_view(self):
        resultdb_path = self.stat.ts_datasource.spatialite_cache_filepath()
        con_res = dbapi.connect(resultdb_path)
        con_res.row_factory = dbapi.Row
        cursor = con_res.execute(
            "SELECT * FROM pipe_stats_dwa_mixed_view WHERE id=27468"
        )
        pipe = cursor.fetchone()
        self.assertAlmostEqual(pipe["max_hydro_gradient"], 0, places=3)
        self.assertIsNone(pipe["max_filling"])  # dont know why not just 0
        self.assertIsNone(pipe["end_filling"])  # same here
        self.assertAlmostEqual(pipe["cum_discharge"], 0, places=2)
        self.assertAlmostEqual(pipe["cum_discharge_positive"], 0, places=1)
        self.assertAlmostEqual(pipe["cum_discharge_negative"], 0, places=1)
        self.assertAlmostEqual(pipe["max_discharge"], 0, places=1)
        self.assertAlmostEqual(pipe["end_discharge"], 0, places=1)
        self.assertAlmostEqual(pipe["max_velocity"], 0, places=1)
        self.assertAlmostEqual(pipe["end_velocity"], 0, places=1)
        self.assertAlmostEqual(pipe["max_head_difference"], 0, places=1)
        self.assertIsNone(pipe["max_waterlevel_start"])
        self.assertIsNone(pipe["max_waterlevel_end"])

    def test_pipe_stats_rwa_view(self):
        resultdb_path = self.stat.ts_datasource.spatialite_cache_filepath()
        con_res = dbapi.connect(resultdb_path)
        con_res.row_factory = dbapi.Row
        cursor = con_res.execute("SELECT * FROM pipe_stats_rwa_view WHERE id=27481")
        pipe = cursor.fetchone()
        self.assertAlmostEqual(pipe["max_hydro_gradient"], 14870.6, places=1)
        self.assertAlmostEqual(pipe["max_filling"], 100.0, places=1)
        self.assertAlmostEqual(pipe["end_filling"], 100.0, places=1)
        self.assertAlmostEqual(pipe["cum_discharge"], 83.049, places=2)
        self.assertAlmostEqual(pipe["cum_discharge_positive"], 83.049, places=2)
        self.assertAlmostEqual(pipe["cum_discharge_negative"], 0, places=1)
        self.assertAlmostEqual(pipe["max_discharge"], 0.28464, places=3)
        self.assertAlmostEqual(pipe["end_discharge"], 0.06361, places=3)
        self.assertAlmostEqual(pipe["max_velocity"], 1.4496, places=3)
        self.assertAlmostEqual(pipe["end_velocity"], 0.3239, places=3)
        self.assertAlmostEqual(pipe["max_head_difference"], 9996.79, places=1)
        self.assertAlmostEqual(pipe["max_waterlevel_start"], -0.4699, places=3)
        self.assertAlmostEqual(pipe["max_waterlevel_end"], -0.338, places=3)

    def test_pipe_stats_view(self):
        resultdb_path = self.stat.ts_datasource.spatialite_cache_filepath()
        con_res = dbapi.connect(resultdb_path)
        con_res.row_factory = dbapi.Row
        cursor = con_res.execute("SELECT * FROM pipe_stats_view WHERE id=27485")
        pipe = cursor.fetchone()
        self.assertAlmostEqual(pipe["max_hydro_gradient"], 17635.36, places=2)
        self.assertAlmostEqual(pipe["max_filling"], 100.0, places=1)
        self.assertAlmostEqual(pipe["end_filling"], 100.0, places=1)
        self.assertAlmostEqual(pipe["cum_discharge"], 56.792, places=2)
        self.assertAlmostEqual(pipe["cum_discharge_positive"], 93.040, places=1)
        self.assertAlmostEqual(pipe["cum_discharge_negative"], 36.247, places=1)
        self.assertAlmostEqual(pipe["max_discharge"], 0.3353, places=3)
        self.assertAlmostEqual(pipe["end_discharge"], -0.082, places=3)
        self.assertAlmostEqual(pipe["max_velocity"], 1.1309, places=3)
        self.assertAlmostEqual(pipe["end_velocity"], -0.2136, places=3)
        self.assertAlmostEqual(pipe["max_head_difference"], 9996.60, places=1)
        self.assertAlmostEqual(pipe["max_waterlevel_start"], -0.4069, places=3)
        self.assertAlmostEqual(pipe["max_waterlevel_end"], -0.4799, places=3)

    def test_pump_stats_view(self):
        resultdb_path = self.stat.ts_datasource.spatialite_cache_filepath()
        con_res = dbapi.connect(resultdb_path)
        con_res.row_factory = dbapi.Row
        cursor = con_res.execute("SELECT * FROM pump_stats_view WHERE id=16")
        pump = cursor.fetchone()
        self.assertAlmostEqual(pump["cum_discharge"], 12.667, places=2)
        self.assertAlmostEqual(pump["end_discharge"], 0.0149, places=3)
        self.assertAlmostEqual(pump["max_discharge"], 0.0149, places=3)
        self.assertAlmostEqual(pump["perc_max_discharge"], 100, places=1)
        self.assertAlmostEqual(pump["perc_end_discharge"], 100, places=1)
        self.assertAlmostEqual(pump["perc_end_discharge"], 100, places=1)
        self.assertAlmostEqual(pump["duration_pump_on_max"], 0.2349, places=3)

    def test_weir_stats_view(self):
        resultdb_path = self.stat.ts_datasource.spatialite_cache_filepath()
        con_res = dbapi.connect(resultdb_path)
        con_res.row_factory = dbapi.Row
        cursor = con_res.execute("SELECT * FROM weir_stats_view WHERE id=29857")
        weir = cursor.fetchone()
        self.assertAlmostEqual(weir["perc_volume"], -0.01, places=2)
        self.assertAlmostEqual(weir["perc_volume_positive"], 0.01, places=2)
        self.assertAlmostEqual(weir["perc_volume_negative"], 0.08, places=2)
        self.assertAlmostEqual(weir["max_overfall_height"], 0.114, places=3)
        self.assertAlmostEqual(weir["cum_discharge"], -0.023, places=3)
        self.assertAlmostEqual(weir["cum_discharge_positive"], 0.050, places=3)
        self.assertAlmostEqual(weir["cum_discharge_negative"], 0.0729, places=3)
        self.assertAlmostEqual(weir["max_discharge"], -0.0083, places=3)
        self.assertAlmostEqual(weir["end_discharge"], -0.0083, places=3)
        self.assertAlmostEqual(weir["max_velocity"], -0.0304, places=3)
        self.assertAlmostEqual(weir["end_velocity"], -0.030, places=3)
        self.assertAlmostEqual(weir["max_head_difference"], 0.00050, places=4)
        self.assertAlmostEqual(weir["max_waterlevel_start"], -1.796, places=3)
        self.assertAlmostEqual(weir["max_waterlevel_end"], -1.796, places=3)
