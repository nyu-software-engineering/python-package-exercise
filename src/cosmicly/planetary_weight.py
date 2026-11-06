from .data import PLANETS


def weight_on_planet(_type_, value, planet):
    if type(_type_) != str:
       raise TypeError("_type_ must be a string")
    
    if type(planet) != str:
           raise TypeError("planet must be a string")
    _type_ = _type_.lower()
    planet = planet.lower()

    if type(value) != int and type(value) != float:
        raise TypeError("value must be a number")

    if _type_ != "m" and _type_ != "mass" and _type_ != "weight" and _type_ != "w":
       raise ValueError("type must be either mass or weight (m or w)")

    if planet not in PLANETS.keys():
       raise ValueError("No such planet in our solar system")
       
    if value < 0:
       raise ValueError("Neither weight nor mass can be negative")

    if _type_ == "m" or _type_ == "mass":
    
     return round(value * PLANETS[planet]['gravity_m_s2'],2)

    elif _type_ == "w" or _type_ == "weight":
        weight = value / PLANETS['earth']['gravity_m_s2']
        weight = weight * PLANETS[planet]['gravity_m_s2']

        return round (weight,2)

if __name__ == "__main__":
  
    print(weight_on_planet('w',900,'mercury'))
