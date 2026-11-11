
import random

def generate_excuse(assignment):
    excuses = [
        "My laptop broke down from the academic pressure. Honestly, I think we both need an extension.",

        f"The internet stopped working right when I was about to submit {assignment}. I believe this was a targeted attack.",

        f"I was dealing with a family emergency. The family member was me, and the emergency was {assignment}.",

        f"I spent so long mentally preparing to complete {assignment} that I ran out of time to actually complete it.",

        "I accidentally took a nap that was supposed to last 20 minutes. I woke up in a different academic semester.",

        "I was experiencing technical difficulties, emotional difficulties, and difficulties identifying what day it was.",

        f"My dog ate {assignment}, but in his defense, he has always been more interested in academics than I am."
    ]

    return random.choice(excuses) + f" Unfortunately, I couldn't submit {assignment}."


def grade_beg(current_grade, desired_grade, professor_name):
    messages = [
        "I would like to respectfully ask if my grade could be viewed through a more generous mathematical interpretation.",

        "I understand that grades are earned, not given, but I was hoping we could explore a small academic miracle.",

        "I have spent considerable time reflecting on my grade, and I believe we have both suffered enough.",

        "I humbly ask that you consider the possibility that my grade is simply a passing grade experiencing a difficult time.",

        "I would be eternally grateful if you could find it in your heart, and potentially your gradebook, to help me out."
    ]

    message = random.choice(messages)

    email = (
        f"Dear Professor {professor_name},\n\n"
        f"I hope you are doing well. I am writing regarding my current "
        f"grade of {current_grade}%.\n\n"
        f"{message}\n\n"
        f"I was hoping you might consider adjusting my grade to "
        f"{desired_grade}%. I completely understand if this is not "
        f"possible, but I figured it was worth one final attempt "
        f"before I start looking into alternative career paths.\n\n"
        f"Thank you for your time, patience, and continued tolerance "
        f"of my academic journey.\n\n"
        f"Best regards,\n"
        f"A Student Who Is This Close"
    )

    return email


def apology_multiplier(email, desperation):
    apologies = [
        "I sincerely apologize for the inconvenience and take full responsibility for my actions. I assure you this will not happen again.",

        "I deeply regret this unfortunate situation and apologize for the unnecessary chaos I have brought into your inbox.",

        "I am profoundly, immeasurably, and astronomically sorry. Words cannot express the depth of my regret, although I am clearly going to try.",

        "I sincerely, deeply, emotionally, and spiritually apologize. I have disappointed myself, my family, my ancestors, and possibly the entire academic community.",

        "I BEG FOR YOUR FORGIVENESS. I have never been more humbled in my entire existence. I am prepared to turn my academic career around and name my firstborn after you."
    ]

    desperation = max(1, min(10, desperation))

    apology = apologies[(desperation - 1) // 2]

    return apology + "\n\n" + email


def absence_excuse(class_name):
    if not isinstance(class_name, str):
        raise TypeError("Class name must be a string")

    class_name = class_name.strip()

    if not class_name:
        raise ValueError("Class name cannot be empty")
    
    absence_excuses = [
         "I meant to come to class, but my morning unraveled before I could pull it back together.",

         "I woke up convinced I still had time, which was honestly the most confident mistake I made all day.",
         
         "I was ready to leave, but the quiet of my room became strangely difficult to walk away from.",
         
         "I missed class after losing an argument with my alarm, and unfortunately, it had the stronger case.",

         "I had every intention of showing up, but the morning moved faster than I did.",

         "I stayed home because I needed a moment to collect myself, and that moment became the entire class period.",

         "I was not absent by choice; I was simply overwhelmed by the very ordinary tragedy of getting out the door."
    ]

    excuse = random.choice(absence_excuses)
    return f"I am sorry I missed {class_name}. {excuse}"

if __name__=="__main__":
    email = grade_beg(current_grade=70, desired_grade=100, professor_name="John Smith")
    print(apology_multiplier(email, 7))
