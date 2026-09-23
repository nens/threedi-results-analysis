import shutil
from pathlib import Path
from uuid import uuid4

from qgis.core import QgsLayerTreeGroup, QgsProject, QgsVectorLayer

from threedi_results_analysis.threedi_plugin_layer_manager import (
    GRID_GROUP_NAME,
    ThreeDiPluginLayerManager,
    WATERDEPTH_GROUP_NAME,
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


def test_legacy_result_unload_keeps_grid_layers():
    """Legacy result removal still leaves the grid-owned layer in place."""
    project = QgsProject.instance()
    layer = QgsVectorLayer("Point?crs=EPSG:28992", "Node", "memory")
    assert layer.isValid()
    project.addMapLayer(layer, addToLegend=False)

    grid_item = ThreeDiGridItem(Path("c:/test/gridadmin.gpkg"), "grid")
    grid_item.layer_ids["node"] = layer.id()
    result_item = ThreeDiResultItem(Path("c:/test/results_3di.nc"))
    grid_item.appendRow(result_item)

    try:
        manager = ThreeDiPluginLayerManager()
        assert manager.load_result(result_item, grid_item)
        assert manager.unload_result(result_item)
        assert project.mapLayer(layer.id()) is not None
        assert layer.id() in grid_item.layer_ids.values()
    finally:
        project.removeMapLayer(layer.id())


def test_grouped_result_aliases_fields_and_resets_its_own_style(tmp_path):
    """Grouped field and style changes stay isolated from a sibling result.

    Both results share one logical grid, but each result owns a separate set of
    QGIS layers. The test changes only the first result and verifies that the
    second result is unaffected.
    """
    # Copy the source GeoPackage so the test can open it without creating
    # SQLite sidecar files next to the committed fixture.
    source_gpkg_path = (
        Path(__file__).parent
        / "data"
        / "testmodel"
        / "v2_bergermeer"
        / "gridadmin.gpkg"
    )
    gpkg_path = tmp_path / "gridadmin.gpkg"
    shutil.copy(source_gpkg_path, gpkg_path)
    group_root = f"task6-{uuid4().hex}"

    # Keep both results under one model grid while giving them different QGIS
    # layer-tree paths. This is the distinction the grouped ownership model
    # must preserve.
    grid_item = ThreeDiGridItem(gpkg_path, "grid")
    result_items = []
    for result_name, result_text in (
        ("result-a.zip", "Result A"),
        ("result-b.zip", "Result B"),
    ):
        result_item = ThreeDiResultItem(Path(f"c:/{result_name}/results_3di.nc"))
        result_item.group_path = [group_root, result_name]
        result_item.setText(result_text)
        grid_item.appendRow(result_item)
        result_items.append(result_item)

    project = QgsProject.instance()
    root = project.layerTreeRoot()

    try:
        manager = ThreeDiPluginLayerManager()

        # Loading creates independent memory layers and adds each result's
        # dynamic fields to its own layer set.
        for result_item in result_items:
            assert manager.load_result(result_item, grid_item)

        first_result, second_result = result_items
        first_layer_id = first_result.layer_ids["node"]
        second_layer_id = second_result.layer_ids["node"]
        first_layer = project.mapLayer(first_layer_id)
        second_layer = project.mapLayer(second_layer_id)

        # Users cannot edit generated computational-grid layers. The manager
        # may still remove the dynamic fields it created during result cleanup.
        assert first_layer.readOnly()
        assert second_layer.readOnly()

        first_field_names = first_result._result_field_names[first_layer_id]
        second_field_names = second_result._result_field_names[second_layer_id]

        # Each result has its own fields and receives its own initial aliases;
        # the two results must not share field state through the parent grid.
        assert all(
            first_layer.fields().indexFromName(name) != -1 for name in first_field_names
        )
        assert all(
            second_layer.fields().indexFromName(name) != -1
            for name in second_field_names
        )
        assert first_layer.fields().field(first_field_names[0]).alias() == "Result A"
        assert second_layer.fields().field(second_field_names[0]).alias() == "Result B"

        # Renaming the first result updates only aliases on the first result's
        # layers. The sibling retains its original display name.
        first_result.setText("Renamed A")
        manager.update_result(first_result)
        assert first_layer.fields().field(first_field_names[0]).alias() == "Renamed A"
        assert second_layer.fields().field(second_field_names[0]).alias() == "Result B"

        # result_unchecked() must reset styling/name state on the selected
        # grouped result, not on the sibling's independently owned layers.
        first_layer.setName("Changed layer name")
        second_layer.setName("Sibling layer name")
        manager.result_unchecked(first_result)
        assert first_layer.name() == "Node"
        assert second_layer.name() == "Sibling layer name"

        # Removing the first result invokes internal cleanup of its generated
        # fields and (for grouped results) its owned layers.
        assert manager.unload_result(first_result)
        assert all(
            second_layer.fields().indexFromName(name) != -1
            for name in second_field_names
        )
        assert not first_result.layer_ids
        assert project.mapLayer(first_layer_id) is None
        assert project.mapLayer(second_layer_id) is not None
    finally:
        # The test owns both temporary result layer sets and their group tree.
        for result_item in result_items:
            for layer_id in result_item.layer_ids.values():
                project.removeMapLayer(layer_id)
        root.removeChildNode(root.findGroup(group_root))


def test_grouped_result_unload_prunes_empty_ancestors(tmp_path):
    """Removing the only grouped result prunes its empty path hierarchy."""
    source_gpkg_path = (
        Path(__file__).parent
        / "data"
        / "testmodel"
        / "v2_bergermeer"
        / "gridadmin.gpkg"
    )
    gpkg_path = tmp_path / "gridadmin.gpkg"
    shutil.copy(source_gpkg_path, gpkg_path)
    group_path = [f"task7-{uuid4().hex}", "files", "result.zip"]
    grid_item = ThreeDiGridItem(gpkg_path, "grid")
    result_item = ThreeDiResultItem(Path("c:/result.zip/results_3di.nc"))
    result_item.group_path = group_path
    grid_item.appendRow(result_item)

    project = QgsProject.instance()
    root = project.layerTreeRoot()

    try:
        manager = ThreeDiPluginLayerManager()
        assert manager.load_result(result_item, grid_item)
        layer_ids = set(result_item.layer_ids.values())

        assert manager.unload_result(result_item)

        assert not result_item.layer_ids
        assert result_item.layer_group is None
        assert all(project.mapLayer(layer_id) is None for layer_id in layer_ids)
        assert root.findGroup(group_path[0]) is None
    finally:
        group = root.findGroup(group_path[0])
        if group is not None:
            root.removeChildNode(group)


def test_grouped_result_unload_preserves_sibling_and_external_layer(tmp_path):
    """Removal preserves sibling results and external shared-ancestor layers."""
    source_gpkg_path = (
        Path(__file__).parent
        / "data"
        / "testmodel"
        / "v2_bergermeer"
        / "gridadmin.gpkg"
    )
    gpkg_path = tmp_path / "gridadmin.gpkg"
    shutil.copy(source_gpkg_path, gpkg_path)
    group_root = f"task7-{uuid4().hex}"
    grid_item = ThreeDiGridItem(gpkg_path, "grid")
    result_items = []
    for result_name in ("result-a.zip", "result-b.zip"):
        result_item = ThreeDiResultItem(Path(f"c:/{result_name}/results_3di.nc"))
        result_item.group_path = [group_root, result_name]
        grid_item.appendRow(result_item)
        result_items.append(result_item)

    project = QgsProject.instance()
    root = project.layerTreeRoot()
    external_layer = QgsVectorLayer("Point?crs=EPSG:28992", "External", "memory")
    assert external_layer.isValid()
    project.addMapLayer(external_layer, addToLegend=False)

    try:
        manager = ThreeDiPluginLayerManager()
        for result_item in result_items:
            assert manager.load_result(result_item, grid_item)

        common_group = root.findGroup(group_root)
        assert common_group is not None
        common_group.addLayer(external_layer)

        first_result, second_result = result_items
        first_layer_ids = set(first_result.layer_ids.values())
        second_layer_ids = set(second_result.layer_ids.values())
        assert manager.unload_result(first_result)

        # Only the removed result's QGIS layers and final group are gone.
        assert all(project.mapLayer(layer_id) is None for layer_id in first_layer_ids)
        assert all(
            project.mapLayer(layer_id) is not None for layer_id in second_layer_ids
        )
        assert first_result.layer_group is None
        assert second_result.layer_group is not None
        assert root.findGroup(group_root).findGroup("result-a.zip") is None
        assert root.findGroup(group_root).findGroup("result-b.zip") is not None

        # The shared ancestor remains because it contains both the sibling and
        # an externally added layer.
        assert project.mapLayer(external_layer.id()) is not None
        assert root.findGroup(group_root).findLayer(external_layer.id()) is not None
    finally:
        for result_item in result_items:
            for layer_id in result_item.layer_ids.values():
                project.removeMapLayer(layer_id)
        project.removeMapLayer(external_layer.id())
        group = root.findGroup(group_root)
        if group is not None:
            root.removeChildNode(group)


def test_grouped_waterdepth_is_owned_and_removed_independently(tmp_path):
    """Grouped Waterdepth layers live below and belong to their result group."""
    source_gpkg_path = (
        Path(__file__).parent
        / "data"
        / "testmodel"
        / "v2_bergermeer"
        / "gridadmin.gpkg"
    )
    source_raster_path = Path(__file__).parent / "data" / "rasters" / "test1.tif"
    gpkg_path = tmp_path / "gridadmin.gpkg"
    shutil.copy(source_gpkg_path, gpkg_path)

    result_dirs = []
    for result_name in ("result-a", "result-b"):
        result_dir = tmp_path / result_name
        result_dir.mkdir()
        shutil.copy(source_raster_path, result_dir / "max_waterdepth.tif")
        result_dirs.append(result_dir)

    group_root = f"task8-{uuid4().hex}"
    grid_item = ThreeDiGridItem(gpkg_path, "grid")
    result_items = []
    for result_dir in result_dirs:
        result_item = ThreeDiResultItem(result_dir / "results_3di.nc")
        result_item.group_path = [group_root, f"{result_dir.name}.zip"]
        grid_item.appendRow(result_item)
        result_items.append(result_item)

    project = QgsProject.instance()
    root = project.layerTreeRoot()
    manager = ThreeDiPluginLayerManager()
    waterdepth_ids = []

    try:
        for result_item in result_items:
            assert manager.load_result(result_item, grid_item)
            manager.load_waterdepth(result_item)
            assert result_item.waterdepth_layer_id
            waterdepth_ids.append(result_item.waterdepth_layer_id)

        assert waterdepth_ids[0] != waterdepth_ids[1]
        grouped_root = root.findGroup(group_root)
        assert grouped_root is not None

        for result_item in result_items:
            result_group = grouped_root.findGroup(f"{result_item.path.parent.name}.zip")
            assert result_group is not None
            assert result_group.findGroup(WATERDEPTH_GROUP_NAME) is not None
            assert result_item.layer_group is result_group
            assert result_group.findGroup(GRID_GROUP_NAME) is not None

        # The normal result-removal signal order calls unload_result first and
        # unload_waterdepth second. The latter must still find result A's group.
        first_result, second_result = result_items
        first_waterdepth_id, second_waterdepth_id = waterdepth_ids
        assert manager.unload_result(first_result)
        manager.unload_waterdepth(first_result)

        assert first_result.waterdepth_layer_id is None
        assert project.mapLayer(first_waterdepth_id) is None
        assert project.mapLayer(second_waterdepth_id) is not None
        assert grouped_root.findGroup("result-a.zip") is None
        assert grouped_root.findGroup("result-b.zip") is not None
        assert grouped_root.findGroup("result-b.zip").findGroup(WATERDEPTH_GROUP_NAME)
    finally:
        for result_item in result_items:
            for layer_id in result_item.layer_ids.values():
                project.removeMapLayer(layer_id)
            if result_item.waterdepth_layer_id:
                project.removeMapLayer(result_item.waterdepth_layer_id)
        group = root.findGroup(group_root)
        if group is not None:
            root.removeChildNode(group)


def test_legacy_waterdepth_stays_under_grid_group(tmp_path):
    """Legacy Waterdepth placement remains owned by the parent grid group."""
    source_raster_path = Path(__file__).parent / "data" / "rasters" / "test1.tif"
    result_dir = tmp_path / "legacy-result"
    result_dir.mkdir()
    shutil.copy(source_raster_path, result_dir / "max_waterdepth.tif")

    grid_item = ThreeDiGridItem(tmp_path / "gridadmin.gpkg", "grid")
    result_item = ThreeDiResultItem(result_dir / "results_3di.nc")
    grid_item.appendRow(result_item)
    manager = ThreeDiPluginLayerManager()
    grid_item.layer_group = manager._get_or_create_group(f"task8-{uuid4().hex}")
    root = QgsProject.instance().layerTreeRoot()
    group = grid_item.layer_group

    try:
        manager.load_waterdepth(result_item)

        assert result_item.waterdepth_layer_id
        assert group.findGroup(WATERDEPTH_GROUP_NAME) is not None
        assert result_item.layer_group is None
        assert manager.unload_waterdepth(result_item) is None
        assert result_item.waterdepth_layer_id is None
        assert group.findGroup(WATERDEPTH_GROUP_NAME) is None
    finally:
        if result_item.waterdepth_layer_id:
            QgsProject.instance().removeMapLayer(result_item.waterdepth_layer_id)
        if group is not None and group.parent() is not None:
            root_group = root.findGroup(group.parent().name())
            if root_group is not None:
                root.removeChildNode(root_group)


def test_grouped_layer_restore_reuses_existing_layer_ids(tmp_path):
    """Restoring valid grouped IDs reuses layers instead of creating duplicates."""
    source_gpkg_path = (
        Path(__file__).parent
        / "data"
        / "testmodel"
        / "v2_bergermeer"
        / "gridadmin.gpkg"
    )
    gpkg_path = tmp_path / "gridadmin.gpkg"
    shutil.copy(source_gpkg_path, gpkg_path)
    group_path = [f"task12-{uuid4().hex}", "files", "result.zip"]
    grid_item = ThreeDiGridItem(gpkg_path, "grid")
    original_result = ThreeDiResultItem(Path("c:/result/results_3di.nc"))
    original_result.group_path = group_path
    grid_item.appendRow(original_result)

    project = QgsProject.instance()
    root = project.layerTreeRoot()
    manager = ThreeDiPluginLayerManager()

    try:
        assert manager.load_result(original_result, grid_item)
        stored_layer_ids = dict(original_result.layer_ids)
        stored_feature_counts = {
            table_name: project.mapLayer(layer_id).featureCount()
            for table_name, layer_id in stored_layer_ids.items()
        }
        initial_project_layer_ids = set(project.mapLayers())

        restored_result = ThreeDiResultItem(Path("c:/result/results_3di.nc"))
        restored_result.group_path = list(group_path)
        restored_result.layer_ids = dict(stored_layer_ids)
        grid_item.appendRow(restored_result)

        assert manager.load_result(restored_result, grid_item)
        assert restored_result.layer_ids == stored_layer_ids
        assert set(project.mapLayers()) == initial_project_layer_ids
        assert {
            table_name: project.mapLayer(layer_id).featureCount()
            for table_name, layer_id in restored_result.layer_ids.items()
        } == stored_feature_counts
        assert {
            layer_node.layerId()
            for layer_node in restored_result.layer_group.findGroup(
                GRID_GROUP_NAME
            ).findLayers()
        } == set(stored_layer_ids.values())
    finally:
        for layer_id in stored_layer_ids if "stored_layer_ids" in locals() else []:
            project.removeMapLayer(layer_id)
        group = root.findGroup(group_path[0])
        if group is not None:
            root.removeChildNode(group)
