class CustomCommandBase:
    def run_it(self):
        """Run the script

        This should contain the actual implementation of the script logic.

        """
        raise NotImplementedError

    def show_gui(self):
        """Show a GUI as a frontend for this script."""
        raise NotImplementedError

    def run(self):
        """Entry point of CustomCommand. Either call show_gui or run_it here."""
        raise NotImplementedError
