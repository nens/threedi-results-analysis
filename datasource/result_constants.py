from collections import namedtuple

# NetCDF variable information
NcVar = namedtuple("NcVar", ["name", "verbose_name", "unit"])

WATERLEVEL = NcVar("s1", "waterlevel", "m MSL")
DISCHARGE = NcVar("q", "discharge", "m3/s")
VELOCITY = NcVar("u1", "velocity", "m/s")
VOLUME = NcVar("vol", "volume", "m3")
DISCHARGE_PUMP = NcVar("q_pump", "discharge pump", "m3/s")
DISCHARGE_INTERFLOW = NcVar("qp", "discharge interflow", "m3/s")
DISCHARGE_LATERAL = NcVar("q_lat", "discharge lateral", "m3/s")
VELOCITY_INTERFLOW = NcVar("up1", "velocity interflow", "m/s")
RAIN_INTENSITY = NcVar("rain", "rain intensity", "m3/s")
WET_SURFACE_AREA = NcVar("su", "wet surface area", "m2")
INFILTRATION = NcVar("infiltration_rate", "infiltration rate", "m3/s")
INFILTRATION_RATE_SIMPLE = NcVar("infiltration_rate_simple", "infiltration_rate_simple", "m3/s")
WET_CROSS_SECTION_AREA = NcVar("au", "wet cross section area", "m2")
LEAKAGE_RATE = NcVar("leak", "leakage rate", "m3/s")
INTERCEPTION = NcVar("intercepted_volume", "intercepted volume", "m3")
SOURCES_AND_SINKS = NcVar("q_sss", "sources and sinks", "m3/s")

_Q_TYPES = [
    DISCHARGE,
    DISCHARGE_INTERFLOW,
    DISCHARGE_PUMP,
    VELOCITY,
    VELOCITY_INTERFLOW,
    WET_CROSS_SECTION_AREA,
]
_H_TYPES = [
    WATERLEVEL,
    VOLUME,
    RAIN_INTENSITY,
    WET_SURFACE_AREA,
    INFILTRATION,
    DISCHARGE_LATERAL,
    INFILTRATION_RATE_SIMPLE,
    LEAKAGE_RATE,
    INTERCEPTION,
    SOURCES_AND_SINKS,
]

Q_TYPES = [v.name for v in _Q_TYPES]
H_TYPES = [v.name for v in _H_TYPES]

SUBGRID_MAP_VARIABLES = _Q_TYPES + _H_TYPES  # just take all variables..

AGGREGATION_VARIABLES = [
    DISCHARGE,
    DISCHARGE_INTERFLOW,
    DISCHARGE_PUMP,
    VELOCITY,
    VELOCITY_INTERFLOW,
    WATERLEVEL,
    VOLUME,
    RAIN_INTENSITY,
    WET_SURFACE_AREA,
    INFILTRATION,
    INFILTRATION_RATE_SIMPLE,
    DISCHARGE_LATERAL,
    WET_CROSS_SECTION_AREA,
    LEAKAGE_RATE,
    INTERCEPTION,
    SOURCES_AND_SINKS,
]

AGGREGATION_OPTIONS = {
    "min",
    "max",
    "avg",
    "med",
    "cum",
    "cum_positive",
    "cum_negative",
    "current",
}

layer_information = [
    # layer name, (normalized) object_type, q/h type
    # Note: the reason why this is plural is because this is (inconsistently)
    # also plural in the id mapping json, in contrast to all other object
    # types
    ("v2_connection_nodes", "connection_nodes", "h"),
    ("v2_pipe_view", "pipe", "q"),
    ("v2_channel", "channel", "q"),
    ("v2_culvert_view", "culvert", "q"),
    ("v2_manhole_view", "manhole", "h"),
    ("v2_pumpstation", "pumpstation", "q"),
    ("v2_pumpstation_view", "pumpstation", "q"),
    ("v2_weir_view", "weir", "q"),
    ("v2_orifice_view", "orifice", "q"),
    ("sewerage_manhole", "manhole", "h"),
    ("sewerage_pipe_view", "pipe", "q"),
    ("sewerage_pumpstation", "pumpstation", "q"),
    ("sewerage_pumpstation_view", "pumpstation", "q"),
    ("sewerage_weir_view", "weir", "q"),
    ("sewerage_orifice_view", "orifice", "q"),
    ("flowlines", "flowline", "q"),
    ("nodes", "node", "h"),
    ("pumplines", "pumpline", "q"),
    ("line_results", "flowline", "q"),
    ("node_results", "node", "h"),
]

layer_object_type_mapping = dict([(a[0], a[1]) for a in layer_information])
layer_qh_type_mapping = dict([(a[0], a[2]) for a in layer_information])
