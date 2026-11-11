
from desktop_cat import Cat, MOODS, FOODS, PET_AREAS

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
    print("Available petting areas:", PET_AREAS)

    # Demonstrate renaming
    print("\n" + cat.set_name("Mittens"))

    # Demonstrate feeding
    print(cat.feed("fish"))
    print(cat.feed("kibble"))

    # Demonstrate feeding statistics
    print("Foods eaten:", cat.foods_eaten)

    # Demonstrate petting
    print("\n" + cat.pet("belly", times=5))
    print(cat.status())
    print(cat.pet("head", times=3))
    print(cat.status())
    print("Total times petted:", cat.times_petted)

    # Demonstrate sleeping
    print("\n" +cat.sleep(2))

    # Demonstrate status
    print("\nShort status:")
    print(cat.status())

    print("\nDetailed status:")
    print(cat.status(long=True))

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
