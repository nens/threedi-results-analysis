import os.path

from qgis.core import (
    QgsMapLayerRegistry, QgsProject, QgsDataSourceURI, QgsVectorLayer,
    QgsRectangle, QgsLayerTreeNode, QgsCoordinateTransform)

from ..utils.user_messages import pop_up_question
from ..stats.utils import (
    generate_structure_stats,
    generate_manhole_stats,
    generate_pump_stats,
    get_structure_layer_id_name,
    get_manhole_layer_id_name,
    get_pump_layer_id_name,
    get_default_csv_path,
    csv_join,
)
from . import styler
from .threedi_database import ThreediDatabase


def _clone_vector_layer(layer):
    """Create a new instance of a QgsVectorLayer from an existing one.

    Note that QgsVectorLayer is just view on the underlying data source.

    See CHANGES release 0.8.2 for the reason why layers are cloned in this
    way. Tl;dr: segfaults occur when you delete layer groups when the same
    layers are added multiple times
    """
    if layer:
        return QgsVectorLayer(
            layer.source(), layer.name(), layer.providerType())


class LayerTreeManager(object):

    model_layergroup_basename = '3Di model: '
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

    @staticmethod
    def _mark(tree_node, marker):
        """Mark the group or layer with a marker value.

        Args:
            tree_node: a QgsLayerTreeGroup or QgsLayerTreeLayer instance
            marker: property value
        """
        tree_node.setCustomProperty('legend/3di_tracer', marker)

    @staticmethod
    def _find_marked_child(tree_node, marker):
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

        # adjust spatialite for correct visualization of layers
        threedi_db = ThreediDatabase({'db_path': filename})
        threedi_db.fix_views()

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
                    styler.apply_style(vector_layer, layer_name,
                                       'schematisation')
                    QgsMapLayerRegistry.instance().addMapLayer(vector_layer,
                                                               False)
                    group.insertLayer(100, vector_layer)

        # tables without geometry
        tables = [(oned_group, 'v2_cross_section_definition'),
                  (self.schematisation_layergroup, 'v2_global_settings'),
                  (self.schematisation_layergroup, 'v2_numerical_settings'),
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

            node_layer_names = ['v2_manhole']
            line_layer_names = ['v2_weir_view',
                                'v2_culvert_view',
                                'v2_orifice_view',
                                'v2_pipe_view',
                                ]
            pump_layer_names = ['v2_pumpstation_view']

            styled_layers = {
                # {layer_name: [(name, style, field), ...], ... }
                'v2_manhole': [
                    ('Manhole statistieken', '', None),
                ],
                'v2_weir_view': [
                    ('Totaal overstort volume positief [tot_vol_positive]',
                     'totaal overstort volume positief',
                     'tot_vol_positive'),
                    ('Totaal overstort volume negatief [tot_vol_negative]',
                     'totaal overstort volume negatief',
                     'tot_vol_negative'),
                    ('Overstort max positief debiet [q_max]',
                     'overstort max positief debiet',
                     'q_max'),
                ],
                'v2_orifice_view': [
                    ('orifice statistieken', '', None),
                ],
                'v2_pipe_view': [
                    ('pipe max debiet [q_max]', 'pipe max debiet', 'q_max'),
                ],
                'nodes': [
                    ('node statistieken', '', None),
                ],
                'flowlines': [
                    ('line statistieken', '', None),
                ],
                'v2_culvert_view': [
                    ('culvert statistieken', '', None),
                ],
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

                sli1 = StatsLayerInfo(node_layers,
                                      get_manhole_layer_id_name,
                                      generate_manhole_stats)
                sli2 = StatsLayerInfo(line_layers,
                                      get_structure_layer_id_name,
                                      generate_structure_stats)
                sli3 = StatsLayerInfo(pump_layers,
                                      get_pump_layer_id_name,
                                      generate_pump_stats)
                for s in [sli1, sli2, sli3]:
                    s.generate_layers(output_dir, result, group, styled_layers)

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


class StatsLayerInfo(object):
    """Small wrapper for grouping functions used to generate statistics
    for some types of layers (node-like, line-like, pump-like)."""

    def __init__(self, layers, layer_id_name_func, generate_stats_func):
        self.layers = layers
        self.layer_id_name_func = layer_id_name_func
        self.generate_stats_func = generate_stats_func

    def generate_layers(self, output_dir, result, group, styled_layers):
        for lyr in self.layers:
            if not lyr:
                continue
            if lyr.isValid():
                # Generate stats, join the csv with layer, and
                # insert the csv as layer
                layer_id_name = self.layer_id_name_func(
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
                        filepath = self.generate_stats_func(
                            result.datasource(), output_dir,
                            lyr, layer_id_name,
                            include_2d=False)
                        print("Generated %s" % filepath)
                    except ValueError as e:
                        print(e.message)
                        continue

                # There *are* stats, but there is no entry in the
                # styled_layers dict, either because there is no styling, or
                # because it hasn't been added yet. Either way, We still want
                # to show the layer.
                if lyr.name() not in styled_layers:
                    layer = _clone_vector_layer(lyr)
                    csv_join(filepath, layer, layer_id_name,
                             add_to_legend=False)
                    QgsMapLayerRegistry.instance().addMapLayer(
                        layer, False)
                    tree_layer = group.insertLayer(100, layer)
                    LayerTreeManager._mark(tree_layer, lyr.name())
                    continue

                # There is an entry in the styled_layers dict, so apply the
                # corresponding style if possible. If not possible, just
                # add the joined layer.
                for name, style, field in styled_layers[lyr.name()]:
                    layer = _clone_vector_layer(lyr)
                    csv_layer = csv_join(
                        filepath, layer, layer_id_name,
                        add_to_legend=False)

                    # IMPORTANT: the style will only be applied if the field
                    # name is present in the layer:
                    fieldnames = [f.name() for f in csv_layer.fields()]
                    if field in fieldnames:
                        styler.apply_style(layer, style, 'stats')
                        layer.setLayerName(name)

                    layernames = [
                        tl.layer().name() for tl in group.children()]
                    if layer.name() not in layernames:
                        QgsMapLayerRegistry.instance().addMapLayer(
                            layer, False)

                        tree_layer = group.insertLayer(100, layer)
                        LayerTreeManager._mark(tree_layer, lyr.name())
