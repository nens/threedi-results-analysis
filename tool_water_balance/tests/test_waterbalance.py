from pathlib import Path
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsCoordinateTransform
from qgis.core import QgsGeometry
from qgis.core import QgsPointXY
from qgis.core import QgsProject
from ThreeDiToolbox.tests.test_init import TEST_DATA_DIR
from ThreeDiToolbox.tests.utilities import ensure_qgis_app_is_initialized
from ThreeDiToolbox.tool_result_selection.models import TimeseriesDatasourceModel
from ThreeDiToolbox.tool_water_balance.tools.waterbalance import WaterBalanceCalculation
from ThreeDiToolbox.tool_water_balance.views.waterbalance_widget import BarManager
from ThreeDiToolbox.tool_water_balance.views.waterbalance_widget import INPUT_SERIES
from ThreeDiToolbox.tool_water_balance.views.waterbalance_widget import (
    WaterBalanceWidget,
)

import mock
import numpy as np
import pytest


TESTMODEL_DIR = TEST_DATA_DIR.joinpath("testmodel", "v2_bergermeer")
MODEL_SQLITE_PATH = TESTMODEL_DIR / "v2_bergermeer.sqlite"
assert Path.is_dir(TESTMODEL_DIR), "testmodel dir not found"
assert Path.is_file(MODEL_SQLITE_PATH), "modelspatialite not found"


# links_expected consists of (lines, pumps)
LINKS_EXPECTED = (
    {
        "1d_in": [29136],
        "1d_out": [],
        "1d_bound_in": [],
        "1d_bound_out": [],
        "2d_in": [1557, 3689, 3690, 3710, 4879, 6573, 8900, 8901, 8964, 10314],
        "2d_out": [3730, 4895, 5348, 10347, 10369],
        "2d_bound_in": [],
        "2d_bound_out": [],
        "1d__1d_2d_flow": [],
        "2d__1d_2d_flow": [],
        "1d_2d_exch": [30649, 31654],
        "2d_groundwater_in": [
            17968,
            20100,
            20101,
            20121,
            21290,
            22984,
            25311,
            25312,
            25375,
            26725,
        ],
        "2d_groundwater_out": [20141, 21306, 21759, 26758, 26780],
        "2d_vertical_infiltration": [11591, 11592, 12503, 12504, 12517, 14931],
    },
    {"in": [], "out": []},
)

NODES_EXPECTED = {
    "1d": [11553, 12961],
    "2d": [554, 555, 1466, 1467, 1480, 3894],
    "2d_groundwater": [5928, 5929, 6840, 6841, 6854, 9268],
}

TIMESTEPS_EXPECTED = np.array(
    [
        0.0,
        300.46375545,
        602.91879098,
        918.32741104,
        1204.65442229,
        1504.12043258,
        1801.25668355,
    ]
)


def helper_round_numpy(one_array):
    """round numpy values to certain decimal precision so that we can test it
    more easily """
    DECIMAL_PRECISION = 6
    return np.around(one_array, decimals=DECIMAL_PRECISION)


def helper_get_input_series_id(input_serie_name):
    id_found = [id[1] for id in INPUT_SERIES if id[0] == input_serie_name]
    assert len(id_found) == 1
    return id_found[0]


def helper_calculate_agg_flow(aggregated_flows, input_serie_id):
    timesteps = aggregated_flows[0]
    all_time_series = aggregated_flows[1]
    cum_flow = 0
    prev_t = 0
    for timestep_index, time in enumerate(timesteps):
        dt = time - prev_t
        prev_t = time
        flow = all_time_series[timestep_index, input_serie_id] * dt
        cum_flow += flow
    return cum_flow


@pytest.fixture
def wb_polygon():
    """WaterBalancePolyon is to select links, nodes, pumps from model schematisation"""
    POINTS_IN_WGS84 = True
    polygon_points = [
        QgsPointXY(4.70635793604164299, 52.64214387449186461),
        QgsPointXY(4.70644905107772882, 52.64329192394655621),
        QgsPointXY(4.70765176955406783, 52.64332836996099019),
        QgsPointXY(4.70806178721645541, 52.6419889789305202),
        QgsPointXY(4.70725997489889636, 52.64173385682948236),
        QgsPointXY(4.70635793604164299, 52.64214387449186461),
    ]
    polygon = QgsGeometry.fromPolygonXY([polygon_points])
    if not POINTS_IN_WGS84:
        tr = QgsCoordinateTransform(
            QgsCoordinateReferenceSystem(
                28992, QgsCoordinateReferenceSystem.PostgisCrsId
            ),
            QgsCoordinateReferenceSystem(
                4326, QgsCoordinateReferenceSystem.PostgisCrsId
            ),
            QgsProject.instance(),
        )
        polygon.transform(tr)
    assert polygon.isGeosValid(), "polygon is GeoInvalid. WaterBalance tests will fail"
    return polygon


@pytest.fixture()
def ts_datasources():
    ts_datasources = TimeseriesDatasourceModel()
    ts_datasources.spatialite_filepath = MODEL_SQLITE_PATH
    items = [
        {
            "type": "netcdf-groundwater",
            "name": "results_3di",
            "file_path": str(TESTMODEL_DIR / "results_3di.nc"),
        }
    ]
    ts_datasources.insertRows(items)
    return ts_datasources


@pytest.fixture()
def wb_calculation(ts_datasources):
    ensure_qgis_app_is_initialized()
    wb_calculation = WaterBalanceCalculation(ts_datasources)
    return wb_calculation


def test_waterbalance_calc_instance(wb_calculation):
    assert isinstance(wb_calculation, WaterBalanceCalculation)


@mock.patch("ThreeDiToolbox.tool_result_selection.models.StatusProgressBar")
def test_get_incoming_and_outcoming_link_ids(
    progress_bar_mock, wb_calculation, wb_polygon
):
    """We mock StatusProgressBar which is not refered from
    'utils.user_messages.StatusProgressBar', but from
    .tool_result_selection.models.StatusProgressBar' """
    links = wb_calculation.get_incoming_and_outcoming_link_ids(wb_polygon, None)
    assert links == LINKS_EXPECTED


@mock.patch("ThreeDiToolbox.tool_result_selection.models.StatusProgressBar")
def test_get_nodes(progress_bar_mock, wb_calculation, wb_polygon):
    nodes = wb_calculation.get_nodes(wb_polygon, None)
    assert nodes == NODES_EXPECTED


@mock.patch("ThreeDiToolbox.tool_result_selection.models.StatusProgressBar")
def test_time_steps_get_aggregated_flows(progress_bar_mock, wb_calculation):
    """test A) number of timesteps, B) wheter we get a time series for each link,
     pump and node"""
    link_ids = LINKS_EXPECTED[0]
    pump_ids = LINKS_EXPECTED[1]
    node_ids = NODES_EXPECTED
    aggregated_flows = wb_calculation.get_aggregated_flows(
        link_ids, pump_ids, node_ids, None
    )
    assert len(aggregated_flows) == 2
    time_steps = aggregated_flows[0]
    total_time = aggregated_flows[1]

    assert (
        helper_round_numpy(time_steps) == helper_round_numpy(TIMESTEPS_EXPECTED)
    ).all(), (
        "aggregation timesteps array is not what we expected (even when "
        "we round numbers)"
    )
    assert (
        len(time_steps) == total_time.shape[0]
    ), "Number of time_steps is not equal to number of values in time_series"

    assert len(INPUT_SERIES) == total_time.shape[1], (
        "For all INPUT_SERIES elements " "a time series should be calculated"
    )


@mock.patch("ThreeDiToolbox.tool_result_selection.models.StatusProgressBar")
def test_get_aggregated_flows_2d_and_1d(progress_bar_mock, wb_calculation):
    link_ids = LINKS_EXPECTED[0]
    pump_ids = LINKS_EXPECTED[1]
    node_ids = NODES_EXPECTED
    # empty values of dicts 'pumps' and 'nodes', but keep their keys so
    # that less aggregated flows have to be calculated
    pump_ids = pump_ids.fromkeys(pump_ids, [])
    node_ids = node_ids.fromkeys(node_ids, [])
    aggregated_flows = wb_calculation.get_aggregated_flows(
        link_ids, pump_ids, node_ids, None
    )

    EXPECTED_CUMM_2D_IN = 719.93930714
    ID = helper_get_input_series_id("2d_in")
    cumm_flow = helper_calculate_agg_flow(aggregated_flows, ID)
    assert helper_round_numpy(cumm_flow) == helper_round_numpy(EXPECTED_CUMM_2D_IN)

    EXPECTED_CUMM_2D_OUT = -12690.85412108924
    ID = helper_get_input_series_id("2d_out")
    cumm_flow = helper_calculate_agg_flow(aggregated_flows, ID)
    assert helper_round_numpy(cumm_flow) == helper_round_numpy(EXPECTED_CUMM_2D_OUT)

    EXPECTED_CUMM_1D_IN = 7.1771299119876979e-09
    ID = helper_get_input_series_id("1d_in")
    cumm_flow = helper_calculate_agg_flow(aggregated_flows, ID)
    assert helper_round_numpy(cumm_flow) == helper_round_numpy(EXPECTED_CUMM_1D_IN)

    EXPECTED_CUMM_1D_OUT = -2832.9581887459126
    ID = helper_get_input_series_id("1d_out")
    cumm_flow = helper_calculate_agg_flow(aggregated_flows, ID)
    assert helper_round_numpy(cumm_flow) == helper_round_numpy(EXPECTED_CUMM_1D_OUT)


