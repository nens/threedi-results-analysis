from __future__ import division

from builtins import str
from builtins import map
from builtins import range
from builtins import object
import logging
import os.path

import numpy as np
import numpy.ma as ma
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import QgsFeatureRequest, QgsPointXY
from ThreeDiToolbox.datasource.netcdf import find_h5_file
from ThreeDiToolbox.utils.patched_threedigrid import GridH5Admin
from threedigrid.admin.gridresultadmin import GridH5ResultAdmin


# Import the code for the DockWidget
from ThreeDiToolbox.water_balance.views.waterbalance_widget \
    import WaterBalanceWidget


log = logging.getLogger('DeltaresTdi.' + __name__)


class WaterBalanceCalculation(object):

    def __init__(self, ts_datasource):
        self.ts_datasource = ts_datasource

        # gridadmin
        nc_path = self.ts_datasource.rows[0].datasource().file_path
        h5 = find_h5_file(nc_path)
        ga = GridH5Admin(h5)

        # total nr of x-dir (horizontal in topview) 2d lines
        nr_2d_x_dir = ga.get_from_meta('liutot')
        # total nr of y-dir (vertical in topview) 2d lines
        nr_2d_y_dir = ga.get_from_meta('livtot')
        # total nr of 2d lines
        nr_2d = ga.get_from_meta('l2dtot')
        # total nr of groundwater lines
        start_gr = ga.get_from_meta('lgrtot')

        # get range of horizontal (in top view) surface water line ids
        x2d_surf_range_min = 1
        x2d_surf_range_max = nr_2d_x_dir
        self.x2d_surf_range = list(range(x2d_surf_range_min, x2d_surf_range_max + 1))  # noqa

        # get range of vertical (in top view) surface water line ids
        y2d_surf_range_min = x2d_surf_range_max + 1
        y2d_surf_range_max = x2d_surf_range_max + nr_2d_y_dir
        self.y2d_surf_range = list(range(y2d_surf_range_min, y2d_surf_range_max + 1))  # noqa

        # get range of vertical (in side view) line ids in the gridadmin.
        # These lines represent surface-groundwater (vertical) flow
        vert_flow_range_min = y2d_surf_range_max + 1
        vert_flow_range_max = y2d_surf_range_max + nr_2d
        self.vert_flow_range = list(range(
            vert_flow_range_min, vert_flow_range_max + 1))

        if ga.has_groundwater:
            # total nr of x-dir (horizontal in topview) 2d groundwater lines
            x_grndwtr_range_min = start_gr + 1
            x_grndwtr_range_max = start_gr + nr_2d_x_dir
            self.x_grndwtr_range = list(range(
                x_grndwtr_range_min, x_grndwtr_range_max + 1))

            # total nr of y-dir (vertical in topview) 2d groundwater lines
            y_grndwtr_range_min = x_grndwtr_range_max + 1
            y_grndwtr_range_max = x_grndwtr_range_max + nr_2d
            self.y_grndwtr_range = list(range(
                y_grndwtr_range_min, y_grndwtr_range_max + 1))

    def get_incoming_and_outcoming_link_ids(self, wb_polygon, model_part):
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

        log.info('polygon of wb area: %s', wb_polygon.asWkt())

        # the '_out' and '_in' indicate the draw direction of the flow_line.
        # a flow line can have in 1 simulation both positive and negative
        # discharge (with extend to the draw direction). Later on, in
        # get_aggregated_flows() this numpy timeserie is clipped with
        # max=0 for flow in 1 direction and min=0 for flow in the opposite
        # direction.
        flow_lines = {
            '1d_in': [],
            '1d_out': [],
            '1d_bound_in': [],
            '1d_bound_out': [],
            '2d_in': [],
            '2d_out': [],
            '2d_bound_in': [],
            '2d_bound_out': [],
            # 1d2d flow lines intersect polygon (1d is inside polygon)
            '1d__1d_2d_flow': [],
            # 1d2d flow lines intersect polygon (2d is inside polygon)
            '2d__1d_2d_flow': [],
            # 1d2d exchange lines are within polygon (both nodes inside)
            '1d_2d_exch': [],
            '2d_groundwater_in': [],
            '2d_groundwater_out': [],
            '2d_vertical_infiltration': [],
            # TODO: add 1d_2d_groundwater?
        }
        pump_selection = {
            'in': [],
            'out': []
        }

        lines, points, pumps = self.ts_datasource.rows[0].get_result_layers()

        # all links in and out
        # use bounding box and spatial index to prefilter lines
        request_filter = QgsFeatureRequest().setFilterRect(
            wb_polygon.get().boundingBox())
        for line in lines.getFeatures(request_filter):

            if line['type'] == '2d_vertical_infiltration':
                geom = line.geometry().asPolyline()
                # 2d vertical infiltration line is handmade diagonal (drawn
                # from 2d point 15m towards south-west ). Thus, if at-least
                # its startpoint is within polygon then include the line
                if wb_polygon.contains(QgsPointXY(geom[0])):
                    flow_lines['2d_vertical_infiltration'].append(line['id'])

            # test if lines are crossing boundary of polygon
            if line.geometry().crosses(wb_polygon):
                geom = line.geometry().asPolyline()
                # check if flow is in or out by testing if startpoint
                # is inside polygon --> out
                outgoing = wb_polygon.contains(QgsPointXY(geom[0]))
                # check if flow is in or out by testing if endpoint
                # is inside polygon --> in
                incoming = wb_polygon.contains(QgsPointXY(geom[-1]))

                if incoming and outgoing:
                    # skip lines that do have start- and end vertex outside of
                    # polygon
                    pass
                elif outgoing:
                    if line['type'] in [
                            '1d', 'v2_pipe', 'v2_channel', 'v2_culvert',
                            'v2_orifice', 'v2_weir']:
                        flow_lines['1d_out'].append(line['id'])
                    elif line['type'] in ['1d_2d']:
                        # draw direction of 1d_2d is always from 2d node to
                        # 1d node. So when 2d node is inside polygon (and 1d
                        # node is not) we define it as a '2d__1d_2d_flow' link
                        # because
                        flow_lines['2d__1d_2d_flow'].append(line['id'])
                elif incoming:
                    if line['type'] in [
                            '1d', 'v2_pipe', 'v2_channel', 'v2_culvert',
                            'v2_orifice', 'v2_weir']:
                        flow_lines['1d_in'].append(line['id'])
                    elif line['type'] in ['1d_2d']:
                        # draw direction of 1d_2d is always from 2d node to
                        # 1d node. So when 1d node is inside polygon (and 2d
                        # node is not) we define it as a '1d__1d_2d_flow' link
                        flow_lines['1d__1d_2d_flow'].append(line['id'])

                if line['type'] in ['2d'] and not (incoming and outgoing):
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
                        if wb_polygon.contains(QgsPointXY(geom[0])):
                            # directed to east?
                            # long coords increase going east, so:
                            if end_x > start_x:
                                # thus, positive q means flow to east.
                                # Startpoint is in polygon. Endpoint is
                                # located eastwards of startpoint, so positive
                                # q means flow goes OUT!! of polygon
                                flow_lines['2d_out'].append(line['id'])
                            else:
                                flow_lines['2d_in'].append(line['id'])
                        # endpoint in polygon?
                        elif wb_polygon.contains(QgsPointXY(geom[-1])):
                            # directed to east?
                            # long coords increase going east
                            if end_x > start_x:
                                # positive q means flow to east. Endpoint is
                                # inside polygon and located eastwards of
                                # startpoint, so positive q means flow goes
                                # INTO!! polygon
                                flow_lines['2d_in'].append(line['id'])
                            else:
                                flow_lines['2d_out'].append(line['id'])

                    # vertical line?
                    if line.id() in self.y2d_surf_range:
                        # startpoint in polygon?
                        if wb_polygon.contains(QgsPointXY(geom[0])):
                            # directed to north?
                            # lat coords increase going north, so:
                            if end_y > start_y:
                                # thus, positive q means flow to north.
                                # Startpoint is in polygon. Endpoint is
                                # located northwards of startpoint, so positive
                                # q means flow goes OUT!! of polygon
                                flow_lines['2d_out'].append(line['id'])
                            else:
                                flow_lines['2d_in'].append(line['id'])
                        # endpoint in polygon?
                        elif wb_polygon.contains(QgsPointXY(geom[-1])):
                            # directed to north?
                            # lat coords increase going north, so:
                            if end_y > start_y:
                                # positive q means flow to north. Endpoint is
                                # inside polygon and located northwards of
                                # startpoint, so flow goes INTO!! polygon
                                flow_lines['2d_in'].append(line['id'])
                            else:
                                flow_lines['2d_out'].append(line['id'])

                if line['type'] in ['2d_groundwater'] and not (
                        incoming and outgoing):

                    start_x = geom[0][0]
                    start_y = geom[0][1]
                    end_x = geom[-1][0]
                    end_y = geom[-1][1]

                    # horizontal line?
                    if line.id() in self.x_grndwtr_range:
                        # startpoint in polygon?
                        if wb_polygon.contains(QgsPointXY(geom[0])):
                            if end_x > start_x:
                                flow_lines['2d_groundwater_out'].append(
                                    line['id'])
                            else:
                                flow_lines['2d_groundwater_in'].append(
                                    line['id'])
                        # endpoint in polygon?
                        elif wb_polygon.contains(QgsPointXY(geom[-1])):
                            if end_x > start_x:
                                flow_lines['2d_groundwater_in'].append(
                                    line['id'])
                            else:
                                flow_lines['2d_groundwater_out'].append(
                                    line['id'])
                    # vertical line?
                    if line.id() in self.y_grndwtr_range:
                        # startpoint in polygon?
                        if wb_polygon.contains(QgsPointXY(geom[0])):
                            if end_y > start_y:
                                flow_lines['2d_groundwater_out'].append(
                                    line['id'])
                            else:
                                flow_lines['2d_groundwater_in'].append(
                                    line['id'])
                        elif wb_polygon.contains(QgsPointXY(geom[-1])):
                            if end_y > start_y:
                                flow_lines['2d_groundwater_in'].append(
                                    line['id'])
                            else:
                                flow_lines['2d_groundwater_out'].append(
                                    line['id'])

            elif line['type'] == '1d_2d' and line.geometry().within(
                    wb_polygon):
                flow_lines['1d_2d_exch'].append(line['id'])

        # find boundaries in polygon
        request_filter = QgsFeatureRequest().setFilterRect(
            wb_polygon.get().boundingBox()
        ).setFilterExpression(u'"type" = '
                              u'\'1d_bound\' or "type" = '
                              u'\'2d_bound\'')

        # all boundaries in polygon
        for bound in points.getFeatures(request_filter):
            if wb_polygon.contains(QgsPointXY(bound.geometry().asPoint())):
                # find link connected to boundary
                request_filter_bound = QgsFeatureRequest().\
                    setFilterExpression(u'"start_node_idx" = '
                                        u'\'{idx}\' or "end_node_idx" ='
                                        u' \'{idx}\''.format(idx=bound['id']))
                bound_lines = lines.getFeatures(request_filter_bound)
                for bound_line in bound_lines:
                    if bound_line['start_node_idx'] == bound['id']:
                        if bound['type'] == '1d_bound':
                            flow_lines['1d_bound_in'].append(bound_line['id'])
                        else:  # 2d
                            flow_lines['2d_bound_in'].append(bound_line['id'])
                    else:  # out
                        if bound['type'] == '1d_bound':
                            flow_lines['1d_bound_out'].append(bound_line['id'])
                        else:  # 2d
                            flow_lines['2d_bound_out'].append(bound_line['id'])

        # pumps
        # use bounding box and spatial index to prefilter pumps
        if pumps is None:
            f_pumps = []
        else:
            request_filter = QgsFeatureRequest().setFilterRect(
                wb_polygon.get().boundingBox())
            f_pumps = pumps.getFeatures(request_filter)

        for pump in f_pumps:
            # test if lines are crossing boundary of polygon
            if pump.geometry().crosses(wb_polygon):
                geom = pump.geometry().asPolyline()
                # check if flow is in or out by testing if startpoint
                # is inside polygon --> out
                outgoing = wb_polygon.contains(QgsPointXY(geom[0]))
                # check if flow is in or out by testing if endpoint
                # is inside polygon --> in
                incoming = wb_polygon.contains(QgsPointXY(geom[-1]))

                if incoming and outgoing:
                    # skip
                    pass
                elif outgoing:
                    pump_selection['out'].append(pump['id'])
                elif incoming:
                    pump_selection['in'].append(pump['id'])

        log.info(str(flow_lines))
        return flow_lines, pump_selection

    def get_nodes(self, wb_polygon, model_part):
        """Returns a dictionary with node ids by category:

        {
            '1d': [..., ...],
            '2d': [..., ...],
            '2d_groundwater': [..., ...],
        }
        """

        log.info('polygon of wb area: %s', wb_polygon.asWkt())

        nodes = {
            '1d': [],
            '2d': [],
            '2d_groundwater': [],
        }

        lines, points, pumps = self.ts_datasource.rows[0].get_result_layers()

        # use bounding box and spatial index to prefilter lines
        request_filter = QgsFeatureRequest().setFilterRect(
            wb_polygon.get().boundingBox())
        if model_part == '1d':
            request_filter.setFilterExpression(u'"type" = \'1d\'')
        elif model_part == '2d':
            request_filter.setFilterExpression(
                u'"type" = \'2d\' OR "type" = \'2d_groundwater\'')
        else:
            request_filter.setFilterExpression(
                u'"type" = \'1d\' OR "type" '
                u'= \'2d\' OR "type" = \'2d_groundwater\'')
        # todo: check if boundary nodes could not have rain, infiltration, etc.

        for point in points.getFeatures(request_filter):
            # test if points are contained by polygon
            if wb_polygon.contains(point.geometry()):
                _type = point['type']
                nodes[_type].append(point['id'])

        return nodes

    def get_aggregated_flows(self, link_ids, pump_ids, node_ids, model_part):
        """
        Returns a tuple (ts, total_time) defined as:

            ts = array of timestamps
            total_time = array with shape (np.size(ts, 0), len(INPUT_SERIES))
        """
        # constants referenced in record array
        # shared by links and nodes
        TYPE_1D = '1d'
        TYPE_2D = '2d'
        TYPE_2D_GROUNDWATER = '2d_groundwater'
        # links only
        TYPE_1D_BOUND_IN = '1d_bound_in'
        TYPE_2D_BOUND_IN = '2d_bound_in'
        TYPE_1D__1D_2D_EXCH = '1d__1d_2d_exch'
        TYPE_2D__1D_2D_EXCH = '2d__1d_2d_exch'
        TYPE_1D__1D_2D_FLOW = '1d__1d_2d_flow'
        TYPE_2D__1D_2D_FLOW = '2d__1d_2d_flow'
        TYPE_2D_VERTICAL_INFILTRATION = '2d_vertical_infiltration'

        ALL_TYPES = [
            TYPE_1D, TYPE_2D, TYPE_2D_GROUNDWATER, TYPE_1D_BOUND_IN,
            TYPE_2D_BOUND_IN, TYPE_1D__1D_2D_EXCH, TYPE_2D__1D_2D_EXCH,
            TYPE_1D__1D_2D_FLOW, TYPE_2D__1D_2D_FLOW,
            TYPE_2D_VERTICAL_INFILTRATION,
        ]

        NTYPE_MAXLEN = 25
        assert max(list(map(len, ALL_TYPES))) <= NTYPE_MAXLEN, \
            "NTYPE_MAXLEN insufficiently large for all values"
        NTYPE_DTYPE = 'U%s' % NTYPE_MAXLEN

        # LINKS
        #######

        # create numpy table with flowlink information
        tlink = []  # id, 1d or 2d, in or out
        for idx in link_ids['2d_in']:
            tlink.append((idx, TYPE_2D, 1))
        for idx in link_ids['2d_out']:
            tlink.append((idx, TYPE_2D, -1))

        for idx in link_ids['2d_bound_in']:
            tlink.append((idx, TYPE_2D_BOUND_IN, 1))
        for idx in link_ids['2d_bound_out']:
            tlink.append((idx, TYPE_2D_BOUND_IN, -1))

        for idx in link_ids['1d_in']:
            tlink.append((idx, TYPE_1D, 1))
        for idx in link_ids['1d_out']:
            tlink.append((idx, TYPE_1D, -1))

        for idx in link_ids['1d_bound_in']:
            tlink.append((idx, TYPE_1D_BOUND_IN, 1))
        for idx in link_ids['1d_bound_out']:
            tlink.append((idx, TYPE_1D_BOUND_IN, -1))

        for idx in link_ids['2d_groundwater_in']:
            tlink.append((idx, TYPE_2D_GROUNDWATER, 1))
        for idx in link_ids['2d_groundwater_out']:
            tlink.append((idx, TYPE_2D_GROUNDWATER, -1))

        for idx in link_ids['2d_vertical_infiltration']:
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
        for idx in link_ids['1d__1d_2d_flow']:
            tlink.append((idx, TYPE_1D__1D_2D_FLOW, -1))
        # 1d_2d_out: 1d node is outside polygon, 2d node is inside
        for idx in link_ids['2d__1d_2d_flow']:
            tlink.append((idx, TYPE_2D__1D_2D_FLOW, 1))
        # 1d_2d within the polygon (from 1d perspective so everything flipped)
        for idx in link_ids['1d_2d_exch']:
            tlink.append((idx, TYPE_1D__1D_2D_EXCH, -1))
        # 1d_2d within the polygon (from 2d perspective)
        for idx in link_ids['1d_2d_exch']:
            tlink.append((idx, TYPE_2D__1D_2D_EXCH, 1))

        np_link = np.array(
            tlink, dtype=[('id', int), ('ntype', NTYPE_DTYPE), ('dir', int)])

        # sort for faster reading of netcdf
        np_link.sort(axis=0)

        # create masks
        mask_2d = np_link['ntype'] != TYPE_2D
        mask_1d = np_link['ntype'] != TYPE_1D
        mask_2d_bound = np_link['ntype'] != TYPE_2D_BOUND_IN
        mask_1d_bound = np_link['ntype'] != TYPE_1D_BOUND_IN

        mask_1d__1d_2d_flow = np_link['ntype'] != TYPE_1D__1D_2D_FLOW
        mask_2d__1d_2d_flow = np_link['ntype'] != TYPE_2D__1D_2D_FLOW
        mask_1d__1d_2d_exch = np_link['ntype'] != TYPE_1D__1D_2D_EXCH
        mask_2d__1d_2d_exch = np_link['ntype'] != TYPE_2D__1D_2D_EXCH
        mask_2d_groundwater = np_link['ntype'] != TYPE_2D_GROUNDWATER
        mask_2d_vertical_infiltration = np_link['ntype'] != \
            TYPE_2D_VERTICAL_INFILTRATION

        ds = self.ts_datasource.rows[0].datasource()

        # get all flows through incoming and outgoing flows
        ts = ds.get_timestamps(parameter='q_cum')

        len_input_series = len(WaterBalanceWidget.INPUT_SERIES)
        total_time = np.zeros(shape=(np.size(ts, 0), len_input_series))
        # total_location = np.zeros(shape=(np.size(np_link, 0), 2))

        # non-2d links
        pos_pref = 0
        neg_pref = 0

        if np_link.size > 0:
            for ts_idx, t in enumerate(ts):
                # (1) inflow and outflow through 1d and 2d
                # vol = ds.get_values_by_timestep_nr('q', ts_idx,
                # np_link['id']) * np_link['dir']  # * dt

                flow_pos = ds.get_values_by_timestep_nr(
                    'q_cum_positive', ts_idx, np_link['id']) * np_link[
                               'dir']
                flow_neg = ds.get_values_by_timestep_nr(
                    'q_cum_negative', ts_idx, np_link['id']) * np_link[
                               'dir'] * -1

                in_sum = flow_pos - pos_pref
                out_sum = flow_neg - neg_pref
                pos_pref = flow_pos
                neg_pref = flow_neg

                # 2d flow (2d_in)
                total_time[ts_idx, 0] = ma.masked_array(
                    in_sum, mask=mask_2d).clip(min=0).sum() + ma.masked_array(
                    out_sum, mask=mask_2d).clip(min=0).sum()
                # 2d flow (2d_out)
                total_time[ts_idx, 1] = ma.masked_array(
                    in_sum, mask=mask_2d).clip(max=0).sum() + ma.masked_array(
                    out_sum, mask=mask_2d).clip(max=0).sum()

                # 1d flow (1d_in)
                total_time[ts_idx, 2] = ma.masked_array(
                    in_sum, mask=mask_1d).clip(min=0).sum() + ma.masked_array(
                    out_sum, mask=mask_1d).clip(min=0).sum()
                # 1d flow (1d_out)
                total_time[ts_idx, 3] = ma.masked_array(
                    in_sum, mask=mask_1d).clip(max=0).sum() + ma.masked_array(
                    out_sum, mask=mask_1d).clip(max=0).sum()

                # 2d bound (2d_bound_in)
                total_time[ts_idx, 4] = ma.masked_array(
                    in_sum, mask=mask_2d_bound).clip(
                    min=0).sum() + ma.masked_array(
                    out_sum, mask=mask_2d_bound).clip(min=0).sum()
                # 2d bound (2d_bound_out)
                total_time[ts_idx, 5] = ma.masked_array(
                    in_sum, mask=mask_2d_bound).clip(
                    max=0).sum() + ma.masked_array(
                    out_sum, mask=mask_2d_bound).clip(max=0).sum()

                # 1d bound (1d_bound_in)
                total_time[ts_idx, 6] = ma.masked_array(
                    in_sum, mask=mask_1d_bound).clip(
                    min=0).sum() + ma.masked_array(
                    out_sum, mask=mask_1d_bound).clip(min=0).sum()
                # 1d bound (1d_bound_out)
                total_time[ts_idx, 7] = ma.masked_array(
                    in_sum, mask=mask_1d_bound).clip(
                    max=0).sum() + ma.masked_array(
                    out_sum, mask=mask_1d_bound).clip(max=0).sum()

                # 1d__1d_2d_flow_in
                total_time[ts_idx, 8] = ma.masked_array(
                    in_sum, mask=mask_1d__1d_2d_flow).clip(
                    min=0).sum() + ma.masked_array(
                    out_sum, mask=mask_1d__1d_2d_flow).clip(min=0).sum()
                # 1d__1d_2d_flow_out
                total_time[ts_idx, 9] = ma.masked_array(
                    in_sum, mask=mask_1d__1d_2d_flow).clip(
                    max=0).sum() + ma.masked_array(
                    out_sum, mask=mask_1d__1d_2d_flow).clip(max=0).sum()

                # 2d__1d_2d_flow_in
                total_time[ts_idx, 30] = ma.masked_array(
                    in_sum, mask=mask_2d__1d_2d_flow).clip(
                    min=0).sum() + ma.masked_array(
                    out_sum, mask=mask_2d__1d_2d_flow).clip(min=0).sum()
                # 2d__1d_2d_flow_out
                total_time[ts_idx, 31] = ma.masked_array(
                    in_sum, mask=mask_2d__1d_2d_flow).clip(
                    max=0).sum() + ma.masked_array(
                    out_sum, mask=mask_2d__1d_2d_flow).clip(max=0).sum()

                # 1d (1d__1d_2d_exch_in)
                total_time[ts_idx, 10] = ma.masked_array(
                    in_sum, mask=mask_1d__1d_2d_exch).clip(
                    min=0).sum() + ma.masked_array(
                    out_sum, mask=mask_1d__1d_2d_exch).clip(min=0).sum()
                # 1d (1d__1d_2d_exch_out)
                total_time[ts_idx, 11] = ma.masked_array(
                    in_sum, mask=mask_1d__1d_2d_exch).clip(
                    max=0).sum() + ma.masked_array(
                    out_sum, mask=mask_1d__1d_2d_exch).clip(max=0).sum()

                # 2d (2d__1d_2d_exch_in)
                total_time[ts_idx, 32] = ma.masked_array(
                    in_sum, mask=mask_2d__1d_2d_exch).clip(
                    min=0).sum() + ma.masked_array(
                    out_sum, mask=mask_2d__1d_2d_exch).clip(min=0).sum()
                # 2d (2d__1d_2d_exch_out)
                total_time[ts_idx, 33] = ma.masked_array(
                    in_sum, mask=mask_2d__1d_2d_exch).clip(
                    max=0).sum() + ma.masked_array(
                    out_sum, mask=mask_2d__1d_2d_exch).clip(max=0).sum()

                # 2d groundwater (2d_groundwater_in)
                total_time[ts_idx, 23] = ma.masked_array(
                    in_sum, mask=mask_2d_groundwater).clip(
                    min=0).sum() + ma.masked_array(
                    out_sum, mask=mask_2d_groundwater).clip(min=0).sum()
                # 2d groundwater (2d_groundwater_out)
                total_time[ts_idx, 24] = ma.masked_array(
                    in_sum, mask=mask_2d_groundwater).clip(
                    max=0).sum() + ma.masked_array(
                    out_sum, mask=mask_2d_groundwater).clip(max=0).sum()

                # NOTE: positive vertical infiltration is from surface to
                # groundwater node. We make this negative because it's
                # 'sink-like', and to make it in line with the
                # infiltration_rate_simple which also has a -1 multiplication
                # factor.
                # 2d_vertical_infiltration (2d_vertical_infiltration_pos)
                total_time[ts_idx, 28] = -1 * ma.masked_array(
                    in_sum, mask=mask_2d_vertical_infiltration).clip(
                    min=0).sum() + ma.masked_array(
                    out_sum, mask=mask_2d_vertical_infiltration).clip(
                    min=0).sum()
                # 2d_vertical_infiltration (2d_vertical_infiltration_neg)
                total_time[ts_idx, 29] = -1 * ma.masked_array(
                    in_sum, mask=mask_2d_vertical_infiltration).clip(
                    max=0).sum() + ma.masked_array(
                    out_sum, mask=mask_2d_vertical_infiltration).clip(
                    max=0).sum()

        # PUMPS
        #######

        tpump = []
        for idx in pump_ids['in']:
            tpump.append((idx, 1))
        for idx in pump_ids['out']:
            tpump.append((idx, -1))
        np_pump = np.array(tpump, dtype=[('id', int), ('dir', int)])
        np_pump.sort(axis=0)

        if np_pump.size > 0:
            # pumps
            pump_pref = 0
            for ts_idx, t in enumerate(ts):
                # (2) inflow and outflow through pumps
                pump_flow = ds.get_values_by_timestep_nr(
                    'q_pump_cum', ts_idx, np_pump['id']) * np_pump['dir']

                flow_dt = pump_flow - pump_pref
                pump_pref = pump_flow

                in_sum = flow_dt.clip(min=0)
                out_sum = flow_dt.clip(max=0)

                total_time[ts_idx, 12] = in_sum.sum()
                total_time[ts_idx, 13] = out_sum.sum()

        # NODES
        #######

        tnode = []  # id, 1d or 2d, in or out
        for idx in node_ids['2d']:
            tnode.append((idx, TYPE_2D))
        for idx in node_ids['1d']:
            tnode.append((idx, TYPE_1D))
        for idx in node_ids['2d_groundwater']:
            tnode.append((idx, TYPE_2D_GROUNDWATER))
        NTYPE_DTYPE
        np_node = np.array(tnode,
                           dtype=[('id', int), ('ntype', NTYPE_DTYPE)])
        np_node.sort(axis=0)

        mask_2d_nodes = np_node['ntype'] != TYPE_2D
        mask_1d_nodes = np_node['ntype'] != TYPE_1D
        mask_2d_groundwater_nodes = np_node[
                                        'ntype'] != TYPE_2D_GROUNDWATER

        np_2d_node = ma.masked_array(
            np_node['id'], mask=mask_2d_nodes).compressed()
        np_1d_node = ma.masked_array(
            np_node['id'], mask=mask_1d_nodes).compressed()
        np_2d_groundwater_node = ma.masked_array(
            np_node['id'], mask=mask_2d_groundwater_nodes).compressed()

        for parameter, agg_method, node, pnr, factor in [
            ('rain', '_cum', np_2d_node, 14, 1),
            # TODO: in old model results this parameter is called
            # 'infiltration_rate', thus it is not backwards compatible right
            # now
            ('infiltration_rate_simple', '_cum', np_2d_node, 15, -1),
            # TODO: inefficient because we look up q_lat data twice
            ('q_lat', '_cum', np_2d_node, 16, 1),
            ('q_lat', '_cum', np_1d_node, 17, 1),
            ('leak', '_cum', np_2d_groundwater_node, 26, 1),
            ('rain', '_cum', np_1d_node, 27, 1),
            ('intercepted_volume', '_current', np_2d_node, 34, -1),
            ('q_sss', '_cum', np_2d_node, 35, 1),

        ]:

            if node.size > 0:
                if parameter + agg_method in ds.get_available_variables():
                    values_pref = 0
                    for ts_idx, t in enumerate(ts):
                        values = ds.get_values_by_timestep_nr(
                            parameter + agg_method, ts_idx, node).sum()
                        values_dt = values - values_pref
                        values_pref = values
                        total_time[ts_idx, pnr] = values_dt * factor
        t_pref = 0

        for ts_idx, t in enumerate(ts):
            if ts_idx == 0:
                # just to make sure machine precision distortion
                # is reduced for the first timestamp (everything
                # should be 0
                total_time[ts_idx] = total_time[ts_idx] / (ts[1] - t)
            else:
                total_time[ts_idx] = total_time[ts_idx] / (t - t_pref)
                t_pref = t

        if np_node.size > 0:
            # delta volume
            t_pref = 0
            vol_pref = 0
            for ts_idx, t in enumerate(ts):
                # delta volume
                if ts_idx == 0:
                    # volume difference first timestep is always 0
                    total_time[ts_idx, 18] = 0
                    total_time[ts_idx, 19] = 0
                    total_time[ts_idx, 25] = 0

                    vol_current = ds.get_values_by_timestep_nr(
                        'vol_current', ts_idx, np_node['id'])
                    td_vol_pref = ma.masked_array(
                        vol_current, mask=mask_2d_nodes).sum()
                    od_vol_pref = ma.masked_array(
                        vol_current, mask=mask_1d_nodes).sum()
                    td_vol_pref_gw = ma.masked_array(
                        vol_current,
                        mask=mask_2d_groundwater_nodes).sum()
                    t_pref = t
                else:
                    vol_ts_idx = ts_idx

                    ts_normal = ds.get_timestamps(
                        parameter='vol_current')
                    vol_ts_idx = np.nonzero(ts_normal == t)[0]

                    vol_current = ds.get_values_by_timestep_nr(
                        'vol_current', vol_ts_idx, np_node['id'])

                    td_vol = ma.masked_array(
                        vol_current, mask=mask_2d_nodes).sum()
                    od_vol = ma.masked_array(
                        vol_current, mask=mask_1d_nodes).sum()
                    td_vol_gw = ma.masked_array(
                        vol_current,
                        mask=mask_2d_groundwater_nodes).sum()

                    dt = t - t_pref
                    total_time[ts_idx, 18] = (td_vol - td_vol_pref) / dt
                    total_time[ts_idx, 19] = (od_vol - od_vol_pref) / dt
                    total_time[ts_idx, 25] = (td_vol_gw - td_vol_pref_gw) / dt

                    td_vol_pref = td_vol
                    od_vol_pref = od_vol
                    td_vol_pref_gw = td_vol_gw
                    t_pref = t
        total_time = np.nan_to_num(total_time)

        return ts, total_time


