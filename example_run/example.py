#The student functions return a "desperation level" from 1 to 10 based on the student's class information, and also returns a "professional" version of a situation given by the student. For example,
```pycon
 import realesagent
 from realesagent import student
 print(student.desperation_level(grade=90, hours_until_deadline=36, missing_assignments=7))
6
 print(student.professionalize(truth="My internet connectivity failed and I was too lazy to do anything about it."))
I experienced an unexpected interruption to my digital connectivity.
```
You can use the excuses functions to obtain excuse messages, grade request messages, and apology messages as appropriate for your situation. For example,
```pycon
 import realesagent
 from realesagent import excuses
 print(excuses.generate_excuse(assignment="Web Development Project"))
I was dealing with a family emergency. The family member was me, and the emergency was Web Development Project.
 email = excuses.grade_beg(current_grade=70, desired_grade=100, professor_name="John Smith")
 print(email)
Dear Professor John Smith,

I hope you are doing well. I am writing regarding my current grade of 70%.

I humbly ask that you consider the possibility that my grade is simply a passing grade experiencing a difficult time.

I was hoping you might consider adjusting my grade to 100%. I completely understand if this is not possible, but I figured it was worth one final attempt before I start looking into alternative career paths.

Thank you for your time, patience, and continued tolerance of my academic journey.

Best regards,
A Student Who Is This Close
 print(excuses.apology_multiplier(email=email, desperation=7)) # Note that desperation must be from 1 to 10 inclusive, and "email" can be any valid string. 
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
 import realesagent
 from realesagent import emails
 print(emails.subject_line(situation="I left my pencil in the classroom.", urgency=1)) # Urgency must be an integer between 1 and 5, inclusive. 
Quick Question About I left my pencil in the classroom.
 print(emails.extension_request(days_late=3, professor_name="Jacob Williams"))
Dear Professor Jacob Williams,

I realize this assignment was due several days ago. I've spent those days reflecting on my choices rather than making better ones.

Best,
A Student With Excellent Intentions
```
Finally, the responses functions simulate how a professor might respond based on his tone, with the default tone being "strict":
```pycon
 import realesagent
 from realesagent import responses
 informal_email = "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."
 print(responses.professor_reply(email=informal_email)) 
Dear Student,

Regarding your message: "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."

As stated in the syllabus, the course policies still apply.

Best,
Your Fictional Professor
 print(responses.professor_reply(email=informal_email, tone="sympathetic"))
Dear Student,

Regarding your message: "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."

Thank you for explaining. Let's discuss a realistic plan to get you back on track.

Best,
Your Fictional Professor
```
