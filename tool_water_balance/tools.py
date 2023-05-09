import logging
from pathlib import Path
from itertools import zip_longest

import numpy as np
import numpy.ma as ma
from qgis.core import QgsFeatureRequest
from qgis.core import QgsProject
from qgis.core import QgsPointXY
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QMessageBox
from threedigrid_builder.constants import LineType
from threedigrid_builder.constants import NodeType

from .config import INPUT_SERIES
from .views.waterbalance_widget import WaterBalanceWidget

NO_ENDPOINT_ID = -9999

LINE_TYPES_1D = {
    LineType.LINE_1D_EMBEDDED,
    LineType.LINE_1D_ISOLATED,
    LineType.LINE_1D_CONNECTED,
    LineType.LINE_1D_LONG_CRESTED,
    LineType.LINE_1D_SHORT_CRESTED,
    LineType.LINE_1D_DOUBLE_CONNECTED,
}
LINE_TYPES_1D2D = {
    LineType.LINE_1D2D_SINGLE_CONNECTED_CLOSED,
    LineType.LINE_1D2D_SINGLE_CONNECTED_OPEN_WATER,
    LineType.LINE_1D2D_DOUBLE_CONNECTED_CLOSED,
    LineType.LINE_1D2D_DOUBLE_CONNECTED_OPEN_WATER,
    LineType.LINE_1D2D_POSSIBLE_BREACH,
    LineType.LINE_1D2D_ACTIVE_BREACH,
    LineType.LINE_1D2D_GROUNDWATER,
    58,  # Also LINE_1D2D_GROUNDWATER?
}
NODE_TYPES_1D = {
    NodeType.NODE_1D_NO_STORAGE,
    NodeType.NODE_1D_STORAGE,
    NodeType.NODE_1D_BOUNDARIES,
}
NODE_TYPES_2D = {
    NodeType.NODE_2D_OPEN_WATER,
    NodeType.NODE_2D_BOUNDARIES,
}
NODE_TYPES_2D_GROUNDWATER = {
    NodeType.NODE_2D_GROUNDWATER_BOUNDARIES,
    NodeType.NODE_2D_GROUNDWATER,
}
NODE_TYPES_BOUNDARIES = {
    NodeType.NODE_1D_BOUNDARIES,
    NodeType.NODE_2D_BOUNDARIES,
}

logger = logging.getLogger(__name__)


def get_missing_agg_vars(threedi_result):
    """Returns a list with tuples of aggregation vars (vol, discharge) +
    methods (cum, current, etc) that are not (but should be) in the
    v2_aggregation_settings

    1.  some vars_methods are always required: minimum_agg_vars
    2.  some vars methods are required when included in the model
        schematisation (e.g. pumps, laterals).
    """
    check_available_vars = threedi_result.available_vars

    ga = threedi_result.gridadmin
    gr = threedi_result.result_admin

    minimum_agg_vars = [
        ("q_cum_negative", "negative cumulative discharge"),
        ("q_cum_positive", "negative cumulative discharge"),
        ("q_cum", "cumulative discharge"),
        ("vol_current", "current volume"),
    ]

    # some vars must be aggregated when included in the model
    # schematisation (e.g. pumps, laterals). problem is that threedigrid
    # does not support e.g. ga.has_lateral, ga.has_leakage etc. For those
    # fields, we read the threedigrid metadata.
    simulated_vars_nodes = ga.nodes._meta.get_fields(only_names=True)

    if gr.has_pumpstations:
        to_add = ("q_pump_cum", "cumulative pump discharge")
        minimum_agg_vars.append(to_add)

    # TODO: wait for threedigrid's e.g. 'gr.has_rained')
    # u'rain' is always in simulated_vars_nodes. So it does not make sense
    # to check there. Thus, we're gonna read the nc's rain data
    if np.nanmax(gr.nodes.rain) > 0:
        to_add = ("rain_cum", "cumulative rain")
        minimum_agg_vars.append(to_add)

    # gr.has_simple_infiltration and gr.has_interception are added to
    # threedigrid some months after groundwater release. To coop with the
    # .h5 that has been created in that period we use the meta data
    try:
        if gr.has_simple_infiltration:
            to_add = (
                "infiltration_rate_simple_cum",
                "cumulative infiltration rate",
            )
            minimum_agg_vars.append(to_add)
    except AttributeError:
        if "infiltration" in simulated_vars_nodes:
            to_add = (
                "infiltration_rate_simple_cum",
                "cumulative infiltration rate",
            )
            minimum_agg_vars.append(to_add)

    try:
        if gr.has_interception:
            to_add = ("intercepted_volume_current", "current interception")
            minimum_agg_vars.append(to_add)
    except AttributeError:
        # gr.has_interception is added to threedigrid some months after
        # groundwater release. To coop with .h5 that has been created in
        # that period we read the simulated_vars_nodes
        if "intercepted_volume" in simulated_vars_nodes:
            to_add = ("intercepted_volume_current", "current interception")
            minimum_agg_vars.append(to_add)

    if "q_lat" in simulated_vars_nodes:
        to_add = ("q_lat_cum", "cumulative lateral discharge")
        minimum_agg_vars.append(to_add)

    if "leak" in simulated_vars_nodes:
        to_add = ("leak_cum", "cumulative leakage")
        minimum_agg_vars.append(to_add)

    if "q_sss" in simulated_vars_nodes:
        if np.count_nonzero(gr.nodes.timeseries(indexes=slice(0, -1)).q_sss) > 0:
            minimum_agg_vars.append(
                ("q_sss_cum", "cumulative surface sources and sinks")
            )

    missing_vars = []
    for required_var in minimum_agg_vars:
        if required_var[0] not in check_available_vars:
            msg = "the aggregation nc misses aggregation: %s", required_var[1]
            logger.error(msg)
            missing_vars.append(required_var[1])
    return missing_vars


