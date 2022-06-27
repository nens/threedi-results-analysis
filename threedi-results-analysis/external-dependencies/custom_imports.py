# 3Di Results Analysis for QGIS, licensed under GPLv2 or (at your option) any later version
# Copyright (C) 2022 by Lutra Consulting for 3Di Water Management
from collections import OrderedDict
import os
from subprocess import check_call, CalledProcessError

DEPS_DIR = os.path.dirname(os.path.abspath(__file__))
THREEDIGRID_WHL = "threedigrid-1.2.3-py2.py3-none-any.whl"
THREEDIGRID_BUILDER_WHL = "threedigrid_builder-1.3.6-cp39-cp39-win_amd64.whl"
PYGEOS_WHL = "pygeos-0.12.0-cp39-cp39-win_amd64.whl"
CONDENSER = "condenser-0.1.1-py2.py3-none-any.whl"


def patch_wheel_imports():
    """
    Function that tests if extra modules are installed.
    If a module is not available, it adds the module wheel to the Python path.
    """
    try:
        import threedigrid
    except (ImportError, FileNotFoundError, ModuleNotFoundError):
        reinstall_packages_from_wheels(os.path.join(DEPS_DIR, THREEDIGRID_WHL))

    try:
        import threedigrid_builder
    except (ImportError, FileNotFoundError, ModuleNotFoundError):
        reinstall_packages_from_wheels(os.path.join(DEPS_DIR, THREEDIGRID_BUILDER_WHL))

    try:
        import pygeos
    except (ImportError, FileNotFoundError, ModuleNotFoundError):
        reinstall_packages_from_wheels(os.path.join(DEPS_DIR, PYGEOS_WHL))

    try:
        import condenser
    except (ImportError, FileNotFoundError, ModuleNotFoundError):
        reinstall_packages_from_wheels(os.path.join(DEPS_DIR, CONDENSER))


def reinstall_packages_from_wheels(*wheel_filepaths):
    """Reinstall wheel packages."""
    flags = ["--upgrade", "--no-external-dependencies", "--force-reinstall"]
    reinstall_results = OrderedDict()
    for package in wheel_filepaths:
        try:
            check_call(["python", "-m", "pip", "install", *flags, package], shell=True)
            reinstall_results[package] = {"success": True, "error": ""}
        except CalledProcessError as e:
            feedback_message = e.output
            reinstall_results[package] = {"success": False, "error": feedback_message}
    return reinstall_results
