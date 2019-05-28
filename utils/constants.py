# connection node constants
NODE_CALC_TYPE_BOUNDARY = -1
NODE_CALC_TYPE_ISOLATED = 1
NODE_CALC_TYPE_CONNECTED = 2
NODE_CALC_TYPE_EMBEDDED = 0
NODE_CALC_TYPE_BROAD_CRESTED = 3
NODE_CALC_TYPE_SHORT_CRESTED = 4
NODE_CALC_TYPE_DOUBLE_CONNECTED = 5

CALC_TYPE_RANKING = (
    NODE_CALC_TYPE_BOUNDARY,  # -1
    NODE_CALC_TYPE_EMBEDDED,  # 0
    NODE_CALC_TYPE_ISOLATED,  # 1
    NODE_CALC_TYPE_DOUBLE_CONNECTED,  # 5
    NODE_CALC_TYPE_CONNECTED,  # 2
    NODE_CALC_TYPE_BROAD_CRESTED,  # 3
    NODE_CALC_TYPE_SHORT_CRESTED,  # 4
)

# different range is used to reflect
# that objects have their own geometry,
# e.g. channels and culverts
CALC_TYPE_MAP = {
    101: NODE_CALC_TYPE_ISOLATED,
    105: NODE_CALC_TYPE_DOUBLE_CONNECTED,
    102: NODE_CALC_TYPE_CONNECTED,
    100: NODE_CALC_TYPE_EMBEDDED,
}

CONNECTED_PNTS_THRESHOLD = {
    NODE_CALC_TYPE_BOUNDARY: 0,
    NODE_CALC_TYPE_ISOLATED: 0,
    NODE_CALC_TYPE_EMBEDDED: 0,
    NODE_CALC_TYPE_CONNECTED: 1,
    NODE_CALC_TYPE_DOUBLE_CONNECTED: 2,
}

DEGREE_IN_METERS = 111325.0

TABLE_NAME_CALC_PNT = "v2_calculation_point"
TABLE_NAME_CONN_PNT = "v2_connected_pnt"
TABLE_NAME_LEVEE = "v2_levee"

EPSG_WGS84 = 4326
EPSG_RD_NEW = 28992

# A dictionary to link tables names to the table views names
DICT_TABLE_NAMES = {
    "culvert": "v2_culvert",
    "orifice": "v2_orifice",
    "pumpstation": "v2_pumpstation",
    "weir": "v2_weir",
}
# A dictionary to link tables names to the id names
DICT_TABLE_ID = {
    "culvert": "cul_id",
    "orifice": "orf_id",
    "pumpstation": "pump_id",
    "weir": "weir_id",
}
# A dictionary to link the table view names to the action types
DICT_ACTION_TYPES = {
    "culvert": ["set_discharge_coefficient"],
    "orifice": ["set_crest_level", "set_discharge_coefficient"],
    "pumpstation": ["set_capacity"],
    "weir": ["set_crest_level", "set_discharge_coefficient"],
}
