from osgeo import ogr
from numpy import isnan

def threedigrid_to_ogr(
    tgt_ds: ogr.DataSource,
    attributes: dict,
    attr_data_types: dict,
):
    """
    Create an ogr target_node_layer from the ogr Datasource with custom attributes

    :param tgt_ds: ogr Datasource
    :param attributes: {attribute name: list of values}
    :param attr_data_types: {attribute name: ogr data type}
    :return: modified ogr Datasource
    """
    print("Starting threedigrid_to_ogr", tgt_ds)
    # Iterate over layers in the target data source
    for index in range(tgt_ds.GetLayerCount()):
        print("Layer", index)
        layer = tgt_ds.GetLayer(index)
        print("Layer feature counts", layer.GetFeatureCount())
        # feature_defn = layer.GetLayerDefn()
        # feature = ogr.Feature(feature_defn)

        # Add additional attributes to the layer
        for attr_name, attr_values in attributes.items():
            print("Attribute", attr_name)
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

                print("Value", f"index-{i}", val)
                feature = layer.GetFeature(i)
                if feature is None:
                    print(f"Failed to retrieve feature for index-{i}")
                    continue
                feature[attr_name] = val
                layer.SetFeature(feature)

            # create the actual feature
            # layer.SetFeature(feature)

    print("Finished threedigrid_to_ogr")
    # Return the modified OGR DataSource
    return tgt_ds
