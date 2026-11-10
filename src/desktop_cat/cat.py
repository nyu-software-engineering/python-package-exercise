import random
# Defines the states up front so everyone builds off of the same attributes/methods

MOODS = ("happy", "sad", "angry", "tired", "hungry", "annoyed")
FOODS = ("fish", "milk", "kibble", "canned food", "mouse")
PET_AREAS = ("head", "back", "belly", "tail", "paws")


class Cat:
    def __init__(self, name="Whiskers", mood="happy"):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        
        name = name.strip()

        if not name:
            raise ValueError("Name cannot be empty.")
        if len(name) > 20:
            raise ValueError("Name must be 20 characters or fewer.")

        if not isinstance(mood, str):
            raise TypeError("Mood must be a string.")

        mood = mood.strip().lower()
        if mood not in MOODS:
            raise ValueError(f"Invalid mood: {mood}")
        
        self.name = name
        self.mood = mood
        self.hunger = 5            # 0 = full, 10 = starving
        self.sleepiness = 5        # 0 = rested, 10 = exhausted
        self.times_petted = 0
        self.foods_eaten = {}      # e.g. {"fish": 2}
        self.message = ""
        self.last_action = "idle"  # render() will read this to pick a frame to draw

    def set_mood(self, mood):
        raise NotImplementedError

    def feed(self, food):
        if not isinstance(food, str):
            raise TypeError("Food must be a string.")
        
        food = food.strip().lower()

        if food not in FOODS:
            raise ValueError(f"Invalid food: {food}")

        reaction = ""
        hungerchange = 0
        eaten = True
        liked = random.choice([True, True, False])
        if liked:
            hungerchange = random.randint(2, 5)
            self.mood = "happy"
            reaction = f"{self.name} loved the {food}!"
        else:
            hungerchange = random.randint(0, 2)
            if hungerchange == 0:
                self.mood = "angry"
                reaction = f"{self.name} refused to eat the {food}."
                eaten = False
            else:
                self.mood = "sad"
                reaction = f"{self.name} did not like the {food}."
        if eaten:
            if food in self.foods_eaten:
                self.foods_eaten[food] += 1
            else:
                self.foods_eaten[food] = 1
        self.hunger = max(self.hunger-hungerchange, 0)
        self.last_action = "eating"
        return reaction

    def pet(self, area, times=1):
        if not isinstance(area, str):
            raise TypeError("Petting area must be a string.")
        
        area = area.strip().lower()

        if area not in PET_AREAS:
            raise ValueError(f"Invalid petting area: {area}")

        if isinstance(times, bool) or not isinstance(times, int):
            raise TypeError("Times must be an integer.")
        if times <= 0:
            raise ValueError("Times must be greater than 0.")
        
        reaction = ""
        self.times_petted += times
        self.last_action = "petted"
        if area in ("belly", "paws"):
            if times >= 5:
                if self.mood == "annoyed":
                    self.mood = "angry"
                    reaction = f"{self.name} is angry after being bothered so much!"
                else:
                    self.mood = "annoyed"
                    reaction = f"{self.name} gets annoyed when you pet its {area}."
            else:
                self.mood = "happy"
                reaction = f"{self.name} lets you pet its {area}."
        else:
            if times >= 10:
                if self.mood == "annoyed":
                    self.mood = "angry"
                    reaction = f"{self.name} is angry after being bothered so much!"
                else:
                    self.mood = "annoyed"
                    reaction = f"{self.name} gets tired of being pet on its {area}."
            else:
                self.mood = "happy"
                reaction = f"{self.name} purrs and enjoys the {area} pets."
        return reaction
            
    def sleep(self, hours):
        if not isinstance(hours, int) or isinstance(hours, bool) or hours <= 0:
            raise ValueError("Hours must be a positive integer.")

        if self.sleepiness == 0:
            return f"{self.name} is already fully rested."

        self.sleepiness = max(self.sleepiness - (hours*2), 0)

        if self.sleepiness == 0:
            self.mood = "happy"
            return f"{self.name} slept for {hours} hours and is fully rested!"
        
        return f"{self.name} slept for {hours} hours and feels less tired."

    def status(self, long=False):
        summary = f"{self.name} is feeling {self.mood}."
        if long:
            eaten = sum(self.foods_eaten.values())
            summary += (
                f" Hunger: {self.hunger}/10."
                f" Petted {self.times_petted} times."
                f" Meals eaten: {eaten}."
            )
        return summary

    def set_name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        name = name.strip()
        if not name:
            raise ValueError("Name cannot be empty")
        if len(name) > 20:
            raise ValueError("Name must be 20 characters or fewer")
        old_name = self.name
        self.name = name
        return f"{old_name} is now called {self.name}!"

    def say(self, text):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError