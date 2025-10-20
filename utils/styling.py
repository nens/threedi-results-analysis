from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsRasterShader,
    QgsColorRampShader,
    QgsGradientColorRamp,
    QgsSingleBandPseudoColorRenderer,
)
from PyQt5.QtGui import QColor


def apply_transparency_gradient(
    layer: QgsRasterLayer,
    color: QColor,
    min_value: float,
    max_value: float,
    band: int = 1,
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
    color_ramp = QgsGradientColorRamp(color1=min_color, color2=max_color, stops=[])
    color_ramp_shader.setSourceColorRamp(color_ramp)
    shader.setRasterShaderFunction(color_ramp_shader)

    # Create renderer
    renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), band, shader)
    renderer.setClassificationMin(min_value)
    renderer.setClassificationMax(max_value)

    # Apply renderer to layer
    layer.setRenderer(renderer)
    layer.triggerRepaint()


def apply_gradient_ramp(
        layer: QgsRasterLayer,
        color_ramp: QgsGradientColorRamp,
        min_value: float,
        max_value: float,
        band: int = 1
):
    """
    Apply a gradient color ramp to a raster layer, stretched over given min/max values.

    Parameters
    ----------
    layer : QgsRasterLayer
        The raster layer to style.
    color_ramp : QgsGradientColorRamp
        The gradient color ramp to apply.
    min_value : float
        The minimum value to be used when stretching the color map over the data
    max_value : float
        The maximum value to be used when stretching the color map over the data
    band : int
        Raster band index (default=1).
    """

    # Define the color ramp shader
    color_ramp_shader = QgsColorRampShader()
    color_ramp_shader.setColorRampType(QgsColorRampShader.Interpolated)
    color_ramp_shader.setColorRamp(color_ramp)
    color_ramp_shader.setMinimumValue(min_value)
    color_ramp_shader.setMaximumValue(max_value)

    shader = QgsRasterShader()
    shader.setRasterShaderFunction(color_ramp_shader)

    # Apply renderer
    renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), band, shader)
    layer.setRenderer(renderer)
    layer.triggerRepaint()
