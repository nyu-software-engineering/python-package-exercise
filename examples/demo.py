from realesagent import emails, excuses, responses, student


def section(title):
    print(f"\n===== {title} =====\n")


if __name__ == "__main__":
    # Student: grade 90, 7 missing assignments, deadline in 36 hours, internet "failed"
    section("Student")
    print("Desperation level:", student.desperation_level(grade=90, hours_until_deadline=36, missing_assignments=7))
    print("Already late:", student.desperation_level(grade=40, hours_until_deadline=0, missing_assignments=2))
    print(student.professionalize(truth="My internet connectivity failed and I was too lazy to do anything about it."))
    print(student.professionalize(truth="I overslept."))

    # Excuses: excuse for a project, grade-begging email, then an apology on top
    section("Excuses")
    print(excuses.generate_excuse(assignment="Web Development Project"))
    email = excuses.grade_beg(current_grade=70, desired_grade=100, professor_name="John Smith")
    print("\n--- Grade request ---\n" + email)
    print("\n--- With apology (desperation 7) ---\n" + excuses.apology_multiplier(email=email, desperation=7))

    # Emails: subject lines at every urgency, extension requests at different lateness
    section("Emails")
    for urgency in range(1, 6):
        print(emails.subject_line(situation="the midterm", urgency=urgency))
    print()
    print(emails.extension_request(days_late=0, professor_name="Jacob Williams"))
    print()
    print(emails.extension_request(days_late=3, professor_name="Jacob Williams"))

    # Responses: same informal email, every tone
    section("Professor replies")
    informal_email = "Yo prof, I have a C rn but I need an A to graduate. Can you help a brother out. Thanks man."
    for tone in ("strict", "sympathetic", "sarcastic"):
        print(f"--- {tone} ---")
        print(responses.professor_reply(email=informal_email, tone=tone))
        print()