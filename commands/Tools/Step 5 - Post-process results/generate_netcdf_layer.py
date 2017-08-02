"""This script generates node and line layers from netCDF.
"""
from qgis.core import QgsMapLayerRegistry

from ThreeDiToolbox.utils.user_messages import pop_up_info
from ThreeDiToolbox.views.tool_dialog import ToolDialogWidget
from ThreeDiToolbox.commands.base.custom_command import CustomCommandBase


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

        vlayers = self.datasource.get_result_layers()

        # add the layers
        QgsMapLayerRegistry.instance().addMapLayers(vlayers)
