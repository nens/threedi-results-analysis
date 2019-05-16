"""Handle dependencies

sqlalchemy: not pure python, but only for some speedups which have a python fallback.
Perhaps use a source dist? Pass "don't compile" option?

geoalchemy2: wheel or sdist, on linux "pip install"

lizard-connector: wheel or sdist, on linux "pip install"

threedigrid: wheel or sdist, on linux "pip install"

h5py: on windows, an osgeo zip download and then extract a subdir.
On linux: assume an "apt-get"



Hmmmmm.... lets just prepare a zip and unzip that in the
/python/threeditoolbox-dependencies/ folder, add it to the path and be done with it.

Everything except h5py can be just the linux version. Perhaps do a special thingy for sqlalchemy to get a proper windows wheel/egg.


Ideally, this means we just use regular import-finding-mechanisms, like
properly naming eggs/wheels.

Hmmmmmmm..... .pth files.... They'd have to point at the proper OS version. So I probably still have to call pip to install it.

"""
from .utils.user_messages import pop_up_info
from collections import namedtuple
from pathlib import Path

import imp
import importlib
import logging
import os
import pkg_resources
import sys


Dependency = namedtuple("Dependency", ["name", "package", "constraint"])

DEPENDENCIES = [
    Dependency("GeoAlchemy2", "geoalchemy2", ">=0.6.2, <0.7"),
    Dependency("SQLAlchemy", "sqlalchemy", ">=1.1.11, <1.2"),
    Dependency("h5py", "h5py", ">= 2.7.1"),
    Dependency("lizard-connector", "lizard_connector", "==0.6"),
    Dependency("pyqtgraph", "pyqtgraph", ">=0.10.0"),
    Dependency("threedigrid", "threedigrid", "==1.0.13"),
]

our_dir = Path(__file__).parent
CUSTOM_LIBRARY_DIR = our_dir.parent.parent / "threeditoolbox-libraries"

logger = logging.getLogger(__name__)


def ensure_everything_installed():
    """Check if DEPENDENCIES are installed and install them if missing."""
    setup_custom_library_dir()
    missing = _check_presence(DEPENDENCIES)
    _install_dependencies(missing)


def setup_custom_library_dir():
    if not CUSTOM_LIBRARY_DIR.exists():
        CUSTOM_LIBRARY_DIR.mkdir(parents=True)
        logger.info("Created custom library dir %s", CUSTOM_LIBRARY_DIR)
    if CUSTOM_LIBRARY_DIR not in sys.path:
        sys.path.insert(0, CUSTOM_LIBRARY_DIR)
        logger.info("Added custom library dir %s to sys.path", CUSTOM_LIBRARY_DIR)
        logger.debug("sys.path: %s", sys.path)


def _check_importability(necessary_imports):
    """Check if necessary_import is importable, add the name to ``not_findable`` if not."""
    missing = []
    for necessary_import in necessary_imports:
        spec = importlib.util.find_spec(necessary_import)
        if spec is None:
            logger.warning("Cannot import '%s'", necessary_import)
            missing.append(necessary_import)
            continue
        logger.info(
            "Import '%s' found. Name=%s, origin=%s",
            necessary_import,
            spec.name,
            spec.origin,
        )
    return missing


def _install_dependencies(dependencies, target_dir=CUSTOM_LIBRARY_DIR):
    for dependency in dependencies:
        pass


def _check_presence(dependencies):
    """Check if all dependencies are present. Return missing dependencies."""
    missing = []
    for dependency in dependencies:
        requirement = dependency.name + dependency.constraint
        try:
            distributions = pkg_resources.require(requirement)
            logger.info("Dependency '%s' found: %s", dependency.name, distributions)
        except pkg_resources.DistributionNotFound:
            logger.exception(
                "Dependency '%s' (%s) not found", dependency.name, dependency.constraint
            )
            missing.append(dependency)
    return missing


def try_to_import_dependencies():
    """Try to import everything we need and pop up an error upon failures."""
    logger.debug("Starting to look at dependencies...")
    logger.debug("sys.path: %s", sys.path)
    necessary_imports = [
        "geoalchemy2",
        "h5py",
        "lizard_connector",
        "pkg_resources",  # setuptools
        "pyqtgraph",
        "sqlalchemy",
        "threedigrid",
    ]
    not_findable = _check_importability(necessary_imports)
    if not_findable:
        pop_up_info("Error loading modules: %s", ", ".join(not_findable))

    # TODO: use next location to do some "pip install" magic with the external
    # directory as index location.
    # python_dir_in_profile = os.path.abspath(os.path.join(current_directory, "..", ".."))

    try:
        # Note: we're not importing it directly using the import statement because
        # this will cause .pyd files to be loaded in dynamically. Because the
        # loaded files are open in QGIS you can't delete them unless you close the
        # program (at least with Windows), which is problematic when trying to
        # update the plugin using the plugin manager (because it tries to delete
        # the old plugin files). Real imports are postponed as long as possible.
        imp.find_module("h5py")
        logger.info("Using local h5py installation.")
    except ImportError:
        if os.name == "nt":
            if sys.maxsize > 2 ** 32:
                sys.path.append(
                    os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        "external",
                        "h5py-win64",
                    )
                )
                logger.info("Using h5py provided by plugin.")
            else:
                pop_up_info(
                    "Error: could not find h5py installation. Change "
                    "to the 64-bit version of QGIS or try to install the "
                    "h5py python libary yourself."
                )
        else:
            pop_up_info(
                "Error: could not find h5py installation. Please "
                "install the h5py package manually."
            )


def generate_constraints_txt():
    constraints_file = our_dir / "constraints.txt"
    lines = [(dependency.name + dependency.constraint) for dependency in DEPENDENCIES]
    lines.append("")
    constraints_file.write_text("\n".join(lines))
    print("Wrote constraints to %s" % constraints_file)


if __name__ == "__main__":
    generate_constraints_txt()
