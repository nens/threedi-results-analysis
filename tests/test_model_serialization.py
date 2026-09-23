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


def _serialize_model(model):
    document = QDomDocument()
    document.setContent("<qgis/>")
    success, _ = ThreeDiPluginModelSerializer.write(model, document, IdentityResolver())
    assert success
    root = document.elementsByTagName(TOOLBOX_XML_ELEMENT_ROOT).at(0)
    assert not root.isNull()
    return root


def test_grouped_result_serializes_display_path_and_owned_layers():
    model = ThreeDiPluginModel()
    grid = ThreeDiGridItem(Path("c:/grid/gridadmin.gpkg"), "grid")
    grid.layer_ids["node"] = "grid-node-id"
    result = ThreeDiResultItem(Path("c:/result/results_3di.nc"))
    result.setCheckState(Qt.CheckState.Checked)
    result.group_path = ["project", "files", "result.zip"]
    result.layer_ids = {"node": "result-node-id", "flowline": "result-flowline-id"}
    assert model.add_grid(grid)
    assert model.add_result(result, grid)

    grid_element = _serialize_model(model).firstChildElement("grid")
    result_element = grid_element.firstChildElement("result")

    assert result_element.attribute("path") == "resolved:c:/result/results_3di.nc"
    assert result_element.attribute("group_path") == "project/files/result.zip"
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


def test_legacy_result_omits_grouped_metadata():
    model = ThreeDiPluginModel()
    grid = ThreeDiGridItem(Path("c:/grid/gridadmin.gpkg"), "grid")
    result = ThreeDiResultItem(Path("c:/result/results_3di.nc"))
    assert model.add_grid(grid)
    assert model.add_result(result, grid)

    result_element = (
        _serialize_model(model).firstChildElement("grid").firstChildElement("result")
    )

    assert not result_element.hasAttribute("group_path")
    assert result_element.elementsByTagName("layer").length() == 0
