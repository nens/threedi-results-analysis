from pathlib import Path

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtXml import QDomDocument

from threedi_results_analysis.threedi_plugin_model import (
    ThreeDiGridItem,
    ThreeDiPluginModel,
    ThreeDiResultItem,
)
from threedi_results_analysis.threedi_plugin_model_serialization import (
    ThreeDiPluginModelSerializer,
)
from threedi_results_analysis.utils.constants import TOOLBOX_XML_ELEMENT_ROOT


class IdentityResolver:
    def writePath(self, path):
        return f"resolved:{path}"

    def readPath(self, path):
        return path.removeprefix("resolved:")


class RecordingLoader:
    def __init__(self):
        self.grids = []
        self.results = []

    def load_grid(self, grid_item, project=None):
        self.grids.append((grid_item, project))
        return True

    def load_result(self, result_item, grid_item):
        self.results.append((result_item, grid_item))
        return True


def _serialize_model(model):
    document = QDomDocument()
    document.setContent("<qgis/>")
    success, _ = ThreeDiPluginModelSerializer.write(model, document, IdentityResolver())
    assert success
    root = document.elementsByTagName(TOOLBOX_XML_ELEMENT_ROOT).at(0)
    assert not root.isNull()
    return root


def test_isolated_result_serializes_display_path_and_owned_layers():
    model = ThreeDiPluginModel()
    grid = ThreeDiGridItem(Path("c:/grid/gridadmin.gpkg"), "grid")
    grid.layer_ids["node"] = "grid-node-id"
    result = ThreeDiResultItem(Path("c:/result/results_3di.nc"))
    result.setCheckState(Qt.CheckState.Checked)
    result.layer_path = ["project", "files", "result.zip"]
    result.layer_ids = {"node": "result-node-id", "flowline": "result-flowline-id"}
    assert model.add_grid(grid)
    assert model.add_result(result, grid)

    grid_element = _serialize_model(model).firstChildElement("grid")
    result_element = grid_element.firstChildElement("result")

    assert result_element.attribute("path") == "resolved:c:/result/results_3di.nc"
    assert result_element.attribute("layer_path") == "project/files/result.zip"
    assert result_element.attribute("check_state") == "2"
    layers = result_element.elementsByTagName("layer")
    assert layers.length() == 2
    assert {
        (
            layers.at(index).toElement().attribute("table_name"),
            layers.at(index).toElement().attribute("id"),
        )
        for index in range(layers.length())
    } == {
        ("node", "result-node-id"),
        ("flowline", "result-flowline-id"),
    }

    grid_layer = grid_element.firstChildElement("layer")
    assert grid_layer.attribute("id") == "grid-node-id"


def test_standalone_result_omits_isolated_metadata():
    model = ThreeDiPluginModel()
    grid = ThreeDiGridItem(Path("c:/grid/gridadmin.gpkg"), "grid")
    result = ThreeDiResultItem(Path("c:/result/results_3di.nc"))
    assert model.add_grid(grid)
    assert model.add_result(result, grid)

    result_element = (
        _serialize_model(model).firstChildElement("grid").firstChildElement("result")
    )

    assert not result_element.hasAttribute("layer_path")
    assert result_element.elementsByTagName("layer").length() == 0


def test_isolated_result_read_restores_path_and_owned_layers():
    model = ThreeDiPluginModel()
    grid = ThreeDiGridItem(Path("c:/grid/gridadmin.gpkg"), "grid")
    grid.layer_ids["node"] = "grid-node-id"
    result = ThreeDiResultItem(Path("c:/result/results_3di.nc"))
    result.layer_path = ["project", "files", "result.zip"]
    result.layer_ids = {"node": "result-node-id", "flowline": "result-flowline-id"}
    assert model.add_grid(grid)
    assert model.add_result(result, grid)
    document = QDomDocument()
    document.setContent("<qgis/>")
    assert ThreeDiPluginModelSerializer.write(model, document, IdentityResolver())[0]

    loader = RecordingLoader()
    assert ThreeDiPluginModelSerializer.read(loader, document, IdentityResolver())[0]

    restored_grid = loader.grids[0][0]
    restored_result, result_parent = loader.results[0]
    assert restored_grid.layer_ids == {"node": "grid-node-id"}
    assert restored_result.layer_path == ["project", "files", "result.zip"]
    assert restored_result.layer_ids == {
        "node": "result-node-id",
        "flowline": "result-flowline-id",
    }
    assert result_parent is restored_grid


