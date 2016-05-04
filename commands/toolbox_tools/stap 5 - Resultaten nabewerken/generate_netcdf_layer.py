"""This script calculates statistics on the selected layer for structures and
outputs it to csv.
"""
from qgis.core import (
    QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsPoint,
    QgsMapLayerRegistry
    )
from PyQt4.QtCore import QVariant

from ThreeDiToolbox.utils.user_messages import pop_up_info
from ThreeDiToolbox.views.tool_dialog import ToolDialogWidget
from ThreeDiToolbox.commands.base.custom_command import CustomCommandBase
from ThreeDiToolbox.utils.layer_from_netCDF import make_flowline_layer, make_node_layer
from ThreeDiToolbox.datasource.netcdf import get_node_mapping


def make_pumpline_layer(ds):
    """Make a memory layer that contains all pumplines.

    Args:
        ds: netCDF Dataset
    """
    # Get relevant netCDF.Variables
    projection = ds.variables['projected_coordinate_system']
    epsg = projection.epsg  # = 28992
    # Pumpline connections (2, jap1d):
    pumpline = ds.variables['pump_mapping']
    # FlowElem centers:
    flowelem_xcc = ds.variables['FlowElem_xcc']  # in meters
    flowelem_ycc = ds.variables['FlowElem_ycc']  # in meters

    # -1 probably because of fortran indexing
    pumpline_p1 = pumpline[0, :].astype(int)  # - 1
    pumpline_p2 = pumpline[1, :].astype(int)  # - 1

    # TODO: Not very efficient, but this mapping is not needed anyway in the
    # future, so who cares?
    node_mapping = get_node_mapping(ds)
    for i in range(pumpline.shape[1]):
        # Note: there is no need to subtract 1 from the index because the
        # node_mapping already does this for you
        pumpline_p1[i] = node_mapping.get(pumpline_p1[i], 0)
        pumpline_p2[i] = node_mapping.get(pumpline_p2[i], 0)

    # Point 1 of the connection
    x_p1 = flowelem_xcc[:][pumpline_p1]
    y_p1 = flowelem_ycc[:][pumpline_p1]

    # Point 2 of the connection
    x_p2 = flowelem_xcc[:][pumpline_p2]
    y_p2 = flowelem_ycc[:][pumpline_p2]

    # create layer
    # "Point?crs=epsg:4326&field=id:integer&field=name:string(20)&index=yes"
    uri = "LineString?crs=epsg:{}&index=yes".format(
        epsg)
    vl = QgsVectorLayer(uri, "pumplines", "memory")
    pr = vl.dataProvider()

    # add fields
    pr.addAttributes([
        # This is the flowline index in Python (0-based indexing)
        # Important: this differs from the feature id which is flowline idx+1!!
        QgsField("pumpline_idx", QVariant.Int),
        ])
    vl.updateFields()  # tell the vector layer to fetch changes from the provider

    # add features
    features = []
    number_of_pumplines = pumpline.shape[1]
    for i in range(number_of_pumplines):
        fet = QgsFeature()

        p1 = QgsPoint(x_p1[i], y_p1[i])
        p2 = QgsPoint(x_p2[i], y_p2[i])

        fet.setGeometry(QgsGeometry.fromPolyline([p1, p2]))
        fet.setAttributes([i])
        features.append(fet)
    pr.addFeatures(features)

    # update layer's extent when new features have been added
    # because change of extent in provider is not propagated to the layer
    vl.updateExtents()

    # add the layer
    QgsMapLayerRegistry.instance().addMapLayers([vl])


class CustomCommand(CustomCommandBase):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.iface = kwargs.get('iface')
        self.ts_datasource = kwargs.get('ts_datasource')

        # These will be dynamically set:
        self.layer = None
        self.datasource = None

    def run(self):
        self.show_gui()

    def show_gui(self):
        self.tool_dialog_widget = ToolDialogWidget(
            iface=self.iface, ts_datasource=self.ts_datasource, command=self)
        self.tool_dialog_widget.exec_()  # block execution

    def run_it(self, layer=None, datasource=None):
        if datasource:
            self.datasource = datasource
        if not self.datasource:
            pop_up_info("No datasource found, aborting.", title='Error')
            return
        nds = self.datasource.datasource()  # the netcdf datasource

        vlayer = make_flowline_layer(nds)
        # add the layer
        QgsMapLayerRegistry.instance().addMapLayers([vlayer])

        vlayer = make_node_layer(nds)
        # add the layer
        QgsMapLayerRegistry.instance().addMapLayers([vlayer])

        try:
            make_pumpline_layer(nds.ds)
        except:
            print("Pumps are still in development")
            pass
