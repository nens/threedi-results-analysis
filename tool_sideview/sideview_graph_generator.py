from pathlib import Path
from qgis.core import QgsVectorLayer, QgsFeature
from qgis.core import QgsGeometry, QgsPointXY, QgsField
from threedigrid.admin.gridadmin import GridH5Admin
from threedi_results_analysis.tool_sideview.utils import LineType
from qgis.PyQt.QtCore import QVariant

import logging
logger = logging.getLogger(__name__)


class SideViewGraphGenerator():
    """Generates a graph based on a gridadmin file"""

    @staticmethod
    def generate(gridadmin_file: Path) -> QgsVectorLayer:
        logger.error(f"Calculating layer from {gridadmin_file}")

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
    #             QgsField("end_node_idx", QVariant.Int),
    # # #         # This is the flowline index in Python (0-based indexing)
    # # #         # Important: this differs from the feature id which is flowline
    # # #         # idx+1!!
    # # #         QgsField("nr", QVariant.Int),
    #             # QgsField("start_node", QVariant.String),
    #             # QgsField("end_node", QVariant.String),
    # # #         QgsField("channel_id", QVariant.Int),
    # # #         QgsField("sub_channel_nr", QVariant.Int),
    # # #         QgsField("start_channel_distance", QVariant.Double),
    #         ]
    #     )

        # Tell the vector layer to fetch changes from the provider
        graph_layer.updateFields()

        # Retrieve lines from gridadmin
        ga = GridH5Admin(gridadmin_file.with_suffix('.h5'))

        features = []
        lines_1d = ga.lines.subset("1D")
        distances_1d = lines_1d.ds1d.tolist()  # tolist converts to native python floats
        line_coords = lines_1d.line_coords.transpose()
        line_ids = lines_1d.id.tolist()
        nodes_ids = lines_1d.line.transpose().tolist()
        content_types = lines_1d.content_type.tolist()
        invert_level_start_points = lines_1d.invert_level_start_point.tolist()
        invert_level_end_points = lines_1d.invert_level_end_point.tolist()
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
            # TODO: Retrieve cross section
            start_height = 3.0
            end_height = 3.0

            line_type = SideViewGraphGenerator.content_type_to_line_type(content_types[count].decode())

            if line_type == LineType.PIPE:
                start_level = invert_level_start_points[count]
                end_level = invert_level_end_points[count]
            elif line_type == LineType.CULVERT:
                start_level = invert_level_start_points[count]
                end_level = invert_level_end_points[count]
            elif line_type == LineType.ORIFICE:
                crest_level = lines_1d.orifices.filter(id=line_ids[count]).crest_level[0].item()
                start_level = crest_level
                end_level = crest_level
            elif line_type == LineType.WEIR:
                crest_level = lines_1d.weirs.filter(id=line_ids[count]).crest_level[0].item()
                start_level = crest_level
                end_level = crest_level
            elif line_type == LineType.CHANNEL:
                reference_level = lines_1d.channels.filter(id=line_ids[count]).dpumax[0].item()
                start_level = reference_level
                end_level = reference_level

            # Note that id (count) is the flowline index in Python (0-based indexing)
            feat.setAttributes([count, nodes_ids[count][0], nodes_ids[count][1], distances_1d[count], line_type, start_level, end_level, start_height, end_height])
            features.append(feat)
            last_index = count

        # Pumps are not part of lines, add as well.
        pump_coords = ga.pumps.node_coordinates.transpose()[1:].tolist()  # drop nan-element
        node1_ids = ga.pumps.node1_id[1:].tolist()
        node2_ids = ga.pumps.node2_id[1:].tolist()
        for count, pump_coord in enumerate(pump_coords):
            feat = QgsFeature()

            p1 = QgsPointXY(pump_coord[0], pump_coord[1])
            p2 = QgsPointXY(pump_coord[2], pump_coord[3])
            geom = QgsGeometry.fromPolylineXY([p1, p2])
            feat.setGeometry(geom)

            feat.setAttributes([count+last_index, node1_ids[count], node2_ids[count], None, LineType.PUMP, start_level, end_level, start_height, end_height])
            features.append(feat)

        if not pr.addFeatures(features):
            logger.error(f"Unable to add all features: {pr.lastError()}")
        graph_layer.updateExtents()
        return graph_layer

    @staticmethod
    def content_type_to_line_type(content_type: str) -> int:
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
