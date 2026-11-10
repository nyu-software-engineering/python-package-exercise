import pytest
from PySide6.QtWidgets import QApplication

from desktop_cat import Cat
from desktop_cat.window import Window

@pytest.fixture(scope="module")
def app():
    return QApplication.instance() or QApplication([])


def test_window_initializes_with_cat(app):
    cat = Cat()
    window = Window(cat, size=120)

    assert isinstance(window, Window)
    assert window.cat is cat
    assert window.size().width() == 120
    assert window.size().height() == 120
    window.close()


def test_window_say_displays_message_in_bubble(app):
    window = Window(Cat())

    window.say("Hello, human!", duration=1000)

    assert window.speech_bubble.text() == "Hello, human!"
    assert window.speech_bubble.isVisible()
    assert window._speech_hide_timer.isActive()

    window.close()


def test_window_say_truncates_long_message(app):
    window = Window(Cat())

    window.say("a" * 250)

    assert len(window.speech_bubble.text()) == 200

    window.close()


def test_window_say_invalid_duration(app):
    window = Window(Cat())

    with pytest.raises(TypeError):
        window.say("Hello", duration="1000")

    with pytest.raises(TypeError):
        window.say("Hello", duration=True)

    with pytest.raises(ValueError):
        window.say("Hello", duration=-1)

    window.close()


def test_update_speech_position(app):
    window = Window(Cat())
    window.move(200, 300)
    window.say("Hello!", duration=1000)

    window.move(400, 500)
    window.update_speech_position()

    bubble = window.speech_bubble
    assert bubble.x() == window.x() + (window.width() - bubble.width()) // 2
    assert bubble.y() == window.y() - bubble.height() - 10
    assert bubble.isVisible()

    window.close()
    bubble.close()
