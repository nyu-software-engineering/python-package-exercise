def professor_reply(email, tone="strict"):
   
    if not isinstance(email, str):
        raise TypeError("email must be a string")
    if not isinstance(tone, str):
        raise TypeError("tone must be a string")
    email = " ".join(email.split())
    if not email:
        raise ValueError("email cannot be empty")

    replies = {
        "strict": "As stated in the syllabus, the course policies still apply.",
        "sympathetic": (
            "Thank you for explaining. Let's discuss a realistic plan to get you back on track."
        ),
        "sarcastic": (
            "A remarkable plot twist. Unfortunately, the syllabus has declined to rewrite itself."
        ),
    }
    if tone not in replies:
        raise ValueError("tone must be strict, sympathetic, or sarcastic")

    return (
        f'Dear Student,\n\nRegarding your message: "{email}"\n\n'
        f"{replies[tone]}\n\nBest,\nYour Fictional Professor"
    )
