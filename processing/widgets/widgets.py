import logging
from pathlib import Path
from typing import Dict

from processing.gui.wrappers import DIALOG_BATCH, DIALOG_STANDARD
from processing.gui.wrappers import WidgetWrapper
from qgis.core import QgsProcessingContext
from qgis.gui import QgsGui
from qgis.gui import QgsProcessingGui
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QComboBox, QSpinBox
import h5py

from threedi_results_analysis.utils.user_messages import pop_up_info

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


# class ProcessingParameterNetcdfNumber(QgsProcessingParameterNumber):
#     def __init__(self, *args, parentParameterName="", optional=False, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.parentParameterName = parentParameterName
#         self.optional = optional
#         self.setMetadata({"widget_wrapper": {"class": ThreediResultTimeSliderWidget}})


# class ProcessingParameterNetcdfString(QgsProcessingParameterString):
#     def __init__(self, *args, parentParameterName="", **kwargs):
#         super().__init__(*args, **kwargs)
#         self.parentParameterName = parentParameterName
#         self.setMetadata({"widget_wrapper": {"class": SubstanceWidgetWrapper}})


class ThreediResultTimeSliderWidgetWrapper(WidgetWrapper):
    def createWidget(self):
        if self.dialogType == DIALOG_STANDARD:
            if not self.param.metadata().get("optional"):
                self._widget = TimeSliderWidget()
            else:
                self._widget = CheckboxTimeSliderWidget()
        elif self.dialogType == DIALOG_BATCH:
            self._widget = TimeStepsCombobox()
        else:
            registry = QgsGui.instance().processingGuiRegistry()
            default_wrapper = registry.createParameterWidgetWrapper(
                self.parameterDefinition(),
                QgsProcessingGui.WidgetType.Modeler
            )
            print(f"dir(self): {dir(self)}")
            self._widget = default_wrapper.createWrappedWidget(QgsProcessingContext())
        return self._widget

    def value(self):
        return self._widget.getValue()

    def setValue(self, value):
        if value is not None:
            self._widget.setValue(int(value))

    def postInitialize(self, wrappers):
        # Connect the result-file parameter to the TimeSliderWidget/TimeStepsCombobox
        for wrapper in wrappers:
            if wrapper.parameterDefinition().name() == self.param.metadata().get("parentParameterName"):
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

    def setValue(self, value):
        if value is not None:
            self.set_lcd_value(int(value))
            self.horizontalSlider.setValue(int(value))

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

    def setValue(self, value: int):
        self.setCurrentIndex(value)
        pass

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


# class SubstanceWidgetFactory(QgsProcessingParameterWidgetFactoryInterface):
#     def parameterType(self):
#         return QgsProcessingParameterString.typeName()
#
#     # def canCreateWrapperFor(self, param):
#     #     return param.metadata().get("widget_wrapper") == "SubstanceWidgetWrapper"
#
#     def createWidgetWrapper(self, parameter):
#         return SubstanceWidgetWrapper(parameter)


class SubstanceWidgetWrapper(WidgetWrapper):
    def createWidget(self):
        self._widget = SubstanceCombobox()
        return self._widget

    def value(self):
        return self._widget.getValue()

    def setValue(self, value):
        if value is not None:
            self._widget.setValue(str(value))

    def postInitialize(self, wrappers):
        # Connect the result-file parameter to the SubstanceCombobox
        for wrapper in wrappers:
            if wrapper.parameterDefinition().name() == self.param.metadata().get("parentParameterName"):
                wrapper.wrappedWidget().fileChanged.connect(self._widget.new_file_event)


class SubstanceCombobox(QComboBox):
    """
    Combobox with populated substance data.
    Displayed texts are the substance names ("Chloride", "Phosphate", etc.).
    The user data behind it are the substance IDs ("substance1", "substance2", etc.)
    """

    def getValue(self):
        return self.currentData()

    def setValue(self, value: str):
        """Set combobox to the item whose substance ID (e.g. "substance1") matches the given value."""
        for i in range(self.count()):
            if self.itemData(i) == value:
                self.setCurrentIndex(i)
                return

    def populate(self, data: Dict[str, str]):
        """
        Populates the widget from a {substance id: substance name} Dict
        """
        self.clear()
        for substance_id, substance_name in data.items():
            self.addItem(substance_name, substance_id)
        if data:
            self.setCurrentIndex(0)

    @staticmethod
    def substances_from_netcdf(netcdf: str | Path) -> Dict[str, str]:
        """
        Get a {substance id: substance name} Dict for a water_quality_results_3di.nc file
        """
        f = h5py.File(netcdf)
        substances = {}
        for key in f.keys():
            if key.startswith("substance"):
                substance_id = key.split("_")[0]
                substance_name = f[key].attrs["substance_name"]
                substances[substance_id] = substance_name
        return substances

    def new_file_event(self, file_path):
        """New file has been selected by the user. Try to read in the substance data from the file."""
        if not file_path or not Path(file_path).is_file():
            self.clear()
            return

        try:
            substance_data = self.substances_from_netcdf(file_path)
            self.populate(substance_data)
        except Exception as e:
            logger.exception(e)
            pop_up_info(msg="Unable to read the file, see the logging for more information.")
            self.clear()
