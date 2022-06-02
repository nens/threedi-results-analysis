"""Handle dependencies: installation and checking/logging.

See :doc:`linked_external-dependencies_readme`
(``external-dependencies/README.rst``) for a full explanation of the
dependency handling.

``python3 dependencies.py`` runs ``generate_constraints_txt()``: it generates
``constraints.txt``.

:py:func:`ensure_everything_installed()` checks if :py:data:`DEPENDENCIES` are
installed and installs them if needed.

:py:func:`check_importability()` double-checks if everything is importable. It also
logs the locations.

Note that we use *logging* in ``check_importability()`` as we want to have the
result in the logfile. The rest of the module uses ``print()`` statements
because it gets executed before any logging has been configured.

As we're called directly from ``__init__.py``, the imports should be
resticted. No qgis message boxes and so!

"""
from collections import namedtuple
from pathlib import Path

import importlib
import logging
import os
import pkg_resources
import platform
import re
import subprocess
import sys


Dependency = namedtuple("Dependency", ["name", "package", "constraint"])

#: List of expected dependencies.
DEPENDENCIES = [
    Dependency("SQLAlchemy", "sqlalchemy", "<1.4"),
    Dependency("GeoAlchemy2", "geoalchemy2", "==0.10.2"),
    Dependency("lizard-connector", "lizard_connector", "==0.7.3"),
    Dependency("pyqtgraph", "pyqtgraph", ">=0.11.1,<0.12"),
    Dependency("threedigrid", "threedigrid", ">=1.1.13"),
    Dependency("cached-property", "cached_property", ""),
    Dependency("threedi-modelchecker", "threedi_modelchecker", ">=0.27.1"),
    Dependency("threedidepth", "threedidepth", "==0.4"),
    Dependency("click", "click", ">=8.0"),
    Dependency("alembic", "alembic", "==1.6.5"),
    Dependency("mako", "mako", ""),
    Dependency("netCDF4", "netCDF4", ""),
    Dependency("cftime", "cftime", ""),
    Dependency("packaging", "packaging", ""),
]

# Dependencies that contain compiled extensions for windows platform
WINDOWS_PLATFORM_DEPENDENCIES = [
    Dependency("scipy", "scipy", "==1.6.2"),
]
H5PY_DEPENDENCY = Dependency("h5py", "h5py", "==2.10.0")
SUPPORTED_HDF5_VERSIONS = ["1.10.7"]

# If you add a dependency, also adjust external-dependencies/populate.sh
INTERESTING_IMPORTS = ["numpy", "osgeo", "pip", "setuptools"]

OUR_DIR = Path(__file__).parent

logger = logging.getLogger(__name__)


def ensure_everything_installed():
    """Check if DEPENDENCIES are installed and install them if missing."""
    print("sys.path:")
    for directory in sys.path:
        print("  - %s" % directory)
    profile_python_names = [item.name for item in _dependencies_target_dir().iterdir()]
    print("Contents of our profile's python dir:\n    %s" % "\n    ".join(profile_python_names))
    _ensure_prerequisite_is_installed()
    missing = _check_presence(DEPENDENCIES)
    if platform.system() == "Windows":
        missing += _check_presence(WINDOWS_PLATFORM_DEPENDENCIES)
        _ensure_h5py_installed()
    target_dir = _dependencies_target_dir()
    _install_dependencies(missing, target_dir=target_dir)


def _ensure_h5py_installed():
    """
    On Windows Qgis comes with a hdf5 version installed.
    This plugin uses the h5py python package, which is built against a specific version
    of HDF5. The Qgis HDF5 version and the HDF5 version of the h5py package must be the
    same, otherwise it will not work. In the external-dependencies folder we supply a
    Windows version of h5py built using HDF5 1.10.7. On pypi there is no h5py 2.10.0 package available
    built with Python 3.9 and HDF5 1.10.7. We need creat such wheel ourselves.

    The following situations can occur:

                           | QGIS HDF5 = 1.10.7  | QGIS HDF5 != 1.10.7
    -----------------------|---------------------|---------------
    h5py build with 1.10.7 | A: Good             | B: Qgis crash

    The different situations are marked A and B in the table above.

    In situations A everything is good and the plugin can be loaded without any
    problems.

    Situations B occur when a user upgrades/downgrades their Qgis version when
    the ThreediToolbox is already installed with a specific version of h5py.
    In these cases we also need to upgrade/downgrade the h5py version installed with
    ThreediToolbox.

    In situations B Qgis will crash when trying to import h5py.

    We use the H5pyMarker to mark the installed h5py version. This is because we cannot check the version
    by importing h5py, as Qgis will crash if the HDF5 and h5py binaries do not match.
    """
    h5py_dependency = Dependency("h5py", "h5py", "==2.10.0")
    hdf5_version = "1.10.7"  # there is only one version of HDF5 available in the QGIS installer
    h5py_missing = _check_presence([h5py_dependency])
    marker_version = H5pyMarker.version()
    if h5py_missing:
        _install_h5py(hdf5_version)

    if hdf5_version == "1.10.7":
        if marker_version == "1.10.7":
            # Do nothing
            pass
        else:
            _install_h5py(hdf5_version)


