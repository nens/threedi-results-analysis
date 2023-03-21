from . import styler
# from .threedi_database import ThreediDatabase
from PyQt5.QtCore import QSettings
from qgis.core import QgsCoordinateTransform
from qgis.core import QgsDataSourceUri
from qgis.core import QgsLayerTreeNode
from qgis.core import QgsProject
from qgis.core import QgsRectangle
from qgis.core import QgsVectorLayer

import os.path


def _clone_vector_layer(layer):
    """Create a new instance of a QgsVectorLayer from an existing one.

    Note that QgsVectorLayer is just view on the underlying data source.

    See CHANGES release 0.8.2 for the reason why layers are cloned in this
    way. Tl;dr: segfaults occur when you delete layer groups when the same
    layers are added multiple times
    """
    if layer:
        return QgsVectorLayer(layer.source(), layer.name(), layer.providerType())


class LayerTreeManager(object):

    model_layergroup_basename = "3Di model: "
    schematisation_group_name = "schematisation"
    schematisation_settings_group_name = "settings"
    schematisation_boundary_group_name = "boundary conditions"
    schematisation_lateral_group_name = "laterals"
    schematisation_oned_group_name = "1d"
    schematisation_additional_oned_group_name = "additional tables for editing 1d"
    schematisation_obstacle_group_name = "obstacles"
    schematisation_grid_refinement_group_name = "grid refinements"

    schematisation_inflow_group_name = "inflow"
    inflow_imp_surface_subgroup_name = "impervious_surface"
    inflow_surface_subgroup_name = "surface"

    schematisation_advanced_settings_group_name = "advanced numerics"
    result_layergroup_basename = "result: "

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
            ("root", "model_layergroup"),
            ("schematisation_root", "schematisation_layergroup"),
        )

        # add listeners
        self.model.model_schematisation_change.connect(self._on_set_schematisation)
        # self.model.dataChanged.connect(self.on_change)
        # self.model.rowsAboutToBeRemoved.connect(self.remove_results)
        self.model.rowsInserted.connect(self.add_results)
        self.init_references_from_layer_tree()

    @property
    def model_layergroup(self):
        return self._model_layergroup

    @model_layergroup.setter
    def model_layergroup(self, value):
        if self._model_layergroup_connected:
            # self._model_layergroup.destroyed.disconnect(
            #     self._on_delete_model_layergroup)
            self._model_layergroup_connected = False
        self._model_layergroup = value
        if isinstance(value, QgsLayerTreeNode):
            # self._model_layergroup.destroyed.connect(
            #     self._on_delete_model_layergroup)
            self._model_layergroup_connected = True

    def _on_delete_model_layergroup(self):
        if self._model_layergroup_connected:
            # self._model_layergroup.destroyed.disconnect(
            #     self._on_delete_model_layergroup)
            self._model_layergroup_connected = False
        self._model_layergroup = None

    def on_unload(self):
        self.model.model_schematisation_change.disconnect(self._on_set_schematisation)
        self.model.rowsAboutToBeRemoved.connect(self.remove_results)
        self.model.rowsInserted.connect(self.add_results)

    @staticmethod
    def _mark(tree_node, marker):
        """Mark the group or layer with a marker value.

        Args:
            tree_node: a QgsLayerTreeGroup or QgsLayerTreeLayer instance
            marker: property value
        """
        tree_node.setCustomProperty("legend/3di_tracer", marker)

    @staticmethod
    def _find_marked_child(tree_node, marker):
        """Find a marked node in the children of a tree node."""
        if tree_node is None:
            return None

        for node in tree_node.children():
            if node.customProperty("legend/3di_tracer") == str(marker):
                return node
        return None

    @staticmethod
    def create_layer(
        db_path,
        layer_name,
        geometry_column="",
        provider_type="spatialite",
        display_name=None,
    ):
        if display_name is None:
            display_name = layer_name

        uri = QgsDataSourceUri()
        uri.setDatabase(db_path)
        uri.setDataSource("", layer_name, geometry_column)
        return QgsVectorLayer(uri.uri(), display_name, provider_type)

    def init_references_from_layer_tree(self):
        root = QgsProject.instance().layerTreeRoot()
        tracer = dict([(ref, ident) for ident, ref in self.tracer_mapping])

        self.model_layergroup = self._find_marked_child(
            root, tracer["model_layergroup"]
        )

        if self.model_layergroup is not None:
            self.schematisation_layergroup = self._find_marked_child(
                self.model_layergroup, tracer["schematisation_layergroup"]
            )
        else:
            self.schematisation_layergroup = None

    def _on_set_schematisation(self, something, filename=""):
        """Method is called when schematisation setting is changed in
        datasource model.

        Args:
            something:
            filename:

        Returns: None
        """

        self.init_references_from_layer_tree()

        tracer = dict([(ref, ident) for ident, ref in self.tracer_mapping])

        if filename == "":
            if self.model_layergroup is not None:
                self.model_layergroup.removeAllChildren()
            return

        split = os.path.split(filename)
        split_dir = os.path.split(split[0])

        name = self.model_layergroup_basename + "/".join((split_dir[-1], split[-1]))

        # adjust spatialite for correct visualization of layers
        # db_settings = {"db_path": filename}
        # threedi_db = ThreediDatabase(db_settings)
        # threedi_db.fix_spatial_indices()

        if self.model_layergroup is None:
            # todo: see if we can set 'tracer' as custom property to identify
            # group later on
            root = QgsProject.instance().layerTreeRoot()
            self.model_layergroup = root.insertGroup(2, name)
            self._mark(self.model_layergroup, tracer["model_layergroup"])
        else:
            self.model_layergroup.setName(name)

        if self.schematisation_layergroup is None:
            self.schematisation_layergroup = self.model_layergroup.insertGroup(
                1, self.schematisation_group_name
            )
            self._mark(
                self.schematisation_layergroup, tracer["schematisation_layergroup"]
            )
        else:
            self.schematisation_layergroup.removeAllChildren()

        self.schematisation_layergroup.insertGroup(
            0, self.schematisation_advanced_settings_group_name
        )

        # schematisation_inflow_group_name = 'inflow'
        # inflow_imp_surface_subgroup_name = 'impervious_surface'
        # inflow_surface_subgroup_name = 'surface'

        self.inflow_root = self.schematisation_layergroup.insertGroup(
            1, self.schematisation_inflow_group_name
        )
        self.inflow_root.addGroup(self.inflow_imp_surface_subgroup_name)
        self.inflow_root.addGroup(self.inflow_surface_subgroup_name)

        self.schematisation_layergroup.insertGroup(
            0, self.schematisation_grid_refinement_group_name
        )
        self.schematisation_layergroup.insertGroup(
            0, self.schematisation_obstacle_group_name
        )
        self.schematisation_layergroup.insertGroup(
            0, self.schematisation_additional_oned_group_name
        )
        self.schematisation_layergroup.insertGroup(
            0, self.schematisation_oned_group_name
        )
        self.schematisation_layergroup.insertGroup(
            0, self.schematisation_lateral_group_name
        )
        self.schematisation_layergroup.insertGroup(
            0, self.schematisation_boundary_group_name
        )
        self.schematisation_layergroup.insertGroup(
            0, self.schematisation_settings_group_name
        )

        # add_schematisation layers
        self._add_model_schematisation_layers(filename)

        # zoom to model extent:
        extent = QgsRectangle()
        extent.setMinimal()

        tree_layer = None
        for tree_layer in self.schematisation_layergroup.findLayers():
            extent.combineExtentWith(tree_layer.layer().extent())

        extent.scale(1.1)

        if not tree_layer:
            return

        transform = QgsCoordinateTransform(
            tree_layer.layer().crs(), QgsProject.instance().crs(), QgsProject.instance()
        )

        self.iface.mapCanvas().setExtent(transform.transform(extent))

        return

    def _add_model_schematisation_layers(self, threedi_spatialite):
        """Assumes that the group layers are available
        tables can be distinguished by having a geometry or not.
        First handle all tables with geometry"""

        # First, handle all tables with geometry

        settings_layers = []

        boundary_condition_layers = [
            "v2_1d_boundary_conditions_view",
            "v2_2d_boundary_conditions",
        ]

        lateral_layers = ["v2_1d_lateral_view", "v2_2d_lateral"]

        oned_layers = [
            "v2_connection_nodes",
            "v2_manhole_view",
            "v2_pumpstation_point_view",
            "v2_pumpstation_view",
            "v2_weir_view",
            "v2_culvert_view",
            "v2_orifice_view",
            "v2_pipe_view",
            "v2_cross_section_location_view",
            "v2_channel",
        ]

        additional_oned_layers = ["v2_culvert", "v2_cross_section_location"]

        obstacle_layers = ["v2_obstacle", "v2_levee"]

        grid_refinement_layers = ["v2_grid_refinement", "v2_grid_refinement_area"]

        inflow_imp_surface_layers = ["v2_impervious_surface"]

        inflow_surface_layers = ["v2_surface"]

        advanced_numerics_layers = ["v2_dem_average_area"]

        # little bit administration: get all the groups
        settings_group = self.schematisation_layergroup.findGroup(
            self.schematisation_settings_group_name
        )
        boundary_group = self.schematisation_layergroup.findGroup(
            self.schematisation_boundary_group_name
        )
        lateral_group = self.schematisation_layergroup.findGroup(
            self.schematisation_lateral_group_name
        )
        oned_group = self.schematisation_layergroup.findGroup(
            self.schematisation_oned_group_name
        )
        additional_oned_group = self.schematisation_layergroup.findGroup(
            self.schematisation_additional_oned_group_name
        )
        obstacle_group = self.schematisation_layergroup.findGroup(
            self.schematisation_obstacle_group_name
        )
        grid_refinement_group = self.schematisation_layergroup.findGroup(
            self.schematisation_grid_refinement_group_name
        )

        inflow_surface_subgroup = self.inflow_root.findGroup(
            self.inflow_surface_subgroup_name
        )
        inflow_imp_surface_subgroup = self.inflow_root.findGroup(
            self.inflow_imp_surface_subgroup_name
        )

        advanced_settings_group = self.schematisation_layergroup.findGroup(
            self.schematisation_advanced_settings_group_name
        )

        # now make the layers and add them to the groups
        for group, layers in [
            (settings_group, settings_layers),
            (boundary_group, boundary_condition_layers),
            (lateral_group, lateral_layers),
            (oned_group, oned_layers),
            (additional_oned_group, additional_oned_layers),
            (obstacle_group, obstacle_layers),
            (grid_refinement_group, grid_refinement_layers),
            (inflow_surface_subgroup, inflow_surface_layers),
            (inflow_imp_surface_subgroup, inflow_imp_surface_layers),
            (advanced_settings_group, advanced_numerics_layers),
        ]:

            for layer_name in layers:
                vector_layer = self.create_layer(
                    threedi_spatialite, layer_name, geometry_column="the_geom"
                )

                if vector_layer.isValid():
                    styler.apply_style(vector_layer, layer_name, "schematisation")
                    QgsProject.instance().addMapLayer(vector_layer, False)
                    group.insertLayer(100, vector_layer)
                    if group == additional_oned_group:
                        node = group.findLayer(vector_layer)
                        if node:
                            node.setItemVisibilityChecked(False)

        # Secondly, handle tables without geometry
        tables = [
            (settings_group, "v2_groundwater"),
            (settings_group, "v2_interflow"),
            (settings_group, "v2_aggregation_settings"),
            (settings_group, "v2_global_settings"),
            (settings_group, "v2_simple_infiltration"),
            (lateral_group, "v2_1d_lateral"),
            (boundary_group, "v2_1d_boundary_conditions"),
            (additional_oned_group, "v2_cross_section_definition"),
            (additional_oned_group, "v2_windshielding"),
            (additional_oned_group, "v2_pumpstation"),
            (additional_oned_group, "v2_manhole"),
            (additional_oned_group, "v2_orifice"),
            (additional_oned_group, "v2_weir"),
            (additional_oned_group, "v2_pipe"),
            (advanced_settings_group, "v2_numerical_settings"),
            (inflow_surface_subgroup, "v2_surface_map"),
            (inflow_surface_subgroup, "v2_surface_parameters"),
            (inflow_imp_surface_subgroup, "v2_impervious_surface_map"),
        ]

        # add tables without geometry
        for group, table_name in tables:
            table_layer = self.create_layer(threedi_spatialite, table_name)

            if table_layer.isValid():
                styler.apply_style(table_layer, table_name, "schematisation")
                QgsProject.instance().addMapLayer(table_layer, False)
                group.insertLayer(0, table_layer)
        QSettings().setValue("/Map/identifyAutoFeatureForm", "true")

    def add_results(self, index, start_row, stop_row):
        # unique identifier?

        for row_nr in range(start_row, stop_row + 1):
            result = self.model.rows[row_nr]
            name = self.result_layergroup_basename + result.name.value

            if self.model_layergroup is not None:
                group = self._find_marked_child(
                    self.model_layergroup, "result_" + result.file_path.value
                )

                if group is None:
                    group = self.model_layergroup.insertGroup(2, name)
                    self._mark(group, "result_" + result.file_path.value)

                line, node, cell, pumpline = result.get_result_layers()

                if self._find_marked_child(group, "flowlines") is None:
                    # apply default styling on memory layers
                    line.loadNamedStyle(
                        os.path.join(
                            os.path.dirname(os.path.realpath(__file__)),
                            os.path.pardir,
                            "layer_styles",
                            "tools",
                            "flowlines.qml",
                        )
                    )

                    node.loadNamedStyle(
                        os.path.join(
                            os.path.dirname(os.path.realpath(__file__)),
                            os.path.pardir,
                            "layer_styles",
                            "tools",
                            "nodes.qml",
                        )
                    )

                    QgsProject.instance().addMapLayers([line, node, pumpline], False)

                    tree_layer = group.insertLayer(0, line)
                    self._mark(tree_layer, "flowlines")

                    tree_layer2 = group.insertLayer(1, pumpline)
                    if tree_layer2 is not None:
                        self._mark(tree_layer2, "pumplines")

                    tree_layer3 = group.insertLayer(2, node)
                    self._mark(tree_layer3, "nodes")

    # TODO: make static or just function
    def _create_layers(self, db_path, group, layernames, geometry_column=""):
        layers = []
        for layername in layernames:
            if self._find_marked_child(group, layername) is None:
                new_layer = self.create_layer(
                    db_path, layername, geometry_column=geometry_column
                )
                layers.append(new_layer)
        return layers

    def remove_results(self, index, start_row, stop_row):
        for row_nr in range(start_row, stop_row + 1):
            result = self.model.rows[row_nr]
            group = self._find_marked_child(
                self.model_layergroup, "result_" + result.file_path.value
            )
            if group is not None:
                group.removeAllChildren()
                self.model_layergroup.removeChildNode(group)
