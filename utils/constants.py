# connection node constants
NODE_CALC_TYPE_BOUNDARY = -1
NODE_CALC_TYPE_ISOLATED = 1
NODE_CALC_TYPE_CONNECTED = 2
NODE_CALC_TYPE_EMBEDDED = 0
NODE_CALC_TYPE_BROAD_CRESTED = 3
NODE_CALC_TYPE_SHORT_CRESTED = 4
NODE_CALC_TYPE_DOUBLE_CONNECTED = 5

CALC_TYPE_RANKING = (
    NODE_CALC_TYPE_BOUNDARY,          # -1
    NODE_CALC_TYPE_EMBEDDED,          # 0
    NODE_CALC_TYPE_ISOLATED,          # 1
    NODE_CALC_TYPE_DOUBLE_CONNECTED,  # 5
    NODE_CALC_TYPE_CONNECTED,         # 2
    NODE_CALC_TYPE_BROAD_CRESTED,     # 3
    NODE_CALC_TYPE_SHORT_CRESTED      # 4
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
    NODE_CALC_TYPE_DOUBLE_CONNECTED: 2
}

DEGREE_IN_METERS = 111325.0

TABLE_NAME_CALC_PNT = 'v2_calculation_point'
TABLE_NAME_CONN_PNT = 'v2_connected_pnt'
TABLE_NAME_LEVEE = 'v2_levee'

EPSG_WGS84 = 4326
EPSG_RD_NEW = 28992

# A dictionary to link tables names to the table views names
DICT_TABLE_NAMES = {
    "v2_culvert": "v2_culvert_view",
    "v2_orifice": "v2_orifice_view",
    "v2_pumpstation": "v2_pumpstation_view",
    "v2_weir": "v2_weir_view"
}
# A dictionary to link tables names to the id names
DICT_TABLE_ID = {
    "v2_culvert": "cul_id",
    "v2_orifice": "orf_id",
    "v2_pumpstation": "pump_id",
    "v2_weir": "weir_id"
}
# A dictionary to link the table view names to the action types
DICT_ACTION_TYPES = {
    "v2_culvert": "set_discharge_coefficient",
    "v2_orificew": "set_discharge_coefficient",
    "v2_pumpstation": "set_capacity",
    "v2_weir": "set_crest_level"
}
