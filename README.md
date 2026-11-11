# Python Package Exercise Desktop-Cat


A Python package for creating and interacting with a virtual desktop cat.


## PyPI Package


[PyPi Link](https://pypi.org/project/desktop-cat/)


## Installation and Usage


### Requirements


- Python 3.11 or newer


### Installation


Install the package from PyPI:


```bash
pip install desktop-cat
```


Install with the optional GUI feature:


```bash
pip install "desktop-cat[gui]"
```


The GUI option installs the additional dependencies required for the graphical interface.


### Available Moods, Foods, and Petting Areas


**Moods:**
- Happy
- Sad
- Angry
- Tired
- Hungry
- Annoyed


**Foods:**
- Fish
- Milk
- Kibble
- Canned Food
- Mouse


**Petting Areas:**
- Head
- Back
- Belly
- Tail
- Paws


### Functions


#### `Cat()`


Creates a new desktop cat.


```python
from desktop_cat import Cat


cat = Cat()
```


#### `set_name(name)`


Renames the cat with a limit of 20 characters.


```python
cat.set_name("Whiskers")
```


#### `set_mood(mood)`


Changes the cat's mood to one of the available moods.


```python
cat.set_mood("happy")
```


#### `feed(food)`


Feeds the cat one of the available foods, and returns a reaction. Foods eaten are recorded in foods_eaten, and mood and hunger are updated when the cat is fed.


```python
reaction = cat.feed("fish")


print(reaction)
print(cat.foods_eaten)
```


#### `pet(area, times)`


Pets the cat in an available area. The cat may enjoy it, or get annoyed or angry, depending on how many times it is pet.


```python
cat.pet("head", 3)
```


#### `sleep(hours)`


The cat sleeps for the specified number of hours, reducing sleepiness.


```python
cat.sleep(4)
```


#### `status()`


Returns a string that describes the cat's mood, hunger, sleepiness, times petted, and meals eaten.


```python
print(cat.status())
```


#### `Cat.say(message)`


Prints the message and prints the cat's message.


```python
cat.say("Hello! Nice to meet you!")
```


#### `Window.say(message)`


Displays a textbox above the cat with message text.


```python
from desktop_cat import Window


window = Window()
window.say("Hello! Nice to meet you!")
```


#### `render()`


Returns an ASCII art of the cat based on the cat's mood.


```python
print(cat.render())
```


### Example Program


See the [example Python program](https://github.com/software-students-fall2026/python-package-exercise-busy-bees/blob/16639eacf80e33b3268a9e686cb9f8f151a08131/tests/example_program.py) demonstrating package usage.


## Contributing and Development Setup


Developers who want to contribute to Desktop-Cat can follow these instructions.


### Requirements


- Python 3.11 or newer
- Git
- Pipenv


### Clone the repository


```bash
git clone https://github.com/software-students-fall2026/python-package-exercise-busy-bees
```


### Install Pipenv


```bash
pip install pipenv
```


### Set up the virtual environment


Install all project dependencies:


```bash
pipenv sync --dev
```


### Run tests


Run the tests using pytest:


```bash
pipenv run python -m pytest
```


### Build the package


```bash
pipenv run python -m build
```


### Verify the package build


Verify that the generated files are valid for PyPi:


```bash
pipenv run python -m twine check dist/*
```


## Group Members


- [slvrtngd](https://github.com/slvrtngd)
- [saramhersch](https://github.com/saramhersch)
- [ange285](https://github.com/ange285)
- [Trisolis](https://github.com/Trisolis)
- [aw4580](https://github.com/aw4580)
