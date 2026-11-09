def get_question(question):
    """
    Accept and validate a user's Magic 8 Ball question.
    """
    if not isinstance(question, str):
        raise TypeError("Question must be a string.")

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    return question