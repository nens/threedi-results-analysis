# core
import numpy as np

# custom
from osgeo import ogr
from threedigrid.admin.utils import KCUDescriptor

# local
from .aggregation_classes import (
    AggregationVariableList,
    AggregationSign,
    AggregationMethod,
    AggregationVariable,
    VR_INTERFLOW,
    VR_SIMPLE_INFILTRATION,
    VR_INTERCEPTION,
    VR_PUMP,
    VT_NODE,
    VT_NODE_HYBRID,
    VT_FLOW,
    VT_FLOW_HYBRID,
    VT_PUMP,
    PRM_NONE,
    PRM_SPLIT,
    PRM_1D,
)

KCU_DICT = KCUDescriptor()
NODE_TYPE_DICT = {
    1: "2D surface water",
    2: "2D groundwater",
    3: "1D without storage",
    4: "1D with storage",
    5: "2D surface water boundary",
    6: "2D groundwater boundary",
    7: "1D boundary",
}

# Python to Ogr data type conversions
NP_OGR_DTYPES = {
    np.dtype("float32"): ogr.OFTReal,
    np.dtype("float64"): ogr.OFTReal,
    np.dtype("int32"): ogr.OFTInteger,
    np.dtype("int64"): ogr.OFTInteger64,
}

# Magic threshold attribute for nodes.
# Nodes do not have this attribute, but will be derived from flowlines connected to the node
EXCHANGE_LEVEL_1D2D = "exchange_level_1d2d"

# Number of decimals to round values to before comparing them in below/at/above threshold methods
THRESHOLD_PRECISION = 1e-6  # If variable is in m3, this is 0.001 L


# Aggregation methods
AGGREGATION_METHODS = AggregationVariableList()

agg_method_list = [
    {"short_name": "sum", "long_name": "Sum", "integrates_over_time": True},
    {"short_name": "max", "long_name": "Max"},
    {"short_name": "max_time", "long_name": "Time to max"},
    {"short_name": "min", "long_name": "Min"},
    {"short_name": "mean", "long_name": "Mean"},
    {"short_name": "median", "long_name": "Median"},
    {"short_name": "first", "long_name": "First"},
    {"short_name": "first_non_empty", "long_name": "First non-empty"},
    {"short_name": "last", "long_name": "Last"},
    {"short_name": "last_non_empty", "long_name": "Last non-empty"},
    {
        "short_name": "time_below_threshold",
        "long_name": "Time below threshold",
        "has_threshold": True,
        "is_duration": True,
    },
    {
        "short_name": "time_on_threshold",
        "long_name": "Time on threshold",
        "has_threshold": True,
        "is_duration": True,
    },
    {
        "short_name": "time_above_threshold",
        "long_name": "Time above threshold",
        "has_threshold": True,
        "is_duration": True,
    },
    {
        "short_name": "below_thres",
        "long_name": "% of time below threshold",
        "has_threshold": True,
        "is_percentage": True,
    },
    {
        "short_name": "on_thres",
        "long_name": "% of time on threshold",
        "has_threshold": True,
        "is_percentage": True,
    },
    {
        "short_name": "above_thres",
        "long_name": "% of time above threshold",
        "has_threshold": True,
        "is_percentage": True,
    },
]

for var in agg_method_list:
    AGGREGATION_METHODS.append(AggregationMethod(**var))

ALL_AGG_METHODS = list(AGGREGATION_METHODS.short_names())
ALL_AGG_METHODS_NO_SUM = list(AGGREGATION_METHODS.short_names())
ALL_AGG_METHODS_NO_SUM.remove("sum")