class WaterBalanceTool(object):
    """QGIS Plugin Implementation."""

    def __init__(self, iface, ts_datasource):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.ts_datasource = ts_datasource

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.icon_path = \
            ':/plugins/ThreeDiToolbox/icons/weight-scale.png'
        self.menu_text = u'Water Balance Tool'

        self.plugin_is_active = False
        self.widget = None

        self.toolbox = None

    def on_unload(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        if self.widget is not None:
            self.widget.close()

    def on_close_child_widget(self):
        """Cleanup necessary items here when plugin widget is closed"""
        self.widget.closingWidget.disconnect(self.on_close_child_widget)
        self.widget = None
        self.plugin_is_active = False

    def pop_up_no_agg_found(self):
        header = 'Error: No aggregation netcdf found'
        msg = "The WaterBalanceTool requires an 'aggregate_results_3di.nc' " \
              "but this file could not be found. Please make sure you run " \
              "your simulation using the 'v2_aggregation_settings' table " \
              "with the following variables:" \
              "\n\ncurrent:" \
              "\n- volume" \
              "\n- interception (in case model has interception)" \
              "\n\ncumulative:"\
              "\n- rain"\
              "\n- discharge"\
              "\n- leakage (in case model has leakage)" \
              "\n- laterals (in case model has laterals)"\
              "\n- pump discharge (in case model has pumps)" \
              "\n- simple_infiltration (in case model has " \
              "simple_infiltration)" \
              "\n- sources and sinks (in case model has sources and sinks)"\
              "\n\npositive cumulative:" \
              "\n- discharge"\
              "\n\nnegative cumulative:" \
              "\n- discharge"
        QMessageBox.warning(None, header, msg)

    def pop_up_missing_agg_vars(self):
        header = 'Error: Missing aggregation settings'
        missing_vars = self.get_missing_agg_vars()
        msg = "The WaterBalanceTool found the 'aggregate_results_3di.nc' but "\
              "the file does not include all required aggregation " \
              "variables. Please add them to the sqlite table " \
              "'v2_aggregation_settings' and run your simulation again. The " \
              "required variables are:" \
              "\n\ncurrent:" \
              "\n- volume" \
              "\n- interception (in case model has interception)" \
              "\n\ncumulative:"\
              "\n- rain"\
              "\n- discharge"\
              "\n- leakage (in case model has leakage)" \
              "\n- laterals (in case model has laterals)"\
              "\n- pump discharge (in case model has pumps)" \
              "\n- simple_infiltration (in case model has " \
              "simple_infiltration)" \
              "\n- sources and sinks (in case model has sources and sinks)" \
              "\n\npositive cumulative:" \
              "\n- discharge"\
              "\n\nnegative cumulative:" \
              "\n- discharge" \
              "\n\nYour aggregation .nc misses the following variables:\n" + \
              ', '.join(missing_vars)
        QMessageBox.warning(None, header, msg)

    def get_missing_agg_vars(self):
        """Returns a list with tuples of aggregation vars (vol, discharge) +
        methods (cum, current, etc) that are not (but should be) in the
        v2_aggregation_settings

        1.  some vars_methods are always required: minimum_agg_vars
        2.  some vars methods are required when included in the model
            schematisation (e.g. pumps, laterals).
        """

        selected_ds = self.ts_datasource.rows[0].datasource()
        check_available_vars = selected_ds.get_available_variables()

        ga = self.ts_datasource.rows[0].datasource().gridadmin
        gr = self.ts_datasource.rows[0].datasource().gridadmin_result

        minimum_agg_vars = [
            ('q_cum_negative', 'negative cumulative discharge'),
            ('q_cum_positive', 'negative cumulative discharge'),
            ('q_cum', 'cumulative discharge'),
            ('vol_current', 'current volume')
            ]

        # some vars must be aggregated when included in the model
        # schematisation (e.g. pumps, laterals). problem is that threedigrid
        # does not support e.g. ga.has_lateral, ga.has_leakage etc. For those
        # fields, we read the threedigrid metadata.
        simulated_vars_nodes = ga.nodes._meta.get_fields(only_names=True)

        if gr.has_pumpstations:
            to_add = ('q_pump_cum', 'cumulative pump discharge')
            minimum_agg_vars.append(to_add)

        # TODO: wait for threedigrid's e.g. 'gr.has_rained')
        # u'rain' is always in simulated_vars_nodes. So it does not make sense
        # to check there. Thus, we're gonna read the nc's rain data
        if np.nanmax(gr.nodes.rain) > 0:
            to_add = ('rain_cum', 'cumulative rain')
            minimum_agg_vars.append(to_add)

        # gr.has_simple_infiltration and gr.has_interception are added to
        # threedigrid some months after groundwater release. To coop with the
        # .h5 that has been created in that period we use the meta data
        try:
            if gr.has_simple_infiltration:
                to_add = ('infiltration_rate_simple_cum',
                          'cumulative infiltration rate')
                minimum_agg_vars.append(to_add)
        except AttributeError:
            if 'infiltration' in simulated_vars_nodes:
                to_add = ('infiltration_rate_simple_cum',
                          'cumulative infiltration rate')
                minimum_agg_vars.append(to_add)

        try:
            if gr.has_interception:
                to_add = ('intercepted_volume_current', 'current interception')
                minimum_agg_vars.append(to_add)
        except AttributeError:
            # gr.has_interception is added to threedigrid some months after
            # groundwater release. To coop with .h5 that has been created in
            # that period we read the simulated_vars_nodes
            if 'intercepted_volume' in simulated_vars_nodes:
                to_add = ('intercepted_volume_current', 'current interception')
                minimum_agg_vars.append(to_add)

        if 'q_lat' in simulated_vars_nodes:
            to_add = ('q_lat_cum', 'cumulative lateral discharge')
            minimum_agg_vars.append(to_add)

        if 'leak' in simulated_vars_nodes:
            to_add = ('leak_cum', 'cumulative leakage')
            minimum_agg_vars.append(to_add)

        if 'q_sss' in gr.nodes.Meta.subset_fields.keys():
            if np.count_nonzero(gr.nodes.timeseries(
                    indexes=slice(0, -1)).q_sss) > 0:
                minimum_agg_vars.append(('q_sss_cum', 'cumulative surface '
                                                      'sources and sinks'))

        missing_vars = []
        for required_var in minimum_agg_vars:
            if required_var[0] not in check_available_vars:
                msg = 'the aggregation nc misses aggregation: %s', \
                      required_var[1]
                log.error(msg)
                missing_vars.append(required_var[1])
        return missing_vars

    def run(self):
        selected_ds = self.ts_datasource.rows[0].datasource()
        if not selected_ds.ds_aggregation:
            self.pop_up_no_agg_found()
        elif self.get_missing_agg_vars():
            self.pop_up_missing_agg_vars()
        else:
            self.run_it()

    def run_it(self):
        """Run_it method that loads and starts the plugin"""

        if not self.plugin_is_active:
            self.plugin_is_active = True

            if self.widget is None:
                # Create the widget (after translation) and keep reference
                self.widget = WaterBalanceWidget(
                    iface=self.iface,
                    ts_datasource=self.ts_datasource,
                    wb_calc=WaterBalanceCalculation(self.ts_datasource))

            # connect to provide cleanup on closing of widget
            self.widget.closingWidget.connect(self.on_close_child_widget)

            # show the #widget
            self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.widget)

            self.widget.show()
