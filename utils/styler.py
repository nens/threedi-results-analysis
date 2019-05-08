import logging
import os

logger = logging.getLogger(__name__)

STYLES_ROOT = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "layer_styles"
)


def apply_style(layer, style_name, stype="tools"):
    style = os.path.join(STYLES_ROOT, stype, "{0}.qml".format(style_name))
    if os.path.exists(style):
        layer.loadNamedStyle(style)
    else:
        logger.info("Style not exist {0}".format(style))
    return
