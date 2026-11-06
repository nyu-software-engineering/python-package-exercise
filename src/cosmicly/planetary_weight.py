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



#Think about adding the following
#def draw_moon(radius, phase):
 #   if type(radius) != int:
  #      raise TypeError("radius must be an integer")
   # if type(phase) != int and type(phase) != float:
    #    raise TypeError("phase must be a number")
    #if radius < 2:
     #   raise ValueError("radius must be at least 2")
    #if phase < 0 or phase > 1:
    #    raise ValueError("phase must be between 0 and 1")

    #boundary = 1 - 2 * phase
    #lines = []

    #for row in range(-radius, radius + 1):
    #    line = ""
     #   for col in range(-2 * radius, 2 * radius + 1):
      #      x = col / (2 * radius + 1)
       #     y = row / (radius + 0.5)
        #    if x * x + y * y > 1:
         #       line += " "
          #  elif x >= boundary:
           #     line += "#"
            #else:
            #    line += "."
       # lines.append(line.rstrip())

   # return "\n".join(lines)


#if __name__ == "__main__":
#   print(draw_moon(8, 1))
 #   print()
  #  print(draw_moon(8, 0.5))
