import random

from project.magic8ball import (

    get_question,
    select_category,
    get_response,
    custom_answer,
    normalize_category,
)

def main():
    print(r"""
              ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⣿⣿⡿⠟⣉⣡⣤⣴⣶⣶⣶⣶⣦⣤⣌⣉⠻⢿⣿⣿⣿⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⠟⢁⣴⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡈⠻⣿⣿⣿⣿⣿
              ⣿⣿⣿⡿⢁⣴⡟⠁⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡈⢿⣿⣿⣿
              ⣿⣿⡟⢡⣿⠏⠀⠀⢠⣿⣿⣿⣿⣿⣿⠟⠋⠁⠀⠀⠉⠙⠻⣿⣿⣿⡌⢻⣿⣿
              ⣿⣿⠁⣾⠏⠀⠀⣰⣿⣿⣿⣿⣿⡿⠁⠀⠀⢠⡤⠤⣤⠀⠀⠘⢿⣿⣷⠈⣿⣿
              ⣿⡇⢰⣿⠀⠀⢰⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠸⣄⣀⣟⠀⠀⠀⠘⣿⣿⡆⢸⣿
              ⣿⡇⢸⣿⠀⢠⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⢠⡏⠀⠈⣷⠀⠀⢠⣿⣿⡇⢸⣿
              ⣿⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠻⠶⠞⠃⠀⢀⣾⣿⣿⠇⢸⣿
              ⣿⣿⡀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⡀⠀⠀⢀⣠⣴⣿⣿⣿⡿⢀⣿⣿
              ⣿⣿⣧⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⣼⣿⣿
              ⣿⣿⣿⣷⡈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢁⣾⣿⣿⣿
              ⣿⣿⣿⣿⣿⣦⡈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢁⣴⣿⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⣿⣿⣷⣦⣉⡙⠛⠻⠿⠿⠿⠿⠟⠛⢋⣉⣴⣾⣿⣿⣿⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿""")

    question = get_question("Will I pass my exam?")
    print("\nQuestion:", question)

    number = random.randint(0, 8)
    category = select_category(number)
    print("Category:", category)

    response = get_response(category)
    print("Magic 8 Ball says:", response)

    custom = custom_answer(
        "Absolutely!",
        "positive"
    )
    print("\nCustom answers:", custom)

    response = get_response(
        "positive",
        custom_answers=custom
    )
    print("Custom response:", response)

    normalized = normalize_category("Non Committal")
    print("\nNormalized category:", normalized)

if __name__ == "__main__":
    main()