from desktop_cat import Cat
from desktop_cat.window import Window, run


cat = Cat()
window = Window(cat)
window.say("Hello! Drag me around the screen.")
run()
