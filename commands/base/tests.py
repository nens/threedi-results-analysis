from ThreeDiToolbox.commands.base.custom_command import CustomCommandBase

import pytest


@pytest.mark.parametrize("method_name", ["run_it", "show_gui", "run"])
def test_signature(method_name):
    """The base class has three methods that raise NotImplementedError."""
    sample_object = CustomCommandBase()
    with pytest.raises(NotImplementedError):
        getattr(sample_object, method_name)()
