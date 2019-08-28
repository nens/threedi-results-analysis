from PyQt5.QtQml import QQmlComponent, QQmlEngine
from qgis.core import qgsfunction
from PyQt5.QtQuick import QQuickView
from qgis.PyQt.QtCore import QUrl


@qgsfunction(args='auto', group='Custom')
def load_qml2(value1, value2, feature, parent):
    """
    Calculates the sum of the two parameters value1 and value2.
    <h2>Example usage:</h2>
    <ul>
      <li>my_sum(5, 8) -> 13</li>
      <li>my_sum("field1", "field2") -> 42</li>
    </ul>
    """
    return value1 * value2


@qgsfunction(args='auto', group='Custom')
def load_qml_shape(shape_type, feature, parent):
    """
    Loads a qml-file depending on the shape type

    1: rectangle
    2: round
    3: egg
    4: tabulated rectangle
    5: tabulated trapezium

    :param shape_type: type of the shape
    :return:
    """
    # either return the path to the qml file and load the qml-file in qml if possible
    # or load a qml object?
    engine = QQmlEngine()
    qml_component = QQmlComponent(
        engine,
        QUrl('layer_styles/tools/rectangle.qml')
    )
    return qml_component


if __name__ == "__main__":
    import sys

    from PyQt5 import QtWidgets
    from qgis.PyQt.QtCore import QUrl
    # from qgis.PyQt.QtGui import QApplication
    # from qgis.PyQt.QtDeclarative import QDeclarativeView
    from PyQt5.QtQuick import QQuickView

    app = QtWidgets.QApplication(sys.argv)
    # app = QApplication(sys.argv)
    # Create the QML user interface.
    view = QQuickView()
    view.setSource(QUrl('layer_styles/tools/rectangle.qml'))
    # view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
    # view.setGeometry(100, 100, 400, 240)
    view.show()

    app.exec_()
