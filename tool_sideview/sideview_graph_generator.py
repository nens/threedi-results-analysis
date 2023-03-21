from pathlib import Path
from qgis.core import QgsVectorLayer, QgsField, QgsFeature
from qgis.core import QgsGeometry, QgsPointXY, QgsProject
from qgis.PyQt.QtCore import QVariant
from threedigrid.admin.gridadmin import GridH5Admin

import logging
logger = logging.getLogger(__name__)

class SideViewGraphGenerator():
    """Generates a graph based on a gridadmin file"""

    @staticmethod
    def generate(self, gridadmin: Path) -> QgsVectorLayer:
        logger.error("Calculating layer")

        graph_layer = QgsVectorLayer("LineString?crs=epsg:4326&index=yes", "yoyo", "memory")
        pr = graph_layer.dataProvider()

        # pr.addAttributes(
        #     [
        #         # This is the flowline index in Python (0-based indexing)
        #         # Important: this differs from the feature id which is flowline
        #         # idx+1!!
        #         QgsField("nr", QVariant.Int),
        #         QgsField("id", QVariant.String, len=25),
        #         QgsField("type", QVariant.Int),
        #         QgsField("start_node", QVariant.String),
        #         QgsField("end_node", QVariant.String),
        #         QgsField("start_node_idx", QVariant.Int),
        #         QgsField("end_node_idx", QVariant.Int),
        #         QgsField("start_level", QVariant.Double),
        #         QgsField("end_level", QVariant.Double),
        #         QgsField("start_height", QVariant.Double),
        #         QgsField("end_height", QVariant.Double),
        #         QgsField("channel_id", QVariant.Int),
        #         QgsField("sub_channel_nr", QVariant.Int),
        #         QgsField("start_channel_distance", QVariant.Double),
        #         QgsField("real_length", QVariant.Double),
        #     ]
        # )
        # tell the vector layer to fetch changes from the provider
        graph_layer.updateFields()

        # Retrieve lines from gridadmin
        ga = GridH5Admin(str(gridadmin))

        features = []
        i = 0
        line_coords = ga.lines.subset("1D_ALL").line_coords.transpose()
        for x_start, y_start, x_end, y_end in line_coords:
            feat = QgsFeature()

            p1 = QgsPointXY(x_start, y_start)
            p2 = QgsPointXY(x_end, y_end)

            geom = QgsGeometry.fromPolylineXY([p1, p2])
            # geom = line.get('geom', QgsGeometry.fromPolyline([p1, p2]))

            feat.setGeometry(geom)
            # Casting ids to strings is needed due to issue with casting values in memory layers in QGIS < 3.16.6
            # feat.setAttributes(
            #     [
            #         i,
            #         str(line["id"]),
            #         line["type"],
            #         str(line["start_node"]),
            #         str(line["end_node"]),
            #         line.get("start_node_idx", None),
            #         line.get("end_node_idx", None),
            #         line.get("start_level", None),
            #         line.get("end_level", None),
            #         line.get("start_height", None),
            #         line.get("end_height", None),
            #         line.get("channel_id", None),
            #         line.get("sub_channel_nr", None),
            #         line.get("start_channel_distance", None),
            #         line.get("real_length", None),
            #     ]
            # )
            features.append(feat)
            i += 1

        pr.addFeatures(features)
        graph_layer.updateExtents()

        QgsProject.instance().addMapLayer(graph_layer)