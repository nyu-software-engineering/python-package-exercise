def custom_answer():
    responses = {
        "positive": [],
        "non-committal": [],
        "negative": []
    }
    answer = input("Enter your custom answer: ")
    category = input("Is the answer positive, negative, or non-committal?").lower()
    if category in responses:
        responses[category].append(answer)
        print("Answer added!")
    else:
        print("Invalid category")
    return responses