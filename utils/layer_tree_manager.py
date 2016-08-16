import os.path

from qgis.core import (
    QgsMapLayerRegistry, QgsProject, QgsDataSourceURI, QgsVectorLayer,
    QgsRectangle, QgsLayerTreeNode, QgsCoordinateTransform)


class LayerTreeManager(object):

    model_grouplayer_basename = '3di model: '
    schematisation_group_name = 'schematisation'
    schematisation_oned_group_name = '1d'
    schematisation_twod_group_name = '2d'
    schematisation_inflow_group_name = 'inflow'
    result_grouplayer_basename = 'result: '
    schematisation_grouplayer = None

    @property
    def model_grouplayer(self):
        return self._modelgrouplayer

    @model_grouplayer.setter
    def model_grouplayer(self, value):
        if self._modelgrouplayer_connected:
            self._modelgrouplayer.destroyed.disconnect(
                self._on_delete_modelgrouplayer)
            self._modelgrouplayer_connected = False
        self._modelgrouplayer = value
        if isinstance(value, QgsLayerTreeNode):
            self._modelgrouplayer.destroyed.connect(
                self._on_delete_modelgrouplayer)
            self._modelgrouplayer_connected = True

    def _on_delete_modelgrouplayer(self):
        if self._modelgrouplayer_connected:
            self._modelgrouplayer.destroyed.disconnect(
                self._on_delete_modelgrouplayer)
            self._modelgrouplayer_connected = False
        self._modelgrouplayer = None

    def __init__(self, iface, model_results_model):

        self.iface = iface
        self.model = model_results_model

        self._modelgrouplayer = None
        self._modelgrouplayer_connected = False

        self.result_grouplayers = []
        self.results_layers = []

        self.tool_grouplayer = None
        self.tools_layers = None

        self.tracer_mapping = (
            # tracer, variable name
            ('root', 'model_grouplayer'),
            ('schematisation_root', 'schematisation_grouplayer')
        )

        # add listeners
        self.model.model_schematisation_change.connect(
            self._on_set_schematisation)
        # self.model.dataChanged.connect(self.on_change)
        self.model.rowsAboutToBeRemoved.connect(self.remove_results)
        self.model.rowsInserted.connect(self.add_results)

        self.init_references_from_layer_tree()

    def on_unload(self):
        self.model.model_schematisation_change.disconnect(
            self._on_set_schematisation)
        self.model.rowsAboutToBeRemoved.connect(self.remove_results)
        self.model.rowsInserted.connect(self.add_results)

    def _find_marked_child(self, group_layer, marker):

        if group_layer is None:
            return None

        for node in group_layer.children():
            if node.customProperty('legend/3di_tracer') == unicode(marker):
                return node
        return None

    def init_references_from_layer_tree(self):
        root = QgsProject.instance().layerTreeRoot()
        tracer = dict([(ref, ident) for ident, ref in self.tracer_mapping])

        self.model_grouplayer = self._find_marked_child(
            root, tracer['model_grouplayer'])

        if self.model_grouplayer is not None:
            self.schematisation_grouplayer = self._find_marked_child(
                self.model_grouplayer, tracer['schematisation_grouplayer'])
        else:
            self.schematisation_grouplayer = None

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
            if self.model_grouplayer is not None:
                self.model_grouplayer.removeAllChildren()
            return

        split = os.path.split(filename)
        split_dir = os.path.split(split[0])

        name = (self.model_grouplayer_basename +
                '/'.join((split_dir[-1], split[-1])))

        if self.model_grouplayer is None:
            # todo: see if we can set 'tracer' as custom property to identify
            # group later on
            root = QgsProject.instance().layerTreeRoot()
            self.model_grouplayer = root.insertGroup(2, name)
            self.model_grouplayer.setCustomProperty('legend/3di_tracer',
                                                    tracer['model_grouplayer'])
        else:
            self.model_grouplayer.setName(name)

        if self.schematisation_grouplayer is None:
            self.schematisation_grouplayer = self.model_grouplayer.insertGroup(
                0, self.schematisation_group_name)
            self.schematisation_grouplayer.setCustomProperty(
                'legend/3di_tracer', tracer['schematisation_grouplayer'])
        else:
            self.schematisation_grouplayer.removeAllChildren()

        self.schematisation_grouplayer.insertGroup(
            0, self.schematisation_inflow_group_name)
        self.schematisation_grouplayer.insertGroup(
            0, self.schematisation_twod_group_name)
        self.schematisation_grouplayer.insertGroup(
            0, self.schematisation_oned_group_name)

        # add_schematisation layers
        self._add_model_schematisation_layers(filename)

        # zoom to model extent:
        extent = QgsRectangle()
        extent.setMinimal()
        for tree_layer in self.schematisation_grouplayer.findLayers():
            extent.combineExtentWith(tree_layer.layer().extent())

        extent.scale(1.1)

        transform = QgsCoordinateTransform(
            tree_layer.layer().crs(),
            self.iface.mapCanvas().mapRenderer().destinationCrs())

        self.iface.mapCanvas().setExtent(transform.transform(extent))

        return

    def _add_model_schematisation_layers(self, threedi_spatialite):
        """
            Assumes that the group layers are available
        Args:
            threedi_spatialite:

        Returns:

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
        twod_layers = ['v2_grid_refinement', 'v2_floodfill', 'v2_2d_lateral',
                       'v2_levee', 'v2_obstacle', 'v2_2d_boundary_conditions']
        inflow_layers = ['v2_impervious_surface']

        # not added: v2_windshielding, v2_pumped_drainage_area,
        # v2_initial_waterlevel

        for group, layers in [
            (self.schematisation_grouplayer.findGroup(
                self.schematisation_oned_group_name), oned_layers),
            (self.schematisation_grouplayer.findGroup(
                self.schematisation_twod_group_name), twod_layers),
            (self.schematisation_grouplayer.findGroup(
                self.schematisation_inflow_group_name), inflow_layers)]:

            for layer_name in layers:
                uri = QgsDataSourceURI()
                uri.setDatabase(threedi_spatialite)
                uri.setDataSource('', layer_name, 'the_geom')

                vector_layer = QgsVectorLayer(
                    uri.uri(), layer_name, 'spatialite')

                if vector_layer.isValid():
                    QgsMapLayerRegistry.instance().addMapLayer(vector_layer,
                                                               False)
                    group.insertLayer(100, vector_layer)

        # add tables without geometry
        tables = [(self.schematisation_grouplayer.findGroup(
                   self.schematisation_oned_group_name),
                   'v2_cross_section_definition'),
                  (self.schematisation_grouplayer,
                   'v2_global_settings')
                  ]

        for group, table_name in tables:
            uri = QgsDataSourceURI()
            uri.setDatabase(threedi_spatialite)
            uri.setDataSource('', table_name, '')

            table_layer = QgsVectorLayer(uri.uri(),
                                         table_name,
                                         'spatialite')

            if table_layer.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(table_layer, False)
                group.insertLayer(0, table_layer)

    def add_results(self, index, start_row, stop_row):
        # unique identifier?

        for row_nr in range(start_row, stop_row + 1):
            result = self.model.rows[row_nr]
            name = self.result_grouplayer_basename + result.name.value

            if self.model_grouplayer is not None:
                group = self._find_marked_child(
                    self.model_grouplayer, 'result_' + result.file_path.value)

                if group is None:
                    group = self.model_grouplayer.insertGroup(2, name)
                    group.setCustomProperty('legend/3di_tracer',
                                            'result_' + result.file_path.value)

                line, node, pumpline = result.get_memory_layers()

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
                    tree_layer.setCustomProperty(
                        'legend/3di_tracer', 'flowlines')
                    tree_layer2 = group.insertLayer(1, pumpline)
                    if tree_layer2 is not None:
                        tree_layer2.setCustomProperty(
                            'legend/3di_tracer', 'pumplines')
                    tree_layer3 = group.insertLayer(2, node)
                    tree_layer3.setCustomProperty('legend/3di_tracer', 'nodes')

    def add_statistic_layers(self, result_row_nr):
        result = self.model.row[result_row_nr]

    def remove_results(self, index, start_row, stop_row):
        for row_nr in range(start_row, stop_row + 1):
            result = self.model.rows[row_nr]
            group = self._find_marked_child(self.model_grouplayer,
                                            'result_' + result.file_path.value)
            if group is not None:
                group.removeAllChildren()
                self.model_grouplayer.removeChildNode(group)
