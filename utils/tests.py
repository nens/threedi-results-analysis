from ThreeDiToolbox.utils.signal_helper import  ValueWithChangeSignal
import mock


def test_value_with_change_signal():
    class Person(object):
        age_changed_signal = mock.Mock()
        age = ValueWithChangeSignal("age_changed_signal", "age_changed")

    person = Person()
    # No default value, so None:
    assert person.age is None
    person.age = 42
    # The setter/getter mechanism works:
    assert person.age == 42
    # And yes, we emitted the signal:
    assert Person.age_changed_signal.emit.called
