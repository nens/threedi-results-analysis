from future.utils import with_metaclass
from ThreeDiToolbox.utils.user_messages import pop_up_info

import abc


class CustomCommandBase(with_metaclass(abc.ABCMeta, object)):

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
        """Entry point of CustomCommand. Either call show_gui or run_it here.
        """
        pass
