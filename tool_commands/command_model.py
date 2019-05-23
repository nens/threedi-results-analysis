from functools import reduce
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtGui import QStandardItem
from qgis.PyQt.QtGui import QStandardItemModel

import os


DEFAULT_COMMAND_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "commands"
)


class CommandModel(QStandardItemModel):
    def __init__(self, toolbox_dir=None, parent=None):
        super(CommandModel, self).__init__(parent)

        self.directory = toolbox_dir
        if self.directory is None:
            self.directory = DEFAULT_COMMAND_DIR

        self.file_structure = self.get_directory_structure(self.directory)
        self.add_items(self, self.file_structure)

    def add_items(self, parent, elements):
        icon_command = QIcon(":/plugins/ThreeDiToolbox/icons/icon_command_small.png")
        icon_hammer = QIcon(":/plugins/ThreeDiToolbox/icons/icon_hammer_small.png")

        for text, children in iter(sorted(elements.items())):
            item = QStandardItem(text)
            parent.appendRow(item)
            if children:
                item.setIcon(icon_command)
                self.add_items(item, children)
            else:
                # show the hammer icon for the actual command scripts
                if text.endswith(".py"):
                    item.setIcon(icon_hammer)
                else:
                    # empty command directory should have the command icon
                    item.setIcon(icon_command)

    def get_directory_structure(self, rootdir):
        """
        Creates a nested dictionary that represents the folder structure of
        rootdir.
        """
        dir = {}
        rootdir = rootdir.rstrip(os.sep)
        start = rootdir.rfind(os.sep) + 1
        for path, dirs, files in os.walk(rootdir):
            folders = path[start:].split(os.sep)
            subdir = dict.fromkeys(
                [
                    f
                    for f in files
                    if os.path.splitext(f)[1] == ".py" and f != "__init__.py"
                ]
            )
            parent = reduce(dict.get, folders[:-1], dir)
            parent[folders[-1]] = subdir
        return dir
