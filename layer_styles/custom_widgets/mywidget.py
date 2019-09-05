# https://github.com/elpaso/qgis-formawarevaluerelationwidget/blob/master/FormAwareValueRelationWidget.py
# https://gis.stackexchange.com/questions/202371/how-to-format-qgis-field-names-on-editor-form


from qgis.gui import QgsEditorWidgetWrapper
from qgis.gui import QgsEditorWidgetFactory
from qgis.gui import QgsEditorConfigWidget
from qgis.PyQt.QtWidgets import QWidget


class MyCustomWidget(QgsEditorWidgetWrapper):
    def __init__(self, vl, fieldIdx, editor, parent):
        super().__init__(vl, fieldIdx, editor, parent)
        self.key_index = -1
        self.value_index = -1
        self.context = None
        self.expression = None
        # Re-create the cache if the layer is modified
        self.mLayer.layerModified.connect(self.createCache)
        self.completer_list = None  # Caches completer elements
        self.completer = None  # Store compler instance
        self.editor = editor

    # def createWidget(self, parent):
    #     return super().create()


class MyQgsEditorConfigWidget(QgsEditorConfigWidget):

    def __init__(self, vl, fieldIdx, parent):
        super(MyQgsEditorConfigWidget, self).__init__(vl, fieldIdx, parent)


class MyCustomWidgetFactory(QgsEditorWidgetFactory):

    def __init__(self, name):
        super(MyCustomWidgetFactory, self).__init__(name)
        self.wrapper = None
        self.dlg = None

    def configWidget(self, vl, fieldIdx, parent):
        print("MY CUSTOM CONFIGWIDGET FUNCTION")
        self.dlg = MyQgsEditorConfigWidget(vl, fieldIdx, parent)
        return self.dlg

    def create(self, vl, fieldIdx, editor, parent):
        # QgsVectorLayer* vl, int fieldIdx, QWidget* editor, QWidget* parent
        self.wrapper = MyCustomWidget(vl, fieldIdx, editor, parent)
        return self.wrapper


if __name__ == '__main__':
    config_widget = MyQgsEditorConfigWidget()
    print('done')
