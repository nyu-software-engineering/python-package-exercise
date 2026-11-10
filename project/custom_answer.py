def custom_answer(answer, category):
    responses = {
        "positive": [],
        "non-committal": [],
        "negative": []
    }
    
    category = category.lower()
    if category in responses:
        responses[category].append(answer)
        print("Answer added!")
    else:
        print("Invalid category")
    return responses

if __name__ == "__main__":
    answer = input("Enter your custom answer: ")
    category = input("Is the answer positive, negative, or non-committal?")
    responses = custom_answer(answer, category)
    print(responses)