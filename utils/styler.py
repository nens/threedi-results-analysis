import logging
import os
from pathlib import Path

from qgis.core import QgsMapLayerStyle

logger = logging.getLogger(__name__)

STYLES_ROOT = Path(__file__).parent.parent / "layer_styles"


def apply_style(layer, style_name, stype="tools"):
    qml_path = STYLES_ROOT / stype / style_name

    style_manager = layer.styleManager()
    style_manager.reset()

    style = QgsMapLayerStyle()
    style.readFromLayer(layer)

    current_style_name = layer.styleManager().currentStyle()  # default style name depends on language settings

    for qml_file in qml_path.glob("*.qml"):
        style_name = qml_file.stem.capitalize()
        style_manager.addStyle(style_name, style)
        style_manager.setCurrentStyle(style_name)
        (message, success) = layer.loadNamedStyle(os.path.join(qml_path, qml_file))

        if not success:  # if style not loaded remove it
            style_manager.removeStyle(style_name)
            logger.info("Styling file not succesfully loaded: {fn}".format(fn=qml_file))
            logger.info(message)

    layer.styleManager().setCurrentStyle('Default')
    layer.styleManager().removeStyle(current_style_name)
    return
