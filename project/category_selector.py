import random

def select_category(number):
    numbers = list(range(9))
    random.shuffle(numbers)

    positive = numbers[0:3]
    non_committal = numbers[3:6]
    negative = numbers[6:9]

    if type(number) != int or number < 0 or number > 8:
        return "Invalid number"

    if number in positive:
        return "Positive"
    elif number in non_committal:
        return "Non-Committal"
    elif number in negative:
        return "Negative"
    else:
        return "Invalid number"
    

if __name__ == "__main__":
    number = int(input("Pick a number from 0 to 8 to find out your destiny: "))
    category = select_category(number)
    print("your category is:", category)