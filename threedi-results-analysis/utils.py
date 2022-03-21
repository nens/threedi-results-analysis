import os


def safe_join(*path):
    """
    Join path parts and replace any backslashes with slash to make QGIS happy when accessing a Windows network location.
    """
    joined = os.path.join(*path)
    return joined.replace("\\", "/")


def icon_path(icon_filename):
    return safe_join(os.path.dirname(os.path.realpath(__file__)), "img", icon_filename)
