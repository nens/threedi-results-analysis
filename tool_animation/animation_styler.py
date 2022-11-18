from pathlib import Path
from qgis.core import QgsMapLayerStyle
from qgis.core import QgsVectorLayer
from qgis.utils import iface
from ThreeDiToolbox.datasource.result_constants import WET_CROSS_SECTION_AREA
from ThreeDiToolbox.utils.color import COLOR_RAMP_OCEAN_CURL
from ThreeDiToolbox.utils.color import COLOR_RAMP_OCEAN_DEEP
from ThreeDiToolbox.utils.color import COLOR_RAMP_OCEAN_HALINE
from ThreeDiToolbox.utils.color import color_ramp_from_data
from typing import List

import logging
import numpy as np
import os


STYLES_ROOT = Path(__file__).parent / "layer_styles"
ANIMATION_LAYERS_NR_LEGEND_CLASSES = 24
assert ANIMATION_LAYERS_NR_LEGEND_CLASSES % 2 == 0

logger = logging.getLogger(__name__)


def style_animation_flowline_current(
    lyr: QgsVectorLayer, class_bounds: List[float], variable
):
    """Applies styling to Animation Toolbar flowline layer in 'current' mode"""

    # Load basic style settings from qml file
    qml_path = STYLES_ROOT / "flowline_current.qml"
    lyr.loadNamedStyle(str(qml_path))
    renderer = lyr.renderer()

    # Set correct legend symbol rotation
    symbol = renderer.sourceSymbol().clone()
    if variable == WET_CROSS_SECTION_AREA.name:
        symbol.deleteSymbolLayer(1)
        max_symbol_size = 1.5
    else:
        symbol.symbolLayers()[1].setSymbolAngle(90)
        max_symbol_size = 2.5
    renderer.updateSymbols(symbol)

    # Set classes and colors
    color_ramp = color_ramp_from_data(COLOR_RAMP_OCEAN_DEEP)
    renderer.deleteAllClasses()
    nr_classes = len(class_bounds) - 1
    for i in range(nr_classes):
        renderer.addClassLowerUpper(lower=class_bounds[i], upper=class_bounds[i + 1])
        class_middle = (class_bounds[i] + class_bounds[i + 1]) / 2
        symbol = renderer.symbolForValue(class_middle).clone()
        color_ramp_fraction = (i + 0.5) / nr_classes
        color = color_ramp.color(color_ramp_fraction)
        symbol.setColor(color)
        renderer.setLegendSymbolItem(str(i), symbol)

    # Symbol size
    renderer.setSymbolSizes(0.1, max_symbol_size)

    # Add velocity thresholds style
    style_manager = lyr.styleManager()
    lyr.styleManager().removeStyle("Thresholds")
    if variable == "u1":
        default_style_name = (
            style_manager.currentStyle()
        )  # default style name depends on language settings
        style_name = "Thresholds"
        qml_path = (
            STYLES_ROOT / "velocity_thresholds.qml"
        )
        style = QgsMapLayerStyle()
        style.readFromLayer(lyr)
        style_manager.addStyle(style_name, style)
        style_manager.setCurrentStyle(style_name)
        (message, success) = lyr.loadNamedStyle(os.path.join(qml_path, qml_path))
        if not success:  # if style not loaded remove it
            style_manager.removeStyle(style_name)
            logger.info("Styling file not succesfully loaded: {fn}".format(fn=qml_path))
            logger.info(message)
        style_manager.setCurrentStyle(default_style_name)

    iface.layerTreeView().refreshLayerSymbology(lyr.id())
    lyr.triggerRepaint()


def style_animation_node_current(
    lyr: QgsVectorLayer, percentiles: List[float], variable: str, cells: bool = False
):
    """Applies styling to Animation Toolbar node layer in 'current' mode"""

    # Load basic style settings from qml file
    if cells:
        qml_path = STYLES_ROOT / "cell_current.qml"
    else:
        qml_path = STYLES_ROOT / "node_current.qml"
    lyr.loadNamedStyle(str(qml_path))
    renderer = lyr.renderer()

    # Set classes
    if variable == "s1":
        class_attribute_str = "coalesce(result, z_coordinate)"
    else:
        class_attribute_str = "result"
    lyr.renderer().setClassAttribute(class_attribute_str)
    renderer.deleteAllClasses()
    nr_classes = len(percentiles) - 1
    percentiles[0] = float(
        -9999
    )  # to make nodes / cells also visible when dry and z_coordinate < percentile[0]
    for i in range(nr_classes):
        renderer.addClassLowerUpper(lower=percentiles[i], upper=percentiles[i + 1])
    color_ramp = color_ramp_from_data(COLOR_RAMP_OCEAN_HALINE)
    lyr.renderer().updateColorRamp(color_ramp)

    iface.layerTreeView().refreshLayerSymbology(lyr.id())
    lyr.triggerRepaint()


def style_animation_node_difference(
    lyr: QgsVectorLayer, percentiles: List[float], variable: str, cells: bool = False
):
    """Applies styling to Animation Toolbar node layer in 'difference' mode"""

    # Load basic style settings from qml file
    if cells:
        qml_path = STYLES_ROOT / "cell_current.qml"
    else:
        qml_path = STYLES_ROOT / "node_difference.qml"
    lyr.loadNamedStyle(str(qml_path))

    # disregard the absolute maximum values when defining class bounds for a prettier result
    # instead, base the class bounds on the second highest percentile value (abs_high)
    # and include the absolute maximum afterwards, so that all values are visualized
    abs_high = max(abs(percentiles[1]), abs(percentiles[-2]))
    abs_max = max(abs(percentiles[0]), abs(percentiles[-1]))

    if abs_high != 0:
        class_bounds = (
            [abs_max * -1]
            + list(
                np.arange(
                    start=abs_high * -1,
                    stop=abs_high,
                    step=(
                        (abs_high - abs_high * -1)
                        / (ANIMATION_LAYERS_NR_LEGEND_CLASSES - 2)
                    ),
                )
            )
            + [abs_high, abs_max]
        )

        if variable == "s1":
            class_attribute_str = str(
                "coalesce(result, z_coordinate) - coalesce(initial_value, z_coordinate)"
            )
        else:
            class_attribute_str = str("result - initial_value")
        lyr.renderer().setClassAttribute(class_attribute_str)
        lyr.renderer().deleteAllClasses()
        for i in range(len(class_bounds) - 1):
            lyr.renderer().addClassLowerUpper(
                lower=class_bounds[i], upper=class_bounds[i + 1]
            )

    color_ramp = color_ramp_from_data(COLOR_RAMP_OCEAN_CURL)
    lyr.renderer().updateColorRamp(color_ramp)
    lyr.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(lyr.id())
