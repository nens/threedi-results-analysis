from pathlib import Path

from qgis.core import QgsProject, QgsVectorLayer

from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel
from threedi_results_analysis.threedi_plugin_model import (
    ThreeDiGridItem,
    ThreeDiResultItem,
)
from threedi_results_analysis.tool_graph.graph_view import (
    GraphDockWidget,
)
from threedi_results_analysis.tool_water_balance.utils import WrappedResult


def test_water_balance_wrapper_resolves_isolated_result_layers():
    """Result-scoped consumers resolve isolated layers instead of grid layers."""
    project = QgsProject.instance()
    grid_layer = QgsVectorLayer("Point?crs=EPSG:28992", "Grid node", "memory")
    result_layer = QgsVectorLayer("Point?crs=EPSG:28992", "Result node", "memory")
    assert grid_layer.isValid()
    assert result_layer.isValid()
    project.addMapLayer(grid_layer, addToLegend=False)
    project.addMapLayer(result_layer, addToLegend=False)

    grid_item = ThreeDiGridItem(Path("c:/test/gridadmin.gpkg"), "grid")
    grid_item.layer_ids["node"] = grid_layer.id()
    result_item = ThreeDiResultItem(Path("c:/test/results_3di.nc"))
    result_item.layer_path = ["files", "result.zip"]
    result_item.layer_ids["node"] = result_layer.id()
    grid_item.appendRow(result_item)

    try:
        wrapped_result = WrappedResult(result_item)

        # An isolated result must resolve its node layer from its own layer IDs,
        # rather than from the parent grid's layer IDs.
        assert wrapped_result.points is result_layer

        # Without an isolated layer path, the wrapper deliberately falls back
        # to the shared grid-owned layer used by standalone results.
        result_item.layer_path = None
        assert wrapped_result.points is grid_layer
    finally:
        project.removeMapLayer(grid_layer.id())
        project.removeMapLayer(result_layer.id())


def test_graph_relevant_layers_include_isolated_result_layers():
    """Graph map-tool input accepts isolated and standalone-owned layers."""
    model = ThreeDiPluginModel()
    grid_item = ThreeDiGridItem(Path("c:/test/gridadmin.gpkg"), "grid")
    assert model.add_grid(grid_item)

    grid_layer = QgsVectorLayer("Point?crs=EPSG:28992", "Grid node", "memory")
    isolated_layer = QgsVectorLayer("Point?crs=EPSG:28992", "Isolated node", "memory")
    assert grid_layer.isValid()
    assert isolated_layer.isValid()
    project = QgsProject.instance()
    project.addMapLayer(grid_layer, addToLegend=False)
    project.addMapLayer(isolated_layer, addToLegend=False)
    grid_item.layer_ids["node"] = grid_layer.id()

    isolated_result = ThreeDiResultItem(Path("c:/test/results_3di.nc"))
    isolated_result.layer_path = ["files", "result.zip"]
    isolated_result.layer_ids["node"] = isolated_layer.id()
    assert model.add_result(isolated_result, grid_item)

    try:
        # Graph input must include both the shared grid layer and the separate
        # layer owned by the isolated result.
        relevant_layer_ids = GraphDockWidget._get_relevant_layer_ids(model, ["node"])
        assert grid_layer.id() in relevant_layer_ids
        assert isolated_layer.id() in relevant_layer_ids
    finally:
        project.removeMapLayer(grid_layer.id())
        project.removeMapLayer(isolated_layer.id())


def test_result_owned_group_and_node_layer_are_resolved_for_outputs():
    """Result-derived outputs can resolve isolated layer-group and node ownership."""
    grid_item = ThreeDiGridItem(Path("c:/test/gridadmin.gpkg"), "grid")
    result_item = ThreeDiResultItem(Path("c:/test/results_3di.nc"))
    result_item.layer_path = ["files", "result.zip"]
    result_item.layer_group = object()
    result_item.layer_ids["node"] = "isolated-node-id"
    grid_item.layer_group = object()
    grid_item.layer_ids["node"] = "grid-node-id"
    grid_item.appendRow(result_item)

    # Isolated outputs use both the result-owned group and the result-owned
    # computational layer.
    assert result_item.get_layer_group() is result_item.layer_group
    assert result_item.get_layer_ids()["node"] == "isolated-node-id"

    # Removing the layer path switches ownership back to the parent grid.
    result_item.layer_path = None
    assert result_item.get_layer_group() is grid_item.layer_group
    assert result_item.get_layer_ids()["node"] == "grid-node-id"
