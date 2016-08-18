import abc
import os

from qgis.core import QgsVectorLayer, QgsMapLayerRegistry, QgsVectorJoinInfo

from ThreeDiToolbox.utils.user_messages import pop_up_info


def join_stats(filepath, layer, view_layer_field, csv_field='id',
               interactive=True):
    """Join the generated stats csv with the layer

    Args:
        filepath: path to the csv file
        layer: the layer we want to join the csv with
        view_layer_field: the id (e.g. primary key) of layer
        csv_field: the id of the csv layer (which is always 'id' in the case
            of the CustomCommand scripts)
    """
    filename = os.path.basename(filepath)
    csv_layer_name = os.path.splitext(filename)[0]
    csv_uri = "file:///" + filepath
    csv_layer = QgsVectorLayer(csv_uri, csv_layer_name, "delimitedtext")
    QgsMapLayerRegistry.instance().addMapLayer(csv_layer)
    join_info = QgsVectorJoinInfo()
    join_info.joinLayerId = csv_layer.id()
    join_info.joinFieldName = csv_field
    join_info.targetFieldName = view_layer_field
    join_info.memoryCache = True
    layer.addJoin(join_info)

    if interactive:
        pop_up_info("Finished joining '%s' with '%s'." % (
            csv_layer_name, layer.name()), title='Join finished')


class CustomCommandBase(object):
    __metaclass__ = abc.ABCMeta

    def load_defaults(self):
        """If you only want to use run_it without show_gui, you can try calling
        this method first to set some defaults.

        This method will try to load the first datasource and the current QGIS
        layer.
        """
        try:
            self.datasource = self.ts_datasource.rows[0]
        except IndexError:
            pop_up_info("No datasource found. Aborting.", title='Error')
            return

        # Current layer information
        self.layer = self.iface.mapCanvas().currentLayer()
        if not self.layer:
            pop_up_info("No layer selected, things will not go well..",
                        title='Error')
            return

    @abc.abstractmethod
    def run_it(self):
        """Runs the script; this should contain the actual implementation of
        the script logic.
        """
        pass

    @abc.abstractmethod
    def show_gui(self):
        """Show a GUI as a frontend for this script."""
        pass

    @abc.abstractmethod
    def run(self):
        """Entry point of CustomCommand. Either call show_gui or run_it here."""
        pass
