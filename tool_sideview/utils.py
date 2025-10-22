from qgis.PyQt.QtCore import Qt

available_styles = [
        Qt.PenStyle.SolidLine,
        Qt.PenStyle.DashLine,
        Qt.PenStyle.DotLine,
        Qt.PenStyle.DashDotLine,
        Qt.PenStyle.DashDotDotLine,
    ]


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
