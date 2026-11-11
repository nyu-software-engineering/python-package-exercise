"""Example program that shows everything the cosmicly package can do."""

from cosmicly.compare_planets import compare_planets, earth_age
from cosmicly.data import PLANETS
from cosmicly.planetary_age import age_on_planet
from cosmicly.planetary_weight import weight_on_planet
from cosmicly.relative_time import relative_time
from cosmicly.planetary_travel import (
    arrival_age,
    distance_from_earth,
    drive_to,
    fly_to,
    format_duration,
    light_speed_to,
    travel_at_speed,
)


def show_weight():
    """Show example weights on Mars, Jupiter, and the Moon."""
    print("========= Weight =========")
    print("70 kg on Earth weighs this much on Mars:", weight_on_planet("w", 70, "mars"))
    print(
        "70 kg on Earth weighs this much on Jupiter:",
        weight_on_planet("weight", 70, "jupiter"),
    )
    print(
        "A 70 kg person on the Moon feels a force of",
        weight_on_planet("m", 70, "moon"),
        "newtons",
    )
    print()


def show_age():
    """Show example age conversions and an age calculated from a birthdate."""
    print("========= Age =========")
    print("Being 20 on Earth means on Mercury you are:", age_on_planet(20, "mercury"))
    print("Being 20 on Earth means on Neptune you are:", age_on_planet(20, "neptune"))
    print(
        "Someone born on 2000-01-01 is this old in Earth years:",
        earth_age("2000-01-01"),
    )
    print()


def show_time():
    """Show the current simulated time on Earth, Mars, and Jupiter."""
    print("========= Time right now =========")
    print("On Earth:", relative_time("earth"))
    print("On Mars:", relative_time("mars"))
    print("On Jupiter:", relative_time("jupiter"))
    print()


def show_travel():
    """Show example distances and travel times from Earth."""
    print("========= Travel from Earth =========")
    print("Driving to the Moon:", drive_to("moon"))
    print("Flying to Mars:", fly_to("mars"))
    print("Light-speed to Neptune:", light_speed_to("neptune"))
    print("A rocket at 40,000 km/h to Mars:", travel_at_speed("mars", 40_000))
    print("Distance from Earth to Mars:", distance_from_earth("mars"), "km")
    print("100,000 seconds is about", format_duration(100_000))
    print("Driving to Mars on 2026-11-10:", drive_to("mars", "2026-11-10"))
    print("A 20-year-old driving to Mars arrives aged:", arrival_age("mars", 100, 20))
    print()


def show_comparison():
    """Show an example age and weight comparison for two planets."""
    print(
        "========= Mars vs Jupiter for someone born 2000-01-01 who weighs 70 ========="
    )
    result = compare_planets("mars", "jupiter", "2000-01-01", 70)
    for planet, stats in result.items():
        print(planet, "-> age:", stats["age"], "| weight:", stats["weight"])
    print()


def show_table():
    """Show age, weight, and time for each destination."""
    print("========= All planets for a 20-year-old who weighs 70 =========")
    print("Planet", "Weight", "Age", "Time now", sep="\t")
    for planet in PLANETS:
        weight = weight_on_planet("w", 70, planet)
        age = age_on_planet(20, planet)
        time_now = relative_time(planet)
        print(planet, weight, age, time_now, sep="\t")
    print()


def ask_planet(prompt="Planet: "):
    """Read a destination name and trim surrounding whitespace."""
    return input(prompt).strip()


def ask_number(prompt):
    """Read a number from the user as a float."""
    return float(input(prompt))


def menu():
    """Run the interactive menu until the user quits."""
    while True:
        print("=== Cosmicly ===")
        print("1. My weight on another planet")
        print("2. My age on another planet")
        print("3. What time is it on another planet?")
        print("4. How long to travel there?")
        print("5. Compare two planets")
        print("6. Quit")
        choice = input("Choose 1-6: ").strip()

        try:
            if choice == "1":
                weight = ask_number("Your weight on Earth: ")
                planet = ask_planet()
                print("You would weigh", weight_on_planet("w", weight, planet))
            elif choice == "2":
                age = ask_number("Your age in Earth years: ")
                planet = ask_planet()
                print("You would be", age_on_planet(age, planet), "years old")
            elif choice == "3":
                planet = ask_planet()
                print("The time there is", relative_time(planet))
            elif choice == "4":
                planet = ask_planet()
                print("By car:", drive_to(planet))
                print("By plane:", fly_to(planet))
                print("At light speed:", light_speed_to(planet))
            elif choice == "5":
                planet_a = ask_planet("First planet: ")
                planet_b = ask_planet("Second planet: ")
                birthdate = input("Your birthdate (YYYY-MM-DD): ").strip()
                weight = ask_number("Your weight on Earth: ")
                result = compare_planets(planet_a, planet_b, birthdate, weight)
                for planet, stats in result.items():
                    print(planet, "-> age:", stats["age"], "| weight:", stats["weight"])
            elif choice == "6":
                print("Goodbye, space traveler!")
                break
            else:
                print("Please choose a number from 1 to 6.")
        except ValueError as error:
            print("Error:", error)
        print()


def main():
    """Show the examples and start the interactive menu."""
    show_weight()
    show_age()
    show_time()
    show_travel()
    show_comparison()
    show_table()
    menu()


main()
