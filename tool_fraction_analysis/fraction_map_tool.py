from qgis.gui import QgsMapToolIdentify


class AddMapTool(QgsMapToolIdentify):
    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = widget

    def canvasReleaseEvent(self, event):
        results = self.identify(
            x=int(event.pos().x()),
            y=int(event.pos().y()),
            layerList=self.parent().layers()
        )
        self.widget.add_results(results)
