
from desktop_cat import Cat, MOODS, FOODS

import inspect
print(inspect.getfile(Cat))
print(inspect.signature(Cat.pet))

def main():
    # Create a cat
    cat = Cat(name="Whiskers", mood="happy")
    
    print("Welcome to Desktop Cat!")
    print(cat.status(long=True))

    print("\nAvailable moods:", MOODS)
    print("Available foods:", FOODS)

    # Demonstrate renaming
    print("\n" + cat.set_name("Mittens"))

    # Demonstrate feeding
    print(cat.feed("fish"))

    # Demonstrate petting
    print(cat.pet("head", times=3))

    # Demonstrate sleeping
    print(cat.sleep(2))

    # Demonstrate status
    print("\nShort status:")
    print(cat.status())

    print("\nDetailed status:")
    print(cat.status(long=True))

    # Demonstrate feeding statistics
    print("\nFoods eaten:", cat.foods_eaten)

    # Demonstrate GUI (optional dependency)
    print("\nWould you like to launch the desktop cat?")
    choice = input("Launch GUI? (y/n): ").strip().lower()

    if choice == "y":
        try:
            from desktop_cat import Window, run

            window = Window(cat)
            window.say(f"Hello! I'm {cat.name}!")
            run()

        except ImportError as exc:
            print(f"\nCould not launch GUI: {exc}")

    print("\nExample completed!")


if __name__ == "__main__":
    main()