@pytest.fixture()
@mock.patch(
    "ThreeDiToolbox.tool_water_balance.views.waterbalance_widget.PolygonDrawTool"
)
def wb_widget(mock_it, ts_datasources, wb_calculation):
    ensure_qgis_app_is_initialized()
    iface = mock.Mock()
    waterbalance_widget = WaterBalanceWidget(
        iface=iface, ts_datasources=ts_datasources, wb_calc=wb_calculation
    )
    return waterbalance_widget


def test_waterbalance_widget_instance(wb_widget):
    assert isinstance(wb_widget, WaterBalanceWidget)
    print("kak")


def test_wb_widget_get_io_series_net(wb_widget):
    io_series_net = wb_widget._get_io_series_net()
    expected = [
        {
            "label_name": "2D flow to 1D (all domains)",
            "in": ["1d__1d_2d_flow_in", "2d__1d_2d_flow_in"],
            "out": ["1d__1d_2d_flow_out", "2d__1d_2d_flow_out"],
            "type": "NETVOL",
        },
        {
            "label_name": "leakage",
            "in": ["leak"],
            "out": ["leak"],
            "type": "2d_groundwater",
        },
        {
            "label_name": "constant infiltration",
            "in": ["infiltration_rate_simple"],
            "out": ["infiltration_rate_simple"],
            "type": "2d",
        },
        {"label_name": "2D flow", "in": ["2d_in"], "out": ["2d_out"], "type": "2d"},
        {"label_name": "1D flow", "in": ["1d_in"], "out": ["1d_out"], "type": "1d"},
        {
            "label_name": "groundwater flow",
            "in": ["2d_groundwater_in"],
            "out": ["2d_groundwater_out"],
            "type": "2d_groundwater",
        },
        {
            "label_name": "lateral flow to 2D",
            "in": ["lat_2d"],
            "out": ["lat_2d"],
            "type": "2d",
        },
        {
            "label_name": "lateral flow to 1D",
            "in": ["lat_1d"],
            "out": ["lat_1d"],
            "type": "1d",
        },
        {
            "label_name": "2D boundary flow",
            "in": ["2d_bound_in"],
            "out": ["2d_bound_out"],
            "type": "2d",
        },
        {
            "label_name": "1D boundary flow",
            "in": ["1d_bound_in"],
            "out": ["1d_bound_out"],
            "type": "1d",
        },
        {
            "label_name": "0D rainfall runoff on 1D",
            "in": ["inflow"],
            "out": ["inflow"],
            "type": "1d",
        },
        {
            "label_name": "change in storage",
            "in": ["d_2d_vol", "d_2d_groundwater_vol", "d_1d_vol"],
            "out": ["d_2d_vol", "d_2d_groundwater_vol", "d_1d_vol"],
            "type": "NETVOL",
        },
        {"label_name": "pump", "in": ["pump_in"], "out": ["pump_out"], "type": "1d"},
        {"label_name": "rain on 2D", "in": ["rain"], "out": ["rain"], "type": "2d"},
        {
            "label_name": "interception",
            "in": ["intercepted_volume"],
            "out": ["intercepted_volume"],
            "type": "2d",
        },
        {
            "label_name": "surface sources and sinks",
            "in": ["q_sss"],
            "out": ["q_sss"],
            "type": "2d",
        },
    ]
    assert io_series_net == expected


def test_barmanger_2d_groundwater(wb_widget):
    io_series_2d_groundwater = wb_widget._get_io_series_2d_groundwater()
    bm_2d_groundwater = BarManager(io_series_2d_groundwater)
    assert isinstance(bm_2d_groundwater, BarManager)
    expected_labels = [
        "groundwater flow",
        "in/exfiltration (domain exchange)",
        "leakage",
        "net change in storage",
    ]
    assert bm_2d_groundwater.xlabels == expected_labels