def pop_up_no_agg_found():
    header = "Error: No aggregation netcdf found"
    msg = (
        "The WaterBalanceTool requires an 'aggregate_results_3di.nc' "
        "but this file could not be found. Please make sure you run "
        "your simulation using the 'v2_aggregation_settings' table "
        "with the following variables:"
        "\n\ncurrent:"
        "\n- volume"
        "\n- interception (in case model has interception)"
        "\n\ncumulative:"
        "\n- rain"
        "\n- discharge"
        "\n- leakage (in case model has leakage)"
        "\n- laterals (in case model has laterals)"
        "\n- pump discharge (in case model has pumps)"
        "\n- simple_infiltration (in case model has "
        "simple_infiltration)"
        "\n- sources and sinks (in case model has sources and sinks)"
        "\n\npositive cumulative:"
        "\n- discharge"
        "\n\nnegative cumulative:"
        "\n- discharge"
    )
    QMessageBox.warning(None, header, msg)


def pop_up_missing_agg_vars(missing_vars):
    header = "Error: Missing aggregation settings"
    msg = (
        "The WaterBalanceTool found the 'aggregate_results_3di.nc' but "
        "the file does not include all required aggregation "
        "variables. Please add them to the sqlite table "
        "'v2_aggregation_settings' and run your simulation again. The "
        "required variables are:"
        "\n\ncurrent:"
        "\n- volume"
        "\n- interception (in case model has interception)"
        "\n\ncumulative:"
        "\n- rain"
        "\n- discharge"
        "\n- leakage (in case model has leakage)"
        "\n- laterals (in case model has laterals)"
        "\n- pump discharge (in case model has pumps)"
        "\n- simple_infiltration (in case model has "
        "simple_infiltration)"
        "\n- sources and sinks (in case model has sources and sinks)"
        "\n\npositive cumulative:"
        "\n- discharge"
        "\n\nnegative cumulative:"
        "\n- discharge"
        "\n\nYour aggregation .nc misses the following variables:\n"
        + ", ".join(missing_vars)
    )
    QMessageBox.warning(None, header, msg)


def pop_up_not_synchronized_timestamps(a, b):
    header = "Error: timestamps are not synchronized"
    table = "\n".join(zip_longest(a, b))
    msg = "q_cum and vol_current have different timesteps:\n" + table
    QMessageBox.warning(None, header, msg)


class ResultWrapper:
    def __init__(self, result):
        self.result = result

    def _get_layer_by_name(self, layer_name):
        layer_id = self.result.parent().layer_ids[layer_name]
        return QgsProject.instance().mapLayer(layer_id)

    @property
    def lines(self):
        return self._get_layer_by_name('flowline')

    @property
    def points(self):
        return self._get_layer_by_name('node')

    @property
    def pumps(self):
        return None  # TODO

    @property
    def threedi_result(self):
        return self.result.threedi_result

    def has_required_vars(self):
        if self.threedi_result.aggregate_result_admin is None:
            pop_up_no_agg_found()
            return False

        missing_agg_vars = get_missing_agg_vars(self.threedi_result)
        if missing_agg_vars:
            pop_up_missing_agg_vars(missing_agg_vars)
            return False
        return True

    def has_synchronized_timestamps(self):
        threedi_result = self.threedi_result
        t_q_cum = threedi_result.get_timestamps(parameter="q_cum")
        t_vol_c = threedi_result.get_timestamps(parameter="vol_current")
        if not (t_q_cum == t_vol_c).all():
            pop_up_not_synchronized_timestamps(
                t_q_cum.tolist(), t_vol_c.tolist()
            )
            return False
        return True


