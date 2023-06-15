from .threedi_result_aggregation.base import Aggregation
from .threedi_result_aggregation.constants import AGGREGATION_VARIABLES, AGGREGATION_METHODS
from .style import (
    Style,
    STYLE_SINGLE_COLUMN_GRADUATED_NODE,
    STYLE_SINGLE_COLUMN_GRADUATED_CELL,
    STYLE_CHANGE_WL,
    STYLE_VECTOR,
    STYLE_TIMESTEP_REDUCTION_ANALYSIS,
    STYLE_BALANCE,
)


class Preset:
    def __init__(
        self,
        name: str,
        description: str = "",
        aggregations=None,
        resample_point_layer: bool = False,
        flowlines_style: Style = None,
        cells_style: Style = None,
        nodes_style: Style = None,
        flowlines_style_param_values: dict = None,
        cells_style_param_values: dict = None,
        nodes_style_param_values: dict = None,
    ):
        if aggregations is None:
            aggregations = list()
        self.name = name
        self.description = description
        self.__aggregations = aggregations
        self.resample_point_layer = resample_point_layer
        self.flowlines_style = flowlines_style
        self.cells_style = cells_style
        self.nodes_style = nodes_style
        self.flowlines_style_param_values = flowlines_style_param_values  # style_param_values can also contain layer names
        self.cells_style_param_values = cells_style_param_values
        self.nodes_style_param_values = nodes_style_param_values

    def add_aggregation(self, aggregation: Aggregation):
        self.__aggregations.append(aggregation)

    def aggregations(self):
        return self.__aggregations


# No preset selected
NO_PRESET = Preset(name="(no preset selected)", aggregations=[])

# Maximum water level
max_wl_aggregations = [
    Aggregation(
        variable=AGGREGATION_VARIABLES.get_by_short_name("s1"),
        method=AGGREGATION_METHODS.get_by_short_name("max"),
    )
]

MAX_WL_PRESETS = Preset(
    name="Maximum water level",
    description="Calculates the maximum water level for nodes and cells within the chosen "
    "time filter.",
    aggregations=max_wl_aggregations,
    nodes_style=STYLE_SINGLE_COLUMN_GRADUATED_NODE,
    cells_style=STYLE_SINGLE_COLUMN_GRADUATED_CELL,
    nodes_style_param_values={"column": "s1_max", "layer_name": "maximum_water_level_node"},
    cells_style_param_values={"column": "s1_max", "layer_name": "maximum_water_level_cell"},
)

# Change in water level
change_wl_aggregations = [
    Aggregation(
        variable=AGGREGATION_VARIABLES.get_by_short_name("s1"),
        method=AGGREGATION_METHODS.get_by_short_name("first"),
    ),
    Aggregation(
        variable=AGGREGATION_VARIABLES.get_by_short_name("s1"),
        method=AGGREGATION_METHODS.get_by_short_name("last"),
    ),
    Aggregation(
        variable=AGGREGATION_VARIABLES.get_by_short_name("s1"),
        method=AGGREGATION_METHODS.get_by_short_name("min"),
    ),
    Aggregation(
        variable=AGGREGATION_VARIABLES.get_by_short_name("s1"),
        method=AGGREGATION_METHODS.get_by_short_name("max"),
    ),
]

CHANGE_WL_PRESETS = Preset(
    name="Change in water level",
    description="Calculates the difference in water level (last - first). In the styling "
    "NULL values (when the cell is dry) are replaced by the cells lowest "
    "pixel elevation (z_coordinate).",
    aggregations=change_wl_aggregations,
    cells_style=STYLE_CHANGE_WL,
    cells_style_param_values={"first": "s1_first", "last": "s1_last", "layer_name": "change_in_water_level_cell"},
)

# Flow pattern
flow_pattern_aggregations = [
    Aggregation(
        variable=AGGREGATION_VARIABLES.get_by_short_name("q_out_x"),
        method=AGGREGATION_METHODS.get_by_short_name("sum"),
    ),
    Aggregation(
        variable=AGGREGATION_VARIABLES.get_by_short_name("q_out_y"),
        method=AGGREGATION_METHODS.get_by_short_name("sum"),
    ),
]

FLOW_PATTERN_PRESETS = Preset(
    name="Flow pattern",
    description="Generates a flow pattern map. The aggregation calculates total outflow per "
    "node in x and y directions, resampled to grid_space. In the styling that is "
    "applied, the shade of blue and the rotation of the arrows are based on the "
    "resultant of these two.\n\n"
    "To save the output to disk, save to GeoPackage (Export > Save features as),"
    "copy the styling to the new layer (Styles > Copy Style / Paste Style). Then "
    "save the styling as default in the GeoPackage (Properties > Style > Save as "
    "Default > Save default style to Datasource Database). ",
    aggregations=flow_pattern_aggregations,
    resample_point_layer=True,
    nodes_style=STYLE_VECTOR,
    nodes_style_param_values={"x": "q_out_x_sum", "y": "q_out_y_sum", "layer_name": "flow_pattern_node"},
)

