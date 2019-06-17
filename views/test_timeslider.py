from ThreeDiToolbox.views.timeslider import TimesliderWidget
from unittest import mock


def test_index_to_duration(qtbot):
    iface = mock.Mock()
    ts_datasource = mock.Mock()
    time_slider = TimesliderWidget(iface, ts_datasource)
    # 2 days, 3 hours, 2 minutes and 10 seconds
    duration = (2 * 24 * 60 * 60) + (3 * 60 * 60) + 120 + 10
    time_slider.timestamps = [duration]
    days, hours, minutes = time_slider.index_to_duration(0)
    assert days == 2
    assert hours == 3
    assert minutes == 2