class WaterBalanceCalculation(object):
    def __init__(self, wrapper, polygon):
        self.wrapper = wrapper
        self.polygon = polygon

        logger.info("polygon of wb area: %s", self.polygon.asWkt())

        ga = self.wrapper.threedi_result.gridadmin

        # total nr of x-dir (horizontal in topview) 2d lines
        nr_2d_x_dir = ga.get_from_meta("liutot")
        # total nr of y-dir (vertical in topview) 2d lines
        nr_2d_y_dir = ga.get_from_meta("livtot")
        # total nr of 2d lines
        nr_2d = ga.get_from_meta("l2dtot")
        # total nr of groundwater lines
        start_gr = ga.get_from_meta("lgrtot")

        # get range of horizontal (in top view) surface water line ids
        x2d_surf_range_min = 1
        x2d_surf_range_max = nr_2d_x_dir
        self.x2d_surf_range = list(
            range(x2d_surf_range_min, x2d_surf_range_max + 1)
        )  # noqa

        # get range of vertical (in top view) surface water line ids
        y2d_surf_range_min = x2d_surf_range_max + 1
        y2d_surf_range_max = x2d_surf_range_max + nr_2d_y_dir
        self.y2d_surf_range = list(range(y2d_surf_range_min, y2d_surf_range_max + 1))

        # get range of vertical (in side view) line ids in the gridadmin.
        # These lines represent surface-groundwater (vertical) flow
        vert_flow_range_min = y2d_surf_range_max + 1
        vert_flow_range_max = y2d_surf_range_max + nr_2d
        self.vert_flow_range = list(range(vert_flow_range_min, vert_flow_range_max + 1))

        if ga.has_groundwater:
            # total nr of x-dir (horizontal in topview) 2d groundwater lines
            x_grndwtr_range_min = start_gr + 1
            x_grndwtr_range_max = start_gr + nr_2d_x_dir
            self.x_grndwtr_range = list(
                range(x_grndwtr_range_min, x_grndwtr_range_max + 1)
            )

            # total nr of y-dir (vertical in topview) 2d groundwater lines
            y_grndwtr_range_min = x_grndwtr_range_max + 1
            y_grndwtr_range_max = x_grndwtr_range_max + nr_2d
            self.y_grndwtr_range = list(
                range(y_grndwtr_range_min, y_grndwtr_range_max + 1)
            )

        # dictionary with link ids by model part
        # TODO note that the _node_ids depended on model_part (1d, 1d and 2d,
        # 2d) so they have to be selected when using these.
        self.flowline_ids, self.pump_ids = self._get_flowline_pump_ids()
        self.node_ids = self._get_node_ids()
        self.time, self.flow = self._get_aggregated_flows()

    def _get_flowline_pump_ids(self):
        """Returns a tuple of dictionaries with ids by category:

        flow_lines = {
            '1d_in': [...],
            '1d_out': [...],
            '1d_bound_in': [...],
            ...
        }

        pump_selection = {
            'in': [...],
            'out': [...],
        }

        returned value = (flow_lines, pump_selection)
        """
        # TODO: implement model_part. One of the problems of not having
        # this implemented is that the on hover map highlight selects all
        # links, even when the 2D or 1D modelpart is selected in the combo box.

        # the '_out' and '_in' indicate the draw direction of the flow_line.
        # a flow line can have in 1 simulation both positive and negative
        # discharge (with extend to the draw direction). Later on, in
        # get_aggregated_flows() this numpy timeserie is clipped with
        # max=0 for flow in 1 direction and min=0 for flow in the opposite
        # direction.
        flow_lines = {
            "1d_in": [],
            "1d_out": [],
            "1d_bound_in": [],
            "1d_bound_out": [],
            "2d_in": [],
            "2d_out": [],
            "2d_bound_in": [],
            "2d_bound_out": [],
            # 1d2d flow lines intersect polygon (1d is inside polygon)
            "1d__1d_2d_flow": [],
            # 1d2d flow lines intersect polygon (2d is inside polygon)
            "2d__1d_2d_flow": [],
            # 1d2d exchange lines are within polygon (both nodes inside)
            "1d_2d_exch": [],
            "2d_groundwater_in": [],
            "2d_groundwater_out": [],
            "2d_vertical_infiltration": [],
            # TODO: add 1d_2d_groundwater?
        }
        pump_selection = {"in": [], "out": []}

        lines = self.wrapper.lines
        points = self.wrapper.points
        pumps = self.wrapper.pumps

        # all links in and out
        # use bounding box and spatial index to prefilter lines
        request_filter = QgsFeatureRequest().setFilterRect(
            self.polygon.get().boundingBox()
        )
        for line in lines.getFeatures(request_filter):
            line_type = line.attribute('line_type')

            if line_type == LineType.LINE_2D_VERTICAL:
                geom = line.geometry().asPolyline()
                # 2d vertical infiltration line is handmade diagonal (drawn
                # from 2d point 15m towards south-west ). Thus, if at-least
                # its startpoint is within polygon then include the line
                if self.polygon.contains(QgsPointXY(geom[0])):
                    flow_lines["2d_vertical_infiltration"].append(line["id"])

            # test if lines are crossing boundary of polygon
            if line.geometry().crosses(self.polygon):
                geom = line.geometry().asPolyline()
                # check if flow is in or out by testing if startpoint
                # is inside polygon --> out
                outgoing = self.polygon.contains(QgsPointXY(geom[0]))
                # check if flow is in or out by testing if endpoint
                # is inside polygon --> in
                incoming = self.polygon.contains(QgsPointXY(geom[-1]))

                if incoming and outgoing:
                    # skip lines that do have start- and end vertex outside of
                    # polygon
                    pass
                elif outgoing:
                    if line_type in LINE_TYPES_1D:
                        flow_lines["1d_out"].append(line["id"])
                    elif line_type in LINE_TYPES_1D2D:
                        # draw direction of 1d_2d is always from 2d node to
                        # 1d node. So when 2d node is inside polygon (and 1d
                        # node is not) we define it as a '2d__1d_2d_flow' link
                        # because
                        flow_lines["2d__1d_2d_flow"].append(line["id"])
                elif incoming:
                    if line_type in LINE_TYPES_1D:
                        flow_lines["1d_in"].append(line["id"])
                    elif line_type in LINE_TYPES_1D2D:
                        # draw direction of 1d_2d is always from 2d node to
                        # 1d node. So when 1d node is inside polygon (and 2d
                        # node is not) we define it as a '1d__1d_2d_flow' link
                        flow_lines["1d__1d_2d_flow"].append(line["id"])

                if line_type == LineType.LINE_2D and not (incoming and outgoing):
                    # 2d lines are a separate story: discharge on a 2d
                    # link in the nc can be positive and negative during 1
                    # simulation - like you would expect - but we also have
                    # to account for 2d link direction. We have to determine
                    # two things:

                    # A) is 2d link a vertical or horizontal one. Why?
                    # vertical 2d lines (calc cells above each other):
                    # when positive discharge then flow is to north, negative
                    # discharge then flow southwards, while horizontal 2d lines
                    # (calc cells next to each other) yields positive discharge
                    # is flow to the east, negative is flow to west

                    # B) how the start and endpoint are located with
                    # reference to each other. Why? a positive discharge on
                    # a vertical link in the north of your polygon DECREASES
                    # the volume in the polygon, while a positive discharge on
                    # a vertical link in the south of your polygon INCREASES
                    # the volume in the polygon).

                    # so why not only determine (B)?
                    # because then a positive discharge on a diagonal 2d link -
                    # in topview e.g. left up to right down - can mean flow
                    # to east. But it can also mean flow to the north. If we
                    # know it is a vertical link we can be sure flow is to the
                    # north (thats why we need to know (A)

                    # TODO: after I made this code Martijn Siemerink adviced:
                    # 2d links drawing direction is always from south to north
                    # OR west to east, so it not required to get start- and
                    # endpoint of a 2d link

                    start_x = geom[0][0]
                    start_y = geom[0][1]
                    end_x = geom[-1][0]
                    end_y = geom[-1][1]

                    # horizontal line?
                    if line.id() in self.x2d_surf_range:
                        # startpoint in polygon?
                        if self.polygon.contains(QgsPointXY(geom[0])):
                            # directed to east?
                            # long coords increase going east, so:
                            if end_x > start_x:
                                # thus, positive q means flow to east.
                                # Startpoint is in polygon. Endpoint is
                                # located eastwards of startpoint, so positive
                                # q means flow goes OUT!! of polygon
                                flow_lines["2d_out"].append(line["id"])
                            else:
                                flow_lines["2d_in"].append(line["id"])
                        # endpoint in polygon?
                        elif self.polygon.contains(QgsPointXY(geom[-1])):
                            # directed to east?
                            # long coords increase going east
                            if end_x > start_x:
                                # positive q means flow to east. Endpoint is
                                # inside polygon and located eastwards of
                                # startpoint, so positive q means flow goes
                                # INTO!! polygon
                                flow_lines["2d_in"].append(line["id"])
                            else:
                                flow_lines["2d_out"].append(line["id"])

                    # vertical line?
                    if line.id() in self.y2d_surf_range:
                        # startpoint in polygon?
                        if self.polygon.contains(QgsPointXY(geom[0])):
                            # directed to north?
                            # lat coords increase going north, so:
                            if end_y > start_y:
                                # thus, positive q means flow to north.
                                # Startpoint is in polygon. Endpoint is
                                # located northwards of startpoint, so positive
                                # q means flow goes OUT!! of polygon
                                flow_lines["2d_out"].append(line["id"])
                            else:
                                flow_lines["2d_in"].append(line["id"])
                        # endpoint in polygon?
                        elif self.polygon.contains(QgsPointXY(geom[-1])):
                            # directed to north?
                            # lat coords increase going north, so:
                            if end_y > start_y:
                                # positive q means flow to north. Endpoint is
                                # inside polygon and located northwards of
                                # startpoint, so flow goes INTO!! polygon
                                flow_lines["2d_in"].append(line["id"])
                            else:
                                flow_lines["2d_out"].append(line["id"])

                if line_type == LineType.LINE_2D_GROUNDWATER and not (incoming and outgoing):

                    start_x = geom[0][0]
                    start_y = geom[0][1]
                    end_x = geom[-1][0]
                    end_y = geom[-1][1]

                    # horizontal line?
                    if line.id() in self.x_grndwtr_range:
                        # startpoint in polygon?
                        if self.polygon.contains(QgsPointXY(geom[0])):
                            if end_x > start_x:
                                flow_lines["2d_groundwater_out"].append(line["id"])
                            else:
                                flow_lines["2d_groundwater_in"].append(line["id"])
                        # endpoint in polygon?
                        elif self.polygon.contains(QgsPointXY(geom[-1])):
                            if end_x > start_x:
                                flow_lines["2d_groundwater_in"].append(line["id"])
                            else:
                                flow_lines["2d_groundwater_out"].append(line["id"])
                    # vertical line?
                    if line.id() in self.y_grndwtr_range:
                        # startpoint in polygon?
                        if self.polygon.contains(QgsPointXY(geom[0])):
                            if end_y > start_y:
                                flow_lines["2d_groundwater_out"].append(line["id"])
                            else:
                                flow_lines["2d_groundwater_in"].append(line["id"])
                        elif self.polygon.contains(QgsPointXY(geom[-1])):
                            if end_y > start_y:
                                flow_lines["2d_groundwater_in"].append(line["id"])
                            else:
                                flow_lines["2d_groundwater_out"].append(line["id"])

            elif line_type in LINE_TYPES_1D2D and line.geometry().within(self.polygon):
                flow_lines["1d_2d_exch"].append(line["id"])

        # find boundaries in polygon
        node_types_csv = ",".join(str(n.value) for n in NODE_TYPES_BOUNDARIES)
        request_filter = (
            QgsFeatureRequest()
            .setFilterRect(self.polygon.get().boundingBox())
            .setFilterExpression(f"node_type in ({node_types_csv})")
        )

        # all boundaries in polygon
        for bound in points.getFeatures(request_filter):
            if self.polygon.contains(QgsPointXY(bound.geometry().asPoint())):
                # find link connected to boundary
                request_filter_bound = QgsFeatureRequest().setFilterExpression(
                    f"calculation_node_id_start == {bound.id()} OR"
                    f"calculation_node_id_end == {bound.id()}"
                )
                bound_lines = lines.getFeatures(request_filter_bound)
                for bound_line in bound_lines:
                    if bound_line["calculation_node_id_start"] == bound["id"]:
                        if bound["node_type"] == NodeType.NODE_1D_BOUNDARIES:
                            flow_lines["1d_bound_in"].append(bound_line["id"])
                        else:  # 2d
                            flow_lines["2d_bound_in"].append(bound_line["id"])
                    else:  # out
                        if bound["node_type"] == NodeType.NODE_1D_BOUNDARIES:
                            flow_lines["1d_bound_out"].append(bound_line["id"])
                        else:  # 2d
                            flow_lines["2d_bound_out"].append(bound_line["id"])

        # pumps
        # use bounding box and spatial index to prefilter pumps
        if pumps is None:
            f_pumps = []
        else:
            request_filter = QgsFeatureRequest().setFilterRect(
                self.polygon.get().boundingBox()
            )
            f_pumps = pumps.getFeatures(request_filter)

        for pump in f_pumps:
            # test if lines are crossing boundary of polygon
            pump_geometry = pump.geometry()
            if pump_geometry.intersects(self.polygon):
                pump_end_node_id = pump["node_idx2"]
                linestring = pump_geometry.asPolyline()
                # check if flow is in or out by testing if startpoint
                # is inside polygon --> out
                startpoint = QgsPointXY(linestring[0])
                endpoint = QgsPointXY(linestring[-1])
                outgoing = self.polygon.contains(startpoint)
                # check if flow is in or out by testing if endpoint
                # is inside polygon --> in
                incoming = self.polygon.contains(endpoint) if not pump_end_node_id == NO_ENDPOINT_ID else False

                if incoming and outgoing:
                    # skip
                    pass
                elif outgoing:
                    pump_selection["out"].append(pump["id"])
                elif incoming:
                    pump_selection["in"].append(pump["id"])

        logger.info(str(flow_lines))
        return flow_lines, pump_selection

    def _get_node_ids(self):
        """Returns a dictionary with node ids by category:

        {
            '1d': [..., ...],
            '2d': [..., ...],
            '2d_groundwater': [..., ...],
        }
        """

        node_ids = {"1d": [], "2d": [], "2d_groundwater": []}

        # use bounding box and spatial index to prefilter lines
        request_filter = QgsFeatureRequest().setFilterRect(
            self.polygon.get().boundingBox()
        )
        node_types = NODE_TYPES_1D | NODE_TYPES_2D | NODE_TYPES_2D_GROUNDWATER
        node_types_csv = ",".join(str(n.value) for n in node_types)
        request_filter.setFilterExpression(f"node_type in ({node_types_csv})")
        # todo: check if boundary nodes could not have rain, infiltration, etc.

        node_type_map = {}
        node_type_map.update({n.value: "1d" for n in NODE_TYPES_1D})
        node_type_map.update({n.value: "2d" for n in NODE_TYPES_2D})
        node_type_map.update({n.value: "2d_groundwater"
                              for n in NODE_TYPES_2D_GROUNDWATER})

        for point in self.wrapper.points.getFeatures(request_filter):
            # test if points are contained by polygon
            if self.polygon.contains(point.geometry()):
                node_ids[node_type_map[point['node_type']]].append(point.id())
        return node_ids

    def _get_aggregated_flows(self):
        """
        Returns a tuple (times, all_flows) defined as:

            times = array of timestamps
            all_flows = array with shape (np.size(times, 0), len(INPUT_SERIES))
        """
        # constants referenced in record array
        # shared by links and nodes
        TYPE_1D = "1d"
        TYPE_2D = "2d"
        TYPE_2D_GROUNDWATER = "2d_groundwater"
        # links only
        TYPE_1D_BOUND_IN = "1d_bound_in"
        TYPE_2D_BOUND_IN = "2d_bound_in"
        TYPE_1D__1D_2D_EXCH = "1d__1d_2d_exch"
        TYPE_2D__1D_2D_EXCH = "2d__1d_2d_exch"
        TYPE_1D__1D_2D_FLOW = "1d__1d_2d_flow"
        TYPE_2D__1D_2D_FLOW = "2d__1d_2d_flow"
        TYPE_2D_VERTICAL_INFILTRATION = "2d_vertical_infiltration"

        ALL_TYPES = [
            TYPE_1D,
            TYPE_2D,
            TYPE_2D_GROUNDWATER,
            TYPE_1D_BOUND_IN,
            TYPE_2D_BOUND_IN,
            TYPE_1D__1D_2D_EXCH,
            TYPE_2D__1D_2D_EXCH,
            TYPE_1D__1D_2D_FLOW,
            TYPE_2D__1D_2D_FLOW,
            TYPE_2D_VERTICAL_INFILTRATION,
        ]

        NTYPE_MAXLEN = 25
        assert (
            max(list(map(len, ALL_TYPES))) <= NTYPE_MAXLEN
        ), "NTYPE_MAXLEN insufficiently large for all values"
        NTYPE_DTYPE = "U%s" % NTYPE_MAXLEN

        # LINKS
        #######

        # create numpy table with flowlink information
        tlink = []  # id, 1d or 2d, in or out
        for idx in self.flowline_ids["2d_in"]:
            tlink.append((idx, TYPE_2D, 1))
        for idx in self.flowline_ids["2d_out"]:
            tlink.append((idx, TYPE_2D, -1))

        for idx in self.flowline_ids["2d_bound_in"]:
            tlink.append((idx, TYPE_2D_BOUND_IN, 1))
        for idx in self.flowline_ids["2d_bound_out"]:
            tlink.append((idx, TYPE_2D_BOUND_IN, -1))

        for idx in self.flowline_ids["1d_in"]:
            tlink.append((idx, TYPE_1D, 1))
        for idx in self.flowline_ids["1d_out"]:
            tlink.append((idx, TYPE_1D, -1))

        for idx in self.flowline_ids["1d_bound_in"]:
            tlink.append((idx, TYPE_1D_BOUND_IN, 1))
        for idx in self.flowline_ids["1d_bound_out"]:
            tlink.append((idx, TYPE_1D_BOUND_IN, -1))

        for idx in self.flowline_ids["2d_groundwater_in"]:
            tlink.append((idx, TYPE_2D_GROUNDWATER, 1))
        for idx in self.flowline_ids["2d_groundwater_out"]:
            tlink.append((idx, TYPE_2D_GROUNDWATER, -1))

        for idx in self.flowline_ids["2d_vertical_infiltration"]:
            tlink.append((idx, TYPE_2D_VERTICAL_INFILTRATION, 1))

        # 1d_2d flow intersects the polygon:
        # the in- or out flow for 1d2d is different than flows dirs above:
        #   - discharge from 1d to 2d is always positive in the .nc
        #   - discharge from 2d to 1d is always negative in the .nc
        # 1d__1d_2d_flow: 1d node is inside polygon, 2d node is outside.
        #   - positive discharge means flow outwards polygon
        #   - negative discharge means flow inwards polygon
        # 2d__1d_2d_flow: 1d node is outside polygon, 2d node is inside
        #   - positive discharge means flow inwards polygon
        #   - negative discharge means flow outwards polygon
        for idx in self.flowline_ids["1d__1d_2d_flow"]:
            tlink.append((idx, TYPE_1D__1D_2D_FLOW, -1))
        # 1d_2d_out: 1d node is outside polygon, 2d node is inside
        for idx in self.flowline_ids["2d__1d_2d_flow"]:
            tlink.append((idx, TYPE_2D__1D_2D_FLOW, 1))
        # 1d_2d within the polygon (from 1d perspective so everything flipped)
        for idx in self.flowline_ids["1d_2d_exch"]:
            tlink.append((idx, TYPE_1D__1D_2D_EXCH, -1))
        # 1d_2d within the polygon (from 2d perspective)
        for idx in self.flowline_ids["1d_2d_exch"]:
            tlink.append((idx, TYPE_2D__1D_2D_EXCH, 1))

        np_link = np.array(
            tlink, dtype=[("id", int), ("ntype", NTYPE_DTYPE), ("dir", int)]
        )

        # sort for faster reading of netcdf
        np_link.sort(axis=0)

        # create masks
        mask_2d = np_link["ntype"] != TYPE_2D
        mask_1d = np_link["ntype"] != TYPE_1D
        mask_2d_bound = np_link["ntype"] != TYPE_2D_BOUND_IN
        mask_1d_bound = np_link["ntype"] != TYPE_1D_BOUND_IN

        mask_1d__1d_2d_flow = np_link["ntype"] != TYPE_1D__1D_2D_FLOW
        mask_2d__1d_2d_flow = np_link["ntype"] != TYPE_2D__1D_2D_FLOW
        mask_1d__1d_2d_exch = np_link["ntype"] != TYPE_1D__1D_2D_EXCH
        mask_2d__1d_2d_exch = np_link["ntype"] != TYPE_2D__1D_2D_EXCH
        mask_2d_groundwater = np_link["ntype"] != TYPE_2D_GROUNDWATER
        mask_2d_vertical_infiltration = (
            np_link["ntype"] != TYPE_2D_VERTICAL_INFILTRATION
        )

        threedi_result = self.wrapper.threedi_result

        # get all flows through incoming and outgoing flows
        times = threedi_result.get_timestamps(parameter="q_cum")

        all_flows = np.zeros(shape=(len(times), len(INPUT_SERIES)))
        # total_location = np.zeros(shape=(np.size(np_link, 0), 2))

        # non-2d links
        pos_pref = 0
        neg_pref = 0

        if np_link.size > 0:
            for ts_idx, t in enumerate(times):
                # (1) inflow and outflow through 1d and 2d
                # vol = threedi_result.get_values_by_timestep_nr('q', ts_idx,
                # np_link['id']) * np_link['dir']  # * dt

                flow_pos = (
                    threedi_result.get_values_by_timestep_nr(
                        "q_cum_positive", ts_idx, np_link["id"]
                    )
                    * np_link["dir"]
                )
                flow_neg = (
                    threedi_result.get_values_by_timestep_nr(
                        "q_cum_negative", ts_idx, np_link["id"]
                    )
                    * np_link["dir"]
                    * -1
                )

                in_sum = flow_pos - pos_pref
                out_sum = flow_neg - neg_pref
                pos_pref = flow_pos
                neg_pref = flow_neg

                # 2d flow (2d_in)
                all_flows[ts_idx, 0] = (
                    ma.masked_array(in_sum, mask=mask_2d).clip(min=0).sum()
                    + ma.masked_array(out_sum, mask=mask_2d).clip(min=0).sum()
                )
                # 2d flow (2d_out)
                all_flows[ts_idx, 1] = (
                    ma.masked_array(in_sum, mask=mask_2d).clip(max=0).sum()
                    + ma.masked_array(out_sum, mask=mask_2d).clip(max=0).sum()
                )

                # 1d flow (1d_in)
                all_flows[ts_idx, 2] = (
                    ma.masked_array(in_sum, mask=mask_1d).clip(min=0).sum()
                    + ma.masked_array(out_sum, mask=mask_1d).clip(min=0).sum()
                )
                # 1d flow (1d_out)
                all_flows[ts_idx, 3] = (
                    ma.masked_array(in_sum, mask=mask_1d).clip(max=0).sum()
                    + ma.masked_array(out_sum, mask=mask_1d).clip(max=0).sum()
                )

                # 2d bound (2d_bound_in)
                all_flows[ts_idx, 4] = (
                    ma.masked_array(in_sum, mask=mask_2d_bound).clip(min=0).sum()
                    + ma.masked_array(out_sum, mask=mask_2d_bound).clip(min=0).sum()
                )
                # 2d bound (2d_bound_out)
                all_flows[ts_idx, 5] = (
                    ma.masked_array(in_sum, mask=mask_2d_bound).clip(max=0).sum()
                    + ma.masked_array(out_sum, mask=mask_2d_bound).clip(max=0).sum()
                )

                # 1d bound (1d_bound_in)
                all_flows[ts_idx, 6] = (
                    ma.masked_array(in_sum, mask=mask_1d_bound).clip(min=0).sum()
                    + ma.masked_array(out_sum, mask=mask_1d_bound).clip(min=0).sum()
                )
                # 1d bound (1d_bound_out)
                all_flows[ts_idx, 7] = (
                    ma.masked_array(in_sum, mask=mask_1d_bound).clip(max=0).sum()
                    + ma.masked_array(out_sum, mask=mask_1d_bound).clip(max=0).sum()
                )

                # 1d__1d_2d_flow_in
                all_flows[ts_idx, 8] = (
                    ma.masked_array(in_sum, mask=mask_1d__1d_2d_flow).clip(min=0).sum()
                    + ma.masked_array(out_sum, mask=mask_1d__1d_2d_flow)
                    .clip(min=0)
                    .sum()
                )
                # 1d__1d_2d_flow_out
                all_flows[ts_idx, 9] = (
                    ma.masked_array(in_sum, mask=mask_1d__1d_2d_flow).clip(max=0).sum()
                    + ma.masked_array(out_sum, mask=mask_1d__1d_2d_flow)
                    .clip(max=0)
                    .sum()
                )

                # 2d__1d_2d_flow_in
                all_flows[ts_idx, 30] = (
                    ma.masked_array(in_sum, mask=mask_2d__1d_2d_flow).clip(min=0).sum()
                    + ma.masked_array(out_sum, mask=mask_2d__1d_2d_flow)
                    .clip(min=0)
                    .sum()
                )
                # 2d__1d_2d_flow_out
                all_flows[ts_idx, 31] = (
                    ma.masked_array(in_sum, mask=mask_2d__1d_2d_flow).clip(max=0).sum()
                    + ma.masked_array(out_sum, mask=mask_2d__1d_2d_flow)
                    .clip(max=0)
                    .sum()
                )

                # 1d (1d__1d_2d_exch_in)
                all_flows[ts_idx, 10] = (
                    ma.masked_array(in_sum, mask=mask_1d__1d_2d_exch).clip(min=0).sum()
                    + ma.masked_array(out_sum, mask=mask_1d__1d_2d_exch)
                    .clip(min=0)
                    .sum()
                )
                # 1d (1d__1d_2d_exch_out)
                all_flows[ts_idx, 11] = (
                    ma.masked_array(in_sum, mask=mask_1d__1d_2d_exch).clip(max=0).sum()
                    + ma.masked_array(out_sum, mask=mask_1d__1d_2d_exch)
                    .clip(max=0)
                    .sum()
                )

                # 2d (2d__1d_2d_exch_in)
                all_flows[ts_idx, 32] = (
                    ma.masked_array(in_sum, mask=mask_2d__1d_2d_exch).clip(min=0).sum()
                    + ma.masked_array(out_sum, mask=mask_2d__1d_2d_exch)
                    .clip(min=0)
                    .sum()
                )
                # 2d (2d__1d_2d_exch_out)
                all_flows[ts_idx, 33] = (
                    ma.masked_array(in_sum, mask=mask_2d__1d_2d_exch).clip(max=0).sum()
                    + ma.masked_array(out_sum, mask=mask_2d__1d_2d_exch)
                    .clip(max=0)
                    .sum()
                )

                # 2d groundwater (2d_groundwater_in)
                all_flows[ts_idx, 23] = (
                    ma.masked_array(in_sum, mask=mask_2d_groundwater).clip(min=0).sum()
                    + ma.masked_array(out_sum, mask=mask_2d_groundwater)
                    .clip(min=0)
                    .sum()
                )
                # 2d groundwater (2d_groundwater_out)
                all_flows[ts_idx, 24] = (
                    ma.masked_array(in_sum, mask=mask_2d_groundwater).clip(max=0).sum()
                    + ma.masked_array(out_sum, mask=mask_2d_groundwater)
                    .clip(max=0)
                    .sum()
                )

                # NOTE: positive vertical infiltration is from surface to
                # groundwater node. We make this negative because it's
                # 'sink-like', and to make it in line with the
                # infiltration_rate_simple which also has a -1 multiplication
                # factor.
                # 2d_vertical_infiltration (2d_vertical_infiltration_pos)
                all_flows[ts_idx, 28] = (
                    -1
                    * ma.masked_array(in_sum, mask=mask_2d_vertical_infiltration)
                    .clip(min=0)
                    .sum()
                    + ma.masked_array(out_sum, mask=mask_2d_vertical_infiltration)
                    .clip(min=0)
                    .sum()
                )
                # 2d_vertical_infiltration (2d_vertical_infiltration_neg)
                all_flows[ts_idx, 29] = (
                    -1
                    * ma.masked_array(in_sum, mask=mask_2d_vertical_infiltration)
                    .clip(max=0)
                    .sum()
                    + ma.masked_array(out_sum, mask=mask_2d_vertical_infiltration)
                    .clip(max=0)
                    .sum()
                )

        # PUMPS
        #######

        tpump = []
        for idx in self.pump_ids["in"]:
            tpump.append((idx, 1))
        for idx in self.pump_ids["out"]:
            tpump.append((idx, -1))
        np_pump = np.array(tpump, dtype=[("id", int), ("dir", int)])
        np_pump.sort(axis=0)

        if np_pump.size > 0:
            # pumps
            pump_pref = 0
            for ts_idx, t in enumerate(times):
                # (2) inflow and outflow through pumps
                pump_flow = (
                    threedi_result.get_values_by_timestep_nr(
                        "q_pump_cum", ts_idx, np_pump["id"]
                    )
                    * np_pump["dir"]
                )

                flow_dt = pump_flow - pump_pref
                pump_pref = pump_flow

                in_sum = flow_dt.clip(min=0)
                out_sum = flow_dt.clip(max=0)

                all_flows[ts_idx, 12] = in_sum.sum()
                all_flows[ts_idx, 13] = out_sum.sum()

        # NODES
        #######

        tnode = []  # id, 1d or 2d, in or out
        for idx in self.node_ids["2d"]:
            tnode.append((idx, TYPE_2D))
        for idx in self.node_ids["1d"]:
            tnode.append((idx, TYPE_1D))
        for idx in self.node_ids["2d_groundwater"]:
            tnode.append((idx, TYPE_2D_GROUNDWATER))
        NTYPE_DTYPE
        np_node = np.array(tnode, dtype=[("id", int), ("ntype", NTYPE_DTYPE)])
        np_node.sort(axis=0)

        mask_2d_nodes = np_node["ntype"] != TYPE_2D
        mask_1d_nodes = np_node["ntype"] != TYPE_1D
        mask_2d_groundwater_nodes = np_node["ntype"] != TYPE_2D_GROUNDWATER

        np_2d_node = ma.masked_array(np_node["id"], mask=mask_2d_nodes).compressed()
        np_1d_node = ma.masked_array(np_node["id"], mask=mask_1d_nodes).compressed()
        np_2d_groundwater_node = ma.masked_array(
            np_node["id"], mask=mask_2d_groundwater_nodes
        ).compressed()

        for parameter, agg_method, node, pnr, factor in [
            ("rain", "_cum", np_2d_node, 14, 1),
            # TODO: in old model results this parameter is called
            # 'infiltration_rate', thus it is not backwards compatible right
            # now
            ("infiltration_rate_simple", "_cum", np_2d_node, 15, -1),
            # TODO: inefficient because we look up q_lat data twice
            ("q_lat", "_cum", np_2d_node, 16, 1),
            ("q_lat", "_cum", np_1d_node, 17, 1),
            ("leak", "_cum", np_2d_groundwater_node, 26, 1),
            ("rain", "_cum", np_1d_node, 27, 1),
            ("intercepted_volume", "_current", np_2d_node, 34, -1),
            ("q_sss", "_cum", np_2d_node, 35, 1),
        ]:

            if node.size > 0:
                if parameter + agg_method in threedi_result.available_vars:
                    values_pref = 0
                    for ts_idx, t in enumerate(times):
                        values = threedi_result.get_values_by_timestep_nr(
                            parameter + agg_method, ts_idx, node
                        ).sum()
                        values_dt = values - values_pref
                        values_pref = values
                        all_flows[ts_idx, pnr] = values_dt * factor
        t_pref = 0

        for ts_idx, t in enumerate(times):
            if ts_idx == 0:
                # just to make sure machine precision distortion
                # is reduced for the first timestamp (everything
                # should be 0
                all_flows[ts_idx] = all_flows[ts_idx] / (times[1] - t)
            else:
                all_flows[ts_idx] = all_flows[ts_idx] / (t - t_pref)
                t_pref = t

        if np_node.size > 0:
            # delta volume
            t_pref = 0
            for ts_idx, t in enumerate(times):
                # delta volume
                if ts_idx == 0:
                    # volume difference first timestep is always 0
                    all_flows[ts_idx, 18] = 0
                    all_flows[ts_idx, 19] = 0
                    all_flows[ts_idx, 25] = 0

                    vol_current = threedi_result.get_values_by_timestep_nr(
                        "vol_current", ts_idx, np_node["id"]
                    )
                    td_vol_pref = ma.masked_array(vol_current, mask=mask_2d_nodes).sum()
                    od_vol_pref = ma.masked_array(vol_current, mask=mask_1d_nodes).sum()
                    td_vol_pref_gw = ma.masked_array(
                        vol_current, mask=mask_2d_groundwater_nodes
                    ).sum()
                    t_pref = t
                else:
                    vol_current = threedi_result.get_values_by_timestep_nr(
                        "vol_current", ts_idx, np_node["id"]
                    )

                    td_vol = ma.masked_array(vol_current, mask=mask_2d_nodes).sum()
                    od_vol = ma.masked_array(vol_current, mask=mask_1d_nodes).sum()
                    td_vol_gw = ma.masked_array(
                        vol_current, mask=mask_2d_groundwater_nodes
                    ).sum()

                    dt = t - t_pref
                    all_flows[ts_idx, 18] = (td_vol - td_vol_pref) / dt
                    all_flows[ts_idx, 19] = (od_vol - od_vol_pref) / dt
                    all_flows[ts_idx, 25] = (td_vol_gw - td_vol_pref_gw) / dt

                    td_vol_pref = td_vol
                    od_vol_pref = od_vol
                    td_vol_pref_gw = td_vol_gw
                    t_pref = t
        all_flows = np.nan_to_num(all_flows)

        return times, all_flows


