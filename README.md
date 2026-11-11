# Cosmicly

![Tests](https://github.com/software-students-fall2026/python-package-exercise-LCDJ/actions/workflows/tests.yml/badge.svg?event=pull_request)

**Cosmicly** is a Python package that answers the important questions in life:

- How much would I weigh on Jupiter?
- How old would I be on Mercury?
- What time is it on Mars right now?
- How long would it take to *drive* to Neptune?

It uses real planetary data, so the numbers are (mostly) real, even if the questions are strange.


Find out how old you would be on Mars, how much you would weigh on the Moon, or how long it would take to fly to Jupiter at airplane speed. **cosmicly** is a Python package that uses orbital periods, gravity, and solar day lengths to explore the eight planets and Earth's Moon.

## Install from source

You need Python 3.11 or newer and [Pipenv](https://pipenv.pypa.io/). Run these commands in a terminal:

```bash
git clone https://github.com/software-students-fall2026/python-package-exercise-LCDJ.git
cd python-package-exercise-LCDJ
pipenv install --dev
pipenv run python -m pip install -e .
```

The editable install lets Python import `cosmicly` from `src` and pick up your changes immediately. The package includes its planetary data and needs no environment variables or database.

The distribution is named `cosmicly`. Use the source installation above until a release is available. [PyPI project page](https://pypi.org/project/cosmicly/)

## Use cosmicly

Save these examples in a Python file and run it with `pipenv run python your_script.py`. For an interactive tour of the package, run the included [example program](example.py):

```bash
pipenv run python example.py
```

### Age and weight

`age_on_planet` converts Earth years to years on the destination using its orbital period. `earth_age` calculates your age in Earth years from a birthdate. `weight_on_planet` scales an Earth weight in `"w"` mode and calculates weight in newtons from a mass in kilograms in `"m"` mode.

```python
from cosmicly import age_on_planet, earth_age
from cosmicly.planetary_weight import weight_on_planet

print(age_on_planet(20, "mercury"))            # 83.0 Mercury years
print(earth_age("2000-01-01"))                 # Age in Earth years as of today
print(weight_on_planet("w", 70, "mars"))       # 26.43 in the input weight unit
print(weight_on_planet("m", 70, "moon"))       # 112.0 newtons
```

### Planetary clocks and comparisons

`relative_time` returns an `HH:MM:SS` reading on a simulated planetary clock. It starts the Earth and destination clocks together at midnight and uses the destination's solar day length. Pass a `datetime` for a fixed reference reading or omit it to use the current local time. `compare_planets` returns your age and weight on two different destinations as a dictionary.

```python
from datetime import datetime

from cosmicly import compare_planets, relative_time

print(relative_time("mars"))                             # Simulated time now
print(relative_time("mars", datetime(2026, 1, 1, 12)))     # 11:40:44

comparison = compare_planets("mars", "jupiter", "2000-01-01", 70)
print(comparison["mars"]["age"])
print(comparison["jupiter"]["weight"])
```

### Travel from Earth

`distance_from_earth` estimates distance from the difference in the planets' distances from the Sun and uses a fixed distance for the Moon. `travel_at_speed` estimates travel time at a constant speed in km/h. The car, plane, and light-speed shortcuts use preset speeds, and `format_duration` converts seconds to a readable duration.

```python
from cosmicly.planetary_travel import (
    distance_from_earth,
    drive_to,
    fly_to,
    format_duration,
    light_speed_to,
    travel_at_speed,
)

print(distance_from_earth("moon"))            # 384400 km
print(travel_at_speed("mars", 40_000))         # Travel time at 40,000 km/h
print(drive_to("mars"))                       # 89 years at 100 km/h
print(fly_to("moon"))                        # 18 days at 900 km/h
print(light_speed_to("mars"))                 # 4 minutes
print(format_duration(3600))                  # 1 hour
```

## Build and test

Run these commands from the repository root after installing the development dependencies:

```bash
pipenv run python -m build
pipenv run python -m pytest
pipenv run python -m pytest --cov=cosmicly --cov-report=term-missing
```

The build writes a wheel and a source archive to `dist/`. The tests live in [`tests/`](tests/). GitHub Actions builds the package and runs the tests on pull requests targeting `main`. [Tests workflow](.github/workflows/tests.yml)

## Team

- [Carina Ilie](https://github.com/carinutza)
- [Abubakar Diallo](https://github.com/Dialloni)
- [Julian  Leitersdorf](https://github.com/Jrleitersdorf)
- [Leonid (Leo) Gurevich](https://github.com/Leonid2004)

## Data sources

The package stores orbital periods, gravity, distances from the Sun, and solar day lengths in [`data.py`](src/cosmicly/data.py). [NASA Planetary Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/) · [NASA Mars24](https://www.giss.nasa.gov/tools/mars24/help/notes.html)