def _install_h5py(hdf5_version: str):
    if hdf5_version not in SUPPORTED_HDF5_VERSIONS:
        # raise an error because we cannot continue
        message = (
            f"Unsupported HDF5 version: {hdf5_version}. "
            f"The following HDF5 versions are supported: {SUPPORTED_HDF5_VERSIONS}"
        )
        raise RuntimeError(message)
    use_pypi = False  # There is no official Python 3.9 wheel for h5py 2.10.0

    # In case the (old) h5py library is already imported, we cannot uninstall
    # h5py because the windows acquires a lock on the *.dll-files. Therefore
    # we need to restart Qgis.
    # _uninstall_dependency(H5PY_DEPENDENCY)
    try:
        _install_dependencies([H5PY_DEPENDENCY], target_dir=_dependencies_target_dir(), use_pypi=use_pypi)
    except RuntimeError:
        from ThreeDiToolbox.utils.user_messages import pop_up_info

        pop_up_info(
            "Please restart QGIS to complete the installation process of " "ThreediToolbox.",
            title="Restart required",
        )
        return
    H5pyMarker.create(hdf5_version)


class H5pyMarker:
    """Marker indicating with which HDF5 binaries the h5py is installed.

    Currently, there is 1 supported HDF5 version:
    - 1.10.7: use h5py from the external-dependencies folder in this repo
    """

    H5PY_MARKER = OUR_DIR / ".h5py_marker"

    @classmethod
    def version(cls) -> str:
        if cls.H5PY_MARKER.exists():
            with open(cls.H5PY_MARKER, "r") as marker:
                version = marker.readline()
            return version
        else:
            return ""

    @classmethod
    def create(cls, version: str):
        with open(cls.H5PY_MARKER, "w") as marker:
            marker.write(version)

    @classmethod
    def remove(cls):
        cls.H5PY_MARKER.unlink()


def _ensure_prerequisite_is_installed(prerequisite="pip"):
    """Check the basics: pip.

    People using OSGEO custom installs sometimes exclude those
    dependencies. Our installation scripts fail, then, because of the missing
    'pip'.

    """
    try:
        importlib.import_module(prerequisite)
    except Exception as e:
        msg = (
            "%s. 'pip', which we need, is missing. It is normally included with "
            "python. You are *probably* using a custom minimal OSGEO release. "
            "Please re-install with 'pip' included."
        ) % e
        print(msg)
        raise RuntimeError(msg)


def _dependencies_target_dir(our_dir=OUR_DIR):
    """Return python dir inside our profile

    Return two dirs up if we're inside the plugins dir. If not, we have to
    import from qgis (which we don't really want in this file) and ask for our
    profile dir.

    """
    if "plugins" in str(our_dir).lower():
        # Looks like we're in the plugin dir. Return ../..
        return OUR_DIR.parent.parent
    # We're somewhere outside of the plugin directory. Perhaps a symlink?
    # Perhaps a development setup? We're forced to import qgis and ask for our
    # profile directory, something we'd rather not do at this stage. But ok.
    print("We're not in our plugins directory: %s" % our_dir)
    from qgis.core import QgsApplication

    python_dir = Path(QgsApplication.qgisSettingsDirPath()) / "python"
    print("We've asked qgis for our python directory: %s" % python_dir)
    return python_dir


def check_importability():
    """Check if the dependendies are importable and log the locations.

    If something is not importable, which should not happen, it raises an
    ImportError automatically. Which is exactly what we want, because we
    cannot continue.

    """
    packages = [dependency.package for dependency in DEPENDENCIES]
    packages += INTERESTING_IMPORTS
    logger.info("sys.path:\n    %s", "\n    ".join(sys.path))
    profile_python_names = [item.name for item in _dependencies_target_dir().iterdir()]
    logger.info(
        "Contents of our profile's python dir:\n    %s",
        "\n    ".join(profile_python_names),
    )
    for package in packages:
        imported_package = importlib.import_module(package)
        logger.info("Import '%s' found at \n    '%s'", package, imported_package.__file__)


