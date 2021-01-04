import logging
import os

from qgis.core import QgsMapLayerStyle

logger = logging.getLogger(__name__)

STYLES_ROOT = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "layer_styles"
)


def apply_style(layer, style_name, stype="tools"):
    qml_path = os.path.join(STYLES_ROOT, stype, style_name)

    style_manager = layer.styleManager()
    style_manager.reset()

    style = QgsMapLayerStyle()
    style.readFromLayer(layer)

    current_style_name = layer.styleManager().currentStyle()  # default style name depends on language settings

    for qml_file in [f for f in os.listdir(qml_path)
                     if os.path.isfile(os.path.join(qml_path, f)) and
                     f.endswith('.qml')]:
        style_name = os.path.basename(qml_file)[:-4].capitalize()
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
