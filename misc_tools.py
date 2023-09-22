# (c) Nelen & Schuurmans, see LICENSE.rst.
"""
Miscellaneous tools.
"""
from ThreeDiToolbox import PLUGIN_DIR
from ThreeDiToolbox.utils.user_messages import pop_up_info


class About(object):

    def __init__(self, iface):
        self.iface = iface
        self.icon_path = ":/plugins/ThreeDiToolbox/icons/icon_sunset.png"
        self.menu_text = "3Di about"

    def run(self):
        version_file = PLUGIN_DIR / "version.rst"
        version = version_file.read_text().rstrip()

        pop_up_info(
            "3Di Toolbox version %s" % version, "About", self.iface.mainWindow()
        )

    def on_unload(self):
        pass
