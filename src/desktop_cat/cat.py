# Defines the states up front so everyone builds off of the same attributes/methods
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"

MOODS = ("happy", "sad", "angry", "tired", "hungry")
FOODS = ("fish", "milk", "kibble", "canned food", "mouse")


class Cat(QLabel):
    def __init__(self, name="Whiskers", mood="happy", size=90):
        self.app = QApplication.instance()

        if self.app is None:
            self.app = QApplication([])

        super().__init__()

        # Cat data
        self.name = name
        self.mood = mood
        self.hunger = 5
        self.times_petted = 0
        self.foods_eaten = {}
        self.message = ""
        self.last_action = "idle"

        # Window settings
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        # Load cat image
        self.resize(size, size)
        self.drag_position = None

        # Load initial mood
        self.set_mood(mood)

        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint() -
                self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if self.drag_position is not None:
            self.move(
                event.globalPosition().toPoint() -
                self.drag_position
            )
            self.update_speech_position()

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def update_speech_position(self):
        if hasattr(self, "speech_bubble") and self.speech_bubble.isVisible():
            x = self.x() + (self.width() - self.speech_bubble.width()) // 2
            y = self.y() - self.speech_bubble.height() - 10

            self.speech_bubble.move(x, y)

    def set_mood(self, mood):
        if mood not in MOODS:
            raise ValueError(f"Invalid mood: {mood}")

        self.mood = mood

        pixmap = QPixmap(str(ASSETS / f"Cat{mood.capitalize()}.png"))

        self.setPixmap(
            pixmap.scaled(
                self.width(),
                self.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def feed(self, food):
        raise NotImplementedError

    def pet(self, times=1):
        raise NotImplementedError

    def status(self):
        raise NotImplementedError

    def set_name(self, name):
        raise NotImplementedError

    def say(self, message, duration=3000):
        if not hasattr(self, "speech_bubble"):
            self.speech_bubble = QLabel()
            self.speech_bubble.setWindowFlags(
                Qt.WindowType.FramelessWindowHint |
                Qt.WindowType.WindowStaysOnTopHint |
                Qt.WindowType.Tool
            )
            self.speech_bubble.setWordWrap(True)
            self.speech_bubble.setMaximumWidth(250)
            self.speech_bubble.setStyleSheet("""
                QLabel {
                    background-color: rgba(255, 255, 255, 220);
                    color: black;
                    border: 1px solid black;
                    padding: 6px 10px;
                    font-size: 13px;
                    font-family: "Comic Neue Angular";
                    font-size: 14px;
                }
            """)

        # Limit message length
        message = str(message)[:200]

        self.speech_bubble.setText(message)
        self.speech_bubble.adjustSize()

        # Position bubble above cat
        x = self.x() + (self.width() - self.speech_bubble.width()) // 2
        y = self.y() - self.speech_bubble.height() - 10

        self.speech_bubble.move(x, y)
        self.speech_bubble.show()

        QTimer.singleShot(duration, self.speech_bubble.hide)

    def render(self):
        raise NotImplementedError

def run():
    app = QApplication.instance()

    if app is not None:
        app.exec()