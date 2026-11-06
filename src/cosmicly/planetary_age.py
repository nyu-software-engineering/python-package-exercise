from .data import PLANETS


def age_on_planet(age, planet):
    if type(age) != int and type(age) != float:
        raise TypeError("age must be a number")

    if type(planet) != str:
        raise TypeError("planet must be a string")

    planet = planet.lower()

    if age < 0:
        raise ValueError("age cannot be negative")

    if planet not in PLANETS:
        raise ValueError("No such planet in our solar system")

    earth_year = PLANETS["earth"]["orbital_period_days"]
    planet_year = PLANETS[planet]["orbital_period_days"]
    planetary_age = age * earth_year / planet_year

    return round(planetary_age, 2)


if __name__ == "__main__":
    print(age_on_planet(20, "mercury"))
