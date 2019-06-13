from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtGui import QStandardItem
from qgis.PyQt.QtGui import QStandardItemModel
from ThreeDiToolbox.tool_commands.constants import COMMAND_STRUCTURE


class CommandModel(QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.command_structure = self.get_command_structure()
        self.add_items(self, self.command_structure)

    def add_items(self, parent, elements):
        icon_command = QIcon(":/plugins/ThreeDiToolbox/icons/icon_command_small.png")
        icon_hammer = QIcon(":/plugins/ThreeDiToolbox/icons/icon_hammer_small.png")

        for text, children in iter(sorted(elements.items())):
            item = QStandardItem(text)
            parent.appendRow(item)
            if children:
                # command directory should have the command icon
                item.setIcon(icon_command)
                self.add_items(item, children)
            else:
                if text.endswith(".py"):
                    # command script should have the hammer icon
                    item.setIcon(icon_hammer)
                else:
                    # empty command directory should also have the command icon
                    item.setIcon(icon_command)

    def get_command_structure(self):
        """Creates a nested dictionary that represents the command structure. Nested
        values are None, which will be assigned in self.add_items() with an icon path
        :return: nested dict e.g: {
            "Step 1 - Check data": {
                "schematisation_checker.py": None,
                "raster_checker.py": None,
                },
            "Step 2 - Convert and import data": {
                "import_sufhyd.py": None},
                },
            }
        """
        command_structure = COMMAND_STRUCTURE.copy()
        for step, commands in command_structure.items():
            for module_name, package_name in commands.items():
                # set nested values to None (why? see docstring)
                commands[module_name] = None
        return command_structure
