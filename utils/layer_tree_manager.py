import os.path

from qgis.core import (
    QgsMapLayerRegistry, QgsProject, QgsDataSourceURI, QgsVectorLayer,
    QgsRectangle, QgsLayerTreeNode, QgsCoordinateTransform)

from .utils import csv_join
from ..utils.user_messages import pop_up_question
from ..stats.utils import (
    generate_structure_stats,
    generate_manhole_stats,
    generate_pump_stats,
    get_structure_layer_id_name,
    get_manhole_layer_id_name,
    get_default_csv_path,
    )
from .styler import Styler


class LayerTreeManager(object):

    model_layergroup_basename = '3di model: '
    schematisation_group_name = 'schematisation'
    schematisation_oned_group_name = '1d'
    schematisation_twod_group_name = '2d'
    schematisation_inflow_group_name = 'inflow'
    result_layergroup_basename = 'result: '
    statistic_layergroup_basename = 'statistics: '

    def __init__(self, iface, model_results_model):

        self.iface = iface
        self.model = model_results_model

        self.schematisation_layergroup = None
        self._model_layergroup = None
        self._model_layergroup_connected = False

        self.result_layergroups = []
        self.results_layers = []

        self.tool_layergroup = None
        self.tools_layers = None

        self.tracer_mapping = (
            # tracer, variable name
            ('root', 'model_layergroup'),
            ('schematisation_root', 'schematisation_layergroup')
        )

        # add listeners
        self.model.model_schematisation_change.connect(
            self._on_set_schematisation)
        # self.model.dataChanged.connect(self.on_change)
        self.model.rowsAboutToBeRemoved.connect(self.remove_results)
        self.model.rowsAboutToBeRemoved.connect(self.remove_statistics)
        self.model.rowsInserted.connect(self.add_results)
        self.model.rowsInserted.connect(self.add_statistic_layers)

        self.init_references_from_layer_tree()

    @property
    def model_layergroup(self):
        return self._model_layergroup

    @model_layergroup.setter
    def model_layergroup(self, value):
        if self._model_layergroup_connected:
            self._model_layergroup.destroyed.disconnect(
                self._on_delete_model_layergroup)
            self._model_layergroup_connected = False
        self._model_layergroup = value
        if isinstance(value, QgsLayerTreeNode):
            self._model_layergroup.destroyed.connect(
                self._on_delete_model_layergroup)
            self._model_layergroup_connected = True

    def _on_delete_model_layergroup(self):
        if self._model_layergroup_connected:
            self._model_layergroup.destroyed.disconnect(
                self._on_delete_model_layergroup)
            self._model_layergroup_connected = False
        self._model_layergroup = None

    def on_unload(self):
        self.model.model_schematisation_change.disconnect(
            self._on_set_schematisation)
        self.model.rowsAboutToBeRemoved.connect(self.remove_results)
        self.model.rowsAboutToBeRemoved.connect(self.remove_statistics)
        self.model.rowsInserted.connect(self.add_results)
        self.model.rowsInserted.connect(self.add_statistic_layers)

    def _mark(self, tree_node, marker):
        """Mark the group or layer with a marker value.

        Args:
            tree_node: a QgsLayerTreeGroup or QgsLayerTreeLayer instance
            marker: property value
        """
        tree_node.setCustomProperty('legend/3di_tracer', marker)

    def _find_marked_child(self, tree_node, marker):
        """Find a marked node in the children of a tree node."""
        if tree_node is None:
            return None

        for node in tree_node.children():
            if node.customProperty('legend/3di_tracer') == unicode(marker):
                return node
        return None

    @staticmethod
    def create_layer(db_path, layer_name, geometry_column='',
                     provider_type='spatialite', display_name=None):
        if display_name is None:
            display_name = layer_name

        uri = QgsDataSourceURI()
        uri.setDatabase(db_path)
        uri.setDataSource('', layer_name, geometry_column)
        return QgsVectorLayer(uri.uri(), display_name, provider_type)

    def init_references_from_layer_tree(self):
        root = QgsProject.instance().layerTreeRoot()
        tracer = dict([(ref, ident) for ident, ref in self.tracer_mapping])

        self.model_layergroup = self._find_marked_child(
            root, tracer['model_layergroup'])

        if self.model_layergroup is not None:
            self.schematisation_layergroup = self._find_marked_child(
                self.model_layergroup, tracer['schematisation_layergroup'])
        else:
            self.schematisation_layergroup = None

    def _on_set_schematisation(self, something, filename=''):
        """Method is called when schematisation setting is changed in
        datasource model.

        Args:
            something:
            filename:

        Returns: None
        """
        self.init_references_from_layer_tree()

        tracer = dict([(ref, ident) for ident, ref in self.tracer_mapping])

        if filename == '':
            if self.model_layergroup is not None:
                self.model_layergroup.removeAllChildren()
            return

        split = os.path.split(filename)
        split_dir = os.path.split(split[0])

        name = (self.model_layergroup_basename +
                '/'.join((split_dir[-1], split[-1])))

        if self.model_layergroup is None:
            # todo: see if we can set 'tracer' as custom property to identify
            # group later on
            root = QgsProject.instance().layerTreeRoot()
            self.model_layergroup = root.insertGroup(2, name)
            self._mark(self.model_layergroup, tracer['model_layergroup'])
        else:
            self.model_layergroup.setName(name)

        if self.schematisation_layergroup is None:
            self.schematisation_layergroup = self.model_layergroup.insertGroup(
                0, self.schematisation_group_name)
            self._mark(self.schematisation_layergroup,
                       tracer['schematisation_layergroup'])
        else:
            self.schematisation_layergroup.removeAllChildren()

        self.schematisation_layergroup.insertGroup(
            0, self.schematisation_inflow_group_name)
        self.schematisation_layergroup.insertGroup(
            0, self.schematisation_twod_group_name)
        self.schematisation_layergroup.insertGroup(
            0, self.schematisation_oned_group_name)

        # add_schematisation layers
        self._add_model_schematisation_layers(filename)

        # zoom to model extent:
        extent = QgsRectangle()
        extent.setMinimal()
        for tree_layer in self.schematisation_layergroup.findLayers():
            extent.combineExtentWith(tree_layer.layer().extent())

        extent.scale(1.1)

        transform = QgsCoordinateTransform(
            tree_layer.layer().crs(),
            self.iface.mapCanvas().mapRenderer().destinationCrs())

        self.iface.mapCanvas().setExtent(transform.transform(extent))

        return

    def _add_model_schematisation_layers(self, threedi_spatialite):
        """Assumes that the group layers are available

        Args:
            threedi_spatialite:
        """

        oned_layers = ['v2_pumpstation_view',
                       'v2_weir_view',
                       'v2_culvert_view',
                       'v2_orifice_view',
                       'v2_cross_section_locations',
                       'v2_outlet',
                       'v2_cross_section_location',
                       'v2_connection_nodes',
                       'v2_pipe_view',
                       'v2_channel',
                       ]
        twod_layers = ['v2_grid_refinement',
                       'v2_floodfill',
                       'v2_2d_lateral',
                       'v2_levee',
                       'v2_obstacle',
                       'v2_2d_boundary_conditions',
                       ]
        inflow_layers = ['v2_impervious_surface']
        # not added: v2_windshielding, v2_pumped_drainage_area,
        # v2_initial_waterlevel

        # little bit administration: get all the groups
        oned_group = self.schematisation_layergroup.findGroup(
            self.schematisation_oned_group_name)
        twod_group = self.schematisation_layergroup.findGroup(
            self.schematisation_twod_group_name)
        inflow_group = self.schematisation_layergroup.findGroup(
            self.schematisation_inflow_group_name)

        # now make the layers and add them to the groups
        for group, layers in [(oned_group, oned_layers),
                              (twod_group, twod_layers),
                              (inflow_group, inflow_layers),
                              ]:

            for layer_name in layers:
                vector_layer = self.create_layer(threedi_spatialite,
                                                 layer_name,
                                                 geometry_column='the_geom')

                if vector_layer.isValid():
                    Styler.apply_style(vector_layer, layer_name, 'schematisation')
                    QgsMapLayerRegistry.instance().addMapLayer(vector_layer,
                                                               False)
                    group.insertLayer(100, vector_layer)

        # tables without geometry
        tables = [(oned_group, 'v2_cross_section_definition'),
                  (self.schematisation_layergroup, 'v2_global_settings'),
                  (twod_group, 'v2_manhole'),
                  ]

        # add tables without geometry
        for group, table_name in tables:
            table_layer = self.create_layer(threedi_spatialite, table_name)

            if table_layer.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(table_layer, False)
                group.insertLayer(0, table_layer)

    def add_results(self, index, start_row, stop_row):
        # unique identifier?

        for row_nr in range(start_row, stop_row + 1):
            result = self.model.rows[row_nr]
            name = self.result_layergroup_basename + result.name.value

            if self.model_layergroup is not None:
                group = self._find_marked_child(
                    self.model_layergroup, 'result_' + result.file_path.value)

                if group is None:
                    group = self.model_layergroup.insertGroup(2, name)
                    self._mark(group, 'result_' + result.file_path.value)

                line, node, pumpline = result.get_result_layers()

                if self._find_marked_child(group, 'flowlines') is None:
                    # apply default styling on memory layers
                    line.loadNamedStyle(os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        os.path.pardir, 'layer_styles', 'tools',
                        'flowlines.qml'))

                    node.loadNamedStyle(os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        os.path.pardir, 'layer_styles', 'tools', 'nodes.qml'))

                    QgsMapLayerRegistry.instance().addMapLayers(
                        [line, node, pumpline], False)

                    tree_layer = group.insertLayer(0, line)
                    self._mark(tree_layer, 'flowlines')

                    tree_layer2 = group.insertLayer(1, pumpline)
                    if tree_layer2 is not None:
                        self._mark(tree_layer2, 'pumplines')

                    tree_layer3 = group.insertLayer(2, node)
                    self._mark(tree_layer3, 'nodes')

    # TODO: make static or just function
    def _create_layers(self, db_path, group, layernames, geometry_column=''):
        layers = []
        for layername in layernames:
            if self._find_marked_child(group, layername) is None:
                new_layer = self.create_layer(
                    db_path, layername, geometry_column=geometry_column)
                layers.append(new_layer)
        return layers

    def add_statistic_layers(self, result_row_nr, start_row, stop_row):

        if not pop_up_question('Do you want to calculate statistics (in this '
                               'version it can still take forever with large '
                               'netcdf files)?',
                               'Calculate statistics?',):
            return

        for row_nr in range(start_row, stop_row + 1):
            result = self.model.rows[row_nr]
            name = "%s%s" % (self.statistic_layergroup_basename,
                             result.name.value)
            marker = 'statistic_%s' % result.file_path.value

            # TODO: not sure if I am doing things twice by calling this
            # function again... Layers are cached in sqlite right, so it
            # should be okay? --> yes, they are cached
            line, node, pumpline = result.get_result_layers()

            node_layer_names = ['v2_manhole',
                                ]
            line_layer_names = ['v2_weir_view',
                                'v2_culvert_view',
                                'v2_orifice_view',
                                'v2_pipe_view',
                                ]
            pump_layer_names = ['v2_pumpstation_view']

            styled_layers = {
                'v2_manhole': [ # name, style, field
                    ('Manhole statistieken', '', None),
                ],
                'v2_weir_view': [
                    ('Totaal overstort volume positief [q_cum]', 'totaal overstort volume positief', None),
                    ('Totaal overstort volume negatief [q_cum]', 'totaal overstort volume negatief', None),
                    ('Overstort max positief debiet [q]', 'overstort max positief debiet', None),
                ],
                'v2_orifice_view': [
                    ('orifice statistieken', '', None),
                ],
                'v2_pipe_view': [
                    ('pipe max debiet [q_max]', 'pipe max debiet', None),
                ],
                'nodes': [
                    ('node statistieken', '', None),
                ],
                'flowlines': [],
                'v2_culvert_view': [
                    ('culvert statistieken', '', None),
                ]
            }

            # output dir of the csvs (= model result dir)
            output_dir = os.path.dirname(result.file_path.value)

            if self.model_layergroup is not None:
                group = self._find_marked_child(self.model_layergroup, marker)

                if group is None:
                    group = self.model_layergroup.insertGroup(3, name)
                    self._mark(group, marker)

                node_layers = [node] + self._create_layers(
                    self.model.model_spatialite_filepath,
                    group, node_layer_names, geometry_column='')
                line_layers = [line] + self._create_layers(
                    self.model.model_spatialite_filepath,
                    group, line_layer_names, geometry_column='the_geom')
                pump_layers = [pumpline] + self._create_layers(
                    self.model.model_spatialite_filepath,
                    group, pump_layer_names, geometry_column='the_geom')

                for new_layer in node_layers:
                    if new_layer.isValid():
                        # Generate stats, join the csv with layer, and
                        # insert the csv as layer
                        layer_id_name = get_manhole_layer_id_name(
                            new_layer.name())
                        _filepath = get_default_csv_path(
                            new_layer.name(), output_dir)
                        if os.path.exists(_filepath):
                            # The csv was already generated, reuse it
                            print("Reusing existing statistics csv: %s" %
                                  _filepath)
                            filepath = _filepath
                        else:
                            # No stats; generate it
                            try:
                                filepath = generate_manhole_stats(
                                    result.datasource(), output_dir,
                                    new_layer, layer_id_name,
                                    include_2d=True)
                                print("Generated %s" % filepath)
                            except ValueError as e:
                                print(e.message)
                                continue

                        for name, style, field in styled_layers[new_layer.name()]:
                            
                            layer = QgsVectorLayer(new_layer.source(), name, new_layer.providerType())

                            csv_layer = csv_join(
                                filepath, layer, layer_id_name,
                                add_to_legend=False)

                            Styler.apply_style(layer, style, 'stats')

                            QgsMapLayerRegistry.instance().addMapLayer(
                                layer, False)

                            tree_layer = group.insertLayer(100, layer)
                            self._mark(tree_layer, new_layer.name())


                for new_layer in line_layers:
                    if new_layer.isValid():

                        # Generate stats, join the csv with layer, and
                        # insert the csv as layer
                        layer_id_name = get_structure_layer_id_name(
                            new_layer.name())
                        _filepath = get_default_csv_path(
                            new_layer.name(), output_dir)
                        if os.path.exists(_filepath):
                            # The csv was already generated, reuse it
                            print("Reusing existing statistics csv: %s" %
                                  _filepath)
                            filepath = _filepath
                        else:
                            # No stats; generate it
                            try:
                                filepath = generate_structure_stats(
                                    result.datasource(), output_dir,
                                    new_layer, layer_id_name,
                                    include_2d=True)
                                print("Generated %s" % filepath)
                            except ValueError as e:
                                print(e.message)
                                continue

                        for name, style, field in styled_layers[new_layer.name()]:
                            # this could be a way, but not work correctly: s = new_layer.source()

                            layer = QgsVectorLayer(new_layer.source(), name, new_layer.providerType())

                            csv_layer = csv_join(
                                filepath, layer, layer_id_name,
                                add_to_legend=False)

                            Styler.apply_style(layer, style, 'stats')

                            QgsMapLayerRegistry.instance().addMapLayer(
                                layer, False)

                            tree_layer = group.insertLayer(100, layer)
                            self._mark(tree_layer, new_layer.name())

                for lyr in pump_layers:
                    if not lyr:
                        continue
                    if lyr.isValid():
                        QgsMapLayerRegistry.instance().addMapLayer(
                            lyr, False)
                        tree_layer = group.insertLayer(100, lyr)
                        self._mark(tree_layer, lyr.name())

                        # Generate stats, join the csv with layer, and
                        # insert the csv as layer
                        layer_id_name = get_structure_layer_id_name(
                            lyr.name())
                        _filepath = get_default_csv_path(
                            lyr.name(), output_dir)
                        if os.path.exists(_filepath):
                            # The csv was already generated, reuse it
                            print("Reusing existing statistics csv: %s" %
                                  _filepath)
                            filepath = _filepath
                        else:
                            # No stats; generate it
                            try:
                                filepath = generate_pump_stats(
                                    result.datasource(), output_dir,
                                    lyr, layer_id_name,
                                    include_2d=True)
                                print("Generated %s" % filepath)
                            except ValueError as e:
                                print(e.message)
                                continue
                        csv_layer = csv_join(
                            filepath, lyr, layer_id_name,
                            add_to_legend=False)

                        csv_tree_layer = group.insertLayer(100, csv_layer)
                        self._mark(csv_tree_layer, csv_layer.name())

    def remove_results(self, index, start_row, stop_row):
        for row_nr in range(start_row, stop_row + 1):
            result = self.model.rows[row_nr]
            group = self._find_marked_child(self.model_layergroup,
                                            'result_' + result.file_path.value)
            if group is not None:
                group.removeAllChildren()
                self.model_layergroup.removeChildNode(group)

    def remove_statistics(self, index, start_row, stop_row):
        for row_nr in range(start_row, stop_row + 1):
            result = self.model.rows[row_nr]
            group = self._find_marked_child(
                self.model_layergroup, 'statistic_' + result.file_path.value)
            if group is not None:
                group.removeAllChildren()
                self.model_layergroup.removeChildNode(group)
