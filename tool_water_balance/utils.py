from qgis.core import QgsCoordinateTransform
from qgis.core import QgsGeometry
from qgis.core import QgsProject


class PolygonWithCRS:
    def __init__(self, polygon, crs):
        self.polygon = polygon
        self.crs = crs

    def transformed(self, crs):
        polygon = QgsGeometry(self.polygon)
        qct = QgsCoordinateTransform(self.crs, crs, QgsProject.instance())
        polygon.transform(qct)
        return polygon
