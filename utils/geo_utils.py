# (c) Nelen & Schuurmans, see LICENSE.rst.

from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsCoordinateTransform
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.core import QgsField
from qgis.core import QgsWkbTypes


def get_coord_transformation_instance(src_epsg, dest_epsg):
    """
    :param src_epsg: epsg code of the source geometry
    :param dest_epsg: epsg code to transform to
    """
    src_crs = QgsCoordinateReferenceSystem(int(src_epsg))
    dest_crs = QgsCoordinateReferenceSystem(int(dest_epsg))
    return QgsCoordinateTransform(src_crs, dest_crs, QgsProject.instance())


def create_vectorlayer(source_layer: QgsVectorLayer, layer_name: str, additional_attributes) -> QgsVectorLayer:
    """
    Create a new QgsVectorLayer containing the attributes of the base_layer plus the list
    of additional attributes.
    """
    source_provider = source_layer.dataProvider()

    uri = "{0}?crs=EPSG:{1}".format(
        QgsWkbTypes.displayString(source_provider.wkbType()).lstrip("WKB"),
        str(source_provider.crs().postgisSrid()),
    )

    dest_layer = QgsVectorLayer(uri, layer_name, "memory")
    dest_provider = dest_layer.dataProvider()
    dest_provider.addAttributes(source_provider.fields())

    new_attributes = []
    for name, type in additional_attributes.items():
        new_attributes.append(QgsField(name, type))

    dest_provider.addAttributes(new_attributes)
    dest_layer.updateFields()

    return dest_layer
