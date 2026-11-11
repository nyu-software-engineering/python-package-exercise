![Python Build and Test](https://github.com/software-students-fall2026/python-package-exercise-realesagent/actions/workflows/build.yaml/badge.svg?branch=main)

# Python Package Exercise

## Package Description
As seen on the PyPI website [here](https://pypi.org/project/realesagent/), our package is intended to mimic student and professor email responses in a university class. Specifically, our functions give representative samples of student excuses and apologies based on various personal factors (the student's grade, how professional the student seeks seek to be, etc.), and professor decisions based on their own personal factors (how "sympathetic" they seek to be, etc.).

## Installation
We require Python 3.11 or greater. We do not require any environment or database variables. Install the package using pip: 
```console
pip install realesagent 
```  
Alternatively, if the above fails due to multiple python installations, use `python -m pip install realesagent`.  
To use the package in your program, add the following to your import statements at the top of the program:
```python
import realesagent 
```
As expected, you can also work directly in the interpreter:
```pycon
>>> import realesagent
```

## Usage

Every function can be imported from its module or straight from the package:

```python
from realesagent import excuses            # module style: excuses.generate_excuse(...)
from realesagent import generate_excuse    # direct style: generate_excuse(...)
```

For a program that uses every function, see [demos/example.py](demos/example.py).

---

### Student functions

Measure how desperate a student is, and turn the honest truth into professional language.

#### `student.desperation_level(grade, hours_until_deadline, missing_assignments)`

Calculates a desperation score from 1 (calm) to 10 (panic) based on the student's situation.

- `grade` (int or float, 0–100): the student's current grade. Lower grades raise the score.
- `hours_until_deadline` (int or float): hours until the deadline. 48 or fewer raises the score; 0 or below (already late) raises it most.
- `missing_assignments` (int, 0 or more): number of missing assignments. Each adds 1 point, up to 3.

**Returns:** `int` from 1 to 10.

**Raises:**
- `TypeError` if `grade` or `hours_until_deadline` is not a number, or `missing_assignments` is not an integer.
- `ValueError` if `grade` is outside 0–100, a number is infinite or NaN, or `missing_assignments` is negative.

```pycon
>>> from realesagent import student
>>> student.desperation_level(grade=90, hours_until_deadline=36, missing_assignments=7)
6
```

#### `student.professionalize(truth)`

Rewrites an honest explanation as a formal-sounding one. It recognizes oversleeping, forgetting, procrastinating, internet/Wi-Fi problems, and the dog eating your homework. Anything else gets a generic formal statement.

- `truth` (str): what actually happened. Extra whitespace is ignored.

**Returns:** `str`, the professional version.

**Raises:**
- `TypeError` if `truth` is not a string.
- `ValueError` if `truth` is empty or only whitespace.

```pycon
>>> student.professionalize(truth="My internet connectivity failed and I was too lazy to do anything about it.")
'I experienced an unexpected interruption to my digital connectivity.'
>>> student.professionalize(truth="I was at a concert.")
'I wish to formally report the following circumstance: "I was at a concert.". I respectfully request your consideration while I address this matter.'
```

---

### Excuses functions

Generate excuses, grade requests, and apologies. `generate_excuse` and `grade_beg` pick a message at random, so your output may differ from the examples.

#### `excuses.generate_excuse(assignment)`

Returns a random excuse for not finishing an assignment. Some excuses mention the assignment by name.

- `assignment` (str): the name of the assignment.

**Returns:** `str`, one randomly chosen excuse.

```pycon
>>> from realesagent import excuses
>>> print(excuses.generate_excuse(assignment="Web Development Project"))
I was dealing with a family emergency. The family member was me, and the emergency was Web Development Project.
```

#### `excuses.grade_beg(current_grade, desired_grade, professor_name)`

Writes a complete email asking a professor to raise your grade, with a randomly chosen plea in the middle.

- `current_grade` (int or float): your current grade, shown as a percentage.
- `desired_grade` (int or float): the grade you're hoping for.
- `professor_name` (str): the professor's name for the greeting.

**Returns:** `str`, the full email.

```pycon
>>> email = excuses.grade_beg(current_grade=70, desired_grade=100, professor_name="John Smith")
>>> print(email)
Dear Professor John Smith,

I hope you are doing well. I am writing regarding my current grade of 70%.

I humbly ask that you consider the possibility that my grade is simply a passing grade experiencing a difficult time.

I was hoping you might consider adjusting my grade to 100%. I completely understand if this is not possible, but I figured it was worth one final attempt before I start looking into alternative career paths.

Thank you for your time, patience, and continued tolerance of my academic journey.

Best regards,
A Student Who Is This Close
```

#### `excuses.apology_multiplier(email, desperation)`

Adds an apology to the start of an email. The higher the desperation, the more dramatic the apology.

- `email` (str): any message to put the apology in front of.
- `desperation` (int, 1–10): how intense the apology is. Values below 1 are treated as 1, and above 10 as 10.

**Returns:** `str`, the apology, a blank line, then the original email.

```pycon
>>> print(excuses.apology_multiplier(email="Can I have an extension?", desperation=7))
I sincerely, deeply, emotionally, and spiritually apologize. I have disappointed myself, my family, my ancestors, and possibly the entire academic community.

Can I have an extension?
```

---

### Emails functions

Write subject lines and extension requests whose tone matches how bad the situation is.

#### `emails.subject_line(situation, urgency)`

Creates an email subject line that gets more dramatic as urgency rises.

- `situation` (str): what the email is about.
- `urgency` (int, 1–5): 1 is a casual question, 5 is a full emergency.

**Returns:** `str`, the subject line, or `"Invalid urgency level"` if `urgency` is not 1–5.

```pycon
>>> from realesagent import emails
>>> emails.subject_line(situation="the midterm", urgency=1)
'Quick Question About the midterm'
>>> emails.subject_line(situation="the midterm", urgency=5)
'PLEASE READ BEFORE I BECOME A CAMPUS URBAN LEGEND: the midterm'
```

#### `emails.extension_request(days_late, professor_name)`

Writes an extension request email. The message changes depending on how late the assignment is: on time (0), 1–2 days, 3–5 days, 6–10 days, or more than 10.

- `days_late` (int, 0 or more): how many days past the deadline.
- `professor_name` (str): the professor's name for the greeting.

**Returns:** `str`, the full email.

**Raises:** `ValueError` if `days_late` is negative or `professor_name` is empty.

```pycon
>>> print(emails.extension_request(days_late=3, professor_name="Jacob Williams"))
Dear Professor Jacob Williams,

I realize this assignment was due several days ago. I've spent those days reflecting on my choices rather than making better ones.

Best,
A Student With Excellent Intentions
```

---

### Responses functions

Simulate how a professor might reply to your email.

#### `responses.professor_reply(email, tone="strict")`

Generates a professor's reply that quotes your message and responds in the chosen tone.

- `email` (str): the student's message. Extra whitespace is collapsed.
- `tone` (str, default `"strict"`): one of `"strict"`, `"sympathetic"`, or `"sarcastic"`.

**Returns:** `str`, the professor's reply.

**Raises:**
- `TypeError` if `email` or `tone` is not a string.
- `ValueError` if `email` is empty or `tone` is not one of the three options.

```pycon
>>> from realesagent import responses
>>> informal_email = "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."
>>> print(responses.professor_reply(email=informal_email))
Dear Student,

Regarding your message: "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."

As stated in the syllabus, the course policies still apply.

Best,
Your Fictional Professor
>>> print(responses.professor_reply(email=informal_email, tone="sarcastic"))
Dear Student,

Regarding your message: "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."

A remarkable plot twist. Unfortunately, the syllabus has declined to rewrite itself.

Best,
Your Fictional Professor
```
## Contribute as a Developer

### Prerequisites

- [Python 3.11 or newer](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [pipenv](https://pipenv.pypa.io/), installed with:

```bash
pip install pipenv
```

If `pipenv` isn't recognized afterward (common on Windows), replace `pipenv` with `python -m pipenv` in every command below.

### Set up the project

Clone the repository and move into it:

```bash
git clone https://github.com/software-students-fall2026/python-package-exercise-realesagent.git
cd python-package-exercise-realesagent
```

Create the virtual environment and install all dependencies, including the dev tools (`pytest`, `build`, `twine`):

```bash
pipenv install --dev
```

This also installs `realesagent` itself in editable mode, so changes you make in `src/realesagent/` take effect immediately without reinstalling.

No environment variables, database, or secret configuration files are needed.

### Run the tests

```bash
pipenv run pytest
```

To run a single test file:

```bash
pipenv run pytest tests/test_emails.py
```

### Run the example program

```bash
pipenv run python demos/example.py
```

### Build the package

```bash
pipenv run python -m build
```

This creates a `.whl` and a `.tar.gz` file in the `dist/` folder.

### Contribution workflow

1. Pull the latest `main`:
   ```bash
   git checkout main
   git pull
   ```
2. Create a feature branch:
   ```bash
   git checkout -b your-feature-name
   ```
3. Make your changes, add tests for them, and make sure `pipenv run pytest` passes.
4. Commit and push your branch:
   ```bash
   git add .
   git commit -m "Describe your change"
   git push -u origin your-feature-name
   ```
5. Open a pull request into `main`. **Set the base repository to `software-students-fall2026/python-package-exercise-realesagent`**, not the instructor's original repository.
6. GitHub Actions automatically builds the package and runs the tests on two Python versions. Ask a teammate to review the code and run the tests locally.
7. Once approved and passing, merge the pull request and delete the feature branch.

### Publish a new version (maintainers only)

1. Increase the `version` number in `pyproject.toml`. PyPI rejects versions that already exist.
2. Delete the old `dist/` folder, then rebuild:
   ```bash
   pipenv run python -m build
   ```
3. Upload to PyPI:
   ```bash
   pipenv run twine upload dist/*
   ```
   When prompted, use `__token__` as the username and your PyPI API token as the password.

## Authors
This project was completed by Amitav Narayan ([github](https://github.com/AmitavNarayan)), Nihal Sundari ([github](https://github.com/NISUN05)), Nishika Gorla ([github](https://github.com/nishikagorla)), and Asritha Pannem([github](https://github.com/scanfasri)).