# Timestep reduction analysis
ts_reduction_analysis_aggregations = [
    Aggregation(
        variable=AGGREGATION_VARIABLES.get_by_short_name("ts_max"),
        method=AGGREGATION_METHODS.get_by_short_name("below_thres"),
        threshold=1.0,
    ),
    Aggregation(
        variable=AGGREGATION_VARIABLES.get_by_short_name("ts_max"),
        method=AGGREGATION_METHODS.get_by_short_name("below_thres"),
        threshold=3.0,
    ),
    Aggregation(
        variable=AGGREGATION_VARIABLES.get_by_short_name("ts_max"),
        method=AGGREGATION_METHODS.get_by_short_name("below_thres"),
        threshold=5.0,
    ),
]
TS_REDUCTION_ANALYSIS_PRESETS = Preset(
    name="Timestep reduction analysis",
    description="Timestep reduction analysis calculates the % of time that the flow "
    "through each flowline limits the calculation timestep to below 1, "
    "3, "
    "or 5 seconds. \n\n"
    "The styling highlights the flowlines that have a timestep of \n"
    "    < 1 s for 10% of the time and/or\n"
    "    < 3 s for 50% of the time and/or\n"
    "    < 5 s for 80% of the time;"
    "\n\n"
    "Replacing these flowlines with orifices may speed up the "
    "simulation "
    "without large impact on the results. Import the highlighted lines "
    "from the aggregation result into your 3Di spatialite as "
    "'ts_reducers' and use this query to replace line elements ("
    "example "
    "for v2_pipe):\n\n"
    "-- Add orifice:\n"
    "INSERT INTO v2_orifice(display_name, code, crest_level, sewerage, "
    "cross_section_definition_id, friction_value, friction_type, "
    "discharge_coefficient_positive, discharge_coefficient_negative, "
    "zoom_category, crest_type, connection_node_start_id, "
    "connection_node_end_id)\n"
    "SELECT display_name, code, max(invert_level_start_point, "
    "invert_level_end_point) AS crest_level, TRUE AS sewerage, "
    "cross_section_definition_id, friction_value, friction_type, "
    "1 AS discharge_coefficient_positive, "
    "1 AS discharge_coefficient_negative, zoom_category, "
    "4 AS crest_type, "
    "connection_node_start_id, connection_node_end_id\n"
    "FROM v2_pipe\n"
    "WHERE id IN (SELECT spatialite_id FROM ts_reducers WHERE "
    "content_type='v2_pipe');\n\n"
    "-- Remove pipe\n"
    "DELETE FROM v2_pipe WHERE id IN (SELECT spatialite_id FROM "
    "ts_reducers WHERE content_type='v2_pipe');",
    aggregations=ts_reduction_analysis_aggregations,
    flowlines_style=STYLE_TIMESTEP_REDUCTION_ANALYSIS,
    flowlines_style_param_values={
        "col1": "ts_max_below_thres_1_0",
        "col2": "ts_max_below_thres_3_0",
        "col3": "ts_max_below_thres_5_0",
        "layer_name": "timestep_reduction_analysis_flow",
    },
)

# Source or sink (mm)
source_sink_mm_aggregations = [
    Aggregation(
        variable=AGGREGATION_VARIABLES.get_by_short_name("rain_depth"),
        method=AGGREGATION_METHODS.get_by_short_name("sum"),
    ),
    Aggregation(
        variable=AGGREGATION_VARIABLES.get_by_short_name(
            "infiltration_rate_simple_mm"
        ),
        method=AGGREGATION_METHODS.get_by_short_name("sum"),
    ),
    Aggregation(
        variable=AGGREGATION_VARIABLES.get_by_short_name(
            "intercepted_volume_mm"
        ),
        method=AGGREGATION_METHODS.get_by_short_name("last"),
    ),
]
SOURCE_SINK_MM_PRESETS = Preset(
    name="Source or sink (mm)",
    description="Calculate by how many mm a node or cell is a net source or sink."
    "A positive results indicates a source, negative result a sink.",
    aggregations=source_sink_mm_aggregations,
    cells_style=STYLE_BALANCE,
    cells_style_param_values={
        "positive_col1": "rain_depth_sum",
        "positive_col2": "",
        "positive_col3": "",
        "negative_col1": "infiltration_rate_simple_mm_sum",
        "negative_col2": "intercepted_volume_mm_last",
        "negative_col3": "",
        "layer_name": "source_or_sink_cell",
    },
)

PRESETS = [
    NO_PRESET,
    MAX_WL_PRESETS,
    CHANGE_WL_PRESETS,
    SOURCE_SINK_MM_PRESETS,
    FLOW_PATTERN_PRESETS,
    TS_REDUCTION_ANALYSIS_PRESETS,
]