def test_legacy_enum_check_state_is_read():
    document = QDomDocument()
    document.setContent(
        """<qgis><threediPluginModel>
        <grid id="grid" path="resolved:c:/grid/gridadmin.gpkg" text="grid">
            <result id="result" path="resolved:c:/result/results_3di.nc"
                    text="result" check_state="CheckState.Checked"/>
        </grid>
        </threediPluginModel></qgis>"""
    )

    loader = RecordingLoader()
    assert ThreeDiPluginModelSerializer.read(loader, document, IdentityResolver())[0]
    assert loader.results[0][0].checkState() == Qt.CheckState.Checked


def test_legacy_group_path_is_read_as_layer_path():
    document = QDomDocument()
    document.setContent(
        """<qgis><threediPluginModel>
        <grid id="grid" path="resolved:c:/grid/gridadmin.gpkg" text="grid">
            <result id="result" path="resolved:c:/result/results_3di.nc"
                    text="result" group_path="files/result.zip"/>
        </grid>
        </threediPluginModel></qgis>"""
    )

    loader = RecordingLoader()
    assert ThreeDiPluginModelSerializer.read(loader, document, IdentityResolver())[0]
    assert loader.results[0][0].layer_path == ["files", "result.zip"]


def test_missing_check_state_defaults_to_unchecked():
    document = QDomDocument()
    document.setContent(
        """<qgis><threediPluginModel>
        <grid id="grid" path="resolved:c:/grid/gridadmin.gpkg" text="grid">
            <result id="result" path="resolved:c:/result/results_3di.nc"
                    text="result"/>
        </grid>
        </threediPluginModel></qgis>"""
    )

    loader = RecordingLoader()
    assert ThreeDiPluginModelSerializer.read(loader, document, IdentityResolver())[0]
    assert loader.results[0][0].checkState() == Qt.CheckState.Unchecked


def test_standalone_result_read_does_not_claim_grid_layers():
    model = ThreeDiPluginModel()
    grid = ThreeDiGridItem(Path("c:/grid/gridadmin.gpkg"), "grid")
    grid.layer_ids["node"] = "grid-node-id"
    result = ThreeDiResultItem(Path("c:/result/results_3di.nc"))
    assert model.add_grid(grid)
    assert model.add_result(result, grid)
    document = QDomDocument()
    document.setContent("<qgis/>")
    assert ThreeDiPluginModelSerializer.write(model, document, IdentityResolver())[0]

    loader = RecordingLoader()
    assert ThreeDiPluginModelSerializer.read(loader, document, IdentityResolver())[0]

    restored_result = loader.results[0][0]
    assert restored_result.layer_path is None
    assert restored_result.layer_ids == {}


def test_grid_with_only_isolated_results_restores_as_deferred():
    """Restoring a project where every result under a grid is isolated must
    not eagerly recreate the grid's own (shared) layers on reopen."""
    model = ThreeDiPluginModel()
    grid = ThreeDiGridItem(Path("c:/grid/gridadmin.gpkg"), "grid")
    result_a = ThreeDiResultItem(Path("c:/result-a/results_3di.nc"))
    result_a.layer_path = ["files", "result-a.zip"]
    result_b = ThreeDiResultItem(Path("c:/result-b/results_3di.nc"))
    result_b.layer_path = ["files", "result-b.zip"]
    assert model.add_grid(grid)
    assert model.add_result(result_a, grid)
    assert model.add_result(result_b, grid)

    document = QDomDocument()
    document.setContent("<qgis/>")
    assert ThreeDiPluginModelSerializer.write(model, document, IdentityResolver())[0]

    loader = RecordingLoader()
    assert ThreeDiPluginModelSerializer.read(loader, document, IdentityResolver())[0]

    restored_grid = loader.grids[0][0]
    assert restored_grid.defer_layer_creation is True


def test_grid_with_a_standalone_result_does_not_restore_as_deferred():
    """If any result under a grid is non-isolated, the grid's own layers are
    needed and must not be deferred on restore."""
    model = ThreeDiPluginModel()
    grid = ThreeDiGridItem(Path("c:/grid/gridadmin.gpkg"), "grid")
    isolated_result = ThreeDiResultItem(Path("c:/result-a/results_3di.nc"))
    isolated_result.layer_path = ["files", "result-a.zip"]
    standalone_result = ThreeDiResultItem(Path("c:/result-b/results_3di.nc"))
    assert model.add_grid(grid)
    assert model.add_result(isolated_result, grid)
    assert model.add_result(standalone_result, grid)

    document = QDomDocument()
    document.setContent("<qgis/>")
    assert ThreeDiPluginModelSerializer.write(model, document, IdentityResolver())[0]

    loader = RecordingLoader()
    assert ThreeDiPluginModelSerializer.read(loader, document, IdentityResolver())[0]

    restored_grid = loader.grids[0][0]
    assert restored_grid.defer_layer_creation is False
