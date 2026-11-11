def subject_line(situation, urgency):
    if not isinstance(situation, str) or not situation.strip():
        raise ValueError("Situation must be a non-empty string")

    if type(urgency) is not int or urgency not in range(1, 6):
        return "Invalid urgency level"

    subjects = {
        1: f"Quick Question About {situation}",
        2: f"A Humble Request Regarding {situation}",
        3: f"URGENT: My Academic Future Depends on {situation}",
        4: f"FINAL PLEA: I Am Fighting for My Life Over {situation}",
        5: f"PLEASE READ BEFORE I BECOME A CAMPUS URBAN LEGEND: {situation}",
    }

    return subjects[urgency]


def extension_request(days_late, professor_name):

    if type(days_late) is not int:
        raise TypeError("Days late must be an integer")

    if days_late < 0:
        raise ValueError("Days late cannot be negative")

    if not isinstance(professor_name, str):
        raise TypeError("Professor name must be a string")

    professor_name = professor_name.strip()

    if not professor_name:
        raise ValueError("Professor name cannot be empty")

    if days_late == 0:
        message = "I was wondering if I could have a little extra time on this assignment. I promise I'm almost done."

    elif days_late <= 2:
        message = "I know the deadline has passed, but I was hoping we could both pretend it hasn't for another 24 hours."

    elif days_late <= 5:
        message = "I realize this assignment was due several days ago. I've spent those days reflecting on my choices rather than making better ones."

    elif days_late <= 10:
        message = "I understand this is an unreasonable request, but I was wondering if we could approach the deadline as more of a suggestion."

    else:
        message = "I am aware this assignment was due a concerning amount of time ago. I was hoping enough time had passed for this to feel like a fresh start."

    return f"Dear Professor {professor_name},\n\n{message}\n\nBest,\nA Student With Excellent Intentions"
