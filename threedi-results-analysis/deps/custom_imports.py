# 3Di Results Analysis for QGIS, licensed under GPLv2 or (at your option) any later version
# Copyright (C) 2022 by Lutra Consulting for 3Di Water Management
import os
import sys
from subprocess import check_call, CalledProcessError

DEPS_DIR = os.path.dirname(os.path.abspath(__file__))


def import_deps():
    """
    Function that tests if extra modules are installed.
    If a module is not available, it adds the module wheel to the Python path.
    """
    try:
        import threedigrid_builder
    except (ImportError, FileNotFoundError):
        install_package_from_wheel(os.path.join(DEPS_DIR, "threedigrid_builder-1.3.5-cp39-cp39-win_amd64.whl"))


def install_package_from_wheel(wheel_path):
    """Install package from the wheel."""
    flags = ["--upgrade", "--force-reinstall"]
    package_reinstalled, feedback_message = False, None
    try:
        check_call(["python", "-m", "pip", "install", *flags, wheel_path], shell=True)
        package_reinstalled = True
    except CalledProcessError as e:
        feedback_message = e.output
    return package_reinstalled, feedback_message
