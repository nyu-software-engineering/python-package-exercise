![Python Build and Test](https://github.com/software-students-fall2026/python-package-exercise-realesagent/actions/workflows/build.yaml/badge.svg?branch=main)

# Python Package Exercise

## Package Description
As seen on the PyPI website [here](https://www.google.com), our package is intended to mimic student and professor email responses in a university class. Specifically, our functions give representative samples of student excuses and apologies based on various personal factors (the student's grade, how professional the student seeks seek to be, etc.), and professor decisions based on their own personal factors (how "sympathetic" they seek to be, etc.).

## Installation and Usage
We require Python 3 or greater. We do not require any environment or database variables. Install the package using pip: 
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
To see how the functions work, you can access an example program [here](example/example.py) and use ' or read more below.
The student functions return a "desperation level" from 1 to 10 based on the student's class information, and also returns a "professional" version of a situation given by the student. For example,
```pycon
>>> import realesagent
>>> from realesagent import student
>>> print(student.desperation_level(grade=90, hours_until_deadline=36, missing_assignments=7))
6
>>> print(student.professionalize(truth="My internet connectivity failed and I was too lazy to do anything about it."))
I experienced an unexpected interruption to my digital connectivity.
```
You can use the excuses functions to obtain excuse messages, grade request messages, and apology messages as appropriate for your situation. For example,
```pycon
>>> import realesagent
>>> from realesagent import excuses
>>> print(excuses.generate_excuse(assignment="Web Development Project"))
I was dealing with a family emergency. The family member was me, and the emergency was Web Development Project.
>>> email = excuses.grade_beg(current_grade=70, desired_grade=100, professor_name="John Smith")
>>> print(email)
Dear Professor John Smith,

I hope you are doing well. I am writing regarding my current grade of 70%.

I humbly ask that you consider the possibility that my grade is simply a passing grade experiencing a difficult time.

I was hoping you might consider adjusting my grade to 100%. I completely understand if this is not possible, but I figured it was worth one final attempt before I start looking into alternative career paths.

Thank you for your time, patience, and continued tolerance of my academic journey.

Best regards,
A Student Who Is This Close
>>> print(excuses.apology_multiplier(email=email, desperation=7)) # Note that desperation must be from 1 to 10 inclusive, and "email" can be any valid string. 
I sincerely, deeply, emotionally, and spiritually apologize. I have disappointed myself, my family, my ancestors, and possibly the entire academic community.

Dear Professor John Smith,

I hope you are doing well. I am writing regarding my current grade of 70%.

I have spent considerable time reflecting on my grade, and I believe we have both suffered enough.

I was hoping you might consider adjusting my grade to 100%. I completely understand if this is not possible, but I figured it was worth one final attempt before I start looking into alternative career paths.

Thank you for your time, patience, and continued tolerance of my academic journey.

Best regards,
A Student Who Is This Close
```
The emails functions return messages that the student can send to the professor based on the urgency and days late of the situation. For example,
```pycon
>>> import realesagent
>>> from realesagent import emails
>>> print(emails.subject_line(situation="I left my pencil in the classroom.", urgency=1)) # Urgency must be an integer between 1 and 5, inclusive. 
Quick Question About I left my pencil in the classroom.
>>> print(emails.extension_request(days_late=3, professor_name="Jacob Williams"))
Dear Professor Jacob Williams,

I realize this assignment was due several days ago. I've spent those days reflecting on my choices rather than making better ones.

Best,
A Student With Excellent Intentions
```
Finally, the responses functions simulate how a professor might respond based on his tone, with the default tone being "strict":
```pycon
>>> import realesagent
>>> from realesagent import responses
>>> informal_email = "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."
>>> print(responses.professor_reply(email=informal_email)) 
Dear Student,

Regarding your message: "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."

As stated in the syllabus, the course policies still apply.

Best,
Your Fictional Professor
>>> print(responses.professor_reply(email=informal_email, tone="sympathetic"))
Dear Student,

Regarding your message: "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."

Thank you for explaining. Let's discuss a realistic plan to get you back on track.

Best,
Your Fictional Professor
```

## Contribute as a Developer


## Authors
This project was completed by Amitav Narayan ([github](https://github.com/AmitavNarayan)), Nihal Sundari ([github](https://github.com/NISUN05)), Nishika Gorla ([github](https://github.com/nishikagorla)), and Asritha Pannem([github](https://github.com/scanfasri)). 


Replace the contents of the [README.md](./README.md) file with a beautifully-formatted Markdown file including


- how a developer who wants to contribute to your project can set up the virtual environment, install dependencies, and build and test your package for themselves.
- instructions for how to configure and run all parts of your project for any developer on any platform - these instructions must work!
- instructions for how to set up any environment variables and import any starter data into the database, as necessary, for the system to operate correctly when run.
- if there are any "secret" configuration files, such as `.env` or similar files, that are not included in the version control repository, examples of these files, such as `env.example`, with dummy data must be included in the repository and exact instructions for how to create the proper configuration files and what their contents should be must be supplied to the course admins by the due date.