# Aggregation variables
agg_var_list = [
    # Flowline variables
    {
        "short_name": "q",
        "long_name": "Discharge",
        "signed": True,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_FLOW,
        "units": {("m3", "s"): (1, 1)},
        "can_resample": False,
        "pre_resample_method": PRM_NONE,
    },
    {
        "short_name": "u1",
        "long_name": "Velocity",
        "signed": True,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_FLOW,
        "units": {("m", "s"): (1, 1)},
        "can_resample": False,
        "pre_resample_method": PRM_NONE,
    },
    {
        "short_name": "au",
        "long_name": "Wet crosssectional area",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_FLOW,
        "units": {("m2",): (1,)},
        "can_resample": False,
        "pre_resample_method": PRM_NONE,
    },
    {
        "short_name": "qp",
        "long_name": "Discharge in interflow layer",
        "signed": True,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_FLOW,
        "units": {("m3", "s"): (1, 1)},
        "can_resample": False,
        "pre_resample_method": PRM_NONE,
        "requirements": [VR_INTERFLOW],
    },
    {
        "short_name": "up1",
        "long_name": "Velocity in interflow layer",
        "signed": True,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_FLOW,
        "units": {("m", "s"): (1, 1)},
        "can_resample": False,
        "pre_resample_method": PRM_NONE,
        "requirements": [VR_INTERFLOW],
    },
    {
        "short_name": "ts_max",
        "long_name": "Max. possible timestep",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_FLOW,
        "units": {"s": (1,)},
        "can_resample": False,
        "pre_resample_method": PRM_NONE,
    },
    {
        "short_name": "grad",
        "long_name": "Water level gradient",
        "signed": True,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_FLOW_HYBRID,
        "units": {("m",): (1,)},
        "can_resample": False,
        "pre_resample_method": PRM_NONE,
    },
    {
        "short_name": "bed_grad",
        "long_name": "Bed level gradient",
        "signed": False,
        "applicable_methods": [],
        "var_type": VT_FLOW_HYBRID,
        "units": {("m",): (1,)},
        "can_resample": False,
        "pre_resample_method": PRM_NONE,
    },
    {
        "short_name": "wl_at_xsec",
        "long_name": "Water level at cross section",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_FLOW_HYBRID,
        "units": {("m",): (1,)},
        "can_resample": False,
        "pre_resample_method": PRM_NONE,
    },
    # Pump variables
    {
        'short_name': 'q_pump',
        'long_name': 'Pump discharge',
        'signed': False,
        'applicable_methods': ALL_AGG_METHODS,
        'var_type': VT_PUMP,
        'units': {('m3', 's'): (1, 1), ('m3', 'h'): (1, 3600), ('L', 's'): (1000, 1)},
        'can_resample': False,
        'pre_resample_method': PRM_NONE,
        "requirements": [VR_PUMP]
    },
    # Node variables
    {
        "short_name": "s1",
        "long_name": "Water level",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_NODE,
        "units": {("m.a.s.l.",): (1,)},
        "can_resample": True,
        "pre_resample_method": PRM_NONE,
    },
    {
        "short_name": "vol",
        "long_name": "Volume",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_NODE,
        "units": {("m3",): (1,)},
        "can_resample": True,
        "pre_resample_method": PRM_SPLIT,
    },
    {
        "short_name": "rain",
        "long_name": "Rain intensity",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE,
        "units": {("m3", "s"): (1, 1), ("m3", "h"): (1, 3600)},
        "can_resample": True,
        "pre_resample_method": PRM_SPLIT,
    },
    {
        "short_name": "rain_depth",
        "long_name": "Rain depth",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE,
        "units": {("mm", "s"): (1000, 1), ("mm", "h"): (1000, 3600)},
        "can_resample": True,
        "pre_resample_method": PRM_NONE,
    },
    {
        "short_name": "infiltration_rate_simple",
        "long_name": "Infiltration rate",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE,
        "units": {("m3", "s"): (1, 1), ("m3", "h"): (1, 3600)},
        "can_resample": True,
        "pre_resample_method": PRM_NONE,
        "requirements": [VR_SIMPLE_INFILTRATION],
    },
    {
        "short_name": "infiltration_rate_simple_mm",
        "long_name": "Infiltration rate per m2",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE,
        "units": {("mm", "s"): (1000, 1), ("mm", "h"): (1000, 3600)},
        "can_resample": True,
        "pre_resample_method": PRM_NONE,
        "requirements": [VR_SIMPLE_INFILTRATION],
    },
    {
        "short_name": "su",
        "long_name": "Wet surface area",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_NODE,
        "units": {("m2",): (1,)},
        "can_resample": False,
        "pre_resample_method": PRM_NONE,
    },
    {
        "short_name": "uc",
        "long_name": "Flow velocity at cell center",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_NODE,
        "units": {("m", "s"): (1, 1)},
        "can_resample": True,
        "pre_resample_method": PRM_NONE,
    },
    {
        "short_name": "ucx",
        "long_name": "Flow velocity in x direction at cell center",
        "signed": True,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_NODE,
        "units": {("m", "s"): (1, 1)},
        "can_resample": True,
        "pre_resample_method": PRM_NONE,
    },
    {
        "short_name": "ucy",
        "long_name": "Flow velocity in y direction at cell center",
        "signed": True,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_NODE,
        "units": {("m", "s"): (1, 1)},
        "can_resample": True,
        "pre_resample_method": PRM_NONE,
    },
    # 'Leakage' ???
    {
        "short_name": "q_lat",
        "long_name": "Lateral discharge",
        "signed": True,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE,
        "units": {("m3", "s"): (1, 1)},
        "can_resample": True,
        "pre_resample_method": PRM_SPLIT,
    },
    {
        "short_name": "q_lat_mm",
        "long_name": "Lateral discharge per m2",
        "signed": True,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE,
        "units": {("mm", "s"): (1000, 1), ("mm", "h"): (1000, 3600)},
        "can_resample": True,
        "pre_resample_method": PRM_NONE,
    },
    {
        "short_name": "intercepted_volume",
        "long_name": "Intercepted volume",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_NODE,
        "units": {("m3",): (1,)},
        "can_resample": True,
        "pre_resample_method": PRM_SPLIT,
        "requirements": [VR_INTERCEPTION],
    },
    {
        "short_name": "intercepted_volume_mm",
        "long_name": "Intercepted volume per m2",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS_NO_SUM,
        "var_type": VT_NODE,
        "units": {("mm",): (1000,)},
        "can_resample": True,
        "pre_resample_method": PRM_NONE,
        "requirements": [VR_INTERCEPTION],
    },
    {
        "short_name": "q_sss",
        "long_name": "Surface sources and sinks discharge",
        "signed": True,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE,
        "units": {("m3", "s"): (1, 1)},
        "can_resample": True,
        "pre_resample_method": PRM_SPLIT,
    },
    {
        "short_name": "q_sss_mm",
        "long_name": "Surface sources and sinks discharge per m2",
        "signed": True,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE,
        "units": {("mm", "s"): (1000, 1), ("mm", "h"): (1000, 3600)},
        "can_resample": True,
        "pre_resample_method": PRM_NONE,
    },
    {
        "short_name": "q_in_x",
        "long_name": "Node inflow in x direction",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE_HYBRID,
        "units": {("m3", "s"): (1, 1)},
        "can_resample": True,
        "pre_resample_method": PRM_1D,
    },
    {
        "short_name": "q_in_x_mm",
        "long_name": "Node inflow in x direction per m2",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE_HYBRID,
        "units": {("mm", "s"): (1000, 1)},
        "can_resample": True,
        "pre_resample_method": PRM_1D,
    },
    {
        "short_name": "q_in_y",
        "long_name": "Node inflow in y direction",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE_HYBRID,
        "units": {("m3", "s"): (1, 1)},
        "can_resample": True,
        "pre_resample_method": PRM_1D,
    },
    {
        "short_name": "q_in_y_mm",
        "long_name": "Node inflow in y direction per m2",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE_HYBRID,
        "units": {("mm", "s"): (1000, 1)},
        "can_resample": True,
        "pre_resample_method": PRM_1D,
    },
    {
        "short_name": "q_out_x",
        "long_name": "Node outflow in x direction",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE_HYBRID,
        "units": {("m3", "s"): (1, 1)},
        "can_resample": True,
        "pre_resample_method": PRM_1D,
    },
    {
        "short_name": "q_out_x_mm",
        "long_name": "Node outflow in x direction per m2",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE_HYBRID,
        "units": {("mm", "s"): (1000, 1)},
        "can_resample": True,
        "pre_resample_method": PRM_1D,
    },
    {
        "short_name": "q_out_y",
        "long_name": "Node outflow in y direction",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE_HYBRID,
        "units": {("m3", "s"): (1, 1)},
        "can_resample": True,
        "pre_resample_method": PRM_1D,
    },
    {
        "short_name": "q_out_y_mm",
        "long_name": "Node outflow in y direction per m2",
        "signed": False,
        "applicable_methods": ALL_AGG_METHODS,
        "var_type": VT_NODE_HYBRID,
        "units": {("mm", "s"): (1000, 1)},
        "can_resample": True,
        "pre_resample_method": PRM_1D,
    },
]

AGGREGATION_VARIABLES = AggregationVariableList()

for var in agg_var_list:
    AGGREGATION_VARIABLES.append(AggregationVariable(**var))

NA_TEXT = "[Not applicable]"
AGGREGATION_SIGN_NA = AggregationSign(short_name="", long_name=NA_TEXT)
AGGREGATION_SIGNS = [
    AggregationSign(short_name="net", long_name="Net"),
    AggregationSign(short_name="pos", long_name="Positive"),
    AggregationSign(short_name="neg", long_name="Negative"),
    AggregationSign(short_name="abs", long_name="Absolute"),
    AGGREGATION_SIGN_NA,
]

NON_TS_REDUCING_KCU = [
    3,
    4,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    150,
    200,
    300,
    400,
    500,
]