@pytest.fixture()
@mock.patch("ThreeDiToolbox.tool_result_selection.models.StatusProgressBar")
def waterbalance_widget_timeseries(progress_bar_mock, wb_widget, wb_polygon):
    # always use domain '1d and 2d' to get all flows in the barchart
    wb_widget.wb_polygon = wb_polygon
    wb_barchart_modelpart = "1d and 2d"
    timesteps, ts_series = wb_widget.calc_wb_barchart(wb_barchart_modelpart)
    return timesteps, ts_series


def test_waterbalance_widget_timesteps(waterbalance_widget_timeseries):
    """It looks like that we tested this before (in
    test_time_steps_get_aggregated_flows), but those timesteps were
    retrieved from the WaterBalanceCalculation. These are retrieved from
    WaterBalanceWidget (they must be the same)"""
    timesteps, ts_series = waterbalance_widget_timeseries
    assert (
        helper_round_numpy(timesteps) == helper_round_numpy(TIMESTEPS_EXPECTED)
    ).all()


def helper_get_flows_and_dvol(domain=None):
    STORAGE_CHANGE_LABELS = ["net change in storage", "change in storage"]
    sum_inflow = 0
    sum_outflow = 0
    d_vol = 0
    for idx, label in enumerate(domain.xlabels):
        inflow = domain.end_balance_in[idx]
        outflow = domain.end_balance_out[idx]
        if label in STORAGE_CHANGE_LABELS:
            d_vol += inflow + outflow
        else:
            sum_inflow += inflow
            sum_outflow += outflow
    return sum_inflow, sum_outflow, d_vol


@mock.patch("ThreeDiToolbox.tool_result_selection.models.StatusProgressBar")
def test_waterbalance_closure(
    progress_bar_mock, wb_widget, wb_polygon, waterbalance_widget_timeseries
):
    """the netto inflows and outflows of the three sub-domains (1d, 2d,
    2d_groundwater) must equal the netto inflow and outflow"""
    timesteps, time_series = waterbalance_widget_timeseries
    t1 = min(timesteps)
    t2 = max(timesteps)

    wb_widget.wb_polygon = wb_polygon
    # always use domain '1d and 2d' to get all flows in the barchart
    wb_barchart_modelpart = "1d and 2d"
    timesteps, ts_series = wb_widget.calc_wb_barchart(wb_barchart_modelpart)

    io_series_net = wb_widget._get_io_series_net()
    io_series_2d = wb_widget._get_io_series_2d()
    io_series_2d_groundwater = wb_widget._get_io_series_2d_groundwater()
    io_series_1d = wb_widget._get_io_series_1d()

    bm_net = BarManager(io_series_net)
    bm_2d = BarManager(io_series_2d)
    bm_2d_groundwater = BarManager(io_series_2d_groundwater)
    bm_1d = BarManager(io_series_1d)

    # netto domain
    bm_net.calc_balance(timesteps, time_series, t1, t2, net=True)
    sum_inflow, sum_outflow, d_vol_net = helper_get_flows_and_dvol(domain=bm_net)
    assert helper_round_numpy(d_vol_net) == helper_round_numpy(
        sum([sum_inflow, sum_outflow])
    )

    # 1d domain
    bm_1d.calc_balance(timesteps, time_series, t1, t2)
    sum_inflow, sum_outflow, d_vol_1d = helper_get_flows_and_dvol(domain=bm_1d)
    assert helper_round_numpy(d_vol_1d) == helper_round_numpy(
        sum([sum_inflow, sum_outflow])
    )

    # 2d domain
    bm_2d.calc_balance(timesteps, time_series, t1, t2)
    sum_inflow, sum_outflow, d_vol_2d = helper_get_flows_and_dvol(domain=bm_2d)
    assert helper_round_numpy(d_vol_2d) == helper_round_numpy(
        sum([sum_inflow, sum_outflow])
    )

    # 2d_groundwater domain
    bm_2d_groundwater.calc_balance(
        timesteps, time_series, t1, t2, invert=["in/exfiltration (domain exchange)"]
    )
    sum_inflow, sum_outflow, d_vol_2d_gr = helper_get_flows_and_dvol(
        domain=bm_2d_groundwater
    )
    assert helper_round_numpy(d_vol_2d_gr) == helper_round_numpy(
        sum([sum_inflow, sum_outflow])
    )

    # the sum of volume changes in the 3 sub-domains must equal volume change
    # of the netto domain
    assert helper_round_numpy(
        sum([d_vol_1d, d_vol_2d, d_vol_2d_gr])
    ) == helper_round_numpy(d_vol_net)
