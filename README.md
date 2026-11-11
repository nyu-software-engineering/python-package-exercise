[![Python Build and Test](https://github.com/software-students-fall2026/python-package-exercise-realesagent/actions/workflows/build-and-test.yaml/badge.svg?branch=main)](https://github.com/software-students-fall2026/python-package-exercise-realesagent/actions/workflows/build-and-test.yaml)

# Realesagent
A light-hearted Python package that mimics student and professor email responses in a university class. Generate student excuses, apologies, grade requests, and extension emails based on different personal factors, such as grades, deadlines, and desperation levels. You can also simulate professor responses in different tones, including strict, sympathetic, and sarcastic.

PyPI: https://pypi.org/project/realesagent/

## Team members
- [Amitav Narayan](https://github.com/AmitavNarayan)
- [Nihal Sundari](https://github.com/NISUN05)
- [Nishika Gorla](https://github.com/nishikagorla)
- [Asritha Pannem](https://github.com/scanfasri)

## Installation

Requires Python 3.11 or newer.

```bash
pip install realesagent
```

If pip isn't found, use `python -m pip install realesagent`.

Then import it in your own code:

```python
import realesagent
```

You can also import individual modules or functions:

```python
from realesagent import excuses
from realesagent import generate_excuse
```

## Contributing

On Windows, use `python` or `py` in place of `python3`. If pipenv isn't found, run `python -m pipenv`.

Install Python 3.11 or newer from [Python downloads](https://www.python.org/downloads/).

Install Git from [Git downloads](https://git-scm.com/downloads).

Install pipenv from [Pipenv documentation](https://pipenv.pypa.io/):

```bash
pip install pipenv
```

Clone the repository and install the development dependencies:

```bash
git clone https://github.com/software-students-fall2026/python-package-exercise-realesagent.git
cd python-package-exercise-realesagent
pipenv install --dev
pipenv run pytest
pipenv run python -m build
```

This installs the package in editable mode, so changes made in `src/realesagent/` take effect immediately.

To run a single test file:

```bash
pipenv run pytest tests/test_emails.py
```

Every pull request is automatically built and tested using GitHub Actions on two Python versions.

## Example Program

See [examples/demo.py](https://github.com/software-students-fall2026/python-package-exercise-realesagent/blob/main/examples/demo.py), which demonstrates the functions available in the package.

If you cloned the repository, run the example from the repository root:

```bash
pipenv run python demos/example.py
```

## Functions

### Student Functions

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

```python
from realesagent import student

print(student.desperation_level(grade=90, hours_until_deadline=36, missing_assignments=7))
```

Output:

```text
6
```

#### `student.professionalize(truth)`

Rewrites an honest explanation as a formal-sounding one. It recognizes oversleeping, forgetting, procrastinating, internet/Wi-Fi problems, and the dog eating your homework. Anything else gets a generic formal statement.

- `truth` (str): what actually happened. Extra whitespace is ignored.

**Returns:** `str`, the professional version.

**Raises:**
- `TypeError` if `truth` is not a string.
- `ValueError` if `truth` is empty or only whitespace.

```python
from realesagent import student

print(student.professionalize(truth="My internet connectivity failed and I was too lazy to do anything about it."))
print(student.professionalize(truth="I was at a concert."))
```

Output:

```text
I experienced an unexpected interruption to my digital connectivity.
I wish to formally report the following circumstance: "I was at a concert.". I respectfully request your consideration while I address this matter.
```

### Excuses Functions

Generate excuses, grade requests, and apologies. `generate_excuse` and `grade_beg` pick a message at random, so your output may differ from the examples.

#### `excuses.generate_excuse(assignment)`

Returns a random excuse for not finishing an assignment. Some excuses mention the assignment by name.

- `assignment` (str): the name of the assignment.

**Returns:** `str`, one randomly chosen excuse.

```python
from realesagent import excuses

print(excuses.generate_excuse(assignment="Web Development Project"))
```

Output:

```text
I was dealing with a family emergency. The family member was me, and the emergency was Web Development Project.
```

#### `excuses.grade_beg(current_grade, desired_grade, professor_name)`

Writes a complete email asking a professor to raise your grade, with a randomly chosen plea in the middle.

- `current_grade` (int or float): your current grade, shown as a percentage.
- `desired_grade` (int or float): the grade you're hoping for.
- `professor_name` (str): the professor's name for the greeting.

**Returns:** `str`, the full email.

```python
from realesagent import excuses

email = excuses.grade_beg(current_grade=70, desired_grade=100, professor_name="John Smith")
print(email)
```

Output:

```text
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

```python
from realesagent import excuses

print(excuses.apology_multiplier(email="Can I have an extension?", desperation=7))
```

Output:

```text
I sincerely, deeply, emotionally, and spiritually apologize. I have disappointed myself, my family, my ancestors, and possibly the entire academic community.

Can I have an extension?
```

#### `excuses.absence_excuse(class_name)`

Generates a humorous excuse for missing a class.

- `class_name` (str): the name of the class that was missed.

**Returns:** `str`, an apology followed by a randomly selected excuse for the absence.

```python
from realesagent import excuses

print(excuses.absence_excuse("English"))
```

Example output:

```text
I am sorry I missed English. I missed class after losing an argument with my alarm, and unfortunately, it had the stronger case.
```

### Emails Functions

Write subject lines and extension requests whose tone matches how bad the situation is.

#### `emails.subject_line(situation, urgency)`

Creates an email subject line that gets more dramatic as urgency rises.

- `situation` (str): what the email is about.
- `urgency` (int, 1–5): 1 is a casual question, 5 is a full emergency.

**Returns:** `str`, the subject line, or `"Invalid urgency level"` if `urgency` is not 1–5.

```python
from realesagent import emails

print(emails.subject_line(situation="the midterm", urgency=1))
print(emails.subject_line(situation="the midterm", urgency=5))
```

Output:

```text
Quick Question About the midterm
PLEASE READ BEFORE I BECOME A CAMPUS URBAN LEGEND: the midterm
```

#### `emails.extension_request(days_late, professor_name)`

Writes an extension request email. The message changes depending on how late the assignment is: on time (0), 1–2 days, 3–5 days, 6–10 days, or more than 10.

- `days_late` (int, 0 or more): how many days past the deadline.
- `professor_name` (str): the professor's name for the greeting.

**Returns:** `str`, the full email.

**Raises:** `ValueError` if `days_late` is negative or `professor_name` is empty.

```python
from realesagent import emails

print(emails.extension_request(days_late=3, professor_name="Jacob Williams"))
```

Output:

```text
Dear Professor Jacob Williams,

I realize this assignment was due several days ago. I've spent those days reflecting on my choices rather than making better ones.

Best,
A Student With Excellent Intentions
```

### Responses Functions

Simulate how a professor might reply to your email.

#### `responses.professor_reply(email, tone="strict")`

Generates a professor's reply that quotes your message and responds in the chosen tone.

- `email` (str): the student's message. Extra whitespace is collapsed.
- `tone` (str, default `"strict"`): one of `"strict"`, `"sympathetic"`, or `"sarcastic"`.

**Returns:** `str`, the professor's reply.

**Raises:**
- `TypeError` if `email` or `tone` is not a string.
- `ValueError` if `email` is empty or `tone` is not one of the three options.

```python
from realesagent import responses

informal_email = "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."

print(responses.professor_reply(email=informal_email))
print(responses.professor_reply(email=informal_email, tone="sarcastic"))
```

Output:

```text
Dear Student,

Regarding your message: "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."

As stated in the syllabus, the course policies still apply.

Best,
Your Fictional Professor

Dear Student,

Regarding your message: "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."

A remarkable plot twist. Unfortunately, the syllabus has declined to rewrite itself.

Best,
Your Fictional Professor
```

## Valid Options

Desperation levels: 1–10

Urgency levels: 1–5

Professor tones: strict, sympathetic, sarcastic

## Configuration

No environment variables, databases, or secret configuration files are needed.