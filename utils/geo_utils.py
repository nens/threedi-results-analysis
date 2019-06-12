# (c) Nelen & Schuurmans, see LICENSE.rst.

from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsCoordinateTransform
from qgis.core import QgsProject


def get_coord_transformation_instance(src_epsg, dest_epsg):
    """
    :param src_epsg: epsg code of the source geometry
    :param dest_epsg: epsg code to transform to
    """
    src_crs = QgsCoordinateReferenceSystem(int(src_epsg))
    dest_crs = QgsCoordinateReferenceSystem(int(dest_epsg))
    return QgsCoordinateTransform(src_crs, dest_crs, QgsProject.instance())
