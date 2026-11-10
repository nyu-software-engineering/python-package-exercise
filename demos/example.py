
from realesagent import emails, excuses, responses, student


if __name__=="__main__":
    # The setup: a student has a grade of 90 in a class, with 7 missing assignments and 36 hours until the deadline. The internet
    # connectivity has failed and the student doesn't feel like doing work for the next few days.
    # The student wants to know how "desperate" he/she should be and wants to communicate the problem to the professor.
    desp_level = student.desperation_level(grade=90, hours_until_deadline=36, missing_assignments=7)
    professional_truth = student.professionalize(truth="My internet connectivity failed and I was too lazy to do anything about it.")
    print(f"Desperation level: {desp_level}; Professional Truth: {professional_truth}")

    # The setup: a student has a current grade of 70 and a desired grade of 100 in a class with Professor John Smith. He/she wants to generate
    # an excuse for an upcoming assignment (Web Development Project), along with an email to ask for a better grade. The student also has become desperate, 
    # though not overly so, and wants to obtain an apology to add to the email. The apology and email need not be related in general.
    excuse = excuses.generate_excuse(assignment="Web Development Project")
    email = excuses.grade_beg(current_grade=70, desired_grade=100, professor_name="John Smith")
    apology = excuses.apology_multiplier(email=email, desperation=7)
    print(f"Excuse: {excuse}")
    print(f"Apology for Email: {apology}. Email: {email}")
   
    # The setup: a student has a minor problem and wants to email the professor. He/she later wants to ask the professor, Jacob Williams,
    # for an extension request for an assignment that is three days late.
    print(emails.subject_line(situation="I left my pencil in the classroom.", urgency=1)) 
    print(emails.extension_request(days_late=3, professor_name="Jacob Williams"))

    # The setup: a student informally wants to ask the professor for an improved grade. The professor can respond strictly, sympathetically, or
    # sarcastically (sarcasm not shown below).
    informal_email = "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."
    strict_reply = responses.professor_reply(email=informal_email)
    sympathetic_reply = responses.professor_reply(email=informal_email, tone="sympathetic")
    print(f"Strict reply: {strict_reply}. Sympathetic reply: {sympathetic_reply}.")

    