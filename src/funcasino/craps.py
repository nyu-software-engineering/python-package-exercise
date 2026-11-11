import random
import sys
import time

dice_art = {
    1: ("┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"),
    2: ("┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"),
    3: ("┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"),
    4: ("┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"),
    5: ("┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"),
    6: ("┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘")
}

def print_dice (dice1, dice2):
    for line in range(5):
        print(dice_art[dice1][line] + "  " + dice_art[dice2][line])


def play_craps(balance):
    print("------ Welcome to CRAPS ------ ")
    while True:
        bet_input = input(f"Enter your Pass Line bet (Current Balance: ${balance}): $").strip()
        try:
            bet = int(bet_input)
            if bet <= 0:
                print("Bet must be greater than $0.")
                continue
            if bet > balance:
                print(f"You don't have enough money! Current balance is ${balance}.")
                continue
            break  
        except ValueError:
            print("Please enter a valid number (e.g., 10).")
    
    input("Press enter to roll your die!")
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    sum1 = dice1+dice2
    
    print_dice(dice1, dice2)
    print (f"Your total is {sum1}")

    #first round of craps, either 2x, 0x, or advance to next phase
    if (sum1) in (7,11):
        return(f"You win! You have won ${bet*2}") 
    elif (dice1+dice2) in (2,3,12):
        return(f"You lose your bet of ${bet}")
    else:
        print (f"Your point is now: {sum1}, try to hit it before rolling a 7" )


    #Second round
    #Player can increase their bet and depending on their sum, different multipliers
    #4 or 10 gives 3x
    #5 or 9 gives 2.5x
    #6 or 8 gives 2.2x

while True:
        input("Press enter to roll again!")
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        sum2 = dice1 + dice2

        print_dice(dice1, dice2)

        if sum1 == sum2:
            balance += bet
            print(f"You got {dice1} and {dice2}, so you WIN! Won ${bet}. New Balance: ${balance}")
            return balance

        if sum2 == 7:
            balance -= bet
            print(f"You got {dice1} and {dice2}, so you LOSE. Lost ${bet}. New Balance: ${balance}")
            return balance

        print(f"You rolled a: {dice1} and {dice2}, not your point: {sum1} or 7, rerolling...\n")

# testing
if __name__ == "__main__":
    print(play_craps(100))


