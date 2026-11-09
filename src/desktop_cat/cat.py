# Defines the states up front so everyone builds off of the same attributes/methods
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
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
        pixmap = QPixmap(str(ASSETS / "Cat.png"))
        self.setPixmap(
            pixmap.scaled(
                size,
                size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

        self.resize(size, size)
        self.drag_position = None

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

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def run(self):
        self.app.exec()

    def set_mood(self, mood):
        raise NotImplementedError

    def feed(self, food):
        raise NotImplementedError

    def pet(self, times=1):
        raise NotImplementedError

    def status(self):
        raise NotImplementedError

    def set_name(self, name):
        raise NotImplementedError

    def say(self, text):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    