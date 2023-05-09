import math
from PyQt5.QtGui import QPainter, QPen
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.QtCore import Qt

available_styles = [
        Qt.SolidLine,
        Qt.DashLine,
        Qt.DotLine,
        Qt.DashDotLine,
        Qt.DashDotDotLine,
    ]


class PenStyleWidget(QWidget):
    """A simple widget than can be used to display examples of pen styles"""
    def __init__(
        self,
        pen_style: Qt.PenStyle,
        pen_color: QColor,
        parent : QWidget,
    ):
        super().__init__(parent)
        self.pen_style = pen_style
        self.pen_color = pen_color

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.begin(self)
        pen = QPen(self.pen_color, 2, self.pen_style)
        qp.setPen(pen)
        qp.drawLine(round(0.1*self.width()), round(self.height()/2.0), round(0.9*self.width()), round(self.height()/2.0))
        qp.end()


class LineType:
    CONNECTION_NODE = 1
    MANHOLE = 2
    BOUNDARY = 3
    CROSS_SECTION = 4
    CALCULATION_NODE = 5
    PIPE = 11
    WEIR = 12
    CULVERT = 13
    ORIFICE = 14
    PUMP = 15
    CHANNEL = 16


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    Source: http://gis.stackexchange.com/a/56589
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = list(map(math.radians, [lon1, lat1, lon2, lat2]))
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km
