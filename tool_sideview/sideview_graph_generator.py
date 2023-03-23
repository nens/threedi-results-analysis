from pathlib import Path
from qgis.core import QgsVectorLayer, QgsFeature
from qgis.core import QgsGeometry, QgsPointXY, QgsField
from threedigrid.admin.gridadmin import GridH5Admin
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

        pr.addAttributes([QgsField("id", QVariant.Int), QgsField("start_node_idx", QVariant.Int), QgsField("end_node_idx", QVariant.Int), QgsField("real_length", QVariant.Double)])
    #             QgsField("end_node_idx", QVariant.Int),
    # # #         # This is the flowline index in Python (0-based indexing)
    # # #         # Important: this differs from the feature id which is flowline
    # # #         # idx+1!!
    # # #         QgsField("nr", QVariant.Int),
    #             QgsField("id", QVariant.Int),
    # # #         QgsField("type", QVariant.Int),
    #             # QgsField("start_node", QVariant.String),
    #             # QgsField("end_node", QVariant.String),
    #             QgsField("start_node_idx", QVariant.Int),
    #             QgsField("end_node_idx", QVariant.Int),
    # # #         QgsField("start_level", QVariant.Double),
    # # #         QgsField("end_level", QVariant.Double),
    # # #         QgsField("start_height", QVariant.Double),
    # # #         QgsField("end_height", QVariant.Double),
    # # #         QgsField("channel_id", QVariant.Int),
    # # #         QgsField("sub_channel_nr", QVariant.Int),
    # # #         QgsField("start_channel_distance", QVariant.Double),
    #             QgsField("real_length", QVariant.Double),
    #         ]
    #     )

        # Tell the vector layer to fetch changes from the provider
        graph_layer.updateFields()

        # Retrieve lines from gridadmin
        ga = GridH5Admin(gridadmin_file.with_suffix('.h5'))

        features = []
        distances_1d = ga.lines.subset("1D").ds1d.tolist()  # tolist converts to native python floats
        line_coords = ga.lines.subset("1D").line_coords.transpose()
        nodes_ids = ga.lines.subset("1D").line.transpose().tolist()
        assert len(distances_1d) == len(line_coords)
        assert len(nodes_ids) == len(line_coords)

        # As we already subset the list, we do not need to skip the first nan-element
        last_index = 0
        for count, (x_start, y_start, x_end, y_end) in enumerate(line_coords):
            feat = QgsFeature()

            p1 = QgsPointXY(x_start, y_start)
            p2 = QgsPointXY(x_end, y_end)
            geom = QgsGeometry.fromPolylineXY([p1, p2])
            feat.setGeometry(geom)

            # Note that id is the flowline index in Python (0-based indexing)
            feat.setAttributes([count, nodes_ids[count][0], nodes_ids[count][1], distances_1d[count]])
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

            feat.setAttributes([count+last_index, node1_ids[count], node2_ids[count], None])
            features.append(feat)

        pr.addFeatures(features)
        graph_layer.updateExtents()
        return graph_layer
