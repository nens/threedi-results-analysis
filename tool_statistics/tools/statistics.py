from ..sql_models.statistics import Flowline
from ..sql_models.statistics import FlowlineStats
from ..sql_models.statistics import ManholeStats
from ..sql_models.statistics import Node
from ..sql_models.statistics import PipeStats
from ..sql_models.statistics import PumplineStats
from ..sql_models.statistics import StatSource
from ..sql_models.statistics import WeirStats
from ..utils.statistics_database import StaticsticsDatabase
from functools import cached_property
from collections import OrderedDict
from qgis.core import QgsDataSourceUri
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.core import NULL
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy import MetaData
from sqlalchemy import text
from sqlalchemy.event import listen
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2
from threedi_results_analysis.datasource.threedi_results import ThreediResult
from threedi_results_analysis.utils.threedi_database import load_spatialite
from threedi_results_analysis.utils.user_messages import pop_up_info
from threedi_results_analysis.utils.user_messages import pop_up_question
from threedi_results_analysis.utils.user_messages import progress_bar

import logging
import numpy as np
import os.path


logger = logging.getLogger(__name__)


class DataSourceAdapter(object):
    """Adapter or proxy-like for a datasource.

    TODO: this whole adapter is only used in the statisticstool below. Can it
    not use the datasource directly? Perhaps timestamps and the "nflowline"
    should be cached on the actual datasource?

    """

    def __init__(self, proxied_datasource):
        """Contructor.

        Args:
            proxied_datasource: BaseDataSource instance that is being proxied
        """
        self.proxied_datasource = proxied_datasource

    def __getattr__(self, attr):
        # __getattr__ runs only on undefined attribute accesses, which is
        # the desired behavior
        return getattr(self.proxied_datasource, attr)

    @cached_property
    def nFlowLine(self):
        if hasattr(self.proxied_datasource, "nFlowLine"):
            return self.proxied_datasource.nFlowLine
        else:
            # TODO: minus 1?
            return (
                self.proxied_datasource.datasource.get("nMesh2D_lines").size
                + self.proxied_datasource.datasource.get("nMesh1D_lines").size
            )

    @property
    def has_groundwater(self):
        return isinstance(self.proxied_datasource, ThreediResult)

    @cached_property
    def timestamps(self):
        # ``get_timestamps`` is a public method, we should use that
        return self.proxied_datasource.get_timestamps()


