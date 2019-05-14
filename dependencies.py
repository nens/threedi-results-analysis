"""Handle dependencies

TODO: for now, this is try/except code copied out of ``__init__.py``, later on
this ought to be made more explicit and verbose.

"""
from .utils.user_messages import pop_up_info

import imp
import importlib
import logging
import os
import sys


logger = logging.getLogger(__name__)


def _check_importability(necessary_import, not_findable):
    """Check if necessary_import is importable, add the name to ``not_findable`` if not."""
    spec = importlib.util.find_spec(necessary_import)
    if spec is None:
        logger.warning("Cannot import '%s'", necessary_import)
        not_findable.append(necessary_import)
        return
    logger.info(
        "Import '%s' found. Name=%s, origin=%s",
        necessary_import,
        spec.name,
        spec.origin,
    )


def _check_requirements(requirements):
    """Require all requirements, this raises an error if something is missing."""
    import pkg_resources  # It might be missing.
    missing = []
    for requirement in requirements:
        distributions = pkg_resources.require(requirement)
        logger.info("Requirement '%s' found: %s", requirement, distributions)


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
    not_findable = []
    for necessary_import in necessary_imports:
        _check_importability(necessary_import, not_findable)

    if not_findable:
        pop_up_info("Error loading modules: %s", ", ".join(not_findable))

    current_directory = os.path.dirname(__file__)
    requirements_txt = os.path.join(current_directory, "requirements.txt")
    requirements = open(requirements_txt).read().strip().split("\n")
    requirements = [r.strip() for r in requirements]
    requirements = [r for r in sorted(requirements) if r and not r.startswith("#")]
    try:
        _check_requirements(requirements)
    except Exception:
        logger.exception("Not all requirements are OK")

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