class WaterBalanceTool(object):
    """QGIS Plugin Implementation."""

    def __init__(self, iface, model):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        self.iface = iface
        self.icon_path = str(Path(__file__).parent.parent / 'icons' / 'weight-scale.png')
        self.menu_text = u"Water Balance Tool"

        self.is_active = False
        self.widget = None
        self.manager = WaterBalanceCalculationManager(model)

    def run(self):
        if self.is_active:
            return

        widget = WaterBalanceWidget(
            "3Di water balance", manager=self.manager, iface=self.iface,
        )
        widget.closingWidget.connect(self.on_close_child_widget)
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, widget)
        widget.show()

        self.is_active = True
        self.widget = widget
        # TODO connect signals of results changes

    def on_unload(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""
        if self.widget is not None:
            self.widget.close()
        self.active = False

    def on_close_child_widget(self):
        """Cleanup necessary items here when plugin widget is closed"""
        self.widget.closingWidget.disconnect(self.on_close_child_widget)
        self.widget = None
        self.is_active = False
        # TODO disconnect signals of result changes


class WaterBalanceCalculationManager:
    def __init__(self, model):
        self.model = model
        self.calculations = {}
        self._polygon = None

    def add_result(self, result):
        wrapper = ResultWrapper(result)
        if not wrapper.has_required_vars():  # missing aggvars etc.?
            return
        if not wrapper.has_synchronized_timestamps():
            return

        polygon = self.polygon.transformed(crs=wrapper.lines.crs())
        calculation = WaterBalanceCalculation(wrapper=wrapper, polygon=polygon)
        self.calculations[result.path] = calculation
        # TODO signal update of widget

    def remove_result(self, result):
        del self.calculations[result]
        # TODO signal update of widget

    @property
    def polygon(self):
        return self._polygon

    @polygon.setter
    def polygon(self, polygon):
        if polygon is None:
            self._polygon = None
            self.calculations = {}
            return

        self._polygon = polygon
        for result in self.model.get_results(checked_only=False):
            self.add_result(result)
        # TODO signal update of widget

    def __iter__(self):
        return iter(self.calculations.values())
