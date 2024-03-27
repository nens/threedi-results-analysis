from osgeo import ogr
from numpy import isnan

def threedigrid_to_ogr(
    src_ds: ogr.DataSource,
    tgt_ds: ogr.DataSource,
    layer_type: str,
    attributes: dict,
    attr_data_types: dict,
):
    """
    Create an ogr target_node_layer from the ogr Datasource with custom attributes

    :param src_ds: source ogr Datasource
    :param tgt_ds: target ogr Datasource
    :param layer_type: layer type to add to the target datasource (node, cell, flowline)
    :param attributes: {attribute name: list of values}
    :param attr_data_types: {attribute name: ogr data type}
    :return: modified ogr Datasource
    """
    # Iterate through the layers in the GeoPackage and copy them to the target datasource
    for i in range(src_ds.GetLayerCount()):
        layer = src_ds.GetLayer(i)
        name = layer.GetName()
        if name == layer_type:
            tgt_ds.CopyLayer(layer, name)

    # Iterate over layers in the target data source
    for index in range(tgt_ds.GetLayerCount()):
        layer = tgt_ds.GetLayer(index)
        layer_name = layer.GetName()
        layer_defn = layer.GetLayerDefn()

        # Set geometry type
        # the initial geometry type of the layer is unknown or none
        # thus we need to set it manually
        if layer_name == "node":
            layer_defn.SetGeomType(ogr.wkbPoint)
        elif layer_name == "cell":
            layer_defn.SetGeomType(ogr.wkbPolygon)
        elif layer_name == "flowline":
            layer_defn.SetGeomType(ogr.wkbLineString)

        # Add additional attributes to the layer
        for attr_name, attr_values in attributes.items():
            # Check if the attribute already exists
            if layer.GetLayerDefn().GetFieldIndex(attr_name) == -1:
                # Add the attribute to the layer
                field_defn = ogr.FieldDefn(attr_name, attr_data_types[attr_name])
                layer.CreateField(field_defn)

            # Set the additional attribute value for each feature
            for i in range(layer.GetFeatureCount()):
                if i >= len(attr_values):
                    break
                val = attr_values[i]
                if val is None or isnan(val):
                    continue
                if attr_data_types[attr_name] in [ogr.OFTInteger]:
                    val = int(val)
                elif attr_data_types[attr_name] in [ogr.OFTString]:
                    val = val.decode("utf-8") if isinstance(val, bytes) else str(val)

                feature = layer.GetFeature(i)
                if feature is None:
                    continue
                feature[attr_name] = val
                layer.SetFeature(feature)
                feature = None

    return
