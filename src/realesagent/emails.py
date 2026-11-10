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
