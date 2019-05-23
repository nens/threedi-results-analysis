from functools import reduce
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtGui import QStandardItem
from qgis.PyQt.QtGui import QStandardItemModel

import inspect
import os


DEFAULT_COMMAND_DIR = os.path.join(
    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
    "..",
    "tool_commands",
    "commands",
)


class Tool(object):
    def __init__(self, parent, tool_file):
        self.tool_file = tool_file
        self.parent = parent

        self.subnodes = None

        if parent is not None:
            self.parent.addChild(self)


class ToolGroup(object):
    def __init__(self, parent, directory):
        self.directory = directory
        self.parent = parent

        self.subnodes = []

        if parent is not None:
            self.parent.addChild(self)

    def addChild(self, child):
        self.subnodes.append(child)


class CommandModel(QStandardItemModel):
    def __init__(self, toolbox_dir=None, parent=None):
        super(CommandModel, self).__init__(parent)

        self.directory = toolbox_dir
        if self.directory is None:
            self.directory = DEFAULT_COMMAND_DIR

        self.file_structure = self.get_directory_structure(self.directory)
        self.add_items(self, self.file_structure)

    def add_items(self, parent, elements):
        icon_commands = QIcon(":/plugins/ThreeDiToolbox/icons/icon_commands_small.png")
        icon_hammer = QIcon(":/plugins/ThreeDiToolbox/icons/icon_hammer_small.png")

        for text, children in iter(sorted(elements.items())):
            item = QStandardItem(text)
            parent.appendRow(item)
            if children:
                item.setIcon(icon_commands)
                self.add_items(item, children)
            else:
                # show the hammer icon for the actual command scripts
                if text.endswith(".py"):
                    item.setIcon(icon_hammer)
                else:
                    # empty command directory should have the command icon
                    item.setIcon(icon_commands)

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
