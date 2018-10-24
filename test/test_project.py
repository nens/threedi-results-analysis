# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

from __future__ import absolute_import
import unittest
import tempfile
import os.path

from qgis.core import QgsProject
from qgis.PyQt.QtCore import QObject, pyqtSignal, QFileInfo

from ThreeDiToolbox.utils.qprojects import ProjectStateMixin
from .utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class ExampleTool(QObject):

    state_changed = pyqtSignal([str, str, list])
    tool_name = 'example_tool'
    state = {}

    def emit_value(self, setting_key, value):
        self.state_changed.emit(self.tool_name, setting_key, [value])

    def set_state(self, settings_dict):
        self.state = settings_dict

    def get_state_description(self):
        return (self.tool_name,
                {
                    'bool_value': bool,
                    'int_value': int,
                    'float_value': float,
                    'str_value': str,
                    'list_value': list
                })


class ExampleProjectManager(QObject, ProjectStateMixin):

    def __init__(self, iface, tools):
        QObject.__init__(self)
        self.iface = iface
        self.tools = tools
        self.init_state_sync(connect_to_save_and_load=False)


class TestProjectState(unittest.TestCase):
    """Test functions that convert parameters to variable names in the
    datasource."""

    def setUp(self):
        app, canvas, self.iface, parent = QGIS_APP

        self.tmp_directory = tempfile.mkdtemp()
        self.qgs_file_path = os.path.join(self.tmp_directory, 'test.qgs')

        self.tool = ExampleTool()
        self.prm = ExampleProjectManager(self.iface, [self.tool])

    def function_set_and_load_compare_value(self, key, value):

        # initial_project
        proj = QgsProject.instance()
        self.prm.load_and_set_state()
        # test state not present, must be None
        self.assertIsNone(self.tool.state[key])

        # set value and write
        self.tool.emit_value(key, value)
        # check value is set
        self.prm.load_and_set_state()
        # self.assertEqual(self.tool.state[key], value)
        proj.write(self.qgs_file_path)

        # reset project
        proj.clear()
        self.tool.set_state({})
        # check reset
        self.prm.load_and_set_state()
        self.assertIsNone(self.tool.state[key])

        # read project file
        proj.read(self.qgs_file_path)
        # no connection to load signal in test, so run manually
        self.prm.load_and_set_state()
        # check value read and transformed correctly
        self.assertEqual(self.tool.state[key], value)

        # reset project
        proj.clear()

    def test_set_and_load_bool_true(self):
        self.function_set_and_load_compare_value('bool_value', True)

    def test_set_and_load_bool_false(self):
        self.function_set_and_load_compare_value('bool_value', False)

    def test_set_and_load_float(self):
        self.function_set_and_load_compare_value('float_value', 5.40)

    def test_set_and_load_int(self):
        self.function_set_and_load_compare_value('int_value', 5)

    def test_set_and_load_str(self):
        self.function_set_and_load_compare_value('str_value', 'test_test')

    def test_set_and_load_list(self):

        value = ['test', 'test2', 'test3']
        key = 'list_value'
        # initial_project
        proj = QgsProject.instance()
        self.prm.load_and_set_state()
        # test state not present, must be None
        self.assertIsInstance(self.tool.state[key], list)
        self.assertEqual(len(self.tool.state[key]), 0)

        # set value and write
        self.tool.emit_value(key, value)
        # check value is set
        self.prm.load_and_set_state()
        self.assertIsInstance(self.tool.state[key], list)
        self.assertEqual(len(self.tool.state[key]), 3)
        self.assertEqual(self.tool.state[key][0], value[0])
        proj.write(self.qgs_file_path)

        # reset project
        proj.clear()
        self.tool.set_state({})
        # check reset
        self.prm.load_and_set_state()
        self.assertIsInstance(self.tool.state[key], list)
        self.assertEqual(len(self.tool.state[key]), 0)

        # read project file
        proj.read(self.qgs_file_path)
        # no connection to load signal in test, so run manually
        self.prm.load_and_set_state()
        # check value read and transformed correctly
        self.assertIsInstance(self.tool.state[key], list)
        self.assertEqual(len(self.tool.state[key]), 3)
        self.assertEqual(self.tool.state[key][0], value[0])
