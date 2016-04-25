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


def make_flowline_layer(ds):
    """Make a memory layer that contains all flowlines.

    Args:
        ds: netCDF Dataset
    """
    # Get relevant netCDF.Variables
    projection = ds.variables['projected_coordinate_system']
    epsg = projection.epsg  # = 28992
    # Connections (2, nFlowLine):
    flowline_connection = ds.variables['FlowLine_connection']
    # FlowElem centers:
    flowelem_xcc = ds.variables['FlowElem_xcc']  # in meters
    flowelem_ycc = ds.variables['FlowElem_ycc']  # in meters

    # -1 probably because of fortran indexing
    flowline_p1 = flowline_connection[0, :].astype(int) - 1
    flowline_p2 = flowline_connection[1, :].astype(int) - 1

    # Point 1 of the connection
    x_p1 = flowelem_xcc[:][flowline_p1]
    y_p1 = flowelem_ycc[:][flowline_p1]

    # Point 2 of the connection
    x_p2 = flowelem_xcc[:][flowline_p2]
    y_p2 = flowelem_ycc[:][flowline_p2]

    # create layer
    # "Point?crs=epsg:4326&field=id:integer&field=name:string(20)&index=yes"
    uri = "LineString?crs=epsg:{}&index=yes".format(
        epsg)
    vl = QgsVectorLayer(uri, "flowlines", "memory")
    pr = vl.dataProvider()

    # add fields
    pr.addAttributes([
        # This is the flowline index in Python (0-based indexing)
        QgsField("flowline_idx", QVariant.Int),
        ])
    vl.updateFields()  # tell the vector layer to fetch changes from the provider

    # add features
    features = []
    for i in range(flowline_connection.shape[1]):
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
        ds = nds.ds

        make_flowline_layer(ds)
