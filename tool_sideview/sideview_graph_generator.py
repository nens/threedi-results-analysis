from pathlib import Path
from qgis.core import QgsVectorLayer, QgsFeature
from qgis.core import QgsGeometry, QgsPointXY, QgsField
from threedigrid.admin.gridadmin import GridH5Admin
from threedi_results_analysis.tool_sideview.utils import LineType
from threedi_results_analysis.tool_sideview.cross_section_utils import CrossSectionShape
from qgis.PyQt.QtCore import QVariant
import numpy as np
import statistics
import math
import logging
logger = logging.getLogger(__name__)


class SideViewGraphGenerator():
    """Generates a graph based on a gridadmin file"""

    @staticmethod
    def generate_layer(gridadmin_file: Path) -> QgsVectorLayer:
        graph_layer = QgsVectorLayer("LineString?crs=EPSG:28992&index=yes", "graph_layer", "memory")
        pr = graph_layer.dataProvider()

        pr.addAttributes([QgsField("id", QVariant.Int),
                          QgsField("start_node_idx", QVariant.Int),
                          QgsField("end_node_idx", QVariant.Int),
                          QgsField("real_length", QVariant.Double),
                          QgsField("type", QVariant.Int),
                          QgsField("start_level", QVariant.Double),
                          QgsField("end_level", QVariant.Double),
                          QgsField("start_height", QVariant.Double),
                          QgsField("end_height", QVariant.Double)])

        # Tell the vector layer to fetch changes from the provider
        graph_layer.updateFields()

        # Retrieve lines from gridadmin
        ga = GridH5Admin(gridadmin_file.with_suffix('.h5'))

        features = []
        lines_1d = ga.lines.subset("1D")
        lines_1d2d = ga.lines.subset("1D2D")

        distances_1d = lines_1d.ds1d.tolist()  # tolist converts to native python floats
        line_coords = lines_1d.line_coords.transpose()
        line_ids = lines_1d.id.tolist()
        line_pks = lines_1d.content_pk.tolist()
        nodes_ids = lines_1d.line.transpose().tolist()
        content_types = lines_1d.content_type.tolist()
        invert_level_start_points = lines_1d.invert_level_start_point.tolist()
        invert_level_end_points = lines_1d.invert_level_end_point.tolist()
        cross1_ids = lines_1d.cross1.tolist()
        cross2_ids = lines_1d.cross2.tolist()
        assert len(distances_1d) == len(line_coords)
        assert len(nodes_ids) == len(line_coords)
        assert len(nodes_ids) == len(content_types)
        assert len(nodes_ids) == len(invert_level_start_points)
        assert len(nodes_ids) == len(invert_level_end_points)
        assert len(nodes_ids) == len(line_ids)

        # As we already subset the list, we do not need to skip the first nan-element
        last_index = 0
        for count, (x_start, y_start, x_end, y_end) in enumerate(line_coords):
            feat = QgsFeature()

            p1 = QgsPointXY(x_start, y_start)
            p2 = QgsPointXY(x_end, y_end)
            geom = QgsGeometry.fromPolylineXY([p1, p2])
            feat.setGeometry(geom)

            start_level = None
            end_level = None
            start_height = None
            end_height = None

            line_type = SideViewGraphGenerator.content_type_to_line_type(content_types[count].decode())

            if line_type == LineType.PIPE or line_type == LineType.CULVERT:
                start_level = invert_level_start_points[count]
                end_level = invert_level_end_points[count]
                cross1 = cross1_ids[count]
                cross2 = cross2_ids[count]
                assert cross1 == cross2  # pipes and culverts have only one cross section definition

                cross_section = ga.cross_sections.filter(id=cross1)
                assert ga.cross_sections.id[cross1] == cross_section.id[0]
                try:
                    height = SideViewGraphGenerator.cross_section_max_height(cross_section, ga.cross_sections.tables, nodes_ids[count][0], nodes_ids[count][1], lines_1d2d, ga.nodes, ga.has_2d)
                except AttributeError:
                    logger.error(f"Unable to derive height of cross section: {cross_section.id[0]} {cross1} {cross2} with shape {cross_section.shape[0]} for line {line_ids[count]}, count {count}, pk: {line_pks[count]}, type: {line_type}, start_level {start_level}, end_level {end_level}, cs_pk {cross_section.content_pk[0]}, width_1d {cross_section.width_1d[0]}")

                if math.isnan(height):
                    logger.warning(f"Unable to derive cross section height for cross section {cross1}, setting height to 0")
                    height = 0.0
                start_height = height
                end_height = height

            # Note that id (count) is the flowline index in Python (0-based indexing)
            feat.setAttributes([count, nodes_ids[count][0], nodes_ids[count][1], distances_1d[count], line_type, start_level, end_level, start_height, end_height])
            features.append(feat)
            last_index = count  # noqa

        # # Pumps are not part of lines, add as well.
        # pump_coords = ga.pumps.node_coordinates.transpose()[1:].tolist()  # drop nan-element
        # node1_ids = ga.pumps.node1_id[1:].tolist()
        # node2_ids = ga.pumps.node2_id[1:].tolist()

        # # TODO: Retrieve this info
        # start_level = 3.0
        # end_level = 3.0
        # start_height = 3.0
        # end_height = 3.0
        # for count, pump_coord in enumerate(pump_coords):
        #     feat = QgsFeature()

        #     p1 = QgsPointXY(pump_coord[0], pump_coord[1])
        #     p2 = QgsPointXY(pump_coord[2], pump_coord[3])
        #     geom = QgsGeometry.fromPolylineXY([p1, p2])
        #     feat.setGeometry(geom)

        #     feat.setAttributes([count+last_index, node1_ids[count], node2_ids[count], None, LineType.PUMP, start_level, end_level, start_height, end_height])
        #     features.append(feat)

        if not pr.addFeatures(features):
            logger.error(f"Unable to add all features: {pr.lastError()}")
        graph_layer.updateExtents()
        return graph_layer

    @staticmethod
    def generate_nodes(gridadmin_file: Path) -> QgsVectorLayer:
        graph_layer = QgsVectorLayer("Point?crs=EPSG:28992&index=yes", "point_layer", "memory")
        pr = graph_layer.dataProvider()

        pr.addAttributes([QgsField("id", QVariant.Int)])
        graph_layer.updateFields()

        features = []
        ga = GridH5Admin(gridadmin_file.with_suffix('.h5'))
        nodes_1d = ga.nodes.subset("1D")

        node_coords = nodes_1d.coordinates.transpose().tolist()
        node_ids = nodes_1d.id.tolist()
        assert len(node_coords) == len(node_ids)
        for count, (x_pos, y_pos) in enumerate(node_coords):
            feat = QgsFeature()
            p = QgsPointXY(x_pos, y_pos)
            feat.setGeometry(QgsGeometry.fromPointXY(p))
            feat.setAttributes([node_ids[count]])
            features.append(feat)

        if not pr.addFeatures(features):
            logger.error(f"Unable to add all features: {pr.lastError()}")
        graph_layer.updateExtents()
        return graph_layer

    @staticmethod
    def content_type_to_line_type(content_type: str) -> int:
        """Convertes content_type string to LineType enum"""
        content_type = content_type.removeprefix('v2_')
        if content_type == "pipe":
            return LineType.PIPE
        elif content_type == "culvert":
            return LineType.CULVERT
        elif content_type == "orifice":
            return LineType.ORIFICE
        elif content_type == "weir":
            return LineType.WEIR
        elif content_type == "channel":
            return LineType.CHANNEL

        raise AttributeError(f"Unknown content type: {content_type}")

    @staticmethod
    def cross_section_max_height(cross_section, tables, node1_id: int, node2_id: int, lines_1d2d, nodes, has_2d: bool) -> float:
        """Retrieves (or estimates) the height for a cross section using various heuristics.
            Returns nan when estimation not possible. Raises exception when inconsistencies are
            encountered.
        """
        count = cross_section.count[0]
        offset = cross_section.offset[0]
        shape = cross_section.shape[0]
        width_1d = cross_section.width_1d[0]

        if shape == CrossSectionShape.CIRCLE.value:
            assert count == 0
            return width_1d  # for circle width = height
        elif shape in (CrossSectionShape.TABULATED_RECTANGLE.value, CrossSectionShape.TABULATED_TRAPEZIUM.value):
            return max(tables[:, offset:offset+count][1])
        elif shape == CrossSectionShape.OPEN_RECTANGLE.value:
            # In case cross section is OPEN_RECTANGLE, the cross section itself does not have an height.
            # For 1D model (ga.has_2d is False, take drain_level from adjacent nodes)
            if not has_2d:
                height1 = nodes.filter(id=node1_id).drain_level[0]  # Can be nan when not manhole
                height2 = nodes.filter(id=node2_id).drain_level[0]
                return np.nanmean([height1, height2])
            else:
                # For 2D model, take average dpumax from adjacent 1D2D lines (if available)
                nodes_ids = lines_1d2d.line.transpose().tolist()
                dpumax = lines_1d2d.dpumax.tolist()
                assert len(nodes_ids) == len(dpumax)
                dpumax_list = []
                for count, (node1d2d_1, node1d2d_2) in enumerate(nodes_ids):
                    if node1_id == node1d2d_1 or node1_id == node1d2d_2:
                        dpumax_list.append(dpumax[count])
                    if node2_id == node1d2d_1 or node2_id == node1d2d_2:
                        dpumax_list.append(dpumax[count])

                if dpumax_list:
                    return statistics.fmean(dpumax_list)
                else:
                    # Check whether the nodes are manholes and isolated (1), in that
                    # case it is correct that there are no adjacent 1D2D lines
                    if not (nodes.filter(id=node1_id)[0] == 1) and (nodes.filter(id=node2_id)[0] == 1):
                        raise AttributeError(f"Unexpected missing 1D2D lines for cross section: {cross_section.id[0]}")
                    else:
                        return math.nan

        raise AttributeError(f"Unable to derive height of cross section: {cross_section.id[0]} with shape {shape}")
