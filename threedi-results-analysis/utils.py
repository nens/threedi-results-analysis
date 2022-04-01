import os
import pathlib


def safe_join(*path):
    """
    Join path parts and replace any backslashes with slash to make QGIS happy when accessing a Windows network location.
    """
    joined = os.path.join(*path)
    return joined.replace("\\", "/")


def icon_path(icon_filename):
    return safe_join(os.path.dirname(os.path.realpath(__file__)), "img", icon_filename)


def same_path(path1, path2):
    """Check if the two paths are the same."""
    if not path1 or not path2:
        return False
    p1 = pathlib.Path(path1)
    p2 = pathlib.Path(path2)
    return p1 == p2
