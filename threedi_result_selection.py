# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import os.path
import json

from PyQt4.QtCore import Qt, pyqtSignal, QObject

from views.result_selection import ThreeDiResultSelectionWidget


class ThreeDiResultSelection(QObject):
    """QGIS Plugin Implementation."""

    state_changed = pyqtSignal([str, str, list])

    tool_name = 'result_selection'

    def __init__(self, iface, ts_datasource):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        QObject.__init__(self)
        self.iface = iface

        self.ts_datasource = ts_datasource

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.icon_path = ':/plugins/ThreeDiToolbox/icon_add_datasource.png'
        self.menu_text = u'Selecteer 3Di resultaten'

        self.is_active = False
        self.dialog = None
        self.ts_datasource.model_schematisation_change.connect(self.on_state_changed)
        self.ts_datasource.results_change.connect(self.on_state_changed)

    def on_unload(self):
        """Cleanup necessary items here when dialog is closed"""

        # disconnects
        if self.dialog:
            self.dialog.close()

    def on_close_dialog(self):
        """Cleanup necessary items here when dialog is closed"""

        self.dialog.closingDialog.disconnect(self.on_close_dialog)

        self.dialog = None
        self.is_active = False

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.is_active:

            self.is_active = True

            if self.dialog is None:
                # Create the dialog (after translation) and keep reference
                self.dialog = ThreeDiResultSelectionWidget(None,
                                                           self.iface,
                                                           self.ts_datasource)

            # connect to provide cleanup on closing of dockwidget
            self.dialog.closingDialog.connect(self.on_close_dialog)

            # show the widget
            self.dialog.show()
        else:
            self.dialog.setWindowState(
                    self.dialog.windowState() & ~Qt.WindowMinimized |
                    Qt.WindowActive)
            self.dialog.raise_()

    def on_state_changed(self, setting_key, value):

        if setting_key == 'result_directories':
            output = []
            for result in value:
                output.append(json.JSONEncoder().encode({
                    'active': result.active.value,
                    'name': result.name.value,
                    'file_path': result.file_path.value,
                    'type': result.type.value
                }))
        else:
            output = value

        self.state_changed.emit(self.tool_name, setting_key, [output])

    def set_state(self, setting_dict):
        self.ts_datasource.reset()

        self.ts_datasource.model_spatialite_filepath = setting_dict.get(
                'model_schematisation', None)

        result_list = setting_dict.get('result_directories', None)
        if result_list is not None:
            for result_json in result_list:
                result = json.JSONDecoder().decode(result_json)
                self.ts_datasource.insertRows([result])

    def get_state_description(self):
        return (self.tool_name,
                {
                    'model_schematisation': file,
                    'result_directories': list
                })
