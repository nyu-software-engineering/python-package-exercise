from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel

ASSETS = Path(__file__).parent / "assets"

class Window(QLabel):
    def __init__(self, cat, size: int = 150, parent=None):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication([])

        super().__init__(parent)
        self.cat = cat
        self.drag_position = None
        self.speech_bubble = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(size, size)

        pixmap = QPixmap(str(ASSETS / "CatHappy.png"))
        self.setPixmap(
            pixmap.scaled(
                self.width(),
                self.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            self.update_speech_position()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.drag_position = None
        super().mouseReleaseEvent(event)

    def update_speech_position(self) -> None:
        bubble = self.speech_bubble
        if bubble is not None and bubble.isVisible():
            x = self.x() + (self.width() - bubble.width()) // 2
            y = self.y() - bubble.height() - 10
            bubble.move(x, y)

    def say(self, message, duration=3000):
        if self.speech_bubble is None:
            self.speech_bubble = QLabel()
            self.speech_bubble.setWindowFlags(
                Qt.WindowType.FramelessWindowHint
                | Qt.WindowType.WindowStaysOnTopHint
                | Qt.WindowType.Tool
            )
            self.speech_bubble.setWordWrap(True)
            self.speech_bubble.setMaximumWidth(250)
            self.speech_bubble.setStyleSheet(
                """
                QLabel {
                    background-color: rgba(255, 255, 255, 220);
                    color: black;
                    border: 1px solid black;
                    padding: 6px 10px;
                    font-size: 14px;
                }
                """
            )
            self._speech_hide_timer = QTimer(self.speech_bubble)
            self._speech_hide_timer.setSingleShot(True)
            self._speech_hide_timer.timeout.connect(self.speech_bubble.hide)

        self.speech_bubble.setText(str(message)[:200])
        self.speech_bubble.adjustSize()
        x = self.x() + (self.width() - self.speech_bubble.width()) // 2
        y = self.y() - self.speech_bubble.height() - 10
        self.speech_bubble.move(x, y)
        self.speech_bubble.show()
        self._speech_hide_timer.start(max(0, duration))
        self.speech_bubble.move(x, y)


def run() -> None:
    app = QApplication.instance()
    if app is not None:
        app.exec()
