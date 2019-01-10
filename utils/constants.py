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
    "culvert": "v2_culvert",
    "orifice": "v2_orifice",
    "pumpstation": "v2_pumpstation",
    "weir": "v2_weir"
}
# A dictionary to link tables names to the id names
DICT_TABLE_ID = {
    "culvert": "cul_id",
    "orifice": "orf_id",
    "pumpstation": "pump_id",
    "weir": "weir_id"
}
# A dictionary to link the table view names to the action types
DICT_ACTION_TYPES = {
    "culvert": ["set_discharge_coefficient"],
    "orifice": ["set_crest_level", "set_discharge_coefficient"],
    "pumpstation": ["set_capacity"],
    "weir": ["set_crest_level", "set_discharge_coefficient"]
}


v2_tables_list = [
    'v2_1d_boundary_conditions',
    'v2_1d_lateral',
    'v2_2d_boundary_conditions',
    'v2_2d_lateral',
    'v2_aggregation_settings',
    'v2_calculation_point',
    'v2_channel',
    'v2_connected_pnt',
    'v2_connection_nodes',
    'v2_control',
    'v2_control_delta',
    'v2_control_group',
    'v2_control_measure_group',
    'v2_control_measure_map',
    'v2_control_memory',
    'v2_control_pid',
    'v2_control_table',
    'v2_control_timed',
    'v2_cross_section_definition',
    'v2_cross_section_location',
    'v2_cross_section_view',
    'v2_culvert',
    'v2_culvert_view',
    'v2_dem_average_area',
    'v2_global_settings',
    'v2_grid_refinement',
    'v2_grid_refinement_area',
    'v2_groundwater',
    'v2_impervious_surface',
    'v2_impervious_surface_map',
    'v2_interflow',
    'v2_levee',
    'v2_manhole',
    'v2_manhole_view',
    'v2_numerical_settings',
    'v2_obstacle',
    'v2_orifice',
    'v2_pipe',
    'v2_pumpstation',
    'v2_simple_infiltration',
    'v2_surface',
    'v2_surface_map',
    'v2_surface_parameters',
    'v2_weir',
    'v2_windshielding',
]

non_settings_tbl_with_rasters = [
    ['v2_simple_infiltration', 'simple_infiltration_setting_id'],
    ['v2_groundwater', 'groundwater_setting_id'],
    ['v2_interflow', 'interflow_setting_id']
]