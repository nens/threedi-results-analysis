





class with:
- attributes:
  - icon_path
  - menu_text
- with at least the functions:
  - run
  - on_unload

For restoring the program state when loading a qgis project (*.qgs) file:
- add functions:
  - get_state(self)
  - set_state(self, setting_dictionary)
  - get_state_description(self)
- signal:
  - state_changed(plugin_name, setting, value)