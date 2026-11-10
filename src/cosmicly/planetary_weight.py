"""Convert a mass or an Earth weight into a weight on another planet."""

from .data import PLANETS


def weight_on_planet(mode, value, planet):
    """Return the weight on the given planet, rounded to two decimal places.

    mode "m"/"mass": value is a mass in kg, the result is in newtons.
    mode "w"/"weight": value is a weight on Earth, the result is in the same unit.

    Raises:
        TypeError: If mode or planet is not a string, or value is not a number.
        ValueError: If mode or planet is unknown, or value is negative.
    """
    if type(mode) != str:
       raise TypeError("_type_ must be a string")
    
    if type(planet) != str:
           raise TypeError("planet must be a string")
    mode = mode.lower()
    planet = planet.lower()

    if type(value) != int and type(value) != float:
        raise TypeError("value must be a number")

    if mode != "m" and mode != "mass" and mode != "weight" and mode != "w":
       raise ValueError("mode must be either mass or weight (m or w)")

    if planet not in PLANETS.keys():
       raise ValueError("No such planet in our solar system")
       
    if value < 0:
       raise ValueError("Neither weight nor mass can be negative")

    if mode == "m" or mode == "mass":
    
     return round(value * PLANETS[planet]['gravity_m_s2'],2)

    elif mode == "w" or mode == "weight":
        weight = value / PLANETS['earth']['gravity_m_s2']
        weight = weight * PLANETS[planet]['gravity_m_s2']

        return round (weight,2)
