from threedi_results_analysis.threedi_plugin_tool import ThreeDiPluginTool

import os


class StatisticsTool(ThreeDiPluginTool):

    def __init__(self, iface, model):
        super().__init__()

        self.iface = iface
        self.model = model
        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons", "icon_custom_statistics.png")
        self.menu_text = u"Statistics"

    def run(self):
        pass
