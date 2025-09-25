from typing import Tuple
from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsRasterShader,
    QgsColorRampShader,
    QgsSingleBandPseudoColorRenderer
)
from PyQt5.QtGui import QColor


def apply_transparency_gradient(
    layer: QgsRasterLayer,
    color: QColor,
    min_value: float,
    max_value: float,
):
    # Create shader function
    shader = QgsRasterShader()
    color_ramp_shader = QgsColorRampShader()
    color_ramp_shader.setColorRampType(QgsColorRampShader.Interpolated)

    items = []

    # Transparent at min value
    min_color = QColor(color)
    min_color.setAlpha(0)   # fully transparent
    items.append(QgsColorRampShader.ColorRampItem(min_value, min_color))

    # Opaque at value 10
    max_color = QColor(color)
    max_color.setAlpha(255)  # fully opaque
    items.append(QgsColorRampShader.ColorRampItem(max_value, max_color))

    color_ramp_shader.setColorRampItemList(items)
    color_ramp_shader.setMinimumValue(min_value)
    color_ramp_shader.setMaximumValue(max_value)
    shader.setRasterShaderFunction(color_ramp_shader)

    # Create renderer (assuming band 1)
    renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, shader)

    # Apply renderer to layer
    layer.setRenderer(renderer)
    layer.triggerRepaint()
