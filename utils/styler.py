import logging
import os
import numpy as np

from typing import List
from pathlib import Path
from qgis.PyQt.QtGui import QColor
from qgis.core import (
    QgsGradientColorRamp,
    QgsGradientStop,
    QgsMapLayerStyle,
    QgsStyle,
    QgsVectorLayer
)
from qgis.utils import iface
from ThreeDiToolbox.utils.color import (
    ColorRampData,
    COLOR_RAMP_OCEAN_DEEP,
    COLOR_RAMP_OCEAN_HALINE,
    COLOR_RAMP_OCEAN_CURL
)
from ThreeDiToolbox.datasource.result_constants import WET_CROSS_SECTION_AREA

logger = logging.getLogger(__name__)

STYLES_ROOT = Path(__file__).parent.parent / "layer_styles"
ANIMATION_LAYERS_NR_LEGEND_CLASSES = 24
assert ANIMATION_LAYERS_NR_LEGEND_CLASSES % 2 == 0

def color_ramp_from_data(data: ColorRampData):
    color1 = QColor(data.colors[0])
    color2 = QColor(data.colors[-1])
    stops = []
    for i, color in enumerate(data.colors[1:-1]):
        stop = QgsGradientStop((i + 1) / (len(data.colors) - 1), QColor(color))
        stops.append(stop)

    ramp = QgsGradientColorRamp(color1=color1, color2=color2, stops=stops)
    ramp.setInfo(data.info)
    return ramp


def add_color_ramp(data: ColorRampData):
    """Add color ramp to QGIS or replace if exists"""

    QgsStyle.defaultStyle().addColorRamp(data.name, color_ramp_from_data(data))
    # If ramp with this name already exists, it will be overridden (default QGIS API behaviour)


def style_animation_flowline_current(
        lyr: QgsVectorLayer,
        class_bounds: List[float],
        variable
):
    """Applies styling to Animation Toolbar flowline layer in 'current' mode"""

    # Load basic style settings from qml file
    qml_path = STYLES_ROOT / 'tools' / 'animation_toolbar' / 'flowline_current.qml'
    lyr.loadNamedStyle(str(qml_path))
    ren = lyr.renderer()

    # Set correct legend symbol rotation
    sym = ren.sourceSymbol().clone()
    if variable == WET_CROSS_SECTION_AREA.name:
        sym.deleteSymbolLayer(1)
        max_symbol_size = 1.5
    else:
        sym.symbolLayers()[1].setSymbolAngle(90)
        max_symbol_size = 2.5
    ren.updateSymbols(sym)

    # Set classes and colors
    color_ramp = color_ramp_from_data(COLOR_RAMP_OCEAN_DEEP)
    ren.deleteAllClasses()
    nr_classes = len(class_bounds) - 1
    for i in range(nr_classes):
        ren.addClassLowerUpper(
            lower=class_bounds[i],
            upper=class_bounds[i + 1]
        )
        class_middle = (class_bounds[i] + class_bounds[i + 1]) / 2
        sym = ren.symbolForValue(class_middle).clone()
        color_ramp_fraction = ((i + 0.5) / nr_classes)
        color = color_ramp.color(color_ramp_fraction)
        sym.setColor(color)
        ren.setLegendSymbolItem(str(i), sym)

    # Symbol size
    ren.setSymbolSizes(0.1, max_symbol_size)
    iface.layerTreeView().refreshLayerSymbology(lyr.id())
    lyr.triggerRepaint()


def style_animation_node_current(
        lyr: QgsVectorLayer,
        percentiles: List[float]
):
    """Applies styling to Animation Toolbar node layer in 'current' mode"""

    # Load basic style settings from qml file
    qml_path = STYLES_ROOT / 'tools' / 'animation_toolbar' / 'node_current.qml'
    lyr.loadNamedStyle(str(qml_path))
    ren = lyr.renderer()

    # Set classes
    ren.deleteAllClasses()
    nr_classes = len(percentiles) - 1
    for i in range(nr_classes):
        ren.addClassLowerUpper(
            lower=percentiles[i],
            upper=percentiles[i + 1]
        )
    color_ramp = color_ramp_from_data(COLOR_RAMP_OCEAN_HALINE)
    lyr.renderer().updateColorRamp(color_ramp)

    iface.layerTreeView().refreshLayerSymbology(lyr.id())
    lyr.triggerRepaint()


def style_animation_node_difference(
        lyr: QgsVectorLayer,
        percentiles: List[float],
        variable: str
):
    """Applies styling to Animation Toolbar node layer in 'difference' mode"""

    # Load basic style settings from qml file
    qml_path = STYLES_ROOT / 'tools' / 'animation_toolbar' / 'node_difference.qml'
    lyr.loadNamedStyle(str(qml_path))

    abs_high = max(abs(percentiles[1]), abs(percentiles[-2]))
    abs_max = max(abs(percentiles[0]), abs(percentiles[-1]))

    if abs_high != 0:
        class_bounds = \
            [abs_max * -1] + \
            list(np.arange(
                start=abs_high * -1,
                stop=abs_high,
                step=((abs_high - abs_high * -1) / (ANIMATION_LAYERS_NR_LEGEND_CLASSES - 2))
            )) + \
            [abs_high, abs_max]

        if variable == 's1':
            class_attribute_str = str('coalesce(result, z_coordinate) - coalesce(initial_value, z_coordinate)')
        else:
            class_attribute_str = str('result - initial_value')
        lyr.renderer().setClassAttribute(class_attribute_str)
        lyr.renderer().deleteAllClasses()
        for i in range(len(class_bounds) - 1):
            lyr.renderer().addClassLowerUpper(lower=class_bounds[i], upper=class_bounds[i + 1])

    color_ramp = color_ramp_from_data(COLOR_RAMP_OCEAN_CURL)
    lyr.renderer().updateColorRamp(color_ramp)
    lyr.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(lyr.id())


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
