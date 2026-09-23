from pathlib import Path
from uuid import uuid4

from qgis.core import QgsLayerTreeGroup, QgsProject

from threedi_results_analysis.threedi_plugin_layer_manager import (
    GRID_GROUP_NAME,
    ThreeDiPluginLayerManager,
)
from threedi_results_analysis.threedi_plugin_model import (
    ThreeDiGridItem,
    ThreeDiResultItem,
)


def test_grouped_result_uses_direct_group_path():
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
