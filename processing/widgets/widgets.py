import logging
from pathlib import Path

from processing.gui.wrappers import DIALOG_STANDARD
from processing.gui.wrappers import WidgetWrapper
from qgis.core import QgsProcessingParameterNumber
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QComboBox
from threedi_results_analysis.utils.user_messages import pop_up_info
import h5py

logger = logging.getLogger(__name__)
plugin_path = Path(__file__).resolve().parent.parent.parent


def format_timestep_value(value: float, drop_leading_zero: bool = False) -> str:
    days, seconds = divmod(int(value), 24 * 60 * 60)
    hours, seconds = divmod(seconds, 60 * 60)
    minutes, seconds = divmod(seconds, 60)

    if days == 0 and drop_leading_zero:
        formatted_display = "{:02d}:{:02d}".format(hours, minutes)
        return formatted_display

    formatted_display = "{:d} {:02d}:{:02d}".format(days, hours, minutes)
    return formatted_display


class ProcessingParameterNetcdfNumber(QgsProcessingParameterNumber):
    def __init__(self, *args, parentParameterName="", optional=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.parentParameterName = parentParameterName
        self.optional = optional
        self.setMetadata({"widget_wrapper": {"class": ThreediResultTimeSliderWidget}})


class ThreediResultTimeSliderWidget(WidgetWrapper):
    def createWidget(self):
        if self.dialogType == DIALOG_STANDARD:
            if not self.parameterDefinition().optional:
                self._widget = TimeSliderWidget()
            else:
                self._widget = CheckboxTimeSliderWidget()
        else:
            self._widget = TimeStepsCombobox()
        return self._widget

    def value(self):
        return self._widget.getValue()

    def postInitialize(self, wrappers):
        # Connect the result-file parameter to the TimeSliderWidget/TimeStepsCombobox
        for wrapper in wrappers:
            if wrapper.parameterDefinition().name() == self.param.parentParameterName:
                wrapper.wrappedWidget().fileChanged.connect(self._widget.new_file_event)


WIDGET, BASE = uic.loadUiType(plugin_path / "processing" / "ui" / "widgetTimeSlider.ui")


class TimeSliderWidget(BASE, WIDGET):
    """
    Timeslider form widget. Provide a horizontal slider and an LCD connected to the slider.
    """

    def __init__(self):
        super(TimeSliderWidget, self).__init__(None)
        self.setupUi(self)
        self.horizontalSlider.valueChanged.connect(self.set_lcd_value)
        self.index = None
        self.timestamps = None
        self.reset()

    def getValue(self):
        return self.index

    def set_timestamps(self, timestamps):
        self.setDisabled(False)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(len(timestamps) - 1)
        self.timestamps = timestamps
        self.set_lcd_value(0)  # also sets self.index

    def set_lcd_value(self, index: int):
        self.index = index
        if self.timestamps is not None:
            value = self.timestamps[index]
        else:
            value = 0
        lcd_value = format_timestep_value(value=value, drop_leading_zero=True)
        self.lcdNumber.display(lcd_value)

    def reset(self):
        self.setDisabled(True)
        self.index = None
        self.timestamps = None
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(0)
        self.horizontalSlider.setValue(0)

    def new_file_event(self, file_path):
        """New file has been selected by the user. Try to read in the timestamps from the file."""
        if not file_path or not Path(file_path).is_file():
            self.reset()
            return

        try:
            with h5py.File(file_path, "r") as results:
                timestamps = results["time"][()]
                self.set_timestamps(timestamps)
        except Exception as e:
            logger.exception(e)
            pop_up_info(msg="Unable to read the file, see the logging for more information.")
            self.reset()


WIDGET, BASE = uic.loadUiType(plugin_path / "processing" / "ui" / "widgetTimeSliderCheckbox.ui")


class CheckboxTimeSliderWidget(TimeSliderWidget, WIDGET, BASE):
    """Time slider widget with a checkbox to enable/disable the time slider"""

    def __init__(self):
        super().__init__()
        self.horizontalSlider.setDisabled(not self.checkBox.isChecked())
        self.checkBox.stateChanged.connect(self.new_check_box_event)

    def getValue(self):
        if self.checkBox.isChecked():
            return self.index
        else:
            return None

    def new_check_box_event(self, state):
        self.horizontalSlider.setDisabled(not self.checkBox.isChecked())


class TimeStepsCombobox(QComboBox):
    """Combobox with populated timestep data."""

    def getValue(self):
        return self.currentIndex()

    def populate_timestamps(self, timestamps):
        for i, value in enumerate(timestamps):
            human_readable_value = format_timestep_value(value)
            if human_readable_value.startswith("0"):
                human_readable_value = human_readable_value.split(" ", 1)[-1]
            self.addItem(human_readable_value)
        self.setCurrentIndex(0)

    def new_file_event(self, file_path):
        """New file has been selected by the user. Try to read in the timestamps from the file."""
        if not file_path or not Path(file_path).is_file():
            self.clear()
            return

        try:
            with h5py.File(file_path, "r") as results:
                timestamps = results["time"][()]
                self.populate_timestamps(timestamps)
        except Exception as e:
            logger.exception(e)
            pop_up_info(msg="Unable to read the file, see the logging for more information.")
            self.clear()
