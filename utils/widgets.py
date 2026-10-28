import logging
from qgis.PyQt.QtGui import QPainter, QPen
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtCore import QTimer, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QLineEdit

logger = logging.getLogger(__name__)


class DebouncedSearchBox(QLineEdit):
    """
    A search box with debounced search signal.
    Emits searchChanged signal only after user stops typing for specified delay.
    Includes a trailing clear button that fires searchChanged immediately.
    """

    # Custom signal that will be emitted when the debounced search should occur
    searchChanged = pyqtSignal(str)

    def __init__(
        self,
        parent=None,
        delay_ms=50,
        min_chars=0,
        placeholder="Search schematisations by name...",
        show_search_icon=True,
    ):
        super().__init__(parent)

        # Setup timer for debouncing
        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._on_timeout)

        self.delay_ms = delay_ms
        self.min_chars = min_chars

        # Setup UI
        self.setPlaceholderText(placeholder)
        if show_search_icon:
            self.addAction(
                QIcon(":images/themes/default/mIconZoom.svg"), QLineEdit.LeadingPosition
            )

        # Clear button -- visible only when there is text
        self._clear_action = self.addAction(
            QIcon(":images/themes/default/mIconClearText.svg"),
            QLineEdit.TrailingPosition,
        )
        self._clear_action.setVisible(False)
        self._clear_action.triggered.connect(self._on_clear)

        # Connect the text changed signal
        self.textEdited.connect(self._on_text_edited)

    def _on_text_edited(self, text):
        """Handle text changes and apply debouncing."""
        self._clear_action.setVisible(bool(text))
        self._timer.stop()
        if len(text) >= self.min_chars or len(text) == 0:
            self._timer.start(self.delay_ms)

    def _on_clear(self):
        """Clear text and emit searchChanged immediately, bypassing debounce."""
        self._timer.stop()
        self.clear()
        self._clear_action.setVisible(False)
        self.searchChanged.emit("")

    def _on_timeout(self):
        """Emit the searchChanged signal with current text."""
        self.searchChanged.emit(self.text())


class PenStyleWidget(QWidget):
    """A simple widget than can be used to display examples of pen styles"""
    def __init__(
        self,
        pen_style: Qt.PenStyle,
        pen_color: QColor,
        pen_width: int,
        parent : QWidget,
    ):
        super().__init__(parent)
        self.pen_style = pen_style
        self.pen_color = pen_color
        self.pen_width = pen_width
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.begin(self)
        pen = QPen(self.pen_color, self.pen_width, self.pen_style)
        qp.setPen(pen)
        qp.drawLine(round(0.1*self.width()), round(self.height()/2.0), round(0.9*self.width()), round(self.height()/2.0))
        qp.end()
