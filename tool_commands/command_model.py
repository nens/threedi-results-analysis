from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtGui import QStandardItem
from qgis.PyQt.QtGui import QStandardItemModel
from ThreeDiToolbox.tool_commands.constants import STEP_MODULENAME_MAPPING


class CommandModel(QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.add_items(self)

    def add_items(self, parent):
        icon_command = QIcon(":/plugins/ThreeDiToolbox/icons/icon_command_small.png")
        icon_hammer = QIcon(":/plugins/ThreeDiToolbox/icons/icon_hammer_small.png")

        for step_text, commands in iter(sorted(STEP_MODULENAME_MAPPING.items())):
            item = QStandardItem(step_text)
            # command directory (empty or not) should have the command icon
            item.setIcon(icon_command)
            parent.appendRow(item)
            if commands:
                for command in commands:
                    sub_item = QStandardItem(command)
                    item.appendRow(sub_item)
                    # command script should have the hammer icon
                    sub_item.setIcon(icon_hammer)
