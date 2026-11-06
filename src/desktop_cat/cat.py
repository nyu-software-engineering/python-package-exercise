# Defines the states up front so everyone builds off of the same attributes/methods

MOODS = ("happy", "sad", "angry", "tired", "hungry")
FOODS = ("fish", "milk", "kibble", "canned food", "mouse")


class Cat:
    def __init__(self, name="Whiskers", mood="happy"):
        self.name = name
        self.mood = mood
        self.hunger = 5            # 0 = full, 10 = starving. Up to you if you want to use this system
        self.times_petted = 0
        self.foods_eaten = {}      # e.g. {"fish": 2}
        self.message = ""
        self.last_action = "idle"  # render() will read this to pick a frame to animate (not sure if necessary)

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