def _uninstall_dependency(dependency):
    print("Trying to uninstalling dependency %s" % dependency.name)
    python_interpreter = _get_python_interpreter()
    process = subprocess.Popen(
        [
            python_interpreter,
            "-m",
            "pip",
            "uninstall",
            "--yes",
            (dependency.name),
        ],
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # The input/output/error stream handling is a bit involved, but it is
    # necessary because of a python bug on windows 7, see
    # https://bugs.python.org/issue3905 .
    i, o, e = (process.stdin, process.stdout, process.stderr)
    i.close()
    result = o.read() + e.read()
    o.close()
    e.close()
    print(result)
    exit_code = process.wait()
    if exit_code:
        print("Uninstalling %s failed" % dependency.name)


def _install_dependencies(dependencies, target_dir, use_pypi=False):
    python_interpreter = _get_python_interpreter()
    base_command = [
        python_interpreter,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "--no-deps",
        "--find-links",
        str(OUR_DIR / "external-dependencies"),
        "--no-index",
        "--target",
        str(target_dir),
    ]
    if use_pypi:
        index = base_command.index("--find-links")
        base_command.pop(index)  # --find-links
        base_command.pop(index)  # the dir
        base_command.pop(index)  # --no-index

    for dependency in dependencies:
        _uninstall_dependency(dependency)
        print("Installing '%s' into %s" % (dependency.name, target_dir))
        command = base_command + [dependency.name + dependency.constraint]
        process = subprocess.Popen(
            command,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # The input/output/error stream handling is a bit involved, but it is
        # necessary because of a python bug on windows 7, see
        # https://bugs.python.org/issue3905 .
        i, o, e = (process.stdin, process.stdout, process.stderr)
        i.close()
        result = o.read() + e.read()
        o.close()
        e.close()
        print(result)
        exit_code = process.wait()
        if exit_code:
            raise RuntimeError("Installing %s failed" % dependency.name)
        print("Installed %s into %s" % (dependency.name, target_dir))
        if dependency.package in sys.modules:
            print("Unloading old %s module" % dependency.package)
            del sys.modules[dependency.package]
            # check_importability() will be called soon, which will import them again.
            # By removing them from sys.modules, we prevent older versions from
            # sticking around.


def _get_python_interpreter():
    """Return the path to the python3 interpreter.

    Under linux sys.executable is set to the python3 interpreter used by Qgis.
    However, under Windows/Mac this is not the case and sys.executable refers to the
    Qgis start-up script.
    """
    interpreter = None
    executable = sys.executable
    directory, filename = os.path.split(executable)
    if "python3" in filename.lower():
        interpreter = executable
    elif "qgis" in filename.lower():
        interpreter = os.path.join(directory, "python3.exe")
    else:
        raise EnvironmentError("Unexpected value for sys.executable: %s" % executable)
    assert os.path.exists(interpreter)  # safety check
    return interpreter


def _get_hdf5_version() -> str:
    process = subprocess.Popen(
        [
            "h5stat.exe",
            "--version",
        ],
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # The input/output/error stream handling is a bit involved, but it is
    # necessary because of a python bug on windows 7, see
    # https://bugs.python.org/issue3905 .
    i, o, e = (process.stdin, process.stdout, process.stderr)
    i.close()
    result = o.read() + e.read()
    o.close()
    e.close()
    pattern = re.compile(r"[\d]+.[\d]+.[\d]+")
    match = pattern.search(result)
    if match:
        return match.group()
    else:
        return None


def _check_presence(dependencies):
    """Check if all dependencies are present. Return missing dependencies."""
    missing = []
    for dependency in dependencies:
        requirement = dependency.name + dependency.constraint
        print("Checking presence of %s..." % requirement)
        try:
            result = pkg_resources.require(requirement)
            print("Requirement %s found: %s" % (requirement, result))
        except pkg_resources.DistributionNotFound:
            print("Dependency '%s' (%s) not found" % (dependency.name, dependency.constraint))
            missing.append(dependency)
        except pkg_resources.VersionConflict:
            print("Dependency '%s' (%s) has the wrong version" % (dependency.name, dependency.constraint))
            missing.append(dependency)
    return missing


def generate_constraints_txt(target_dir=OUR_DIR):
    """Called from the ``__main__`` to generate ``constraints.txt``."""
    constraints_file = target_dir / "constraints.txt"
    lines = ["# Generated by dependencies.py"]
    lines += [(dependency.name + dependency.constraint) for dependency in DEPENDENCIES]
    lines.append("")
    constraints_file.write_text("\n".join(lines))
    print("Wrote constraints to %s" % constraints_file)


if __name__ == "__main__":  # pragma: no cover
    generate_constraints_txt()
