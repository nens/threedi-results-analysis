import shutil
from pathlib import Path
from uuid import uuid4

from qgis.core import QgsLayerTreeGroup, QgsProject, QgsVectorLayer

from threedi_results_analysis.threedi_plugin_layer_manager import (
    GRID_GROUP_NAME,
    ThreeDiPluginLayerManager,
    gpkg_layers,
)
from threedi_results_analysis.threedi_plugin_model import (
    ThreeDiGridItem,
    ThreeDiResultItem,
)


def test_grouped_result_uses_direct_group_path():
    """A grouped result gets the exact path and a computational-grid subgroup."""
    group_path = [f"task4-{uuid4().hex}", "files", "result.zip"]
    grid_item = ThreeDiGridItem(Path("c:/test/gridadmin.gpkg"), "grid")
    result_item = ThreeDiResultItem(Path("c:/test/results_3di.nc"))
    result_item.group_path = group_path
    grid_item.appendRow(result_item)
    root = QgsProject.instance().layerTreeRoot()

    try:
        assert ThreeDiPluginLayerManager().load_result(result_item, grid_item)

        current_group = root
        for group_name in group_path:
            matching_groups = [
                child
                for child in current_group.children()
                if isinstance(child, QgsLayerTreeGroup) and child.name() == group_name
            ]
            assert len(matching_groups) == 1
            current_group = matching_groups[0]

        assert result_item.layer_group is current_group
        assert [child.name() for child in current_group.children()] == [GRID_GROUP_NAME]
    finally:
        root.removeChildNode(root.findGroup(group_path[0]))


def test_grouped_results_get_independent_grid_layers(tmp_path):
    """Two results sharing a GeoPackage receive separate QGIS layer sets."""
    # Work on a copy because opening a GeoPackage through QGIS may create
    # SQLite sidecar files next to it.
    source_gpkg_path = (
        Path(__file__).parent
        / "data"
        / "testmodel"
        / "v2_bergermeer"
        / "gridadmin.gpkg"
    )
    gpkg_path = tmp_path / "gridadmin.gpkg"
    shutil.copy(source_gpkg_path, gpkg_path)
    group_root = f"task5-{uuid4().hex}"

    # Both results use the same logical grid but represent different source
    # files, so each receives a different result-owned layer subtree.
    grid_item = ThreeDiGridItem(gpkg_path, "grid")
    result_items = []
    for result_name in ("result-a.zip", "result-b.zip"):
        result_item = ThreeDiResultItem(Path(f"c:/{result_name}/results_3di.nc"))
        result_item.group_path = [group_root, result_name]
        grid_item.appendRow(result_item)
        result_items.append(result_item)

    project = QgsProject.instance()
    root = project.layerTreeRoot()
    initial_layer_ids = set(project.mapLayers())

    try:
        manager = ThreeDiPluginLayerManager()

        # Loading each result must copy from the shared GeoPackage instead of
        # reusing another result's mutable memory layers.
        for result_item in result_items:
            assert manager.load_result(result_item, grid_item)

        # Derive the expected tables from the source because some computational
        # grid tables are legitimately empty and are skipped by the loader.
        expected_tables = set()
        for table_name in gpkg_layers.values():
            source_layer = QgsVectorLayer(
                f"{gpkg_path}|layername={table_name}", table_name, "ogr"
            )
            if source_layer.isValid() and source_layer.featureCount():
                expected_tables.add(table_name)

        result_layer_ids = [
            set(result_item.layer_ids.values()) for result_item in result_items
        ]
        assert all(result_layer_ids)

        # The two result-owned layer sets must not share any QGIS layer object.
        assert result_layer_ids[0].isdisjoint(result_layer_ids[1])
        assert all(
            set(result_item.layer_ids) == expected_tables
            for result_item in result_items
        )

        added_layer_ids = set(project.mapLayers()) - initial_layer_ids
        assert added_layer_ids == result_layer_ids[0] | result_layer_ids[1]

        # Each result's layers belong to its own Computational grid group and
        # have the result fields added to that independent memory layer.
        for result_item in result_items:
            grid_group = result_item.layer_group.findGroup(GRID_GROUP_NAME)
            assert grid_group is not None
            assert {
                layer_tree_layer.layerId()
                for layer_tree_layer in grid_group.findLayers()
            } == set(result_item.layer_ids.values())

            for layer_id in result_item.layer_ids.values():
                layer = project.mapLayer(layer_id)
                assert layer is not None
                assert layer.providerType() == "memory"
                assert layer.isValid()
                assert set(result_item._result_field_names[layer_id]).issubset(
                    {field.name() for field in layer.fields()}
                )
    finally:
        # Remove all QGIS objects created by this test, including both layer
        # instances and their temporary source-file groups.
        for result_item in result_items:
            for layer_id in result_item.layer_ids.values():
                project.removeMapLayer(layer_id)
        root.removeChildNode(root.findGroup(group_root))


def test_legacy_result_load_uses_grid_layers_before_model_addition():
    """Legacy loading still targets grid layers before model insertion."""
    project = QgsProject.instance()
    layer = QgsVectorLayer("Point?crs=EPSG:28992", "Node", "memory")
    assert layer.isValid()
    project.addMapLayer(layer, addToLegend=False)

    grid_item = ThreeDiGridItem(Path("c:/test/gridadmin.gpkg"), "grid")
    grid_item.layer_ids["node"] = layer.id()
    result_item = ThreeDiResultItem(Path("c:/test/results_3di.nc"))

    try:
        assert ThreeDiPluginLayerManager().load_result(result_item, grid_item)
        result_field_names = result_item._result_field_names[layer.id()]
        assert all(
            layer.fields().indexFromName(name) != -1 for name in result_field_names
        )
    finally:
        project.removeMapLayer(layer.id())
