from pathlib import Path

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QPixmap, QPainter
from qgis.PyQt.QtSvg import QSvgRenderer


def pixmap_from_svg(svg_path: Path|str, width: int, height: int) -> QPixmap:
    renderer = QSvgRenderer(str(svg_path))
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap
