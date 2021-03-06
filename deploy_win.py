import os
import shutil

plugin = "threedi-results-analysis"
qgis_profile_name = "default"

this_dir = os.path.dirname(os.path.realpath(__file__))
home_dir = os.path.expanduser("~")
dest_dir_plug = os.path.join(
    home_dir, "AppData", "Roaming", "QGIS", "QGIS3", "profiles", qgis_profile_name, "python", "plugins", plugin
)
print(dest_dir_plug)
src_dir_plug = os.path.join(this_dir, plugin)
try:
    shutil.rmtree(dest_dir_plug)
except OSError:
    pass  # directory doesn't exist
shutil.copytree(src_dir_plug, dest_dir_plug)
