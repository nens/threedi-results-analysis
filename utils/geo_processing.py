from qgis.core import QgsVectorLayer
from qgis.core import QgsWkbTypes


def copy_layer_into_memory_layer(source_layer, layer_name):

    source_provider = source_layer.dataProvider()

    uri = "{0}?crs=EPSG:{1}".format(
        QgsWkbTypes.displayString(source_provider.wkbType()).lstrip("WKB"),
        str(source_provider.crs().postgisSrid()),
    )

    dest_layer = QgsVectorLayer(uri, layer_name, "memory")
    dest_provider = dest_layer.dataProvider()

    dest_provider.addAttributes(source_provider.fields())
    dest_layer.updateFields()

    dest_provider.addFeatures([f for f in source_provider.getFeatures()])
    dest_layer.updateExtents()

    return dest_layer
