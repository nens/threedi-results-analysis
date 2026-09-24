from pathlib import Path
from types import SimpleNamespace

from qgis.core import QgsProject, QgsVectorLayer

from threedi_results_analysis.threedi_plugin_model import ThreeDiPluginModel
from threedi_results_analysis.threedi_plugin_model import (
    ThreeDiGridItem,
    ThreeDiResultItem,
)
from threedi_results_analysis.tool_graph.graph_view import (
    GraphDockWidget,
    NODE_OR_CELL,
)
from threedi_results_analysis.tool_water_balance.utils import WrappedResult


def test_water_balance_wrapper_resolves_grouped_result_layers():
    """Result-scoped consumers resolve grouped layers instead of grid layers."""
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
    result_item.group_path = ["files", "result.zip"]
    result_item.layer_ids["node"] = result_layer.id()
    grid_item.appendRow(result_item)

    try:
        wrapped_result = WrappedResult(result_item)
        assert wrapped_result.points is result_layer

        result_item.group_path = None
        assert wrapped_result.points is grid_layer
    finally:
        project.removeMapLayer(grid_layer.id())
        project.removeMapLayer(result_layer.id())


def test_graph_relevant_layers_include_grouped_result_layers():
    """Graph map-tool input accepts grouped and legacy-owned layers."""
    model = ThreeDiPluginModel()
    grid_item = ThreeDiGridItem(Path("c:/test/gridadmin.gpkg"), "grid")
    assert model.add_grid(grid_item)

    grid_layer = QgsVectorLayer("Point?crs=EPSG:28992", "Grid node", "memory")
    grouped_layer = QgsVectorLayer("Point?crs=EPSG:28992", "Grouped node", "memory")
    assert grid_layer.isValid()
    assert grouped_layer.isValid()
    project = QgsProject.instance()
    project.addMapLayer(grid_layer, addToLegend=False)
    project.addMapLayer(grouped_layer, addToLegend=False)
    grid_item.layer_ids["node"] = grid_layer.id()

    grouped_result = ThreeDiResultItem(Path("c:/test/results_3di.nc"))
    grouped_result.group_path = ["files", "result.zip"]
    grouped_result.layer_ids["node"] = grouped_layer.id()
    assert model.add_result(grouped_result, grid_item)

    try:
        relevant_layer_ids = GraphDockWidget._get_relevant_layer_ids(model, ["node"])
        assert grid_layer.id() in relevant_layer_ids
        assert grouped_layer.id() in relevant_layer_ids
    finally:
        project.removeMapLayer(grid_layer.id())
        project.removeMapLayer(grouped_layer.id())


def test_result_owned_group_and_node_layer_are_resolved_for_outputs():
    """Result-derived outputs can resolve grouped group and node ownership."""
    grid_item = ThreeDiGridItem(Path("c:/test/gridadmin.gpkg"), "grid")
    result_item = ThreeDiResultItem(Path("c:/test/results_3di.nc"))
    result_item.group_path = ["files", "result.zip"]
    result_item.layer_group = object()
    result_item.layer_ids["node"] = "grouped-node-id"
    grid_item.layer_group = object()
    grid_item.layer_ids["node"] = "grid-node-id"
    grid_item.appendRow(result_item)

    assert result_item.get_layer_group() is result_item.layer_group
    assert result_item.get_layer_ids()["node"] == "grouped-node-id"

    result_item.group_path = None
    assert result_item.get_layer_group() is grid_item.layer_group
    assert result_item.get_layer_ids()["node"] == "grid-node-id"


def test_graph_add_results_calls_relevant_layer_ids_correctly():
    """Regression test: add_results() must call the _get_relevant_layer_ids
    staticmethod with the model explicitly, since staticmethods do not
    receive an implicit `self`/`model` argument through `self.<name>(...)`.
    """
    model = ThreeDiPluginModel()

    # A minimal stand-in for GraphDockWidget: only the attributes touched by
    # add_results() when there are no results to add.
    fake_widget = SimpleNamespace(
        model=model,
        q_graph_widget=None,
        h_graph_widget=None,
        _get_relevant_layer_ids=GraphDockWidget._get_relevant_layer_ids,
    )

    # Must not raise (previously raised TypeError: missing 'layer_keys').
    GraphDockWidget.add_results(fake_widget, [], feature_type=NODE_OR_CELL)
