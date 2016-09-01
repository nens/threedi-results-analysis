import abc
from ThreeDiToolbox.utils.user_messages import pop_up_info


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
