
def subject_line(situation, urgency):
    if urgency == 1:
        return f"Quick Question About {situation}"
    elif urgency == 2:
        return f"A Humble Request Regarding {situation}"
    elif urgency == 3:
        return f"URGENT: My Academic Future Depends on {situation}"
    elif urgency == 4:
        return f"FINAL PLEA: I Am Fighting for My Life Over {situation}"
    elif urgency == 5:
        return f"PLEASE READ BEFORE I BECOME A CAMPUS URBAN LEGEND: {situation}"
    else:
        return "Invalid urgency level"

def extension_request(days_late, professor_name):
    if days_late < 0:
        raise ValueError("Days late cannot be negative")

    if not professor_name.strip():
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

def generate_excuse(reason, dramatic_level):
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("Reason cannot be empty")

    if type(dramatic_level) is not int or dramatic_level < 1 or dramatic_level > 5:
        raise ValueError("Dramatic level must be between 1 and 5")

    if dramatic_level == 1:
        return f"I was unable to complete the assignment because {reason}."

    elif dramatic_level == 2:
        return f"Unfortunately, {reason}, which was inconvenient for both me and my GPA."

    elif dramatic_level == 3:
        return f"I had every intention of completing the assignment, but {reason}. I understand this sounds like a personal problem."

    elif dramatic_level == 4:
        return f"I regret to inform you that {reason}. At this point, I am also disappointed in me."

    else:
        return f"Following an internal investigation, I have determined that {reason}. I will be taking full accountability in a future statement."
