# 3Di Schematisation Editor for QGIS, licensed under GPLv2 or (at your option) any later version
# Copyright (C) 2022 by Lutra Consulting for 3Di Water Management
import os
import shutil
import re


def get_version(directory):
    metadata = os.path.join(directory, "metadata.txt")
    reg = "\nversion=(.+)\n"
    version = ""
    with open(metadata, "r") as f:
        m0 = re.search(reg, f.read())
        if m0:
            version = m0.group(1)
    return version


if __name__ == "__main__":
    print("ZIPPING PLUGIN STARTED")
    this_dir = os.path.dirname(os.path.realpath(__file__))
    plugin_dirname = "threedi-results-analysis"
    plugin_path = os.path.join(this_dir, plugin_dirname)
    plugin_version = get_version(plugin_path)
    zip_filename = f"{plugin_dirname}.{plugin_version}"
    plugin_zip_path = os.path.join(this_dir, zip_filename)
    shutil.make_archive(plugin_zip_path, "zip", this_dir, plugin_dirname)
    print("ZIPPING PLUGIN FINISHED")