class StatisticsTool(object):
    """QGIS Plugin Implementation."""

    def __init__(self, iface, ts_datasources):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.ts_datasources = ts_datasources

        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "icons", "icon_statistical_analysis.png")
        self.menu_text = u"Statistical Tool"

        self.plugin_is_active = False
        self.widget = None

        self.toolbox = None
        self.modeldb_engine = None
        self.modeldb_meta = None
        self.db = None
        self.db_meta = None

    def on_unload(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""
        pass

    def get_modeldb_session(self):

        if self.modeldb_engine is None:
            self.modeldb_engine = create_engine(
                "sqlite:///{0}".format(self.ts_datasources.model_spatialite_filepath),
                echo=False,
            )
            listen(self.modeldb_engine, "connect", load_spatialite)

            # activate the spatialite extension!

            self.modeldb_meta = MetaData()
            self.modeldb_meta.reflect(bind=self.modeldb_engine)

        return sessionmaker(bind=self.modeldb_engine)()

    def get_modeldb_table(self, name):
        return self.modeldb_meta.tables[name]

    def run(self, *args, **kwargs):
        """Start processing on first selected model result (netcdf).
        Assumption is that sqlite1 already exist and is filled with flowlines, pumps and nodes.
        """
        # TODO: the last ts_datasource is taken instead of the first.
        # And result_db_qmodel is called active_ts_datasource in the rest of the code.
        threedi_result = self.ts_datasources.rows[-1].threedi_result()
        self.ds = DataSourceAdapter(threedi_result)
        self.result_db_qmodel = self.ts_datasources.rows[0]

        # setup statistics database sqlalchemy instance and create models (
        # if not exist) in the result cache spatialite
        db_type = "spatialite"
        db_set = {
            "db_path": self.result_db_qmodel.sqlite_gridadmin_filepath().replace(
                "\\", "/"
            )
        }

        self.db = StaticsticsDatabase(db_set, db_type)
        self.db_meta = self.db.get_metadata()

        calculate_stats = True
        if self.has_res_views():
            # in test_statistics we mocked 'pop_up_question' and set return value True
            calculate_stats = pop_up_question("Recalculate statistics?", "Recalculate?")

        if calculate_stats:
            logger.info("Start calculating statistics")

            try:
                self.db.create_and_check_fields()
            except dbapi2.OperationalError:
                logger.exception(
                    "Database error, we're suggesting the user to try it again"
                )
                pop_up_info(
                    "Database error. You could try it again, "
                    "in most cases this fixes the problem.",
                    "ERROR",
                )

            with progress_bar(self.iface) as pb:
                pb.setValue(10)
                self.get_manhole_attributes_and_statistics()
                pb.setValue(30)
                self.create_node_views()
                pb.setValue(40)
                self.calc_flowline_statistics()
                pb.setValue(50)
                self.calc_pipe_and_weir_statistics()
                pb.setValue(70)
                self.create_line_views()
                pb.setValue(80)
                self.get_pump_attributes_and_statistics()
                pb.setValue(90)
                self.create_pump_views()
                pb.setValue(100)

        # add layers to QGIS map (this function is mocked in test_statistics)
        self.add_statistic_layers_to_map()

        self.modeldb_engine = None
        self.modeldb_meta = None
        self.db = None
        logger.info("statistic tool finished")

    def has_mod_views(self):
        mod_session = self.get_modeldb_session()  # e.g. v2_bergermeer.sqlite
        view_table = self.get_modeldb_table("views_geometry_columns")
        return (
            mod_session.query(view_table)
            .filter(view_table.c.view_name == "v2_1d_boundary_conditions_view")
            .count()
            != 0
        )

    def has_res_views(self):
        # bugfix explanation: In QGIS2, all tables and views were put in the
        # 'views_geometry_columns' of the model sqlite (e.g.
        # v2_bergermeer.sqlite) or in the gridadmin.sqlite. Somehow in QGIS3
        # all tables in gridadmin.sqlite's 'views_geometry_columns' are not
        # visible. Solved it by putting these layers in the geometry_columns
        # of the gridadmin.sqlite
        res_session = self.db.get_session()  # gridadmin.sqlite'
        table = self.db.get_metadata().tables["geometry_columns"]
        return (
            res_session.query(table)
            .filter(table.c.f_table_name == "pump_stats_view")
            .count()
            != 0
        )

    def get_manhole_attributes_and_statistics(self):
        """read manhole information from model spatialite and put in manhole statistic table"""

        res_session = self.db.get_session()
        mod_session = self.get_modeldb_session()

        logger.info("Create mapping between result id and connection_node_id")

        nodes = res_session.query(Node.spatialite_id, Node.id).filter(
            Node.spatialite_id != None  # NOQA
        )
        node_mapping = {node.spatialite_id: node.id for node in nodes}

        logger.info("Get information from modeldatabase about manholes")
        # get info for querying model database

        manhole_table = self.get_modeldb_table("v2_manhole")
        pipe_table = self.get_modeldb_table("v2_pipe")

        # get idx and surface level
        manholes_ids_without_surface_level = []
        manhole_idx = []
        manhole_surface_levels = []
        invalid_surface_levels = [None, NULL]
        for manhole in mod_session.query(manhole_table).order_by(
            manhole_table.c.connection_node_id
        ):
            manhole_conn_id = manhole.connection_node_id
            manhole_id = manhole.id
            if manhole_conn_id in node_mapping:
                manhole_surface_level = manhole.surface_level
                if manhole_surface_level not in invalid_surface_levels:
                    manhole_idx.append(node_mapping[manhole_conn_id])
                    manhole_surface_levels.append(manhole_surface_level)
                else:
                    error_msg = "Manhole with id '%s' is missing 'surface_level' value."
                    logger.warning(error_msg, manhole_id)
                    manholes_ids_without_surface_level.append(manhole_id)
            else:
                logger.warning("Manhole with id '%s' not in the results.", manhole_id)

        # create numpy arrays for index based reading of the netcdf and
        # surface level for calculating time on surface
        missing_surface_level_manholes = len(manholes_ids_without_surface_level)
        if missing_surface_level_manholes > 0:
            warn_msg = (
                f"{missing_surface_level_manholes} manholes are missing 'surface_level' value. "
                "Check logfile to get more details."
            )
            pop_up_info(warn_msg, "Missing surface level values")
        nr_manholes = len(manhole_idx)
        if nr_manholes == 0:
            logger.warning("No manholes found, skip manhole statistics.")
            return
        manhole_idx = np.array(manhole_idx)
        manhole_surface_levels = np.array(manhole_surface_levels)

        logger.info("Read results and calculate statistics. ")
        # check if statistic is available, otherwise make empty arrays for getting result from normal results
        if "s1_max" in self.ds.available_vars:
            agg_h_max = True
            h_max = np.full(nr_manholes, -9999.0)
            for i, timestamp in enumerate(self.ds.get_timestamps(parameter="s1_max")):
                h = self.ds.get_values_by_timestep_nr("s1_max", i, node_ids=manhole_idx)
                # unmask result (dry cells no have -9999 values
                h_array = np.asarray(h)
                h_max = np.maximum(h_max, h_array)

        else:
            agg_h_max = False
            h_max = np.full(nr_manholes, -9999.0)

        # make empty arrays for the results
        t_water_surface = np.zeros(nr_manholes, dtype=np.float32)

        # loop over timestamps and calculate statistics
        prev_timestamp = 0.0
        for i, timestamp in enumerate(self.ds.timestamps):
            logger.debug("timestamp %i - %i s", i, timestamp)

            timestep = timestamp - prev_timestamp
            prev_timestamp = timestamp
            # read data from netcdf using index to get only manholes
            h = self.ds.get_values_by_timestep_nr("s1", i, node_ids=manhole_idx)

            # unmask result (dry cells no have -9999 values
            h_array = np.asarray(h)
            # calculate statistics
            if not agg_h_max:
                h_max = np.maximum(h_max, h_array)

            t_water_surface[h >= manhole_surface_levels] += timestep

        h_end = self.ds.get_values_by_timestep_nr(
            "s1", len(self.ds.timestamps) - 1, node_ids=manhole_idx
        )

        manhole_stats = []

        logger.info("Make manhole statistic instances ")
        for i, manhole in enumerate(
            mod_session.query(
                manhole_table,
                func.min(pipe_table.c.sewerage_type).label("sewerage_type"),
            )
            .filter(
                (
                    manhole_table.c.connection_node_id
                    == pipe_table.c.connection_node_start_id
                )
                | (
                    manhole_table.c.connection_node_id
                    == pipe_table.c.connection_node_end_id
                )
            )
            .group_by(manhole_table.c.connection_node_id)
            .order_by(manhole_table.c.connection_node_id)
        ):

            if manhole.connection_node_id in node_mapping:
                idx = node_mapping[manhole.connection_node_id]
                # get element number of manhole result array
                manhole_result_array = np.where(manhole_idx == idx)[0]
                if manhole_result_array.size == 0:
                    continue
                ri = int(manhole_result_array[0])
                mhs = ManholeStats(
                    id=idx,
                    code=manhole.code,
                    display_name=manhole.display_name,
                    sewerage_type=manhole.sewerage_type,
                    bottom_level=round(manhole.bottom_level, 3),
                    surface_level=round(manhole.surface_level, 3),
                    duration_water_on_surface=round(t_water_surface[ri] / 3600, 3),
                    max_waterlevel=None
                    if h_max[ri] == -9999.0
                    else round(h_max[ri], 3),
                    end_waterlevel=None
                    if h_end[ri] == -9999.0
                    else round(h_end[ri], 3),
                    max_waterdepth_surface=None
                    if h_max[ri] == -9999.0
                    else round(h_max[ri] - manhole.surface_level, 3),
                    max_filling=None
                    if (
                        h_max[ri] == -9999.0
                        or manhole.surface_level == manhole.bottom_level
                    )
                    else round(
                        100
                        * (h_max[ri] - manhole.bottom_level)
                        / (manhole.surface_level - manhole.bottom_level),
                        1,
                    ),
                    end_filling=None
                    if (
                        h_end[ri] == -9999.0
                        or manhole.surface_level == manhole.bottom_level
                    )
                    else round(
                        100
                        * (h_end[ri] - manhole.bottom_level)
                        / (manhole.surface_level - manhole.bottom_level),
                        1,
                    ),
                )
                manhole_stats.append(mhs)

        logger.info("delete old mahole statistics from database")
        res_session.execute(text(f"Delete from {ManholeStats.__tablename__}"))

        logger.info("Save manhole statistic instances to database ")
        res_session.bulk_save_objects(manhole_stats)
        res_session.commit()

        # store sources in database
        avg_timestep = int(self.ds.timestamps[-1] / (len(self.ds.timestamps) - 1))
        h_param = "s1"
        self.set_stat_source(
            "manhole_stats", "duration_water_on_surface", False, h_param, avg_timestep
        )
        self.set_stat_source(
            "manhole_stats", "end_waterlevel", False, h_param, avg_timestep
        )
        self.set_stat_source(
            "manhole_stats", "end_filling", False, h_param, avg_timestep
        )
        if agg_h_max:
            h_param = "s1_max"
            self.set_stat_source("manhole_stats", "max_waterlevel", True, h_param)
            self.set_stat_source(
                "manhole_stats", "max_waterdepth_surface", True, h_param
            )
            self.set_stat_source("manhole_stats", "max_filling", True, h_param)
        else:
            h_param = "s1"
            self.set_stat_source(
                "manhole_stats", "max_waterlevel", False, h_param, avg_timestep
            )
            self.set_stat_source(
                "manhole_stats", "max_waterdepth_surface", False, h_param, avg_timestep
            )
            self.set_stat_source(
                "manhole_stats", "max_filling", False, h_param, avg_timestep
            )

        return

    def set_stat_source(
        self, table, field, from_aggregated, input_param, timestep=None
    ):
        res_session = self.db.get_session()
        t = StatSource
        instance = (
            res_session.query(t).filter((t.table == table) & (t.field == field)).first()
        )
        if instance:
            instance.from_agg = from_aggregated
            instance.input_param = input_param
            instance.timestep = timestep
        else:
            instance = StatSource(
                table=table,
                field=field,
                from_agg=from_aggregated,
                input_param=input_param,
                timestep=timestep,
            )
            res_session.add(instance)

        res_session.commit()

    def get_agg_cum_if_available(self, parameter_name, nr=None):
        if nr is None:
            nr = self.ds.nFlowLine

        if parameter_name in self.ds.available_vars:
            agg_cum = True
            result = self.ds.get_values_by_timestep_nr(
                parameter_name,
                len(self.ds.get_timestamps(parameter=parameter_name)) - 1,
            )
        else:
            agg_cum = False
            result = np.zeros(nr)
        return result, agg_cum

    def calc_flowline_statistics(self):

        ds = self.ds
        res_session = self.db.get_session()

        logger.info("create mapping to start and end nodes of flowline.")
        start_idx = []
        end_idx = []
        for flowline in res_session.query(Flowline).order_by(Flowline.id):
            start_idx.append(flowline.start_node_idx)
            end_idx.append(flowline.end_node_idx)

        start_idx = np.array(start_idx)
        end_idx = np.array(end_idx)
        logger.info("read flowline results and calculate stats")

        qcum, agg_q_cum = self.get_agg_cum_if_available("q_cum")
        qcum_pos, agg_q_cum_pos = self.get_agg_cum_if_available("q_cum_positive")
        qcum_neg, agg_q_cum_neg = self.get_agg_cum_if_available("q_cum_negative")

        direction = np.full(ds.nFlowLine, 1)
        qmax = np.zeros(ds.nFlowLine)
        qmin = np.zeros(ds.nFlowLine)
        vmax = np.zeros(ds.nFlowLine)
        vmin = np.zeros(ds.nFlowLine)
        dh_max = np.zeros(ds.nFlowLine)
        hmax_start = np.full(ds.nFlowLine, -9999.0)
        hmax_end = np.full(ds.nFlowLine, -9999.0)
        dh_max_calc = True

        prev_timestamp = 0.0
        for i, timestamp in enumerate(ds.timestamps):
            logger.debug("timestamp %i - %i s", i, timestamp)
            timestep = timestamp - prev_timestamp
            prev_timestamp = timestamp

            q = ds.get_values_by_timestep_nr("q", i)

            if not agg_q_cum:
                # todo: most accurate way to calculate cum based on normal netcdf
                qcum += q * timestep
            if not agg_q_cum_pos:
                qcum_pos += q.clip(min=0) * timestep

            if not agg_q_cum_neg:
                qcum_neg -= q.clip(max=0) * timestep

            qmax = np.maximum(qmax, q)
            qmin = np.minimum(qmin, q)

            v = ds.get_values_by_timestep_nr("u1", i)
            vmax = np.maximum(vmax, v)
            vmin = np.minimum(vmin, v)

            h_start = ds.get_values_by_timestep_nr("s1", i, node_ids=start_idx)
            h_end = ds.get_values_by_timestep_nr("s1", i, node_ids=end_idx)

            try:
                np.copyto(
                    dh_max, np.maximum(dh_max, np.asarray(np.absolute(h_start - h_end)))
                )
            except Exception:
                # TODO: this is quite a broad exception. Is that necessary?
                logger.exception(
                    "dh_max is not loaded for timestep %s, setting dh_max_calc to False",
                    timestamp,
                )
                dh_max_calc = False

            hmax_start = np.maximum(hmax_start, np.asarray(h_start))
            hmax_end = np.maximum(hmax_end, np.asarray(h_end))

        # make it work for 2D models
        if not dh_max_calc:
            dh_max = np.zeros(ds.nFlowLine)

        np.copyto(direction, -1, where=qmax < -1 * qmin)
        qmax = np.maximum(qmax, -1 * qmin) * direction

        np.copyto(direction, -1, where=vmax < -1 * vmin)
        vmax = np.maximum(vmax, -1 * vmin) * direction

        qend = ds.get_values_by_timestep_nr("q", len(ds.timestamps) - 1)
        vend = ds.get_values_by_timestep_nr("u1", len(ds.timestamps) - 1)
        hend_start = ds.get_values_by_timestep_nr(
            "s1", len(ds.timestamps) - 1, node_ids=start_idx
        )
        hend_end = ds.get_values_by_timestep_nr(
            "s1", len(ds.timestamps) - 1, node_ids=end_idx
        )

        # save stats to the database
        logger.info("prepare flowline statistics for database")
        flowline_list = []
        for i, flowline in enumerate(
            res_session.query(
                Flowline.id,
                Flowline.the_geom.ST_Transform(28992).ST_Length().label("abs_length"),
            ).order_by(Flowline.id)
        ):
            # CAUTION: qcum can contain np.nan values, which will be casted
            # to None using ``round``
            fls = FlowlineStats(
                id=flowline.id,
                cum_discharge=round(qcum[i], 3),
                cum_discharge_positive=round(qcum_pos[i], 3),
                cum_discharge_negative=round(qcum_neg[i], 3),
                max_discharge=round(qmax[i], 8),
                end_discharge=round(qend[i], 8),
                max_velocity=round(vmax[i], 8),
                end_velocity=round(vend[i], 8),
                max_head_difference=round(dh_max[i], 4),
                max_waterlevel_start=None
                if hmax_start[i] == -9999.0
                else round(hmax_start[i], 3),
                max_waterlevel_end=None
                if hmax_end[i] == -9999.0
                else round(hmax_end[i], 3),
                end_waterlevel_start=None
                if hend_start[i] == -9999.0
                else round(hend_start[i], 3),
                end_waterlevel_end=None
                if hend_end[i] == -9999.0
                else round(hend_end[i], 3),
                abs_length=round(flowline.abs_length, 3),
            )
            flowline_list.append(fls)

        logger.info("delete old flowline statistics from database")
        res_session.execute(text(f"Delete from {FlowlineStats.__tablename__}"))

        logger.info("commit flowline statistics to database")
        res_session.bulk_save_objects(flowline_list)
        res_session.commit()

        # store sources in database
        avg_timestep = int(self.ds.timestamps[-1] / (len(self.ds.timestamps) - 1))
        param = "q"
        self.set_stat_source(
            "flowline_stats", "max_discharge", False, param, avg_timestep
        )
        self.set_stat_source(
            "flowline_stats", "end_discharge", False, param, avg_timestep
        )

        param = "u1"
        self.set_stat_source(
            "flowline_stats", "max_velocity", False, param, avg_timestep
        )
        self.set_stat_source(
            "flowline_stats", "end_velocity", False, param, avg_timestep
        )

        param = "s1"
        if dh_max_calc:
            self.set_stat_source(
                "flowline_stats", "max_head_difference", False, param, avg_timestep
            )
        else:
            self.set_stat_source(
                "flowline_stats", "max_head_difference", False, "-", None
            )

        self.set_stat_source(
            "flowline_stats", "max_waterlevel_start", False, param, avg_timestep
        )
        self.set_stat_source(
            "flowline_stats", "max_waterlevel_end", False, param, avg_timestep
        )
        self.set_stat_source(
            "flowline_stats", "end_waterlevel_start", False, param, avg_timestep
        )
        self.set_stat_source(
            "flowline_stats", "end_waterlevel_end", False, param, avg_timestep
        )
        self.set_stat_source("pipe_stats", "max_filling", False, param, avg_timestep)
        self.set_stat_source("pipe_stats", "end_filling", False, param, avg_timestep)
        self.set_stat_source(
            "pipe_stats", "max_hydro_gradient", False, param, avg_timestep
        )
        self.set_stat_source(
            "weir_stats", "max_overfall_height", False, param, avg_timestep
        )

        if agg_q_cum:
            param = "q_cum"
            self.set_stat_source("flowline_stats", "cum_discharge", True, param)
            self.set_stat_source("weir_stats", "perc_volume", True, param)
        else:
            param = "q"
            self.set_stat_source(
                "flowline_stats", "cum_discharge", False, param, avg_timestep
            )
            self.set_stat_source(
                "weir_stats", "perc_volume", False, param, avg_timestep
            )

        if agg_q_cum_pos:
            param = "q_cum_pos"
            self.set_stat_source(
                "flowline_stats", "cum_discharge_positive", True, param
            )
            self.set_stat_source("weir_stats", "perc_volume_positive", True, param)
        else:
            param = "q"
            self.set_stat_source(
                "flowline_stats", "cum_discharge_positive", False, param, avg_timestep
            )
            self.set_stat_source(
                "weir_stats", "perc_volume_positive", False, param, avg_timestep
            )

        if agg_q_cum_neg:
            param = "q_cum_neg"
            self.set_stat_source(
                "flowline_stats", "cum_discharge_negative", True, param
            )
            self.set_stat_source("weir_stats", "perc_volume_negative", True, param)
        else:
            param = "q"
            self.set_stat_source(
                "flowline_stats", "cum_discharge_negative", False, param, avg_timestep
            )
            self.set_stat_source(
                "weir_stats", "perc_volume_negative", False, param, avg_timestep
            )

    def calc_pipe_and_weir_statistics(self):

        res_session = self.db.get_session()
        mod_session = self.get_modeldb_session()

        # get info for querying model database
        pipe_table = self.get_modeldb_table("v2_pipe")
        profile_table = self.get_modeldb_table("v2_cross_section_definition")
        weir_table = self.get_modeldb_table("v2_weir")
        # cnode_table = self.get_modeldb_table('v2_connection_node')

        logger.info("Create mapping between idx (result) and flowline_idx")
        pipes = res_session.query(Flowline.spatialite_id, Flowline.id).filter(
            Flowline.type == "v2_pipe"
        )
        pipes_mapping = {pipe.spatialite_id: pipe.id for pipe in pipes}

        logger.info("create pipe statistic instances.")
        pipe_stats = []

        for pipe in mod_session.query(
            pipe_table,
            profile_table.c.shape,
            profile_table.c.height,
            profile_table.c.width,
        ).filter(pipe_table.c.cross_section_definition_id == profile_table.c.id):
            if pipe.id not in pipes_mapping:
                logger.warning("no result for pipe with spatialite id %i", pipe.id)
            idx = pipes_mapping[pipe.id]
            if pipe.shape in (1, 2) and pipe.width is not None:
                height = max(pipe.width.split(" "))
            elif pipe.shape in (5, 6) and pipe.height is not None:
                height = max(pipe.height.split(" "))
            else:
                height = None

            ps = PipeStats(
                id=idx,
                code=pipe.code,
                display_name=pipe.display_name,
                sewerage_type=pipe.sewerage_type,
                invert_level_start=pipe.invert_level_start_point,
                invert_level_end=pipe.invert_level_end_point,
                profile_height=height,
            )
            pipe_stats.append(ps)

        logger.info("delete old pipe statistics from database")
        res_session.execute(text(f"Delete from {PipeStats.__tablename__}"))

        logger.info("commit pipe characteristics to database")
        res_session.bulk_save_objects(pipe_stats)
        res_session.commit()

        logger.info("Create mapping between idx (result) and weir spatialite_id")
        res_session = self.db.get_session()
        weirs = res_session.query(Flowline.spatialite_id, Flowline.id).filter(
            Flowline.type == "v2_weir"
        )
        weirs_mapping = {weir.spatialite_id: weir.id for weir in weirs}

        logger.info("create weir statistic instances.")
        weir_stats = []
        for weir in mod_session.query(weir_table):
            idx = weirs_mapping[weir.id]

            ws = WeirStats(
                id=idx,
                code=weir.code,
                display_name=weir.display_name,
                crest_level=weir.crest_level,
            )
            weir_stats.append(ws)

        logger.info("delete old weir statistics from database")
        res_session.execute(text(f"Delete from {WeirStats.__tablename__}"))

        logger.info("commit weir characteristics to database")
        res_session.bulk_save_objects(weir_stats)
        res_session.commit()

        def get_filling(
            start_level, end_level, start_invert_level, end_invert_level, profile_height
        ):
            if (
                None
                in [
                    start_level,
                    end_level,
                    start_invert_level,
                    end_invert_level,
                    profile_height,
                ]
                or profile_height <= 0.0
            ):
                return None

            fill_start = (start_level - start_invert_level) / profile_height
            # make sure it is between 0 and 1
            fill_start = max(0, min(1, fill_start))
            fill_end = (end_level - end_invert_level) / profile_height
            # make sure it is between 0 and 1
            fill_end = max(0, min(1, fill_end))
            # return average
            return round(100 * (fill_start + fill_end) / 2, 3)

        for pipe in res_session.query(PipeStats).join(Flowline).join(FlowlineStats):
            if (
                pipe.flowline.stats.abs_length is not None
                and pipe.flowline.stats.abs_length > 0
                and pipe.flowline.stats.max_head_difference is not None
            ):
                pipe.max_hydro_gradient = round(
                    100
                    * (
                        pipe.flowline.stats.max_head_difference
                        / pipe.flowline.stats.abs_length
                    ),
                    3,
                )

            pipe.max_filling = get_filling(
                pipe.flowline.stats.max_waterlevel_start,
                pipe.flowline.stats.max_waterlevel_end,
                pipe.invert_level_start,
                pipe.invert_level_end,
                pipe.profile_height,
            )
            pipe.end_filling = get_filling(
                pipe.flowline.stats.end_waterlevel_start,
                pipe.flowline.stats.end_waterlevel_end,
                pipe.invert_level_start,
                pipe.invert_level_end,
                pipe.profile_height,
            )

        res_session.commit()

        # get max cum of weir
        max_cum_discharge = (
            res_session.query(func.max(func.abs(FlowlineStats.cum_discharge)))
            .filter(FlowlineStats.id == WeirStats.id)
            .scalar()
        )
        max_cum_discharge_pos = (
            res_session.query(func.max(FlowlineStats.cum_discharge_positive))
            .filter(FlowlineStats.id == WeirStats.id)
            .scalar()
        )
        max_cum_discharge_neg = (
            res_session.query(func.max(FlowlineStats.cum_discharge_negative))
            .filter(FlowlineStats.id == WeirStats.id)
            .scalar()
        )

        for weir in res_session.query(WeirStats).join(Flowline).join(FlowlineStats):
            # Note: the reason why cum_discharge etc. are sometimes None is
            # because they get casted to None from np.nan when ``round``
            # is called (see calc_flowline_statistics)
            weir.perc_volume = (
                None
                if max_cum_discharge == 0.0 or weir.flowline.stats.cum_discharge is None
                else round(
                    100 * weir.flowline.stats.cum_discharge / max_cum_discharge, 2
                )
            )

            weir.perc_volume_positive = (
                None
                if max_cum_discharge_pos == 0.0
                or weir.flowline.stats.cum_discharge_positive is None
                else round(
                    100
                    * weir.flowline.stats.cum_discharge_positive
                    / max_cum_discharge_pos,
                    2,
                )
            )

            weir.perc_volume_negative = (
                None
                if max_cum_discharge_neg == 0.0
                or weir.flowline.stats.cum_discharge_negative is None
                else round(
                    100
                    * weir.flowline.stats.cum_discharge_negative
                    / max_cum_discharge_neg,
                    2,
                )
            )

            waterlevel_start = weir.flowline.stats.max_waterlevel_start
            waterlevel_end = weir.flowline.stats.max_waterlevel_end
            if waterlevel_start is not None and waterlevel_end is not None:
                weir.max_overfall_height = round(
                    max(waterlevel_start, waterlevel_end) - weir.crest_level, 3
                )
            else:
                weir.max_overfall_height = waterlevel_start or waterlevel_end

        res_session.commit()

    def get_pump_attributes_and_statistics(self):
        """read manhole information from model spatialite and put in manhole statistic table"""
        res_session = self.db.get_session()
        logger.info("Get information from modeldatabase about pumps")
        # get info for querying model database
        mod_session = self.get_modeldb_session()
        pump_table = self.get_modeldb_table("v2_pumpstation")

        if "q_pump" not in self.ds.available_vars:
            logger.info("Variable q_pump is not available, skip pump statistics")
            return

        # get pump capacity
        pump_capacity = []
        for pump in mod_session.query(pump_table).order_by(pump_table.c.id):
            pump_capacity.append(pump.capacity)

        # create numpy arrays for index for index based reading of the netcdf and
        # surface level for calculating time on surface
        nr_pumps = len(pump_capacity)

        logger.info("Read results and calculate statistics. ")
        # make empty arrays for the results

        q_cum, agg_q_cum = self.get_agg_cum_if_available("q_pump_cum", nr_pumps)

        q_max = np.zeros(nr_pumps, dtype=np.float32)

        # loop over timestamps and calculate statistics
        prev_timestamp = 0.0
        for i, timestamp in enumerate(self.ds.timestamps):
            logger.debug("timestamp %i - %i s", i, timestamp)

            timestep = timestamp - prev_timestamp
            prev_timestamp = timestamp
            # read data from netcdf using index to get only manholes
            q = self.ds.get_values_by_timestep_nr("q_pump", i)
            # calculate statistics
            if not agg_q_cum:
                q_cum += q * timestep

            q_max = np.maximum(q_max, q)

        q_end = self.ds.get_values_by_timestep_nr("q_pump", len(self.ds.timestamps) - 1)

        pump_stats = []
        logger.info("Make Pumpline statistic instances ")

        id_mapping = None
        if not self.ds.has_groundwater:
            # no idmapping info in pumpline model, so get from idmapping file
            id_mapping = self.ds.id_mapping["v2_pumpstation"]

        max_q_cum = q_cum.max()

        for i, pump in enumerate(
            mod_session.query(pump_table).order_by(pump_table.c.id)
        ):
            if not self.ds.has_groundwater:
                # no idmapping info in pumpline model, so get from idmapping file
                id_ = id_mapping[str(pump.id)] - 1
            else:
                # groundwater version doesn't have id_mapping. But the pump
                # ids are basically the enumeration of the sorted spatialite
                # ids, starting at 1 (hence the + 1).
                id_ = i + 1
            ps = PumplineStats(
                id=id_,
                spatialite_id=pump.id,
                code=pump.code,
                display_name=pump.display_name,
                capacity=pump.capacity / 1000,
                cum_discharge=round(q_cum[i], 3),
                end_discharge=round(q_end[i], 8),
                max_discharge=round(q_max[i], 8),
                duration_pump_on_max=(
                    None
                    if pump.capacity == 0.0
                    else round(q_cum[i] / (pump.capacity / 1000) / 3600, 3)
                ),
                perc_cum_discharge=None
                if max_q_cum == 0.0
                else round(100 * q_cum[i] / max_q_cum, 1),
                perc_max_discharge=None
                if pump.capacity == 0.0
                else round(100 * q_max[i] / (pump.capacity / 1000), 1),
                perc_end_discharge=None
                if pump.capacity == 0.0
                else round(100 * q_end[i] / (pump.capacity / 1000), 1),
            )
            pump_stats.append(ps)

        logger.info("delete old pumpline statistics from database")
        res_session.execute(text(f"Delete from {PumplineStats.__tablename__}"))

        logger.info("Save pumpline statistic instances to database ")
        res_session.bulk_save_objects(pump_stats)
        res_session.commit()

        # store sources in database
        avg_timestep = int(self.ds.timestamps[-1] / (len(self.ds.timestamps) - 1))
        param = "q_pump"
        self.set_stat_source(
            "pumpline_stats", "end_discharge", False, param, avg_timestep
        )
        self.set_stat_source(
            "pumpline_stats", "max_discharge", False, param, avg_timestep
        )
        self.set_stat_source(
            "pumpline_stats", "perc_end_discharge", False, param, avg_timestep
        )

        if agg_q_cum:
            param = "q_pump_cum"
            self.set_stat_source("pumpline_stats", "cum_discharge", True, param)
            self.set_stat_source("pumpline_stats", "duration_pump_on_max", True, param)
            self.set_stat_source("pumpline_stats", "perc_max_discharge", True, param)
            self.set_stat_source("pumpline_stats", "perc_cum_discharge", True, param)
        else:
            param = "q_pump"
            self.set_stat_source(
                "pumpline_stats", "cum_discharge", False, param, avg_timestep
            )
            self.set_stat_source(
                "pumpline_stats", "duration_pump_on_max", False, param, avg_timestep
            )
            self.set_stat_source(
                "pumpline_stats", "perc_max_discharge", False, param, avg_timestep
            )
            self.set_stat_source(
                "pumpline_stats", "perc_cum_discharge", False, param, avg_timestep
            )
        return

    def create_line_views(self):

        session = self.db.get_session()

        # flowline stat view
        session.execute(text(
            """
            CREATE VIEW IF NOT EXISTS flowline_stats_view AS
            SELECT f.id,
                   f.inp_id,
                   f.spatialite_id,
                   f.type as TYPE,
                   f.start_node_idx,
                   f.end_node_idx,
                   f.the_geom,
                   fs.cum_discharge,
                   fs.cum_discharge_positive,
                   fs.cum_discharge_negative,
                   fs.max_discharge,
                   fs.end_discharge,
                   fs.max_velocity,
                   fs.end_velocity,
                   fs.max_head_difference,
                   fs.max_waterlevel_start,
                   fs.max_waterlevel_end
            FROM flowlines f,
                 flowline_stats fs
            WHERE f.id = fs.id;
           """
        ))

        session.execute(text(
            """
            DELETE FROM geometry_columns WHERE f_table_name = 'flowline_stats_view';
            """
        ))
        session.execute(text(
            """
            INSERT INTO geometry_columns (
                f_table_name, f_geometry_column, geometry_type,
                coord_dimension, SRID, spatial_index_enabled)
            VALUES ('flowline_stats_view', 'the_geom', 2, 2, 4326, 0);
            """
        ))

        session.commit()

        # pipe stat view
        session.execute(text(
            """
            CREATE VIEW IF NOT EXISTS pipe_stats_view AS
            SELECT f.id,
                   f.inp_id,
                   f.spatialite_id,
                   f.type AS TYPE,
                   f.start_node_idx,
                   f.end_node_idx,
                   f.the_geom,
                   ps.code,
                   ps.display_name,
                   ps.sewerage_type,
                   fs.abs_length,
                   ps.invert_level_start,
                   ps.invert_level_end,
                   ps.profile_height,
                   ps.max_hydro_gradient,
                   ps.max_filling,
                   ps.end_filling,
                   fs.cum_discharge,
                   fs.cum_discharge_positive,
                   fs.cum_discharge_negative,
                   fs.max_discharge,
                   fs.end_discharge,
                   fs.max_velocity,
                   fs.end_velocity,
                   fs.max_head_difference,
                   fs.max_waterlevel_start,
                   fs.max_waterlevel_end
            FROM flowlines f,
                 flowline_stats fs,
                 pipe_stats ps
            WHERE f.id = fs.id
              AND f.id = ps.id;
            """
        ))

        session.execute(text(
            """
            DELETE FROM geometry_columns WHERE f_table_name = 'pipe_stats_view';
            """
        ))
        session.execute(text(
            """
            INSERT INTO geometry_columns (
                f_table_name, f_geometry_column, geometry_type,
                coord_dimension, SRID, spatial_index_enabled)
            VALUES ('pipe_stats_view', 'the_geom', 2, 2, 4326, 0);
            """
        ))

        session.commit()

        # dwa+mixed of pipestats
        session.execute(text(
            """
            CREATE VIEW IF NOT EXISTS pipe_stats_dwa_mixed_view
             AS
             SELECT *
             FROM pipe_stats_view
             WHERE pipe_stats_view.sewerage_type IN (0, 2);
            """
        ))

        session.execute(text(
            """
            DELETE FROM geometry_columns WHERE f_table_name = 'pipe_stats_dwa_mixed_view';
            """
        ))
        session.execute(text(
            """
                INSERT INTO geometry_columns (
                    f_table_name, f_geometry_column, geometry_type,
                    coord_dimension, SRID, spatial_index_enabled)
                VALUES ('pipe_stats_dwa_mixed_view', 'the_geom', 2, 2, 4326, 0);
            """
        ))

        session.commit()

        # rwa views of pipestats
        session.execute(text(
            """
            CREATE VIEW IF NOT EXISTS pipe_stats_rwa_view
            AS
            SELECT *
            FROM pipe_stats_view
            WHERE pipe_stats_view.sewerage_type IN (1);
            """
        ))

        session.execute(text(
            """
            DELETE FROM geometry_columns WHERE f_table_name = 'pipe_stats_rwa_view';
            """
        ))
        session.execute(text(
            """
                INSERT INTO geometry_columns (f_table_name, f_geometry_column, geometry_type, coord_dimension,
                  SRID, spatial_index_enabled)
                VALUES ('pipe_stats_rwa_view', 'the_geom', 2, 2, 4326, 0);
            """
        ))

        session.commit()

        # weir stat view
        session.execute(text(
            """
            CREATE VIEW IF NOT EXISTS weir_stats_view AS
            SELECT f.id,
                   f.inp_id,
                   f.spatialite_id,
                   f.type as TYPE,
                   f.start_node_idx,
                   f.end_node_idx,
                   f.the_geom,
                   ws.code,
                   ws.display_name,
                   ws.perc_volume,
                   ws.perc_volume_positive,
                   ws.perc_volume_negative,
                   ws.max_overfall_height,
                   fs.cum_discharge,
                   fs.cum_discharge_positive,
                   fs.cum_discharge_negative,
                   fs.max_discharge,
                   fs.end_discharge,
                   fs.max_velocity,
                   fs.end_velocity,
                   fs.max_head_difference,
                   fs.max_waterlevel_start,
                   fs.max_waterlevel_end
            FROM flowlines f,
                 flowline_stats fs,
                 weir_stats ws
            WHERE f.id = fs.id
              AND f.id = ws.id;
                """
        ))

        session.execute(text(
            """
            DELETE FROM geometry_columns WHERE f_table_name = 'weir_stats_view';
            """
        ))
        session.execute(text(
            """
                INSERT INTO geometry_columns (f_table_name, f_geometry_column, geometry_type, coord_dimension,
                  SRID, spatial_index_enabled)
                VALUES ('weir_stats_view', 'the_geom', 2, 2, 4326, 0);
            """
        ))

        session.commit()

    def create_node_views(self):
        session = self.db.get_session()

        # manhole stat view
        session.execute(text(
            """
            CREATE VIEW IF NOT EXISTS manhole_stats_view AS
            SELECT n.id,
                   n.inp_id,
                   n.spatialite_id,
                   n.featuretype,
                   n.type as TYPE,
                   n.the_geom,
                   mst.code,
                   mst.display_name,
                   mst.sewerage_type,
                   mst.bottom_level,
                   mst.surface_level,
                   mst.duration_water_on_surface,
                   mst.max_waterlevel,
                   mst.end_waterlevel,
                   mst.max_waterdepth_surface,
                   mst.end_filling,
                   mst.max_filling
            FROM nodes n,
                 manhole_stats mst
            WHERE n.id = mst.id;
            """
        ))

        session.execute(text(
            """
            DELETE FROM geometry_columns WHERE f_table_name = 'manhole_stats_view';
            """
        ))
        session.execute(text(
            """
                INSERT INTO geometry_columns (f_table_name, f_geometry_column, geometry_type, coord_dimension,
                  SRID, spatial_index_enabled)
                VALUES ('manhole_stats_view', 'the_geom', 1, 2, 4326, 0);
            """
        ))

        session.commit()

        # dwa+mixed  of manholestats
        session.execute(text(
            """
            CREATE VIEW IF NOT EXISTS manhole_stats_dwa_mixed_view

             AS
            SELECT *
             FROM manhole_stats_view
             WHERE manhole_stats_view.sewerage_type IN (0, 2);
            """
        ))

        session.execute(text(
            """
            DELETE FROM geometry_columns WHERE f_table_name = 'manhole_stats_dwa_mixed_view';
            """
        ))
        session.execute(text(
            """
                INSERT INTO geometry_columns (f_table_name, f_geometry_column, geometry_type, coord_dimension,
                  SRID, spatial_index_enabled)
                VALUES ('manhole_stats_dwa_mixed_view', 'the_geom', 1, 2, 4326, 0);
            """
        ))

        session.commit()

        # rwa views of manholestats
        session.execute(text(
            """
            CREATE VIEW IF NOT EXISTS manhole_stats_rwa_view
             AS
            SELECT *
             FROM manhole_stats_view
             WHERE manhole_stats_view.sewerage_type IN (1);
            """
        ))

        session.execute(text(
            """
            DELETE FROM geometry_columns WHERE f_table_name = 'manhole_stats_rwa_view';
            """
        ))
        session.execute(text(
            """
                INSERT INTO geometry_columns (f_table_name, f_geometry_column, geometry_type, coord_dimension,
                  SRID, spatial_index_enabled)
                VALUES ('manhole_stats_rwa_view', 'the_geom', 1, 2, 4326, 0);
            """
        ))

        session.commit()

    def create_pump_views(self):
        session = self.db.get_session()

        # pump stat view Lines
        session.execute(text(
            """
            CREATE VIEW IF NOT EXISTS pump_stats_view AS
            SELECT p.id,
                   p.node_idx1,
                   p.node_idx2,
                   p.the_geom,
                   ps.spatialite_id,
                   ps.code,
                   ps.display_name,
                   ps.capacity,
                   ps.cum_discharge,
                   ps.end_discharge,
                   ps.max_discharge,
                   ps.perc_max_discharge,
                   ps.perc_end_discharge,
                   ps.perc_cum_discharge,
                   ps.duration_pump_on_max
            FROM pumplines p,
                 pumpline_stats ps
            WHERE p.id = ps.id;
            """
        ))

        session.execute(text(
            """
            DELETE FROM geometry_columns WHERE f_table_name = 'pump_stats_view';
            """
        ))
        session.execute(text(
            """
                INSERT INTO geometry_columns (f_table_name, f_geometry_column, geometry_type, coord_dimension,
                  SRID, spatial_index_enabled)
                VALUES ('pump_stats_view', 'the_geom', 2, 2, 4326, 0);
            """
        ))

        # pump stat view Lines - points
        session.execute(text(
            """
            CREATE VIEW IF NOT EXISTS pump_stats_point_view AS
            SELECT p.id AS ROWID,
                   p.id AS id,
                   p.node_idx1,
                   p.node_idx2,
                   StartPoint(p.the_geom) AS the_geom,
                   ps.spatialite_id,
                   ps.code,
                   ps.display_name,
                   ps.capacity,
                   ps.cum_discharge,
                   ps.end_discharge,
                   ps.max_discharge,
                   ps.perc_max_discharge,
                   ps.perc_end_discharge,
                   ps.perc_cum_discharge,
                   ps.duration_pump_on_max
            FROM pumplines p,
                 pumpline_stats ps
            WHERE p.id = ps.id;
            """
        ))
        session.execute(text(
            """
            DELETE FROM geometry_columns WHERE f_table_name = 'pump_stats_point_view';
            """
        ))
        session.execute(text(
            """
                INSERT INTO geometry_columns (f_table_name, f_geometry_column, geometry_type, coord_dimension,
                  SRID, spatial_index_enabled)
                VALUES ('pump_stats_point_view', 'the_geom', 1, 2, 4326, 0);
            """
        ))

        session.commit()

    def add_statistic_layers_to_map(self):
        # {layer_name: [(name, layer, field, style,), ...], ... }

        styled_layers = OrderedDict(
            [
                (
                    "pipes",
                    [
                        (
                            "discharge (max) [m3/s]",
                            "pipe_stats_view",
                            "max_discharge",
                            "leiding_1",
                        ),
                        (
                            "velocity (max) [m/s]",
                            "pipe_stats_view",
                            "max_velocity",
                            "leiding_1",
                        ),
                        (
                            "gradient (max) [cm/m]",
                            "pipe_stats_view",
                            "max_hydro_gradient",
                            "leiding_1",
                        ),
                        (
                            "velocity (end)",
                            "pipe_stats_view",
                            "end_velocity",
                            "leiding_2",
                        ),
                        (
                            "velocity DWF and CSF (end)",
                            "pipe_stats_dwa_mixed_view",
                            "end_velocity",
                            "leiding_2",
                        ),
                        (
                            "velocity SWF (end)",
                            "pipe_stats_rwa_view",
                            "end_velocity",
                            "leiding_2",
                        ),
                    ],
                ),
                (
                    "manholes",
                    [
                        (
                            "fill level (max) [%]",
                            "manhole_stats_view",
                            "max_filling",
                            "vullingsgraad_put",
                        ),
                        (
                            "fill level DWF and CSF (end) [%]",
                            "manhole_stats_dwa_mixed_view",
                            "end_filling",
                            "vullingsgraad_put",
                        ),
                        (
                            "fill level SWF (end) [%]",
                            "manhole_stats_rwa_view",
                            "end_filling",
                            "vullingsgraad_put",
                        ),
                        (
                            "duration water on street [hr]",
                            "manhole_stats_view",
                            "duration_water_on_surface",
                            "wos",
                        ),
                        (
                            "waterdepth (max) [m]",
                            "manhole_stats_view",
                            "max_waterdepth_surface",
                            "put_0",
                        ),
                        (
                            "waterdepth DWF and CSF (max) [m]",
                            "manhole_stats_dwa_mixed_view",
                            "max_waterdepth_surface",
                            "put_0",
                        ),
                        (
                            "waterdepth SWF (max) [m]",
                            "manhole_stats_rwa_view",
                            "max_waterdepth_surface",
                            "put_0",
                        ),
                    ],
                ),
                (
                    "pumps",
                    [
                        (
                            "percentage of pump capacity in use (max) [%]",
                            "pump_stats_point_view",
                            "perc_max_discharge",
                            "pumps_100",
                        ),
                        (
                            "percentage of pump capacity in use (end) [%]",
                            "pump_stats_point_view",
                            "perc_end_discharge",
                            "pumps_100",
                        ),
                        (
                            "total pumped volume [m3]",
                            "pump_stats_point_view",
                            "perc_cum_discharge",
                            "pumps_100",
                        ),
                        (
                            "pump duration on max capacity [hr]",
                            "pump_stats_point_view",
                            "duration_pump_on_max",
                            "pumps_8",
                        ),
                    ],
                ),
                (
                    "weirs",
                    [
                        (
                            "head difference (max)",
                            "weir_stats_view",
                            "max_overfall_height",
                            "overstort",
                        ),
                        (
                            "overflow volume (cum) [% to max]",
                            "weir_stats_view",
                            "perc_volume",
                            "overstort_perc",
                        ),
                        (
                            "positive overflow volume (cum) [% to max]",
                            "weir_stats_view",
                            "perc_volume_positive",
                            "overstort_perc",
                        ),
                        (
                            "negative overflow volume (cum) [% to max]",
                            "weir_stats_view",
                            "perc_volume_negative",
                            "overstort_perc",
                        ),
                    ],
                ),
            ]
        )

        root = QgsProject.instance().layerTreeRoot()

        stats_group_name = "statistics"
        stat_group = root.findGroup(stats_group_name)
        if stat_group is None:
            stat_group = root.insertGroup(0, stats_group_name)

        stat_group.removeAllChildren()

        # add source stat metadata
        uri = QgsDataSourceUri()
        uri.setDatabase(
            self.result_db_qmodel.sqlite_gridadmin_filepath().replace("\\", "/")
        )
        uri.setDataSource("", "stat_source", "")

        vector_layer = QgsVectorLayer(uri.uri(), "metadata statistics", "spatialite")
        QgsProject.instance().addMapLayer(vector_layer, False)

        stat_group.insertLayer(0, vector_layer)

        for group, layers in list(styled_layers.items()):
            qgroup = stat_group.insertGroup(100, group)
            qgroup.setExpanded(False)

            for layer in layers:
                uri = QgsDataSourceUri()
                uri.setDatabase(
                    self.result_db_qmodel.sqlite_gridadmin_filepath().replace("\\", "/")
                )
                uri.setDataSource("", layer[1], "the_geom")

                vector_layer = QgsVectorLayer(uri.uri(), layer[0], "spatialite")

                if vector_layer.isValid():
                    style_path = os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        os.path.pardir,
                        "layer_styles",
                        "stats",
                        layer[3] + ".qml",
                    )
                    style = open(style_path, "r").read()

                    # replace by column name
                    style = style.replace("<<variable>>", layer[2])

                    new_style_path = os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        os.path.pardir,
                        "layer_styles",
                        "stats",
                        "cr_" + layer[3] + "_" + layer[2] + ".qml",
                    )

                    new_style_file = open(new_style_path, "w")
                    new_style_file.write(style)
                    new_style_file.close()

                    vector_layer.loadNamedStyle(new_style_path)

                    QgsProject.instance().addMapLayer(vector_layer, False)

                    qgroup.insertLayer(100, vector_layer)
